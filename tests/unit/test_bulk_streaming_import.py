"""Parsing IMPORT : corpus normatif synthétique et toutes frontières de segments."""

import csv
import sys
import unittest
from dataclasses import FrozenInstanceError
from unittest import mock

import pixs.backend.bulk_streaming_import as runtime
import pixs.backend.bulk_runtime_contracts as contracts
from pixs.kernel.diagnostics import Diagnostic, VALIDATE
from unit.test_bulk_runtime_contracts import (
    _mapping, _FIELDS, _Hostile, _ForeignDict, _ForeignList,
    _ForeignTuple, _ForeignStr, _ForeignInt, _HashOnce,
)
from unit.test_bulk_execution_values import _valid_policy


class _ForeignBytes(bytes):
    def __len__(self):
        raise AssertionError("foreign byte length")

    def decode(self, *args, **kwargs):
        raise AssertionError("foreign byte decoder")

    def __bool__(self):
        raise AssertionError("foreign byte bool")


def _new(fmt="CSV", *, mapping_updates=None, policy_updates=None, fields=_FIELDS):
    mapping = _mapping()
    mapping["format"] = fmt
    if mapping_updates:
        mapping.update(mapping_updates)
    policy = _valid_policy()
    if policy_updates:
        policy.update(policy_updates)
    parser, refusals = runtime.new_bulk_import_parser(
        mapping=mapping, policy=policy, declared_owner_fields=fields,
        declared_codes=runtime._CONTENT_CODES,
    )
    if refusals:
        raise AssertionError("valid synthetic parser declarations refused")
    return parser


def _run(data, fmt="CSV", *, parts=None, mapping_updates=None, policy_updates=None):
    parser = _new(fmt, mapping_updates=mapping_updates, policy_updates=policy_updates)
    units = []
    chunks = (data,) if parts is None else parts
    for chunk in chunks:
        units.extend(parser.feed(chunk))
    last, summary = parser.finish()
    units.extend(last)
    return parser, units, summary


def _summary_values(summary):
    return summary.as_values()


