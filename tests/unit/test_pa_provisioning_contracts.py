'''Tests du codec pur, jeux synthetiques uniquement.

Couvre nominaux, gardes avant lecture, structure, limites,
canonicite, types hostiles et construction directe.
'''
import unittest
import json
import uuid
import dataclasses
from unittest.mock import patch
from pixs.pa_native.provisioning_contracts import ProvisioningLimits
from pixs.pa_native.provisioning_contracts import SecretRef
from pixs.pa_native.provisioning_contracts import ProvisioningDocument
from pixs.pa_native.provisioning_contracts import ProvisioningContractError
from pixs.pa_native.provisioning_contracts import decode_provisioning_document
from pixs.pa_native.provisioning_contracts import encode_provisioning_document
JSON_LIMIT = 8192
REF_LIMIT = 256
COUNT_LIMIT = 4
UUID_A = '0193a1b2-c3d4-7e5f-8a90-1234567890ab'
UUID_B = '0193a1b2-c3d4-7e5f-8b91-1234567890ac'
FIXED_MESSAGE = 'Contrat provisionnement invalide.'
def make_limits(json_size=8192, ref_size=256, count_size=4):
    '''Fabrique un profil synthetique.'''
    return ProvisioningLimits(max_json_bytes=json_size, max_ref_bytes=ref_size, max_secret_refs=count_size)
def make_base_dict():
    '''Fabrique un dictionnaire valide synthetique.'''
    return {'anchor_ref': 'anchor-synth-001', 'anchor_version': 'v-opaque-001', 'authority_ref': 'authority-synth-001', 'config_revision_ref': 'cfgrev-synth-001', 'document_ref': 'doc-synth-001', 'object_type': 'pa.provisioning.document/v1', 'pa_id': UUID_A, 'policy_ref': 'policy-synth-001', 'policy_version': 'v-opaque-pol-001', 'relation_ref': 'rel-synth-001', 'resource_perimeter_ref': 'perim-synth-001', 'resource_perimeter_version': 'v-opaque-perim-001', 'schema_version': '1.0.0', 'scope_id': None, 'scope_type': 'PLATFORM', 'secret_refs': [{'ref': 'sec-synth-001', 'version': 'v-opaque-sec-001'}], 'tenant_id': None}
def make_canonical(base):
    '''Reemission canonique attendue pour les jeux.'''
    text = json.dumps(base, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)
    return text.encode('utf-8')
class NominalCases(unittest.TestCase):
    '''Cas nominaux publics.'''
    def test_platform_roundtrip(self):
        base = make_base_dict()
        raw = make_canonical(base)
        doc = decode_provisioning_document(raw, make_limits())
        self.assertEqual(doc.scope_type, 'PLATFORM')
        self.assertEqual(encode_provisioning_document(doc, make_limits()), raw)
    def test_tenant_null_scope(self):
        base = make_base_dict()
        base['scope_type'] = 'TENANT'
        base['tenant_id'] = 'tenant-synth-001'
        base['scope_id'] = None
        raw = make_canonical(base)
        doc = decode_provisioning_document(raw, make_limits())
        self.assertEqual(encode_provisioning_document(doc, make_limits()), raw)
    def test_tenant_text_scope(self):
        base = make_base_dict()
        base['scope_type'] = 'TENANT'
        base['tenant_id'] = 'tenant-synth-001'
        base['scope_id'] = 'scope-synth-001'
        raw = make_canonical(base)
        doc = decode_provisioning_document(raw, make_limits())
        self.assertEqual(encode_provisioning_document(doc, make_limits()), raw)
    def test_empty_list(self):
        base = make_base_dict()
        base['secret_refs'] = []
        raw = make_canonical(base)
        doc = decode_provisioning_document(raw, make_limits())
        self.assertEqual(doc.secret_refs, tuple())
    def test_order_kept(self):
        base = make_base_dict()
        base['secret_refs'] = [{'ref': 'b-sec', 'version': 'v2'}, {'ref': 'a-sec', 'version': 'v1'}]
        raw = make_canonical(base)
        doc = decode_provisioning_document(raw, make_limits())
        self.assertEqual(doc.secret_refs[0].ref, 'b-sec')
        self.assertEqual(doc.secret_refs[1].ref, 'a-sec')
    def test_uuid_like_opaque_accepted(self):
        base = make_base_dict()
        base['anchor_ref'] = UUID_A
        raw = make_canonical(base)
        doc = decode_provisioning_document(raw, make_limits())
        self.assertEqual(doc.anchor_ref, UUID_A)
