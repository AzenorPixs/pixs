"""Tests 2.1 : nominal, limites et refus hostiles des contrats C09."""

import datetime
import unittest

from pixs.backend.c09_contracts import (
    C09ConsumerDeclarationV1,
    C09EventBindingV1,
    C09PolicyV1,
    C09RoleDeclarationV1,
    validate_c09_consumer_declaration,
    validate_c09_event_binding,
    validate_c09_policy,
    validate_c09_role_declaration,
)
from pixs.backend.c09_registry import C09RegistryV1, validate_c09_registry
from pixs.kernel.event_contract import DomainEventContract

_INT32_MAX = 2**31 - 1


def _policy(**overrides: object) -> C09PolicyV1:
    base: dict[str, object] = {
        "policy_reference": "c09-policy",
        "policy_version": "1.0.0",
        "lease_seconds": 60,
        "renewal_seconds": 20,
        "max_attempts": 3,
        "retry_delays_seconds": (5, 10),
        "polling_interval_ms": 500,
        "polling_max_batch": 10,
        "max_concurrency": 4,
        "max_units_per_poll": 10,
        "drain_seconds": 30,
        "attempt_timeout_seconds": 20,
        "job_timeout_seconds": 60,
        "process_count": 4,
        "cpu_millicores": 1000,
        "max_connections": 20,
        "memory_mb": 512,
        "effective_from": datetime.datetime(
            2026, 10, 22, tzinfo=datetime.timezone.utc
        ),
    }
    base.update(overrides)
    return C09PolicyV1(**base)  # type: ignore[arg-type]


def _contract(**overrides: object) -> DomainEventContract:
    base: dict[str, object] = {
        "event_type": "job finished",
        "contract_version": "1.0.0",
        "producer_reference": "pixs.jobs",
        "schema_reference": "pixs.schemas.job",
        "order_scope_reference": "tenant-a",
    }
    base.update(overrides)
    return DomainEventContract(**base)  # type: ignore[arg-type]


def _binding(**overrides: object) -> C09EventBindingV1:
    base: dict[str, object] = {
        "owner_reference": "owner-a",
        "entry_reference": "entry-a",
        "contract": _contract(),
        "perimeter_reference": "perimeter-a",
        "tenant_context_reference": None,
    }
    base.update(overrides)
    return C09EventBindingV1(**base)  # type: ignore[arg-type]


def _consumer(**overrides: object) -> C09ConsumerDeclarationV1:
    base: dict[str, object] = {
        "consumer_reference": "consumer-a",
        "entry_reference": "entry-a",
        "consumer_version": "3.0.0",
        "component_reference": "pixs.consumer.synthetic",
        "event_contract_version": "1.0.0",
    }
    base.update(overrides)
    return C09ConsumerDeclarationV1(**base)  # type: ignore[arg-type]


def _role(
    ref: str = "pixs.jobs.run",
    role: str = "worker",
) -> C09RoleDeclarationV1:
    return C09RoleDeclarationV1(
        role=role,
        handler_reference=ref,
        handler_version="1.0.0",
        component_reference="pixs.backend.c09_worker",
    )


class HostileStr(str):
    def __eq__(self, other: object) -> bool:
        raise AssertionError("hostile eq called")

    def __hash__(self) -> int:
        raise AssertionError("hostile hash called")

    def __bool__(self) -> bool:
        raise AssertionError("hostile bool called")

    def __repr__(self) -> str:
        raise AssertionError("hostile repr called")

    def __str__(self) -> str:
        raise AssertionError("hostile str called")