class BulkStreamingImportTests(unittest.TestCase):
    def assert_summary_safe(self, summary):
        values = _summary_values(summary)
        self.assertIs(type(values), dict)
        self.assertIs(type(values["complete"]), bool)
        self.assertIs(type(values["diagnostics"]), tuple)
        for diagnostic in values["diagnostics"]:
            self.assertIs(type(diagnostic), dict)
            self.assertEqual(set(diagnostic), {"code", "field_reference", "line_index"})
            self.assertIn(diagnostic["code"], runtime._CONTENT_CODES)
            self.assertTrue(diagnostic["field_reference"] is None or diagnostic["field_reference"] in _FIELDS)
            self.assertTrue(diagnostic["line_index"] is None or (
                type(diagnostic["line_index"]) is int and diagnostic["line_index"] >= 1
            ))
            self.assertNotIn("LEAK-MARKER", str(diagnostic))
        return values

    def assert_content_refused(self, data, fmt="CSV", **kwargs):
        _parser, _units, summary = _run(data, fmt, **kwargs)
        values = self.assert_summary_safe(summary)
        self.assertFalse(values["complete"])
        self.assertTrue(values["diagnostics"] or values["limit_reason"])

    def test_exports_only_factory(self):
        self.assertEqual(runtime.__all__, ["new_bulk_import_parser"])

    def test_csv_unicode_quotes_multiline_crlf(self):
        data = 'source_name,source_count\r\né,12\r\n"a,b","""x"""\r\n"multi\r\nline",""\r\n'.encode()
        _parser, units, summary = _run(data)
        self.assertEqual([unit.as_values() for unit in units], [
            {"name": "é", "count": "12"},
            {"name": "a,b", "count": '"x"'},
            {"name": "multi\r\nline", "count": ""},
        ])
        self.assertEqual([unit.line_index for unit in units], [2, 3, 4])
        values = self.assert_summary_safe(summary)
        self.assertTrue(values["complete"])
        self.assertEqual(values["units_emitted"], 3)
        self.assertEqual(values["units_refused"], 0)
        self.assertEqual(values["bytes_observed"], len(data))

    def test_csv_all_two_way_byte_boundaries(self):
        data = 'source_name,source_count\r\n"é😀","a,""b"""\r\n"x\r\ny",001'.encode()
        expected = [{"name": "é😀", "count": 'a,"b"'}, {"name": "x\r\ny", "count": "001"}]
        for split in range(len(data) + 1):
            with self.subTest(split=split):
                _parser, units, summary = _run(data, parts=(data[:split], data[split:]))
                self.assertEqual([unit.as_values() for unit in units], expected)
                self.assertTrue(self.assert_summary_safe(summary)["complete"])

    def test_csv_every_fixed_chunk_size_and_empty_chunks(self):
        data = 'source_name,source_count\n"é","""v"""\n'.encode()
        for size in range(1, len(data) + 1):
            parts = [b""]
            parts.extend(data[index:index+size] for index in range(0, len(data), size))
            parts.append(b"")
            _parser, units, summary = _run(data, parts=parts)
            self.assertEqual([unit.as_values() for unit in units], [{"name": "é", "count": '"v"'}])
            self.assertTrue(_summary_values(summary)["complete"])

    def test_csv_no_final_lf_is_returned_by_finish(self):
        parser = _new()
        emitted = parser.feed(b"source_name,source_count\nalice,001")
        self.assertEqual(emitted, ())
        last, summary = parser.finish()
        self.assertEqual([unit.as_values() for unit in last], [{"name": "alice", "count": "001"}])
        self.assertTrue(_summary_values(summary)["complete"])

    def test_csv_optional_column_absent_has_no_bulk_default(self):
        _parser, units, summary = _run(b"source_name\nalice\n")
        self.assertEqual([unit.as_values() for unit in units], [{"name": "alice"}])
        self.assertTrue(_summary_values(summary)["complete"])

    def test_csv_preserves_strings_spaces_empty_and_numeric_text(self):
        data = b"source_name,source_count\n alice ,001\nfalse,\n"
        _parser, units, summary = _run(data)
        self.assertEqual([unit.as_values() for unit in units], [
            {"name": " alice ", "count": "001"}, {"name": "false", "count": ""},
        ])
        self.assertTrue(_summary_values(summary)["complete"])

    def test_csv_header_invalid_cases(self):
        for data in (
            b"\n", b"source_name,source_name\nalice,1\n",
            b"source_name,\nalice,1\n",
            b"source_name,LEAK-MARKER\nalice,1\n",
            b"source_count\n1\n",
        ):
            self.assert_content_refused(data)

    def test_csv_cardinality_and_quote_misuse_refused(self):
        for row in (
            b"alice,1,LEAK-MARKER\n", b"alice\n",
            b'LEAK"MARKER,1\n', b'"alice"x,1\n',
        ):
            self.assert_content_refused(b"source_name,source_count\n" + row)

    def test_csv_bare_cr_and_partial_eof_refused(self):
        for data in (
            b"source_name,source_count\ralice,1\r",
            b'source_name,source_count\n"LEAK-MARKER,1',
            b"source_name,source_count\r",
        ):
            self.assert_content_refused(data)

    def test_csv_utf8_and_bom_refused(self):
        for data in (
            b"\xef\xbb\xbfsource_name,source_count\nalice,1\n",
            b"source_name,source_count\nLEAK-MARKER,\xff\n",
            b"source_name,source_count\nalice,\xe2",
        ):
            self.assert_content_refused(data)

    def test_ndjson_types_and_last_line_without_lf(self):
        data = b'{"source_name":"alice","source_count":1}\n{"source_name":"","source_count":null}'
        _parser, units, summary = _run(data, "NDJSON")
        self.assertEqual([unit.as_values() for unit in units], [
            {"name": "alice", "count": 1}, {"name": "", "count": None},
        ])
        self.assertEqual([unit.line_index for unit in units], [1, 2])
        self.assertTrue(_summary_values(summary)["complete"])

    def test_ndjson_all_byte_boundaries_and_crlf(self):
        data = '{"source_name":"é😀","source_count":false}\r\n{"source_name":"x"}\n'.encode()
        expected = [{"name": "é😀", "count": False}, {"name": "x"}]
        for split in range(len(data) + 1):
            _parser, units, summary = _run(data, "NDJSON", parts=(data[:split], data[split:]))
            self.assertEqual([unit.as_values() for unit in units], expected)
            self.assertTrue(_summary_values(summary)["complete"])

    def test_ndjson_empty_string_nul_and_nested_values(self):
        data = b'{"source_name":"\\u0000","source_count":{"x":[true,0,""]}}\n'
        _parser, units, summary = _run(data, "NDJSON")
        self.assertEqual([unit.as_values() for unit in units], [
            {"name": "\x00", "count": {"x": [True, 0, ""]}},
        ])
        self.assertTrue(_summary_values(summary)["complete"])

    def test_ndjson_empty_lines_and_nonobjects_refused(self):
        for data in (b"\n", b" \t\n", b'["LEAK-MARKER"]\n', b"null\n", b"1\n"):
            self.assert_content_refused(data, "NDJSON")

    def test_ndjson_duplicate_keys_all_depths_refused(self):
        for data in (
            b'{"source_name":"alice","source_name":"LEAK-MARKER"}\n',
            b'{"source_name":{"x":1,"x":2}}\n',
        ):
            self.assert_content_refused(data, "NDJSON")

    def test_ndjson_nonfinite_constants_and_overflow_refused(self):
        for number in (b"NaN", b"Infinity", b"-Infinity", b"1e999"):
            self.assert_content_refused(b'{"source_name":' + number + b"}\n", "NDJSON")

    def test_ndjson_unicode_utf16_bom_invalid_and_extra_document_refused(self):
        for data in (
            b'{"source_name":"\\ud800"}\n',
            b'\xef\xbb\xbf{"source_name":"alice"}\n',
            b'{"source_name":"LEAK-MARKER\xff"}\n',
            '{"source_name":"alice"}\n'.encode("utf-16"),
            b'{"source_name":"alice"} {"source_name":"LEAK-MARKER"}\n',
            b'{"source_name":',
        ):
            self.assert_content_refused(data, "NDJSON")

    def test_ndjson_no_raw_cr_or_unicode_whitespace_normalization(self):
        for data in (
            b'{"source_name":"LEAK-MARKER\rX"}\n',
            '\u00a0{"source_name":"alice"}\n'.encode("utf-8"),
        ):
            self.assert_content_refused(data, "NDJSON")

    def test_ndjson_arrays_members_bound_before_decoder(self):
        parser = _new("NDJSON", policy_updates={"max_json_members": 2})
        with mock.patch.object(runtime.json, "loads", side_effect=AssertionError("array decoded beyond bound")):
            self.assertEqual(parser.feed(b'{"source_name":[1,2,3]}\n'), ())
            _last, summary = parser.finish()
        self.assertFalse(self.assert_summary_safe(summary)["complete"])

    def test_ndjson_unknown_and_missing_required_fields_refused(self):
        for data in (b'{"LEAK-MARKER":1}\n', b'{"source_count":1}\n'):
            self.assert_content_refused(data, "NDJSON")

    def test_factory_foreign_metadata_before_semver_and_codec(self):
        for updates in (
            {"mapping": _ForeignDict(_mapping())},
            {"mapping": {**_mapping(), "owner_reference": _Hostile()}},
            {"policy": {**_valid_policy(), "max_rows": _Hostile()}},
            {"policy": {**_valid_policy(), "retry_delays_seconds": _ForeignList([1, 2])}},
            {"declared_owner_fields": (_Hostile(),)},
            {"declared_codes": (_Hostile(),)},
        ):
            kwargs = {
                "mapping": _mapping(), "policy": _valid_policy(),
                "declared_owner_fields": _FIELDS, "declared_codes": runtime._CONTENT_CODES,
            }
            kwargs.update(updates)
            with mock.patch.object(contracts, "parse_version", side_effect=AssertionError("parse before types")):
                with mock.patch.object(runtime.json, "loads", side_effect=AssertionError("JSON before metadata types")):
                    parser, refusals = runtime.new_bulk_import_parser(**kwargs)
            self.assertIsNone(parser)
            self.assertTrue(refusals)
            self.assertTrue(all(type(d) is Diagnostic and d.step == VALIDATE for d in refusals))

    def test_factory_owner_fields_variant_and_catalogue_required(self):
        for updates in (
            {"declared_owner_fields": ("name",)},
            {"declared_codes": ()},
            {"mapping": {**_mapping(), "variant": "EXPORT"}},
            {"mapping": {**_mapping(), "format": "UNKNOWN"}},
        ):
            kwargs = {
                "mapping": _mapping(), "policy": _valid_policy(),
                "declared_owner_fields": _FIELDS, "declared_codes": runtime._CONTENT_CODES,
            }
            kwargs.update(updates)
            parser, refusals = runtime.new_bulk_import_parser(**kwargs)
            self.assertIsNone(parser)
            self.assertTrue(refusals)

    def test_factory_foreign_key_not_rehashed(self):
        key = _HashOnce()
        mapping = _mapping()
        mapping[key] = _Hostile()
        parser, refusals = runtime.new_bulk_import_parser(
            mapping=mapping, policy=_valid_policy(), declared_owner_fields=_FIELDS,
            declared_codes=runtime._CONTENT_CODES,
        )
        self.assertIsNone(parser)
        self.assertTrue(refusals)
        self.assertEqual(key.calls, 1)

    def test_foreign_feed_types_never_call_hooks(self):
        for chunk in (_Hostile(), _ForeignBytes(b"x"), "x", memoryview(b"x"), bytearray(b"x")):
            parser = _new()
            self.assertEqual(parser.feed(chunk), ())
            _last, summary = parser.finish()
            self.assertFalse(self.assert_summary_safe(summary)["complete"])

    def test_chunk_and_input_byte_limits_stop_incompletely(self):
        self.assert_content_refused(
            b"source_name,source_count\nalice,1\n",
            policy_updates={"read_chunk_bytes": 4},
        )
        self.assert_content_refused(
            b"source_name,source_count\nalice,1\n",
            policy_updates={"max_input_bytes": 4},
        )

    def test_record_bytes_and_columns_limits_stop_incompletely(self):
        self.assert_content_refused(
            b"source_name,source_count\nalice,1\n",
            policy_updates={"max_row_bytes": 8},
        )
        self.assert_content_refused(
            b"source_name,source_count\nalice,1\n",
            policy_updates={"max_columns": 1},
        )

    def test_row_budget_reached_is_incomplete_no_extra_consumption(self):
        parser = _new(policy_updates={"max_rows": 1})
        units = parser.feed(b"source_name,source_count\nalice,1\nbob,2\n")
        _last, summary = parser.finish()
        values = self.assert_summary_safe(summary)
        self.assertFalse(values["complete"])
        self.assertLessEqual(values["units_emitted"] + values["units_refused"], 1)
        self.assertLessEqual(len(units), 1)

    def test_ndjson_limits_before_decoder_construction(self):
        for data, limits in (
            (b'{"source_name":{"x":{"y":1}}}\n', {"max_json_depth": 1}),
            (b'{"source_name":1,"source_count":2}\n', {"max_json_members": 1}),
        ):
            parser = _new("NDJSON", policy_updates=limits)
            with mock.patch.object(runtime.json, "loads", side_effect=AssertionError("unbounded JSON decoder")):
                with mock.patch.object(runtime.json, "JSONDecoder", side_effect=AssertionError("unbounded decoder construction")):
                    self.assertEqual(parser.feed(data), ())
                    _last, summary = parser.finish()
            self.assertFalse(self.assert_summary_safe(summary)["complete"])

    def test_diagnostic_budget_bounded_and_no_values_echoed(self):
        parser = _new("NDJSON", policy_updates={"max_diagnostics": 1})
        parser.feed(b'{"LEAK-MARKER":1}\n{"LEAK-MARKER":2}\n')
        _last, summary = parser.finish()
        values = self.assert_summary_safe(summary)
        self.assertFalse(values["complete"])
        self.assertLessEqual(len(values["diagnostics"]), 1)

    def test_finish_idempotent_and_terminal_feed_no_mutation(self):
        parser = _new()
        parser.feed(b"source_name,source_count\nalice,1")
        units, summary = parser.finish()
        before = _summary_values(summary)
        self.assertEqual(len(units), 1)
        again, same = parser.finish()
        self.assertEqual(again, ())
        self.assertIs(same, summary)
        with self.assertRaises(ValueError):
            parser.feed(b"bob,2\n")
        self.assertEqual(_summary_values(summary), before)
        with self.assertRaises((FrozenInstanceError, AttributeError)):
            summary.complete = False

    def test_close_premature_and_foreign_reason(self):
        parser = _new()
        with self.assertRaises(ValueError):
            parser.close(_Hostile())
        parser.feed(b"source_name,source_count\n")
        parser.close("CANCELLED")
        units, summary = parser.finish()
        self.assertEqual(units, ())
        self.assertFalse(self.assert_summary_safe(summary)["complete"])
        with self.assertRaises(ValueError):
            parser.feed(b"alice,1\n")

    def test_metadata_results_owned_and_globals_unchanged(self):
        csv_limit = csv.field_size_limit()
        int_limit = sys.get_int_max_str_digits()
        mapping = _mapping()
        policy = _valid_policy()
        parser, refusals = runtime.new_bulk_import_parser(
            mapping=mapping, policy=policy, declared_owner_fields=_FIELDS,
            declared_codes=runtime._CONTENT_CODES,
        )
        self.assertEqual(refusals, [])
        mapping["field_bindings"] = ()
        policy["max_rows"] = 1
        parser.feed(b"source_name,source_count\nalice,1\nbob,2\n")
        _last, summary = parser.finish()
        self.assertTrue(_summary_values(summary)["complete"])
        self.assertEqual(csv.field_size_limit(), csv_limit)
        self.assertEqual(sys.get_int_max_str_digits(), int_limit)
        changed = _summary_values(summary)
        if changed["diagnostics"]:
            changed["diagnostics"][0]["code"] = "caller-changed"
        self.assertEqual(_summary_values(summary)["diagnostics"], ())


if __name__ == "__main__":
    unittest.main()