class DuplicateCases(unittest.TestCase):
    '''Doublons JSON valides refuses par l API.'''
    def test_root_duplicate_valid_syntax(self):
        quote = chr(34)
        colon = ':'
        comma = ','
        open_brace = '{'
        close_brace = '}'
        first = quote + 'anchor_ref' + quote + colon + quote + 'first' + quote
        second = quote + 'anchor_ref' + quote + colon + quote + 'second' + quote
        rest_parts = []
        base = make_base_dict()
        for key in base:
            if key == 'anchor_ref':
                continue
            rest_parts.append(quote + key + quote + colon + json.dumps(base[key], ensure_ascii=False))
        text = open_brace + first + comma + second + comma + comma.join(rest_parts) + close_brace
        raw = text.encode('utf-8')
        parsed = json.loads(raw)
        self.assertEqual(parsed['anchor_ref'], 'second')
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw, make_limits())
    def test_nested_duplicate_ref(self):
        quote = chr(34)
        text = quote + 'ref' + quote + ':' + quote + 'a' + quote + ',' + quote + 'ref' + quote + ':' + quote + 'b' + quote + ',' + quote + 'version' + quote + ':' + quote + 'v1' + quote
        inner = '{' + text + '}'
        base = make_base_dict()
        base['secret_refs'] = []
        outer = make_canonical(base)
        outer_text = outer.decode('utf-8')
        marker = '"secret_refs":[]'
        self.assertIn('secret_refs', outer_text)
        injected = outer_text.replace('[]', '[' + inner + ']', 1)
        raw = injected.encode('utf-8')
        parsed = json.loads(raw)
        self.assertEqual(parsed['secret_refs'][0]['ref'], 'b')
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw, make_limits())
class SurrogateCases(unittest.TestCase):
    '''Surrogats et octets invalides jusqu a l API.'''
    def test_escaped_surrogate_rejected(self):
        base = make_base_dict()
        raw = make_canonical(base)
        text = raw.decode('utf-8')
        backslash = chr(92)
        escaped = backslash + 'ud800'
        target = 'anchor-synth-001'
        mutated = text.replace(target, escaped)
        mutated_raw = mutated.encode('utf-8')
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(mutated_raw, make_limits())
    def test_ascii_escaped_surrogate_path(self):
        base = make_base_dict()
        base['anchor_ref'] = chr(55296)
        text = json.dumps(base, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)
        raw = text.encode('utf-8')
        self.assertIn(chr(92), text)
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw, make_limits())
    def test_invalid_utf8_bytes(self):
        raw = bytes([255, 254, 253, 0, 1, 2])
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw, make_limits())
    def test_direct_secret_surrogate(self):
        with self.assertRaises(ProvisioningContractError):
            SecretRef(ref=chr(55296), version='v1')
class ProfileGuardCases(unittest.TestCase):
    '''Garde profil avant lecture.'''
    def test_mutated_profile_blocks_parse(self):
        limits = make_limits()
        object.__setattr__(limits, 'max_json_bytes', 'huge')
        base = make_base_dict()
        raw = make_canonical(base)
        with patch('pixs.pa_native.provisioning_contracts.json.loads') as mocked:
            mocked.side_effect = AssertionError('parse appele trop tot')
            with self.assertRaises(ProvisioningContractError):
                decode_provisioning_document(raw, limits)
            mocked.assert_not_called()
    def test_incomplete_profile_blocks_parse(self):
        limits = object.__new__(ProvisioningLimits)
        base = make_base_dict()
        raw = make_canonical(base)
        with patch('pixs.pa_native.provisioning_contracts.json.loads') as mocked:
            with self.assertRaises(ProvisioningContractError):
                decode_provisioning_document(raw, limits)
            mocked.assert_not_called()
    def test_unexpected_loader_error_propagates(self):
        base = make_base_dict()
        raw = make_canonical(base)
        with patch('pixs.pa_native.provisioning_contracts.json.loads', side_effect=RuntimeError('sentinelle')):
            with self.assertRaises(RuntimeError):
                decode_provisioning_document(raw, make_limits())
