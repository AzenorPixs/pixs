"""Qualification fonctionnelle C01, réservée au RUN CISMP3 nommé ci-dessous.

--plan est sans effet de bord. --execute requiert une autorisation hôte distincte
et UID 0. Deux unités transitoires seulement ; fixtures publiques ; aucune clé
hôte. Le chiffrement null ne démontre ni confidentialité ni authenticité.
Les imports sont purs. Aucun appel à Django setup, PostgreSQL ou session Pixs.
"""
from __future__ import annotations

import argparse
import json
import os
import pwd
import re
import signal
import stat
import subprocess
import time
from dataclasses import asdict, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path('/home/devops/datas/pixs')
BASE = ROOT / 'output/cismp/cismp3-pixs-ab58d92936e94d41/systemd-test/harness'
SELF = ROOT / 'tests/integration/test_c01_systemd_harness.py'
PYTHON = ROOT / '.venv/bin/python3'
CONSUMER = 'pixs-c01-c3-ab58d92936e94d41-consumer.service'
OPERATOR = 'pixs-c01-c3-ab58d92936e94d41-operator.service'
UID = 1002
POLICY_ID = 'c01-systemd-functional-test'
PURPOSE = 'bootstrap-c01-test'
COMMAND = ['/usr/bin/sudo', '-n', '/usr/bin/env', '-i', 'PATH=/usr/bin:/bin',
           'LANG=C.UTF-8', 'PYTHONPATH=' + str(ROOT / 'src'), str(PYTHON), '-B',
           str(SELF), '--execute']
ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8', 'PYTHONPATH': str(ROOT / 'src')}
UNITS = (CONSUMER, OPERATOR)
FIXTURES = {'v1': {'key': 'synth-v1-key-public', 'pwd': 'synth-v1-pwd-public'},
            'v2': {'key': 'synth-v2-key-public', 'pwd': 'synth-v2-pwd-public'}}
CASE_RE = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}')
INV_RE = re.compile(r'[0-9a-f]{32}')


def refuse():
    return ValueError('qualification C01 refusée ; consulter étape publique')


def checked_path(path):
    """Parcours sans symlink ; n'ouvre jamais de contenu ancêtre."""
    path = Path(path)
    if not path.is_absolute() or any(p in ('.', '..') for p in str(path).split('/')):
        raise refuse()
    current = Path('/')
    for part in path.parts[1:]:
        current /= part
        metadata = current.lstat()
        if stat.S_ISLNK(metadata.st_mode):
            raise refuse()
    return path


def run(argv, timeout=10, *, data=None):
    if (not isinstance(argv, list) or not argv or not argv[0].startswith('/')
            or any(type(arg) is not str or '\x00' in arg for arg in argv)):
        raise refuse()
    try:
        result = subprocess.run(argv, input=data, capture_output=True,
                                timeout=timeout, env=ENV, check=False)
    except (OSError, subprocess.SubprocessError):
        raise refuse() from None
    if result.returncode != 0 or len(result.stdout) > 4 * 1024 * 1024:
        raise refuse()
    return result.stdout


def bus(member, signature=None, *arguments):
    command = ['/usr/bin/busctl', '--system', '--json=short', '--no-pager',
               '--allow-interactive-authorization=no', '--auto-start=no', 'call',
               'org.freedesktop.systemd1', '/org/freedesktop/systemd1',
               'org.freedesktop.systemd1.Manager', member]
    if signature is not None:
        command += [signature, *arguments]
    return json.loads(run(command))


def loaded_units():
    reply = bus('ListUnits')
    if reply.get('type') != 'a(ssssssouso)' or type(reply.get('data')) is not list:
        raise refuse()
    rows = reply['data']
    # Les réponses de méthode ont un tableau d'arguments externes.
    if len(rows) != 1 or type(rows[0]) is not list:
        raise refuse()
    names = set()
    for row in rows[0]:
        if type(row) is not list or len(row) != 10 or type(row[0]) is not str:
            raise refuse()
        names.add(row[0])
    return names


