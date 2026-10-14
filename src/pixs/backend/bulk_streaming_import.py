"""Parseurs IMPORT CSV/NDJSON incrémentaux bornés du runtime Bulk v1 (B05, B13).

Module purement mémoire : sans entrée/sortie directe, ORM, Django, psycopg,
stockage, réseau, processus, environnement, import dynamique, sérialisation
globale, callback du payload ni état global mutable (csv.field_size_limit et
sys.set_int_max_str_digits ne sont jamais lus ni modifiés). Les segments
``bytes`` exacts entrent par ``feed()`` et les unités privées sont rendues
immédiatement, sans générateur paresseux ni itérateur fourni par le payload.
``finish()`` fige un bilan borné ; ``close()`` terminalise sans faux succès.

Les refus de métadonnées (mapping, politique, catalogues serveur) sont des
``Diagnostic`` du kernel ; les refus de contenu respectent RowDiagnosticV1
(code statique déclaré, champ déclaré ou None, position) et ne reproduisent
jamais une valeur, un octet fautif ou une exception du payload. Une unité
parsée et mappée ne prétend aucune validation propriétaire, aucune mutation
engagée, aucun checkpoint : les compteurs du bilan sont mécaniques.

Les contrats, validateurs, snapshots et SemVer réutilisés restent inchangés
dans leurs modules livrés ; rien n'ajoute de schéma logique ni de wire format.
"""

from dataclasses import dataclass

import json

from pixs.backend.bulk_execution_values import validate_bulk_policy_values
from pixs.backend.bulk_runtime_contracts import (
    _ContractRefused,
    _capture_policy_values,
    _MappingDescriptorSnapshot,
    _RowDiagnosticSnapshot,
    _build_mapping_descriptor_snapshot,
    _catalog_state,
    _pack,
    _refusal,
    validate_json_value,
    validate_mapping_descriptor_values,
)
from pixs.kernel.diagnostics import Diagnostic

__all__ = ["new_bulk_import_parser"]

_SCOPE = "bulk_streaming_import_parser"

_COMMA = 44
_QUOTE = 34
_LF = 10
_CR = 13
_BOM_PREFIX = b"\xef\xbb\xbf"

_STATE_FIELD_START = 0
_STATE_UNQUOTED = 1
_STATE_QUOTED = 2
_STATE_AFTER_QUOTE = 3
_STATE_DISCARD = 4

_CLOSE_REASONS = frozenset({"CANCELLED", "CLOSED"})

_CSV_BOM_FORBIDDEN = "CSV_BOM_FORBIDDEN"
_CSV_QUOTE_MISUSE = "CSV_QUOTE_MISUSE"
_CSV_LONE_CR = "CSV_LONE_CR"
_CSV_UTF8_INVALID = "CSV_UTF8_INVALID"
_CSV_HEADER_EMPTY = "CSV_HEADER_EMPTY"
_CSV_HEADER_DUPLICATE = "CSV_HEADER_DUPLICATE"
_CSV_HEADER_UNKNOWN = "CSV_HEADER_UNKNOWN"
_CSV_HEADER_INCOMPLETE = "CSV_HEADER_INCOMPLETE"
_CSV_EXTRA_COLUMN = "CSV_EXTRA_COLUMN"
_CSV_MISSING_COLUMN = "CSV_MISSING_COLUMN"
_NDJSON_EMPTY_LINE = "NDJSON_EMPTY_LINE"
_NDJSON_UTF8_INVALID = "NDJSON_UTF8_INVALID"
_NDJSON_DUPLICATE_KEY = "NDJSON_DUPLICATE_KEY"
_NDJSON_CONSTANT_FORBIDDEN = "NDJSON_CONSTANT_FORBIDDEN"
_NDJSON_SYNTAX_INVALID = "NDJSON_SYNTAX_INVALID"
_NDJSON_INT_REPRESENTATION_LIMIT = "NDJSON_INT_REPRESENTATION_LIMIT"
_NDJSON_UNKNOWN_FIELD = "NDJSON_UNKNOWN_FIELD"
_NDJSON_MISSING_REQUIRED = "NDJSON_MISSING_REQUIRED"
_NDJSON_NONFINITE_FLOAT = "NDJSON_NONFINITE_FLOAT"
_INPUT_CHUNK_TYPE_INVALID = "INPUT_CHUNK_TYPE_INVALID"
_LIMIT_READ_CHUNK = "LIMIT_READ_CHUNK"
_LIMIT_INPUT_BYTES = "LIMIT_INPUT_BYTES"
_LIMIT_ROWS = "LIMIT_ROWS"
_LIMIT_ROW_BYTES = "LIMIT_ROW_BYTES"
_LIMIT_COLUMNS = "LIMIT_COLUMNS"
_LIMIT_JSON_DEPTH = "LIMIT_JSON_DEPTH"
_LIMIT_JSON_MEMBERS = "LIMIT_JSON_MEMBERS"
_LIMIT_DIAGNOSTICS = "LIMIT_DIAGNOSTICS"
_EOF_PARTIAL = "EOF_PARTIAL"

