"""Contrats de persistance Core C02 : V01/V06/V07/V12, mémoire seule, sans Django/IO."""

from __future__ import annotations

import datetime
import subprocess
import sys
import unittest
import uuid
from dataclasses import FrozenInstanceError

from pixs.core import contracts as core_contracts
from pixs.core import dto as core_dto
from pixs.core import ports as core_ports
from pixs.core.authz.filter_plan import FilterPlan
from pixs.core.dto import (
    BootstrapActInput,
    CoreInputInvalid,
    CoreQueryInput,
    GroupCreateInput,
    IdentityCreateIdentityInput,
    IdentityCreateUserInput,
    IdentityLinkInput,
    RoleAssignInput,
    RoleUnassignInput,
)
from pixs.core.identity.models import IdentityState, IdentityType
from pixs.core.persistence import uuid7 as uuid7mod
from pixs.core.persistence.uuid7 import Uuid7Error, check_uuid7, generate_uuid7
from pixs.core.ports import CorePortError, StagedRef, TransactionProof
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.kernel.contracts.models import ContractCategory, ContractDescriptor

EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


class Hostile:
    """Objet hostile : toute égalité ou représentation doit rester inexécutée."""

    def __eq__(self, other):
        raise AssertionError("eq hostile exécuté")

    def __repr__(self):
        raise AssertionError("repr hostile exécuté")


def _platform() -> ScopeContext:
    return ScopeContext(scope_type=ScopeType.PLATFORM)


def _tenant(name: str = "tenant-1") -> ScopeContext:
    return ScopeContext(scope_type=ScopeType.TENANT, tenant_id=name)


def _staged(ctx: ScopeContext, op: str = "op-1") -> StagedRef:
    return StagedRef(
        operation_id=op,
        alias="a1",
        transaction_token="tok-1",
        context=ctx,
        staged_kind="audit",
    )


def _proof(ctx: ScopeContext, op: str = "op-1") -> TransactionProof:
    return TransactionProof(
        operation_id=op,
        alias="a1",
        transaction_token="tok-1",
        context=ctx,
        staged=(_staged(ctx, op),),
        prepared_at=datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc),
    )


def _bootstrap(**over: object) -> BootstrapActInput:
    base: dict[str, object] = {
        "operation_id": "op-r01-1",
        "plan_version": "1.0.0",
        "installation_ref": "inst-1",
        "mode": "INSTALLER",
        "operator_proof_ref": "proof-1",
        "operator_subject_ref": "operator-1",
        "authorization_ref": "authz-1",
        "target_identity_ref": "identity-1",
        "target_tenant_ref": None,
        "closed_effects": ("core.identity.create",),
        "confirmations": (),
        "context": _platform(),
        "correlation_id": "corr-1",
        "causation_id": None,
        "idempotency_key": "idem-1",
        "content_sha256": EMPTY_SHA256,
        "serializer_version": "1.0.0",
    }
    base.update(over)
    return BootstrapActInput(**base)