class LimitCases(unittest.TestCase):
    '''Bornes synthetiques, sans defaut production.'''
    def test_four_accepted_both_paths(self):
        base = make_base_dict()
        base['secret_refs'] = [{'ref': 'r' + str(i), 'version': 'v1'} for i in range(4)]
        raw = make_canonical(base)
        doc = decode_provisioning_document(raw, make_limits())
        self.assertEqual(len(doc.secret_refs), 4)
        self.assertEqual(encode_provisioning_document(doc, make_limits()), raw)
    def test_five_rejected_decode_and_encode(self):
        base = make_base_dict()
        base['secret_refs'] = [{'ref': 'r' + str(i), 'version': 'v1'} for i in range(5)]
        raw = make_canonical(base)
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw, make_limits())
        doc = ProvisioningDocument(anchor_ref='a', anchor_version='v1', authority_ref='auth', config_revision_ref='cfg', document_ref='doc', object_type='pa.provisioning.document/v1', pa_id=uuid.UUID(UUID_A), policy_ref='pol', policy_version='v1', relation_ref='rel', resource_perimeter_ref='per', resource_perimeter_version='v1', schema_version='1.0.0', scope_id=None, scope_type='PLATFORM', secret_refs=tuple([SecretRef(ref='r' + str(i), version='v1') for i in range(5)]), tenant_id=None)
        with self.assertRaises(ProvisioningContractError):
            encode_provisioning_document(doc, make_limits())
    def test_json_bound_exact_both_paths(self):
        base = make_base_dict()
        raw = make_canonical(base)
        size = len(raw)
        doc = decode_provisioning_document(raw, make_limits(json_size=size))
        self.assertEqual(encode_provisioning_document(doc, make_limits(json_size=size)), raw)
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw, make_limits(json_size=size - 1))
        with self.assertRaises(ProvisioningContractError):
            encode_provisioning_document(doc, make_limits(json_size=size - 1))
    def test_ref_bound_sizes(self):
        base = make_base_dict()
        base['anchor_ref'] = 'a' * 256
        raw = make_canonical(base)
        decode_provisioning_document(raw, make_limits())
        base['anchor_ref'] = 'a' * 257
        raw = make_canonical(base)
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw, make_limits())
    def test_multibyte_counted_in_bytes(self):
        base = make_base_dict()
        base['anchor_ref'] = chr(233) * 128
        raw = make_canonical(base)
        decode_provisioning_document(raw, make_limits())
        base['anchor_ref'] = chr(233) * 129
        raw = make_canonical(base)
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw, make_limits())
class HostileTypeCases(unittest.TestCase):
    '''Sous-classes et objets hostiles sans appel dangereux.'''
    def test_subclass_str_rejected_quietly(self):
        calls = []
        class TrackingStr(str):
            def __eq__(self, other):
                calls.append('eq')
                return super().__eq__(other)
            def __str__(self):
                calls.append('str')
                return super().__str__()
            def __repr__(self):
                calls.append('repr')
                return super().__repr__()
        hostile = TrackingStr('PLATFORM')
        with self.assertRaises(ProvisioningContractError):
            ProvisioningDocument(anchor_ref='a', anchor_version='v1', authority_ref='auth', config_revision_ref='cfg', document_ref='doc', object_type=TrackingStr('pa.provisioning.document/v1'), pa_id=uuid.UUID(UUID_A), policy_ref='pol', policy_version='v1', relation_ref='rel', resource_perimeter_ref='per', resource_perimeter_version='v1', schema_version='1.0.0', scope_id=None, scope_type=hostile, secret_refs=tuple(), tenant_id=None)
        self.assertNotIn('eq', calls)
        self.assertNotIn('str', calls)
        self.assertNotIn('repr', calls)
    def test_subclass_int_tuple_list_dict_bytes(self):
        '''Sous-classes refusees sans appel dangereux.'''
        calls = []
        class TrackingInt(int):
            def __eq__(self, other):
                calls.append('eq-int')
                return super().__eq__(other)
            def __str__(self):
                calls.append('str-int')
                return super().__str__()
        class TrackingTuple(tuple):
            def __iter__(self):
                calls.append('iter-tuple')
                return super().__iter__()
            def __len__(self):
                calls.append('len-tuple')
                return super().__len__()
        class TrackingList(list):
            def __iter__(self):
                calls.append('iter-list')
                return super().__iter__()
        class TrackingDict(dict):
            def __getitem__(self, key):
                calls.append('getitem-dict')
                return super().__getitem__(key)
        class TrackingBytes(bytes):
            def __len__(self):
                calls.append('len-bytes')
                return super().__len__()
        base = make_base_dict()
        raw = make_canonical(base)
        valid_doc = decode_provisioning_document(raw, make_limits())
        self.assertEqual(encode_provisioning_document(valid_doc, make_limits()), raw)
        bad_limits = make_limits()
        object.__setattr__(bad_limits, 'max_json_bytes', TrackingInt(8192))
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw, bad_limits)
        with self.assertRaises(ProvisioningContractError):
            encode_provisioning_document(valid_doc, bad_limits)
        mutated_doc = decode_provisioning_document(raw, make_limits())
        object.__setattr__(mutated_doc, 'secret_refs', TrackingTuple(()))
        with self.assertRaises(ProvisioningContractError):
            encode_provisioning_document(mutated_doc, make_limits())
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(TrackingBytes(raw), make_limits())
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(TrackingList([1]), make_limits())
        with self.assertRaises(ProvisioningContractError):
            encode_provisioning_document(TrackingDict({}), make_limits())
        self.assertEqual(calls, [])
    def test_generic_object_and_missing_attrs(self):
        class OpaqueObject:
            def __getattribute__(self, name):
                raise AssertionError('acces inattendu')
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(OpaqueObject(), make_limits())
        with self.assertRaises(ProvisioningContractError):
            encode_provisioning_document(OpaqueObject(), make_limits())
        empty_limits = object.__new__(ProvisioningLimits)
        base = make_base_dict()
        raw = make_canonical(base)
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw, empty_limits)
        empty_secret = object.__new__(SecretRef)
        with self.assertRaises(ProvisioningContractError):
            encode_provisioning_document(empty_secret, make_limits())
    def test_mutated_secret_and_uuid(self):
        secret = SecretRef(ref='ok', version='v1')
        object.__setattr__(secret, 'ref', '')
        base = make_base_dict()
        raw = make_canonical(base)
        doc = decode_provisioning_document(raw, make_limits())
        object.__setattr__(doc.secret_refs[0], 'ref', TrackingValue('x'))
        with self.assertRaises(ProvisioningContractError):
            encode_provisioning_document(doc, make_limits())
        good_uuid = uuid.UUID(UUID_A)
        object.__setattr__(good_uuid, 'int', 0)
        with self.assertRaises(ProvisioningContractError):
            ProvisioningDocument(anchor_ref='a', anchor_version='v1', authority_ref='auth', config_revision_ref='cfg', document_ref='doc', object_type='pa.provisioning.document/v1', pa_id=good_uuid, policy_ref='pol', policy_version='v1', relation_ref='rel', resource_perimeter_ref='per', resource_perimeter_version='v1', schema_version='1.0.0', scope_id=None, scope_type='PLATFORM', secret_refs=tuple(), tenant_id=None)
        other_uuid = uuid.UUID(UUID_A)
        try:
            object.__delattr__(other_uuid, 'int')
        except AttributeError:
            pass
        with self.assertRaises(ProvisioningContractError):
            ProvisioningDocument(anchor_ref='a', anchor_version='v1', authority_ref='auth', config_revision_ref='cfg', document_ref='doc', object_type='pa.provisioning.document/v1', pa_id=other_uuid, policy_ref='pol', policy_version='v1', relation_ref='rel', resource_perimeter_ref='per', resource_perimeter_version='v1', schema_version='1.0.0', scope_id=None, scope_type='PLATFORM', secret_refs=tuple(), tenant_id=None)
