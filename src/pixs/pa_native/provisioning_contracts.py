'''Codec pur provisionnement PA02, forme fermee v1.

Valide la forme et restitue les octets canoniques exacts.
Ne resout rien, ne verifie aucun secret, n accorde aucune confiance.
Stdlib seule, sans entree sortie, sans horloge, sans reseau.
'''
import json
import uuid
import dataclasses
__all__ = ['ProvisioningLimits', 'SecretRef', 'ProvisioningDocument', 'ProvisioningContractError', 'decode_provisioning_document', 'encode_provisioning_document']
_SCHEMA_VERSION = '1.0.0'
_OBJECT_TYPE = 'pa.provisioning.document/v1'
_SCOPE_PLATFORM = 'PLATFORM'
_SCOPE_TENANT = 'TENANT'
_DOCUMENT_KEYS = ('anchor_ref', 'anchor_version', 'authority_ref', 'config_revision_ref', 'document_ref', 'object_type', 'pa_id', 'policy_ref', 'policy_version', 'relation_ref', 'resource_perimeter_ref', 'resource_perimeter_version', 'schema_version', 'scope_id', 'scope_type', 'secret_refs', 'tenant_id')
_OPAQUE_KEYS = ('anchor_ref', 'anchor_version', 'authority_ref', 'config_revision_ref', 'document_ref', 'policy_ref', 'policy_version', 'relation_ref', 'resource_perimeter_ref', 'resource_perimeter_version')
_SECRET_KEYS = ('ref', 'version')
_DOCUMENT_KEY_SET = frozenset(_DOCUMENT_KEYS)
_SECRET_KEY_SET = frozenset(_SECRET_KEYS)
_UUID_ALPHABET = '0123456789abcdef-'
_RFC_VARIANTS = '89ab'
class ProvisioningContractError(ValueError):
    '''Diagnostic unique au message fixe, sans donnee.'''
    def __init__(self):
        self.code = 'PROVISIONING_INVALID'
        self.element = 'provisioning_document'
        self.step = 'validate_provisioning_document'
        self.message = 'Contrat provisionnement invalide.'
        super().__init__('Contrat provisionnement invalide.')
    def __str__(self):
        return 'Contrat provisionnement invalide.'
    def __repr__(self):
        return 'ProvisioningContractError(PROVISIONING_INVALID)'
def _reject():
    '''Leve le diagnostic unique.'''
    raise ProvisioningContractError()
@dataclasses.dataclass(frozen=True, slots=True, repr=False)
class ProvisioningLimits:
    '''Bornes locales en octets et en nombre, non serialisees.'''
    max_json_bytes: int
    max_ref_bytes: int
    max_secret_refs: int
    def __post_init__(self):
        _validate_limits(self)
@dataclasses.dataclass(frozen=True, slots=True, repr=False)
class SecretRef:
    '''Reference opaque, sans valeur secrete.'''
    ref: str
    version: str
    def __post_init__(self):
        _validate_secret_object(self, None)
@dataclasses.dataclass(frozen=True, slots=True, repr=False)
class ProvisioningDocument:
    '''Document a 17 champs explicitement fournis.'''
    anchor_ref: str
    anchor_version: str
    authority_ref: str
    config_revision_ref: str
    document_ref: str
    object_type: str
    pa_id: uuid.UUID
    policy_ref: str
    policy_version: str
    relation_ref: str
    resource_perimeter_ref: str
    resource_perimeter_version: str
    schema_version: str
    scope_id: str | None
    scope_type: str
    secret_refs: tuple[SecretRef, ...]
    tenant_id: str | None
    def __post_init__(self):
        _validate_document_object(self, None)
def _is_surrogate(text):
    '''Detecte un surrogate isole.'''
    for ch in text:
        code = ord(ch)
        if 55296 <= code <= 57343:
            return True
    return False
def _validate_limits(limits):
    '''Controle central du profil avant toute lecture.'''
    if type(limits) is not ProvisioningLimits:
        _reject()
    try:
        json_bound = limits.max_json_bytes
        ref_bound = limits.max_ref_bytes
        count_bound = limits.max_secret_refs
    except AttributeError:
        raise ProvisioningContractError() from None
    if type(json_bound) is not int:
        _reject()
    if type(ref_bound) is not int:
        _reject()
    if type(count_bound) is not int:
        _reject()
    if json_bound <= 0:
        _reject()
    if ref_bound <= 0:
        _reject()
    if count_bound <= 0:
        _reject()
