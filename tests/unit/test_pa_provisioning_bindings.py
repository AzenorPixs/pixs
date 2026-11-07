'''Tests de la comparaison pure des liaisons.

Jeux synthetiques uniquement, aucune admission prouvee.
'''
import unittest
import json
from unittest.mock import patch
from pixs.pa_native.provisioning_contracts import ProvisioningLimits
from pixs.pa_native.provisioning_contracts import ProvisioningDocument
from pixs.pa_native.provisioning_contracts import decode_provisioning_document
from pixs.pa_native.provisioning_contracts import encode_provisioning_document
from pixs.pa_native.provisioning_bindings import ProvisioningBindingsError
from pixs.pa_native.provisioning_bindings import assert_provisioning_bindings
from pixs.pa_native.provisioning_bindings import decode_and_check_bindings
UUID_A = '0193a1b2-c3d4-7e5f-8a90-1234567890ab'
UUID_B = '0193a1b2-c3d4-7e5f-8b91-1234567890ac'
BINDINGS_MESSAGE = 'Liaisons non concordantes.'
def make_limits():
    '''Fabrique un profil synthetique.'''
    return ProvisioningLimits(max_json_bytes=8192, max_ref_bytes=256, max_secret_refs=4)
def make_base():
    '''Fabrique un dictionnaire synthetique valide.'''
    return {'anchor_ref': 'anchor-synth-001', 'anchor_version': 'v-opaque-001', 'authority_ref': 'authority-synth-001', 'config_revision_ref': 'cfgrev-synth-001', 'document_ref': 'doc-synth-001', 'object_type': 'pa.provisioning.document/v1', 'pa_id': UUID_A, 'policy_ref': 'policy-synth-001', 'policy_version': 'v-opaque-pol-001', 'relation_ref': 'rel-synth-001', 'resource_perimeter_ref': 'perim-synth-001', 'resource_perimeter_version': 'v-opaque-perim-001', 'schema_version': '1.0.0', 'scope_id': None, 'scope_type': 'PLATFORM', 'secret_refs': [{'ref': 'sec-synth-001', 'version': 'v-opaque-sec-001'}], 'tenant_id': None}
def make_bytes(base):
    '''Reemission canonique pour les jeux.'''
    text = json.dumps(base, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)
    return text.encode('utf-8')
def make_doc(base=None):
    '''Fabrique un document valide synthetique.'''
    if base is None:
        base = make_base()
    return decode_provisioning_document(make_bytes(base), make_limits())
class NominalBindings(unittest.TestCase):
    '''Cas nominaux sans effet.'''
    def test_object_returns_none(self):
        result = assert_provisioning_bindings(make_doc(), make_doc(), make_limits())
        self.assertIsNone(result)
    def test_bytes_returns_document(self):
        base = make_base()
        raw = make_bytes(base)
        result = decode_and_check_bindings(raw, make_doc(base), make_limits())
        self.assertEqual(encode_provisioning_document(result, make_limits()), raw)
    def test_pure_no_flag(self):
        result = assert_provisioning_bindings(make_doc(), make_doc(), make_limits())
        self.assertIsNone(result)
        self.assertFalse(hasattr(result, 'trusted'))
        self.assertFalse(hasattr(result, 'qualified'))
class ScalarMismatch(unittest.TestCase):
    '''Chaque champ scalaire discordant.'''
    def test_each_scalar(self):
        fields = ['anchor_ref', 'anchor_version', 'authority_ref', 'config_revision_ref', 'document_ref', 'policy_ref', 'policy_version', 'relation_ref', 'resource_perimeter_ref', 'resource_perimeter_version']
        for field in fields:
            with self.subTest(field=field):
                other = make_base()
                other[field] = 'autre-synth-999'
                with self.assertRaises(ProvisioningBindingsError):
                    assert_provisioning_bindings(make_doc(), make_doc(other), make_limits())
    def test_pa_id(self):
        other = make_base()
        other['pa_id'] = UUID_B
        with self.assertRaises(ProvisioningBindingsError):
            assert_provisioning_bindings(make_doc(), make_doc(other), make_limits())