class TrackingValue(str):
    '''Valeur temoin pour mutation hostile.'''
    pass
class DirectBuildCases(unittest.TestCase):
    '''Construction directe et champs fermes.'''
    def test_missing_wire_keys_rejected(self):
        for key in list(make_base_dict().keys()):
            base = make_base_dict()
            del base[key]
            raw = make_canonical(base)
            with self.assertRaises(ProvisioningContractError, msg=key):
                decode_provisioning_document(raw, make_limits())
    def test_null_outside_scope_rejected(self):
        base = make_base_dict()
        base['anchor_ref'] = None
        raw = make_canonical(base)
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw, make_limits())
    def test_opaque_versions_and_uuid_like(self):
        base = make_base_dict()
        base['anchor_version'] = 'n importe quelle version'
        base['policy_version'] = UUID_A
        base['resource_perimeter_version'] = 'v9'
        raw = make_canonical(base)
        doc = decode_provisioning_document(raw, make_limits())
        self.assertEqual(doc.policy_version, UUID_A)
    def test_direct_bad_opaques_scopes_uuid(self):
        with self.assertRaises(ProvisioningContractError):
            SecretRef(ref='', version='v1')
        with self.assertRaises(ProvisioningContractError):
            SecretRef(ref=chr(0) + 'a', version='v1')
        with self.assertRaises(ProvisioningContractError):
            ProvisioningDocument(anchor_ref='a', anchor_version='v1', authority_ref='auth', config_revision_ref='cfg', document_ref='doc', object_type='pa.provisioning.document/v1', pa_id=uuid.UUID(UUID_A), policy_ref='pol', policy_version='v1', relation_ref='rel', resource_perimeter_ref='per', resource_perimeter_version='v1', schema_version='1.0.0', scope_id='x', scope_type='PLATFORM', secret_refs=tuple(), tenant_id=None)
        with self.assertRaises(ProvisioningContractError):
            ProvisioningDocument(anchor_ref='a', anchor_version='v1', authority_ref='auth', config_revision_ref='cfg', document_ref='doc', object_type='pa.provisioning.document/v1', pa_id=uuid.UUID('00000000-0000-1000-8000-000000000000'), policy_ref='pol', policy_version='v1', relation_ref='rel', resource_perimeter_ref='per', resource_perimeter_version='v1', schema_version='1.0.0', scope_id=None, scope_type='PLATFORM', secret_refs=tuple(), tenant_id=None)
    def test_duplicate_pair_direct(self):
        with self.assertRaises(ProvisioningContractError):
            ProvisioningDocument(anchor_ref='a', anchor_version='v1', authority_ref='auth', config_revision_ref='cfg', document_ref='doc', object_type='pa.provisioning.document/v1', pa_id=uuid.UUID(UUID_A), policy_ref='pol', policy_version='v1', relation_ref='rel', resource_perimeter_ref='per', resource_perimeter_version='v1', schema_version='1.0.0', scope_id=None, scope_type='PLATFORM', secret_refs=(SecretRef(ref='a', version='v1'), SecretRef(ref='a', version='v1')), tenant_id=None)
    def test_exact_constant_types(self):
        with self.assertRaises(ProvisioningContractError):
            ProvisioningDocument(anchor_ref='a', anchor_version='v1', authority_ref='auth', config_revision_ref='cfg', document_ref='doc', object_type=123, pa_id=uuid.UUID(UUID_A), policy_ref='pol', policy_version='v1', relation_ref='rel', resource_perimeter_ref='per', resource_perimeter_version='v1', schema_version='1.0.0', scope_id=None, scope_type='PLATFORM', secret_refs=tuple(), tenant_id=None)
    def test_frozen_all(self):
        doc = decode_provisioning_document(make_canonical(make_base_dict()), make_limits())
        with self.assertRaises(dataclasses.FrozenInstanceError):
            doc.anchor_ref = 'autre'
        with self.assertRaises(dataclasses.FrozenInstanceError):
            make_limits().max_json_bytes = 1
        with self.assertRaises(dataclasses.FrozenInstanceError):
            doc.secret_refs[0].ref = 'autre'
