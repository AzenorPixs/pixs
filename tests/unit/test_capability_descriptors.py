"""Tests unitaires des descripteurs canoniques de capacités (tâche 2.3).

Matrice : descripteur figé exact à sept champs sans défaut ; dérivation
exclusive des capacités fournies avec valeurs copiées du manifest ; tri
canonique indépendant de l'ordre ; liaison descriptive exacte (fourni
résolu, non consommé ou non résolu, mauvais owner/portée/version ne lie
pas) ; doublons de fournisseurs produisant deux descripteurs distincts ;
refus fermés sans écho de valeur brute ni ValueError contextuel ; types
exacts exigés avant tout hook étranger (itération, booléen, égalité,
hachage, rendu), compteurs mesurés à zéro sur les types invalides.
"""

import unittest
from dataclasses import FrozenInstanceError, fields, replace

from pixs.kernel.capabilities import (
    CapabilityDescriptor,
    bind_capability_descriptors,
    build_capability_descriptors,
)
from pixs.kernel.diagnostics import VALIDATE, Diagnostic
from pixs.kernel.manifest import ComponentManifest, ProvidedCapability

EXPECTED_BINDING_ERROR = "descripteurs de capacités : entrée de liaison invalide"

CAPABILITY_SENTINEL = "cap invalide 999"
CRITICALITY_SENTINEL = "SENTINELLE-CRIT-999"
SCOPE_SENTINEL = "SENTINELLE-SCOPE-999"
ID_SENTINEL = "identifiant invalide 999"


def _manifest(
    component_id: object,
    version: str = "1.0.0",
    provides: tuple = (),
) -> ComponentManifest:
    return ComponentManifest(
        schema_version="1",
        id=component_id,
        type="MODULE",
        version=version,
        provided_capabilities=provides,
    )


def _capability(
    capability_id: object,
    version: str = "1.0.0",
    contracts: tuple = (),
    criticality: str = "REQUIRED",
    fallback: str = "none",
) -> ProvidedCapability:
    return ProvidedCapability(
        id=capability_id,
        version=version,
        contracts=contracts,
        criticality=criticality,
        fallback=fallback,
    )


def _base_descriptor() -> CapabilityDescriptor:
    return CapabilityDescriptor(
        capability_id="cap.a",
        capability_version="1.0.0",
        owner_component="t.a",
        contract_refs=(),
        provider_ref=None,
        criticality="REQUIRED",
        fallback="none",
    )


class _Counter:
    def __init__(self) -> None:
        self.counter = {
            "iter": 0,
            "bool": 0,
            "eq": 0,
            "hash": 0,
            "repr": 0,
            "str": 0,
        }

    def assert_empty(self, testcase: unittest.TestCase) -> None:
        testcase.assertEqual(
            self.counter,
            {"iter": 0, "bool": 0, "eq": 0, "hash": 0, "repr": 0, "str": 0},
        )


class _ForeignObject:
    def __init__(self, counter: _Counter) -> None:
        self._counter = counter.counter

    def __iter__(self):
        self._counter["iter"] += 1
        return iter(())

    def __bool__(self):
        self._counter["bool"] += 1
        return True

    def __eq__(self, other):
        self._counter["eq"] += 1
        return NotImplemented

    def __hash__(self):
        self._counter["hash"] += 1
        return 42

    def __repr__(self):
        self._counter["repr"] += 1
        return "<objet-etranger>"

    def __str__(self):
        self._counter["str"] += 1
        return "objet-etranger"


class _ForeignList(list):
    pass


class _ForeignTuple(tuple):
    pass


class _ForeignManifest(ComponentManifest):
    pass


class _ForeignCapability(ProvidedCapability):
    pass


class _ForeignDescriptor(CapabilityDescriptor):
    pass