#: Codes de contenu statiques émis par les parseurs ; la fabrique exige que le
#: serveur déclare chaque code avant toute consommation (B05/B13, refus sans
#: omission silencieuse). Les codes ne proviennent jamais du payload.
_CONTENT_CODES = frozenset(
    {
        _CSV_BOM_FORBIDDEN,
        _CSV_QUOTE_MISUSE,
        _CSV_LONE_CR,
        _CSV_UTF8_INVALID,
        _CSV_HEADER_EMPTY,
        _CSV_HEADER_DUPLICATE,
        _CSV_HEADER_UNKNOWN,
        _CSV_HEADER_INCOMPLETE,
        _CSV_EXTRA_COLUMN,
        _CSV_MISSING_COLUMN,
        _NDJSON_EMPTY_LINE,
        _NDJSON_UTF8_INVALID,
        _NDJSON_DUPLICATE_KEY,
        _NDJSON_CONSTANT_FORBIDDEN,
        _NDJSON_SYNTAX_INVALID,
        _NDJSON_INT_REPRESENTATION_LIMIT,
        _NDJSON_UNKNOWN_FIELD,
        _NDJSON_MISSING_REQUIRED,
        _NDJSON_NONFINITE_FLOAT,
        _INPUT_CHUNK_TYPE_INVALID,
        _LIMIT_READ_CHUNK,
        _LIMIT_INPUT_BYTES,
        _LIMIT_ROWS,
        _LIMIT_ROW_BYTES,
        _LIMIT_COLUMNS,
        _LIMIT_JSON_DEPTH,
        _LIMIT_JSON_MEMBERS,
        _LIMIT_DIAGNOSTICS,
        _EOF_PARTIAL,
    }
)

#: Contraintes littérales de validate_json_value (module livré) mappées vers les
#: codes de contenu statiques ; la comparaison porte sur la contrainte retournée
#: par le contrat réutilisé, jamais sur une valeur du payload.
_FLOAT_CONSTRAINTS = frozenset({"float exact fini attendu"})
_UNICODE_CONSTRAINTS = frozenset(
    {
        "str Unicode valide attendue",
        "clés dict str Unicode valides attendues",
    }
)
_DEPTH_CONSTRAINTS = frozenset(
    {"profondeur de conteneur inférieure ou égale à la limite attendue"}
)
_MEMBERS_CONSTRAINTS = frozenset(
    {
        "nombre de membres du conteneur inférieur ou égal à la limite attendu",
    }
)

_CHUNK_RULE = "segment bytes exact attendu"
_TERMINAL_RULE = "parseur terminal : opération refusée sans altération du bilan"
_CLOSE_RULE = "raison de fermeture exacte CANCELLED ou CLOSED attendue"
_POLICY_RULE = "PolicyV1 exacte valide attendue avant tout parsing"
_MAPPING_RULE = "MappingDescriptorV1 exact valide attendu avant tout parsing"
_IMPORT_RULE = "variante IMPORT exacte attendue pour un parseur d'import"
_CONTENT_CODE_RULE = (
    "tous les codes de contenu émis doivent être déclarés côté serveur"
)
_TARGET_RULE = "cibles du mapping limitées aux champs publics déclarés du propriétaire"


