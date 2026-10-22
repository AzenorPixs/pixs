"""Erreurs API publiques : localisation et minimisation, sans données techniques."""
import json
import unittest

from pixs.backend.api_core_errors_catalog import CoreApiError, classify_error, error_schema


class CoreApiErrorsTest(unittest.TestCase):
    def test_stable_versioned_envelope_and_localized_messages(self):
        error = CoreApiError("IDEMPOTENCE_CONFLICT")
        english = error.envelope(correlation_id="corr")
        french = error.envelope(correlation_id="corr", language="fr")
        self.assertEqual(error.status, 409)
        self.assertEqual(english["error_code"], "pixs.core.api.v1.IDEMPOTENCE_CONFLICT")
        self.assertEqual(french["message"], "Conflit de contenu d'idempotence.")
        self.assertNotEqual(english["message"], french["message"])
        self.assertEqual(english["details"], {})

    def test_exception_message_is_never_projected(self):
        error = classify_error(RuntimeError("VALEUR_PRIVEE_DE_TEST"))
        body = error.envelope(correlation_id="corr", language="fr")
        self.assertEqual(error.status, 500)
        self.assertNotIn("VALEUR_PRIVEE_DE_TEST", json.dumps(body))
        self.assertEqual(body["details"], {})

    def test_public_code_is_closed_and_correlations_strict(self):
        with self.assertRaises(ValueError):
            CoreApiError("CLIENT_CODE")
        for value in ("", "a" * 129, "a" + chr(10), chr(0), object()):
            with self.assertRaises(ValueError):
                CoreApiError("INPUT_INVALID").envelope(correlation_id=value)

    def test_known_owner_errors_keep_public_meaning(self):
        from pixs.core.services_common import CoreServiceError
        from pixs.auth.contracts import AuthServiceError
        from pixs.auth.runtime_verifier import AuthVerificationError
        for cause, status, code in (
            (CoreServiceError("IDEMPOTENCE_CONFLIT"), 409, "IDEMPOTENCE_CONFLICT"),
            (CoreServiceError("CONFLIT_CAS"), 409, "VERSION_CONFLICT"),
            (CoreServiceError("DECISION_REFUSEE"), 403, "ACCESS_DENIED"),
            (CoreServiceError("ISSUE_INCONNUE"), 503, "UNKNOWN_OUTCOME"),
            (CoreServiceError("AUDIT_REFUS_INDISPONIBLE"), 503, "AUDIT_UNAVAILABLE"),
            (AuthServiceError("AUTH_SESSION_LIMIT"), 409, "SESSION_LIMIT"),
            (AuthVerificationError(), 401, "AUTH_REQUIRED"),
        ):
            with self.subTest(code=code):
                result = classify_error(cause)
                self.assertEqual((result.status, result.public_code), (status, code))

    def test_encapsulated_auth_refusal_remains_401_without_text_inference(self):
        from pixs.core.services_common import CoreServiceError
        from pixs.core.authz.ports import PortError
        from pixs.core.ports import CorePortError
        from pixs.auth.runtime_verifier import AuthVerificationError
        port = PortError()
        port.__cause__ = AuthVerificationError()
        failure = CoreServiceError("FAITS_ILLISIBLES")
        failure.__cause__ = port
        self.assertEqual(classify_error(failure).public_code, "AUTH_REQUIRED")
        opaque = CoreServiceError("FAITS_ILLISIBLES")
        opaque.__cause__ = RuntimeError("AUTH_VERIFICATION_FAILED")
        self.assertEqual(classify_error(opaque).status, 503)
        direct = CorePortError()
        direct.__cause__ = AuthVerificationError()
        self.assertEqual(classify_error(direct).status, 401)
        cycle = CorePortError()
        cycle.__cause__ = cycle
        self.assertEqual(classify_error(cycle).status, 503)

    def test_unknown_owner_code_does_not_echo_it(self):
        from pixs.core.services_common import CoreServiceError
        error = classify_error(CoreServiceError("VALEUR_PRIVEE_DE_TEST"))
        self.assertEqual(error.public_code, "SERVICE_UNAVAILABLE")
        self.assertNotIn("VALEUR_PRIVEE_DE_TEST", json.dumps(error.envelope(correlation_id="corr")))

    def test_schema_and_locale_fallback_match_real_responses(self):
        schema = error_schema()
        body = CoreApiError("ACCESS_DENIED").envelope(correlation_id="corr", language="unknown")
        self.assertEqual(set(body), set(schema["required"]))
        self.assertIn(body["error_code"], schema["properties"]["error_code"]["enum"])
        self.assertEqual(body["message"], "Access denied.")
        self.assertFalse(schema["additionalProperties"])


if __name__ == "__main__":
    unittest.main()
