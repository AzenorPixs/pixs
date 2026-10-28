import datetime
import unittest
from dataclasses import FrozenInstanceError, replace

from pixs.core.authz.ports import Request
from pixs.core.command_metadata import CommandMetadata
from pixs.core.scope.context import ScopeContext, ScopeType
from pixs.dns.contracts import DeclareDesiredDns, DeclareName, GetAppliedDns, GetDesiredDns, ObservedAppliedDns, ResolveViewPolicy, RetireDesiredDns, RetireName, validate_declare_desired_dns, validate_declare_name, validate_get_applied_dns, validate_get_desired_dns, validate_observed_applied_dns, validate_resolve_view_policy, validate_retire_desired_dns, validate_retire_name
from pixs.dns.configuration import DesiredDnsConfig
from pixs.pzt.contracts import DeclareDesiredPzt, GetAppliedPzt, GetDesiredPzt, ObservedAppliedPzt, RetireDesiredPzt, validate_declare_desired_pzt, validate_get_applied_pzt, validate_get_desired_pzt, validate_observed_applied_pzt, validate_retire_desired_pzt


def _ctx(tenant=None, scope=None):
    return ScopeContext(scope_type=ScopeType.PLATFORM, tenant_id=None, scope_id=None)


def _meta(ctype="declare_desired_dns", subject="sujet-test", key="cle-test"):
    return CommandMetadata(command_id="cmd-test", correlation_ids=("corr-test",), causation_ids=(), scope_context=_ctx(), command_type=ctype, subject_id=subject, idempotency_key=key)


def _req(action="declare_desired_dns", resource="pixs.dns", subject="sujet-test"):
    return Request(decision_id="cmd-test", subject_id=subject, resource_id=resource, action_id=action, context=_ctx(), correlation_id="corr-test")


def _gov(owner):
    from pixs.kernel.data_governance_profile import DataGovernanceProfile
    from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
    return DataGovernanceProfile(profile_version="1.0.0", data_asset_id="actif-test", owner_component=owner, source_of_truth="source-test", data_classes=frozenset({"classe-test"}), confidentiality=ConfidentialityLevel.INTERNAL, personal_data=PersonalDataLevel.NONE, purpose_refs=frozenset({"but-test"}), retention_policy="retention-test", deletion_policy="suppression-test", residency_constraints=frozenset({"residence-test"}), authorized_consumers=frozenset({"conso-test"}), processor_refs=frozenset({"traitant-test"}), export_policy="export-test", lineage="ligne-test")


def _sec(owner="pixs.dns"):
    from pixs.kernel.config.resolution import SecretReference
    return SecretReference(owner_id=owner, entry_id="entree-test", source="source-test")


def _dnscfg(rev=2):
    from pixs.dns.configuration import DesiredDnsConfig
    return DesiredDnsConfig(schema_version="1.0.0", owner_id="pixs.dns", config_revision=rev, suffix="pzt.test.internal", ttl_positive=30, ttl_negative=5, views=("vue-test",), governance=_gov("pixs.dns"), secret_refs=(_sec("pixs.dns"),))


def _pztcfg(rev=2):
    from pixs.pzt.configuration import DesiredPztConfig
    return DesiredPztConfig(schema_version="1.0.0", owner_id="pixs.pzt", config_revision=rev, v6_enabled=False, plan_ref="plan-test", budget_ref="budget-test", governance=_gov("pixs.pzt"), secret_refs=(_sec("pixs.pzt"),))


class TestLiaisons(unittest.TestCase):
    def test_declare_lie_sujet_contexte_cible_action(self):
        cmd = DeclareDesiredDns(schema_version="1.0.0", metadata=_meta("declare_desired_dns"), request=_req("declare_desired_dns", "pixs.dns"), resource_id="pixs.dns", expected_revision=1, configuration=_dnscfg(2))
        self.assertEqual(validate_declare_desired_dns(cmd), [])

    def test_request_divergente_sujet_refuse(self):
        cmd = DeclareDesiredDns(schema_version="1.0.0", metadata=_meta("declare_desired_dns", subject="sujet-a"), request=_req("declare_desired_dns", "pixs.dns", subject="sujet-b"), resource_id="pixs.dns", expected_revision=1, configuration=_dnscfg(2))
        self.assertIn("DNS_SUBJECT_MISMATCH", validate_declare_desired_dns(cmd))

    def test_request_divergente_cible_refuse(self):
        cmd = DeclareDesiredDns(schema_version="1.0.0", metadata=_meta("declare_desired_dns"), request=_req("declare_desired_dns", "autre-cible"), resource_id="pixs.dns", expected_revision=1, configuration=_dnscfg(2))
        self.assertIn("DNS_RESOURCE_MISMATCH", validate_declare_desired_dns(cmd))

    def test_request_divergente_action_refuse(self):
        cmd = DeclareDesiredDns(schema_version="1.0.0", metadata=_meta("get_desired_dns"), request=_req("get_desired_dns", "pixs.dns"), resource_id="pixs.dns", expected_revision=1, configuration=_dnscfg(2))
        self.assertIn("DNS_ACTION_MISMATCH", validate_declare_desired_dns(cmd))

    def test_metadata_sous_classee_dans_enveloppe_refusee(self):
        class Fausse(CommandMetadata):
            pass
        faux = Fausse(command_id="cmd-test", correlation_ids=("corr-test",), causation_ids=(), scope_context=_ctx(), command_type="declare_desired_dns", subject_id="sujet-test", idempotency_key="cle-test")
        cmd = DeclareDesiredDns(schema_version="1.0.0", metadata=faux, request=_req("declare_desired_dns", "pixs.dns"), resource_id="pixs.dns", expected_revision=1, configuration=_dnscfg(2))
        self.assertIn("DNS_METADATA_TYPE", validate_declare_desired_dns(cmd))

    def test_objet_hostile_sans_acces(self):
        class Hostile:
            pass
        self.assertTrue(validate_declare_desired_dns(Hostile()))