class _ParserRefused(ValueError):
    """Refus interne statique ; aucun message ne porte de valeur fournie."""


class _DuplicateKeyFound(Exception):
    """Sentinelle privée : doublon de clé détecté avant construction du dict."""


class _ConstantFound(Exception):
    """Sentinelle privée : constante non JSON refusée par parse_constant."""


@dataclass(frozen=True, slots=True)
class _CsvImportUnit:
    line_index: int
    targets: tuple[tuple[str, str], ...]

    def as_values(self) -> dict:
        return {field: value for field, value in self.targets}


@dataclass(frozen=True, slots=True)
class _NdjsonImportUnit:
    line_index: int
    targets: tuple[tuple[str, object], ...]

    def as_values(self) -> dict:
        return {field: _copy_json_value(value) for field, value in self.targets}


@dataclass(frozen=True, slots=True)
class _ImportSummary:
    complete: bool
    limit_reason: str | None
    header: tuple[str, ...] | None
    lines_observed: int
    units_emitted: int
    units_refused: int
    bytes_observed: int
    diagnostics: tuple[_RowDiagnosticSnapshot, ...]

    def as_values(self) -> dict:
        return {
            "complete": self.complete, "limit_reason": self.limit_reason,
            "header": self.header, "lines_observed": self.lines_observed,
            "units_emitted": self.units_emitted, "units_refused": self.units_refused,
            "bytes_observed": self.bytes_observed,
            "diagnostics": tuple(item.as_values() for item in self.diagnostics),
        }


def _reject_duplicate_pairs(pairs: list) -> dict:
    keys: set = set()
    for key, _value in pairs:
        if key in keys:
            raise _DuplicateKeyFound(_NDJSON_DUPLICATE_KEY)
        keys.add(key)
    return dict(pairs)


def _reject_constant(constant: str) -> object:
    raise _ConstantFound(_NDJSON_CONSTANT_FORBIDDEN)


def _copy_json_value(value: object) -> object:
    """Copie itérative de données JSON déjà validées, sans sérialiseur."""
    if type(value) is dict:
        result = {}
    elif type(value) is list:
        result = []
    else:
        return value
    stack = [(value, result)]
    while stack:
        source, target = stack.pop()
        entries = source.items() if type(source) is dict else enumerate(source)
        for key, child in entries:
            if type(child) is dict:
                copied = {}
                stack.append((child, copied))
            elif type(child) is list:
                copied = []
                stack.append((child, copied))
            else:
                copied = child
            if type(target) is dict:
                target[key] = copied
            else:
                target.append(copied)
    return result


def _capture_policy(policy: object) -> tuple[dict | None, list[Diagnostic]]:
    captured = _capture_policy_values(policy)
    refusals = validate_bulk_policy_values(captured)
    if refusals:
        return None, refusals
    return captured, []


def _capture_mapping(mapping: object) -> tuple[_MappingDescriptorSnapshot | None, list[Diagnostic]]:
    try:
        snapshot = _build_mapping_descriptor_snapshot(mapping)
    except (_ContractRefused, KeyError, TypeError):
        return None, [_refusal(_SCOPE, "mapping", _MAPPING_RULE)]
    if snapshot.variant != "IMPORT":
        return None, [_refusal(_SCOPE, "variant", _IMPORT_RULE)]
    return snapshot, []