def description(unit):
    reply = bus('GetUnit', 's', unit)
    if reply.get('type') != 'o' or type(reply.get('data')) is not list or len(reply['data']) != 1:
        raise refuse()
    path = reply['data'][0]
    if type(path) is not str or not path.startswith('/org/freedesktop/systemd1/unit/'):
        raise refuse()
    value = json.loads(run(['/usr/bin/busctl', '--system', '--json=short',
                           'get-property', 'org.freedesktop.systemd1', path,
                           'org.freedesktop.systemd1.Unit', 'Description']))
    if value.get('type') != 's' or type(value.get('data')) is not str:
        raise refuse()
    return value['data']


def assert_absent():
    if set(UNITS) & loaded_units():
        raise refuse()
    reply = bus('ListUnitFiles')
    if (reply.get('type') != 'a(ss)' or type(reply.get('data')) is not list
            or len(reply['data']) != 1 or type(reply['data'][0]) is not list):
        raise refuse()
    for row in reply['data'][0]:
        if type(row) is not list or len(row) != 2 or any(type(v) is not str for v in row):
            raise refuse()
        if Path(row[0]).name in UNITS:
            raise refuse()


def unit_metadata(unit):
    """Propriétés publiques fermées ; aucune valeur de credential ou environnement."""
    if unit not in UNITS:
        raise refuse()
    reply = bus('GetUnit', 's', unit)
    if (reply.get('type') != 'o' or type(reply.get('data')) is not list
            or len(reply['data']) != 1 or type(reply['data'][0]) is not str
            or not re.fullmatch(r'/org/freedesktop/systemd1/unit/[A-Za-z0-9_]+', reply['data'][0])):
        raise refuse()
    path = reply['data'][0]
    values = {}
    fields = [('Unit', 'Description', 's', str), ('Unit', 'Transient', 'b', bool),
              ('Unit', 'FragmentPath', 's', str), ('Unit', 'ActiveState', 's', str),
              ('Unit', 'SubState', 's', str), ('Service', 'User', 's', str),
              ('Service', 'MainPID', 'u', int), ('Service', 'Result', 's', str),
              ('Service', 'ExecMainStatus', 'i', int)]
    for interface, name, signature, expected in fields:
        value = json.loads(run(['/usr/bin/busctl', '--system', '--json=short',
            'get-property', 'org.freedesktop.systemd1', path,
            'org.freedesktop.systemd1.' + interface, name]))
        if (type(value) is not dict or set(value) != {'type', 'data'}
                or value['type'] != signature or type(value['data']) is not expected):
            raise refuse()
        values[name] = value['data']
    return values


def validate_owned(case, unit, value, *, stopped):
    types = {'Description': str, 'Transient': bool, 'FragmentPath': str,
             'ActiveState': str, 'SubState': str, 'User': str, 'MainPID': int,
             'Result': str, 'ExecMainStatus': int}
    if (unit not in UNITS or case.parent != BASE or not CASE_RE.fullmatch(case.name)
            or type(value) is not dict or set(value) != set(types)
            or any(type(value[key]) is not kind for key, kind in types.items())):
        raise refuse()
    if (value['Description'] != 'Pixs C01 test ' + case.name + ' ' + unit
            or value['Transient'] is not True
            or value['FragmentPath'] != '/run/systemd/transient/' + unit
            or value['User'] != str(UID if unit == CONSUMER else 0)
            or value['MainPID'] < 0
            or value['ActiveState'] not in ('active', 'inactive', 'failed', 'activating',
                                          'deactivating', 'reloading', 'maintenance', 'refreshing')):
        raise refuse()
    if stopped and (value['ActiveState'] not in ('inactive', 'failed') or value['MainPID'] != 0):
        raise refuse()


def present_owned(case, unit, *, stopped):
    if unit not in UNITS:
        raise refuse()
    if unit not in loaded_units():
        return None
    try:
        value = unit_metadata(unit)
    except ValueError:
        # Une unité transitoire peut disparaître entre les deux lectures.
        if unit not in loaded_units():
            return None
        raise
    validate_owned(case, unit, value, stopped=stopped)
    return value


