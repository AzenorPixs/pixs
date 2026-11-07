"""Recette S2b2, fixtures synthetiques, verificateur reel seul."""
from __future__ import annotations

import builtins
import copy
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
from pixs.pa_native.selection_snapshot import SnapshotSelection
from pixs.pa_native.selection_snapshot import SnapshotSelectionError
from pixs.pa_native.selection_snapshot import analyze_snapshot

CODE_E = 'PA01_CAMPAIGN_EVIDENCE_INVALID'
CODE_D = 'PA01_CAMPAIGN_METADATA_INVALID'
CY = '3.3.0'
CAMP = 'pa01-2026-10-26-c1'
WHEN = '2026-10-26T21:11:03Z'
SRC = 'https://pypi.org/pypi/Cython/json'


def _h(b):
    return hashlib.sha256(b).hexdigest()


def _env(camp, cy, snap, snapsha, dists):
    s = (
        'schema_version = "1.0.0"\n[campaign]\nid = "' + camp + '"\ncomponent = "pa01"\n'
        '[toolchain]\ncython = "' + cy + '"\n[selection]\nverified_at = "' + WHEN + '"\n'
        'source_url = "' + SRC + '"\nsnapshot = "' + snap + '"\nsnapshot_sha256 = "' + snapsha + '"\n'
    )
    for fn, url, sha in dists:
        s += '[[distributions]]\nfilename = "' + fn + '"\nurl = "' + url + '"\nsha256 = "' + sha + '"\n'
    return s.encode('utf-8')


def _f(fn, url, sha, yanked=False):
    return {'filename': fn, 'url': url, 'digests': {'sha256': sha}, 'yanked': yanked}


def _snap(name, trap, releases, top_extra=None, info_extra=None):
    info = {'name': name, 'version': trap}
    if info_extra is not None:
        info.update(info_extra)
    root = {'info': info, 'releases': releases}
    if top_extra is not None:
        root.update(top_extra)
    return json.dumps(root, separators=(',', ':')).encode('utf-8')


def _nominal():
    sn = 'evidence/snap.json'
    b1 = b'dist-one'
    b2 = b'dist-two'
    f1 = ('cython-3.3.0-py3-none-any.whl', 'https://files.pythonhosted.org/x/a.whl', _h(b1))
    f2 = ('cython-3.3.0.tar.gz', 'https://files.pythonhosted.org/x/b.tar.gz', _h(b2))
    rel = {
        '3.2.0': [_f('cython-3.2.0.tar.gz', 'https://files.pythonhosted.org/x/old.tar.gz', 'a' * 64, False)],
        '3.3.0': [_f(f1[0], f1[1], f1[2], False), _f(f2[0], f2[1], f2[2], False)],
    }
    snapb = _snap('Cython', '3.2.0', rel)
    envb = _env(CAMP, CY, sn, _h(snapb), [f1, f2])
    return snapb, envb


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


def _raise(*a, **k):
    raise AssertionError('io interdite')