def new_bulk_import_parser(
    *, mapping: object, policy: object,
    declared_owner_fields: object, declared_codes: object,
) -> tuple["_BulkImportParser | None", list[Diagnostic]]:
    """Compose les métadonnées serveur gardées avant tout parsing de contenu."""
    owner_fields, owner_refusals = _catalog_state(
        declared_owner_fields, _SCOPE, "declared_owner_fields"
    )
    codes, code_refusals = _catalog_state(
        declared_codes, _SCOPE, "declared_codes"
    )
    policy_values, policy_refusals = _capture_policy(policy)
    refusals = [*owner_refusals, *code_refusals, *policy_refusals]
    if refusals or owner_fields is None or codes is None or policy_values is None:
        return None, _pack(refusals)
    if not _CONTENT_CODES <= codes:
        return None, _pack([_refusal(_SCOPE, "declared_codes", _CONTENT_CODE_RULE)])
    mapping_snapshot, mapping_refusals = _capture_mapping(mapping)
    if mapping_refusals or mapping_snapshot is None:
        return None, _pack(mapping_refusals)
    if not frozenset(mapping_snapshot.target_fields) <= owner_fields:
        return None, _pack([_refusal(_SCOPE, "target_fields", _TARGET_RULE)])
    if mapping_snapshot.format == "CSV":
        parser = _CsvImportParser(mapping_snapshot, policy_values, owner_fields)
    else:
        parser = _NdjsonImportParser(mapping_snapshot, policy_values, owner_fields)
    return parser, []


class _BulkImportParser:
    """Base commune : bornes, compteurs mécaniques et diagnostics capés."""

    def __init__(
        self,
        mapping: _MappingDescriptorSnapshot,
        policy: dict,
        owner_fields: frozenset[str],
    ) -> None:
        self._mapping = mapping
        self._policy = policy
        self._owner_fields = owner_fields
        self._lines_observed = 0
        self._units_emitted = 0
        self._units_refused = 0
        self._bytes_observed = 0
        self._data_rows_seen = 0
        self._diagnostics: list[_RowDiagnosticSnapshot] = []
        self._limit: str | None = None
        self._stopped = False
        self._summary: _ImportSummary | None = None
        self._header: tuple[str, ...] | None = None

    @property
    def _max_diagnostics(self) -> int:
        return self._policy["max_diagnostics"]

    def feed(self, chunk: object) -> tuple:
        if self._summary is not None:
            raise _ParserRefused(_TERMINAL_RULE)
        if self._stopped:
            return ()
        if type(chunk) is not bytes:
            self._halt(_INPUT_CHUNK_TYPE_INVALID, None)
            return ()
        if not chunk:
            return ()
        if len(chunk) > self._policy["read_chunk_bytes"]:
            self._halt(_LIMIT_READ_CHUNK, None)
            return ()
        if self._bytes_observed + len(chunk) > self._policy["max_input_bytes"]:
            self._halt(_LIMIT_INPUT_BYTES, None)
            return ()
        self._bytes_observed += len(chunk)
        return tuple(self._consume(chunk))

    def finish(self) -> tuple:
        if self._summary is not None:
            return ((), self._summary)
        if self._stopped:
            return ((), self._freeze(False))
        units = self._flush()
        return (tuple(units), self._freeze(not self._stopped))

    def close(self, reason: object) -> None:
        if type(reason) is not str or reason not in _CLOSE_REASONS:
            raise _ParserRefused(_CLOSE_RULE)
        if self._summary is not None:
            return
        self._stop(reason)
        self._freeze(False)

    def _freeze(self, complete: bool) -> _ImportSummary:
        unique: dict[tuple[object, object, object], _RowDiagnosticSnapshot] = {}
        for item in self._diagnostics:
            key = (item.code, item.field_reference, item.line_index)
            if key not in unique:
                unique[key] = item
        ordered = sorted(unique.values(), key=_diagnostic_key)
        self._discard_buffers()
        self._summary = _ImportSummary(
            complete=complete and not self._stopped,
            limit_reason=self._limit,
            header=self._header,
            lines_observed=self._lines_observed,
            units_emitted=self._units_emitted,
            units_refused=self._units_refused,
            bytes_observed=self._bytes_observed,
            diagnostics=tuple(ordered),
        )
        return self._summary

    def _emit(self, code: str, line_index: int | None) -> None:
        if self._stopped:
            return
        if len(self._diagnostics) >= self._max_diagnostics:
            self._stop(_LIMIT_DIAGNOSTICS)
            return
        self._diagnostics.append(
            _RowDiagnosticSnapshot(code=code, field_reference=None, line_index=line_index)
        )
        if len(self._diagnostics) >= self._max_diagnostics:
            self._stop(_LIMIT_DIAGNOSTICS)

    def _refuse(self, code: str, line_index: int | None) -> None:
        if self._stopped:
            return
        self._units_refused += 1
        self._halt(code, line_index)

    def _halt(self, code: str, line_index: int | None) -> None:
        if self._stopped:
            return
        self._emit(code, line_index)
        if not self._stopped:
            self._stop(code)

    def _stop(self, code: str) -> None:
        self._stopped = True
        self._limit = code
        self._discard_buffers()

    def _discard_buffers(self) -> None:
        """La base ne détient pas de contenu ; chaque format libère ses buffers."""
        return None

    def _check_rows_limit(self) -> bool:
        if self._data_rows_seen + 1 > self._policy["max_rows"]:
            self._halt(_LIMIT_ROWS, None)
            return False
        return True

    def _consume(self, data: bytes) -> list:
        raise _ParserRefused("méthode de parsing spécifique au format requise")

    def _flush(self) -> list:
        raise _ParserRefused("finalisation spécifique au format requise")


