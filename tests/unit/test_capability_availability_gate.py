"""Tests unitaires du gate de disponibilité des capacités.

Les tuples d'entrée sont synthétiques (TEST) : ils n'attestent pas la
conformité réelle de ``compose``, couverte par la suite d'intégration.
"""

import unittest
from dataclasses import replace

from pixs.kernel.capabilities import CapabilityDescriptor
from pixs.kernel.composition import CompositionResult
from pixs.kernel.lifecycle.availability import (
    CapabilityFallback,
    CapabilityObservation,
    CapabilityState,
    ConsumedCapabilityState,
    STATE_AVAILABLE,
    STATE_BLOCKED,
    STATE_DECLARED,
    STATE_DEGRADED,
    STATE_DISABLED,
    STATE_RESOLVED,
    compute_capability_availability,
    run_gated_hooks,
)
from pixs.kernel.lifecycle.hooks import HookCall
from pixs.kernel.manifest.models import ComponentManifest, ProvidedCapability


def _manifest(component_id, entries=(), optional=False):
    section = (
        {"dependency_capabilities": entries}
        if not optional
        else {"optional_dependency_capabilities": entries}
    )
    provided = (
        (ProvidedCapability(id="cap.alpha", version="1.0.0"),)
        if component_id == "alpha"
        else ()
    )
    return ComponentManifest(
        schema_version="1",
        id=component_id,
        type="MODULE",
        version="1.0.0",
        provided_capabilities=provided,
        **section,
    )


def _base(required=True, provider_ref="alpha"):
    manifests = (
        _manifest("alpha"),
        _manifest("beta", ("cap.alpha",), optional=not required),
    )
    descriptor = CapabilityDescriptor(
        capability_id="cap.alpha",
        capability_version="1.0.0",
        owner_component="alpha",
        contract_refs=(),
        provider_ref=provider_ref,
        criticality="REQUIRED",
        fallback="none",
    )
    composition = CompositionResult(
        stage="activated",
        activated=True,
        order=("alpha", "beta"),
        edges=(("beta", "alpha"),),
        diagnostics=(),
        capability_descriptors=(descriptor,),
    )
    return composition, manifests


def _observation(operable=True, version="1.0.0", provider="alpha"):
    return CapabilityObservation(
        capability_id="cap.alpha",
        capability_version=version,
        provider_id=provider,
        operable=operable,
    )


class TestDescriptorStatePrecedence(unittest.TestCase):
    def test_available(self):
        composition, manifests = _base()
        caps, _, _, _ = compute_capability_availability(
            composition, manifests, (_observation(),)
        )
        self.assertEqual(
            caps, (CapabilityState("cap.alpha", "1.0.0", "alpha", STATE_AVAILABLE),)
        )

    def test_blocked(self):
        composition, manifests = _base()
        caps, _, _, _ = compute_capability_availability(
            composition, manifests, (_observation(operable=False),)
        )
        self.assertEqual(caps[0].state, STATE_BLOCKED)

    def test_resolved(self):
        composition, manifests = _base()
        caps, _, _, _ = compute_capability_availability(
            composition, manifests, ()
        )
        self.assertEqual(caps[0].state, STATE_RESOLVED)

    def test_declared(self):
        composition, manifests = _base(provider_ref=None)
        caps, _, _, _ = compute_capability_availability(
            composition, manifests, ()
        )
        self.assertEqual(caps[0].state, STATE_DECLARED)

    def test_disabled_overrides(self):
        composition, manifests = _base()
        caps, _, _, _ = compute_capability_availability(
            composition, manifests, (_observation(),),
            disabled_capabilities=("cap.alpha",),
        )
        self.assertEqual(caps[0].state, STATE_DISABLED)