class SnapshotTest(unittest.TestCase):
    def test_nominal_two_distributions(self):
        snapb, envb = _nominal()
        r = analyze_snapshot(snapb, envb)
        self.assertIs(type(r), SnapshotSelection)
        self.assertEqual(r.selected_key, '3.3.0')
        self.assertEqual(r.selected_normalized, '3.3.0')
        self.assertEqual(r.snapshot_sha256, _h(snapb))
        self.assertEqual(len(r.files), 2)

    def test_nominal_subset_single_wheel(self):
        snapb, env0 = _nominal()
        sn = 'evidence/snap.json'
        b1 = b'dist-one'
        f1 = ('cython-3.3.0-py3-none-any.whl', 'https://files.pythonhosted.org/x/a.whl', _h(b1))
        envb = _env(CAMP, CY, sn, _h(snapb), [f1])
        r = analyze_snapshot(snapb, envb)
        self.assertEqual(r.selected_key, '3.3.0')
        self.assertEqual(len(r.files), 2)

    def test_lexical_vs_pep440(self):
        sn = 'evidence/snap.json'
        b9 = b'nine'
        b10 = b'ten'
        f9 = ('cython-3.9.0.tar.gz', 'https://files.pythonhosted.org/x/9.tar.gz', _h(b9))
        f10 = ('cython-3.10.0.tar.gz', 'https://files.pythonhosted.org/x/10.tar.gz', _h(b10))
        rel = {
            '3.9.0': [_f(f9[0], f9[1], f9[2], False)],
            '3.10.0': [_f(f10[0], f10[1], f10[2], False)],
        }
        snapb = _snap('Cython', '3.9.0', rel)
        envb = _env(CAMP, '3.10.0', sn, _h(snapb), [f10])
        r = analyze_snapshot(snapb, envb)
        self.assertEqual(r.selected_key, '3.10.0')

    def test_epoch_orders(self):
        sn = 'evidence/snap.json'
        b1 = b'e1'
        b2 = b'e2'
        f1 = ('cython-3.3.0.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1))
        f2 = ('cython-e.tar.gz', 'https://files.pythonhosted.org/x/e.tar.gz', _h(b2))
        rel = {
            '3.3.0': [_f(f1[0], f1[1], f1[2], False)],
            '1!3.0.0': [_f(f2[0], f2[1], f2[2], False)],
        }
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, '1!3.0.0', sn, _h(snapb), [f2])
        r = analyze_snapshot(snapb, envb)
        self.assertEqual(r.selected_key, '1!3.0.0')

    def test_post_greater_than_final(self):
        sn = 'evidence/snap.json'
        b1 = b'p1'
        b2 = b'p2'
        f1 = ('cython-3.3.0.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1))
        f2 = ('cython-3.3.0.post1.tar.gz', 'https://files.pythonhosted.org/x/b.tar.gz', _h(b2))
        rel = {
            '3.3.0': [_f(f1[0], f1[1], f1[2], False)],
            '3.3.0.post1': [_f(f2[0], f2[1], f2[2], False)],
        }
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, '3.3.0.post1', sn, _h(snapb), [f2])
        r = analyze_snapshot(snapb, envb)
        self.assertEqual(r.selected_key, '3.3.0.post1')
        self.assertEqual(r.selected_normalized, '3.3.0.post1')

    def test_rev_variant(self):
        sn = 'evidence/snap.json'
        b1 = b'r1'
        f1 = ('cython-3.3.0-rev1.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1))
        rel = {'3.3.0-rev1': [_f(f1[0], f1[1], f1[2], False)]}
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, '3.3.0.post1', sn, _h(snapb), [f1])
        r = analyze_snapshot(snapb, envb)
        self.assertEqual(r.selected_key, '3.3.0-rev1')
        self.assertEqual(r.selected_normalized, '3.3.0.post1')

    def test_r_variant(self):
        sn = 'evidence/snap.json'
        b1 = b'r1'
        f1 = ('cython-3.3.0-r1.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1))
        rel = {'3.3.0-r1': [_f(f1[0], f1[1], f1[2], False)]}
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, '3.3.0.post1', sn, _h(snapb), [f1])
        r = analyze_snapshot(snapb, envb)
        self.assertEqual(r.selected_key, '3.3.0-r1')
        self.assertEqual(r.selected_normalized, '3.3.0.post1')

    def test_implicit_post_dash(self):
        sn = 'evidence/snap.json'
        b1 = b'i1'
        f1 = ('cython-3.3.0-1.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1))
        rel = {'3.3.0-1': [_f(f1[0], f1[1], f1[2], False)]}
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, '3.3.0.post1', sn, _h(snapb), [f1])
        r = analyze_snapshot(snapb, envb)
        self.assertEqual(r.selected_key, '3.3.0-1')
        self.assertEqual(r.selected_normalized, '3.3.0.post1')

    def test_implicit_post_zero(self):
        for key in ['3.3.0-0', '3.3.0.post', '3.3.0rev', '3.3.0r']:
            sn = 'evidence/snap.json'
            b1 = b'z0'
            f1 = ('cython-sep.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1))
            rel = {key: [_f(f1[0], f1[1], f1[2], False)]}
            snapb = _snap('Cython', '3.3.0', rel)
            envb = _env(CAMP, '3.3.0.post0', sn, _h(snapb), [f1])
            r = analyze_snapshot(snapb, envb)
            self.assertEqual(r.selected_key, key)
            self.assertEqual(r.selected_normalized, '3.3.0.post0')

    def test_separator_variants(self):
        for key in ['3.3.0_post1', '3.3.0post1', '3.3.0-post1']:
            sn = 'evidence/snap.json'
            b1 = b'sep1'
            f1 = ('cython-sep.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1))
            rel = {key: [_f(f1[0], f1[1], f1[2], False)]}
            snapb = _snap('Cython', '3.3.0', rel)
            envb = _env(CAMP, '3.3.0.post1', sn, _h(snapb), [f1])
            r = analyze_snapshot(snapb, envb)
            self.assertEqual(r.selected_key, key)
            self.assertEqual(r.selected_normalized, '3.3.0.post1')

    def test_v_prefix_accepted(self):
        sn = 'evidence/snap.json'
        b1 = b'v1'
        f1 = ('cython-v.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1))
        rel = {'v3.3.0': [_f(f1[0], f1[1], f1[2], False)]}
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [f1])
        r = analyze_snapshot(snapb, envb)
        self.assertEqual(r.selected_key, 'v3.3.0')
        self.assertEqual(r.selected_normalized, '3.3.0')

    def test_leading_zeros_normalized(self):
        sn = 'evidence/snap.json'
        b1 = b'lz1'
        f1 = ('cython-lz.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1))
        rel = {'03.03.0': [_f(f1[0], f1[1], f1[2], False)]}
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [f1])
        r = analyze_snapshot(snapb, envb)
        self.assertEqual(r.selected_key, '03.03.0')
        self.assertEqual(r.selected_normalized, '3.3.0')
        b2 = b'lz2'
        f2 = ('cython-lz2.tar.gz', 'https://files.pythonhosted.org/x/b.tar.gz', _h(b2))
        rel2 = {'01!3.3.0': [_f(f2[0], f2[1], f2[2], False)]}
        snapb2 = _snap('Cython', '3.3.0', rel2)
        envb2 = _env(CAMP, '1!3.3.0', sn, _h(snapb2), [f2])
        r2 = analyze_snapshot(snapb2, envb2)
        self.assertEqual(r2.selected_key, '01!3.3.0')
        self.assertEqual(r2.selected_normalized, '1!3.3.0')

    def test_trailing_zeros_ambiguity_refused(self):
        sn = 'evidence/snap.json'
        b1 = b'z1'
        b2 = b'z2'
        rel = {
            '3.3': [_f('a.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1), False)],
            '3.3.0': [_f('b.tar.gz', 'https://files.pythonhosted.org/x/b.tar.gz', _h(b2), False)],
        }
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [('b.tar.gz', 'https://files.pythonhosted.org/x/b.tar.gz', _h(b2))])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_v_alias_ambiguity_refused(self):
        sn = 'evidence/snap.json'
        b1 = b'v1'
        b2 = b'v2'
        rel = {
            'v3.3.0': [_f('a.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1), False)],
            '3.3.0': [_f('b.tar.gz', 'https://files.pythonhosted.org/x/b.tar.gz', _h(b2), False)],
        }
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [('b.tar.gz', 'https://files.pythonhosted.org/x/b.tar.gz', _h(b2))])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_uppercase_labels(self):
        sn = 'evidence/snap.json'
        b1 = b'c1'
        for key in ['3.3.0.POST', '3.3.0.REV', '3.3.0.R']:
            f1 = ('cython-up.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1))
            rel = {key: [_f(f1[0], f1[1], f1[2], False)]}
            snapb = _snap('Cython', '3.3.0', rel)
            envb = _env(CAMP, '3.3.0.post0', sn, _h(snapb), [f1])
            r = analyze_snapshot(snapb, envb)
            self.assertEqual(r.selected_key, key)
            self.assertEqual(r.selected_normalized, '3.3.0.post0')
        b2 = b'c2'
        f2 = ('cython-fin.tar.gz', 'https://files.pythonhosted.org/x/f.tar.gz', _h(b2))
        rel2 = {
            '3.4RC1': [_f('rc.tar.gz', 'https://files.pythonhosted.org/x/rc.tar.gz', _h(b1), False)],
            '3.4.DEV1': [_f('dv.tar.gz', 'https://files.pythonhosted.org/x/dv.tar.gz', _h(b1), False)],
            '3.3.0': [_f(f2[0], f2[1], f2[2], False)],
        }
        snapb2 = _snap('Cython', '3.4RC1', rel2)
        envb2 = _env(CAMP, CY, sn, _h(snapb2), [f2])
        r2 = analyze_snapshot(snapb2, envb2)
        self.assertEqual(r2.selected_key, '3.3.0')

    def test_pre_excluded(self):
        sn = 'evidence/snap.json'
        b1 = b'pre1'
        b2 = b'fin1'
        fpre = ('cython-3.4a1.tar.gz', 'https://files.pythonhosted.org/x/pre.tar.gz', _h(b1))
        ffin = ('cython-3.3.0.tar.gz', 'https://files.pythonhosted.org/x/fin.tar.gz', _h(b2))
        rel = {
            '3.4a1': [_f(fpre[0], fpre[1], fpre[2], False)],
            '3.3.0': [_f(ffin[0], ffin[1], ffin[2], False)],
        }
        snapb = _snap('Cython', '3.4a1', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [ffin])
        r = analyze_snapshot(snapb, envb)
        self.assertEqual(r.selected_key, '3.3.0')

    def test_dev_excluded(self):
        sn = 'evidence/snap.json'
        b1 = b'dev1'
        b2 = b'fin1'
        rel = {
            '3.4.dev1': [_f('d.tar.gz', 'https://files.pythonhosted.org/x/d.tar.gz', _h(b1), False)],
            '3.3.0': [_f('f.tar.gz', 'https://files.pythonhosted.org/x/f.tar.gz', _h(b2), False)],
        }
        snapb = _snap('Cython', '3.4.dev1', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [('f.tar.gz', 'https://files.pythonhosted.org/x/f.tar.gz', _h(b2))])
        r = analyze_snapshot(snapb, envb)
        self.assertEqual(r.selected_key, '3.3.0')

    def test_local_excluded(self):
        sn = 'evidence/snap.json'
        b1 = b'loc1'
        b2 = b'fin1'
        rel = {
            '3.4+local': [_f('l.tar.gz', 'https://files.pythonhosted.org/x/l.tar.gz', _h(b1), False)],
            '3.3.0': [_f('f.tar.gz', 'https://files.pythonhosted.org/x/f.tar.gz', _h(b2), False)],
        }
        snapb = _snap('Cython', '3.4+local', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [('f.tar.gz', 'https://files.pythonhosted.org/x/f.tar.gz', _h(b2))])
        r = analyze_snapshot(snapb, envb)
        self.assertEqual(r.selected_key, '3.3.0')

    def test_uninterpretable_blocks(self):
        sn = 'evidence/snap.json'
        b1 = b'u1'
        b2 = b'u2'
        rel = {
            '3.3.0': [_f('f.tar.gz', 'https://files.pythonhosted.org/x/f.tar.gz', _h(b2), False)],
            'garbage!!': [_f('g.tar.gz', 'https://files.pythonhosted.org/x/g.tar.gz', _h(b1), False)],
        }
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [('f.tar.gz', 'https://files.pythonhosted.org/x/f.tar.gz', _h(b2))])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_arabic_indic_release_refused(self):
        sn = 'evidence/snap.json'
        b1 = b'a1'
        rel = {
            '٣.3.0': [_f('f.tar.gz', 'https://files.pythonhosted.org/x/f.tar.gz', _h(b1), False)],
            '3.3.0': [_f('g.tar.gz', 'https://files.pythonhosted.org/x/g.tar.gz', _h(b1), False)],
        }
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [('g.tar.gz', 'https://files.pythonhosted.org/x/g.tar.gz', _h(b1))])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_arabic_indic_epoch_refused(self):
        sn = 'evidence/snap.json'
        b1 = b'a1'
        rel = {
            '٣!3.0.0': [_f('f.tar.gz', 'https://files.pythonhosted.org/x/f.tar.gz', _h(b1), False)],
            '3.3.0': [_f('g.tar.gz', 'https://files.pythonhosted.org/x/g.tar.gz', _h(b1), False)],
        }
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [('g.tar.gz', 'https://files.pythonhosted.org/x/g.tar.gz', _h(b1))])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_huge_number_refused(self):
        sn = 'evidence/snap.json'
        b1 = b'h1'
        big = '9' * 5000
        rel = {
            big: [_f('f.tar.gz', 'https://files.pythonhosted.org/x/f.tar.gz', _h(b1), False)],
            '3.3.0': [_f('g.tar.gz', 'https://files.pythonhosted.org/x/g.tar.gz', _h(b1), False)],
        }
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [('g.tar.gz', 'https://files.pythonhosted.org/x/g.tar.gz', _h(b1))])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_edge_spaces_accepted(self):
        for key in ['  3.3.0  ', '\t3.3.0\t', '\n3.3.0\n', '\r3.3.0\r', '\f3.3.0\f', '\v3.3.0\v', ' \t\n\r\f\v3.3.0\v\f\r\n\t ']:
            sn = 'evidence/snap.json'
            b1 = b'e1'
            f1 = ('cython-e.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1))
            rel = {key: [_f(f1[0], f1[1], f1[2], False)]}
            snapb = _snap('Cython', '3.3.0', rel)
            envb = _env(CAMP, CY, sn, _h(snapb), [f1])
            r = analyze_snapshot(snapb, envb)
            self.assertEqual(r.selected_key, key)

    def test_internal_newline_refused(self):
        sn = 'evidence/snap.json'
        b1 = b'n1'
        rel = {'3.3.\n0': [_f('f.tar.gz', 'https://files.pythonhosted.org/x/f.tar.gz', _h(b1), False)]}
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [('f.tar.gz', 'https://files.pythonhosted.org/x/f.tar.gz', _h(b1))])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_yanked_max_skipped(self):
        sn = 'evidence/snap.json'
        b1 = b'y1'
        b2 = b'y2'
        rel = {
            '3.4.0': [_f('n.tar.gz', 'https://files.pythonhosted.org/x/n.tar.gz', _h(b1), True)],
            '3.3.0': [_f('o.tar.gz', 'https://files.pythonhosted.org/x/o.tar.gz', _h(b2), False)],
        }
        snapb = _snap('Cython', '3.4.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [('o.tar.gz', 'https://files.pythonhosted.org/x/o.tar.gz', _h(b2))])
        r = analyze_snapshot(snapb, envb)
        self.assertEqual(r.selected_key, '3.3.0')

    def test_yanked_none_eligible_refused(self):
        sn = 'evidence/snap.json'
        b1 = b'y1'
        rel = {'3.3.0': [_f('n.tar.gz', 'https://files.pythonhosted.org/x/n.tar.gz', _h(b1), True)]}
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [('n.tar.gz', 'https://files.pythonhosted.org/x/n.tar.gz', _h(b1))])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_yanked_partial_subset(self):
        sn = 'evidence/snap.json'
        b1 = b'k1'
        b2 = b'k2'
        f1 = ('keep.tar.gz', 'https://files.pythonhosted.org/x/k.tar.gz', _h(b1))
        rel = {
            '3.3.0': [_f(f1[0], f1[1], f1[2], False), _f('old.tar.gz', 'https://files.pythonhosted.org/x/o.tar.gz', _h(b2), True)],
        }
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [f1])
        r = analyze_snapshot(snapb, envb)
        self.assertEqual(len(r.files), 1)

    def test_yanked_bad_type_refused(self):
        sn = 'evidence/snap.json'
        b1 = b't1'
        rel = {'3.3.0': [_f('f.tar.gz', 'https://files.pythonhosted.org/x/f.tar.gz', _h(b1), 'yes')]}
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [('f.tar.gz', 'https://files.pythonhosted.org/x/f.tar.gz', _h(b1))])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_higher_empty_lower_eligible(self):
        sn = 'evidence/snap.json'
        b1 = b'q1'
        rel = {
            '3.4.0': [],
            '3.3.0': [_f('o.tar.gz', 'https://files.pythonhosted.org/x/o.tar.gz', _h(b1), False)],
        }
        snapb = _snap('Cython', '3.4.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [('o.tar.gz', 'https://files.pythonhosted.org/x/o.tar.gz', _h(b1))])
        r = analyze_snapshot(snapb, envb)
        self.assertEqual(r.selected_key, '3.3.0')

    def test_all_empty_or_withdrawn_refused(self):
        sn = 'evidence/snap.json'
        b1 = b'q1'
        rel = {
            '3.4.0': [],
            '3.3.0': [_f('o.tar.gz', 'https://files.pythonhosted.org/x/o.tar.gz', _h(b1), True)],
        }
        snapb = _snap('Cython', '3.4.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [('o.tar.gz', 'https://files.pythonhosted.org/x/o.tar.gz', _h(b1))])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_max_without_declared_no_downgrade(self):
        sn = 'evidence/snap.json'
        b34 = b'm34'
        b33 = b'm33'
        f34 = ('cython-3.4.0.tar.gz', 'https://files.pythonhosted.org/x/34.tar.gz', _h(b34))
        f33 = ('cython-3.3.0.tar.gz', 'https://files.pythonhosted.org/x/33.tar.gz', _h(b33))
        rel = {
            '3.3.0': [_f(f33[0], f33[1], f33[2], False)],
            '3.4.0': [_f(f34[0], f34[1], f34[2], False)],
        }
        snapb = _snap('Cython', '3.4.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [f33])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_info_version_trap_ignored(self):
        snapb, envb = _nominal()
        root = json.loads(snapb.decode('utf-8'))
        root['info']['version'] = '0.0.1'
        snapb = json.dumps(root, separators=(',', ':')).encode('utf-8')
        sn = 'evidence/snap.json'
        b1 = b'dist-one'
        b2 = b'dist-two'
        f1 = ('cython-3.3.0-py3-none-any.whl', 'https://files.pythonhosted.org/x/a.whl', _h(b1))
        f2 = ('cython-3.3.0.tar.gz', 'https://files.pythonhosted.org/x/b.tar.gz', _h(b2))
        envb = _env(CAMP, CY, sn, _h(snapb), [f1, f2])
        r = analyze_snapshot(snapb, envb)
        self.assertEqual(r.selected_key, '3.3.0')

    def test_json_duplicate_top_refused(self):
        raw = b'{"info": {"name": "Cython", "version": "3.3.0"}, "info": {}, "releases": {}}'
        sn = 'evidence/snap.json'
        envb = _env(CAMP, CY, sn, _h(raw), [('a', 'https://files.pythonhosted.org/x/a', 'a' * 64)])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(raw, envb)

    def test_json_duplicate_nested_refused(self):
        raw = b'{"info": {"name": "Cython", "version": "x"}, "releases": {"3.3.0": [{"filename": "a", "filename": "b", "url": "https://files.pythonhosted.org/x/a", "digests": {"sha256": "' + b'a' * 64 + b'"}, "yanked": false}]}}'
        sn = 'evidence/snap.json'
        envb = _env(CAMP, CY, sn, _h(raw), [('a', 'https://files.pythonhosted.org/x/a', 'a' * 64)])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(raw, envb)

    def test_json_constant_rejected(self):
        raw = b'{"info": {"name": "Cython", "version": NaN}, "releases": {}}'
        sn = 'evidence/snap.json'
        envb = _env(CAMP, CY, sn, _h(raw), [('a', 'https://files.pythonhosted.org/x/a', 'a' * 64)])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(raw, envb)

    def test_exact_types(self):
        snapb, envb = _nominal()
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb.decode('utf-8'), envb)
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb.decode('utf-8'))

    def test_malformed_info(self):
        root = {'releases': {'3.3.0': []}}
        bad = json.dumps(root, separators=(',', ':')).encode('utf-8')
        sn = 'evidence/snap.json'
        envb = _env(CAMP, CY, sn, _h(bad), [('a', 'https://files.pythonhosted.org/x/a', 'a' * 64)])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(bad, envb)

    def test_extra_top_allowed(self):
        snapb, envb = _nominal()
        root = json.loads(snapb.decode('utf-8'))
        root['extra_top'] = {'note': 'legitime'}
        root['info']['extra'] = 'ok'
        snapb = json.dumps(root, separators=(',', ':')).encode('utf-8')
        sn = 'evidence/snap.json'
        b1 = b'dist-one'
        b2 = b'dist-two'
        f1 = ('cython-3.3.0-py3-none-any.whl', 'https://files.pythonhosted.org/x/a.whl', _h(b1))
        f2 = ('cython-3.3.0.tar.gz', 'https://files.pythonhosted.org/x/b.tar.gz', _h(b2))
        envb = _env(CAMP, CY, sn, _h(snapb), [f1, f2])
        r = analyze_snapshot(snapb, envb)
        self.assertEqual(r.selected_key, '3.3.0')

    def test_name_mismatch(self):
        snapb, envb = _nominal()
        root = json.loads(snapb.decode('utf-8'))
        root['info']['name'] = 'Numpy'
        bad = json.dumps(root, separators=(',', ':')).encode('utf-8')
        sn = 'evidence/snap.json'
        envb = _env(CAMP, CY, sn, _h(bad), [('a', 'https://files.pythonhosted.org/x/a', 'a' * 64)])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(bad, envb)

    def test_url_mismatch(self):
        snapb, env0 = _nominal()
        sn = 'evidence/snap.json'
        b1 = b'dist-one'
        f1 = ('cython-3.3.0-py3-none-any.whl', 'https://files.pythonhosted.org/x/WRONG.whl', _h(b1))
        envb = _env(CAMP, CY, sn, _h(snapb), [f1])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_sha_mismatch(self):
        snapb, env0 = _nominal()
        sn = 'evidence/snap.json'
        b1 = b'dist-one'
        f1 = ('cython-3.3.0-py3-none-any.whl', 'https://files.pythonhosted.org/x/a.whl', 'b' * 64)
        envb = _env(CAMP, CY, sn, _h(snapb), [f1])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_filename_mismatch(self):
        snapb, env0 = _nominal()
        sn = 'evidence/snap.json'
        b1 = b'dist-one'
        f1 = ('WRONG.tar.gz', 'https://files.pythonhosted.org/x/a.whl', _h(b1))
        envb = _env(CAMP, CY, sn, _h(snapb), [f1])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_snapshot_sha_binding_mismatch(self):
        snapb, envb = _nominal()
        sn = 'evidence/snap.json'
        b1 = b'dist-one'
        b2 = b'dist-two'
        f1 = ('cython-3.3.0-py3-none-any.whl', 'https://files.pythonhosted.org/x/a.whl', _h(b1))
        f2 = ('cython-3.3.0.tar.gz', 'https://files.pythonhosted.org/x/b.tar.gz', _h(b2))
        envb = _env(CAMP, CY, sn, 'a' * 64, [f1, f2])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_envelope_invalid_propagates(self):
        snapb, envb = _nominal()
        bad_env = b'schema_version = "9.9.9"\n'
        with self.assertRaises(ProfileError) as c:
            analyze_snapshot(snapb, bad_env)
        self.assertIn(CODE_D, str(c.exception))

    def test_envelope_utf8_invalid(self):
        marker = 'marqueur-fuite-zzz-789'
        snapb, envb = _nominal()
        bad_env = marker.encode('utf-8') + b'\xff'
        try:
            analyze_snapshot(snapb, bad_env)
        except ProfileError as e:
            self.assertIn(CODE_D, str(e))
            s = str(e) + traceback.format_exc()
            self.assertNotIn(marker, s)
        else:
            self.fail('attendu echec enveloppe')

    def test_envelope_crlf(self):
        marker = 'marqueur-fuite-zzz-790'
        snapb, envb = _nominal()
        good = envb.decode('utf-8')
        bad_env = ('# ' + marker + '\n' + good).replace('\n', '\r\n').encode('utf-8')
        try:
            analyze_snapshot(snapb, bad_env)
        except ProfileError as e:
            self.assertIn(CODE_D, str(e))
            s = str(e) + traceback.format_exc()
            self.assertNotIn(marker, s)
        else:
            self.fail('attendu echec enveloppe')

    def test_selected_differs_lock(self):
        sn = 'evidence/snap.json'
        b1 = b's1'
        f1 = ('cython-3.4.0.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1))
        rel = {'3.4.0': [_f(f1[0], f1[1], f1[2], False)]}
        snapb = _snap('Cython', '3.4.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [f1])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_filename_ambiguity_diff_tuples(self):
        sn = 'evidence/snap.json'
        b1 = b'g1'
        b2 = b'g2'
        rel = {'3.3.0': [
            _f('dup.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1), False),
            _f('dup.tar.gz', 'https://files.pythonhosted.org/x/b.tar.gz', _h(b2), False),
        ]}
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [('dup.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1))])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_filename_ambiguity_yanked_conflict(self):
        sn = 'evidence/snap.json'
        b1 = b'h1'
        rel = {'3.3.0': [
            _f('dup.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1), False),
            _f('dup.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1), True),
        ]}
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [('dup.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1))])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_filename_exact_duplicate_refused(self):
        sn = 'evidence/snap.json'
        b1 = b'k1'
        item = _f('dup.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1), False)
        rel = {'3.3.0': [item, copy.deepcopy(item)]}
        snapb = _snap('Cython', '3.3.0', rel)
        envb = _env(CAMP, CY, sn, _h(snapb), [('dup.tar.gz', 'https://files.pythonhosted.org/x/a.tar.gz', _h(b1))])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(snapb, envb)

    def test_malformed_file_metadata(self):
        sn = 'evidence/snap.json'
        b1 = b'm1'
        variants = [
            {'3.3.0': {'not': 'a-list'}},
            {'3.3.0': ['not-a-dict']},
            {'3.3.0': [{'filename': 'f.tar.gz', 'url': 'https://files.pythonhosted.org/x/f.tar.gz', 'digests': 'nope', 'yanked': False}]},
            {'3.3.0': [{'filename': 'f.tar.gz', 'url': 'https://files.pythonhosted.org/x/f.tar.gz', 'digests': {}, 'yanked': False}]},
            {'3.3.0': [{'filename': 'f.tar.gz', 'url': 'https://files.pythonhosted.org/x/f.tar.gz', 'digests': {'sha256': 'ZZZ'}, 'yanked': False}]},
            {'3.3.0': [{'filename': 'f.tar.gz', 'url': 'https://files.pythonhosted.org/x/f.tar.gz', 'digests': {'sha256': _h(b1)}}]},
            {'3.3.0': [_f('f.tar.gz', 'https://files.pythonhosted.org/x/f.tar.gz', _h(b1), None)]},
            {'3.3.0': [_f('f.tar.gz', 'https://files.pythonhosted.org/x/f.tar.gz', _h(b1), 1)]},
        ]
        for rel in variants:
            snapb = _snap('Cython', '3.3.0', rel)
            envb = _env(CAMP, CY, sn, _h(snapb), [('f.tar.gz', 'https://files.pythonhosted.org/x/f.tar.gz', _h(b1))])
            with self.assertRaises(SnapshotSelectionError):
                analyze_snapshot(snapb, envb)

    def test_diagnostic_no_leak(self):
        marker = 'marqueur-fuite-zzz-456'
        bad_snap = (marker + '{invalide').encode('utf-8')
        sn = 'evidence/snap.json'
        envb2 = _env(CAMP, CY, sn, _h(bad_snap), [('a', 'https://files.pythonhosted.org/x/a', 'a' * 64)])
        try:
            analyze_snapshot(bad_snap, envb2)
        except SnapshotSelectionError as e:
            s = str(e) + traceback.format_exc()
            self.assertNotIn(marker, s)
        else:
            self.fail('attendu echec snapshot')
        snapb, envb = _nominal()
        bad_env = (marker + '[[[invalide').encode('utf-8')
        try:
            analyze_snapshot(snapb, bad_env)
        except ProfileError as e:
            s = str(e) + traceback.format_exc()
            self.assertNotIn(marker, s)
        else:
            self.fail('attendu echec enveloppe')

    def test_frozen_result_and_file(self):
        import dataclasses
        snapb, envb = _nominal()
        r = analyze_snapshot(snapb, envb)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            r.selected_key = 'x'
        with self.assertRaises(dataclasses.FrozenInstanceError):
            r.files[0].filename = 'x'
        self.assertEqual(r.snapshot_sha256, _h(snapb))
        self.assertEqual(r.envelope_sha256, _h(envb))
        self.assertFalse(hasattr(r, 'usable'))
        self.assertFalse(hasattr(r, 'verified'))

    def test_no_io_env_guards(self):
        snapb, envb = _nominal()
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
                                                    r = analyze_snapshot(snapb, envb)
                                                    self.assertEqual(r.selected_key, '3.3.0')

    def test_releases_absent_refused(self):
        root = {'info': {'name': 'Cython', 'version': '3.3.0'}}
        bad = json.dumps(root, separators=(',', ':')).encode('utf-8')
        sn = 'evidence/snap.json'
        envb = _env(CAMP, CY, sn, _h(bad), [('a', 'https://files.pythonhosted.org/x/a', 'a' * 64)])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(bad, envb)

    def test_releases_empty_refused(self):
        bad = _snap('Cython', '3.3.0', {})
        sn = 'evidence/snap.json'
        envb = _env(CAMP, CY, sn, _h(bad), [('a', 'https://files.pythonhosted.org/x/a', 'a' * 64)])
        with self.assertRaises(SnapshotSelectionError):
            analyze_snapshot(bad, envb)


if __name__ == '__main__':
    unittest.main()