def record_public(case, prefix, value):
    from pixs.backend.bootstrap_audit import generate_uuidv7
    if prefix not in ('recovery-before', 'recovery-after', 'cleanup-before', 'cleanup-after'):
        raise refuse()
    verified, gid = load_plan(case / 'plan.json')
    if verified != case:
        raise refuse()
    write_json(case / (prefix + '-' + generate_uuidv7() + '.json'), value, 0, gid, 0o644)


def wait_absent(names, seconds=3):
    if (not set(names) <= set(UNITS) or type(seconds) is not int or not 1 <= seconds <= 3):
        raise refuse()
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if not set(names) & loaded_units():
            return
        time.sleep(0.05)
    raise refuse()


def stop_owned(case, unit, *, already_stopped=False):
    if present_owned(case, unit, stopped=already_stopped) is None:
        return
    run(['/usr/bin/systemctl', '--system', '--no-ask-password', 'stop', '--', unit], 10)
    value = present_owned(case, unit, stopped=True)
    if value is not None and value['ActiveState'] == 'failed':
        run(['/usr/bin/systemctl', '--system', '--no-ask-password', 'reset-failed', '--', unit], 10)
    wait_absent([unit])


def recover_case(raw):
    """Récupération explicite d'un ancien cas, uniquement arrêté et identifié."""
    if os.getuid() != 0 or os.geteuid() != 0:
        raise refuse()
    case, _gid = load_plan(Path(raw) / 'plan.json')
    states = {}
    # Les deux identités sont contrôlées avant la première écriture ou commande.
    for unit in UNITS:
        value = present_owned(case, unit, stopped=True)
        if value is not None:
            states[unit] = value
    record_public(case, 'recovery-before', {'case': str(case), 'units': states})
    for unit in states:
        # Ne pas arrêter une nouvelle activation apparue après le relevé initial.
        present_owned(case, unit, stopped=True)
        stop_owned(case, unit, already_stopped=True)
    wait_absent(states)
    record_public(case, 'recovery-after', {'case': str(case), 'units_absent': list(states)})


def sync_dir(path):
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def mkdir(path, uid, gid, mode):
    os.mkdir(path, mode)
    os.chown(path, uid, gid)
    os.chmod(path, mode)
    sync_dir(path.parent)


def write_exclusive(path, data, uid, gid, mode):
    checked_path(path.parent)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        view = memoryview(data)
        while view:
            count = os.write(descriptor, view)
            if count <= 0:
                raise refuse()
            view = view[count:]
        os.fchown(descriptor, uid, gid)
        os.fchmod(descriptor, mode)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    sync_dir(path.parent)


def write_json(path, value, uid, gid, mode=0o600):
    data = (json.dumps(value, sort_keys=True, allow_nan=False) + '\n').encode('utf-8')
    write_exclusive(path, data, uid, gid, mode)


def read_json(path, uid, mode):
    checked_path(path)
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        metadata = os.fstat(descriptor)
        if (not stat.S_ISREG(metadata.st_mode) or metadata.st_uid != uid
                or metadata.st_nlink != 1 or stat.S_IMODE(metadata.st_mode) != mode
                or not 0 < metadata.st_size <= 65536):
            raise refuse()
        data = b''
        while len(data) < metadata.st_size:
            chunk = os.read(descriptor, metadata.st_size - len(data))
            if not chunk:
                raise refuse()
            data += chunk
    finally:
        os.close(descriptor)
    value = json.loads(data)
    if type(value) is not dict:
        raise refuse()
    return value


def load_plan(path):
    path = Path(path)
    if path.name != 'plan.json' or path.parent.parent != BASE or not CASE_RE.fullmatch(path.parent.name):
        raise refuse()
    plan = read_json(path, 0, 0o640)
    gid = pwd.getpwuid(UID).pw_gid
    expected = {'case': str(path.parent), 'uid': UID, 'gid': gid,
                'consumer': CONSUMER, 'operator': OPERATOR, 'schema_version': 1}
    metadata = path.parent.lstat()
    if (plan != expected or metadata.st_uid != 0 or metadata.st_gid != gid
            or stat.S_IMODE(metadata.st_mode) != 0o750):
        raise refuse()
    return path.parent, gid