class C09PolicyTests(unittest.TestCase):
    def test_nominal(self) -> None:
        self.assertEqual(validate_c09_policy(_policy()), [])

    def test_extreme_int32(self) -> None:
        self.assertEqual(
            validate_c09_policy(
                _policy(
                    lease_seconds=_INT32_MAX,
                    renewal_seconds=1,
                    max_attempts=1,
                    retry_delays_seconds=(),
                    polling_interval_ms=_INT32_MAX,
                    polling_max_batch=1,
                    max_concurrency=1,
                    max_units_per_poll=1,
                    drain_seconds=1,
                    attempt_timeout_seconds=1,
                    job_timeout_seconds=1,
                    process_count=1,
                    cpu_millicores=1,
                    max_connections=1,
                    memory_mb=1,
                )
            ),
            [],
        )

    def test_zero_et_depassement_refuses(self) -> None:
        self.assertTrue(validate_c09_policy(_policy(lease_seconds=0)))
        self.assertTrue(validate_c09_policy(_policy(lease_seconds=_INT32_MAX + 1)))

    def test_bool_refuse(self) -> None:
        self.assertTrue(validate_c09_policy(_policy(lease_seconds=True)))

    def test_sous_classe_str_refusee(self) -> None:
        self.assertTrue(validate_c09_policy(_policy(policy_reference=HostileStr("x"))))

    def test_conteneur_mutable_refuse(self) -> None:
        self.assertTrue(validate_c09_policy(_policy(retry_delays_seconds=[5, 10])))

    def test_longueur_delais_explicite(self) -> None:
        self.assertTrue(validate_c09_policy(_policy(retry_delays_seconds=(5,))))

    def test_coherences(self) -> None:
        self.assertTrue(validate_c09_policy(_policy(lease_seconds=30, renewal_seconds=20)))
        self.assertTrue(
            validate_c09_policy(_policy(attempt_timeout_seconds=60, job_timeout_seconds=20))
        )
        self.assertTrue(
            validate_c09_policy(_policy(polling_max_batch=11, max_units_per_poll=10))
        )
        self.assertEqual(
            validate_c09_policy(_policy(max_concurrency=5, process_count=4)), []
        )

    def test_naive_et_tz_etrangere_refusees_sans_appel(self) -> None:
        self.assertTrue(
            validate_c09_policy(
                _policy(effective_from=datetime.datetime(2026, 10, 22))
            )
        )
        other = datetime.timezone(datetime.timedelta(hours=1))
        self.assertTrue(
            validate_c09_policy(
                _policy(
                    effective_from=datetime.datetime(
                        2026, 10, 22, tzinfo=other
                    )
                )
            )
        )

    def test_espaces_unicode_casse_preserves(self) -> None:
        policy = _policy(policy_reference="  C09-Été  ")
        self.assertEqual(validate_c09_policy(policy), [])
        self.assertEqual(policy.policy_reference, "  C09-Été  ")


class C09BindingTests(unittest.TestCase):
    def test_nominal(self) -> None:
        self.assertEqual(validate_c09_event_binding(_binding()), [])

    def test_contrat_porte_invalide_refuse(self) -> None:
        self.assertTrue(
            validate_c09_event_binding(_binding(contract=_contract(event_type="")))
        )

    def test_contrat_etranger_refuse(self) -> None:
        self.assertTrue(
            validate_c09_event_binding(_binding(contract=object()))
        )

    def test_vide_et_sous_classe_hostile(self) -> None:
        self.assertTrue(validate_c09_event_binding(_binding(owner_reference="")))
        self.assertTrue(
            validate_c09_event_binding(_binding(owner_reference=HostileStr("x")))
        )


class C09RoleConsumerRegistryTests(unittest.TestCase):
    def test_role_nominal(self) -> None:
        self.assertEqual(validate_c09_role_declaration(_role()), [])

    def test_role_hostile_egalite_non_appelee(self) -> None:
        hostile = HostileStr("worker")
        diags = validate_c09_role_declaration(
            C09RoleDeclarationV1(
                role=hostile,  # type: ignore[arg-type]
                handler_reference="pixs.jobs.run",
                handler_version="1.0.0",
                component_reference="pixs.backend.c09_worker",
            )
        )
        self.assertTrue(diags)

    def test_consommateur_nominal_et_liaison(self) -> None:
        registry = C09RegistryV1(
            roles=(_role(),),
            bindings=(_binding(),),
            consumers=(_consumer(),),
        )
        self.assertEqual(validate_c09_registry(registry), [])

    def test_consommateur_sans_contrat_refuse(self) -> None:
        registry = C09RegistryV1(
            roles=(_role(),),
            bindings=(),
            consumers=(_consumer(),),
        )
        self.assertTrue(validate_c09_registry(registry))

    def test_consommateur_version_incompatible_refusee(self) -> None:
        registry = C09RegistryV1(
            roles=(_role(),),
            bindings=(_binding(),),
            consumers=(_consumer(event_contract_version="2.0.0"),),
        )
        self.assertTrue(validate_c09_registry(registry))

    def test_collisions(self) -> None:
        registry = C09RegistryV1(
            roles=(_role("pixs.jobs.run"), _role("pixs.jobs.run")),
            bindings=(_binding(),),
            consumers=(),
        )
        self.assertTrue(validate_c09_registry(registry))
        registry = C09RegistryV1(
            roles=(_role(),),
            bindings=(_binding(), _binding()),
            consumers=(),
        )
        self.assertTrue(validate_c09_registry(registry))
        registry = C09RegistryV1(
            roles=(_role(),),
            bindings=(_binding(),),
            consumers=(_consumer(), _consumer()),
        )
        self.assertTrue(validate_c09_registry(registry))

    def test_jobs_sans_evenement_autorise(self) -> None:
        registry = C09RegistryV1(roles=(_role(),), bindings=(), consumers=())
        self.assertEqual(validate_c09_registry(registry), [])



