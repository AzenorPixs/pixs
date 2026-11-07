"""Recette S2b1, verificateur reel seul, sans miroir. Fixtures synthetiques."""
from __future__ import annotations

import builtins
import copy
import dataclasses
import hashlib
import json
import os
import pathlib
import socket
import subprocess
import traceback
import unittest
import urllib.request
from unittest.mock import patch

from pixs.pa_native.build_profile import ProfileError
from pixs.pa_native.selection_file_consistency import CythonMismatchError
from pixs.pa_native.selection_file_consistency import FileConsistency
from pixs.pa_native.selection_file_consistency import FileConsistencyError
from pixs.pa_native.selection_file_consistency import verify_selection_files

CODE_E = 'PA01_CAMPAIGN_EVIDENCE_INVALID'
CODE_M = 'PA01_BUILD_CYTHON_MISMATCH'
CODE_D = 'PA01_CAMPAIGN_METADATA_INVALID'
CY = '3.3.0'
CAMP = 'pa01-2026-10-26-c1'
WHEN = '2026-10-26T21:11:03Z'
SRC = 'https://pypi.org/pypi/Cython/json'


def _h(b):
    return hashlib.sha256(b).hexdigest()


def _profile(cy):
    return (
        'schema_version = "1.0.0"\nprofile_version = "1.0.0"\n'
        '[target]\nos = "debian"\nrelease = "13"\narch = "x86_64"\nenvironments = ["physical", "vm"]\n'
        '[toolchain]\ncpython = "3.14.9"\ncython = "' + cy + '"\ngil = true\nsoabi = "cpython-314-x86_64-linux-gnu"\nlinkage = "static"\n'
        '[layout]\nbin = "bin"\nruntime = "runtime"\nlib = "lib"\n'
        '[[executables]]\nname = "pixs-pa-system"\nowner = "pixs.agent"\nmodes = ["system-daemon"]\nsource = "bin/a"\n'
        '[[executables]]\nname = "pixs-pa-events"\nowner = "pixs.agent"\nmodes = ["system-start", "system-stop"]\nsource = "bin/b"\n'
        '[[executables]]\nname = "pixs-pa-session"\nowner = "pixs.agent"\nmodes = ["session-start", "session-stop", "session-daemon"]\nsource = "bin/c"\n'
        '[[executables]]\nname = "pzt"\nowner = "pixs.pzt"\nmodes = ["pzt-daemon"]\nsource = "bin/d"\n'
        '[[operations]]\nname = "inspect_postgresql"\nversion = "1.0.0"\nowner = "pixs.agent"\nmode = "system-daemon"\ncriticality = "Protégé"\ncontract = "pixs.agent.postgresql.inspect_postgresql"\nsource = "op/a"\n'
        '[[operations]]\nname = "prepare_postgresql"\nversion = "1.0.0"\nowner = "pixs.agent"\nmode = "system-daemon"\ncriticality = "Critique"\ncontract = "pixs.agent.postgresql.prepare_postgresql"\nsource = "op/b"\n'
        '[[operations]]\nname = "get_postgresql_result"\nversion = "1.0.0"\nowner = "pixs.agent"\nmode = "system-daemon"\ncriticality = "Protégé"\ncontract = "pixs.agent.postgresql.get_postgresql_result"\nsource = "op/c"\n'
        '[[dependencies]]\nname = "Nuitka"\nversion = "2.7.13"\nprovenance = "pypi"\nlicense = "Apache-2.0"\nsha256 = "' + 'a' * 64 + '"\n'
    )


def _envelope(camp, cy, when, snap, snapsha, dists):
    s = (
        'schema_version = "1.0.0"\n[campaign]\nid = "' + camp + '"\ncomponent = "pa01"\n'
        '[toolchain]\ncython = "' + cy + '"\n[selection]\nverified_at = "' + when + '"\n'
        'source_url = "' + SRC + '"\nsnapshot = "' + snap + '"\nsnapshot_sha256 = "' + snapsha + '"\n'
    )
    for fn, url, sha in dists:
        s += '[[distributions]]\nfilename = "' + fn + '"\nurl = "' + url + '"\nsha256 = "' + sha + '"\n'
    return s


