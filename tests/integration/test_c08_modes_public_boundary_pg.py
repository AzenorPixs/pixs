"""Recette PG frontiere publique modes C08 : 3 cas ciblés, effets reels."""
from __future__ import annotations
import json as _json
import sys as _sys
from pathlib import Path as _Path
ROOT = _Path(__file__).resolve().parents[2]
_sys.path.insert(0, str(ROOT / "src"))
_sys.path.insert(0, str(ROOT / "tests" / "integration"))
CASE_TIMEOUT = 180
CASES = ("FREE_CALLBACK", "CROSS_ACTION", "BAD_DIGEST")
def _run_one(case: str) -> int:
    import core_pg_test_support as _support
    from c08_modes_pg_harness import run_in_modes_schema as _run_harness
    _doc = None
    _code = 1
    with _support.mask_output():
        try:
            from c08_modes_fixture import make_modes_fixture as _make_fx, ROOT_INST as _ROOT_INST
            from pixs.backend.installation.mode_values import ModeOperationKind as _K
            from pixs.core.ports import CorePortError as _CorePortError
            from pixs.core.dto import CoreMutationResult as _Result
            from pixs.core.services_mode_transition import execute_modes_transition as _core_entry
            def _counts(inst, fx):
                from pixs.backend.c08_mode_snapshot_record import C08ModeSnapshotRecord as _S
                from pixs.backend.c08_mode_operation_receipt_record import C08ModeOperationReceiptRecord as _R
                return (_S.objects.using("peer").filter(installation_id=inst).count(), _R.objects.using("peer").filter(installation_id=inst).count())
            def _cb():
                _inner = {}
                if case == "FREE_CALLBACK":
                    def _body():
                        with _make_fx(str(ROOT)) as _fx:
                            _inst = _ROOT_INST
                            _calls = []
                            def _evil(ctx):
                                _calls.append(1)
                                raise AssertionError("CALLBACK_EXECUTED")
                            _n0, _r0 = _counts(_inst, _fx)
                            with _fx["server_call"]("root", _K.FINALIZE_CONFIGURATION, 1, "k-free-1", "op-free-1", "corr-free-1") as _kw:
                                for _extra in ({"apply": _evil}, {"ports": None}, {"participant": None}, {"lock_scopes": ()}, {"expected_owner": "pixs.backend"}, {"facts_source": None}):
                                    try:
                                        _core_entry(**{**_kw, **_extra})  # type: ignore[call-arg]
                                    except TypeError:
                                        pass
                                    else:
                                        return False
                            assert len(_calls) == 0
                            assert _counts(_inst, _fx) == (_n0, _r0)
                            with _fx["server_call"]("root", _K.FINALIZE_CONFIGURATION, 1, "k-free-2", "op-free-2", "corr-free-2") as _kw2:
                                _ok = _core_entry(**_kw2)
                            assert type(_ok) is _Result and _ok.version == 2
                            _rc = _fx["read_receipt_peer"]("op-free-2")
                            assert _rc.status == "SUCCEEDED" and _rc.result_kind == "NEW_SNAPSHOT"
                            _sn = _fx["read_snapshot_peer"](_rc.result_snapshot_id)
                            assert _sn.version == 2 and (_sn.configuration_state, _sn.operating_mode) == ("CONFIGURED", "NORMAL")
                            assert _counts(_inst, _fx) == (_n0 + 1, _r0 + 1)
                            from pixs.core.persistence.models_audit import CoreAuditEvent as _Audit
                            from pixs.backend.c10_receipt_record import C10ReceiptRecord as _C10
                            assert _Audit.objects.using("peer").filter(operation_id="op-free-2").count() == 1
                            assert _C10.objects.using("peer").filter(operation_id="op-free-2", receipt_kind="ATTEST").count() == 1
                            return True
                    _inner[case] = bool(_body())
                elif case == "CROSS_ACTION":
                    def _body():
                        with _make_fx(str(ROOT)) as _fx:
                            _inst = _ROOT_INST
                            _n0, _r0 = _counts(_inst, _fx)
                            with _fx["server_call"]("root", _K.ENTER_MAINTENANCE, 1, "k-cross-1", "op-cross-1", "corr-cross-1", fault="cross_action") as _kw:
                                try:
                                    _core_entry(**_kw)
                                except _CorePortError:
                                    pass
                                else:
                                    return False
                            assert _counts(_inst, _fx) == (_n0, _r0)
                            with _fx["server_call"]("root", _K.ENTER_MAINTENANCE, 1, "k-cross-2", "op-cross-2", "corr-cross-2") as _kw2:
                                _ok = _core_entry(**_kw2)
                            assert type(_ok) is _Result and _ok.version == 2
                            _rc = _fx["read_receipt_peer"]("op-cross-2")
                            assert _rc.status == "SUCCEEDED" and _rc.result_kind == "NEW_SNAPSHOT"
                            _sn2 = _fx["read_snapshot_peer"](_rc.result_snapshot_id)
                            assert _sn2.version == 2 and (_sn2.configuration_state, _sn2.operating_mode) == ("PENDING", "MAINTENANCE")
                            assert _counts(_inst, _fx) == (_n0 + 1, _r0 + 1)
                            from pixs.core.persistence.models_audit import CoreAuditEvent as _Audit2
                            from pixs.backend.c10_receipt_record import C10ReceiptRecord as _C102
                            assert _Audit2.objects.using("peer").filter(operation_id="op-cross-2").count() == 1
                            assert _C102.objects.using("peer").filter(operation_id="op-cross-2", receipt_kind="ATTEST").count() == 1
                            return True
                    _inner[case] = bool(_body())
                elif case == "BAD_DIGEST":
                    def _body():
                        with _make_fx(str(ROOT)) as _fx:
                            _inst = _ROOT_INST
                            _n0, _r0 = _counts(_inst, _fx)
                            with _fx["server_call"]("root", _K.ENTER_MAINTENANCE, 1, "k-dig-1", "op-dig-1", "corr-dig-1", fault="bad_digest") as _kw:
                                try:
                                    _core_entry(**_kw)
                                except _CorePortError:
                                    pass
                                else:
                                    return False
                            assert _counts(_inst, _fx) == (_n0, _r0)
                            with _fx["server_call"]("root", _K.ENTER_MAINTENANCE, 1, "k-dig-2", "op-dig-2", "corr-dig-2") as _kw2:
                                _ok = _core_entry(**_kw2)
                            assert type(_ok) is _Result and _ok.version == 2
                            _rc = _fx["read_receipt_peer"]("op-dig-2")
                            assert _rc.status == "SUCCEEDED" and _rc.result_kind == "NEW_SNAPSHOT"
                            _sn3 = _fx["read_snapshot_peer"](_rc.result_snapshot_id)
                            assert _sn3.version == 2 and (_sn3.configuration_state, _sn3.operating_mode) == ("PENDING", "MAINTENANCE")
                            assert _counts(_inst, _fx) == (_n0 + 1, _r0 + 1)
                            from pixs.core.persistence.models_audit import CoreAuditEvent as _Audit3
                            from pixs.backend.c10_receipt_record import C10ReceiptRecord as _C103
                            assert _Audit3.objects.using("peer").filter(operation_id="op-dig-2").count() == 1
                            assert _C103.objects.using("peer").filter(operation_id="op-dig-2", receipt_kind="ATTEST").count() == 1
                            return True
                    _inner[case] = bool(_body())
                else:
                    _inner[case] = False
                return _inner
            _res = _run_harness(str(ROOT), _cb, (case,))
            _doc = {"case": case, "code": _res["code"], "cases": _res["cases"], "proof": {"real_pg": _res["real_pg"], "namespace": _res["namespace"], "migration": _res["migration"], "core_migration": _res["core_migration"], "backend_migration": _res["backend_migration"], "cleanup": _res["cleanup"], "conns_closed": _res["conns_closed"]}, "versions": {"pg": _res["pg_version_num"], "django": _res["django_version"]}, "failure_type": _res["failure_type"], "failure_frames": _res["failure_frames"]}
        except Exception as _e:
            _doc = {"case": case, "code": "CHILD_FAILED", "failure_type": type(_e).__name__}
            _code = 1
        else:
            _code = 0 if (_doc["code"] == "NONE" and _doc["cases"].get(case) is True and all(v is True for v in _doc["proof"].values())) else 1
    print(_json.dumps(_doc, sort_keys=True, separators=(",", ":")))
    return _code