class ScopeMismatch(unittest.TestCase):
    '''Tous les cas de scope TENANT.'''
    def test_platform_vs_tenant(self):
        tenant_base = make_base()
        tenant_base['scope_type'] = 'TENANT'
        tenant_base['tenant_id'] = 'tenant-synth-001'
        with self.assertRaises(ProvisioningBindingsError):
            assert_provisioning_bindings(make_doc(), make_doc(tenant_base), make_limits())
    def test_tenant_id_diff(self):
        first = make_base()
        first['scope_type'] = 'TENANT'
        first['tenant_id'] = 'tenant-synth-001'
        second = make_base()
        second['scope_type'] = 'TENANT'
        second['tenant_id'] = 'tenant-autre-002'
        with self.assertRaises(ProvisioningBindingsError):
            assert_provisioning_bindings(make_doc(first), make_doc(second), make_limits())
    def test_scope_id_null_vs_text(self):
        first = make_base()
        first['scope_type'] = 'TENANT'
        first['tenant_id'] = 'tenant-synth-001'
        first['scope_id'] = None
        second = make_base()
        second['scope_type'] = 'TENANT'
        second['tenant_id'] = 'tenant-synth-001'
        second['scope_id'] = 'scope-synth-001'
        with self.assertRaises(ProvisioningBindingsError):
            assert_provisioning_bindings(make_doc(first), make_doc(second), make_limits())
class SecretMismatch(unittest.TestCase):
    '''References opaques discordantes.'''
    def test_ref_name(self):
        other = make_base()
        other['secret_refs'] = [{'ref': 'autre-sec', 'version': 'v-opaque-sec-001'}]
        with self.assertRaises(ProvisioningBindingsError):
            assert_provisioning_bindings(make_doc(), make_doc(other), make_limits())
    def test_ref_version(self):
        other = make_base()
        other['secret_refs'] = [{'ref': 'sec-synth-001', 'version': 'autre-version'}]
        with self.assertRaises(ProvisioningBindingsError):
            assert_provisioning_bindings(make_doc(), make_doc(other), make_limits())
    def test_order(self):
        first = make_base()
        first['secret_refs'] = [{'ref': 'a-sec', 'version': 'v1'}, {'ref': 'b-sec', 'version': 'v2'}]
        second = make_base()
        second['secret_refs'] = [{'ref': 'b-sec', 'version': 'v2'}, {'ref': 'a-sec', 'version': 'v1'}]
        with self.assertRaises(ProvisioningBindingsError):
            assert_provisioning_bindings(make_doc(first), make_doc(second), make_limits())
    def test_cardinality_two_valid(self):
        one = make_base()
        one['secret_refs'] = [{'ref': 'a-sec', 'version': 'v1'}]
        two = make_base()
        two['secret_refs'] = [{'ref': 'a-sec', 'version': 'v1'}, {'ref': 'b-sec', 'version': 'v2'}]
        with self.assertRaises(ProvisioningBindingsError):
            assert_provisioning_bindings(make_doc(one), make_doc(two), make_limits())