def _pyproject(reqs):
    return '[build-system]\nrequires = [' + ', '.join(json.dumps(r) for r in reqs) + ']\nbuild-backend = "setuptools.build_meta"\n'


def _nominal():
    pp = 'evidence/build-profile.toml'
    em = 'evidence/campaign.toml'
    py = 'evidence/pyproject.toml'
    sn = 'evidence/snap.json'
    d1p = 'dist/cython-3.3.0-py3-none-any.whl'
    d2p = 'dist/cython-3.3.0.tar.gz'
    prof = _profile(CY).encode('utf-8')
    snapb = b'{"rel":1}'
    b1 = b'dist-one'
    b2 = b'dist-two'
    pyr = _pyproject(['Cython==' + CY, 'Nuitka==2.7.13']).encode('utf-8')
    env = _envelope(CAMP, CY, WHEN, sn, _h(snapb), [
        ('cython-3.3.0-py3-none-any.whl', 'https://files.pythonhosted.org/x/a.whl', _h(b1)),
        ('cython-3.3.0.tar.gz', 'https://files.pythonhosted.org/x/b.tar.gz', _h(b2)),
    ]).encode('utf-8')
    files = {pp: prof, em: env, py: pyr, sn: snapb, d1p: b1, d2p: b2}
    man = {
        'schema_version': '1.0.0', 'campaign_id': CAMP, 'component': 'pa01',
        'cython_version': CY, 'verified_at': WHEN, 'source_url': SRC,
        'acquisition': {
            'requested_url': SRC, 'final_url': SRC,
            'started_at': '2026-10-26T21:10:59Z', 'finished_at': WHEN,
            'http_status': 200, 'client_ref': 'c1', 'tls_policy_ref': 't1',
        },
        'files': [
            {'role': 'build_profile', 'path': pp, 'sha256': _h(prof)},
            {'role': 'campaign_metadata', 'path': em, 'sha256': _h(env)},
            {'role': 'pyproject', 'path': py, 'sha256': _h(pyr)},
            {'role': 'pypi_snapshot', 'path': sn, 'sha256': _h(snapb)},
            {'role': 'distribution', 'path': d1p, 'sha256': _h(b1)},
            {'role': 'distribution', 'path': d2p, 'sha256': _h(b2)},
        ],
    }
    mb = json.dumps(man, separators=(',', ':')).encode('utf-8')
    return mb, files, man


def _rebuild(man, files):
    mb = json.dumps(man, separators=(',', ':')).encode('utf-8')
    return mb, dict(files)


def _set_pyproject(man, files, text: bytes):
    files = dict(files)
    man = copy.deepcopy(man)
    pp = [f['path'] for f in man['files'] if f['role'] == 'pyproject'][0]
    files[pp] = text
    for f in man['files']:
        if f['path'] == pp:
            f['sha256'] = _h(text)
    return _rebuild(man, files)


class _NoEnviron:
    def __getitem__(self, key):
        raise AssertionError('environ interdit')
    def __iter__(self):
        raise AssertionError('environ interdit')
    def __len__(self):
        raise AssertionError('environ interdit')
    def get(self, *a, **k):
        raise AssertionError('environ interdit')
    def keys(self):
        raise AssertionError('environ interdit')
    def items(self):
        raise AssertionError('environ interdit')
    def values(self):
        raise AssertionError('environ interdit')
    def __contains__(self, key):
        raise AssertionError('environ interdit')


class _BadDict(dict):
    def items(self):
        raise AssertionError('callback interdit')


class _BadStr(str):
    pass


class _BadBytes(bytes):
    pass


def _raise(*a, **k):
    raise AssertionError('io interdite')


