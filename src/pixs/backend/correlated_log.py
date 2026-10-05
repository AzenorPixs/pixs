'''Bounded correlated log from valid W3C 00 traceparent and existing UUID.'''

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import NoReturn
from pixs.backend.api.errors import build_infrastructure_error
from pixs.backend.composition_initial import REQUIRED_IDS

__all__ = ['CorrelatedLogError', 'TraceContext', 'emit_correlated_log', 'parse_traceparent']

_EVENT = 'component.context'
_GENERIC = 'correlated log invalid'
_HEX = frozenset('0123456789abcdef')
_ZERO_TRACE = '0' * 32
_ZERO_PARENT = '0' * 16


class CorrelatedLogError(ValueError):
    '''Generic refusal without raw echo.'''


def _fail() -> NoReturn:
    raise CorrelatedLogError(_GENERIC) from None


@dataclass(frozen=True)
class TraceContext:
    '''Parsed valid 00 context only, not all W3C versions.'''
    trace_id: str
    parent_id: str
    sampled: bool


def _checked_traceparent(value: object) -> TraceContext:
    if type(value) is not str:
        _fail()
    if len(value) != 55:
        _fail()
    if value[0:2] != '00':
        _fail()
    if value[2] != '-' or value[35] != '-' or value[52] != '-':
        _fail()
    trace_id = value[3:35]
    parent_id = value[36:52]
    flags = value[53:55]
    for ch in trace_id:
        if ch not in _HEX:
            _fail()
    for ch in parent_id:
        if ch not in _HEX:
            _fail()
    for ch in flags:
        if ch not in _HEX:
            _fail()
    if trace_id == _ZERO_TRACE:
        _fail()
    if parent_id == _ZERO_PARENT:
        _fail()
    sampled = (int(flags, 16) & 1) == 1
    return TraceContext(trace_id=trace_id, parent_id=parent_id, sampled=sampled)


def parse_traceparent(traceparent: object) -> TraceContext:
    '''Parse only already valid version 00 context.'''
    return _checked_traceparent(traceparent)


def _canonical_correlation(correlation_id: object) -> str:
    try:
        envelope = build_infrastructure_error(correlation_id, internal_error=None)
    except Exception:
        _fail()
    try:
        text = envelope['correlation_id']
    except Exception:
        _fail()
    if type(text) is not str:
        _fail()
    return text


def emit_correlated_log(*, traceparent: object, correlation_id: object, component_id: object, sink: object) -> None:
    '''Emit one fixed event to explicit trusted caller sink.
    The sink is caller owned with a write method. A partial write may already
    have an effect even on failure, so there is no rollback or retry.
    '''
    if type(component_id) is not str:
        _fail()
    if component_id not in REQUIRED_IDS:
        _fail()
    parsed = _checked_traceparent(traceparent)
    canonical = _canonical_correlation(correlation_id)
    try:
        write = sink.write
    except Exception:
        _fail()
    if not callable(write):
        _fail()
    record = {
        'component': component_id,
        'correlation_id': canonical,
        'event': _EVENT,
        'parent_id': parsed.parent_id,
        'sampled': parsed.sampled,
        'trace_id': parsed.trace_id,
    }
    line = json.dumps(record, sort_keys=True, separators=(',', ':'), ensure_ascii=False) + '\n'
    try:
        result = write(line)
    except Exception:
        _fail()
    if type(result) is not int or result != len(line):
        _fail()
    return None