def _validate_opaque_base(candidate):
    '''Controle opaque independant du profil.'''
    if type(candidate) is not str:
        _reject()
    if len(candidate) == 0:
        _reject()
    for ch in candidate:
        code = ord(ch)
        if code < 32 or code == 127:
            _reject()
    if _is_surrogate(candidate):
        _reject()
    try:
        candidate.encode('utf-8')
    except UnicodeEncodeError:
        raise ProvisioningContractError() from None
def _validate_opaque_bounded(candidate, ref_bound):
    '''Controle opaque avec borne en octets.'''
    _validate_opaque_base(candidate)
    try:
        size = len(candidate.encode('utf-8'))
    except UnicodeEncodeError:
        raise ProvisioningContractError() from None
    if size > ref_bound:
        _reject()
def _validate_uuid_string(text):
    '''Valide la chaine UUIDv7 canonique et rend l objet.'''
    if type(text) is not str:
        _reject()
    if len(text) != 36:
        _reject()
    if text[8] != '-' or text[13] != '-' or text[18] != '-' or text[23] != '-':
        _reject()
    if text != text.lower():
        _reject()
    for ch in text:
        if ch not in _UUID_ALPHABET:
            _reject()
    if text[14] != '7':
        _reject()
    if text[19] not in _RFC_VARIANTS:
        _reject()
    try:
        uuid_obj = uuid.UUID(text)
    except ValueError:
        raise ProvisioningContractError() from None
    _validate_uuid_object(uuid_obj)
    if str(uuid_obj) != text:
        _reject()
    return uuid_obj
def _validate_uuid_object(uuid_obj):
    '''Controle l objet UUID par son entier exact avant proprietes.'''
    if type(uuid_obj) is not uuid.UUID:
        _reject()
    try:
        raw_int = object.__getattribute__(uuid_obj, 'int')
    except AttributeError:
        raise ProvisioningContractError() from None
    if type(raw_int) is not int:
        _reject()
    if raw_int < 0 or raw_int >= 340282366920938463463374607431768211456:
        _reject()
    if ((raw_int >> 76) & 15) != 7:
        _reject()
    if ((raw_int >> 62) & 3) != 2:
        _reject()
def _validate_secret_object(secret, ref_bound):
    '''Validation centrale d une reference, avec ou sans borne.'''
    if type(secret) is not SecretRef:
        _reject()
    try:
        ref_value = secret.ref
        version_value = secret.version
    except AttributeError:
        raise ProvisioningContractError() from None
    if ref_bound is None:
        _validate_opaque_base(ref_value)
        _validate_opaque_base(version_value)
    else:
        _validate_opaque_bounded(ref_value, ref_bound)
        _validate_opaque_bounded(version_value, ref_bound)
def _read_field(holder, name):
    '''Lecture securisee d un champ apres type exact.'''
    try:
        return object.__getattribute__(holder, name)
    except AttributeError:
        raise ProvisioningContractError() from None
