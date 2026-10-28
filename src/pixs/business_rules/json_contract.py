"""Codec JSON strict et borne pour O06, pur stdlib.

Decodage et encodage bornes des documents JSON v1 et normalisation
defensive des objets Python directs. Sans I/O, sans environnement,
sans horloge et sans modification globale de l'interpreteur.

Bornes : octets UTF-8 <= 65536, profondeur conteneurs <= 8 avec racine
au niveau 1, noeuds <= 256 en comptant tout conteneur ou scalaire et
sans compter les noms de cles. Tout depassement, cle dupliquee, float,
non-fini, Unicode invalide ou type hors liste est refuse avec une
erreur typee stable, sans recopier le contenu brut.

Exemple synthetique, sans secret :

    data = encode_json_document({"a": [1, 2]})
    value = decode_json_document(data)
"""

from __future__ import annotations

import json

__all__ = [
    "JsonContractError",
    "MAX_DOCUMENT_BYTES",
    "MAX_DEPTH",
    "MAX_NODES",
    "decode_json_document",
    "encode_json_document",
    "normalize_python_value",
]

MAX_DOCUMENT_BYTES = 65536
MAX_DEPTH = 8
MAX_NODES = 256

# Chaque chiffre decimal utilise moins de quatre bits : garde conservative
# derivee du plafond d’octets, sans restreindre un entier JSON admissible.
_MAX_INT_BITS = MAX_DOCUMENT_BYTES * 4
_INT_CHUNK_DIGITS = 9
_INT_BASE = 1000000000
_INT_BASE_DIGITS = 9

_FIXED = "Document JSON hors contrat."


class JsonContractError(ValueError):
    """Erreur typee stable, sans valeur refusee recopiee."""

    def __init__(self, code: str = "JSON_CONTRACT_INVALID") -> None:
        super().__init__(_FIXED)
        self.code = code
        self.element = "json_contract"
        self.step = "validate"


def _fail(code: str) -> None:
    raise JsonContractError(code)


def _has_surrogate(text: str) -> bool:
    for char in text:
        point = ord(char)
        if 0xD800 <= point <= 0xDFFF:
            return True
    return False


def _check_str_key(key: object) -> str:
    if type(key) is not str:
        _fail("JSON_KEY_INVALID")
    assert type(key) is str
    return _check_str_value(key)


def _check_str_value(text: str) -> str:
    if len(text) > MAX_DOCUMENT_BYTES:
        _fail("JSON_SIZE_EXCEEDED")
    if _has_surrogate(text):
        _fail("JSON_UNICODE_INVALID")
    if len(text) * 4 > MAX_DOCUMENT_BYTES:
        try:
            encoded = text.encode("utf-8")
        except UnicodeEncodeError as error:
            raise JsonContractError("JSON_UNICODE_INVALID") from error
        if len(encoded) > MAX_DOCUMENT_BYTES:
            _fail("JSON_SIZE_EXCEEDED")
    return text


def _check_int_value(number: int) -> int:
    if type(number) is bool:
        _fail("JSON_TYPE_FORBIDDEN")
    if number.bit_length() > _MAX_INT_BITS:
        _fail("JSON_SIZE_EXCEEDED")
    return number


def _precheck_text_depth(text: str) -> None:
    depth = 0
    maximum = 0
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "[" or char == "{":
            depth += 1
            if depth > maximum:
                maximum = depth
            if maximum > MAX_DEPTH:
                _fail("JSON_DEPTH_EXCEEDED")
        elif char == "]" or char == "}":
            depth -= 1
            if depth < 0:
                return
    return


def _parse_int_blocks(text: str) -> int:
    negative = text.startswith("-")
    digits = text[1:] if negative else text
    if digits == "":
        _fail("JSON_SYNTAX_INVALID")
    result = 0
    for start in range(0, len(digits), _INT_CHUNK_DIGITS):
        chunk = digits[start:start + _INT_CHUNK_DIGITS]
        try:
            chunk_value = int(chunk)
        except ValueError as error:
            raise JsonContractError("JSON_SYNTAX_INVALID") from error
        result = result * (10 ** len(chunk)) + chunk_value
    if negative:
        result = -result
    return result


def _reject_float(text: str) -> None:
    _fail("JSON_FLOAT_FORBIDDEN")


def _reject_constant(text: str) -> None:
    _fail("JSON_NON_FINITE_FORBIDDEN")


def _pairs_no_duplicates(pairs: list) -> dict:
    result: dict = {}
    for key, value in pairs:
        if type(key) is not str:
            _fail("JSON_KEY_INVALID")
        if key in result:
            _fail("JSON_DUPLICATE_KEY")
        result[key] = value
    return result