class TestCapabilityDescriptor(unittest.TestCase):
    def test_sept_champs_exact_sans_defaut(self) -> None:
        self.assertEqual(
            tuple(item.name for item in fields(CapabilityDescriptor)),
            (
                "capability_id",
                "capability_version",
                "owner_component",
                "contract_refs",
                "provider_ref",
                "criticality",
                "fallback",
            ),
        )
        with self.assertRaises(TypeError):
            CapabilityDescriptor()

    def test_fige_sans_mutation(self) -> None:
        descriptors, diagnostics = build_capability_descriptors(
            (_manifest("t.a", provides=(_capability("cap.a", "1.0.0"),)),)
        )
        self.assertEqual(diagnostics, ())
        with self.assertRaises(FrozenInstanceError):
            descriptors[0].criticality = "OPTIONAL"

    def test_build_champs_copies_exact(self) -> None:
        manifest = _manifest(
            "t.a",
            version="1.2.0+build.7",
            provides=(_capability("cap.a", "1.0.0", contracts=("t.a.contract",)),),
        )
        descriptors, diagnostics = build_capability_descriptors((manifest,))
        self.assertEqual(diagnostics, ())
        self.assertEqual(len(descriptors), 1)
        descriptor = descriptors[0]
        self.assertEqual(descriptor.capability_id, "cap.a")
        self.assertEqual(descriptor.capability_version, "1.0.0")
        self.assertEqual(descriptor.owner_component, "t.a")
        self.assertEqual(descriptor.contract_refs, ("t.a.contract",))
        self.assertIsNone(descriptor.provider_ref)
        self.assertEqual(descriptor.criticality, "REQUIRED")
        self.assertEqual(descriptor.fallback, "none")

    def test_required_none_et_optional_repli_copie(self) -> None:
        a = _manifest("t.a", provides=(_capability("cap.a", "1.0.0"),))
        b = _manifest(
            "t.b",
            provides=(
                _capability(
                    "cap.b",
                    "0.9.0",
                    criticality="OPTIONAL",
                    fallback="t.repli.local",
                ),
            ),
        )
        descriptors, diagnostics = build_capability_descriptors((a, b))
        self.assertEqual(diagnostics, ())
        self.assertEqual(
            (descriptors[0].criticality, descriptors[0].fallback),
            ("REQUIRED", "none"),
        )
        self.assertEqual(
            (descriptors[1].criticality, descriptors[1].fallback),
            ("OPTIONAL", "t.repli.local"),
        )

    def test_tri_canonique_deux_ordres_identiques(self) -> None:
        a = _manifest(
            "t.a",
            provides=(_capability("cap.a", "1.0.0"), _capability("cap.c", "2.0.0")),
        )
        b = _manifest("t.b", provides=(_capability("cap.b", "1.5.0"),))
        self.assertEqual(
            build_capability_descriptors((a, b)),
            build_capability_descriptors((b, a)),
        )

    def test_doublons_fournisseurs_deux_descripteurs(self) -> None:
        p1 = _manifest("t.p1", provides=(_capability("cap.x", "1.0.0"),))
        p2 = _manifest("t.p2", provides=(_capability("cap.x", "1.0.0"),))
        descriptors, diagnostics = build_capability_descriptors((p1, p2))
        self.assertEqual(diagnostics, ())
        self.assertEqual(len(descriptors), 2)
        self.assertEqual(
            {d.owner_component for d in descriptors}, {"t.p1", "t.p2"}
        )

    def test_purete_determinisme(self) -> None:
        manifests = (_manifest("t.a", provides=(_capability("cap.a", "1.0.0"),)),)
        first = build_capability_descriptors(manifests)
        second = build_capability_descriptors(manifests)
        self.assertEqual(first, second)
        self.assertIsNot(first[0], second[0])
        self.assertIsNot(first[0][0], second[0][0])

    def test_entree_vide(self) -> None:
        self.assertEqual(build_capability_descriptors(()), ((), ()))


