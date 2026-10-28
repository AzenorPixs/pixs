"""Resolutif transport WEB : injection explicite de confiance, sans decouverte.

Le serveur de confiance injecte les ModuleHttpBinding reellement montes.
La facade contexte publie le resolutif dans meta.transport_resolver.
"""
from __future__ import annotations

from pixs.backend.api_core_catalog import API_CORE_CATALOG_VERSION as _CORE_VERSION
from pixs.backend.api_core_catalog import COMMANDS as _COMMANDS
from pixs.backend.api_core_catalog import QUERIES as _QUERIES
from pixs.backend.api_module_views import ModuleHttpBinding as _Binding

__all__ = ['build_shell_transport_resolver', 'shell_transport_resolver_schema']

_TRANSPORT_VERSION = '1.0.0'
_SCOPES = ('P', 'T', 'S')

def _fail(message):
    raise ValueError(message)

def _check_bindings(bindings):
    if type(bindings) is not tuple:
        _fail('Bindings exacts requis.')
    seen_triples = set()
    seen_names = set()
    for binding in bindings:
        if type(binding) is not _Binding:
            _fail('Binding module exact requis.')
        binding.__post_init__()
        triple = (binding.owner, binding.kind, binding.name)
        if triple in seen_triples:
            _fail('Collision proprietaire/genre/nom.')
        seen_triples.add(triple)
        pair = (binding.kind, binding.name)
        if pair in seen_names:
            _fail('Collision genre/nom.')
        seen_names.add(pair)
    for index in range(len(bindings)):
        for other in range(index + 1, len(bindings)):
            left = bindings[index]
            right = bindings[other]
            if tuple(left.segments) == tuple(right.segments) and set(left.scopes) & set(right.scopes):
                _fail('Route/contextes en collision.')
    return bindings

def build_shell_transport_resolver(*, module_bindings=()):
    """Construit le resolutif client versionne, sans secret ni droit."""
    checked = _check_bindings(module_bindings)
    operations = []
    seen_names = set()
    for name in _COMMANDS:
        spec = _COMMANDS[name]
        declared = spec['roots']
        if (type(declared) is not tuple or not declared
                or any(type(scope) is not str or scope not in _SCOPES for scope in declared)
                or len(set(declared)) != len(declared)):
            _fail('Contexte Core invalide.')
        roots = tuple(scope for scope in _SCOPES if scope in declared)
        for scope in roots:
            if scope not in _SCOPES:
                _fail('Contexte Core invalide.')
        operations.append({
            'kind': 'COMMAND',
            'name': name,
            'owner': 'pixs.core',
            'contractVersion': _CORE_VERSION,
            'scopes': list(roots),
            'segments': ['commands', name],
        })
        seen_names.add(('COMMAND', name))
    for name in _QUERIES:
        spec = _QUERIES[name]
        declared = spec['roots']
        if (type(declared) is not tuple or not declared
                or any(type(scope) is not str or scope not in _SCOPES for scope in declared)
                or len(set(declared)) != len(declared)):
            _fail('Contexte Core invalide.')
        roots = tuple(scope for scope in _SCOPES if scope in declared)
        for scope in roots:
            if scope not in _SCOPES:
                _fail('Contexte Core invalide.')
        operations.append({
            'kind': 'QUERY',
            'name': name,
            'owner': 'pixs.core',
            'contractVersion': _CORE_VERSION,
            'scopes': list(roots),
            'segments': [name],
        })
        seen_names.add(('QUERY', name))
    for binding in checked:
        pair = (binding.kind, binding.name)
        if pair in seen_names:
            _fail('Collision genre/nom.')
        seen_names.add(pair)
        operations.append({
            'kind': binding.kind,
            'name': binding.name,
            'owner': binding.owner,
            'contractVersion': binding.contract_version,
            'scopes': list(binding.scopes),
            'segments': list(binding.segments),
        })
    return {'version': _TRANSPORT_VERSION, 'operations': operations}

def shell_transport_resolver_schema():
    """Schema OpenAPI ferme du resolutif, six champs par operation."""
    operation = {
        'type': 'object',
        'properties': {
            'kind': {'type': 'string', 'enum': ['QUERY', 'COMMAND']},
            'name': {'type': 'string', 'minLength': 1},
            'owner': {'type': 'string', 'minLength': 1},
            'contractVersion': {'type': 'string', 'minLength': 1},
            'scopes': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': {'type': 'string', 'enum': ['P', 'T', 'S']}},
            'segments': {'type': 'array', 'minItems': 1, 'items': {'type': 'string', 'minLength': 1}},
        },
        'required': ['kind', 'name', 'owner', 'contractVersion', 'scopes', 'segments'],
        'additionalProperties': False,
    }
    return {
        'type': 'object',
        'properties': {
            'version': {'type': 'string', 'const': _TRANSPORT_VERSION},
            'operations': {'type': 'array', 'items': operation},
        },
        'required': ['version', 'operations'],
        'additionalProperties': False,
    }
