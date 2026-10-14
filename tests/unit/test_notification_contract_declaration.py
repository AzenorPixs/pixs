"""Tests unitaires de la liaison declarative des gardes au contrat valide."""

import unittest
from dataclasses import replace

from pixs.kernel import notification_contract_declaration as declaration
from pixs.kernel.notification_channel_declaration import (
    NotificationChannelDeclarationError,
)
from pixs.kernel.notification_contract import NotificationContract
from pixs.kernel.notification_contract_declaration import (
    NotificationContractDeclarationError,
    require_contract_declared_channel,
    require_contract_declared_recipient,
)
from pixs.kernel.notification_recipient_declaration import (
    NotificationRecipientDeclarationError,
)
from pixs.kernel.notifications import NotificationChannel

_MSG_INVALID = "contrat de notification valide exact attendu"
_MSG_CHANNEL_MEMBER = "channel : membre NotificationChannel attendu"
_MSG_CHANNEL_UNDECLARED = "channel : membre non declare par declared_channels"
_MSG_RECIPIENT_KEY = "recipient_key : cle exacte non vide attendue"
_MSG_RECIPIENT_UNDECLARED = (
    "recipient_key : cle non declaree par declared_recipient_keys"
)

VALID_CONTRACT = NotificationContract(
    "1.0.0",
    frozenset({"ALPHA"}),
    frozenset({NotificationChannel.EMAIL}),
    "pref",
    "perim",
)
EMPTY_CONTRACT = NotificationContract(
    "1.0.0",
    frozenset(),
    frozenset(),
    "pref",
    "perim",
)


class _HostileFrozenSet(frozenset):
    def __iter__(self):
        raise AssertionError("iteration invoquee sur conteneur invalide")


class _HostileKey(str):
    def __eq__(self, other):
        raise AssertionError("__eq__ invoque")

    def __hash__(self):
        raise AssertionError("__hash__ invoque")

    def __str__(self):
        raise AssertionError("__str__ invoque")

    def __repr__(self):
        raise AssertionError("__repr__ invoque")


class _HostileArgument:
    def __eq__(self, other):
        raise AssertionError("__eq__ invoque")

    def __hash__(self):
        raise AssertionError("__hash__ invoque")

    def __str__(self):
        raise AssertionError("__str__ invoque")

    def __repr__(self):
        raise AssertionError("__repr__ invoque")


class _ForeignContractType:
    def __getattribute__(self, name):
        raise AssertionError("attribut lu avant validation du type exact")


class _ContractSubclass(NotificationContract):
    pass


def _invalid_contract_cases():
    return [
        ("version", replace(VALID_CONTRACT, contract_version="MARKER-VERSION")),
        (
            "recipient_keys",
            replace(VALID_CONTRACT, recipient_keys=_HostileFrozenSet({"ALPHA"})),
        ),
        (
            "channels",
            replace(VALID_CONTRACT, channels=_HostileFrozenSet({NotificationChannel.EMAIL})),
        ),
        ("preference_reference", replace(VALID_CONTRACT, preference_reference="")),
        ("perimeter_reference", replace(VALID_CONTRACT, perimeter_reference="")),
    ]