class TestConsumedCapabilityStates(unittest.TestCase):
    def test_required_available(self):
        composition, manifests = _base()
        _, cons, fatals, warnings = compute_capability_availability(
            composition, manifests, (_observation(),)
        )
        self.assertEqual(fatals, ())
        self.assertEqual(warnings, ())
        self.assertEqual(
            cons,
            (
                ConsumedCapabilityState(
                    consumer_id="beta",
                    capability_id="cap.alpha",
                    provider_id="alpha",
                    capability_version="1.0.0",
                    state=STATE_AVAILABLE,
                    fallback=None,
                ),
            ),
        )

    def test_optional_missing_with_declared_fallback(self):
        composition, manifests = _base(required=False, provider_ref=None)
        _, cons, fatals, warnings = compute_capability_availability(
            composition, manifests, (),
            optional_fallbacks=(CapabilityFallback("cap.alpha", "repli"),),
        )
        self.assertEqual(fatals, ())
        self.assertEqual(len(warnings), 1)
        self.assertEqual(cons[0].state, STATE_DEGRADED)
        self.assertEqual(cons[0].fallback, "repli")
        self.assertIsNone(cons[0].provider_id)

    def test_optional_missing_without_fallback_refused(self):
        composition, manifests = _base(required=False)
        _, cons, fatals, _ = compute_capability_availability(
            composition, manifests, ()
        )
        self.assertEqual(cons[0].state, STATE_BLOCKED)
        self.assertEqual(len(fatals), 1)

    def test_required_without_observation_blocked(self):
        composition, manifests = _base()
        _, cons, fatals, _ = compute_capability_availability(
            composition, manifests, ()
        )
        self.assertEqual(cons[0].state, STATE_BLOCKED)
        self.assertEqual(cons[0].provider_id, "alpha")
        self.assertEqual(len(fatals), 1)

    def test_required_disabled_blocked(self):
        composition, manifests = _base()
        _, cons, fatals, _ = compute_capability_availability(
            composition, manifests, (_observation(),),
            disabled_capabilities=("cap.alpha",),
        )
        self.assertEqual(cons[0].state, STATE_BLOCKED)
        self.assertEqual(len(fatals), 1)

    def test_optional_available_without_fallback(self):
        composition, manifests = _base(required=False)
        _, cons, fatals, warnings = compute_capability_availability(
            composition, manifests, (_observation(),)
        )
        self.assertEqual(fatals, ())
        self.assertEqual(warnings, ())
        self.assertEqual(cons[0].state, STATE_AVAILABLE)
        self.assertIsNone(cons[0].fallback)

    def test_optional_blocked_with_fallback(self):
        composition, manifests = _base(required=False)
        _, cons, fatals, warnings = compute_capability_availability(
            composition, manifests, (_observation(operable=False),),
            optional_fallbacks=(CapabilityFallback("cap.alpha", "repli"),),
        )
        self.assertEqual(fatals, ())
        self.assertEqual(len(warnings), 1)
        self.assertEqual(cons[0].state, STATE_DEGRADED)
        self.assertEqual(cons[0].fallback, "repli")


def _node(component_id, capability_id=None, version="1.0.0", entries=(), optional=False):
    section = (
        {"dependency_capabilities": entries}
        if not optional
        else {"optional_dependency_capabilities": entries}
    )
    return ComponentManifest(
        schema_version="1",
        id=component_id,
        type="MODULE",
        version="1.0.0",
        provided_capabilities=(
            (ProvidedCapability(id=capability_id, version=version),)
            if capability_id is not None
            else ()
        ),
        **section,
    )


def _descriptor_of(capability_id, version, owner, provider_ref=None):
    return CapabilityDescriptor(
        capability_id=capability_id,
        capability_version=version,
        owner_component=owner,
        contract_refs=(),
        provider_ref=provider_ref,
        criticality="REQUIRED",
        fallback="none",
    )


def _composition_of(manifests, descriptors, edges):
    return CompositionResult(
        stage="activated",
        activated=True,
        order=tuple(sorted(m.id for m in manifests)),
        edges=edges,
        diagnostics=(),
        capability_descriptors=descriptors,
    )