class ObjectGuards(unittest.TestCase):
    '''Objets mutes ou incomplets des deux cotes.'''
    def test_actual_mutated(self):
        target = make_doc()
        object.__setattr__(target, 'relation_ref', 'autre')
        with self.assertRaises(ProvisioningBindingsError):
            assert_provisioning_bindings(target, make_doc(), make_limits())
    def test_expected_mutated(self):
        target = make_doc()
        object.__setattr__(target, 'relation_ref', 'autre')
        with self.assertRaises(ProvisioningBindingsError):
            assert_provisioning_bindings(make_doc(), target, make_limits())
    def test_missing_attrs_both(self):
        for side in ['actual', 'expected']:
            with self.subTest(side=side):
                target = make_doc()
                object.__delattr__(target, 'anchor_ref')
                if side == 'actual':
                    with self.assertRaises(ProvisioningBindingsError):
                        assert_provisioning_bindings(target, make_doc(), make_limits())
                else:
                    with self.assertRaises(ProvisioningBindingsError):
                        assert_provisioning_bindings(make_doc(), target, make_limits())
        empty = object.__new__(ProvisioningDocument)
        with self.assertRaises(ProvisioningBindingsError):
            assert_provisioning_bindings(empty, make_doc(), make_limits())
        with self.assertRaises(ProvisioningBindingsError):
            assert_provisioning_bindings(make_doc(), empty, make_limits())
    def test_inexact_type(self):
        with self.assertRaises(ProvisioningBindingsError):
            assert_provisioning_bindings('faux', make_doc(), make_limits())
        with self.assertRaises(ProvisioningBindingsError):
            assert_provisioning_bindings(make_doc(), 'faux', make_limits())
    def test_uuid_mutated_both(self):
        for side in ['actual', 'expected']:
            for op in ['replace', 'delete']:
                with self.subTest(side=side, op=op):
                    valid_actual = make_doc()
                    valid_expected = make_doc()
                    target = valid_actual if side == 'actual' else valid_expected
                    victim = target.pa_id
                    if op == 'replace':
                        object.__setattr__(victim, 'int', 'hostile')
                    else:
                        object.__delattr__(victim, 'int')
                    with self.assertRaises(ProvisioningBindingsError):
                        assert_provisioning_bindings(valid_actual, valid_expected, make_limits())
class ProfileGuards(unittest.TestCase):
    '''Profils hostiles avant analyse.'''
    def test_hostile_profile_both_apis(self):
        base = make_base()
        raw = make_bytes(base)
        expected = make_doc()
        bad = make_limits()
        object.__setattr__(bad, 'max_json_bytes', 'huge')
        with self.assertRaises(ProvisioningBindingsError):
            assert_provisioning_bindings(make_doc(), expected, bad)
        with patch('pixs.pa_native.provisioning_contracts.json.loads') as mocked:
            with self.assertRaises(ProvisioningBindingsError):
                decode_and_check_bindings(raw, expected, bad)
            mocked.assert_not_called()
    def test_mutated_int_profile(self):
        class TrackingInt(int):
            pass
        bad = make_limits()
        object.__setattr__(bad, 'max_ref_bytes', TrackingInt(256))
        expected = make_doc()
        actual = make_doc()
        with self.assertRaises(ProvisioningBindingsError):
            assert_provisioning_bindings(actual, expected, bad)
        base = make_base()
        raw = make_bytes(base)
        with patch('pixs.pa_native.provisioning_contracts.json.loads') as mocked:
            with self.assertRaises(ProvisioningBindingsError):
                decode_and_check_bindings(raw, expected, bad)
            mocked.assert_not_called()
class BytesGuards(unittest.TestCase):
    '''Octets non canoniques et faux conteneurs.'''
    def test_non_canonical(self):
        base = make_base()
        raw = make_bytes(base)
        expected = make_doc()
        spaced = raw.replace(bytes([44]), bytes([44, 32]), 1)
        with self.assertRaises(ProvisioningBindingsError):
            decode_and_check_bindings(spaced, expected, make_limits())
        with_lf = raw + bytes([10])
        with self.assertRaises(ProvisioningBindingsError):
            decode_and_check_bindings(with_lf, expected, make_limits())
    def test_duplicated(self):
        base = make_base()
        raw = make_bytes(base)
        text = raw.decode('utf-8')
        quote = chr(34)
        first = quote + 'anchor_ref' + quote + ':' + quote + 'premier' + quote
        second = quote + 'anchor_ref' + quote + ':' + quote + 'second' + quote
        parts = []
        for key in base:
            if key == 'anchor_ref':
                continue
            parts.append(quote + key + quote + ':' + json.dumps(base[key], ensure_ascii=False))
        dup_text = '{' + first + ',' + second + ',' + ','.join(parts) + '}'
        dup_raw = dup_text.encode('utf-8')
        self.assertEqual(json.loads(dup_raw)['anchor_ref'], 'second')
        with self.assertRaises(ProvisioningBindingsError):
            decode_and_check_bindings(dup_raw, make_doc(), make_limits())
        self.assertNotEqual(text, dup_text)
    def test_bytes_subclass(self):
        class TrackingBytes(bytes):
            def __len__(self):
                raise AssertionError('len appele')
        base = make_base()
        raw = make_bytes(base)
        expected = make_doc()
        with self.assertRaises(ProvisioningBindingsError):
            decode_and_check_bindings(TrackingBytes(raw), expected, make_limits())
        with self.assertRaises(ProvisioningBindingsError):
            decode_and_check_bindings(bytearray(raw), expected, make_limits())
