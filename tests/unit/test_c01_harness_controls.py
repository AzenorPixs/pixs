"""Contrôles du harnais : aucune unité réelle, aucun privilège ni fichier créé."""
from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import json
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('c01_harness_controls', ROOT / 'tests/integration/test_c01_systemd_harness.py')
H = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(H)
CASE = H.BASE / '01a15239-b6b6-7d07-ae75-ef14519c1e13'


def metadata(unit, *, active='failed', pid=0):
    return {'Description': 'Pixs C01 test ' + CASE.name + ' ' + unit,
        'Transient': True, 'FragmentPath': '/run/systemd/transient/' + unit,
        'ActiveState': active, 'SubState': 'failed' if active == 'failed' else 'running',
        'User': str(H.UID if unit == H.CONSUMER else 0), 'MainPID': pid,
        'Result': 'exit-code', 'ExecMainStatus': 1}


class HarnessControls(unittest.TestCase):
    def setUp(self):
        self.states = {H.CONSUMER: metadata(H.CONSUMER)}
        self.commands = []
        self.records = []
        self.enterContext(mock.patch.object(H.os, 'getuid', return_value=0))
        self.enterContext(mock.patch.object(H.os, 'geteuid', return_value=0))
        self.enterContext(mock.patch.object(H, 'load_plan', return_value=(CASE, 1002)))
        self.enterContext(mock.patch.object(H, 'loaded_units', side_effect=lambda: set(self.states)))
        self.enterContext(mock.patch.object(H, 'unit_metadata', side_effect=lambda unit: copy.deepcopy(self.states[unit])))
        self.enterContext(mock.patch.object(H, 'record_public', side_effect=lambda case, prefix, value: self.records.append((prefix, copy.deepcopy(value)))))
        self.run_mock = self.enterContext(mock.patch.object(H, 'run', side_effect=self.fake_run))

    def fake_run(self, command, timeout=10, *, data=None):
        self.commands.append(command)
        unit = command[-1]
        if command == ['/usr/bin/systemctl', '--system', '--no-ask-password', 'stop', '--', unit]:
            if self.states[unit]['ActiveState'] != 'failed':
                del self.states[unit]
        elif command == ['/usr/bin/systemctl', '--system', '--no-ask-password', 'reset-failed', '--', unit]:
            del self.states[unit]
        else:
            self.fail('Commande hors des deux opérations fermées')
        return b''

    def test_recovery_preserves_before_and_after_and_resets_only_the_owned_failed_unit(self):
        H.recover_case(CASE)
        self.assertEqual(self.commands, [
            ['/usr/bin/systemctl', '--system', '--no-ask-password', 'stop', '--', H.CONSUMER],
            ['/usr/bin/systemctl', '--system', '--no-ask-password', 'reset-failed', '--', H.CONSUMER]])
        self.assertEqual([p for p, _ in self.records], ['recovery-before', 'recovery-after'])
        self.assertEqual(self.records[0][1]['units'][H.CONSUMER]['ExecMainStatus'], 1)
        self.assertEqual(self.records[1][1]['units_absent'], [H.CONSUMER])
        self.assertEqual(self.states, {})

    def test_foreign_or_active_units_refuse_before_any_effect(self):
        cases = [('Description', 'autre unité'), ('Transient', False),
                 ('FragmentPath', '/etc/systemd/system/autre.service'), ('User', '9999'),
                 ('MainPID', True), ('MainPID', 123), ('ActiveState', 'active')]
        for key, value in cases:
            with self.subTest(key=key, value=value):
                self.states = {H.CONSUMER: {**metadata(H.CONSUMER), key: value}}
                with self.assertRaises(ValueError):
                    H.recover_case(CASE)
                self.assertEqual(self.commands, [])
                self.assertEqual(self.records, [])

    def test_both_units_verified_before_first_effect(self):
        self.states[H.OPERATOR] = {**metadata(H.OPERATOR), 'Description': 'étrangère'}
        with self.assertRaises(ValueError):
            H.recover_case(CASE)
        self.assertEqual(self.commands, [])
        self.assertEqual(self.records, [])

    def test_reset_failure_is_propagated_and_no_success_record_exists(self):
        def failing(command, timeout=10, *, data=None):
            if 'reset-failed' in command:
                raise ValueError('refus synthétique')
            return self.fake_run(command, timeout, data=data)
        self.run_mock.side_effect = failing
        with self.assertRaises(ValueError):
            H.recover_case(CASE)
        self.assertEqual([p for p, _ in self.records], ['recovery-before'])
        self.assertIn(H.CONSUMER, self.states)

    def test_recovery_rechecks_stopped_state_at_stop_boundary(self):
        original = H.present_owned
        calls = 0
        def changing(case, unit, *, stopped):
            nonlocal calls
            calls += 1
            if calls == 4:
                self.states[H.CONSUMER] = metadata(H.CONSUMER, active='active', pid=123)
            return original(case, unit, stopped=stopped)
        with mock.patch.object(H, 'present_owned', side_effect=changing):
            with self.assertRaises(ValueError):
                H.recover_case(CASE)
        self.assertEqual(self.commands, [])
        self.assertEqual([p for p, _ in self.records], ['recovery-before'])

    def test_cleanup_can_stop_its_active_unit_and_proves_unload(self):
        self.states[H.CONSUMER] = metadata(H.CONSUMER, active='active', pid=123)
        H.cleanup(CASE, [H.CONSUMER])
        self.assertEqual(self.commands, [
            ['/usr/bin/systemctl', '--system', '--no-ask-password', 'stop', '--', H.CONSUMER]])
        self.assertEqual([p for p, _ in self.records], ['cleanup-before', 'cleanup-after'])

    def test_wait_for_unload_is_bounded(self):
        with mock.patch.object(H.time, 'monotonic', side_effect=[0, 0, 1, 4]):
            with mock.patch.object(H.time, 'sleep') as sleep:
                with self.assertRaises(ValueError):
                    H.wait_absent([H.CONSUMER], 3)
        self.assertEqual(sleep.call_count, 2)
        self.assertEqual(self.commands, [])

    def test_nonroot_rejected_before_native_or_file_actions(self):
        with mock.patch.object(H.os, 'getuid', return_value=1002):
            with self.assertRaises(ValueError):
                H.execute(recovery=CASE)
            with self.assertRaises(ValueError):
                H.recover_case(CASE)
        self.assertEqual(self.commands, [])
        self.assertEqual(self.records, [])

    def test_plan_has_no_effect_and_recovery_option_requires_execute(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(H.plan(), 0)
        self.assertFalse(json.loads(output.getvalue())['crypto_qualification'])
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                H.main(['--plan', '--recover-case', str(CASE)])
        self.assertEqual(error.exception.code, 2)
        self.assertEqual(self.commands, [])
        self.assertEqual(self.records, [])

    def test_worker_records_stage_and_type_without_exception_message_then_reraises(self):
        from pixs.backend.systemd_secret_provider import native
        with mock.patch.object(native, 'prove_self', side_effect=ValueError('synthetic-detail-not-for-diagnostics')):
            with mock.patch.object(H, 'write_json') as write:
                with self.assertRaises(ValueError):
                    H.worker(CASE / 'plan.json')
        self.assertEqual(write.call_args.args[1], {'stage': 'identite', 'error_type': 'ValueError'})
        self.assertEqual(write.call_args.args[0], CASE / 'worker/failure.json')


if __name__ == '__main__':
    unittest.main()