class TestFactAssociation(unittest.TestCase):
    def test_edges_for_other_targets_not_ambiguous(self):
        manifests = (
            _node("alpha", "cap.alpha"),
            _node("gamma", "cap.other"),
            _node("beta", entries=("cap.alpha",)),
        )
        descriptors = (
            _descriptor_of("cap.alpha", "1.0.0", "alpha", "alpha"),
            _descriptor_of("cap.other", "1.0.0", "gamma", "gamma"),
        )
        composition = _composition_of(
            manifests, descriptors, (("beta", "alpha"), ("beta", "gamma"))
        )
        caps, cons, fatals, _ = compute_capability_availability(
            composition, manifests, (_observation(),)
        )
        self.assertEqual(fatals, ())
        self.assertEqual(len(cons), 1)
        self.assertEqual(cons[0].consumer_id, "beta")
        self.assertEqual(cons[0].state, STATE_AVAILABLE)

    def test_two_consumers_disjoint_versions(self):
        manifests = (
            _node("alpha", "cap.alpha"),
            _node("gamma", "cap.alpha", "2.0.0"),
            _node("beta", entries=("cap.alpha >=1.0.0 <2.0.0",)),
            _node("delta", entries=("cap.alpha >=2.0.0",)),
        )
        descriptors = (
            _descriptor_of("cap.alpha", "1.0.0", "alpha", "alpha"),
            _descriptor_of("cap.alpha", "2.0.0", "gamma", "gamma"),
        )
        composition = _composition_of(
            manifests,
            descriptors,
            (
                ("beta", "alpha"),
                ("beta", "gamma"),
                ("delta", "alpha"),
                ("delta", "gamma"),
            ),
        )
        _, cons, fatals, _ = compute_capability_availability(
            composition, manifests, (_observation(),)
        )
        by_consumer = {record.consumer_id: record for record in cons}
        self.assertEqual(by_consumer["beta"].state, STATE_AVAILABLE)
        self.assertEqual(by_consumer["delta"].state, STATE_BLOCKED)
        self.assertEqual(len(fatals), 1)

    def test_optional_incompatible_with_fallback(self):
        manifests = (
            _node("alpha", "cap.alpha"),
            _node("beta", entries=("cap.alpha >=3.0.0",), optional=True),
        )
        descriptors = (_descriptor_of("cap.alpha", "1.0.0", "alpha", "alpha"),)
        composition = _composition_of(manifests, descriptors, (("beta", "alpha"),))
        _, cons, fatals, warnings = compute_capability_availability(
            composition, manifests, (),
            optional_fallbacks=(CapabilityFallback("cap.alpha", "repli"),),
        )
        self.assertEqual(fatals, ())
        self.assertEqual(len(warnings), 1)
        self.assertEqual(cons[0].state, STATE_DEGRADED)
        self.assertIsNone(cons[0].provider_id)
        self.assertEqual(cons[0].fallback, "repli")

    def test_ambiguous_compatible_facts_fatal(self):
        manifests = (
            _node("alpha", "cap.alpha"),
            _node("gamma", "cap.alpha", "2.0.0"),
            _node("beta", entries=("cap.alpha",)),
        )
        descriptors = (
            _descriptor_of("cap.alpha", "1.0.0", "alpha", "alpha"),
            _descriptor_of("cap.alpha", "2.0.0", "gamma", "gamma"),
        )
        composition = _composition_of(
            manifests, descriptors, (("beta", "alpha"), ("beta", "gamma"))
        )
        _, cons, fatals, _ = compute_capability_availability(
            composition, manifests, ()
        )
        self.assertEqual(cons[0].state, STATE_BLOCKED)
        self.assertIsNone(cons[0].provider_id)
        self.assertEqual(len(fatals), 1)


class TestGatedWrapper(unittest.TestCase):
    def test_callbacks_executed_on_available(self):
        composition, manifests = _base()
        counter = []
        hooks = {"alpha": {"install": lambda: counter.append(1)}}
        result = run_gated_hooks(composition, manifests, hooks, (_observation(),))
        self.assertEqual(result.calls, (HookCall("alpha", "install"),))
        self.assertEqual(counter, [1])

    def test_callbacks_executed_on_warnings_only(self):
        composition, manifests = _base(required=False, provider_ref=None)
        counter = []
        hooks = {"alpha": {"install": lambda: counter.append(1)}}
        result = run_gated_hooks(
            composition, manifests, hooks, (),
            optional_fallbacks=(CapabilityFallback("cap.alpha", "repli"),),
        )
        self.assertEqual(result.diagnostics, ())
        self.assertEqual(len(result.warnings), 1)
        self.assertEqual(counter, [1])

    def test_zero_callbacks_on_required_refusals(self):
        cases = (
            (_base(), (), ()),
            (_base(), (_observation(operable=False),), ()),
            (_base(), (_observation(),), ("cap.alpha",)),
        )
        for (composition, manifests), observations, disabled in cases:
            counter = []
            hooks = {"alpha": {"install": lambda: counter.append(1)}}
            result = run_gated_hooks(
                composition, manifests, hooks, observations,
                disabled_capabilities=disabled,
            )
            self.assertEqual(result.calls, ())
            self.assertEqual(counter, [])

    def test_callback_exception_propagates(self):
        composition, manifests = _base()
        counter = []

        def raising():
            raise RuntimeError

        hooks = {
            "alpha": {"install": lambda: counter.append(1)},
            "beta": {"start": raising},
        }
        with self.assertRaises(RuntimeError):
            run_gated_hooks(composition, manifests, hooks, (_observation(),))
        self.assertEqual(counter, [1])

    def test_mixed_required_fatal_optional_warning(self):
        beta = replace(
            _node("beta", entries=("cap.alpha",)),
            optional_dependency_capabilities=("cap.other >=3.0.0",),
        )
        manifests = (_node("alpha", "cap.alpha"), _node("gamma", "cap.other"), beta)
        descriptors = (
            _descriptor_of("cap.alpha", "1.0.0", "alpha", "alpha"),
            _descriptor_of("cap.other", "1.0.0", "gamma", "gamma"),
        )
        composition = _composition_of(
            manifests, descriptors, (("beta", "alpha"), ("beta", "gamma"))
        )
        counter = []
        hooks = {"alpha": {"install": lambda: counter.append(1)}}
        result = run_gated_hooks(
            composition, manifests, hooks, (),
            optional_fallbacks=(CapabilityFallback("cap.other", "repli"),),
        )
        self.assertEqual(result.calls, ())
        self.assertEqual(counter, [])
        self.assertEqual(len(result.diagnostics), 1)
        self.assertEqual(len(result.warnings), 1)
        self.assertEqual(
            [record.state for record in result.consumed_states],
            [STATE_BLOCKED, STATE_DEGRADED],
        )


