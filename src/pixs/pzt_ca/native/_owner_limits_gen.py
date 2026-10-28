#!/usr/bin/env python3
"""Producteur public de construction des bornes proprietaire."""
from __future__ import annotations

import hashlib
import json
import os
import sys

from ._admin_profile_gen import (
    _Refuse,
    _StrictParser,
    _close_keep,
    _open_output_directory,
    _pairs_no_duplicate,
    _read_input,
    _reject_constant,
    _write_output,
)


INPUT_OBJECT_TYPE = "z12.owner_limits_data/v1"
INPUT_SCHEMA_VERSION = "1.0.0"
INPUT_DOMAIN = "pixs.z12.owner.limits/v1"
EXPECTED_FIELDS = frozenset(
    [
        "object_type",
        "schema_version",
        "identity_ref",
        "domain",
        "version",
        "image_exe_max_bytes",
        "procmetadata_max_bytes",
        "unit_path_max_bytes",
        "unit_name_max_bytes",
        "fixture",
    ]
)
DEFAULT_MAX_INPUT_BYTES = 8192
MIN_MAX_INPUT_BYTES = 1024
MAX_MAX_INPUT_BYTES = 65536
OWNER_TEXT_MAX_BYTES = 256
HEADER_FINAL_NAME = "z12_owner_limits.inc"
MANIFEST_FINAL_NAME = "z12_owner_limits.manifest.json"
MANIFEST_OBJECT_TYPE = "z12.owner_limits_manifest/v1"
GENERATOR_REFERENCE = "_owner_limits_gen.py/v1"


def _build_parser():
    """Construit l analyseur strict des options de construction."""
    parser = _StrictParser(prog="_owner_limits_gen.py")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--procedure-ref", required=True)
    parser.add_argument(
        "--max-input-bytes", type=int, default=DEFAULT_MAX_INPUT_BYTES
    )
    return parser


def _check_text_bytes(value: object, limit: int) -> bytes:
    """Controle UTF8 exact sans NUL dans la borne octets."""
    if type(value) is not str:
        raise _Refuse("ERR_FIELD_TEXT_TYPE")
    try:
        encoded = value.encode("utf-8")
    except UnicodeError:
        raise _Refuse("ERR_FIELD_TEXT_ENCODING")
    if len(encoded) < 1 or len(encoded) > limit:
        raise _Refuse("ERR_FIELD_TEXT_RANGE")
    if b"\x00" in encoded:
        raise _Refuse("ERR_FIELD_TEXT_NUL")
    return encoded


def _check_exact_string(value: object, expected: str) -> str:
    """Controle egalite stricte de chaine."""
    if type(value) is not str or value != expected:
        raise _Refuse("ERR_FIELD_VALUE")
    return expected


def _check_u32(value: object) -> int:
    """Controle entier exact u32 positif non bool."""
    if type(value) is not int:
        raise _Refuse("ERR_FIELD_INT_TYPE")
    if value < 1 or value > 0xFFFFFFFF:
        raise _Refuse("ERR_FIELD_INT_RANGE")
    return value


def _parse_input(raw_bytes: bytes) -> dict[str, object]:
    """Analyse JSON ferme sans doublon ni constante."""
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeError:
        raise _Refuse("ERR_JSON_ENCODING")
    try:
        document = json.loads(
            text,
            object_pairs_hook=_pairs_no_duplicate,
            parse_constant=_reject_constant,
        )
    except RecursionError:
        raise _Refuse("ERR_JSON_DEPTH")
    except ValueError:
        raise _Refuse("ERR_JSON_INVALID")
    if type(document) is not dict:
        raise _Refuse("ERR_JSON_TOP")
    if set(document.keys()) != set(EXPECTED_FIELDS):
        raise _Refuse("ERR_JSON_FIELDS")
    return document


def _fsync_directory(directory_fd: int) -> None:
    """Synchronise le repertoire de sortie."""
    try:
        os.fsync(directory_fd)
    except OSError:
        raise _Refuse("ERR_DIR_FSYNC")


def _format_byte_list(data: bytes) -> str:
    """Forme la liste numerique d octets pour le header."""
    return ", ".join("0x%02x" % item for item in data)


def _render_header(
    identity_bytes: bytes,
    domain_bytes: bytes,
    version_bytes: bytes,
    image_exe_max: int,
    procmetadata_max: int,
    unit_path_max: int,
    unit_name_max: int,
    fixture_flag: bool,
) -> bytes:
    """Construit le header de construction."""
    lines = [
        "/* Genere _owner_limits_gen.py */",
        "#pragma once",
        "#define Z12_OWNER_IMAGE_EXE_MAX %du" % image_exe_max,
        "#define Z12_OWNER_PROCMETA_MAX %du" % procmetadata_max,
        "#define Z12_OWNER_UNIT_PATH_MAX %du" % unit_path_max,
        "#define Z12_OWNER_UNIT_NAME_MAX %du" % unit_name_max,
        "#define Z12_OWNER_LIMITS_FIXTURE %d" % (1 if fixture_flag else 0),
        "#define Z12_OWNER_LIMITS_IDENTITY_LEN %du" % len(identity_bytes),
        "static const unsigned char Z12_OWNER_LIMITS_IDENTITY_BYTES[%d] = {%s};"
        % (len(identity_bytes), _format_byte_list(identity_bytes)),
        "#define Z12_OWNER_LIMITS_DOMAIN_LEN %du" % len(domain_bytes),
        "static const unsigned char Z12_OWNER_LIMITS_DOMAIN_BYTES[%d] = {%s};"
        % (len(domain_bytes), _format_byte_list(domain_bytes)),
        "#define Z12_OWNER_LIMITS_VERSION_LEN %du" % len(version_bytes),
        "static const unsigned char Z12_OWNER_LIMITS_VERSION_BYTES[%d] = {%s};"
        % (len(version_bytes), _format_byte_list(version_bytes)),
        "",
    ]
    try:
        return ("\n".join(lines)).encode("utf-8")
    except UnicodeError:
        raise _Refuse("ERR_INTERNAL_ENCODE")