def _diagnostic_key(snapshot: _RowDiagnosticSnapshot) -> tuple:
    field = snapshot.field_reference
    line = snapshot.line_index
    return (
        snapshot.code,
        field is not None,
        field if field is not None else "",
        line is not None,
        line if line is not None else 0,
    )


class _CsvImportParser(_BulkImportParser):
    """Lexer CSV manuel déterministe : valeurs str brutes, sans conversion."""

    def __init__(self, mapping, policy, owner_fields) -> None:
        super().__init__(mapping, policy, owner_fields)
        self._state = _STATE_FIELD_START
        self._pending_cr = False
        self._row_active = False
        self._row_line = 0
        self._row_bytes = 0
        self._line = 0
        self._physical_line_start = True
        self._cells: list[bytes] = []
        self._cell = bytearray()
        self._prefix = bytearray()
        self._prefix_resolved = False
        self._source_set = frozenset(mapping.source_fields)
        self._required_set = frozenset(mapping.required_source_fields)
        self._bindings_order = tuple(mapping.field_bindings)
        self._header_index: dict[str, int] = {}
        self._emit_plan: tuple[tuple[str, int], ...] = ()

    def _consume(self, data: bytes) -> list:
        if not self._prefix_resolved:
            need = len(_BOM_PREFIX) - len(self._prefix)
            if len(data) < need:
                self._prefix.extend(data)
                return []
            self._prefix.extend(data[:need])
            if bytes(self._prefix) == _BOM_PREFIX:
                self._halt(_CSV_BOM_FORBIDDEN, 1)
                return []
            self._prefix_resolved = True
            data = bytes(self._prefix) + data[need:]
        return self._scan(data)

    def _scan(self, data: bytes) -> list:
        units: list = []
        for b in data:
            if self._stopped:
                return units
            if self._physical_line_start:
                self._lines_observed += 1
            self._physical_line_start = b == _LF
            if self._pending_cr:
                self._row_bytes += 1
                if self._row_bytes > self._policy["max_row_bytes"]:
                    self._halt(_LIMIT_ROW_BYTES, self._row_line)
                    return units
                self._pending_cr = False
                if b == _LF:
                    self._line += 1
                    self._finish_row(units)
                else:
                    self._refuse(_CSV_LONE_CR, self._row_line)
                continue
            if not self._row_active:
                self._begin_row()
            self._row_bytes += 1
            if self._row_bytes > self._policy["max_row_bytes"]:
                self._halt(_LIMIT_ROW_BYTES, self._row_line)
                return units
            if self._state == _STATE_FIELD_START:
                if b == _QUOTE:
                    self._state = _STATE_QUOTED
                elif b == _COMMA:
                    self._finish_cell()
                elif b == _LF:
                    self._finish_cell()
                    self._line += 1
                    self._finish_row(units)
                elif b == _CR:
                    self._finish_cell()
                    if not self._stopped:
                        self._pending_cr = True
                else:
                    self._cell.append(b)
                    self._state = _STATE_UNQUOTED
                continue
            if self._state == _STATE_UNQUOTED:
                if b == _QUOTE:
                    self._refuse(_CSV_QUOTE_MISUSE, self._row_line)
                elif b == _COMMA:
                    self._finish_cell()
                    self._state = _STATE_FIELD_START
                elif b == _LF:
                    self._finish_cell()
                    self._line += 1
                    self._finish_row(units)
                elif b == _CR:
                    self._finish_cell()
                    if not self._stopped:
                        self._pending_cr = True
                else:
                    self._cell.append(b)
                continue
            if self._state == _STATE_QUOTED:
                if b == _QUOTE:
                    self._state = _STATE_AFTER_QUOTE
                else:
                    self._cell.append(b)
                    if b == _LF:
                        self._line += 1
                continue
            if b == _QUOTE:
                self._cell.append(_QUOTE)
                self._state = _STATE_QUOTED
            elif b == _COMMA:
                self._finish_cell()
                self._state = _STATE_FIELD_START
            elif b == _LF:
                self._finish_cell()
                self._line += 1
                self._finish_row(units)
            elif b == _CR:
                self._finish_cell()
                self._pending_cr = True
            else:
                self._refuse(_CSV_QUOTE_MISUSE, self._row_line)
        return units

    def _flush(self) -> list:
        units: list = []
        if not self._prefix_resolved:
            self._prefix_resolved = True
            if self._prefix:
                units.extend(self._scan(bytes(self._prefix)))
        if self._stopped:
            return units
        if self._pending_cr:
            self._halt(_EOF_PARTIAL, self._row_line if self._row_active else None)
            return units
        if self._row_active:
            if self._state == _STATE_QUOTED:
                self._halt(_EOF_PARTIAL, self._row_line)
                return units
            self._finish_cell()
            if self._stopped:
                return units
            self._finish_row(units)
        elif self._header is None:
            self._halt(_CSV_HEADER_EMPTY, None)
        return units

    def _begin_row(self) -> None:
        self._row_active = True
        self._row_line = self._line + 1
        self._row_bytes = 0
        self._cells = []
        self._cell = bytearray()
        self._state = _STATE_FIELD_START

    def _reset_row(self) -> None:
        self._row_active = False
        self._pending_cr = False
        self._cells = []
        self._cell = bytearray()
        self._state = _STATE_FIELD_START

    def _finish_cell(self) -> None:
        if self._stopped:
            return
        if len(self._cells) + 1 > self._policy["max_columns"]:
            self._halt(_LIMIT_COLUMNS, self._row_line)
            return
        self._cells.append(bytes(self._cell))
        self._cell = bytearray()

    def _finish_row(self, units: list) -> None:
        if self._stopped:
            return
        cells = tuple(self._cells)
        row_line = self._row_line
        self._reset_row()
        if self._header is None:
            self._accept_header(cells)
        else:
            self._accept_data(units, cells, row_line)

    def _accept_header(self, cells: tuple[bytes, ...]) -> None:
        try:
            names = tuple(cell.decode("utf-8") for cell in cells)
        except UnicodeDecodeError:
            self._halt(_CSV_UTF8_INVALID, 1)
            return
        if any(not name for name in names):
            self._halt(_CSV_HEADER_EMPTY, 1)
            return
        header_set = frozenset(names)
        if len(header_set) != len(names):
            self._halt(_CSV_HEADER_DUPLICATE, 1)
            return
        if not header_set <= self._source_set:
            self._halt(_CSV_HEADER_UNKNOWN, 1)
            return
        if not self._required_set <= header_set:
            self._halt(_CSV_HEADER_INCOMPLETE, 1)
            return
        self._header = names
        self._header_index = {
            name: position for position, name in enumerate(names)
        }
        self._emit_plan = tuple(
            (target, self._header_index[source])
            for source, target in self._bindings_order
            if source in self._header_index
        )

    def _accept_data(
        self, units: list, cells: tuple[bytes, ...], row_line: int
    ) -> None:
        if not self._check_rows_limit():
            return
        if len(cells) > len(self._header):
            self._refuse(_CSV_EXTRA_COLUMN, row_line)
            return
        if len(cells) < len(self._header):
            self._refuse(_CSV_MISSING_COLUMN, row_line)
            return
        try:
            values = tuple(cell.decode("utf-8") for cell in cells)
        except UnicodeDecodeError:
            self._refuse(_CSV_UTF8_INVALID, row_line)
            return
        targets = tuple(
            (target, values[position]) for target, position in self._emit_plan
        )
        self._data_rows_seen += 1
        self._units_emitted += 1
        units.append(_CsvImportUnit(line_index=row_line, targets=targets))

    def _discard_buffers(self) -> None:
        self._prefix_resolved = True
        self._prefix = bytearray()
        self._cells = []
        self._cell = bytearray()
        self._pending_cr = False
        self._row_active = False
        self._state = _STATE_FIELD_START