class DiagnosticGuards(unittest.TestCase):
    '''Diagnostics fixes et erreur inattendue.'''
    def test_form_refusal_fixed(self):
        base = make_base()
        del base['anchor_ref']
        raw = make_bytes(base)
        try:
            decode_and_check_bindings(raw, make_doc(), make_limits())
            self.fail('devrait refuser')
        except ProvisioningBindingsError as err:
            self.assertEqual(str(err), BINDINGS_MESSAGE)
            self.assertEqual(err.code, 'BINDINGS_MISMATCH')
            self.assertNotIn('anchor', str(err))
            self.assertIsNone(err.__cause__)
    def test_mismatch_fixed(self):
        other = make_base()
        other['relation_ref'] = 'autre'
        try:
            assert_provisioning_bindings(make_doc(), make_doc(other), make_limits())
            self.fail('devrait refuser')
        except ProvisioningBindingsError as err:
            self.assertEqual(str(err), BINDINGS_MESSAGE)
            self.assertEqual(err.args, (BINDINGS_MESSAGE,))
            self.assertIn('BINDINGS_MISMATCH', repr(err))
            self.assertIsNone(err.__cause__)
    def test_unexpected_propagates(self):
        base = make_base()
        raw = make_bytes(base)
        expected = make_doc()
        with patch('pixs.pa_native.provisioning_contracts.json.loads', side_effect=RuntimeError('sentinelle')):
            with self.assertRaises(RuntimeError):
                decode_and_check_bindings(raw, expected, make_limits())
class AdditionalConcordance(unittest.TestCase):
    '''Cas nominaux TENANT et echecs bytes.'''
    def test_tenant_nominal_both_apis(self):
        for scope_value in [None, 'scope-synth-001']:
            with self.subTest(scope_value=scope_value):
                base = make_base()
                base['scope_type'] = 'TENANT'
                base['tenant_id'] = 'tenant-synth-001'
                base['scope_id'] = scope_value
                raw = make_bytes(base)
                expected = make_doc(base)
                actual_result = assert_provisioning_bindings(make_doc(base), expected, make_limits())
                self.assertIsNone(actual_result)
                checked = decode_and_check_bindings(raw, expected, make_limits())
                self.assertEqual(encode_provisioning_document(checked, make_limits()), raw)
                self.assertFalse(hasattr(checked, 'trusted'))
                self.assertFalse(hasattr(checked, 'qualified'))
    def test_authority_mismatch_bytes_path(self):
        base = make_base()
        raw = make_bytes(base)
        other = make_base()
        other['authority_ref'] = 'authority-autre-999'
        expected = make_doc(other)
        with self.assertRaises(ProvisioningBindingsError):
            decode_and_check_bindings(raw, expected, make_limits())
    def test_encode_unexpected_propagates(self):
        actual = make_doc()
        expected = make_doc()
        with patch('pixs.pa_native.provisioning_bindings.encode_provisioning_document', side_effect=RuntimeError('sentinelle')):
            with self.assertRaises(RuntimeError):
                assert_provisioning_bindings(actual, expected, make_limits())
if __name__ == '__main__':
    unittest.main()