class FileConsistencyTest(unittest.TestCase):
    def test_nominal_two_distributions(self):
        mb, files, man = _nominal()
        r = verify_selection_files(mb, files)
        self.assertIs(type(r), FileConsistency)
        self.assertEqual(r.campaign_id, CAMP)
        self.assertEqual(r.manifest_sha256, _h(mb))
        self.assertEqual(len(r.distributions), 2)

    def test_singleton_same_basename_allowed(self):
        mb, files, man = _nominal()
        man = copy.deepcopy(man)
        new = ['x/same.toml', 'y/same.toml', 'z/same.toml', 'w/same.toml']
        nf = {}
        for f, np in zip([f for f in man['files'] if f['role'] != 'distribution'], new):
            nf[np] = files[f['path']]
            f['path'] = np
        for f in man['files']:
            if f['role'] == 'distribution':
                nf[f['path']] = files[f['path']]
        for f in man['files']:
            if f['role'] != 'distribution':
                f['sha256'] = _h(nf[f['path']])
        env_text = nf[new[1]].decode('utf-8')
        snap_path = [f['path'] for f in man['files'] if f['role'] == 'pypi_snapshot'][0]
        out = []
        for ln in env_text.split('\n'):
            if ln.startswith('snapshot = '):
                out.append('snapshot = "' + snap_path + '"')
            else:
                out.append(ln)
        nf[new[1]] = ('\n'.join(out)).encode('utf-8')
        for f in man['files']:
            if f['path'] == new[1]:
                f['sha256'] = _h(nf[new[1]])
        mb2, files2 = _rebuild(man, nf)
        r = verify_selection_files(mb2, files2)
        self.assertEqual(r.campaign_id, CAMP)

    def test_sha_mismatch_build_profile(self):
        mb, files, man = _nominal()
        files = dict(files)
        pp = [f['path'] for f in man['files'] if f['role'] == 'build_profile'][0]
        files[pp] = b'altered'
        with self.assertRaises(FileConsistencyError) as c:
            verify_selection_files(mb, files)
        self.assertIn(CODE_E, str(c.exception))

    def test_sha_mismatch_campaign_metadata(self):
        mb, files, man = _nominal()
        files = dict(files)
        pp = [f['path'] for f in man['files'] if f['role'] == 'campaign_metadata'][0]
        files[pp] = b'altered'
        with self.assertRaises(FileConsistencyError) as c:
            verify_selection_files(mb, files)
        self.assertIn(CODE_E, str(c.exception))

    def test_sha_mismatch_pyproject(self):
        mb, files, man = _nominal()
        files = dict(files)
        pp = [f['path'] for f in man['files'] if f['role'] == 'pyproject'][0]
        files[pp] = b'altered'
        with self.assertRaises(FileConsistencyError) as c:
            verify_selection_files(mb, files)
        self.assertIn(CODE_E, str(c.exception))

    def test_sha_mismatch_snapshot(self):
        mb, files, man = _nominal()
        files = dict(files)
        pp = [f['path'] for f in man['files'] if f['role'] == 'pypi_snapshot'][0]
        files[pp] = b'altered'
        with self.assertRaises(FileConsistencyError) as c:
            verify_selection_files(mb, files)
        self.assertIn(CODE_E, str(c.exception))

    def test_sha_mismatch_distribution(self):
        mb, files, man = _nominal()
        files = dict(files)
        pp = [f['path'] for f in man['files'] if f['role'] == 'distribution'][0]
        files[pp] = b'altered'
        with self.assertRaises(FileConsistencyError) as c:
            verify_selection_files(mb, files)
        self.assertIn(CODE_E, str(c.exception))

    def test_missing_file_key(self):
        mb, files, man = _nominal()
        files = dict(files)
        files.pop([f['path'] for f in man['files'] if f['role'] == 'distribution'][0])
        with self.assertRaises(FileConsistencyError) as c:
            verify_selection_files(mb, files)
        self.assertIn(CODE_E, str(c.exception))

    def test_extra_file_key(self):
        mb, files, man = _nominal()
        files = dict(files)
        files['extra/x.bin'] = b'x'
        with self.assertRaises(FileConsistencyError) as c:
            verify_selection_files(mb, files)
        self.assertIn(CODE_E, str(c.exception))

    def test_files_not_dict(self):
        mb, files, man = _nominal()
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb, [(k, v) for k, v in files.items()])

    def test_manifest_not_bytes(self):
        mb, files, man = _nominal()
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb.decode('utf-8'), files)

    def test_file_value_not_bytes(self):
        mb, files, man = _nominal()
        files = dict(files)
        k = next(iter(files))
        files[k] = files[k].decode('utf-8')
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb, files)

    def test_files_dict_subclass_refused(self):
        mb, files, man = _nominal()
        bad = _BadDict(files)
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb, bad)

    def test_file_key_str_subclass_refused(self):
        mb, files, man = _nominal()
        files = dict(files)
        k = next(iter(files))
        v = files.pop(k)
        files[_BadStr(k)] = v
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb, files)

    def test_file_value_bytes_subclass_refused(self):
        mb, files, man = _nominal()
        files = dict(files)
        k = next(iter(files))
        files[k] = _BadBytes(files[k])
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb, files)

    def test_campaign_id_mismatch(self):
        mb, files, man = _nominal()
        files = dict(files)
        man = copy.deepcopy(man)
        em_path = [f['path'] for f in man['files'] if f['role'] == 'campaign_metadata'][0]
        env = files[em_path].decode('utf-8').replace(CAMP, 'pa01-2026-10-26-c2')
        files[em_path] = env.encode('utf-8')
        for f in man['files']:
            if f['path'] == em_path:
                f['sha256'] = _h(files[em_path])
        mb2, files2 = _rebuild(man, files)
        with self.assertRaises(FileConsistencyError) as c:
            verify_selection_files(mb2, files2)
        self.assertIn(CODE_E, str(c.exception))

    def test_component_mismatch(self):
        mb, files, man = _nominal()
        man = copy.deepcopy(man)
        man['component'] = 'pbo'
        mb2, files2 = _rebuild(man, files)
        with self.assertRaises(ProfileError) as c:
            verify_selection_files(mb2, files2)
        self.assertIn(CODE_D, str(c.exception))

    def test_verified_at_mismatch(self):
        mb, files, man = _nominal()
        files = dict(files)
        man = copy.deepcopy(man)
        em_path = [f['path'] for f in man['files'] if f['role'] == 'campaign_metadata'][0]
        env = files[em_path].decode('utf-8').replace(WHEN, '2026-10-26T21:12:00Z')
        files[em_path] = env.encode('utf-8')
        for f in man['files']:
            if f['path'] == em_path:
                f['sha256'] = _h(files[em_path])
        mb2, files2 = _rebuild(man, files)
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb2, files2)

    def test_snapshot_path_mismatch(self):
        mb, files, man = _nominal()
        files = dict(files)
        man = copy.deepcopy(man)
        em_path = [f['path'] for f in man['files'] if f['role'] == 'campaign_metadata'][0]
        env = files[em_path].decode('utf-8').replace('evidence/snap.json', 'evidence/other.json')
        files[em_path] = env.encode('utf-8')
        for f in man['files']:
            if f['path'] == em_path:
                f['sha256'] = _h(files[em_path])
        mb2, files2 = _rebuild(man, files)
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb2, files2)

    def test_distribution_basename_ambiguous(self):
        mb, files, man = _nominal()
        man = copy.deepcopy(man)
        files = dict(files)
        d0 = [f for f in man['files'] if f['role'] == 'distribution'][0]
        d1 = [f for f in man['files'] if f['role'] == 'distribution'][1]
        new_path = 'other/' + d0['path'].split('/')[-1]
        files[new_path] = files[d1['path']]
        del files[d1['path']]
        d1['path'] = new_path
        d1['sha256'] = _h(files[new_path])
        mb2, files2 = _rebuild(man, files)
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb2, files2)

    def test_distribution_set_mismatch(self):
        mb, files, man = _nominal()
        files = dict(files)
        man = copy.deepcopy(man)
        nb = b'new-dist-bytes'
        ndp = 'dist/new-3.3.0.tar.gz'
        d0 = [f for f in man['files'] if f['role'] == 'distribution'][0]
        files[ndp] = nb
        del files[d0['path']]
        d0['path'] = ndp
        d0['sha256'] = _h(nb)
        mb2, files2 = _rebuild(man, files)
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb2, files2)

    def test_profile_version_mismatch(self):
        mb, files, man = _nominal()
        files = dict(files)
        man = copy.deepcopy(man)
        pp = [f['path'] for f in man['files'] if f['role'] == 'build_profile'][0]
        files[pp] = _profile('3.2.0').encode('utf-8')
        for f in man['files']:
            if f['path'] == pp:
                f['sha256'] = _h(files[pp])
        mb2, files2 = _rebuild(man, files)
        with self.assertRaises(CythonMismatchError) as c:
            verify_selection_files(mb2, files2)
        self.assertIn(CODE_M, str(c.exception))

    def test_envelope_version_mismatch(self):
        mb, files, man = _nominal()
        files = dict(files)
        man = copy.deepcopy(man)
        em_path = [f['path'] for f in man['files'] if f['role'] == 'campaign_metadata'][0]
        sn = [f['path'] for f in man['files'] if f['role'] == 'pypi_snapshot'][0]
        snapb = files[sn]
        dpaths = [f['path'] for f in man['files'] if f['role'] == 'distribution']
        env = _envelope(CAMP, '3.2.0', WHEN, sn, _h(snapb), [
            ('cython-3.3.0-py3-none-any.whl', 'https://files.pythonhosted.org/x/a.whl', _h(files[dpaths[0]])),
            ('cython-3.3.0.tar.gz', 'https://files.pythonhosted.org/x/b.tar.gz', _h(files[dpaths[1]])),
        ]).encode('utf-8')
        files[em_path] = env
        for f in man['files']:
            if f['path'] == em_path:
                f['sha256'] = _h(env)
        mb2, files2 = _rebuild(man, files)
        with self.assertRaises(CythonMismatchError):
            verify_selection_files(mb2, files2)

    def test_pyproject_version_mismatch(self):
        mb, files, man = _nominal()
        mb2, files2 = _set_pyproject(man, files, _pyproject(['Cython==3.2.0', 'Nuitka==2.7.13']).encode('utf-8'))
        with self.assertRaises(CythonMismatchError):
            verify_selection_files(mb2, files2)

    def test_manifest_cython_version_mismatch(self):
        mb, files, man = _nominal()
        man = copy.deepcopy(man)
        man['cython_version'] = '3.2.0'
        mb2, files2 = _rebuild(man, files)
        with self.assertRaises(CythonMismatchError) as c:
            verify_selection_files(mb2, files2)
        self.assertIn(CODE_M, str(c.exception))

    def test_envelope_snapshot_sha_mismatch(self):
        mb, files, man = _nominal()
        files = dict(files)
        man = copy.deepcopy(man)
        em_path = [f['path'] for f in man['files'] if f['role'] == 'campaign_metadata'][0]
        sn = [f['path'] for f in man['files'] if f['role'] == 'pypi_snapshot'][0]
        snapb = files[sn]
        dpaths = [f['path'] for f in man['files'] if f['role'] == 'distribution']
        env = _envelope(CAMP, CY, WHEN, sn, 'b' * 64, [
            ('cython-3.3.0-py3-none-any.whl', 'https://files.pythonhosted.org/x/a.whl', _h(files[dpaths[0]])),
            ('cython-3.3.0.tar.gz', 'https://files.pythonhosted.org/x/b.tar.gz', _h(files[dpaths[1]])),
        ]).encode('utf-8')
        files[em_path] = env
        for f in man['files']:
            if f['path'] == em_path:
                f['sha256'] = _h(env)
        mb2, files2 = _rebuild(man, files)
        with self.assertRaises(FileConsistencyError) as c:
            verify_selection_files(mb2, files2)
        self.assertIn(CODE_E, str(c.exception))

    def test_envelope_distribution_sha_mismatch(self):
        mb, files, man = _nominal()
        files = dict(files)
        man = copy.deepcopy(man)
        em_path = [f['path'] for f in man['files'] if f['role'] == 'campaign_metadata'][0]
        sn = [f['path'] for f in man['files'] if f['role'] == 'pypi_snapshot'][0]
        snapb = files[sn]
        dpaths = [f['path'] for f in man['files'] if f['role'] == 'distribution']
        env = _envelope(CAMP, CY, WHEN, sn, _h(snapb), [
            ('cython-3.3.0-py3-none-any.whl', 'https://files.pythonhosted.org/x/a.whl', 'c' * 64),
            ('cython-3.3.0.tar.gz', 'https://files.pythonhosted.org/x/b.tar.gz', _h(files[dpaths[1]])),
        ]).encode('utf-8')
        files[em_path] = env
        for f in man['files']:
            if f['path'] == em_path:
                f['sha256'] = _h(env)
        mb2, files2 = _rebuild(man, files)
        with self.assertRaises(FileConsistencyError) as c:
            verify_selection_files(mb2, files2)
        self.assertIn(CODE_E, str(c.exception))

    def test_pyproject_missing_requires(self):
        mb, files, man = _nominal()
        mb2, files2 = _set_pyproject(man, files, b'[build-system]\nbuild-backend = "setuptools.build_meta"\n')
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb2, files2)

    def test_pyproject_no_cython(self):
        mb, files, man = _nominal()
        mb2, files2 = _set_pyproject(man, files, _pyproject(['Nuitka==2.7.13']).encode('utf-8'))
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb2, files2)

    def test_pyproject_double_cython(self):
        mb, files, man = _nominal()
        mb2, files2 = _set_pyproject(man, files, _pyproject(['Cython==' + CY, 'cython==3.2.0']).encode('utf-8'))
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb2, files2)

    def test_pyproject_double_with_url_extra(self):
        mb, files, man = _nominal()
        mb2, files2 = _set_pyproject(man, files, _pyproject(['Cython==' + CY, 'Cython[extra] @ https://exemple.invalid/archive.whl']).encode('utf-8'))
        with self.assertRaises(FileConsistencyError) as c:
            verify_selection_files(mb2, files2)
        self.assertIn(CODE_E, str(c.exception))

    def test_pyproject_inexact_constraint(self):
        mb, files, man = _nominal()
        mb2, files2 = _set_pyproject(man, files, _pyproject(['Cython>=3.3.0']).encode('utf-8'))
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb2, files2)

    def test_pyproject_url_reference(self):
        mb, files, man = _nominal()
        mb2, files2 = _set_pyproject(man, files, _pyproject(['Cython @ https://example.com/c.tar.gz']).encode('utf-8'))
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb2, files2)

    def test_pyproject_conditional_marker(self):
        mb, files, man = _nominal()
        mb2, files2 = _set_pyproject(man, files, _pyproject(['Cython==' + CY + '; python_version>"3"']).encode('utf-8'))
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb2, files2)

    def test_pyproject_tab_variant_positive(self):
        mb, files, man = _nominal()
        decl = 'Cython\t==\t' + CY
        mb2, files2 = _set_pyproject(man, files, _pyproject([decl, 'Nuitka==2.7.13']).encode('utf-8'))
        r = verify_selection_files(mb2, files2)
        self.assertEqual(r.cython_version, CY)
        self.assertEqual(r.pyproject_decl, decl)

    def test_pyproject_case_space_variants(self):
        for decl in ['cython==' + CY, 'CYTHON  ==  ' + CY, 'Cython == ' + CY]:
            mb, files, man = _nominal()
            mb2, files2 = _set_pyproject(man, files, _pyproject([decl, 'Nuitka==2.7.13']).encode('utf-8'))
            r = verify_selection_files(mb2, files2)
            self.assertEqual(r.cython_version, CY)
            self.assertEqual(r.pyproject_decl, decl)

    def test_pyproject_newline_escaped_negative(self):
        mb, files, man = _nominal()
        mb2, files2 = _set_pyproject(man, files, b'[build-system]\nrequires = ["Cython==3.3.0\\n"]\n')
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb2, files2)

    def test_pyproject_cr_escaped_negative(self):
        mb, files, man = _nominal()
        mb2, files2 = _set_pyproject(man, files, b'[build-system]\nrequires = ["Cython==3.3.0\\r"]\n')
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb2, files2)

    def test_pyproject_decl_preserves_exact(self):
        mb, files, man = _nominal()
        decl = 'cython  ==  ' + CY
        mb2, files2 = _set_pyproject(man, files, _pyproject([decl, 'Nuitka==2.7.13']).encode('utf-8'))
        r = verify_selection_files(mb2, files2)
        self.assertEqual(r.pyproject_decl, decl)
        self.assertEqual(r.pyproject_version, CY)
        self.assertNotEqual(r.pyproject_decl, 'Cython==' + CY)

    def test_pyproject_invalid_toml(self):
        mb, files, man = _nominal()
        mb2, files2 = _set_pyproject(man, files, b'[build-system\nrequires=["x"]\n')
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb2, files2)

    def test_pyproject_invalid_utf8(self):
        mb, files, man = _nominal()
        mb2, files2 = _set_pyproject(man, files, b'[build-system]\nrequires=["\xff"]\n')
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb2, files2)

    def test_pyproject_crlf(self):
        mb, files, man = _nominal()
        files = dict(files)
        man = copy.deepcopy(man)
        pp = [f['path'] for f in man['files'] if f['role'] == 'pyproject'][0]
        files[pp] = files[pp].replace(b'\n', b'\r\n')
        for f in man['files']:
            if f['path'] == pp:
                f['sha256'] = _h(files[pp])
        mb2, files2 = _rebuild(man, files)
        with self.assertRaises(FileConsistencyError):
            verify_selection_files(mb2, files2)

    def test_envelope_invalid_propagates(self):
        mb, files, man = _nominal()
        files = dict(files)
        man = copy.deepcopy(man)
        em_path = [f['path'] for f in man['files'] if f['role'] == 'campaign_metadata'][0]
        files[em_path] = b'schema_version = "9.9.9"\n'
        for f in man['files']:
            if f['path'] == em_path:
                f['sha256'] = _h(files[em_path])
        mb2, files2 = _rebuild(man, files)
        with self.assertRaises(ProfileError) as c:
            verify_selection_files(mb2, files2)
        self.assertIn(CODE_D, str(c.exception))

    def test_profile_error_preserved(self):
        mb, files, man = _nominal()
        files = dict(files)
        man = copy.deepcopy(man)
        pp = [f['path'] for f in man['files'] if f['role'] == 'build_profile'][0]
        bad = _profile(CY).replace('arch = "x86_64"', 'arch = "arm64"').encode('utf-8')
        files[pp] = bad
        for f in man['files']:
            if f['path'] == pp:
                f['sha256'] = _h(bad)
        mb2, files2 = _rebuild(man, files)
        with self.assertRaises(ProfileError) as c:
            verify_selection_files(mb2, files2)
        self.assertNotIn(CODE_E, str(c.exception))

    def test_result_frozen_slots_shas(self):
        mb, files, man = _nominal()
        r = verify_selection_files(mb, files)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            r.campaign_id = 'x'
        pp = [f['path'] for f in man['files'] if f['role'] == 'build_profile'][0]
        em = [f['path'] for f in man['files'] if f['role'] == 'campaign_metadata'][0]
        py = [f['path'] for f in man['files'] if f['role'] == 'pyproject'][0]
        sn = [f['path'] for f in man['files'] if f['role'] == 'pypi_snapshot'][0]
        self.assertEqual(r.manifest_sha256, _h(mb))
        self.assertEqual(r.profile_sha256, _h(files[pp]))
        self.assertEqual(r.envelope_sha256, _h(files[em]))
        self.assertEqual(r.pyproject_sha256, _h(files[py]))
        self.assertEqual(r.snapshot_sha256, _h(files[sn]))
        dists = sorted([(f['path'].split('/')[-1], f['sha256']) for f in man['files'] if f['role'] == 'distribution'])
        self.assertEqual(list(r.distributions), dists)
        for path, sha in [(f['path'], f['sha256']) for f in man['files'] if f['role'] == 'distribution']:
            self.assertEqual(_h(files[path]), sha)
        self.assertFalse(hasattr(r, 'usable'))
        self.assertFalse(hasattr(r, 'verified'))

    def test_diagnostic_no_leak(self):
        marker = 'marqueur-fuite-zzz-123'
        mb0, files0, man0 = _nominal()
        pp0 = [f['path'] for f in man0['files'] if f['role'] == 'build_profile'][0]
        bad_prof = (marker + '[[[invalide').encode('utf-8')
        files1 = dict(files0)
        man1 = copy.deepcopy(man0)
        files1[pp0] = bad_prof
        for f in man1['files']:
            if f['path'] == pp0:
                f['sha256'] = _h(bad_prof)
        mb1, files1 = _rebuild(man1, files1)
        try:
            verify_selection_files(mb1, files1)
        except ProfileError as e:
            s = str(e) + traceback.format_exc()
            self.assertNotIn(marker, s)
        else:
            self.fail('attendu echec profil')
        mb0, files0, man0 = _nominal()
        em0 = [f['path'] for f in man0['files'] if f['role'] == 'campaign_metadata'][0]
        bad_env = (marker + '[[[invalide').encode('utf-8')
        files2 = dict(files0)
        man2 = copy.deepcopy(man0)
        files2[em0] = bad_env
        for f in man2['files']:
            if f['path'] == em0:
                f['sha256'] = _h(bad_env)
        mb2, files2 = _rebuild(man2, files2)
        try:
            verify_selection_files(mb2, files2)
        except ProfileError as e:
            self.assertIn(CODE_D, str(e))
            s = str(e) + traceback.format_exc()
            self.assertNotIn(marker, s)
        else:
            self.fail('attendu echec enveloppe')
        mb0, files0, man0 = _nominal()
        py0 = [f['path'] for f in man0['files'] if f['role'] == 'pyproject'][0]
        bad_py = ('[build-system\nrequires = ["' + marker + '"]\n').encode('utf-8')
        files3 = dict(files0)
        man3 = copy.deepcopy(man0)
        files3[py0] = bad_py
        for f in man3['files']:
            if f['path'] == py0:
                f['sha256'] = _h(bad_py)
        mb3, files3 = _rebuild(man3, files3)
        try:
            verify_selection_files(mb3, files3)
        except FileConsistencyError as e:
            self.assertIn(CODE_E, str(e))
            s = str(e) + traceback.format_exc()
            self.assertNotIn(marker, s)
        else:
            self.fail('attendu echec pyproject')
        bad_mb = (marker + '{invalide').encode('utf-8')
        try:
            verify_selection_files(bad_mb, files0)
        except ProfileError as e:
            self.assertIn(CODE_D, str(e))
            s = str(e) + traceback.format_exc()
            self.assertNotIn(marker, s)
        else:
            self.fail('attendu echec manifeste')

    def test_no_io_env_guards(self):
        mb, files, man = _nominal()
        with patch.object(os, 'environ', new=_NoEnviron()):
            with patch.object(os, 'getenv', new=_raise):
                with patch.object(builtins, 'open', new=_raise):
                    with patch.object(pathlib.Path, 'open', new=_raise):
                        with patch.object(pathlib.Path, 'read_bytes', new=_raise):
                            with patch.object(pathlib.Path, 'read_text', new=_raise):
                                with patch.object(socket, 'create_connection', new=_raise):
                                    with patch.object(socket, 'socket', new=_raise):
                                        with patch.object(urllib.request, 'urlopen', new=_raise):
                                            with patch.object(subprocess, 'Popen', new=_raise):
                                                with patch.object(subprocess, 'run', new=_raise):
                                                    r = verify_selection_files(mb, files)
                                                    self.assertEqual(r.cython_version, CY)

    def test_mutation_during_verification_isolated(self):
        import pixs.pa_native.selection_file_consistency as sfc
        from pixs.pa_native.selection_evidence import parse_manifest as real_parse
        mb, files, man = _nominal()
        expected_manifest_sha = _h(mb)
        pp = [f['path'] for f in man['files'] if f['role'] == 'build_profile'][0]
        expected_profile_sha = _h(files[pp])
        expected_dists = sorted([(f['path'].split('/')[-1], f['sha256']) for f in man['files'] if f['role'] == 'distribution'])
        first_key = next(iter(files))
        def _wrapped(data):
            out = real_parse(data)
            files[first_key] = b'mutee'
            files['extra/mute.bin'] = b'x'
            return out
        with patch.object(sfc, 'parse_manifest', side_effect=_wrapped):
            r = verify_selection_files(mb, files)
        self.assertEqual(files[first_key], b'mutee')
        self.assertIn('extra/mute.bin', files)
        self.assertEqual(r.manifest_sha256, expected_manifest_sha)
        self.assertEqual(r.profile_sha256, expected_profile_sha)
        self.assertEqual(list(r.distributions), expected_dists)
        self.assertEqual(r.cython_version, CY)


if __name__ == '__main__':
    unittest.main()
