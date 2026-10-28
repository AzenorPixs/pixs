"""Tests locaux de delegation vers le producteur courant, sans produit reel.

Aucune qualification de produit, source, canal ou intervalle reel.
Doubles seulement pour logique locale, refus et ordre d'appel.
"""

from __future__ import annotations

import datetime
import unittest

from pixs.core.time_guard import _TimeUseGuard
from pixs.kernel.contracts.models import ContractDescriptorError
from pixs.kernel.contracts.time import TimeDiagnostic, TimeDoubtError, TimeOutcome, TimePublicRef, TimeRefusedError


class EvilStr(str):
    pass


class HostileObject:
    def __getattribute__(self, name: str) -> object:
        raise AssertionError("acces hostile")

    def __repr__(self) -> str:
        raise AssertionError("repr hostile")

    def __bool__(self) -> bool:
        raise AssertionError("bool hostile")


class SubRef(TimePublicRef):
    pass


def _ref(value: str = "usage-courant") -> TimePublicRef:
    return TimePublicRef(value)


_FIXED_DATE = datetime.datetime(2026, 1, 1, tzinfo=datetime.timezone.utc)


class _Ok:
    def __init__(self) -> None:
        self.calls: list[object] = []

    def time_require_use(self, use_ref: TimePublicRef) -> None:
        self.calls.append(use_ref)
        return None


class _Refuse:
    def __init__(self, exc: BaseException) -> None:
        self.exc = exc
        self.calls = 0

    def time_require_use(self, use_ref: TimePublicRef) -> None:
        self.calls += 1
        raise self.exc


class _Return:
    def __init__(self, value: object) -> None:
        self.value = value

    def time_require_use(self, use_ref: TimePublicRef) -> object:
        return self.value