def _driver() -> int:
    import subprocess as _sp
    import core_pg_test_support as _sup
    _agg = {"code": "PASS", "cases": {}, "versions": {}}
    with _sup.mask_output():
        for _c in CASES:
            try:
                _p = _sp.run([_sys.executable, "-I", "-B", str(_Path(__file__)), "--case", _c], cwd=str(ROOT), timeout=CASE_TIMEOUT, capture_output=True, text=True)
            except (OSError, _sp.SubprocessError):
                _agg["cases"][_c] = False
                _agg["code"] = "TEST_FAILED"
                continue
            _line = (_p.stdout.strip().splitlines() or [""])[-1]
            try:
                _d = _json.loads(_line)
            except _json.JSONDecodeError:
                _agg["cases"][_c] = False
                _agg["code"] = "TEST_FAILED"
                continue
            _ok = (type(_d) is dict and _p.returncode == 0 and _d.get("case") == _c and _d.get("code") == "NONE" and type(_d.get("cases")) is dict and set(_d["cases"]) == {_c} and _d["cases"][_c] is True and type(_d.get("proof")) is dict and set(_d["proof"]) == {"real_pg", "namespace", "migration", "core_migration", "backend_migration", "cleanup", "conns_closed"} and all(v is True for v in _d["proof"].values()))
            if type(_d) is dict and type(_d.get("versions")) is dict:
                _agg["versions"][_c] = _d["versions"]
            _agg["cases"][_c] = bool(_ok)
            if not _ok:
                _agg["code"] = "TEST_FAILED"
    print(_json.dumps({"code": _agg["code"], "cases": _agg["cases"], "versions": _agg["versions"]}, sort_keys=True, separators=(",", ":")))
    return 0 if _agg["code"] == "PASS" else 1
if __name__ == "__main__":
    import argparse as _ap
    _parser = _ap.ArgumentParser()
    _parser.add_argument("--case", default=None)
    _ns = _parser.parse_args()
    if _ns.case is None:
        raise SystemExit(_driver())
    if _ns.case not in CASES:
        print(_json.dumps({"case": _ns.case, "code": "UNKNOWN_CASE"}))
        raise SystemExit(2)
    raise SystemExit(_run_one(_ns.case))