def _copy_bounded(root: object) -> object:
    """Validation et copie defensive, ancetres de branche seuls."""
    if root is None:
        return None
    if type(root) is str:
        return _check_str_value(root)
    if type(root) is int:
        return _check_int_value(root)
    if type(root) is bool:
        return root
    if type(root) is not dict and type(root) is not list:
        _fail("JSON_TYPE_FORBIDDEN")
    if type(root) is dict:
        copy_root: object = {}
    else:
        copy_root = []
    count = 1
    ancestors: set = {id(root)}
    if type(root) is dict:
        initial_iter = iter(root.items())
    else:
        initial_iter = iter(root)
    stack: list = [(root, copy_root, 1, initial_iter)]
    while stack:
        original, copy, depth, iterator = stack[-1]
        try:
            if type(original) is dict:
                key, item = next(iterator)
            else:
                key = None
                item = next(iterator)
        except StopIteration:
            ancestors.discard(id(original))
            stack.pop()
            continue
        if type(original) is dict:
            checked_key = _check_str_key(key)
        if item is None or type(item) is str or type(item) is int or type(item) is bool:
            if type(item) is str:
                _check_str_value(item)
            elif type(item) is int:
                _check_int_value(item)
            count += 1
            if count > MAX_NODES:
                _fail("JSON_NODES_EXCEEDED")
            if type(original) is dict:
                copy[checked_key] = item
            else:
                copy.append(item)
            continue
        if type(item) is dict or type(item) is list:
            if id(item) in ancestors:
                _fail("JSON_CYCLIC")
            if depth + 1 > MAX_DEPTH:
                _fail("JSON_DEPTH_EXCEEDED")
            count += 1
            if count > MAX_NODES:
                _fail("JSON_NODES_EXCEEDED")
            if type(item) is dict:
                fresh: object = {}
                child_iter = iter(item.items())
            else:
                fresh = []
                child_iter = iter(item)
            if type(original) is dict:
                copy[checked_key] = fresh
            else:
                copy.append(fresh)
            ancestors.add(id(item))
            stack.append((item, fresh, depth + 1, child_iter))
            continue
        _fail("JSON_TYPE_FORBIDDEN")
    return copy_root


def _int_to_decimal(number: int) -> str:
    if type(number) is bool:
        _fail("JSON_TYPE_FORBIDDEN")
    if number == 0:
        return "0"
    negative = number < 0
    work = -number if negative else number
    if work.bit_length() > _MAX_INT_BITS:
        _fail("JSON_SIZE_EXCEEDED")
    parts: list = []
    while work > 0:
        work, remainder = divmod(work, _INT_BASE)
        parts.append(remainder)
    text = str(parts[-1])
    for remainder in reversed(parts[:-1]):
        text += "%09d" % remainder
    if negative:
        text = "-" + text
    return text


def _append(buffer: bytearray, chunk: bytes) -> None:
    if len(buffer) + len(chunk) > MAX_DOCUMENT_BYTES:
        _fail("JSON_SIZE_EXCEEDED")
    buffer.extend(chunk)


def _encode_into(buffer: bytearray, value: object) -> None:
    if len(buffer) > MAX_DOCUMENT_BYTES:
        _fail("JSON_SIZE_EXCEEDED")
    if value is None:
        _append(buffer, b"null")
        return
    if type(value) is bool:
        _append(buffer, b"true" if value else b"false")
        return
    if type(value) is int:
        _append(buffer, _int_to_decimal(value).encode("ascii"))
        return
    if type(value) is str:
        try:
            chunk = json.dumps(value, ensure_ascii=False).encode("utf-8")
        except UnicodeEncodeError as error:
            raise JsonContractError("JSON_UNICODE_INVALID") from error
        _append(buffer, chunk)
        return
    if type(value) is list:
        _append(buffer, b"[")
        first = True
        for item in value:
            if not first:
                _append(buffer, b",")
            first = False
            _encode_into(buffer, item)
            if len(buffer) > MAX_DOCUMENT_BYTES:
                _fail("JSON_SIZE_EXCEEDED")
        _append(buffer, b"]")
        return
    if type(value) is dict:
        _append(buffer, b"{")
        first = True
        for key in sorted(value.keys()):
            item = value[key]
            try:
                key_chunk = json.dumps(key, ensure_ascii=False).encode("utf-8")
            except UnicodeEncodeError as error:
                raise JsonContractError("JSON_UNICODE_INVALID") from error
            if not first:
                _append(buffer, b",")
            first = False
            _append(buffer, key_chunk)
            _append(buffer, b":")
            _encode_into(buffer, item)
            if len(buffer) > MAX_DOCUMENT_BYTES:
                _fail("JSON_SIZE_EXCEEDED")
        _append(buffer, b"}")
        return
    _fail("JSON_TYPE_FORBIDDEN")


def decode_json_document(data: bytes) -> object:
    """Decode des octets UTF-8 stricts avec bornes."""
    if type(data) is not bytes:
        _fail("JSON_TYPE_FORBIDDEN")
    if len(data) == 0 or len(data) > MAX_DOCUMENT_BYTES:
        _fail("JSON_SIZE_EXCEEDED")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise JsonContractError("JSON_UTF8_INVALID") from error
    _precheck_text_depth(text)
    try:
        loaded = json.loads(
            text,
            object_pairs_hook=_pairs_no_duplicates,
            parse_float=_reject_float,
            parse_int=_parse_int_blocks,
            parse_constant=_reject_constant,
        )
    except JsonContractError:
        raise
    except json.JSONDecodeError as error:
        raise JsonContractError("JSON_SYNTAX_INVALID") from error
    return _copy_bounded(loaded)


def normalize_python_value(value: object) -> object:
    """Copie defensive d'un objet Python direct, memes bornes."""
    snapshot = _copy_bounded(value)
    buffer = bytearray()
    _encode_into(buffer, snapshot)
    return snapshot


def encode_json_document(value: object) -> bytes:
    """Encodage canonique borne d'une valeur defensive."""
    snapshot = _copy_bounded(value)
    buffer = bytearray()
    _encode_into(buffer, snapshot)
    if len(buffer) == 0 or len(buffer) > MAX_DOCUMENT_BYTES:
        _fail("JSON_SIZE_EXCEEDED")
    return bytes(buffer)