class TestCoherenceRefusals(unittest.TestCase):
    def test_hooks_malformed_refused(self):
        composition, manifests = _base()
        for hooks in ("hooks", {1: {}}, {"alpha": []}):
            result = run_gated_hooks(composition, manifests, hooks, ())
            self.assertEqual(result.calls, ())
            self.assertEqual(result.capability_states, ())
            self.assertEqual(result.consumed_states, ())
            self.assertEqual(len(result.diagnostics), 1)

    def test_hooks_unknown_component_refused(self):
        composition, manifests = _base()
        counter = []
        hooks = {"unknown": {"install": lambda: counter.append(1)}}
        result = run_gated_hooks(composition, manifests, hooks, (_observation(),))
        self.assertEqual(result.calls, ())
        self.assertEqual(counter, [])
        self.assertEqual(len(result.diagnostics), 1)

    def test_observation_incoherent_refused(self):
        composition, manifests = _base()
        for observation in (
            _observation(provider="gamma"), _observation(version="2.0.0")
        ):
            caps, cons, fatals, _ = compute_capability_availability(
                composition, manifests, (observation,)
            )
            self.assertTrue(any("observation" in d.constraint for d in fatals))
            self.assertEqual(caps[0].state, STATE_RESOLVED)
            self.assertEqual(cons[0].state, STATE_BLOCKED)

    def test_observation_duplicate_refused(self):
        composition, manifests = _base()
        caps, _, fatals, _ = compute_capability_availability(
            composition, manifests, (_observation(), _observation())
        )
        self.assertTrue(any("observation" in d.constraint for d in fatals))
        self.assertEqual(caps[0].state, STATE_RESOLVED)

    def test_descriptors_duplicate_refused(self):
        composition, manifests = _base()
        duplicated = replace(
            composition,
            capability_descriptors=composition.capability_descriptors * 2,
        )
        caps, cons, fatals, _ = compute_capability_availability(duplicated, manifests, ())
        self.assertEqual(caps, ())
        self.assertEqual(cons, ())
        self.assertEqual(len(fatals), 1)


    def test_duplicate_declarations_refused(self):
        composition, manifests = _base()
        caps, _, fatals, _ = compute_capability_availability(
            composition, manifests, (_observation(),),
            disabled_capabilities=("cap.alpha", "cap.alpha"),
        )
        self.assertEqual(len(fatals), 1)
        self.assertEqual(caps[0].state, STATE_AVAILABLE)
        composition, manifests = _base(required=False)
        _, cons, fatals, _ = compute_capability_availability(
            composition, manifests, (),
            optional_fallbacks=(
                CapabilityFallback("cap.alpha", "repli"),
                CapabilityFallback("cap.alpha", "autre"),
            ),
        )
        self.assertEqual(len(fatals), 2)
        self.assertEqual(cons[0].state, STATE_BLOCKED)
        self.assertIsNone(cons[0].fallback)

    def test_composition_inactive_refused(self):
        composition, manifests = _base()
        inactive = replace(composition, stage="resolve", activated=False)
        caps, cons, fatals, warnings = compute_capability_availability(inactive, manifests, ())
        self.assertEqual(caps, ())
        self.assertEqual(cons, ())
        self.assertEqual(len(fatals), 1)
        self.assertEqual(warnings, ())