def source(case, *, proposed=False):
    from pixs.backend.bootstrap_policy import PolicySource
    return PolicySource(path=str(case / ('stage/next.toml' if proposed else 'policy.toml')),
                        owner_uid=0, policy_id=POLICY_ID, max_policy_bytes=16384)


def wait_json(path, uid, mode, seconds):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        try:
            return read_json(path, uid, mode)
        except FileNotFoundError:
            time.sleep(0.05)
    raise refuse()


def marker(case, version, seconds):
    value = wait_json(case / 'worker' / ('ready-' + version + '.json'), UID, 0o600, seconds)
    if (set(value) != {'version', 'invocation'} or value['version'] != version
            or type(value['invocation']) is not str
            or not INV_RE.fullmatch(value['invocation']) or set(value['invocation']) == {'0'}):
        raise refuse()
    return value


def fixture_policy(case):
    from pixs.backend.bootstrap_audit import generate_uuidv7
    from pixs.backend.bootstrap_policy import C01Policy, CredentialBinding
    from pixs.kernel.config.resolution import SecretReference
    now = datetime.now(timezone.utc)
    begin, end = (now - timedelta(seconds=1)).isoformat(), (now + timedelta(seconds=240)).isoformat()
    bindings = tuple(CredentialBinding(
        reference=SecretReference(owner_id='pixs.backend', entry_id=entry, source='systemd:c01:' + name),
        credential_name=name, credential_version='v1', valid_from=begin, valid_until=end,
        encrypted_source=str(case / 'cipher' / name))
        for name, entry in (('key', 'django_secret_key'), ('pwd', 'db_password')))
    return C01Policy(policy_id=POLICY_ID, policy_version='1', uid=UID,
        unit=CONSUMER, manager='system', role='web', purpose=PURPOSE,
        credential_dir='/run/credentials/' + CONSUMER, bindings=bindings,
        valid_from=begin, valid_until=end, max_event_bytes=8192,
        max_journal_bytes=1048576, max_credential_bytes=16384, max_ttl_s=300,
        max_revocation_delay_s=60, max_stop_budget_s=2, max_restart_budget_s=15,
        journal_dir=str(case / 'journal'), journal_uid=UID,
        journal_id=generate_uuidv7(), retention_days=1, scope_literal='PLATFORM',
        controller_uid=0, controller_unit=OPERATOR, holds=(),
        allowed_actions=('resolve', 'rotate', 'revoke'), revoked_versions=())


