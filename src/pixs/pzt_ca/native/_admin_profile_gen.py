#!/usr/bin/env python3
"""Pin administratif compile Z12, producteur public de build."""
from __future__ import annotations

import argparse
import errno
import hashlib
import json
import os
import stat
import sys


INPUT_OBJECT_TYPE = "z12.admin_profile_data/v1"
INPUT_SCHEMA_VERSION = "1.0.0"
INPUT_DOMAIN = "pixs.z12.admin/v1"
EXPECTED_FIELDS = frozenset(
    [
        "object_type",
        "schema_version",
        "identity_ref",
        "domain",
        "version",
        "public_key_hex",
        "max_payload_len",
        "max_field_len",
        "budget_ns",
        "fixture",
    ]
)
DEFAULT_MAX_INPUT_BYTES = 8192
MIN_MAX_INPUT_BYTES = 1024
MAX_MAX_INPUT_BYTES = 65536
READ_CHUNK_SIZE = 8192
HEADER_FINAL_NAME = "z12_admin_profile.inc"
MANIFEST_FINAL_NAME = "z12_admin_profile.manifest.json"
MANIFEST_OBJECT_TYPE = "z12.admin_profile_manifest/v1"
GENERATOR_REFERENCE = "_admin_profile_gen.py/v1"
TEXT_MAX_BYTES = 256