def _render_manifest(
    identity_ref: str,
    domain_name: str,
    version_name: str,
    procedure_ref: str,
    image_exe_max: int,
    procmetadata_max: int,
    unit_path_max: int,
    unit_name_max: int,
    fixture_flag: bool,
    input_sha256: str,
    header_sha256: str,
) -> bytes:
    """Construit le manifeste declaratif."""
    manifest = {
        "manifest": MANIFEST_OBJECT_TYPE,
        "identity_ref": identity_ref,
        "domain": domain_name,
        "version": version_name,
        "procedure_ref": procedure_ref,
        "image_exe_max_bytes": image_exe_max,
        "procmetadata_max_bytes": procmetadata_max,
        "unit_path_max_bytes": unit_path_max,
        "unit_name_max_bytes": unit_name_max,
        "fixture": fixture_flag,
        "generator": GENERATOR_REFERENCE,
        "input_sha256": input_sha256,
        "header_sha256": header_sha256,
        "outputs": [HEADER_FINAL_NAME, MANIFEST_FINAL_NAME],
    }
    try:
        return (
            json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n"
        ).encode("utf-8")
    except (ValueError, UnicodeError):
        raise _Refuse("ERR_INTERNAL_ENCODE")


def _run(argv: list[str] | None) -> int:
    """Execute la production sans effet import."""
    options = _build_parser().parse_args(argv)
    if (
        type(options.input) is not str
        or type(options.out_dir) is not str
        or type(options.procedure_ref) is not str
    ):
        raise _Refuse("ERR_ARGS_INVALID")
    if (
        type(options.max_input_bytes) is not int
        or options.max_input_bytes < MIN_MAX_INPUT_BYTES
        or options.max_input_bytes > MAX_MAX_INPUT_BYTES
    ):
        raise _Refuse("ERR_MAX_INPUT_RANGE")
    procedure_ref = options.procedure_ref
    _check_text_bytes(procedure_ref, OWNER_TEXT_MAX_BYTES)
    input_bytes = _read_input(options.input, options.max_input_bytes)
    document = _parse_input(input_bytes)
    _check_exact_string(document["object_type"], INPUT_OBJECT_TYPE)
    _check_exact_string(document["schema_version"], INPUT_SCHEMA_VERSION)
    identity_bytes = _check_text_bytes(
        document["identity_ref"], OWNER_TEXT_MAX_BYTES
    )
    _check_exact_string(document["domain"], INPUT_DOMAIN)
    version_bytes = _check_text_bytes(
        document["version"], OWNER_TEXT_MAX_BYTES
    )
    image_exe_max = _check_u32(document["image_exe_max_bytes"])
    procmetadata_max = _check_u32(document["procmetadata_max_bytes"])
    unit_path_max = _check_u32(document["unit_path_max_bytes"])
    unit_name_max = _check_u32(document["unit_name_max_bytes"])
    if type(document["fixture"]) is not bool:
        raise _Refuse("ERR_FIXTURE_TYPE")
    fixture_flag = document["fixture"]
    identity_ref = identity_bytes.decode("utf-8")
    version_name = version_bytes.decode("utf-8")
    domain_bytes = INPUT_DOMAIN.encode("ascii")
    header_bytes = _render_header(
        identity_bytes,
        domain_bytes,
        version_bytes,
        image_exe_max,
        procmetadata_max,
        unit_path_max,
        unit_name_max,
        fixture_flag,
    )
    input_sha256 = hashlib.sha256(input_bytes).hexdigest()
    header_sha256 = hashlib.sha256(header_bytes).hexdigest()
    manifest_bytes = _render_manifest(
        identity_ref,
        INPUT_DOMAIN,
        version_name,
        procedure_ref,
        image_exe_max,
        procmetadata_max,
        unit_path_max,
        unit_name_max,
        fixture_flag,
        input_sha256,
        header_sha256,
    )
    directory_fd = _open_output_directory(options.out_dir)
    try:
        try:
            _write_output(
                directory_fd, HEADER_FINAL_NAME, header_bytes
            )
            _fsync_directory(directory_fd)
            _write_output(
                directory_fd, MANIFEST_FINAL_NAME, manifest_bytes
            )
            _fsync_directory(directory_fd)
        except _Refuse:
            sys.stderr.write("ERR_PAIR_PARTIAL\n")
            raise
    finally:
        _close_keep(
            directory_fd, "ERR_DIR_CLOSE", sys.exc_info()[1]
        )
    return 0


def main(argv: list[str] | None = None) -> int:
    """Frontiere CLI sans traceback ni echo candidat."""
    try:
        return _run(argv)
    except _Refuse as refusal:
        sys.stderr.write(refusal.code + "\n")
        return 2
    except (OSError, ValueError, UnicodeError, RecursionError):
        sys.stderr.write("ERR_INTERNAL\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