class TestBuildRefus(unittest.TestCase):
    def _assert_validate(self, diagnostics) -> None:
        for diagnostic in diagnostics:
            self.assertIsInstance(diagnostic, Diagnostic)
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertEqual(diagnostic.element, "capabilités")

    def test_conteneurs_inexact_sans_hook(self) -> None:
        counter = _Counter()
        foreign = _ForeignObject(counter)
        for container in (
            dict(),
            "t.a",
            42,
            None,
            _ForeignList(),
            _ForeignTuple(()),
            foreign,
        ):
            with self.subTest(container=type(container).__name__):
                descriptors, diagnostics = build_capability_descriptors(container)
                self.assertEqual(descriptors, ())
                self.assertEqual(len(diagnostics), 1)
                self._assert_validate(diagnostics)
                self.assertEqual(
                    diagnostics[0].constraint,
                    "liste ou tuple de manifests attendus",
                )
        counter.assert_empty(self)

    def test_generateur_non_itere(self) -> None:
        touched = []

        def generator():
            touched.append("iteration")
            yield _manifest("t.a")

        descriptors, diagnostics = build_capability_descriptors(generator())
        self.assertEqual(descriptors, ())
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(
            diagnostics[0].constraint, "liste ou tuple de manifests attendus"
        )
        self.assertEqual(touched, [])

    def test_manifest_etranger_ou_sous_classe_refuse(self) -> None:
        counter = _Counter()
        foreign = _ForeignObject(counter)
        subclass = _ForeignManifest(
            schema_version="1",
            id="t.a",
            type="MODULE",
            version="1.0.0",
        )
        for invalid in (None, 42, object(), dict(), foreign, subclass):
            with self.subTest(invalid=type(invalid).__name__):
                descriptors, diagnostics = build_capability_descriptors(
                    (invalid,)
                )
                self.assertEqual(descriptors, ())
                self.assertEqual(len(diagnostics), 1)
                self._assert_validate(diagnostics)
                self.assertIn("manifestes[0]", diagnostics[0].message)
                self.assertEqual(
                    diagnostics[0].constraint, "manifest validé attendu"
                )
        counter.assert_empty(self)

    def test_identifiant_composant_invalide_sans_echo(self) -> None:
        last_diagnostics = ()
        for invalid in (None, 42, "", ID_SENTINEL, "t.a >=1.0.0"):
            with self.subTest(invalid=type(invalid).__name__):
                descriptors, last_diagnostics = build_capability_descriptors(
                    (
                        _manifest(
                            invalid, provides=(_capability("cap.a", "1.0.0"),)
                        ),
                    )
                )
                self.assertEqual(descriptors, ())
                self.assertEqual(len(last_diagnostics), 1)
                self._assert_validate(last_diagnostics)
                self.assertEqual(
                    last_diagnostics[0].constraint,
                    "identifiant de composant nu attendu",
                )
        rendered = "\n".join(str(d) for d in last_diagnostics)
        self.assertNotIn(ID_SENTINEL, rendered)

    def test_provided_capabilities_inexact_sans_hook(self) -> None:
        counter = _Counter()
        foreign = _ForeignObject(counter)
        for invalid in ([], None, 42, foreign):
            with self.subTest(invalid=type(invalid).__name__):
                manifest = ComponentManifest(
                    schema_version="1",
                    id="t.a",
                    type="MODULE",
                    version="1.0.0",
                    provided_capabilities=invalid,
                )
                descriptors, diagnostics = build_capability_descriptors(
                    (manifest,)
                )
                self.assertEqual(descriptors, ())
                self.assertEqual(len(diagnostics), 1)
                self._assert_validate(diagnostics)
                self.assertEqual(
                    diagnostics[0].constraint,
                    "tuple de capacités fournies attendu",
                )
        counter.assert_empty(self)

    def test_capacite_etranger_ou_sous_classe_refuse(self) -> None:
        counter = _Counter()
        foreign = _ForeignObject(counter)
        subclass = _ForeignCapability(
            id="cap.a",
            version="1.0.0",
            contracts=(),
            criticality="REQUIRED",
            fallback="none",
        )
        for invalid in (None, 42, object(), foreign, subclass):
            with self.subTest(invalid=type(invalid).__name__):
                descriptors, diagnostics = build_capability_descriptors(
                    (_manifest("t.a", provides=(invalid,)),)
                )
                self.assertEqual(descriptors, ())
                self.assertEqual(len(diagnostics), 1)
                self._assert_validate(diagnostics)
                self.assertEqual(
                    diagnostics[0].constraint,
                    "capacité fournie validée attendue",
                )
        counter.assert_empty(self)

    def test_champs_capacite_invalides_agreges_sans_echo(self) -> None:
        cases = (
            (
                _capability(CAPABILITY_SENTINEL, "1.0.0"),
                "identifiant de capacité nu attendu",
            ),
            (
                _capability("cap.a", "1.0"),
                "version SemVer 2.0.0 complète attendue",
            ),
            (
                _capability("cap.a", None),
                "version SemVer 2.0.0 complète attendue",
            ),
            (
                _capability(
                    "cap.a", "1.0.0", criticality=CRITICALITY_SENTINEL
                ),
                "criticalité REQUIRED ou OPTIONAL attendue",
            ),
            (
                _capability("cap.a", "1.0.0", fallback="auto"),
                "repli 'none' attendu pour une capacité requise",
            ),
            (
                _capability(
                    "cap.a",
                    "1.0.0",
                    criticality="OPTIONAL",
                    fallback="",
                ),
                "repli non vide attendu pour une capacité optionnelle",
            ),
            (
                _capability("cap.a", "1.0.0", contracts=["t.a.contract"]),
                "références de contrats en tuple de chaînes non vides attendu",
            ),
            (
                _capability("cap.a", "1.0.0", contracts=("",)),
                "références de contrats en tuple de chaînes non vides attendu",
            ),
        )
        all_diagnostics: list = []
        for position, (capability, constraint) in enumerate(cases):
            with self.subTest(position=position):
                descriptors, diagnostics = build_capability_descriptors(
                    (_manifest("t.a", provides=(capability,)),)
                )
                self.assertEqual(descriptors, ())
                self.assertEqual(len(diagnostics), 1)
                self._assert_validate(diagnostics)
                self.assertEqual(diagnostics[0].constraint, constraint)
                self.assertIn(
                    "provides.capabilities[0]", diagnostics[0].message
                )
                all_diagnostics.extend(diagnostics)
        rendered = "\n".join(str(d) for d in all_diagnostics)
        self.assertNotIn(CAPABILITY_SENTINEL, rendered)
        self.assertNotIn(CRITICALITY_SENTINEL, rendered)

    def test_agregation_sans_interruption(self) -> None:
        valid = _capability("cap.a", "1.0.0")
        invalid = _capability(
            "cap.z", "1.0.0", criticality=CRITICALITY_SENTINEL
        )
        descriptors, diagnostics = build_capability_descriptors(
            (
                _manifest("t.a", provides=(valid, invalid)),
                None,
                _manifest("t.b", provides=(_capability("cap.b", "0.9.0"),)),
            )
        )
        self.assertEqual(
            [d.capability_id for d in descriptors], ["cap.a", "cap.b"]
        )
        self.assertEqual(len(diagnostics), 2)
        self._assert_validate(diagnostics)