class CanonicalCases(unittest.TestCase):
    '''Canonicite stricte et profondeur.'''
    def test_key_order_spaces_final_lf_bom(self):
        '''Ordre et espaces refuses, JSON inverse valide.'''
        base = make_base_dict()
        raw = make_canonical(base)
        reversed_base = {}
        for key in reversed(list(base.keys())):
            reversed_base[key] = base[key]
        reversed_text = json.dumps(reversed_base, sort_keys=False, separators=(',', ':'), ensure_ascii=False, allow_nan=False)
        raw_reverse = reversed_text.encode('utf-8')
        self.assertEqual(json.loads(raw_reverse), base)
        self.assertNotEqual(raw_reverse, raw)
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw_reverse, make_limits())
        spaced = raw.replace(bytes([44]), bytes([44, 32]), 1)
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(spaced, make_limits())
        with_lf = raw + bytes([10])
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(with_lf, make_limits())
        with_bom = bytes([239, 187, 191]) + raw
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(with_bom, make_limits())
    def test_ascii_escape_rejected(self):
        base = make_base_dict()
        raw = make_canonical(base)
        text = raw.decode('utf-8')
        backslash = chr(92)
        escaped = text.replace('anchor', backslash + 'u0061nchor')
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(escaped.encode('utf-8'), make_limits())
    def test_numbers_booleans_constants(self):
        for bad in [0, 1, 12, 1.5, True, False]:
            base = make_base_dict()
            base['document_ref'] = bad
            raw = make_canonical(base)
            with self.assertRaises(ProvisioningContractError):
                decode_provisioning_document(raw, make_limits())
        base_text = make_canonical(make_base_dict()).decode('utf-8')
        for token in ['NaN', 'Infinity', '-Infinity']:
            mutated = base_text.replace('null', token, 1)
            with self.assertRaises(ProvisioningContractError):
                decode_provisioning_document(mutated.encode('utf-8'), make_limits())
    def test_uuid_shapes(self):
        for bad_uuid in ['PAS-UN-UUID', '0193A1B2-C3D4-7E5F-8A90-1234567890AB', '00000000-0000-1000-8000-000000000000', '00000000-0000-4000-8000-000000000000', '0193a1b2c3d47e5f8a901234567890ab', '']:
            base = make_base_dict()
            base['pa_id'] = bad_uuid
            raw = make_canonical(base)
            with self.assertRaises(ProvisioningContractError, msg=bad_uuid):
                decode_provisioning_document(raw, make_limits())
    def test_depth_and_lures(self):
        base = make_base_dict()
        base['secret_refs'] = [{'ref': 'a', 'version': 'v1', 'extra': {'deep': []}}]
        raw = make_canonical(base)
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw, make_limits())
        base = make_base_dict()
        tricky = 'crochet ' + chr(91) + ' ' + chr(123) + ' ' + chr(93) + ' ' + chr(125) + ' guillemet ' + chr(34) + ' barre ' + chr(92) + ' fin'
        base['anchor_ref'] = tricky
        raw = make_canonical(base)
        doc = decode_provisioning_document(raw, make_limits())
        self.assertEqual(doc.anchor_ref, tricky)
