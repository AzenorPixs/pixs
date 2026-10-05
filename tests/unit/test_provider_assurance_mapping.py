"""Tests unitaires du mapping d'assurance fournisseur (tâche 2.2).

Porte publique uniquement : ``evaluate_assurance`` et les DTO figés ; aucune
horloge système, tous les horodatages sont des UTC explicites fixes. Les
pièges vérifient qu'aucun crochet étranger (eq/hash/bool/str/repr/call,
itération, utcoffset, nom d'attribut) n'est invoqué sur les entrées invalides.
"""

from __future__ import annotations

import dataclasses
import itertools
import datetime
import unittest
from dataclasses import replace

from pixs.core.authz.assurance_mapping import (
    AssuranceDimension,
    AssuranceMappingError,
    AssuranceResult,
    AssuranceRule,
    ProofObservation,
    ProviderAssuranceMapping,
    evaluate_assurance,
)
from pixs.core.authz.policy import (
    AuthenticationAssurance,
    FederationTrust,
    IdentityAssurance,
)

UTC = datetime.timezone.utc
VALID_FROM = datetime.datetime(2026, 1, 1, tzinfo=UTC)
VALID_UNTIL = datetime.datetime(2027, 1, 1, tzinfo=UTC)
REF = datetime.datetime(2026, 6, 1, tzinfo=UTC)
ATTESTED = datetime.datetime(2026, 5, 1, tzinfo=UTC)
EXPIRES = datetime.datetime(2026, 12, 1, tzinfo=UTC)

EQ_CALLS: list[str] = []
HASH_CALLS: list[str] = []
STR_CALLS: list[str] = []
REPR_CALLS: list[str] = []
BOOL_CALLS: list[str] = []
ITER_CALLS: list[str] = []
CALL_CALLS: list[str] = []
GETATTR_CALLS: list[str] = []
META_CALLS: list[str] = []
UTCOFFSET_CALLS: list[str] = []


class _Hook:
    def __eq__(self, other):
        EQ_CALLS.append("hook")
        return False

    def __hash__(self):
        HASH_CALLS.append("hook")
        return 1

    def __str__(self):
        STR_CALLS.append("hook")
        return "hook"

    def __repr__(self):
        REPR_CALLS.append("hook")
        return "<hook>"

    def __bool__(self):
        BOOL_CALLS.append("hook")
        return True

    def __iter__(self):
        ITER_CALLS.append("hook")
        return iter(())

    def __call__(self, *args, **kwargs):
        CALL_CALLS.append("hook")


class _HookList(list):
    def __iter__(self):
        ITER_CALLS.append("list")
        return list.__iter__(self)


class _HookDto(ProofObservation):
    def __getattr__(self, name):
        GETATTR_CALLS.append(name)
        raise AttributeError(name)


class _TrapMeta(type):
    def __eq__(cls, other):
        META_CALLS.append("meta_eq")
        return type.__eq__(cls, other)


class _MetaHostile(metaclass=_TrapMeta):
    pass


class _HookTuple(tuple):
    def __iter__(self):
        ITER_CALLS.append("tuple")
        return tuple.__iter__(self)


class _HostileTZ(datetime.tzinfo):
    def utcoffset(self, dt):
        UTCOFFSET_CALLS.append("utcoffset")
        raise AssertionError("utcoffset interdit")

    def dst(self, dt):
        UTCOFFSET_CALLS.append("dst")
        raise AssertionError("dst interdit")

    def tzname(self, dt):
        UTCOFFSET_CALLS.append("tzname")
        raise AssertionError("tzname interdit")


WITNESS = ProviderAssuranceMapping(
    provider_id="web.sso",
    max_identity_assurance=IdentityAssurance.PROOFED,
    max_authentication_assurance=AuthenticationAssurance.PHISHING_RESISTANT,
    max_federation_trust=FederationTrust.STRONGLY_BOUND,
    accepted_rules=(
        AssuranceRule(
            dimension=AssuranceDimension.IDENTITY,
            method="webauthn",
            level=IdentityAssurance.VERIFIED,
        ),
        AssuranceRule(
            dimension=AssuranceDimension.AUTHENTICATION,
            method="webauthn",
            level=AuthenticationAssurance.MULTI_FACTOR,
        ),
        AssuranceRule(
            dimension=AssuranceDimension.FEDERATION,
            method="saml",
            level=FederationTrust.TRUSTED,
        ),
    ),
    valid_from=VALID_FROM,
    valid_until=VALID_UNTIL,
)