class DelegationTest(unittest.TestCase):
    def test_succes_retour_none(self) -> None:
        producer = _Ok()
        guard = _TimeUseGuard(producer)
        ref = _ref()
        self.assertIsNone(guard.require_use(ref))
        self.assertEqual(producer.calls, [ref])

    def test_ref_forgee_sans_effet(self) -> None:
        producer = _Ok()
        guard = _TimeUseGuard(producer)
        forged_empty = object.__new__(TimePublicRef)
        object.__setattr__(forged_empty, "value", "")
        with self.assertRaises(ContractDescriptorError):
            guard.require_use(forged_empty)  # type: ignore[arg-type]
        forged_nul = object.__new__(TimePublicRef)
        object.__setattr__(forged_nul, "value", "a\x00b")
        with self.assertRaises(ContractDescriptorError):
            guard.require_use(forged_nul)  # type: ignore[arg-type]
        forged_surrogate = object.__new__(TimePublicRef)
        object.__setattr__(forged_surrogate, "value", "\ud800")
        with self.assertRaises(ContractDescriptorError):
            guard.require_use(forged_surrogate)  # type: ignore[arg-type]
        forged_long = object.__new__(TimePublicRef)
        object.__setattr__(forged_long, "value", "\u00e9" * 129)
        with self.assertRaises(ContractDescriptorError):
            guard.require_use(forged_long)  # type: ignore[arg-type]
        forged_missing = object.__new__(TimePublicRef)
        with self.assertRaises(ContractDescriptorError):
            guard.require_use(forged_missing)  # type: ignore[arg-type]
        self.assertEqual(producer.calls, [])

    def test_limite_256_octets_valide(self) -> None:
        producer = _Ok()
        guard = _TimeUseGuard(producer)
        ref_a = _ref("a" * 256)
        ref_e = _ref("\u00e9" * 128)
        self.assertIsNone(guard.require_use(ref_a))
        self.assertIsNone(guard.require_use(ref_e))
        self.assertEqual(producer.calls, [ref_a, ref_e])

    def test_types_hostiles_sans_effet(self) -> None:
        producer = _Ok()
        guard = _TimeUseGuard(producer)
        for bad in (None, 1, b"a", EvilStr("ok"), HostileObject(), SubRef("ok")):
            with self.assertRaises(ContractDescriptorError):
                guard.require_use(bad)  # type: ignore[arg-type]
        self.assertEqual(producer.calls, [])

    def test_retours_parasites_refuses(self) -> None:
        ref = _ref()
        diag = TimeDiagnostic(TimeOutcome.OBSERVED, _ref("p"), _ref("c"), _ref("d"))
        for bad in (diag, True, _FIXED_DATE):
            guard = _TimeUseGuard(_Return(bad))
            with self.assertRaises(ContractDescriptorError):
                guard.require_use(ref)

    def test_refus_et_doute_propages_identiques(self) -> None:
        ref = _ref()
        refused = TimeRefusedError("TIME_UNVERIFIABLE")
        guard = _TimeUseGuard(_Refuse(refused))
        with self.assertRaises(TimeRefusedError) as ctx:
            guard.require_use(ref)
        self.assertIs(ctx.exception, refused)
        state = _ref("etat-courant")
        doubt = TimeDoubtError(state)
        guard2 = _TimeUseGuard(_Refuse(doubt))
        with self.assertRaises(TimeDoubtError) as ctx2:
            guard2.require_use(ref)
        self.assertIs(ctx2.exception, doubt)

    def test_erreur_inattendue_propagee(self) -> None:
        ref = _ref()
        boom = RuntimeError("panne locale")
        guard = _TimeUseGuard(_Refuse(boom))
        with self.assertRaises(RuntimeError) as ctx:
            guard.require_use(ref)
        self.assertIs(ctx.exception, boom)

    def test_methode_courante_a_chaque_usage(self) -> None:
        ref = _ref()
        first_calls: list[object] = []
        second_calls: list[object] = []

        def first(use: TimePublicRef) -> None:
            first_calls.append(use)
            return None

        def second(use: TimePublicRef) -> None:
            second_calls.append(use)
            return None

        class Changeant:
            def __init__(self) -> None:
                self.time_require_use = first  # type: ignore[method-assign]

        producer = Changeant()
        guard = _TimeUseGuard(producer)
        guard.require_use(ref)
        self.assertEqual(len(first_calls), 1)
        producer.time_require_use = second  # type: ignore[method-assign]
        guard.require_use(ref)
        self.assertEqual(len(first_calls), 1)
        self.assertEqual(second_calls, [ref])

    def test_methode_retiree_ou_non_appelable_sans_cache(self) -> None:
        ref = _ref()

        class _OkInstance:
            def __init__(self) -> None:
                self.calls: list[object] = []

                def _impl(use: TimePublicRef) -> None:
                    self.calls.append(use)
                    return None

                self.time_require_use = _impl  # type: ignore[method-assign]

        producer = _OkInstance()
        guard = _TimeUseGuard(producer)
        guard.require_use(ref)
        self.assertEqual(len(producer.calls), 1)
        del producer.time_require_use  # type: ignore[attr-defined]
        with self.assertRaises(ContractDescriptorError):
            guard.require_use(ref)
        self.assertEqual(len(producer.calls), 1)
        producer2 = _Ok()
        guard2 = _TimeUseGuard(producer2)
        producer2.time_require_use = 1  # type: ignore[method-assign]
        with self.assertRaises(ContractDescriptorError):
            guard2.require_use(ref)
        self.assertEqual(producer2.calls, [])

    def test_construction_invalide(self) -> None:
        with self.assertRaises(ContractDescriptorError):
            _TimeUseGuard(None)
        with self.assertRaises(ContractDescriptorError):
            _TimeUseGuard(1)

        class SansMethode:
            pass

        with self.assertRaises(ContractDescriptorError):
            _TimeUseGuard(SansMethode())

        class NonCallable:
            time_require_use = 1

        with self.assertRaises(ContractDescriptorError):
            _TimeUseGuard(NonCallable())


if __name__ == "__main__":
    unittest.main()