class _Evil:
    def __iter__(self):
        raise AssertionError
    def __bool__(self):
        raise AssertionError
    def __repr__(self):
        raise AssertionError
    def __str__(self):
        raise AssertionError
    def __eq__(self, other):
        raise AssertionError
    def __hash__(self):
        raise AssertionError


class _EvilStr(str):
    def __eq__(self, other):
        raise AssertionError
    def __hash__(self):
        raise AssertionError


class _EvilList(list):
    def __iter__(self):
        raise AssertionError


class _EvilTuple(tuple):
    def __iter__(self):
        raise AssertionError


class _EvilDict(dict):
    def items(self):
        raise AssertionError


class _EvilMeta(type):
    def __eq__(cls, other):
        raise AssertionError


class _EvilInstance(metaclass=_EvilMeta):
    pass


class TestForeignTypes(unittest.TestCase):
    def test_foreign_inputs_refused(self):
        composition, manifests = _base()
        for name in (
            "composition", "manifests", "observations",
            "optional_fallbacks", "disabled_capabilities",
        ):
            inputs = dict(
                composition=composition,
                manifests=manifests,
                observations=(),
            )
            inputs[name] = _Evil()
            caps, cons, fatals, warnings = compute_capability_availability(**inputs)
            self.assertTrue(fatals)
            if name in ("composition", "manifests"):
                self.assertEqual(caps, ())
                self.assertEqual(cons, ())
                self.assertEqual(warnings, ())
            else:
                self.assertEqual(caps[0].state, STATE_RESOLVED)
                self.assertEqual(cons[0].state, STATE_BLOCKED)

    def test_foreign_hooks_refused(self):
        composition, manifests = _base()
        for hooks in (_Evil(), _EvilDict()):
            result = run_gated_hooks(composition, manifests, hooks, ())
            self.assertEqual(result.calls, ())
            self.assertEqual(result.capability_states, ())
            self.assertEqual(result.consumed_states, ())
            self.assertEqual(len(result.diagnostics), 1)


    def test_hostile_metaclass_refused(self):
        composition, manifests = _base()
        cases = (
            {"composition": _EvilInstance()},
            {"manifests": _EvilInstance()},
            {"observations": (_EvilInstance(),)},
            {"optional_fallbacks": (_EvilInstance(),)},
            {"disabled_capabilities": (_EvilInstance(),)},
        )
        for index, overrides in enumerate(cases):
            inputs = dict(
                composition=composition,
                manifests=manifests,
                observations=(),
            )
            inputs.update(overrides)
            caps, cons, fatals, _ = compute_capability_availability(**inputs)
            self.assertTrue(fatals, index)
            if index < 2:
                self.assertEqual(caps, (), index)
                self.assertEqual(cons, (), index)
            else:
                self.assertEqual(caps[0].state, STATE_RESOLVED, index)
                self.assertEqual(cons[0].state, STATE_BLOCKED, index)
        result = run_gated_hooks(composition, manifests, _EvilInstance(), ())
        self.assertEqual(result.calls, ())
        self.assertEqual(result.capability_states, ())
        self.assertEqual(result.consumed_states, ())
        self.assertEqual(len(result.diagnostics), 1)

    def test_foreign_fields_refused(self):
        composition, manifests = _base()
        descriptor = _descriptor_of("cap.alpha", "1.0.0", "alpha", "alpha")
        cases = (
            ("stage", replace(composition, stage=_EvilStr("activated")),
             manifests, ()),
            ("order",
             replace(composition, order=_EvilTuple(composition.order)),
             manifests, ()),
            ("edges",
             replace(composition, edges=_EvilTuple(composition.edges)),
             manifests, ()),
            ("capability_descriptors",
             replace(composition,
                     capability_descriptors=_EvilTuple((descriptor,))),
             manifests, ()),
            ("descriptor.capability_id",
             replace(composition, capability_descriptors=(
                 replace(descriptor, capability_id=_EvilStr("cap.alpha")),)),
             manifests, ()),
            ("descriptor.contract_refs",
             replace(composition, capability_descriptors=(
                 replace(descriptor, contract_refs=_EvilTuple(())),)),
             manifests, ()),
            ("manifest.id", composition,
             (manifests[0], replace(manifests[1], id=_EvilStr("beta"))), ()),
            ("manifest.dependency_capabilities", composition, (
                manifests[0],
                replace(manifests[1],
                        dependency_capabilities=_EvilList(["cap.alpha"])),
            ), ()),
            ("manifests_container", composition, _EvilList(manifests), ()),
            ("observations_container", composition, manifests, _EvilTuple(())),
        )
        for index, (name, comp, manifold, obs) in enumerate(cases):
            with self.subTest(index=index):
                caps, cons, fatals, _ = compute_capability_availability(
                    comp, manifold, obs
                )
                self.assertTrue(fatals)
        hostile = CapabilityObservation(
            capability_id="cap.alpha",
            capability_version="1.0.0",
            provider_id="alpha",
            operable=1,
        )
        caps, cons, fatals, _ = compute_capability_availability(
            composition, manifests, (hostile,)
        )
        self.assertEqual(caps[0].state, STATE_RESOLVED)
        self.assertEqual(cons[0].state, STATE_BLOCKED)
        self.assertTrue(any("observation" in d.constraint for d in fatals))