class DiagnosticCases(unittest.TestCase):
    '''Diagnostic fixe sans fuite.'''
    def test_fixed_fields_no_cause(self):
        base = make_base_dict()
        del base['anchor_ref']
        raw = make_canonical(base)
        try:
            decode_provisioning_document(raw, make_limits())
            self.fail('devrait refuser')
        except ProvisioningContractError as err:
            self.assertEqual(str(err), FIXED_MESSAGE)
            self.assertEqual(err.code, 'PROVISIONING_INVALID')
            self.assertEqual(err.element, 'provisioning_document')
            self.assertEqual(err.step, 'validate_provisioning_document')
            self.assertEqual(err.args, (FIXED_MESSAGE,))
            self.assertNotIn('anchor', str(err))
            self.assertIsNone(err.__cause__)
            self.assertIn('PROVISIONING_INVALID', repr(err))
class ExtraCoverageCases(unittest.TestCase):
    '''Gardes complementaires exigees.'''
    def test_profile_all_bounds_guarded(self):
        '''Bornes invalides refusees avant lecture.'''
        class TrackingInt(int):
            pass
        for field in ('max_json_bytes', 'max_ref_bytes', 'max_secret_refs'):
            for bad in (0, -1, True, 1.5, None):
                kwargs = {'max_json_bytes': 8192, 'max_ref_bytes': 256, 'max_secret_refs': 4}
                kwargs[field] = bad
                with self.assertRaises(ProvisioningContractError, msg=field):
                    ProvisioningLimits(**kwargs)
            kwargs = {'max_json_bytes': 8192, 'max_ref_bytes': 256, 'max_secret_refs': 4}
            kwargs[field] = TrackingInt(8)
            with self.assertRaises(ProvisioningContractError, msg=field):
                ProvisioningLimits(**kwargs)
        base = make_base_dict()
        raw = make_canonical(base)
        valid_doc = decode_provisioning_document(raw, make_limits())
        for field in ('max_json_bytes', 'max_ref_bytes', 'max_secret_refs'):
            mutated = make_limits()
            object.__setattr__(mutated, field, 'bad')
            with patch('pixs.pa_native.provisioning_contracts.json.loads') as mocked:
                with self.assertRaises(ProvisioningContractError):
                    decode_provisioning_document(raw, mutated)
                mocked.assert_not_called()
            with patch('pixs.pa_native.provisioning_contracts.json.loads') as mocked:
                with self.assertRaises(ProvisioningContractError):
                    encode_provisioning_document(valid_doc, mutated)
                mocked.assert_not_called()
    def test_unknown_keys_root_nested(self):
        '''Cles inconnues refusees sur JSON valides.'''
        base = make_base_dict()
        base['extra_root'] = 'x'
        raw = make_canonical(base)
        self.assertIn('extra_root', json.loads(raw))
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw, make_limits())
        base = make_base_dict()
        base['secret_refs'] = [{'ref': 'a', 'version': 'v1', 'extra_nested': 'x'}]
        raw = make_canonical(base)
        self.assertIn('extra_nested', json.loads(raw)['secret_refs'][0])
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw, make_limits())
    def test_direct_surrogate_replace(self):
        '''Surrogate direct refuse sans fuite.'''
        base = make_base_dict()
        raw = make_canonical(base)
        valid_doc = decode_provisioning_document(raw, make_limits())
        with self.assertRaises(ProvisioningContractError):
            dataclasses.replace(valid_doc, anchor_ref=chr(55296))
        with self.assertRaises(ProvisioningContractError):
            SecretRef(ref='ok', version=chr(55296))
    def test_incomplete_and_deleted_attributes(self):
        '''Objets incomplets et attributs supprimes, meme diagnostic.'''
        base = make_base_dict()
        raw = make_canonical(base)
        valid_doc = decode_provisioning_document(raw, make_limits())
        empty_doc = object.__new__(ProvisioningDocument)
        with self.assertRaises(ProvisioningContractError):
            encode_provisioning_document(empty_doc, make_limits())
        incomplete_secret = object.__new__(SecretRef)
        holder = decode_provisioning_document(raw, make_limits())
        object.__setattr__(holder, 'secret_refs', tuple([incomplete_secret]))
        with self.assertRaises(ProvisioningContractError):
            encode_provisioning_document(holder, make_limits())
        target_doc = decode_provisioning_document(raw, make_limits())
        object.__delattr__(target_doc, 'anchor_ref')
        with self.assertRaises(ProvisioningContractError):
            encode_provisioning_document(target_doc, make_limits())
        target_limits = make_limits()
        object.__delattr__(target_limits, 'max_json_bytes')
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw, target_limits)
        target_secret = SecretRef(ref='ok', version='v1')
        object.__delattr__(target_secret, 'ref')
        holder_two = decode_provisioning_document(raw, make_limits())
        object.__setattr__(holder_two, 'secret_refs', tuple([target_secret]))
        with self.assertRaises(ProvisioningContractError):
            encode_provisioning_document(holder_two, make_limits())
        self.assertEqual(valid_doc.scope_type, 'PLATFORM')
    def test_hostile_constants_quiet(self):
        '''Constantes hostiles sans appel.'''
        calls = []
        class TrackingStr(str):
            def __eq__(self, other):
                calls.append('eq')
                return super().__eq__(other)
            def __hash__(self):
                calls.append('hash')
                return super().__hash__()
            def __str__(self):
                calls.append('str')
                return super().__str__()
            def __repr__(self):
                calls.append('repr')
                return super().__repr__()
        with self.assertRaises(ProvisioningContractError):
            ProvisioningDocument(anchor_ref='a', anchor_version='v1', authority_ref='auth', config_revision_ref='cfg', document_ref='doc', object_type=TrackingStr('pa.provisioning.document/v1'), pa_id=uuid.UUID(UUID_A), policy_ref='pol', policy_version='v1', relation_ref='rel', resource_perimeter_ref='per', resource_perimeter_version='v1', schema_version='1.0.0', scope_id=None, scope_type='PLATFORM', secret_refs=tuple(), tenant_id=None)
        with self.assertRaises(ProvisioningContractError):
            ProvisioningDocument(anchor_ref='a', anchor_version='v1', authority_ref='auth', config_revision_ref='cfg', document_ref='doc', object_type='pa.provisioning.document/v1', pa_id=uuid.UUID(UUID_A), policy_ref='pol', policy_version='v1', relation_ref='rel', resource_perimeter_ref='per', resource_perimeter_version='v1', schema_version=TrackingStr('1.0.0'), scope_id=None, scope_type='PLATFORM', secret_refs=tuple(), tenant_id=None)
        with self.assertRaises(ProvisioningContractError):
            ProvisioningDocument(anchor_ref='a', anchor_version='v1', authority_ref='auth', config_revision_ref='cfg', document_ref='doc', object_type='pa.provisioning.document/v1', pa_id=uuid.UUID(UUID_A), policy_ref='pol', policy_version='v1', relation_ref='rel', resource_perimeter_ref='per', resource_perimeter_version='v1', schema_version='1.0.0', scope_id=None, scope_type=TrackingStr('PLATFORM'), secret_refs=tuple(), tenant_id=None)
        base = make_base_dict()
        raw = make_canonical(base)
        mutated = decode_provisioning_document(raw, make_limits())
        object.__setattr__(mutated, 'object_type', TrackingStr('pa.provisioning.document/v1'))
        with self.assertRaises(ProvisioningContractError):
            encode_provisioning_document(mutated, make_limits())
        self.assertEqual(calls, [])
    def test_ref_bounds_both_paths(self):
        '''Bornes opaques en lecture et ecriture.'''
        for field in ('tenant_id', 'scope_id', 'policy_version', 'resource_perimeter_version'):
            base = make_base_dict()
            base['scope_type'] = 'TENANT'
            base['tenant_id'] = 't'
            base['scope_id'] = 's'
            base[field] = 'a' * 257
            raw = make_canonical(base)
            with self.assertRaises(ProvisioningContractError, msg=field):
                decode_provisioning_document(raw, make_limits())
            valid_base = make_base_dict()
            valid_base['scope_type'] = 'TENANT'
            valid_base['tenant_id'] = 't'
            valid_base['scope_id'] = 's'
            valid_raw = make_canonical(valid_base)
            valid_doc = decode_provisioning_document(valid_raw, make_limits())
            object.__setattr__(valid_doc, field, 'a' * 257)
            with self.assertRaises(ProvisioningContractError, msg=field):
                encode_provisioning_document(valid_doc, make_limits())
        base = make_base_dict()
        base['scope_type'] = 'TENANT'
        base['tenant_id'] = chr(233) * 129
        base['scope_id'] = None
        raw = make_canonical(base)
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw, make_limits())
    def test_uuid_variant_and_int_guards(self):
        '''Variante et entier UUID sans coercition.'''
        base = make_base_dict()
        base['pa_id'] = '0193a1b2-c3d4-7e5f-0a90-1234567890ab'
        raw = make_canonical(base)
        with self.assertRaises(ProvisioningContractError):
            decode_provisioning_document(raw, make_limits())
        good = uuid.UUID(UUID_A)
        object.__setattr__(good, 'int', True)
        with self.assertRaises(ProvisioningContractError):
            ProvisioningDocument(anchor_ref='a', anchor_version='v1', authority_ref='auth', config_revision_ref='cfg', document_ref='doc', object_type='pa.provisioning.document/v1', pa_id=good, policy_ref='pol', policy_version='v1', relation_ref='rel', resource_perimeter_ref='per', resource_perimeter_version='v1', schema_version='1.0.0', scope_id=None, scope_type='PLATFORM', secret_refs=tuple(), tenant_id=None)
        class TrackingInt(int):
            pass
        other = uuid.UUID(UUID_A)
        object.__setattr__(other, 'int', TrackingInt(1))
        with self.assertRaises(ProvisioningContractError):
            ProvisioningDocument(anchor_ref='a', anchor_version='v1', authority_ref='auth', config_revision_ref='cfg', document_ref='doc', object_type='pa.provisioning.document/v1', pa_id=other, policy_ref='pol', policy_version='v1', relation_ref='rel', resource_perimeter_ref='per', resource_perimeter_version='v1', schema_version='1.0.0', scope_id=None, scope_type='PLATFORM', secret_refs=tuple(), tenant_id=None)
        huge = uuid.UUID(UUID_A)
        object.__setattr__(huge, 'int', 340282366920938463463374607431768211456)
        with self.assertRaises(ProvisioningContractError):
            ProvisioningDocument(anchor_ref='a', anchor_version='v1', authority_ref='auth', config_revision_ref='cfg', document_ref='doc', object_type='pa.provisioning.document/v1', pa_id=huge, policy_ref='pol', policy_version='v1', relation_ref='rel', resource_perimeter_ref='per', resource_perimeter_version='v1', schema_version='1.0.0', scope_id=None, scope_type='PLATFORM', secret_refs=tuple(), tenant_id=None)
if __name__ == '__main__':
    unittest.main()
