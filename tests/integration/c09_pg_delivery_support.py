"""Wrapper PG C09 2.3 : applique backend 0013 puis scenario exact, sans recopier fixtures/env/cleanup."""
from __future__ import annotations

import re
import types

__all__ = ["run_real"]

_SQLSTATE_RE = re.compile(r"[0-9A-Z]{5}")


def _safe_sqlstate(exc):
    seen = set()
    cur = exc
    while cur is not None and id(cur) not in seen:
        seen.add(id(cur))
        try:
            val = getattr(cur, "sqlstate", None)
        except Exception:
            val = None
        if type(val) is str and _SQLSTATE_RE.fullmatch(val) is not None:
            return val
        try:
            diag = getattr(cur, "diag", None)
            val2 = getattr(diag, "sqlstate", None) if diag is not None else None
        except Exception:
            val2 = None
        if type(val2) is str and _SQLSTATE_RE.fullmatch(val2) is not None:
            return val2
        cur = getattr(cur, "__cause__", None)
    return ""


def _safe_position(exc):
    seen = set()
    cur = exc
    while cur is not None and id(cur) not in seen:
        seen.add(id(cur))
        try:
            diag = getattr(cur, "diag", None)
        except Exception:
            diag = None
        cand = None
        if diag is not None:
            try:
                cand = getattr(diag, "statement_position", None)
            except Exception:
                cand = None
        if type(cand) is int and 1 <= cand <= 2147483647:
            return cand
        if type(cand) is str and re.fullmatch(r"[0-9]+", cand) is not None:
            try:
                num = int(cand, 10)
            except ValueError:
                num = None
            if type(num) is int and 1 <= num <= 2147483647:
                return num
        cur = getattr(cur, "__cause__", None)
    return None


def run_real(root_str, scenarios_callback):
    """Delegue au vrai harness ; applique 0013 puis scenario exact."""
    import c09_pg_test_support as base

    if type(root_str) is not str or type(scenarios_callback) is not types.FunctionType:
        raise ValueError("PARAMETRE_INVALIDE")
    captured = {"sqlstate": "", "position": None, "called": False}

    def migrated_callback(ctx):
        from django.db import connections
        from django.db.migrations.executor import MigrationExecutor

        if type(ctx) is not dict or type(ctx.get("schema")) is not str:
            raise RuntimeError("CONTEXTE_INVALIDE")
        targets = [("backend", "0013_c09_events_scheduler")]
        try:
            if MigrationExecutor(connections["default"]).migration_plan(targets) == []:
                raise RuntimeError("CIBLE_DEJA_APPLIQUEE")
            MigrationExecutor(connections["default"]).migrate(targets)
            if MigrationExecutor(connections["default"]).migration_plan(targets) != []:
                raise RuntimeError("REPLAY_NON_PROUVE")
        except Exception as err:
            captured["sqlstate"] = _safe_sqlstate(err)
            captured["position"] = _safe_position(err)
            raise
        try:
            cases = scenarios_callback(ctx)
        except Exception as err:
            captured["sqlstate"] = _safe_sqlstate(err)
            captured["position"] = _safe_position(err)
            raise
        captured["called"] = True
        if type(cases) is not dict or not cases:
            raise RuntimeError("CAS_NON_PROUVE")
        if any(type(k) is not str or re.fullmatch(r"[a-z][a-z0-9_]{1,100}", k) is None or v is not True for k, v in cases.items()):
            raise RuntimeError("CAS_NON_PROUVE")
        return cases

    out = base.run_real(root_str, migrated_callback)
    if type(out) is not dict:
        return out
    # N'ajoute que metadonnees sures sur echec, jamais de message/params/secrets.
    if not out.get("real_pg"):
        sql = captured.get("sqlstate")
        pos = captured.get("position")
        if type(sql) is str and _SQLSTATE_RE.fullmatch(sql) is not None:
            out["sqlstate"] = sql
        if type(pos) is int and 1 <= pos <= 2147483647:
            out["statement_position"] = pos
        if not captured.get("called") and out.get("code") == "NONE":
            out["code"] = "CAS_NON_PROUVE"
    return out