def _observation(**overrides) -> ProofObservation:
    fields = {
        "observation_id": "obs-1",
        "provider_id": "web.sso",
        "method": "webauthn",
        "status": "VERIFIED",
        "attested_at": ATTESTED,
        "expires_at": EXPIRES,
    }
    fields.update(overrides)
    return ProofObservation(**fields)


def _evaluate(
    mapping: ProviderAssuranceMapping = WITNESS,
    observations: tuple = (),
    reference_time: datetime.datetime = REF,
) -> AssuranceResult:
    return evaluate_assurance(mapping, observations, reference_time)


class ProviderAssuranceMappingTests(unittest.TestCase):
    def setUp(self) -> None:
        for calls in (
            EQ_CALLS, HASH_CALLS, STR_CALLS, REPR_CALLS, BOOL_CALLS,
            ITER_CALLS, CALL_CALLS, GETATTR_CALLS, META_CALLS,
            UTCOFFSET_CALLS,
        ):
            calls.clear()

    def test_error_constant_fields(self) -> None:
        error = AssuranceMappingError()
        self.assertEqual(error.code, "PDP_MAPPING_INVALID")
        self.assertEqual(error.element, "pdp_mapping")
        self.assertEqual(error.step, "validate_mapping")
        self.assertEqual(len(str(error)) > 0, True)

    def test_dto_champs_requis_geles_et_kwargs_inconnus(self) -> None:
        expected_names = {
            AssuranceRule: ("dimension", "method", "level"),
            ProviderAssuranceMapping: (
                "provider_id",
                "max_identity_assurance",
                "max_authentication_assurance",
                "max_federation_trust",
                "accepted_rules",
                "valid_from",
                "valid_until",
            ),
            ProofObservation: (
                "observation_id",
                "provider_id",
                "method",
                "status",
                "attested_at",
                "expires_at",
            ),
            AssuranceResult: (
                "identity_assurance",
                "authentication_assurance",
                "federation_trust",
            ),
        }
        witnesses = {
            AssuranceRule: WITNESS.accepted_rules[0],
            ProviderAssuranceMapping: WITNESS,
            ProofObservation: _observation(),
            AssuranceResult: AssuranceResult(
                identity_assurance=IdentityAssurance.CLAIMED,
                authentication_assurance=AuthenticationAssurance.SINGLE_FACTOR,
                federation_trust=FederationTrust.UNTRUSTED,
            ),
        }
        for dto, names in expected_names.items():
            fields = dataclasses.fields(dto)
            self.assertEqual(tuple(field.name for field in fields), names)
            for field in fields:
                self.assertIs(field.default, dataclasses.MISSING)
                self.assertIs(field.default_factory, dataclasses.MISSING)
            witness = witnesses[dto]
            complete = {name: getattr(witness, name) for name in names}
            for name in names:
                partial = dict(complete)
                partial.pop(name)
                with self.assertRaises(TypeError):
                    dto(**partial)
            with self.assertRaises(TypeError):
                dto(**complete, expression="x")
            with self.assertRaises(dataclasses.FrozenInstanceError):
                setattr(witness, names[0], "muté")

    def test_result_trois_champs_exactes(self) -> None:
        names = tuple(
            field.name for field in dataclasses.fields(AssuranceResult)
        )
        self.assertEqual(
            names,
            ("identity_assurance", "authentication_assurance", "federation_trust"),
        )

    def test_sans_regle_ni_observation_trois_minimums(self) -> None:
        empty = replace(WITNESS, accepted_rules=())
        result = _evaluate(mapping=empty)
        self.assertEqual(result.identity_assurance, IdentityAssurance.CLAIMED)
        self.assertEqual(
            result.authentication_assurance,
            AuthenticationAssurance.SINGLE_FACTOR,
        )
        self.assertEqual(result.federation_trust, FederationTrust.UNTRUSTED)

    def test_temoin_trois_regles_donne_niveaux_declares(self) -> None:
        result = _evaluate(observations=(_observation(),))
        self.assertEqual(result.identity_assurance, IdentityAssurance.VERIFIED)
        self.assertEqual(
            result.authentication_assurance,
            AuthenticationAssurance.MULTI_FACTOR,
        )
        self.assertEqual(result.federation_trust, FederationTrust.UNTRUSTED)

    def test_niveau_declare_jamais_plafond_implicite(self) -> None:
        rule = AssuranceRule(
            dimension=AssuranceDimension.IDENTITY,
            method="otp",
            level=IdentityAssurance.CLAIMED,
        )
        mapping = replace(WITNESS, accepted_rules=(rule,))
        result = _evaluate(
            mapping=mapping,
            observations=(_observation(method="otp"),),
        )
        self.assertEqual(result.identity_assurance, IdentityAssurance.CLAIMED)

    def test_enums_de_dimension_independantes(self) -> None:
        for rule in (
            AssuranceRule(
                dimension=AssuranceDimension.IDENTITY,
                method="webauthn",
                level=AuthenticationAssurance.MULTI_FACTOR,
            ),
            AssuranceRule(
                dimension=AssuranceDimension.AUTHENTICATION,
                method="webauthn",
                level=IdentityAssurance.VERIFIED,
            ),
            AssuranceRule(
                dimension=AssuranceDimension.FEDERATION,
                method="webauthn",
                level=AuthenticationAssurance.PHISHING_RESISTANT,
            ),
        ):
            mapping = replace(WITNESS, accepted_rules=(rule,))
            with self.assertRaises(AssuranceMappingError):
                _evaluate(mapping=mapping, observations=(_observation(),))

    def test_niveau_au_dessus_du_plafond_refuse(self) -> None:
        mapping = replace(
            WITNESS,
            max_identity_assurance=IdentityAssurance.CLAIMED,
        )
        with self.assertRaises(AssuranceMappingError):
            _evaluate(mapping=mapping, observations=(_observation(),))

    def test_unicite_dimension_method(self) -> None:
        duplicate = replace(
            WITNESS,
            accepted_rules=(
                WITNESS.accepted_rules[0],
                AssuranceRule(
                    dimension=AssuranceDimension.IDENTITY,
                    method="webauthn",
                    level=IdentityAssurance.CLAIMED,
                ),
            ),
        )
        with self.assertRaises(AssuranceMappingError):
            _evaluate(mapping=duplicate, observations=())

    def test_unicite_observation_id(self) -> None:
        with self.assertRaises(AssuranceMappingError):
            _evaluate(
                observations=(_observation(), _observation(method="saml"))
            )

    def test_meme_methode_deux_dimensions_exige_deux_regles(self) -> None:
        single = replace(WITNESS, accepted_rules=(WITNESS.accepted_rules[0],))
        result = _evaluate(mapping=single, observations=(_observation(),))
        self.assertEqual(result.identity_assurance, IdentityAssurance.VERIFIED)
        self.assertEqual(
            result.authentication_assurance,
            AuthenticationAssurance.SINGLE_FACTOR,
        )
        both = replace(
            WITNESS, accepted_rules=WITNESS.accepted_rules[:2]
        )
        result = _evaluate(mapping=both, observations=(_observation(),))
        self.assertEqual(result.identity_assurance, IdentityAssurance.VERIFIED)
        self.assertEqual(
            result.authentication_assurance,
            AuthenticationAssurance.MULTI_FACTOR,
        )

    def test_provider_different_statuts_non_verified_inaptes(self) -> None:
        cases = [
            _observation(provider_id="autre.sso"),
            _observation(method="inconnue"),
        ]
        cases.extend(
            _observation(status=status)
            for status in ("ABSENT", "AMBIGUOUS", "EXPIRED", "UNVERIFIED")
        )
        for observation in cases:
            result = _evaluate(observations=(observation,))
            self.assertEqual(
                result.identity_assurance,
                IdentityAssurance.CLAIMED,
                observation,
            )

    def test_fenetres_demi_ouvertes_du_mapping(self) -> None:
        observation = _observation(
            attested_at=VALID_FROM, expires_at=VALID_UNTIL
        )
        for reference, expect in (
            (VALID_FROM, True),
            (VALID_UNTIL - datetime.timedelta(microseconds=1), True),
            (VALID_UNTIL, False),
            (datetime.datetime(2028, 1, 1, tzinfo=UTC), False),
        ):
            result = _evaluate(
                observations=(observation,), reference_time=reference
            )
            self.assertEqual(
                result.identity_assurance is IdentityAssurance.VERIFIED, expect
            )

    def test_fenetres_observation(self) -> None:
        for attested, expires, expect in (
            (REF, EXPIRES, True),
            (ATTESTED, REF, False),
            (ATTESTED, ATTESTED + datetime.timedelta(microseconds=1), False),
            (REF + datetime.timedelta(seconds=1), EXPIRES, False),
        ):
            result = _evaluate(
                observations=(_observation(attested_at=attested, expires_at=expires),),
            )
            self.assertEqual(
                result.identity_assurance == IdentityAssurance.VERIFIED,
                expect,
                (attested, expires),
            )

    def test_mapping_hors_fenetre_trois_minimums_apres_validations(self) -> None:
        stale = replace(
            WITNESS,
            valid_from=datetime.datetime(2020, 1, 1, tzinfo=UTC),
            valid_until=datetime.datetime(2021, 1, 1, tzinfo=UTC),
        )
        result = _evaluate(
            mapping=stale,
            observations=(_observation(),),
            reference_time=REF,
        )
        self.assertEqual(result.identity_assurance, IdentityAssurance.CLAIMED)
        self.assertEqual(
            result.authentication_assurance,
            AuthenticationAssurance.SINGLE_FACTOR,
        )
        self.assertEqual(result.federation_trust, FederationTrust.UNTRUSTED)
        with self.assertRaises(AssuranceMappingError):
            _evaluate(
                mapping=stale,
                observations=(_observation(), _observation()),
                reference_time=REF,
            )

    def test_tzinfo_hostile_refuse_partout_sans_appel(self) -> None:
        hostile_dt = datetime.datetime(2026, 6, 1, tzinfo=_HostileTZ())
        naive = datetime.datetime(2026, 6, 1)
        cases = (
            (WITNESS, (_observation(),), hostile_dt),
            (WITNESS, (_observation(),), naive),
            (replace(WITNESS, valid_from=hostile_dt), (_observation(),), REF),
            (replace(WITNESS, valid_until=hostile_dt), (_observation(),), REF),
            (WITNESS, (_observation(expires_at=hostile_dt),), REF),
            (WITNESS, (_observation(),), type("SubDatetime", (datetime.datetime,), {})(2026, 6, 1, tzinfo=UTC)),
            (WITNESS, (_observation(attested_at=hostile_dt),), REF),
        )
        for mapping, observations, reference in cases:
            with self.assertRaises(AssuranceMappingError):
                evaluate_assurance(mapping, observations, reference)
        self.assertEqual(UTCOFFSET_CALLS, [])

    def test_deux_preuves_meme_niveau_puis_divergence_localisee(self) -> None:
        same = _evaluate(
            observations=(
                _observation(),
                _observation(observation_id="obs-2", method="webauthn"),
            ),
        )
        self.assertEqual(same.identity_assurance, IdentityAssurance.VERIFIED)
        divergent = replace(
            WITNESS,
            accepted_rules=(
                WITNESS.accepted_rules[0],
                AssuranceRule(
                    dimension=AssuranceDimension.IDENTITY,
                    method="otp",
                    level=IdentityAssurance.CLAIMED,
                ),
                WITNESS.accepted_rules[1],
            ),
        )
        result = _evaluate(
            mapping=divergent,
            observations=(
                _observation(),
                _observation(observation_id="obs-2", method="otp"),
            ),
        )
        self.assertEqual(
            result.identity_assurance, IdentityAssurance.CLAIMED
        )
        self.assertEqual(
            result.authentication_assurance,
            AuthenticationAssurance.MULTI_FACTOR,
        )

    def test_permutations_resultats_identiques(self) -> None:
        observations = (
            _observation(),
            _observation(observation_id="obs-2", method="saml"),
        )
        first = _evaluate(observations=observations)
        second = _evaluate(observations=tuple(reversed(observations)))
        self.assertEqual(first, second)
        rules = WITNESS.accepted_rules
        swapped = replace(WITNESS, accepted_rules=(rules[1], rules[0], rules[2]))
        result = _evaluate(
            mapping=swapped,
            observations=(_observation(), _observation(observation_id="obs-2")),
        )
        self.assertEqual(result.identity_assurance, IdentityAssurance.VERIFIED)
        self.assertEqual(
            result.authentication_assurance,
            AuthenticationAssurance.MULTI_FACTOR,
        )

    def test_conteneurs_et_dto_sous_classes_refuses_sans_iteration(self) -> None:
        with self.assertRaises(AssuranceMappingError):
            evaluate_assurance(WITNESS, _HookList([_observation()]), REF)
        with self.assertRaises(AssuranceMappingError):
            evaluate_assurance(
                replace(
                    WITNESS,
                    accepted_rules=_HookTuple((WITNESS.accepted_rules[0],)),
                ),
                (),
                REF,
            )
        with self.assertRaises(AssuranceMappingError):
            evaluate_assurance(_MetaHostile(), (), REF)
        with self.assertRaises(AssuranceMappingError):
            evaluate_assurance(WITNESS, (object.__new__(_HookDto),), REF)
        self.assertEqual(ITER_CALLS, [])
        self.assertEqual(GETATTR_CALLS, [])
        self.assertEqual(META_CALLS, [])

    def test_champs_etrangers_jamais_invokes(self) -> None:
        hook = _Hook()
        for overrides in (
            dict(provider_id=hook),
            dict(method=hook),
            dict(observation_id=hook),
            dict(status=hook),
        ):
            with self.assertRaises(AssuranceMappingError):
                _evaluate(observations=(_observation(**overrides),))
        empty = replace(WITNESS, provider_id="")
        with self.assertRaises(AssuranceMappingError):
            _evaluate(mapping=empty, observations=(_observation(),))
        self.assertEqual(
            EQ_CALLS + HASH_CALLS + STR_CALLS + REPR_CALLS + BOOL_CALLS
            + ITER_CALLS + CALL_CALLS,
            [],
        )

    def test_enums_forges_de_classe_exacte_refusees_avant_hash(self) -> None:
        forged = object.__new__(IdentityAssurance)
        object.__setattr__(forged, "_name_", _Hook())
        rule = AssuranceRule(
            dimension=AssuranceDimension.IDENTITY,
            method="webauthn",
            level=forged,
        )
        mapping = replace(WITNESS, accepted_rules=(rule,))
        with self.assertRaises(AssuranceMappingError):
            _evaluate(mapping=mapping, observations=(_observation(),))
        forged_dimension = object.__new__(AssuranceDimension)
        object.__setattr__(forged_dimension, "_name_", _Hook())
        rule2 = AssuranceRule(
            dimension=forged_dimension, method="webauthn",
            level=IdentityAssurance.VERIFIED,
        )
        with self.assertRaises(AssuranceMappingError):
            _evaluate(
                mapping=replace(WITNESS, accepted_rules=(rule2,)),
                observations=(_observation(),),
            )
        self.assertEqual(HASH_CALLS + EQ_CALLS + STR_CALLS, [])

    def test_dto_partiels_levent_erreur_constante(self) -> None:
        expected = (
            AssuranceMappingError.code,
            AssuranceMappingError.element,
            AssuranceMappingError.step,
            str(AssuranceMappingError()),
        )
        for mapping, observations in (
            (object.__new__(ProviderAssuranceMapping), ()),
            (WITNESS, (object.__new__(ProofObservation),)),
        ):
            with self.assertRaises(AssuranceMappingError) as caught:
                evaluate_assurance(mapping, observations, REF)
            error = caught.exception
            self.assertEqual(
                (error.code, error.element, error.step, str(error)), expected
            )
        with self.assertRaises(AssuranceMappingError) as caught:
            evaluate_assurance(
                replace(
                    WITNESS, accepted_rules=(object.__new__(AssuranceRule),)
                ),
                (),
                REF,
            )
        error = caught.exception
        self.assertEqual(
            (error.code, error.element, error.step, str(error)), expected
        )

    def test_erreurs_malformees_permutees_ont_les_memes_metadonnees(self) -> None:
        sentinel = "SENTINELLE_INVALIDE"
        invalid_mappings = (
            WITNESS,
            replace(WITNESS, provider_id=""),
            replace(WITNESS, valid_from=VALID_UNTIL),
        )
        invalid_observations = (
            _observation(status=sentinel),
            _observation(attested_at=EXPIRES),
        )
        expected = (
            AssuranceMappingError.code,
            AssuranceMappingError.element,
            AssuranceMappingError.step,
            str(AssuranceMappingError()),
        )
        for mapping, order in itertools.product(
            invalid_mappings, itertools.permutations(invalid_observations)
        ):
            with self.assertRaises(AssuranceMappingError) as caught:
                evaluate_assurance(mapping, order, REF)
            error = caught.exception
            self.assertEqual(
                (error.code, error.element, error.step, str(error)), expected
            )
            self.assertNotIn(sentinel, str(error))

    def test_champs_mapping_regles_et_plafond_forge_sans_appels(self) -> None:
        hook = _Hook()
        for overrides in (
            {"provider_id": hook},
            {"accepted_rules": hook},
            {"valid_from": hook},
            {"valid_until": hook},
            {"max_identity_assurance": hook},
            {"max_authentication_assurance": hook},
            {"max_federation_trust": hook},
        ):
            with self.assertRaises(AssuranceMappingError):
                evaluate_assurance(
                    replace(WITNESS, **overrides), (_observation(),), REF
                )
        forged_cap = object.__new__(IdentityAssurance)
        object.__setattr__(forged_cap, "_name_", hook)
        with self.assertRaises(AssuranceMappingError):
            evaluate_assurance(
                replace(WITNESS, max_identity_assurance=forged_cap),
                (_observation(),),
                REF,
            )
        for rule_kwargs in (
            {
                "dimension": hook,
                "method": "webauthn",
                "level": IdentityAssurance.VERIFIED,
            },
            {
                "dimension": AssuranceDimension.IDENTITY,
                "method": hook,
                "level": IdentityAssurance.VERIFIED,
            },
            {
                "dimension": AssuranceDimension.IDENTITY,
                "method": "webauthn",
                "level": hook,
            },
        ):
            with self.assertRaises(AssuranceMappingError):
                evaluate_assurance(
                    replace(
                        WITNESS,
                        accepted_rules=(AssuranceRule(**rule_kwargs),),
                    ),
                    (_observation(),),
                    REF,
                )
        self.assertEqual(
            EQ_CALLS
            + HASH_CALLS
            + STR_CALLS
            + REPR_CALLS
            + BOOL_CALLS
            + ITER_CALLS
            + CALL_CALLS
            + META_CALLS
            + UTCOFFSET_CALLS,
            [],
        )
    def test_invalid_rules_permuted_have_constant_errors(self) -> None:
        sentinel = "SENTINELLE_INVALIDE"
        rules = (
            AssuranceRule(AssuranceDimension.IDENTITY, "webauthn", sentinel),
            AssuranceRule(AssuranceDimension.AUTHENTICATION, "", AuthenticationAssurance.SINGLE_FACTOR),
        )
        expected = (AssuranceMappingError.code, AssuranceMappingError.element, AssuranceMappingError.step, str(AssuranceMappingError()))
        for order in itertools.permutations(rules):
            with self.assertRaises(AssuranceMappingError) as caught:
                evaluate_assurance(replace(WITNESS, accepted_rules=order), (_observation(),), REF)
            error = caught.exception
            self.assertEqual((error.code, error.element, error.step, str(error)), expected)
            self.assertNotIn(sentinel, str(error))


if __name__ == "__main__":
    unittest.main()