class TestCatalogue(unittest.TestCase):
    def test_toutes_operations(self):
        self.assertEqual(validate_get_desired_dns(GetDesiredDns(schema_version="1.0.0", request=_req("get_desired_dns", "pixs.dns"), resource_id="pixs.dns")), [])
        self.assertEqual(validate_get_applied_dns(GetAppliedDns(schema_version="1.0.0", request=_req("get_applied_dns", "pixs.dns"), resource_id="pixs.dns")), [])
        self.assertEqual(validate_resolve_view_policy(ResolveViewPolicy(schema_version="1.0.0", request=_req("resolve_view_policy", "pixs.dns"), resource_id="pixs.dns", view="vue-test", name="nom-test")), [])
        self.assertEqual(validate_declare_name(DeclareName(schema_version="1.0.0", metadata=_meta("declare_name"), request=_req("declare_name", "pixs.dns"), resource_id="pixs.dns", expected_revision=1, name="nom-test", view="vue-test", target_ref="cible-test")), [])
        self.assertEqual(validate_retire_name(RetireName(schema_version="1.0.0", metadata=_meta("retire_name"), request=_req("retire_name", "pixs.dns"), resource_id="pixs.dns", expected_revision=1, name="nom-test", view="vue-test")), [])
        self.assertEqual(validate_retire_desired_dns(RetireDesiredDns(schema_version="1.0.0", metadata=_meta("retire_desired_dns"), request=_req("retire_desired_dns", "pixs.dns"), resource_id="pixs.dns", expected_revision=1, reason="motif-test")), [])
        from pixs.pzt.contracts import DeclareDesiredPzt as DP
        cmd = DP(schema_version="1.0.0", metadata=_meta("declare_desired_pzt"), request=_req("declare_desired_pzt", "pixs.pzt"), resource_id="pixs.pzt", expected_revision=1, configuration=_pztcfg(2))
        self.assertEqual(validate_declare_desired_pzt(cmd), [])
        self.assertEqual(validate_get_desired_pzt(GetDesiredPzt(schema_version="1.0.0", request=_req("get_desired_pzt", "pixs.pzt"), resource_id="pixs.pzt")), [])
        self.assertEqual(validate_get_applied_pzt(GetAppliedPzt(schema_version="1.0.0", request=_req("get_applied_pzt", "pixs.pzt"), resource_id="pixs.pzt")), [])

    def test_owner_arbitraire_refuse(self):
        cfg = replace(_dnscfg(2), owner_id="autre-module", governance=_gov("autre-module"))
        cmd = DeclareDesiredDns(schema_version="1.0.0", metadata=_meta("declare_desired_dns"), request=_req("declare_desired_dns", "pixs.dns"), resource_id="pixs.dns", expected_revision=1, configuration=cfg)
        self.assertIn("DNS_CONFIGURATION_INVALID", validate_declare_desired_dns(cmd))

    def test_expected_negatif_bool_refuses(self):
        cmd = DeclareDesiredDns(schema_version="1.0.0", metadata=_meta("declare_desired_dns"), request=_req("declare_desired_dns", "pixs.dns"), resource_id="pixs.dns", expected_revision=True, configuration=_dnscfg(2))
        self.assertIn("DNS_EXPECTED_INVALID", validate_declare_desired_dns(cmd))
        cmd2 = DeclareDesiredDns(schema_version="1.0.0", metadata=_meta("declare_desired_dns"), request=_req("declare_desired_dns", "pixs.dns"), resource_id="pixs.dns", expected_revision=-1, configuration=_dnscfg(2))
        self.assertIn("DNS_EXPECTED_INVALID", validate_declare_desired_dns(cmd2))

    def test_transition_incorrecte_refusee(self):
        cmd = DeclareDesiredDns(schema_version="1.0.0", metadata=_meta("declare_desired_dns"), request=_req("declare_desired_dns", "pixs.dns"), resource_id="pixs.dns", expected_revision=5, configuration=_dnscfg(2))
        self.assertIn("DNS_PROJECTION_MISMATCH", validate_declare_desired_dns(cmd))

    def test_schema_version_exacte(self):
        self.assertIn("DNS_SCHEMA_VERSION_INVALID", validate_get_applied_dns(GetAppliedDns(schema_version="1", request=_req("get_applied_dns", "pixs.dns"), resource_id="pixs.dns")))

    def test_etat_inconnu_legitime_valide(self):
        obs = ObservedAppliedDns(owner_id="pixs.dns", target_id="cible-test", tenant_id=None, config_revision=1, generation=0, observed_at=None, valid_until=None, expected_executor=None, proof_ref=None, applied_present=None)
        from pixs.dns.contracts import validate_observed_applied_dns
        self.assertEqual(validate_observed_applied_dns(obs), [])

    def test_etat_affirme_incomplet_refuse(self):
        from pixs.dns.contracts import ObservedAppliedDns as O, validate_observed_applied_dns as V
        obs = O(owner_id="pixs.dns", target_id="cible-test", tenant_id=None, config_revision=1, generation=0, observed_at=None, valid_until=None, expected_executor=None, proof_ref=None, applied_present=True)
        self.assertIn("DNS_EXECUTOR_INVALID", V(obs))

    def test_temps_invalide_et_ordre_inverse(self):
        import datetime
        from pixs.dns.contracts import ObservedAppliedDns as O, validate_observed_applied_dns as V
        t0 = datetime.datetime(2026, 1, 2, 3, 4, 5, tzinfo=datetime.timezone.utc)
        t1 = datetime.datetime(2026, 1, 2, 3, 4, 4, tzinfo=datetime.timezone.utc)
        obs = O(owner_id="pixs.dns", target_id="cible-test", tenant_id=None, config_revision=1, generation=0, observed_at=t0, valid_until=t1, expected_executor="exec-test", proof_ref="preuve-test", applied_present=True)
        self.assertIn("DNS_TIME_ORDER_INVALID", V(obs))
        obs2 = O(owner_id="pixs.dns", target_id="cible-test", tenant_id=None, config_revision=1, generation=0, observed_at="pas-un-temps", valid_until=123, expected_executor="exec-test", proof_ref="preuve-test", applied_present=False)
        self.assertIn("DNS_TIME_INVALID", V(obs2))

    def test_diagnostics_sans_echo(self):
        from pixs.dns.contracts import DeclareDesiredDns as D
        cmd = D(schema_version="mauvais", metadata=object(), request=object(), resource_id="mauvais", expected_revision="mauvais", configuration=object())
        for d in validate_declare_desired_dns(cmd):
            self.assertNotIn("mauvais", d)

    def test_immutabilite_precise(self):
        cmd = GetAppliedDns(schema_version="1.0.0", request=_req("get_applied_dns", "pixs.dns"), resource_id="pixs.dns")
        with self.assertRaises(FrozenInstanceError):
            cmd.resource_id = "autre"