def _validate_document_object(document, ref_bound):
    '''Validation centrale du document, avec ou sans borne.'''
    if type(document) is not ProvisioningDocument:
        _reject()
    values = {}
    for name in _DOCUMENT_KEYS:
        try:
            values[name] = object.__getattribute__(document, name)
        except AttributeError:
            raise ProvisioningContractError() from None
    for name in _OPAQUE_KEYS:
        current = values[name]
        if ref_bound is None:
            _validate_opaque_base(current)
        else:
            _validate_opaque_bounded(current, ref_bound)
    object_type = values['object_type']
    if type(object_type) is not str:
        _reject()
    if object_type != 'pa.provisioning.document/v1':
        _reject()
    schema_version = values['schema_version']
    if type(schema_version) is not str:
        _reject()
    if schema_version != '1.0.0':
        _reject()
    _validate_uuid_object(values['pa_id'])
    scope_type = values['scope_type']
    if type(scope_type) is not str:
        _reject()
    if scope_type not in (_SCOPE_PLATFORM, _SCOPE_TENANT):
        _reject()
    tenant_id = values['tenant_id']
    scope_id = values['scope_id']
    if scope_type == 'PLATFORM':
        if tenant_id is not None:
            _reject()
        if scope_id is not None:
            _reject()
    else:
        if ref_bound is None:
            _validate_opaque_base(tenant_id)
        else:
            _validate_opaque_bounded(tenant_id, ref_bound)
        if scope_id is not None:
            if ref_bound is None:
                _validate_opaque_base(scope_id)
            else:
                _validate_opaque_bounded(scope_id, ref_bound)
    raw_refs = values['secret_refs']
    if type(raw_refs) is not tuple:
        _reject()
    for entry in raw_refs:
        _validate_secret_object(entry, ref_bound)
    seen = set()
    for entry in raw_refs:
        ref_value = _read_field(entry, 'ref')
        version_value = _read_field(entry, 'version')
        if type(ref_value) is not str or type(version_value) is not str:
            _reject()
        pair = (ref_value, version_value)
        if pair in seen:
            _reject()
        seen.add(pair)
def _check_depth(raw):
    '''Profondeur 3 avant lecture, chaines et echappements respectes.'''
    if len(raw) >= 3:
        if raw[0] == 239 and raw[1] == 187 and raw[2] == 191:
            _reject()
    depth = 0
    in_string = False
    escaped = False
    for byte in raw:
        if in_string:
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == 34:
                in_string = False
        else:
            if byte == 34:
                in_string = True
            elif byte == 91 or byte == 123:
                depth += 1
                if depth > 3:
                    _reject()
            elif byte == 93 or byte == 125:
                depth -= 1
                if depth < 0:
                    _reject()
    if in_string or escaped:
        _reject()
def _closed_pairs(pairs):
    '''Refuse les cles dupliquees.'''
    keys = tuple(k for k, _v in pairs)
    if len(frozenset(keys)) != len(keys):
        _reject()
    return dict(pairs)
def _reject_number(text):
    _reject()
def _reject_constant(text):
    _reject()
def _parse_json(raw):
    '''Lecture stricte sans fuite de cause.'''
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        raise ProvisioningContractError() from None
    try:
        return json.loads(text, object_pairs_hook=_closed_pairs, parse_int=_reject_number, parse_float=_reject_number, parse_constant=_reject_constant)
    except ProvisioningContractError:
        raise
    except json.JSONDecodeError:
        raise ProvisioningContractError() from None
def _canonical_dict(document):
    '''Construit le dictionnaire canonique preserve.'''
    items = []
    for entry in document.secret_refs:
        ref_value = _read_field(entry, 'ref')
        version_value = _read_field(entry, 'version')
        if type(ref_value) is not str or type(version_value) is not str:
            _reject()
        items.append({'ref': ref_value, 'version': version_value})
    uuid_obj = _read_field(document, 'pa_id')
    _validate_uuid_object(uuid_obj)
    return {'anchor_ref': _read_field(document, 'anchor_ref'), 'anchor_version': _read_field(document, 'anchor_version'), 'authority_ref': _read_field(document, 'authority_ref'), 'config_revision_ref': _read_field(document, 'config_revision_ref'), 'document_ref': _read_field(document, 'document_ref'), 'object_type': _read_field(document, 'object_type'), 'pa_id': str(uuid_obj), 'policy_ref': _read_field(document, 'policy_ref'), 'policy_version': _read_field(document, 'policy_version'), 'relation_ref': _read_field(document, 'relation_ref'), 'resource_perimeter_ref': _read_field(document, 'resource_perimeter_ref'), 'resource_perimeter_version': _read_field(document, 'resource_perimeter_version'), 'schema_version': _read_field(document, 'schema_version'), 'scope_id': _read_field(document, 'scope_id'), 'scope_type': _read_field(document, 'scope_type'), 'secret_refs': items, 'tenant_id': _read_field(document, 'tenant_id')}
def _emit_canonical(document):
    '''Reemission canonique exacte.'''
    mapping = _canonical_dict(document)
    text = json.dumps(mapping, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)
    return text.encode('utf-8')