_LCURLY = 123
_RCURLY = 125
_LSQUARE = 91
_RSQUARE = 93
_COLON = 58
_BSLASH = 92
_MINUS = 45
_VALUE_STARTS = (
    frozenset({_MINUS, 116, 102, 110}) | frozenset(range(48, 58))
)


def _json_prescan_limit(text: str, depth_limit: int, members_limit: int) -> str | None:
    """Borne structurelle avant décodeur: profondeur et membres par conteneur."""
    frames = []
    inside_string = False
    escaped = False
    root_seen = False
    for char in text:
        if inside_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                inside_string = False
            continue
        if char in " \t\r\n":
            continue
        if char in "}]":
            if not frames:
                return _NDJSON_SYNTAX_INVALID
            expected = "}" if frames[-1][0] == "{" else "]"
            if char != expected:
                return _NDJSON_SYNTAX_INVALID
            frames.pop()
            continue
        if char == ",":
            if frames and frames[-1][0] == "[":
                frames[-1][2] = True
            continue
        if char == ":":
            if frames and frames[-1][0] == "{":
                frames[-1][1] += 1
                if frames[-1][1] > members_limit:
                    return _LIMIT_JSON_MEMBERS
            continue
        if frames and frames[-1][0] == "[" and frames[-1][2]:
            frames[-1][1] += 1
            frames[-1][2] = False
            if frames[-1][1] > members_limit:
                return _LIMIT_JSON_MEMBERS
        if char == '"':
            inside_string = True
        elif char in "{[":
            if not frames and root_seen:
                return _NDJSON_SYNTAX_INVALID
            frames.append([char, 0, char == "["])
            if len(frames) > depth_limit:
                return _LIMIT_JSON_DEPTH
            root_seen = True
    if frames or inside_string:
        return _NDJSON_SYNTAX_INVALID
    return None