class TestContractDeclarationGate(unittest.TestCase):
    def test_channel_declared_returns_identity(self):
        self.assertIs(
            require_contract_declared_channel(VALID_CONTRACT, NotificationChannel.EMAIL),
            NotificationChannel.EMAIL,
        )

    def test_recipient_declared_returns_identity(self):
        recipient_key = "".join(("AL", "PHA"))
        self.assertIs(require_contract_declared_recipient(VALID_CONTRACT, recipient_key), recipient_key)

    def test_undeclared_channel_refusal_class_and_message(self):
        with self.assertRaises(NotificationChannelDeclarationError) as ctx:
            require_contract_declared_channel(VALID_CONTRACT, NotificationChannel.SMS)
        self.assertIs(type(ctx.exception), NotificationChannelDeclarationError)
        self.assertEqual(str(ctx.exception), _MSG_CHANNEL_UNDECLARED)

    def test_undeclared_recipient_refusal_class_and_message(self):
        with self.assertRaises(NotificationRecipientDeclarationError) as ctx:
            require_contract_declared_recipient(VALID_CONTRACT, "BRAVO")
        self.assertIs(type(ctx.exception), NotificationRecipientDeclarationError)
        self.assertEqual(str(ctx.exception), _MSG_RECIPIENT_UNDECLARED)

    def test_empty_declared_sets_valid_but_refused(self):
        with self.assertRaises(NotificationChannelDeclarationError) as ctx:
            require_contract_declared_channel(EMPTY_CONTRACT, NotificationChannel.EMAIL)
        self.assertEqual(str(ctx.exception), _MSG_CHANNEL_UNDECLARED)
        with self.assertRaises(NotificationRecipientDeclarationError) as ctx:
            require_contract_declared_recipient(EMPTY_CONTRACT, "ALPHA")
        self.assertEqual(str(ctx.exception), _MSG_RECIPIENT_UNDECLARED)

    def test_five_invalid_fields_rejected_by_both_guards(self):
        for field, invalid_contract in _invalid_contract_cases():
            with self.subTest(field=field):
                with self.assertRaises(NotificationContractDeclarationError) as ctx:
                    require_contract_declared_channel(invalid_contract, NotificationChannel.EMAIL)
                self.assertIs(type(ctx.exception), NotificationContractDeclarationError)
                self.assertEqual(str(ctx.exception), _MSG_INVALID)
                with self.assertRaises(NotificationContractDeclarationError) as ctx:
                    require_contract_declared_recipient(invalid_contract, "ALPHA")
                self.assertIs(type(ctx.exception), NotificationContractDeclarationError)
                self.assertEqual(str(ctx.exception), _MSG_INVALID)

    def test_foreign_contract_type_rejected_before_attribute_read(self):
        for foreign in (object(), _ForeignContractType()):
            with self.subTest(foreign=type(foreign).__name__):
                with self.assertRaises(NotificationContractDeclarationError) as ctx:
                    require_contract_declared_channel(foreign, NotificationChannel.EMAIL)
                self.assertEqual(str(ctx.exception), _MSG_INVALID)
                with self.assertRaises(NotificationContractDeclarationError) as ctx:
                    require_contract_declared_recipient(foreign, "ALPHA")
                self.assertEqual(str(ctx.exception), _MSG_INVALID)

    def test_contract_subclass_rejected(self):
        subclassed = _ContractSubclass(
            "1.0.0",
            frozenset({"ALPHA"}),
            frozenset({NotificationChannel.EMAIL}),
            "pref",
            "perim",
        )
        with self.assertRaises(NotificationContractDeclarationError) as ctx:
            require_contract_declared_channel(subclassed, NotificationChannel.EMAIL)
        self.assertEqual(str(ctx.exception), _MSG_INVALID)
        with self.assertRaises(NotificationContractDeclarationError) as ctx:
            require_contract_declared_recipient(subclassed, "ALPHA")
        self.assertEqual(str(ctx.exception), _MSG_INVALID)

    def test_valid_contract_with_hostile_argument_gives_clean_guard_error(self):
        with self.assertRaises(NotificationChannelDeclarationError) as ctx:
            require_contract_declared_channel(VALID_CONTRACT, _HostileArgument())
        self.assertEqual(str(ctx.exception), _MSG_CHANNEL_MEMBER)
        with self.assertRaises(NotificationRecipientDeclarationError) as ctx:
            require_contract_declared_recipient(VALID_CONTRACT, _HostileKey("ALPHA"))
        self.assertEqual(str(ctx.exception), _MSG_RECIPIENT_KEY)

    def test_invalid_contract_error_priority_over_hostile_argument(self):
        invalid_contract = replace(VALID_CONTRACT, contract_version="MARKER-VERSION")
        with self.assertRaises(NotificationContractDeclarationError) as ctx:
            require_contract_declared_channel(invalid_contract, _HostileArgument())
        self.assertEqual(str(ctx.exception), _MSG_INVALID)
        with self.assertRaises(NotificationContractDeclarationError) as ctx:
            require_contract_declared_recipient(invalid_contract, _HostileKey("ALPHA"))
        self.assertEqual(str(ctx.exception), _MSG_INVALID)

    def test_all_exports_exact(self):
        self.assertEqual(
            sorted(declaration.__all__),
            sorted(
                [
                    "NotificationContractDeclarationError",
                    "require_contract_declared_channel",
                    "require_contract_declared_recipient",
                ]
            ),
        )


if __name__ == "__main__":
    unittest.main()
