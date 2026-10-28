import unittest
from dataclasses import FrozenInstanceError

from pixs.kernel.config.resolution import SecretReference
from pixs.kernel.data_governance_profile import DataGovernanceProfile
from pixs.kernel.data_governance import ConfidentialityLevel, PersonalDataLevel
from pixs.dns.configuration import DesiredDnsConfig, check_cas as dns_cas, validate_desired_dns_config
from pixs.pzt.configuration import DesiredPztConfig, check_cas as pzt_cas, validate_desired_pzt_config


def _gov(owner):
    return DataGovernanceProfile(profile_version="1.0.0", data_asset_id="actif-test", owner_component=owner, source_of_truth="source-test", data_classes=frozenset({"classe-test"}), confidentiality=ConfidentialityLevel.INTERNAL, personal_data=PersonalDataLevel.NONE, purpose_refs=frozenset({"but-test"}), retention_policy="retention-test", deletion_policy="suppression-test", residency_constraints=frozenset({"residence-test"}), authorized_consumers=frozenset({"conso-test"}), processor_refs=frozenset({"traitant-test"}), export_policy="export-test", lineage="ligne-test")


def _sec(owner="pixs.dns"):
    return SecretReference(owner_id=owner, entry_id="entree-test", source="source-test")


class TestConfiguration(unittest.TestCase):
    def test_dns_bornes_inclusives(self):
        cfg = DesiredDnsConfig(schema_version="1.0.0", owner_id="pixs.dns", config_revision=2, suffix="pzt.test.internal", ttl_positive=0, ttl_negative=0, views=("vue-test",), governance=_gov("pixs.dns"), secret_refs=(_sec(),))
        self.assertEqual(validate_desired_dns_config(cfg), [])
        cfg2 = DesiredDnsConfig(schema_version="1.0.0", owner_id="pixs.dns", config_revision=2, suffix="pzt.test.internal", ttl_positive=30, ttl_negative=5, views=("vue-test",), governance=_gov("pixs.dns"), secret_refs=(_sec(),))
        self.assertEqual(validate_desired_dns_config(cfg2), [])

    def test_dns_bornes_exclues(self):
        cfg = DesiredDnsConfig(schema_version="1.0.0", owner_id="pixs.dns", config_revision=2, suffix="pzt.test.internal", ttl_positive=31, ttl_negative=0, views=("vue-test",), governance=_gov("pixs.dns"), secret_refs=(_sec(),))
        self.assertIn("DNS_TTL_POSITIVE_INVALID", validate_desired_dns_config(cfg))

    def test_cas_egal_admis_nouveau_plus_un(self):
        self.assertEqual(dns_cas(3, 3), [])
        self.assertEqual(pzt_cas(3, 3), [])

    def test_cas_negatif_bool_refuses(self):
        self.assertEqual(dns_cas(-1, -1), ["DNS_CAS_NEGATIVE"])
        self.assertEqual(dns_cas(True, 3), ["DNS_CAS_TYPE"])
        self.assertEqual(pzt_cas(False, 3), ["PZT_CAS_TYPE"])

    def test_cas_stale_refuse(self):
        self.assertEqual(dns_cas(4, 3), ["DNS_CAS_MISMATCH"])

    def test_gouvernance_profil_invalide(self):
        cfg = DesiredDnsConfig(schema_version="1.0.0", owner_id="pixs.dns", config_revision=2, suffix="pzt.test.internal", ttl_positive=0, ttl_negative=0, views=("vue-test",), governance="gouvernance-brute", secret_refs=(_sec(),))
        self.assertIn("DNS_GOVERNANCE_TYPE", validate_desired_dns_config(cfg))

    def test_gouvernance_owner_lie_module(self):
        cfg = DesiredDnsConfig(schema_version="1.0.0", owner_id="pixs.dns", config_revision=2, suffix="pzt.test.internal", ttl_positive=0, ttl_negative=0, views=("vue-test",), governance=_gov("autre-module"), secret_refs=(_sec(),))
        self.assertIn("DNS_GOVERNANCE_OWNER_INVALID", validate_desired_dns_config(cfg))

    def test_secret_brut_refuse_chaque_reference(self):
        cfg = DesiredDnsConfig(schema_version="1.0.0", owner_id="pixs.dns", config_revision=2, suffix="pzt.test.internal", ttl_positive=0, ttl_negative=0, views=("vue-test",), governance=_gov("pixs.dns"), secret_refs=("chaine-brute",))
        self.assertIn("DNS_SECRET_REF_TYPE", validate_desired_dns_config(cfg))
        cfg2 = DesiredDnsConfig(schema_version="1.0.0", owner_id="pixs.dns", config_revision=2, suffix="pzt.test.internal", ttl_positive=0, ttl_negative=0, views=("vue-test",), governance=_gov("pixs.dns"), secret_refs=(True,))
        self.assertIn("DNS_SECRET_REF_TYPE", validate_desired_dns_config(cfg2))

    def test_suffix_manquant_refuse_sans_invention(self):
        cfg = DesiredDnsConfig(schema_version="1.0.0", owner_id="pixs.dns", config_revision=2, suffix="", ttl_positive=0, ttl_negative=0, views=("vue-test",), governance=_gov("pixs.dns"), secret_refs=(_sec(),))
        self.assertIn("DNS_SUFFIX_INVALID", validate_desired_dns_config(cfg))

    def test_pzt_sans_io(self):
        cfg = DesiredPztConfig(schema_version="1.0.0", owner_id="pixs.pzt", config_revision=2, v6_enabled=False, plan_ref="plan-test", budget_ref="budget-test", governance=_gov("pixs.pzt"), secret_refs=(_sec("pixs.pzt"),))
        self.assertEqual(validate_desired_pzt_config(cfg), [])

    def test_diagnostics_sans_echo(self):
        cfg = DesiredDnsConfig(schema_version="mauvais", owner_id="", config_revision="mauvais", suffix="", ttl_positive=True, ttl_negative="mauvais", views="mauvais", governance="mauvais", secret_refs="mauvais")
        for d in validate_desired_dns_config(cfg):
            self.assertNotIn("mauvais", d)

    def test_immutabilite(self):
        cfg = DesiredDnsConfig(schema_version="1.0.0", owner_id="pixs.dns", config_revision=2, suffix="pzt.test.internal", ttl_positive=0, ttl_negative=0, views=("vue-test",), governance=_gov("pixs.dns"), secret_refs=(_sec(),))
        with self.assertRaises(FrozenInstanceError):
            cfg.suffix = "autre"


if __name__ == "__main__":
    unittest.main()