class CorePersistenceContractsTest(unittest.TestCase):
    def test_import_facades_sans_django_ni_io(self) -> None:
        proc = subprocess.run(
            [
                sys.executable,
                "-B",
                "-c",
                "import os, sys\ndef guard(event, args):\n    if event.startswith(\"socket.\") or event == \"subprocess.Popen\":\n        raise AssertionError(\"Effet interdit a l import\")\n    if event == \"open\":\n        mode, flags = args[1], args[2]\n        if (isinstance(mode, str) and any(c in mode for c in \"wax+\")) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)):\n            raise AssertionError(\"Ecriture interdite a l import\")\nsys.addaudithook(guard)\nimport pixs.core.contracts, pixs.core.dto, pixs.core.ports, pixs.core.persistence.uuid7, pixs.core.persistence\nassert \"django\" not in sys.modules\nassert \"django.db\" not in sys.modules\nassert \"django.db.models\" not in sys.modules\n",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        import pixs.core.persistence as persistence_pkg

        self.assertEqual(tuple(persistence_pkg.__all__), ())

    def test_uuid7_valide_et_rejet_uuid4(self) -> None:
        made = generate_uuid7()
        self.assertIs(type(made), uuid.UUID)
        self.assertEqual(made.version, 7)
        self.assertEqual(made.variant, uuid.RFC_4122)
        self.assertTrue(check_uuid7(made))
        with self.assertRaises(Uuid7Error):
            check_uuid7(uuid.uuid4())
        for bad in ("x", b"x", 0, None, True, uuid.UUID(int=0)):
            with self.assertRaises(Uuid7Error):
                check_uuid7(bad)

    def test_immutabilite_frozen_slots_sans_repr(self) -> None:
        uid = generate_uuid7()
        obj = IdentityCreateUserInput(user_id=uid, correlation_id="c1")
        with self.assertRaises(FrozenInstanceError):
            obj.correlation_id = "c2"
        self.assertFalse(hasattr(obj, "__dict__"))
        self.assertIs(type(obj).__repr__, object.__repr__)
        proof = _proof(_platform())
        with self.assertRaises(FrozenInstanceError):
            proof.alias = "a2"

    def test_contrats_15_une_categorie_v100(self) -> None:
        all_contracts = core_contracts.ALL_CORE_CONTRACTS
        self.assertIs(type(all_contracts), tuple)
        self.assertEqual(len(all_contracts), 15)
        self.assertEqual(core_contracts.CONTRACT_VERSION, "1.0.0")
        commands = queries = services = 0
        seen: set[str] = set()
        for desc in all_contracts:
            self.assertIs(type(desc), ContractDescriptor)
            self.assertNotIn(desc.contract_id, seen)
            seen.add(desc.contract_id)
            self.assertTrue(desc.contract_id.startswith("pixs.core."))
            self.assertEqual(desc.owner_component, "pixs.core")
            self.assertEqual(desc.version, "1.0.0")
            self.assertTrue(any(desc.category is m for m in ContractCategory))
            if desc.category is ContractCategory.COMMAND:
                commands += 1
            elif desc.category is ContractCategory.QUERY:
                queries += 1
            elif desc.category is ContractCategory.SERVICE:
                services += 1
            else:
                self.fail("catégorie inattendue : %r" % (desc.category,))
        self.assertEqual((commands, queries, services), (5, 5, 5))

    def test_preuve_sur_autre_contexte_refusee(self) -> None:
        platform = _platform()
        tenant = _tenant()
        staged = _staged(platform)
        with self.assertRaises(CorePortError):
            TransactionProof(
                operation_id="op-1",
                alias="a1",
                transaction_token="tok-1",
                context=tenant,
                staged=(staged,),
                prepared_at=datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc),
            )
        other_op = _staged(platform, op="op-2")
        with self.assertRaises(CorePortError):
            TransactionProof(
                operation_id="op-1",
                alias="a1",
                transaction_token="tok-1",
                context=platform,
                staged=(other_op,),
                prepared_at=datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc),
            )
        with self.assertRaises(CorePortError):
            TransactionProof(
                operation_id="op-1",
                alias="a1",
                transaction_token="tok-1",
                context=platform,
                staged=(),
                prepared_at=datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc),
            )

    def test_r01_reutilisation_sans_tenant_sans_creation_implicite(self) -> None:
        # Structure seule : ne prouve aucun parcours de réutilisation runtime.
        ok = _bootstrap(target_tenant_ref=None, closed_effects=("synthetic:reuse_existing",))
        self.assertIsNone(ok.target_tenant_ref)
        with self.assertRaises(CoreInputInvalid):
            _bootstrap(target_tenant_ref="")
        with self.assertRaises(CoreInputInvalid):
            _bootstrap(mode="OTHER")
        with self.assertRaises(CoreInputInvalid):
            _bootstrap(context=_tenant())
        with self.assertRaises(CoreInputInvalid):
            _bootstrap(closed_effects=())
        with self.assertRaises(CoreInputInvalid):
            _bootstrap(closed_effects=("a", "a"))

    def test_refus_mal_types_sans_eq_repr_hostile(self) -> None:
        uid = generate_uuid7()
        with self.assertRaises(CoreInputInvalid):
            IdentityCreateUserInput(user_id=Hostile(), correlation_id="c1")
        with self.assertRaises(CoreInputInvalid):
            IdentityCreateUserInput(user_id=uid, correlation_id=Hostile())
        with self.assertRaises(CoreInputInvalid):
            IdentityCreateIdentityInput(
                identity_id=uid,
                identity_type=Hostile(),
                state=IdentityState.ACTIVE,
                correlation_id="c1",
            )
        with self.assertRaises(CoreInputInvalid):
            IdentityLinkInput(user_id=uid, identity_id=Hostile(), correlation_id="c1")
        with self.assertRaises(CoreInputInvalid):
            GroupCreateInput(group_id=uid, context=Hostile(), correlation_id="c1")
        with self.assertRaises(CoreInputInvalid):
            CoreQueryInput(
                context=_platform(),
                correlation_id="c1",
                resource_refs=("r1", Hostile()),
                filter_plan=None,
            )
        with self.assertRaises(CoreInputInvalid):
            CoreQueryInput(
                context=_platform(),
                correlation_id="c1",
                resource_refs=("r1",),
                filter_plan=Hostile(),
            )
        for input_type in (RoleAssignInput, RoleUnassignInput):
            expected = {"expected_version": 1} if input_type is RoleUnassignInput else {}
            with self.assertRaises(CoreInputInvalid):
                input_type(role_id="role-1", subject_type=Hostile(),
                           subject_ref="subject-1", correlation_id="c1", **expected)
        for bad_version in (None, True, False, 0, -1, Hostile()):
            with self.assertRaises(CoreInputInvalid):
                RoleUnassignInput(role_id="role-1", subject_type="USER",
                                  subject_ref="subject-1", correlation_id="c1",
                                  expected_version=bad_version)
        with self.assertRaises(Uuid7Error):
            check_uuid7(Hostile())
        with self.assertRaises(CorePortError):
            StagedRef(
                operation_id=Hostile(),
                alias="a1",
                transaction_token="tok-1",
                context=_platform(),
                staged_kind="audit",
            )

    def test_ports_absents_refuses(self) -> None:
        with self.assertRaises(CorePortError):
            core_ports.CoreServicePorts(
                facts_provider=None,
                clock=None,
                decider=None,
                filter_provider=None,
                audit=None,
                idempotence=None,
                outbox=None,
            )
        with self.assertRaises(CorePortError):
            core_ports.BootstrapServicePorts(
                operator=None,
                decider=None,
                plans=None,
                stamper=None,
                clock=None,
                audit=None,
                idempotence=None,
                outbox=None,
            )


if __name__ == "__main__":
    unittest.main()
