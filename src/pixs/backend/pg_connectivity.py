'''Bounded async PG connectivity probe, SELECT 1 only.'''

from __future__ import annotations

import asyncio
import ipaddress
import math
from typing import NoReturn

__all__ = ['PgProbeError', 'probe_pg_connectivity']

_GENERIC = 'pg connectivity invalid'
_MAX_LABEL = 63
_MAX_SECRET = 4096
_MAX_INT32 = 2147483647


class PgProbeError(ValueError):
    '''Fixed generic refusal without connection detail.'''


def _fail() -> NoReturn:
    raise PgProbeError(_GENERIC) from None


def _checked_text(value: object, limit: int) -> str:
    if type(value) is not str:
        _fail()
    if value == '' or len(value) > limit:
        _fail()
    if chr(0) in value:
        _fail()
    try:
        value.encode('utf-8')
    except UnicodeError:
        _fail()
    return value


def _checked_ip(value: object) -> str:
    if type(value) is not str:
        _fail()
    if value == '' or len(value) > 45:
        _fail()
    if '%' in value:
        _fail()
    try:
        parsed = ipaddress.ip_address(value)
    except ValueError:
        _fail()
    text = str(parsed)
    if text != value:
        _fail()
    return text


def _checked_dbname(value: object) -> str:
    text = _checked_text(value, _MAX_LABEL)
    if '=' in text or '://' in text:
        _fail()
    return text


def _checked_port(value: object) -> int:
    if type(value) is not int:
        _fail()
    if value < 1 or value > 65535:
        _fail()
    return value


def _checked_connect_timeout(value: object) -> int:
    if type(value) is not int:
        _fail()
    if value < 2 or value > _MAX_INT32:
        _fail()
    return value


def _checked_query_timeout(value: object) -> float:
    if type(value) is bool:
        _fail()
    if type(value) is int:
        if value <= 0:
            _fail()
        try:
            number = float(value)
        except (OverflowError, ValueError):
            _fail()
        if not math.isfinite(number) or number <= 0.0:
            _fail()
        return number
    if type(value) is float:
        if not math.isfinite(value) or value <= 0.0:
            _fail()
        return value
    _fail()


def _checked_statement_timeout(value: object) -> int:
    if type(value) is not int:
        _fail()
    if value <= 0 or value > _MAX_INT32:
        _fail()
    return value


async def probe_pg_connectivity(*, hostaddr: object, dbname: object, user: object, password: object, port: object, connect_timeout_s: object, query_timeout_s: object, statement_timeout_ms: object, _connect: object = None) -> bool:
    '''Probe one SELECT 1 over an explicitly held connection.
    Credentials and delays come from the trusted caller only. The obtained
    connection is helper owned until closed and is never returned, so the
    internal SDK object stays inside. On a local timeout the held connection
    is closed BEFORE cancelling the query task. A caller cancel closes first
    as well and then propagates after cleanup. Partial effects are never
    rolled back and nothing is retried.
    '''
    ip = _checked_ip(hostaddr)
    name = _checked_dbname(dbname)
    login = _checked_text(user, _MAX_LABEL)
    secret = _checked_text(password, _MAX_SECRET)
    port_number = _checked_port(port)
    connect_timeout = _checked_connect_timeout(connect_timeout_s)
    query_timeout = _checked_query_timeout(query_timeout_s)
    statement_timeout = _checked_statement_timeout(statement_timeout_ms)
    if _connect is None:
        try:
            from psycopg import AsyncConnection
            connector = AsyncConnection.connect
        except Exception:
            _fail()
    else:
        connector = _connect
        try:
            ok = callable(connector)
        except Exception:
            _fail()
        if not ok:
            _fail()
    options = ' '.join(['-c default_transaction_read_only=on', '-c statement_timeout=' + str(statement_timeout)])
    try:
        conn = await connector(host=ip, hostaddr=ip, dbname=name, user=login, password=secret, port=port_number, connect_timeout=connect_timeout, autocommit=True, options=options)
    except Exception:
        _fail()
    async def _once():
        try:
            cur = conn.cursor()
        except Exception:
            _fail()
        try:
            await cur.execute('SELECT 1')
            row = await cur.fetchone()
        finally:
            try:
                await cur.close()
            except Exception:
                _fail()
        if type(row) is not tuple or len(row) != 1:
            _fail()
        if type(row[0]) is not int or row[0] != 1:
            _fail()
        return row
    query_task = asyncio.ensure_future(_once())
    outcome_error = False
    caller_cancel = False
    cleanup_failure = False
    cancel_requested = False
    try:
        try:
            done, _pending = await asyncio.wait([query_task], timeout=query_timeout)
        except asyncio.CancelledError:
            caller_cancel = True
        except Exception:
            outcome_error = True
        else:
            if len(done) == 0:
                outcome_error = True
            else:
                try:
                    query_task.result()
                except PgProbeError:
                    outcome_error = True
                except asyncio.CancelledError:
                    outcome_error = True
                except Exception:
                    outcome_error = True
    finally:
        try:
            await conn.close()
        except asyncio.CancelledError:
            cleanup_failure = True
        except Exception:
            cleanup_failure = True
        if not query_task.done():
            query_task.cancel()
            cancel_requested = True
        try:
            await query_task
        except asyncio.CancelledError:
            if not (cancel_requested or caller_cancel):
                outcome_error = True
        except Exception:
            outcome_error = True
    if cleanup_failure or outcome_error:
        _fail()
    if caller_cancel:
        raise asyncio.CancelledError from None
    return True