class TestDeterminism(unittest.TestCase):
    def test_input_permutations_identical(self):
        composition, base_manifests = _base(required=False)
        manifests = base_manifests + (_node("gamma", "cap.other"),)
        descriptor_alpha = _descriptor_of("cap.alpha", "1.0.0", "alpha", "alpha")
        descriptor_other = _descriptor_of("cap.other", "1.0.0", "gamma", "gamma")
        alpha_observation = _observation()
        other_observation = CapabilityObservation(
            capability_id="cap.other",
            capability_version="1.0.0",
            provider_id="gamma",
            operable=True,
        )
        fallback_main = CapabilityFallback("cap.alpha", "repli")
        fallback_other = CapabilityFallback("cap.other", "autre")

        def build(flip):
            variants = {
                "manifests": manifests,
                "observations": (alpha_observation, other_observation),
                "optional_fallbacks": (fallback_main, fallback_other),
                "disabled_capabilities": ("cap.other", "cap.zzz"),
                "edges": (("beta", "alpha"), ("beta", "gamma")),
                "capability_descriptors": (descriptor_alpha, descriptor_other),
            }
            if flip:
                variants = {
                    key: tuple(reversed(value)) for key, value in variants.items()
                }
            variant = replace(
                composition,
                order=("alpha", "beta", "gamma"),
                edges=variants.pop("edges"),
                capability_descriptors=variants.pop("capability_descriptors"),
            )
            return compute_capability_availability(variant, **variants)

        self.assertEqual(build(True), build(False))

    def test_fallback_map_shared_between_consumers(self):
        manifests = (
            _node("alpha", "cap.alpha"),
            _node("beta", entries=("cap.alpha",), optional=True),
            _node("gamma", entries=("cap.alpha",), optional=True),
        )
        composition = _composition_of(
            manifests,
            (_descriptor_of("cap.alpha", "1.0.0", "alpha", "alpha"),),
            (("beta", "alpha"), ("gamma", "alpha")),
        )
        caps, cons, fatals, warnings = compute_capability_availability(
            composition, manifests, (),
            optional_fallbacks=(CapabilityFallback("cap.alpha", "repli"),),
        )
        self.assertEqual(fatals, ())
        self.assertEqual(
            [(record.state, record.fallback) for record in cons],
            [(STATE_DEGRADED, "repli"), (STATE_DEGRADED, "repli")],
        )
        self.assertEqual(len(warnings), 2)

    def test_diagnostics_without_invalid_echo(self):
        composition, manifests = _base()
        observation = CapabilityObservation(
            capability_id="cap.alpha",
            capability_version="1.0.0:marqueur",
            provider_id="alpha",
            operable=True,
        )
        _, _, fatals, _ = compute_capability_availability(
            composition, manifests, (observation,)
        )
        for diagnostic in fatals:
            self.assertNotIn("marqueur", diagnostic)
        counter = []

        def callback():
            counter.append("called")

        for hooks in (
            {"a:b": {"start": callback}},
            {"alpha": {"x:y": callback}},
        ):
            result = run_gated_hooks(composition, manifests, hooks, (_observation(),))
            self.assertTrue(result.diagnostics)
            self.assertEqual(result.calls, ())
            self.assertEqual(result.capability_states, ())
            self.assertEqual(counter, [])
            for diagnostic in result.diagnostics:
                self.assertNotIn("a:b", diagnostic)
                self.assertNotIn("x:y", diagnostic)


if __name__ == "__main__":
    unittest.main()