class TestBindLiaisonDescriptive(unittest.TestCase):
    def _descriptors(self):
        a = _manifest(
            "t.a",
            provides=(
                _capability("cap.a", "1.0.0"),
                _capability(
                    "cap.opt",
                    "0.9.0",
                    criticality="OPTIONAL",
                    fallback="t.repli.local",
                ),
            ),
        )
        b = _manifest(
            "t.b",
            version="2.0.0",
            provides=(
                _capability("cap.b", "1.5.0", contracts=("t.b.contract",)),
            ),
        )
        descriptors, diagnostics = build_capability_descriptors((a, b))
        self.assertEqual(diagnostics, ())
        return descriptors

    def test_liaison_exacte_owner_scope_id_version(self) -> None:
        descriptors = self._descriptors()
        bound = bind_capability_descriptors(
            descriptors,
            (("t.a", "CAPABILITY", "cap.a", "1.0.0"),),
        )
        mapping = {d.capability_id: d.provider_ref for d in bound}
        self.assertEqual(
            mapping, {"cap.a": "t.a", "cap.b": None, "cap.opt": None}
        )

    def test_mauvais_owner_scope_version_ne_lie_pas(self) -> None:
        for binding in (
            ("t.z", "CAPABILITY", "cap.a", "1.0.0"),
            ("t.a", "CONTRACT", "cap.a", "1.0.0"),
            ("t.a", "CAPABILITY", "cap.a", "1.0.1"),
            ("t.a", "CAPABILITY", "cap.z", "1.0.0"),
        ):
            with self.subTest(binding=binding):
                descriptors = self._descriptors()
                bound = bind_capability_descriptors(descriptors, (binding,))
                mapping = {d.capability_id: d.provider_ref for d in bound}
                self.assertEqual(
                    mapping, {"cap.a": None, "cap.b": None, "cap.opt": None}
                )

    def test_aucune_cible_aucune_liaison(self) -> None:
        bound = bind_capability_descriptors(self._descriptors(), ())
        self.assertTrue(all(d.provider_ref is None for d in bound))

    def test_doublons_fournisseurs_selection_unique(self) -> None:
        p1 = _manifest("t.p1", provides=(_capability("cap.x", "1.0.0"),))
        p2 = _manifest("t.p2", provides=(_capability("cap.x", "1.0.0"),))
        descriptors, _ = build_capability_descriptors((p1, p2))
        bound = bind_capability_descriptors(
            descriptors, (("t.p2", "CAPABILITY", "cap.x", "1.0.0"),)
        )
        mapping = {d.owner_component: d.provider_ref for d in bound}
        self.assertEqual(mapping, {"t.p1": None, "t.p2": "t.p2"})

    def test_purete_et_determinisme(self) -> None:
        descriptors = self._descriptors()
        bindings = (("t.a", "CAPABILITY", "cap.a", "1.0.0"),)
        first = bind_capability_descriptors(descriptors, bindings)
        second = bind_capability_descriptors(descriptors, bindings)
        self.assertEqual(first, second)
        self.assertIsNot(first[0], second[0])
        self.assertTrue(all(d.provider_ref is None for d in descriptors))


