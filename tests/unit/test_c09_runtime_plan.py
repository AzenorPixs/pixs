"""Plans C09 : budgets effectifs, cumuls, types fermés et absence d'application implicite."""
from __future__ import annotations
import dataclasses
import datetime as dt
import unittest
from unittest.mock import patch

from pixs.backend.c09_authorization_adapter import C09Refused
from pixs.backend.c09_contracts import C09PolicyV1
from pixs.backend.c09_runtime_plan import (
    C09RuntimePlanV1, C09QueueBudgetV1, C09RolePlanV1,
    C09BudgetObservationV1, C09AppliedObservationV1,
    c09_runtime_plan_sha256, c09_role_plan, validate_c09_runtime_plan, validate_c09_applied_observation,
)

_NOW = dt.datetime(2026, 5, 1, tzinfo=dt.timezone.utc)


def policy(role, **changes):
    values = dict(
        policy_reference="policy:"+role, policy_version="1.0.0", lease_seconds=30,
        renewal_seconds=5, max_attempts=3, retry_delays_seconds=(1,2), polling_interval_ms=50,
        polling_max_batch=1, max_concurrency=2 if role=="WEB" else 1,
        max_units_per_poll=1, drain_seconds=5, attempt_timeout_seconds=10, job_timeout_seconds=120,
        process_count=1, cpu_millicores=100, max_connections=5, memory_mb=128,
        effective_from=dt.datetime(2026,1,1,tzinfo=dt.timezone.utc))
    values.update(changes)
    return C09PolicyV1(**values)


def plan():
    return C09RuntimePlanV1("plan-pbo","1.0.0","owner-pbo","environment-pbo",
        tuple(C09RolePlanV1(role, policy(role)) for role in ("SCHEDULER","WEB","WORKER")),
        C09QueueBudgetV1(100,20,100,200,8192,8,65536))


def budget(**changes):
    values = dict(
        source_reference="synthetic-supervisor-budget", source_version="1.0.0",
        environment_reference="environment-pbo", revision=1,
        observed_at=_NOW-dt.timedelta(seconds=1), valid_until=_NOW+dt.timedelta(seconds=60),
        detected_cpu_millicores=16000, detected_memory_mb=32768,
        granted_cpu_millicores=1000, granted_memory_mb=1024, granted_pg_connections=32,
        granted_processes=6, granted_concurrency=8, reserved_cpu_millicores=100,
        reserved_memory_mb=128, reserved_pg_connections=2)
    values.update(changes)
    return C09BudgetObservationV1(**values)


def applied(selected_plan=None, **changes):
    selected_plan = plan() if selected_plan is None else selected_plan
    values = dict(
        source_reference="synthetic-supervisor-applied", source_version="1.0.0",
        environment_reference="environment-pbo", plan_sha256=c09_runtime_plan_sha256(selected_plan),
        role="WORKER", process_index=0, process_reference="process-test", revision=1,
        observed_at=_NOW-dt.timedelta(seconds=1), valid_until=_NOW+dt.timedelta(seconds=60),
        state="APPLIED", cpu_millicores=100, memory_mb=128, pg_connections=5,
        concurrency=1, buffer_bytes=65536,
        process_counts=(("SCHEDULER",1),("WEB",1),("WORKER",1)))
    values.update(changes)
    return C09AppliedObservationV1(**values)


class Hostile:
    def __eq__(self, other):
        raise AssertionError("EGALITE_HOSTILE")
    def __hash__(self):
        raise AssertionError("HASH_HOSTILE")
    def __str__(self):
        raise AssertionError("STR_HOSTILE")


