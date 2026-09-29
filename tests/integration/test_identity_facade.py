"""Usage des contrats identité par un consommateur de la façade publique."""

import unittest
import uuid

import pixs.core as core
from pixs.core import identity
from pixs.core import scope


def u7(n):
    return uuid.UUID(int=(7 << 76) | (2 << 62) | n)


class IdentityFacadeTest(unittest.TestCase):
    def test_public_exports_and_existing_scope_preserved(self):
        expected = {"User", "DigitalIdentity", "IdentityLink", "IdentityType",
                    "IdentityState", "IdentityError", "validate_user",
                    "validate_identity", "validate_link", "validate_links",
                    "Group", "Membership", "GroupError", "validate_group",
                    "validate_membership", "validate_memberships"}
        self.assertEqual(set(identity.__all__), expected)
        self.assertIs(core.identity, identity)
        self.assertIs(core.scope, scope)
        self.assertIn("identity", core.__all__)
        self.assertIn("scope", core.__all__)
        self.assertNotIn("models", identity.__all__)
        for name in expected:
            self.assertTrue(hasattr(identity, name))
        self.assertTrue(scope.validate_structure(scope.ScopeContext(scope.ScopeType.PLATFORM)))

    def test_consumer_builds_optional_then_explicit_link(self):
        user = identity.User(u7(1))
        ident = identity.DigitalIdentity(u7(2), identity.IdentityType.HUMAN,
                                         identity.IdentityState.ACTIVE)
        self.assertTrue(identity.validate_links((user,), (ident,), ()))
        link = identity.IdentityLink(user.user_id, ident.identity_id)
        self.assertTrue(identity.validate_links((user,), (ident,), (link,)))
        other = identity.User(u7(3))
        with self.assertRaises(identity.IdentityError):
            identity.validate_links((user, other), (ident,),
                                    (link, identity.IdentityLink(other.user_id, ident.identity_id)))

    def test_service_without_user_is_only_structural(self):
        service = identity.DigitalIdentity(u7(4), identity.IdentityType.SERVICE,
                                           identity.IdentityState.REVOKED)
        self.assertTrue(identity.validate_links((), (service,), ()))
        self.assertFalse(hasattr(service, "permissions"))
        self.assertFalse(hasattr(service, "authentication_assurance"))
        self.assertFalse(hasattr(service, "session"))
        # Un autre appel n'hérite d'aucune identité précédemment validée.
        with self.assertRaises(identity.IdentityError):
            identity.validate_links((identity.User(u7(5)),), (),
                                    (identity.IdentityLink(u7(5), service.identity_id),))

    def test_public_errors_have_stable_code_without_input(self):
        marker = "synthetic-invalid-identity"
        with self.assertRaises(identity.IdentityError) as caught:
            identity.User(marker)
        self.assertEqual(caught.exception.code, "IDENTITY_INVALID")
        self.assertNotIn(marker, str(caught.exception))
        self.assertNotIn(marker, repr(caught.exception))


if __name__ == "__main__":
    unittest.main()