class _MetaCounting(type):
    def __eq__(cls, other):
        cls.hooks["eq"] += 1
        return True

    def __hash__(cls):
        return id(cls)


class _ForeignByMeta(metaclass=_MetaCounting):
    hooks = {"eq": 0, "iter": 0}

    def __iter__(self):
        _ForeignByMeta.hooks["iter"] += 1
        return iter(())


class TestExactTypeFiltering(unittest.TestCase):
    def test_metaclasse_etrangere_refusee_sans_hooks(self) -> None:
        _ForeignByMeta.hooks = {"eq": 0, "iter": 0}
        foreign = _ForeignByMeta()
        with self.assertRaises(ValueError) as caught:
            bind_capability_descriptors(foreign, ())
        self.assertEqual(str(caught.exception), EXPECTED_BINDING_ERROR)
        with self.assertRaises(ValueError) as caught:
            bind_capability_descriptors((), foreign)
        self.assertEqual(str(caught.exception), EXPECTED_BINDING_ERROR)
        descriptors, diagnostics = build_capability_descriptors(
            foreign
        )
        self.assertEqual(descriptors, ())
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(
            diagnostics[0].constraint,
            "liste ou tuple de manifests attendus",
        )
        self.assertEqual(_ForeignByMeta.hooks, {"eq": 0, "iter": 0})