def _json_refusal_code(constraint: str) -> str:
    if constraint in _FLOAT_CONSTRAINTS:
        return _NDJSON_NONFINITE_FLOAT
    if constraint in _UNICODE_CONSTRAINTS:
        return _NDJSON_UTF8_INVALID
    if constraint in _DEPTH_CONSTRAINTS:
        return _LIMIT_JSON_DEPTH
    if constraint in _MEMBERS_CONSTRAINTS:
        return _LIMIT_JSON_MEMBERS
    return _NDJSON_SYNTAX_INVALID


class _NdjsonImportParser(_BulkImportParser):
    """Parseur NDJSON incrémental : bytes bornés, pré-scan puis décodage borné."""

    def __init__(self, mapping, policy, owner_fields) -> None:
        super().__init__(mapping, policy, owner_fields)
        self._buffer = bytearray()
        self._pending_cr = False
        self._line_active = False
        self._line = 0
        self._line_start = 1
        self._source_set = frozenset(mapping.source_fields)
        self._required_set = frozenset(mapping.required_source_fields)
        self._bindings_order = tuple(mapping.field_bindings)

    def _consume(self, data: bytes) -> list:
        units = []
        for byte in data:
            if self._stopped:
                break
            if not self._line_active:
                self._line_active = True
                self._line_start = self._line + 1
                self._lines_observed += 1
            if len(self._buffer) + 1 > self._policy["max_row_bytes"]:
                self._halt(_LIMIT_ROW_BYTES, self._line_start)
                break
            if byte == _LF:
                line_bytes = bytes(self._buffer)
                if line_bytes.endswith(b"\r"):
                    line_bytes = line_bytes[:-1]
                line_start = self._line_start
                self._buffer = bytearray()
                self._line_active = False
                self._line += 1
                self._line_start = self._line + 1
                self._complete_line(line_bytes, line_start, units)
            else:
                self._buffer.append(byte)
        return units

    def _flush(self) -> list:
        units = []
        if self._line_active:
            line_bytes = bytes(self._buffer)
            self._buffer = bytearray()
            self._line_active = False
            self._complete_line(line_bytes, self._line_start, units)
        return units

    def _complete_line(
        self, line_bytes: bytes, line_start: int, units: list
    ) -> None:
        try:
            text = line_bytes.decode("utf-8")
        except UnicodeDecodeError:
            self._refuse(_NDJSON_UTF8_INVALID, line_start)
            return
        significant = text.lstrip(" \t\r\n")
        if not significant:
            self._refuse(_NDJSON_EMPTY_LINE, line_start)
            return
        if significant[0] != "{":
            self._refuse(_NDJSON_SYNTAX_INVALID, line_start)
            return
        limit = _json_prescan_limit(
            text,
            self._policy["max_json_depth"],
            self._policy["max_json_members"],
        )
        if limit is not None:
            self._halt(limit, line_start)
            return
        try:
            record = json.loads(
                text,
                object_pairs_hook=_reject_duplicate_pairs,
                parse_constant=_reject_constant,
            )
        except _DuplicateKeyFound:
            self._refuse(_NDJSON_DUPLICATE_KEY, line_start)
            return
        except _ConstantFound:
            self._refuse(_NDJSON_CONSTANT_FORBIDDEN, line_start)
            return
        except RecursionError:
            self._refuse(_LIMIT_JSON_DEPTH, line_start)
            return
        except json.JSONDecodeError:
            self._refuse(_NDJSON_SYNTAX_INVALID, line_start)
            return
        except ValueError:
            self._refuse(_NDJSON_INT_REPRESENTATION_LIMIT, line_start)
            return
        self._accept_record(record, line_start, units)

    def _accept_record(
        self, record: object, line_start: int, units: list
    ) -> None:
        if type(record) is not dict:
            self._refuse(_NDJSON_SYNTAX_INVALID, line_start)
            return
        keys = tuple(record)
        if any(type(key) is not str for key in keys):
            self._refuse(_NDJSON_SYNTAX_INVALID, line_start)
            return
        if len(keys) > self._policy["max_columns"]:
            self._halt(_LIMIT_COLUMNS, line_start)
            return
        key_set = frozenset(keys)
        if not key_set <= self._source_set:
            self._refuse(_NDJSON_UNKNOWN_FIELD, line_start)
            return
        if not self._required_set <= key_set:
            self._refuse(_NDJSON_MISSING_REQUIRED, line_start)
            return
        refusals = validate_json_value(
            record,
            max_depth=self._policy["max_json_depth"],
            max_members=self._policy["max_json_members"],
        )
        if refusals:
            self._refuse(_json_refusal_code(refusals[0].constraint), line_start)
            return
        targets = tuple(
            (target, _copy_json_value(record[source]))
            for source, target in self._bindings_order
            if source in record
        )
        if not self._check_rows_limit():
            return
        self._data_rows_seen += 1
        self._units_emitted += 1
        units.append(_NdjsonImportUnit(line_index=line_start, targets=targets))

    def _discard_buffers(self) -> None:
        self._buffer = bytearray()
        self._pending_cr = False
        self._line_active = False