def decode_provisioning_document(data: bytes, limits: ProvisioningLimits) -> ProvisioningDocument:
    '''Decode des octets exacts vers un document valide.'''
    _validate_limits(limits)
    if type(data) is not bytes:
        _reject()
    json_bound = _read_field(limits, 'max_json_bytes')
    ref_bound = _read_field(limits, 'max_ref_bytes')
    count_bound = _read_field(limits, 'max_secret_refs')
    if len(data) > json_bound:
        _reject()
    _check_depth(data)
    parsed = _parse_json(data)
    if type(parsed) is not dict:
        _reject()
    if frozenset(parsed.keys()) != _DOCUMENT_KEY_SET:
        _reject()
    for name in _DOCUMENT_KEYS:
        if name not in parsed:
            _reject()
    if type(parsed['scope_type']) is not str:
        _reject()
    if parsed['scope_type'] not in (_SCOPE_PLATFORM, _SCOPE_TENANT):
        _reject()
    for name in _OPAQUE_KEYS:
        _validate_opaque_bounded(parsed[name], ref_bound)
    object_type = parsed['object_type']
    if type(object_type) is not str:
        _reject()
    if object_type != 'pa.provisioning.document/v1':
        _reject()
    schema_version = parsed['schema_version']
    if type(schema_version) is not str:
        _reject()
    if schema_version != '1.0.0':
        _reject()
    identifier = _validate_uuid_string(parsed['pa_id'])
    if parsed['scope_type'] == 'PLATFORM':
        if parsed['tenant_id'] is not None:
            _reject()
        if parsed['scope_id'] is not None:
            _reject()
    else:
        _validate_opaque_bounded(parsed['tenant_id'], ref_bound)
        if parsed['scope_id'] is not None:
            _validate_opaque_bounded(parsed['scope_id'], ref_bound)
    raw_refs = parsed['secret_refs']
    if type(raw_refs) is not list:
        _reject()
    if len(raw_refs) > count_bound:
        _reject()
    built = []
    seen = set()
    for entry in raw_refs:
        if type(entry) is not dict:
            _reject()
        if frozenset(entry.keys()) != _SECRET_KEY_SET:
            _reject()
        _validate_opaque_bounded(entry['ref'], ref_bound)
        _validate_opaque_bounded(entry['version'], ref_bound)
        pair = (entry['ref'], entry['version'])
        if pair in seen:
            _reject()
        seen.add(pair)
        built.append(SecretRef(ref=entry['ref'], version=entry['version']))
    document = ProvisioningDocument(anchor_ref=parsed['anchor_ref'], anchor_version=parsed['anchor_version'], authority_ref=parsed['authority_ref'], config_revision_ref=parsed['config_revision_ref'], document_ref=parsed['document_ref'], object_type=parsed['object_type'], pa_id=identifier, policy_ref=parsed['policy_ref'], policy_version=parsed['policy_version'], relation_ref=parsed['relation_ref'], resource_perimeter_ref=parsed['resource_perimeter_ref'], resource_perimeter_version=parsed['resource_perimeter_version'], schema_version=parsed['schema_version'], scope_id=parsed['scope_id'], scope_type=parsed['scope_type'], secret_refs=tuple(built), tenant_id=parsed['tenant_id'])
    _validate_document_object(document, ref_bound)
    expected = _emit_canonical(document)
    if expected != data:
        _reject()
    return document
def encode_provisioning_document(value: ProvisioningDocument, limits: ProvisioningLimits) -> bytes:
    '''Encode un document valide vers octets canoniques exacts.'''
    _validate_limits(limits)
    ref_bound = _read_field(limits, 'max_ref_bytes')
    count_bound = _read_field(limits, 'max_secret_refs')
    json_bound = _read_field(limits, 'max_json_bytes')
    _validate_document_object(value, ref_bound)
    raw_refs = _read_field(value, 'secret_refs')
    if type(raw_refs) is not tuple:
        _reject()
    if len(raw_refs) > count_bound:
        _reject()
    emitted = _emit_canonical(value)
    if len(emitted) > json_bound:
        _reject()
    return emitted