def encrypt_fixture(name, version, target, gid):
    if target.exists():
        raise refuse()
    data = json.dumps({'schema_version': 1, 'credential_version': version,
                       'value': FIXTURES[version][name]}, separators=(',', ':')).encode('utf-8')
    run(['/usr/bin/systemd-creds', 'encrypt', '--with-key=null', '--name=' + name,
         '-', str(target)], 20, data=data)
    metadata = target.lstat()
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_uid != 0 or metadata.st_nlink != 1:
        raise refuse()
    os.chown(target, 0, gid)
    os.chmod(target, 0o400)
    descriptor = os.open(target, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    sync_dir(target.parent)


def create_fixture(case, gid):
    from pixs.backend.bootstrap_policy import render_c01_policy
    mkdir(case, 0, gid, 0o750)
    for name in ('cipher', 'stage'):
        mkdir(case / name, 0, gid, 0o700)
    for name in ('journal', 'worker'):
        mkdir(case / name, UID, gid, 0o700)
    write_json(case / 'plan.json', {'case': str(case), 'uid': UID, 'gid': gid,
        'consumer': CONSUMER, 'operator': OPERATOR, 'schema_version': 1}, 0, gid, 0o640)
    current = fixture_policy(case)
    proposed = replace(current, policy_version='2', revoked_versions=('v1',),
                       bindings=tuple(replace(b, credential_version='v2') for b in current.bindings))
    write_exclusive(case / 'policy.toml', render_c01_policy(current).encode('utf-8'), 0, gid, 0o640)
    write_exclusive(case / 'stage/next.toml', render_c01_policy(proposed).encode('utf-8'), 0, gid, 0o600)
    for name in ('key', 'pwd'):
        encrypt_fixture(name, 'v1', case / 'cipher' / name, gid)
        encrypt_fixture(name, 'v2', case / 'stage' / (name + '.encrypted'), gid)


def unit_command(case, unit):
    consumer = unit == CONSUMER
    if unit not in UNITS:
        raise refuse()
    props = {'Description': 'Pixs C01 test ' + case.name + ' ' + unit,
             'User': str(UID if consumer else 0), 'WorkingDirectory': str(ROOT),
             'Type': 'exec', 'RuntimeMaxSec': '30' if consumer else '45',
             'RuntimeRandomizedExtraSec': '0', 'TimeoutStopSec': '2',
             'TimeoutStopFailureMode': 'kill', 'KillMode': 'control-group',
             'SendSIGKILL': 'yes', 'Restart': 'no', 'LimitCORE': '0',
             'StandardOutput': 'null', 'StandardError': 'null',
             'Environment': 'PYTHONPATH=' + str(ROOT / 'src')}
    command = ['/usr/bin/systemd-run', '--system', '--quiet', '--unit=' + unit]
    if not consumer:
        command.append('--collect')
    command += ['--property=' + key + '=' + value for key, value in props.items()]
    if consumer:
        command += ['--property=PrivateMounts=yes']
        command += ['--property=LoadCredentialEncrypted=' + name + ':' + str(case / 'cipher' / name)
                    for name in ('key', 'pwd')]
    return command + ['--', str(PYTHON), '-B', str(SELF),
                      '--worker' if consumer else '--controller', '--plan-file', str(case / 'plan.json')]


def worker(path):
    from django.conf import LazySettings
    from pixs.backend.bootstrap_audit import init_journal, read_open_records
    from pixs.backend.bootstrap_policy import load_c01_policy
    from pixs.backend.runtime_resolve import resolve_runtime_settings
    from pixs.backend.settings import build_settings_template
    from pixs.backend.startup_mode import StartupMode
    from pixs.backend.systemd_secret_provider import native
    case, gid = load_plan(path)
    stage = 'identite'
    try:
        native.prove_self(manager='system', expect_uid=UID, expect_unit=CONSUMER)
        stage = 'politique'
        policy = load_c01_policy(source(case))
        stage = 'journal'
        if policy.policy_version == '1':
            init_journal(journal_dir=policy.journal_dir, journal_uid=UID,
                         journal_id=policy.journal_id, retention_days=1, holds=())
        elif policy.policy_version == '2':
            read_open_records(journal_dir=policy.journal_dir, journal_uid=UID,
                journal_id=policy.journal_id, max_journal_bytes=policy.max_journal_bytes,
                max_event_bytes=policy.max_event_bytes)
        else:
            raise refuse()
        version = 'v' + policy.policy_version
        refs = {b.credential_name: b.reference for b in policy.bindings}
        template = build_settings_template(profile='web',
            database={'name': 'fixture', 'user': 'fixture', 'host': '127.0.0.1', 'port': 5432},
            allowed_hosts=['localhost'], secret_key_ref=refs['key'], database_password_ref=refs['pwd'])
        stage = 'resolution'
        runtime = resolve_runtime_settings(template=template, source=source(case),
            mode=StartupMode.INSTALLER, purpose=PURPOSE)
        stage = 'consommation'
        values = runtime.as_dict()
        if (runtime.ready is not False or values['SECRET_KEY'] != FIXTURES[version]['key']
                or values['DATABASES']['default']['PASSWORD'] != FIXTURES[version]['pwd']):
            raise refuse()
        stage = 'django'
        settings = LazySettings()
        settings.configure(**values)
        if settings.SECRET_KEY != FIXTURES[version]['key']:
            raise refuse()
        stage = 'snapshot'
        invocation = native.snapshot_service(manager='system', unit=CONSUMER,
                                             timeout_s=5, uid=UID).invocation_hex
        stage = 'marqueur'
        write_json(case / 'worker' / ('ready-' + version + '.json'),
                   {'version': version, 'invocation': invocation}, UID, gid)
        del values, settings, runtime
        signal.pause()
    except Exception as error:
        # Métadonnées de test seules ; l’exception inattendue reste propagée.
        write_json(case / 'worker' / 'failure.json',
                   {'stage': stage, 'error_type': type(error).__name__}, UID, gid)
        raise


def controller(path):
    from pixs.backend.startup_mode import StartupMode
    from pixs.backend.systemd_secret_provider import native
    from pixs.backend.systemd_secret_provider.lifecycle import rotate_credentials, revoke_credentials
    case, gid = load_plan(path)
    native.prove_self(manager='system', expect_uid=0, expect_unit=OPERATOR)
    stage = 'rotation'
    try:
        rotated = rotate_credentials(source(case), new_policy_source=source(case, proposed=True),
            staged_credentials={name: str(case / 'stage' / (name + '.encrypted')) for name in ('key', 'pwd')},
            mode=StartupMode.INSTALLER, purpose=PURPOSE)
        stage = 'configuration-django-v2'
        ready = marker(case, 'v2', 5)
        if ready['invocation'] != rotated.new_invocation_hex:
            raise refuse()
        stage = 'révocation'
        revoked = revoke_credentials(source(case), mode=StartupMode.INSTALLER, purpose=PURPOSE)
        write_json(case / 'result.json', {'status': 'success', 'rotation': asdict(rotated),
                   'revocation': asdict(revoked)}, 0, gid, 0o644)
    except (ValueError, OSError, subprocess.SubprocessError):
        write_json(case / 'result.json', {'status': 'failure', 'stage': stage}, 0, gid, 0o644)
        raise refuse() from None


def verify_results(case, result):
    from pixs.backend.bootstrap_audit import read_open_records, verify_receipt
    from pixs.backend.bootstrap_policy import load_c01_policy
    if set(result) != {'status', 'rotation', 'revocation'} or result['status'] != 'success':
        raise refuse()
    policy = load_c01_policy(source(case))
    if 'resolve' in policy.allowed_actions or not {'v1', 'v2'} <= set(policy.revoked_versions):
        raise refuse()
    records = read_open_records(journal_dir=policy.journal_dir, journal_uid=UID,
        journal_id=policy.journal_id, max_journal_bytes=policy.max_journal_bytes,
        max_event_bytes=policy.max_event_bytes)
    v1, v2 = marker(case, 'v1', 1), marker(case, 'v2', 1)
    if v1['invocation'] == v2['invocation']:
        raise refuse()
    rotations = result['rotation'], result['revocation']
    for item, action in zip(rotations, ('secret.rotate.completed', 'secret.revoke.completed')):
        receipt = item['completion']
        actual = verify_receipt(journal_dir=policy.journal_dir, journal_uid=UID,
            journal_id=policy.journal_id, event_id=receipt['event_id'],
            max_journal_bytes=policy.max_journal_bytes, max_event_bytes=policy.max_event_bytes)
        if asdict(actual) != receipt or item['unit'] != CONSUMER:
            raise refuse()
        event = next(r.event for r in records if r.event.event_id == receipt['event_id'])
        if (event.action, event.result, event.actor_reference) != (action, 'success', 'uid:0:unit:' + OPERATOR):
            raise refuse()
    if (result['rotation']['old_invocation_hex'] != v1['invocation']
            or result['rotation']['new_invocation_hex'] != v2['invocation']
            or result['revocation']['old_invocation_hex'] != v2['invocation']
            or result['revocation']['new_invocation_hex'] is not None):
        raise refuse()
    for version, ready in (('v1', v1), ('v2', v2)):
        found = set()
        for record in records:
            event = record.event
            if (event.action, event.result, event.actor_reference) == (
                    'secret.resolve', 'success', 'uid:' + str(UID) + ':unit:' + CONSUMER):
                if 'systemd-invocation:' + ready['invocation'] in event.correlation_ids:
                    metadata = json.loads(event.resource_id)
                    if metadata['credential_version'] == version:
                        found.add(metadata['credential_name'])
        if found != {'key', 'pwd'}:
            raise refuse()
    # Seules les fixtures publiques sont comparées ; aucune valeur réelle n'existe dans ce test.
    audit_text = json.dumps([asdict(record) for record in records])
    if any(value in audit_text for pair in FIXTURES.values() for value in pair.values()):
        raise refuse()
    return len(records)


def cleanup(case, attempted):
    if len(set(attempted)) != len(attempted) or not set(attempted) <= set(UNITS):
        raise refuse()
    if not attempted:
        return
    states = {}
    for unit in attempted:
        value = present_owned(case, unit, stopped=False)
        if value is not None:
            states[unit] = value
    record_public(case, 'cleanup-before', {'case': str(case), 'units': states})
    errors = []
    for unit in reversed(attempted):
        try:
            stop_owned(case, unit)
        except (ValueError, OSError, subprocess.SubprocessError):
            errors.append(unit)
    if errors:
        raise ValueError('arrêt des unités du test non prouvé : ' + ','.join(errors))
    record_public(case, 'cleanup-after', {'case': str(case), 'units_absent': list(attempted)})


def execute(recovery=None):
    if os.getuid() != 0 or os.geteuid() != 0:
        raise refuse()
    from pixs.backend.bootstrap_audit import generate_uuidv7
    if recovery is not None:
        recover_case(recovery)
    assert_absent()
    checked_path(BASE.parent)
    if not BASE.exists():
        mkdir(BASE, 0, pwd.getpwuid(UID).pw_gid, 0o755)
    checked_path(BASE)
    case = BASE / generate_uuidv7()
    attempted = []
    stage = 'fixtures'
    success = False
    failure = None
    try:
        gid = pwd.getpwuid(UID).pw_gid
        create_fixture(case, gid)
        stage = 'démarrage-consommateur'
        attempted.append(CONSUMER)
        run(unit_command(case, CONSUMER), 15)
        marker(case, 'v1', 20)
        stage = 'démarrage-opérateur'
        attempted.append(OPERATOR)
        run(unit_command(case, OPERATOR), 15)
        stage = 'résultat-opérateur'
        result = wait_json(case / 'result.json', 0, 0o644, 60)
        stage = 'preuves'
        count = verify_results(case, result)
        success = True
    except (ValueError, OSError, subprocess.SubprocessError, KeyError, StopIteration) as error:
        failure = {'status': 'failure', 'type': type(error).__name__, 'stage': stage, 'case': str(case)}
        if case.exists():
            write_json(case / 'execution.json', failure, 0, pwd.getpwuid(UID).pw_gid, 0o644)
    finally:
        # Les seuls noms autorisés ont été constatés absents puis tentés par ce test.
        cleanup(case, attempted)
    if not success:
        print(json.dumps(failure, sort_keys=True))
        return 1
    print(json.dumps({'status': 'success', 'case': str(case), 'audit_records': count,
        'units_stopped': list(UNITS), 'crypto_qualification': False,
        'transport': 'LoadCredentialEncrypted --with-key=null public fixture only'}, sort_keys=True))
    return 0


def plan():
    print(json.dumps({'command': ' '.join(COMMAND), 'argv': COMMAND, 'units': list(UNITS), 'consumer_uid': UID,
        'operator_uid': 0, 'fixture_root': str(BASE), 'effects':
        ['création de fixtures publiques', 'deux unités système transitoires',
         'rotation par arrêt et démarrage contrôlés', 'révocation et arrêt des deux unités',
         'conservation des preuves sans purge'],
        'host_key_created': False, 'crypto_qualification': False}, sort_keys=True, ensure_ascii=False))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--plan', action='store_true')
    modes.add_argument('--execute', action='store_true')
    modes.add_argument('--worker', action='store_true')
    modes.add_argument('--controller', action='store_true')
    parser.add_argument('--plan-file', type=Path)
    parser.add_argument('--recover-case', type=Path)
    args = parser.parse_args(argv)
    if args.recover_case is not None and not args.execute:
        parser.error('--recover-case exige --execute')
    if args.plan:
        return plan()
    if args.execute:
        return execute(recovery=args.recover_case)
    if args.plan_file is None:
        parser.error('--plan-file requis pour unité du test')
    if args.worker:
        worker(args.plan_file)
    else:
        controller(args.plan_file)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