class _Refuse(Exception):
    """Refus fixe, converti en code sortie par la frontiere CLI."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


class _StrictParser(argparse.ArgumentParser):
    def error(self, message: object) -> None:
        self.exit(2, "ERR_ARGS_INVALID\n")


def _build_parser() -> argparse.ArgumentParser:
    parser = _StrictParser(prog="_admin_profile_gen.py")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--procedure-ref", required=True)
    parser.add_argument(
        "--max-input-bytes", type=int, default=DEFAULT_MAX_INPUT_BYTES
    )
    return parser


def _close_keep(file_descriptor: int, code: str, active: object) -> None:
    try:
        os.close(file_descriptor)
    except OSError:
        sys.stderr.write(code + "\n")
        if active is None:
            raise _Refuse(code)


def _check_text_bytes(value: object, limit: int) -> bytes:
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
    if type(value) is not str or value != expected:
        raise _Refuse("ERR_FIELD_VALUE")
    return expected


def _check_public_key(value: object) -> bytes:
    if type(value) is not str:
        raise _Refuse("ERR_PUBKEY_TYPE")
    if len(value) != 64:
        raise _Refuse("ERR_PUBKEY_LENGTH")
    for character in value:
        if not (("0" <= character <= "9") or ("a" <= character <= "f")):
            raise _Refuse("ERR_PUBKEY_HEX")
    try:
        raw_key = bytes.fromhex(value)
    except ValueError:
        raise _Refuse("ERR_PUBKEY_HEX")
    if raw_key == bytes(32):
        raise _Refuse("ERR_PUBKEY_ZERO")
    return raw_key


def _check_u32(value: object) -> int:
    if type(value) is not int:
        raise _Refuse("ERR_FIELD_INT_TYPE")
    if value < 1 or value > 0xFFFFFFFF:
        raise _Refuse("ERR_FIELD_INT_RANGE")
    return value


def _check_u64(value: object) -> int:
    if type(value) is not int:
        raise _Refuse("ERR_FIELD_INT_TYPE")
    if value < 1 or value > 0xFFFFFFFFFFFFFFFF:
        raise _Refuse("ERR_FIELD_INT_RANGE")
    return value


def _reject_constant(raw: str) -> None:
    raise ValueError("const")


def _pairs_no_duplicate(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, item in pairs:
        if type(key) is not str:
            raise ValueError("cle")
        if key in result:
            raise ValueError("doublon")
        result[key] = item
    return result


def _read_input(input_path: str, limit: int) -> bytes:
    if type(input_path) is not str or not input_path:
        raise _Refuse("ERR_INPUT_OPEN")
    try:
        input_fd = os.open(
            input_path,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK,
        )
    except (OSError, ValueError):
        raise _Refuse("ERR_INPUT_OPEN")
    try:
        try:
            first_stat = os.fstat(input_fd)
        except OSError:
            raise _Refuse("ERR_INPUT_FSTAT")
        if not stat.S_ISREG(first_stat.st_mode):
            raise _Refuse("ERR_INPUT_NOT_REGULAR")
        expected_size = first_stat.st_size
        expected_mtime = first_stat.st_mtime_ns
        expected_ctime = first_stat.st_ctime_ns
        expected_dev = first_stat.st_dev
        expected_ino = first_stat.st_ino
        if expected_size <= 0 or expected_size > limit:
            raise _Refuse("ERR_INPUT_SIZE")
        output = bytearray()
        while len(output) < expected_size:
            try:
                chunk = os.read(
                    input_fd, min(READ_CHUNK_SIZE, expected_size - len(output))
                )
            except OSError:
                raise _Refuse("ERR_INPUT_READ")
            if not chunk:
                raise _Refuse("ERR_INPUT_TRUNCATED")
            output.extend(chunk)
            if len(output) > limit:
                raise _Refuse("ERR_INPUT_TOO_LARGE")
        try:
            tail = os.read(input_fd, 1)
        except OSError:
            raise _Refuse("ERR_INPUT_READ")
        if tail != b"":
            raise _Refuse("ERR_INPUT_GROWN")
        try:
            last_stat = os.fstat(input_fd)
        except OSError:
            raise _Refuse("ERR_INPUT_FSTAT")
        if (
            last_stat.st_dev,
            last_stat.st_ino,
            last_stat.st_size,
            last_stat.st_mtime_ns,
            last_stat.st_ctime_ns,
        ) != (expected_dev, expected_ino, expected_size, expected_mtime, expected_ctime):
            raise _Refuse("ERR_INPUT_CHANGED")
        return bytes(output)
    finally:
        _close_keep(input_fd, "ERR_INPUT_CLOSE", sys.exc_info()[1])


def _parse_input(raw_bytes: bytes) -> dict[str, object]:
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeError:
        raise _Refuse("ERR_JSON_ENCODING")
    try:
        parsed = json.loads(
            text,
            object_pairs_hook=_pairs_no_duplicate,
            parse_constant=_reject_constant,
        )
    except RecursionError:
        raise _Refuse("ERR_JSON_DEPTH")
    except ValueError:
        raise _Refuse("ERR_JSON_INVALID")
    if type(parsed) is not dict:
        raise _Refuse("ERR_JSON_TOP")
    if set(parsed.keys()) != set(EXPECTED_FIELDS):
        raise _Refuse("ERR_JSON_FIELDS")
    return parsed


def _open_output_directory(output_path: str) -> int:
    if type(output_path) is not str or not output_path:
        raise _Refuse("ERR_OUTDIR_OPEN")
    try:
        directory_fd = os.open(
            output_path,
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
        )
    except (OSError, ValueError):
        raise _Refuse("ERR_OUTDIR_OPEN")
    try:
        directory_stat = os.fstat(directory_fd)
    except OSError:
        _close_keep(directory_fd, "ERR_DIR_CLOSE", sys.exc_info()[1])
        raise _Refuse("ERR_OUTDIR_FSTAT")
    if not stat.S_ISDIR(directory_stat.st_mode):
        _close_keep(directory_fd, "ERR_DIR_CLOSE", sys.exc_info()[1])
        raise _Refuse("ERR_OUTDIR_NOT_DIR")
    return directory_fd


def _fsync_directory(directory_fd: int) -> None:
    try:
        os.fsync(directory_fd)
    except OSError:
        raise _Refuse("ERR_DIR_FSYNC")


def _write_output(directory_fd: int, file_name: str, data: bytes) -> None:
    try:
        file_fd = os.open(
            file_name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
            0o600,
            dir_fd=directory_fd,
        )
    except (OSError, ValueError) as error:
        if isinstance(error, OSError) and error.errno == errno.EEXIST:
            raise _Refuse("ERR_FINAL_EXISTS")
        raise _Refuse("ERR_OUTPUT_CREATE")
    try:
        offset = 0
        while offset < len(data):
            try:
                written = os.write(file_fd, data[offset:])
            except OSError:
                raise _Refuse("ERR_OUTPUT_WRITE")
            if written <= 0:
                raise _Refuse("ERR_OUTPUT_WRITE")
            offset += written
        try:
            os.fsync(file_fd)
        except OSError:
            raise _Refuse("ERR_OUTPUT_FSYNC")
    finally:
        _close_keep(file_fd, "ERR_OUTPUT_CLOSE", sys.exc_info()[1])


def _format_byte_list(data: bytes) -> str:
    return ", ".join("0x%02x" % item for item in data)


def _render_header(
    identity_bytes: bytes,
    domain_bytes: bytes,
    version_bytes: bytes,
    public_key_bytes: bytes,
    max_payload_len: int,
    max_field_len: int,
    budget_ns: int,
    fixture_flag: bool,
) -> bytes:
    lines = [
        "/* Genere _admin_profile_gen.py */",
        "#pragma once",
        "#define Z12_ADMIN_IDENTITY_LEN %du" % len(identity_bytes),
        "static const unsigned char kZ12AdminIdentity[%d] = {%s};"
        % (len(identity_bytes), _format_byte_list(identity_bytes)),
        "#define Z12_ADMIN_DOMAIN_LEN %du" % len(domain_bytes),
        "static const unsigned char kZ12AdminDomain[%d] = {%s};"
        % (len(domain_bytes), _format_byte_list(domain_bytes)),
        "#define Z12_ADMIN_VERSION_LEN %du" % len(version_bytes),
        "static const unsigned char kZ12AdminVersion[%d] = {%s};"
        % (len(version_bytes), _format_byte_list(version_bytes)),
        "#define Z12_ADMIN_PUBKEY_LEN 32u",
        "static const unsigned char kZ12AdminPubkey[32] = {%s};"
        % _format_byte_list(public_key_bytes),
        "#define Z12_ADMIN_MAX_PAYLOAD_LEN %du" % max_payload_len,
        "#define Z12_ADMIN_MAX_FIELD_LEN %du" % max_field_len,
        "#define Z12_ADMIN_BUDGET_NS %dULL" % budget_ns,
        "#define Z12_ADMIN_FIXTURE %d" % (1 if fixture_flag else 0),
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
    public_key_hex: str,
    public_key_bytes: bytes,
    max_payload_len: int,
    max_field_len: int,
    budget_ns: int,
    fixture_flag: bool,
    input_sha256: str,
    header_sha256: str,
) -> bytes:
    manifest = {
        "manifest": MANIFEST_OBJECT_TYPE,
        "identity_ref": identity_ref,
        "domain": domain_name,
        "version": version_name,
        "procedure_ref": procedure_ref,
        "public_key_hex": public_key_hex,
        "public_key_sha256": hashlib.sha256(public_key_bytes).hexdigest(),
        "max_payload_len": max_payload_len,
        "max_field_len": max_field_len,
        "budget_ns": budget_ns,
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
    _check_text_bytes(procedure_ref, TEXT_MAX_BYTES)
    input_bytes = _read_input(options.input, options.max_input_bytes)
    document = _parse_input(input_bytes)
    _check_exact_string(document["object_type"], INPUT_OBJECT_TYPE)
    _check_exact_string(document["schema_version"], INPUT_SCHEMA_VERSION)
    identity_bytes = _check_text_bytes(document["identity_ref"], TEXT_MAX_BYTES)
    _check_exact_string(document["domain"], INPUT_DOMAIN)
    version_bytes = _check_text_bytes(document["version"], TEXT_MAX_BYTES)
    public_key_bytes = _check_public_key(document["public_key_hex"])
    max_payload_len = _check_u32(document["max_payload_len"])
    max_field_len = _check_u32(document["max_field_len"])
    if max_field_len > max_payload_len:
        raise _Refuse("ERR_BOUNDS_ORDER")
    budget_ns = _check_u64(document["budget_ns"])
    if type(document["fixture"]) is not bool:
        raise _Refuse("ERR_FIXTURE_TYPE")
    fixture_flag = document["fixture"]
    identity_ref = identity_bytes.decode("utf-8")
    version_name = version_bytes.decode("utf-8")
    public_key_hex = public_key_bytes.hex()
    domain_bytes = INPUT_DOMAIN.encode("ascii")
    header_bytes = _render_header(
        identity_bytes,
        domain_bytes,
        version_bytes,
        public_key_bytes,
        max_payload_len,
        max_field_len,
        budget_ns,
        fixture_flag,
    )
    input_sha256 = hashlib.sha256(input_bytes).hexdigest()
    header_sha256 = hashlib.sha256(header_bytes).hexdigest()
    manifest_bytes = _render_manifest(
        identity_ref,
        INPUT_DOMAIN,
        version_name,
        procedure_ref,
        public_key_hex,
        public_key_bytes,
        max_payload_len,
        max_field_len,
        budget_ns,
        fixture_flag,
        input_sha256,
        header_sha256,
    )
    directory_fd = _open_output_directory(options.out_dir)
    try:
        try:
            _write_output(directory_fd, HEADER_FINAL_NAME, header_bytes)
            _fsync_directory(directory_fd)
            _write_output(directory_fd, MANIFEST_FINAL_NAME, manifest_bytes)
            _fsync_directory(directory_fd)
        except _Refuse:
            sys.stderr.write("ERR_PAIR_PARTIAL\n")
            raise
    finally:
        _close_keep(directory_fd, "ERR_DIR_CLOSE", sys.exc_info()[1])
    return 0


def main(argv: list[str] | None = None) -> int:
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