class HostileValue:
    def __eq__(self, other):
        raise AssertionError("égalité étrangère appelée")
    def __hash__(self):
        raise AssertionError("hachage étranger appelé")
    def __bool__(self):
        raise AssertionError("conversion étrangère appelée")
    def __repr__(self):
        raise AssertionError("représentation étrangère appelée")
    def __str__(self):
        raise AssertionError("chaîne étrangère appelée")


class C09BoundaryTests(unittest.TestCase):
    def test_fields_hostiles_sans_methode(self):
        fields = (
            "lease_seconds", "renewal_seconds", "max_attempts",
            "polling_interval_ms", "polling_max_batch", "max_concurrency",
            "max_units_per_poll", "drain_seconds", "attempt_timeout_seconds",
            "job_timeout_seconds", "process_count", "cpu_millicores",
            "max_connections", "memory_mb", "effective_from",
            "policy_reference", "policy_version",
        )
        for field in fields:
            with self.subTest(field=field):
                self.assertTrue(validate_c09_policy(_policy(**{field: HostileValue()})))
        self.assertTrue(validate_c09_policy(_policy(retry_delays_seconds=(HostileValue(), 1))))
        for candidate, validator in (
            (HostileValue(), validate_c09_policy),
            (HostileValue(), validate_c09_registry),
            (HostileValue(), validate_c09_role_declaration),
            (HostileValue(), validate_c09_event_binding),
            (HostileValue(), validate_c09_consumer_declaration),
        ):
            self.assertTrue(validator(candidate))

    def test_registry_refuse_avant_tri_hachage(self):
        from dataclasses import replace
        bad_role = replace(_role(), handler_reference=HostileValue())
        bad_binding = _binding(entry_reference=HostileValue())
        bad_consumer = _consumer(consumer_reference=HostileValue())
        self.assertTrue(validate_c09_registry(C09RegistryV1(
            roles=(bad_role,), bindings=(bad_binding,), consumers=(bad_consumer,))))

    def test_tzinfo_hostile_non_appele(self):
        class HostileTimezone(datetime.tzinfo):
            def utcoffset(self, value):
                raise AssertionError("zone étrangère appelée")
        date = datetime.datetime(2026, 1, 1, tzinfo=HostileTimezone())
        self.assertTrue(validate_c09_policy(_policy(effective_from=date)))

    def test_valeurs_valides_immuables(self):
        from dataclasses import FrozenInstanceError
        policy = _policy()
        with self.assertRaises(FrozenInstanceError):
            policy.lease_seconds = 99
        with self.assertRaises(TypeError):
            policy.retry_delays_seconds[0] = 99

    def test_version_consommateur_distincte_evenement(self):
        registry = C09RegistryV1(
            roles=(), bindings=(_binding(),),
            consumers=(_consumer(consumer_version="9.2.1", event_contract_version="1.0.0"),))
        self.assertEqual(validate_c09_registry(registry), [])
        self.assertTrue(validate_c09_consumer_declaration(
            _consumer(component_reference=HostileValue())))



class C09DeclaredContractTests(unittest.TestCase):
    def test_domain_integration_restant_distincts(self):
        from pixs.kernel.event_contract import IntegrationEventContract
        domain = _contract()
        integration = IntegrationEventContract(
            domain.event_type, domain.contract_version, domain.producer_reference,
            domain.schema_reference, domain.order_scope_reference)
        binding = _binding(contract=integration)
        self.assertEqual(validate_c09_event_binding(binding), [])
        self.assertIs(binding.contract, integration)
        self.assertIs(type(binding.contract), IntegrationEventContract)
        self.assertIs(type(domain), DomainEventContract)

    def test_semver_invalide_et_diagnostics_stables(self):
        value = _policy(policy_version="1", lease_seconds=False)
        first = validate_c09_policy(value)
        self.assertTrue(first)
        self.assertEqual(first, validate_c09_policy(value))
        keys = [(d.element, d.constraint, d.message) for d in first]
        self.assertEqual(keys, sorted(set(keys)))
        self.assertTrue(validate_c09_event_binding(
            _binding(contract=_contract(contract_version="1"))))

    def test_ordre_non_trie_refuse_sans_normalisation(self):
        registry = C09RegistryV1(
            roles=(_role("z"), _role("a")), bindings=(), consumers=())
        self.assertTrue(validate_c09_registry(registry))
        self.assertEqual(registry.roles[0].handler_reference, "z")

    def test_conteneurs_etrangers_refuses(self):
        self.assertTrue(validate_c09_registry(C09RegistryV1(
            roles=[_role()], bindings=(), consumers=())))
        class TupleSubclass(tuple):
            def __iter__(self):
                raise AssertionError("itération étrangère appelée")
        self.assertTrue(validate_c09_registry(C09RegistryV1(
            roles=TupleSubclass((_role(),)), bindings=(), consumers=())))


if __name__ == "__main__":
    unittest.main()