class TestFrontieresSupplementaires(unittest.TestCase):
    def test_attendu_non_entier_refuse_sans_exception(self):
        for value in ("valeur-privee-test", object(), True, -1):
            cmd = DeclareDesiredDns(schema_version="1.0.0", metadata=_meta(), request=_req(), resource_id="pixs.dns", expected_revision=value, configuration=_dnscfg(2))
            self.assertIn("DNS_EXPECTED_INVALID", validate_declare_desired_dns(cmd))

    def test_cible_opaque_distincte_du_module(self):
        resource = "configuration-test"
        cmd = DeclareDesiredDns(schema_version="1.0.0", metadata=_meta(), request=_req(resource=resource), resource_id=resource, expected_revision=1, configuration=_dnscfg(2))
        self.assertEqual(validate_declare_desired_dns(cmd), [])

    def test_contexte_tenant_divergent_refuse(self):
        request = replace(_req(), context=ScopeContext(ScopeType.TENANT, "tenant-test"))
        cmd = DeclareDesiredDns(schema_version="1.0.0", metadata=_meta(), request=request, resource_id="pixs.dns", expected_revision=1, configuration=_dnscfg(2))
        self.assertIn("DNS_CONTEXT_MISMATCH", validate_declare_desired_dns(cmd))

    def test_query_champ_request_hostile_refuse_sans_comparaison(self):
        class Hostile:
            def __eq__(self, other):
                raise AssertionError("comparaison interdite")
        request = _req(action="get_applied_dns")
        object.__setattr__(request, "subject_id", Hostile())
        query = GetAppliedDns(schema_version="1.0.0", request=request, resource_id="pixs.dns")
        self.assertIn("DNS_REQUEST_FIELDS_INVALID", validate_get_applied_dns(query))


if __name__ == "__main__":
    unittest.main()