class RuntimePlanTests(unittest.TestCase):
    def validate(self, value=None, observed=None):
        return validate_c09_runtime_plan(plan() if value is None else value,
                                         budget() if observed is None else observed, now=_NOW)
    def observed(self, observation):
        return validate_c09_applied_observation(plan(),budget(),observation,
                    role="WORKER",process_index=0,process_reference="process-test",now=_NOW)
    def role_changed(self, role, **changes):
        value=plan()
        return dataclasses.replace(value,roles=tuple(
            dataclasses.replace(item,policy=dataclasses.replace(item.policy,**changes)) if item.role==role else item
            for item in value.roles))

    def test_cumuls_exacts(self):
        self.assertEqual(self.validate(),dict(cpu_millicores=300,memory_mb=384,
                                              pg_connections=15,processes=3,concurrency=4))
    def test_quotas_effectifs_priment_ressources_physiques(self):
        with self.assertRaises(C09Refused):
            self.validate(observed=budget(granted_cpu_millicores=200))
    def test_marges_cpu_memoire_connexions(self):
        for changes in (dict(reserved_cpu_millicores=701),dict(reserved_memory_mb=641),
                        dict(reserved_pg_connections=18)):
            with self.subTest(changes=changes),self.assertRaises(C09Refused):
                self.validate(observed=budget(**changes))
    def test_processus_et_concurrence_cumules(self):
        for changes in (dict(granted_processes=2),dict(granted_concurrency=3)):
            with self.assertRaises(C09Refused):
                self.validate(observed=budget(**changes))
    def test_process_count_multiplie_tous_les_budgets(self):
        value=self.role_changed("WORKER",process_count=2)
        totals=self.validate(value)
        self.assertEqual(totals["pg_connections"],20)
        self.assertEqual(totals["memory_mb"],512)
        self.assertEqual(totals["cpu_millicores"],400)
        self.assertEqual(totals["processes"],4)
    def test_nombre_coeurs_ne_change_pas_plan(self):
        value=plan()
        self.assertEqual(self.validate(value,budget(detected_cpu_millicores=64000)),
                         self.validate(value,budget(detected_cpu_millicores=500)))
        self.assertEqual(value.roles,plan().roles)
    def test_detection_absente_peut_rester_na_si_budget_verifie(self):
        self.assertEqual(self.validate(observed=budget(detected_cpu_millicores=None,detected_memory_mb=None)),
                         self.validate())
    def test_budget_absent_ou_etranger(self):
        for value in (None,{},Hostile()):
            with self.assertRaises(C09Refused):
                validate_c09_runtime_plan(plan(),value,now=_NOW)
    def test_budget_autre_environnement_refuse(self):
        with self.assertRaises(C09Refused):
            self.validate(observed=budget(environment_reference="environment-pa-distant"))
    def test_budget_fraicheur_et_horloge(self):
        for changes in (dict(valid_until=_NOW),dict(observed_at=_NOW+dt.timedelta(seconds=1)),
                        dict(observed_at=_NOW.replace(tzinfo=None))):
            with self.assertRaises(C09Refused):
                self.validate(observed=budget(**changes))
    def test_roles_tries_uniques_fermes(self):
        value=plan()
        for roles in ((value.roles[0],value.roles[0]),tuple(reversed(value.roles)),
                      (C09RolePlanV1("PA",policy("WORKER")),),(),
                      (C09RolePlanV1(Hostile(),policy("WORKER")),)):
            with self.assertRaises(C09Refused):
                self.validate(dataclasses.replace(value,roles=roles))
    def test_worker_et_scheduler_serialises_v1(self):
        for role in ("WORKER","SCHEDULER"):
            with self.assertRaises(C09Refused):
                self.validate(self.role_changed(role,max_concurrency=2))
    def test_connexions_control_et_paires_par_unite(self):
        with self.assertRaises(C09Refused):
            self.validate(self.role_changed("WORKER",max_connections=2))
    def test_files_et_buffers_sans_defaut(self):
        with self.assertRaises(TypeError):
            C09QueueBudgetV1()
        with self.assertRaises(TypeError):
            C09RuntimePlanV1("p","1.0.0","o","e",plan().roles)
    def test_bool_bornes_et_hostiles_files(self):
        for field in dataclasses.fields(C09QueueBudgetV1):
            for value in (True,0,-1,Hostile()):
                with self.subTest(field=field.name),self.assertRaises(C09Refused):
                    self.validate(dataclasses.replace(plan(),queues=dataclasses.replace(plan().queues,**{field.name:value})))
    def test_buffer_minimal_et_limite_memoire(self):
        for size in (1,128*1024*1024):
            with self.assertRaises(C09Refused):
                self.validate(dataclasses.replace(plan(),queues=dataclasses.replace(plan().queues,buffer_bytes=size)))
    def test_references_utf8_et_versions(self):
        for value in ("", "nul\x00ref", "\ud800", Hostile()):
            with self.assertRaises(C09Refused):
                self.validate(dataclasses.replace(plan(),plan_reference=value))
        with self.assertRaises(C09Refused):
            self.validate(dataclasses.replace(plan(),plan_version="1"))
        with self.assertRaises(C09Refused):
            self.validate(self.role_changed("WEB",policy_reference="\ud800"))
    def test_hash_deterministe_et_tous_proprietaires(self):
        initial=c09_runtime_plan_sha256(plan())
        self.assertEqual(initial,c09_runtime_plan_sha256(plan()))
        for changes in (dict(plan_reference="p2"),dict(plan_version="1.0.1"),
                        dict(owner_reference="o2"),dict(environment_reference="e2")):
            self.assertNotEqual(initial,c09_runtime_plan_sha256(dataclasses.replace(plan(),**changes)))
        self.assertNotEqual(initial,c09_runtime_plan_sha256(self.role_changed("WEB",cpu_millicores=101)))
        self.assertNotEqual(initial,c09_runtime_plan_sha256(dataclasses.replace(
            plan(),queues=dataclasses.replace(plan().queues,max_pending_jobs=101))))
    def test_immuable(self):
        with self.assertRaises(dataclasses.FrozenInstanceError):
            plan().plan_reference="other"
    def test_plan_valide_ne_vaut_pas_applique(self):
        self.validate()
        with self.assertRaises(C09Refused):
            self.observed(None)
    def test_application_exacte(self):
        self.assertEqual(self.observed(applied()),c09_role_plan(plan(),"WORKER"))
    def test_partiel_unknown_et_mauvais_hash_fermes(self):
        for changes in (dict(state="PARTIAL"),dict(state="UNKNOWN"),dict(plan_sha256="0"*64),
                        dict(plan_sha256=Hostile()),dict(state=Hostile())):
            with self.assertRaises(C09Refused):
                self.observed(applied(**changes))
    def test_application_toutes_limites_concordantes(self):
        for field in ("cpu_millicores","memory_mb","pg_connections","concurrency","buffer_bytes"):
            with self.assertRaises(C09Refused):
                self.observed(applied(**{field:getattr(applied(),field)+1}))
    def test_application_processus_et_identite_fermes(self):
        for changes in (dict(role="WEB"),dict(process_index=True),dict(process_index=1),
                        dict(process_reference="foreign"),dict(revision=True),
                        dict(environment_reference="environment-pa")):
            with self.assertRaises(C09Refused):
                self.observed(applied(**changes))
    def test_application_fraiche(self):
        with self.assertRaises(C09Refused):
            self.observed(applied(valid_until=_NOW))
    def test_comptes_processus_distincts_et_bornes(self):
        for counts in ((("WORKER",1),), (("SCHEDULER",1),("WEB",1),("WORKER",2)),
                       (("SCHEDULER",1),("WEB",1),("WORKER",0)),
                       (("SCHEDULER",1),("WEB",1),("WORKER",1),("WORKER",1)),
                       (("PA",1),("WEB",1),("WORKER",1))):
            with self.assertRaises(C09Refused):
                self.observed(applied(process_counts=counts))
    def test_pure_sans_io(self):
        with patch("builtins.open",side_effect=AssertionError("IO_INTERDITE")):
            self.validate()
            self.observed(applied())
    def test_diags_pas_echo_valeur(self):
        marker="marqueur-ne-pas-echo"
        with self.assertRaises(C09Refused) as caught:
            self.validate(dataclasses.replace(plan(),plan_version=marker))
        self.assertNotIn(marker,str(caught.exception))


if __name__=="__main__":
    unittest.main()