class TestBindRefus(unittest.TestCase):
    def _assert_refusal(self, operation) -> None:
        with self.assertRaises(ValueError) as caught:
            operation()
        self.assertEqual(str(caught.exception), EXPECTED_BINDING_ERROR)
        self.assertIsNone(caught.exception.__cause__)

    def test_conteneurs_inexact(self) -> None:
        base = _base_descriptor()
        cases = (
            lambda: bind_capability_descriptors(dict(), ()),
            lambda: bind_capability_descriptors((base,), dict()),
            lambda: bind_capability_descriptors((base,), "x"),
            lambda: bind_capability_descriptors((base,), 42),
            lambda: bind_capability_descriptors(_ForeignList(), ()),
            lambda: bind_capability_descriptors(
                (base,), _ForeignTuple(())
            ),
        )
        for position, operation in enumerate(cases):
            with self.subTest(position=position):
                self._assert_refusal(operation)

    def test_entrees_malformees_sans_echo(self) -> None:
        descriptors = (_base_descriptor(),)
        cases = (
            (42,),
            (["t.a", "CAPABILITY", "cap.a", "1.0.0"],),
            (_ForeignTuple(("t.a", "CAPABILITY", "cap.a", "1.0.0")),),
            (("t.a", "CAPABILITY", "cap.a"),),
            (("t.a", "CAPABILITY", "cap.a", "1.0.0", "excès"),),
            ((None, "CAPABILITY", "cap.a", "1.0.0"),),
            (("t.a", None, "cap.a", "1.0.0"),),
            (("t.a", "CAPABILITY", None, "1.0.0"),),
            (("t.a", "CAPABILITY", "cap.a", None),),
            ((42, "CAPABILITY", "cap.a", "1.0.0"),),
            (("t.a", 42, "cap.a", "1.0.0"),),
            (("t.a", "CAPABILITY", 42, "1.0.0"),),
            (("t.a", "CAPABILITY", "cap.a", 42),),
            (("", "CAPABILITY", "cap.a", "1.0.0"),),
            (("t.a", "", "cap.a", "1.0.0"),),
            (("t.a", "CAPABILITY", "", "1.0.0"),),
            (("t.a", "CAPABILITY", "cap.a", ""),),
            (("t.a", SCOPE_SENTINEL, "cap.a", "1.0.0"),),
            (("t.a >=1.0.0", "CAPABILITY", "cap.a", "1.0.0"),),
            (("t.a", "CAPABILITY", "cap invalide 999", "1.0.0"),),
            (("t.a", "CAPABILITY", "cap.a", "1.0"),),
        )
        for position, bindings in enumerate(cases):
            with self.subTest(position=position):
                self._assert_refusal(
                    lambda bindings=bindings: bind_capability_descriptors(
                        descriptors, bindings
                    )
                )
                self.assertNotIn(SCOPE_SENTINEL, EXPECTED_BINDING_ERROR)

    def test_descripteurs_invalides_matrix(self) -> None:
        base = _base_descriptor()
        variants = {
            "capability_id": ("cap.x >=1.0.0", "", None, 42),
            "capability_version": ("1.0", "", None, 42),
            "owner_component": ("BAD ID", "", None, 42),
            "contract_refs": (["t.a.contract"], ("",), (42,), (None,)),
            "provider_ref": (42, [], "", "BAD ID", "t.x >=1.0.0"),
            "criticality": ("URGENT", "", None, 42),
            "fallback": ("auto", "", None, 42),
        }
        for field, values in variants.items():
            for value in values:
                with self.subTest(field=field):
                    descriptor = replace(base, **{field: value})
                    self._assert_refusal(
                        lambda descriptor=descriptor: bind_capability_descriptors(
                            (descriptor,), ()
                        )
                    )

    def test_types_etrangers_refuses(self) -> None:
        self._assert_refusal(lambda: bind_capability_descriptors((object(),), ()))
        self._assert_refusal(
            lambda: bind_capability_descriptors(
                (_ForeignDescriptor(
                    capability_id="cap.a",
                    capability_version="1.0.0",
                    owner_component="t.a",
                    contract_refs=(),
                    provider_ref=None,
                    criticality="REQUIRED",
                    fallback="none",
                ),),
                (),
            )
        )

    def test_hooks_etrangers_jamais_invoques(self) -> None:
        counter = _Counter()
        foreign = _ForeignObject(counter)
        bad = replace(
            _capability("cap.a", "1.0.0"), criticality=foreign
        )
        descriptors, diagnostics = build_capability_descriptors(
            (_manifest("t.a", provides=(bad,)),)
        )
        self.assertEqual(descriptors, ())
        self.assertEqual(len(diagnostics), 1)
        base = replace(
            _base_descriptor(), contract_refs=(foreign,)
        )
        self._assert_refusal(
            lambda: bind_capability_descriptors((base,), ())
        )
        self._assert_refusal(
            lambda: bind_capability_descriptors(
                (), ((foreign, "CAPABILITY", "cap.a", "1.0.0"),)
            )
        )
        counter.assert_empty(self)


if __name__ == "__main__":
    unittest.main()
