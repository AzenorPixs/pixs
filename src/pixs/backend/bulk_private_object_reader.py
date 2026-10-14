"""Lecteur privé B04 borné : invocation réelle sous contrôles actuels.

Module purement mémoire : sans ORM, Django, psycopg, fichier, réseau,
processus, environnement, route, worker, upload, purge, sérialisation,
import dynamique ni état global mutable. Les diagnostics sont VALIDATE
statiques, triés et dédupliqués, sans valeur fournie ni exception brute.
"""

from __future__ import annotations

import asyncio
import inspect
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from types import FunctionType, MethodType

from pixs.backend.bulk_execution_values import validate_bulk_policy_values
from pixs.backend.bulk_object_staging import (
    new_object_integrity_verifier,
    validate_object_metadata_values,
)
from pixs.backend.bulk_trusted_ports import _BulkTrustedPorts, _capture_python_method
from pixs.kernel.diagnostics import Diagnostic, VALIDATE
from pixs.kernel.manifest.semver import parse_version

_SCOPE = "bulk_private_object_reader"

_OPAQUE_RULE = "référence opaque str exacte non vide UTF-8 sans NUL attendue"
_UTC_RULE = "datetime exact aware UTC attendu"
_EVENT_RULE = "asyncio.Event exact attendu"
_TRUSTED_RULE = "ports de confiance serveur exacts attendus"
_RESOLVER_RULE = "résolveur de qualification serveur exact attendu"
_BINDING_RULE = "liaison qualifiée serveur exacte attendue"
_COOP_RULE = "capacité fournisseur async coopérative exacte attendue"
_AUTHORITY_RULE = "autorité EXECUTE actuelle ALLOW attendue"
_GOVERNANCE_RULE = "gouvernance RESOLVED actuelle attendue"
_TENANT_RULE = "tenant attendu identique au contexte courant attendu"
_POLICY_RULE = "limites résolues identiques à la politique attendue"
_VERSION_RULE = "métadonnées stables avant et après flux attendues"
_CLOSE_RULE = "fermeture réussie avant tout résultat positif attendue"
_CANCEL_RULE = "annulation serveur refuse avant résultat"
_EXPIRED_RULE = "échéance effective atteinte refuse avant résultat"
_PROVIDER_RULE = "fournisseur indisponible sans détail brut attendu"


class _ServerCancelled(ValueError):
    """Signal serveur Event, distinct de CancelledError externe."""


class _ReadRefused(ValueError):
    """Refus interne portant seulement des diagnostics déjà construits."""

    def __init__(self, diagnostics: list[Diagnostic]):
        super().__init__("lecture privée refusée")
        self.diagnostics = list(diagnostics)


def _refusal(field: str, rule: str) -> Diagnostic:
    return Diagnostic(step=VALIDATE, element=f"{_SCOPE}.{field}", constraint=rule, message=rule)


def _pack(refusals: list[Diagnostic]) -> list[Diagnostic]:
    unique: dict[tuple[str, str, str], Diagnostic] = {}
    for item in refusals:
        unique[(item.element, item.constraint, item.message)] = item
    return [unique[key] for key in sorted(unique)]


def _is_opaque_text(value: object) -> bool:
    if type(value) is not str or not value or "\x00" in value:
        return False
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _is_complete_semver(value: object) -> bool:
    if type(value) is not str or not value:
        return False
    try:
        parse_version(value)
    except ValueError:
        return False
    return True


@dataclass(frozen=True, slots=True)
class _QualifiedStorageBinding:
    """Liaison qualifiée exacte, construite côté serveur sans I/O."""

    provider_reference: str
    object_reference: str
    version_reference: str
    provider: object
    stat_private: object
    iter_bytes: object
    immutability: str
    cancellation_supported: bool


@dataclass(frozen=True, slots=True)
class _StorageResolverEnvelope:
    """Enveloppe serveur du résolveur, qualify capturée statiquement."""

    qualify: object


@dataclass(frozen=True, slots=True)
class _PrivateReadResult:
    """Bilan mécanique du vérificateur existant, sans octets."""

    complete: bool
    accepted_size: int
    sha256: str


def _capture_storage_resolver(resolver: object) -> _StorageResolverEnvelope | None:
    """Fabrique privée : capture statique exacte de qualify, sans I/O."""
    if type(resolver) is type or resolver is None:
        return None
    captured = _capture_python_method(resolver, "qualify")
    if captured is None:
        return None
    if type(captured) is not MethodType and type(captured) is not FunctionType:
        return None
    if not inspect.iscoroutinefunction(captured):
        return None
    return _StorageResolverEnvelope(qualify=captured)


def _make_qualified_storage_binding(
    *, provider: object, object_reference: str, version_reference: str, provider_reference: str
) -> _QualifiedStorageBinding | None:
    """Fabrique serveur : capture sur PROVIDER puis binding figé, sans I/O."""
    if type(provider) is type or provider is None:
        return None
    if not _is_opaque_text(provider_reference) or not _is_opaque_text(object_reference):
        return None
    if not _is_opaque_text(version_reference):
        return None
    stat_fn = _capture_python_method(provider, "stat_private")
    iter_fn = _capture_python_method(provider, "iter_bytes")
    for fn in (stat_fn, iter_fn):
        if fn is None or type(fn) is not MethodType:
            return None
        if type(fn.__func__) is not FunctionType:
            return None
        if fn.__self__ is not provider:
            return None
        if not inspect.iscoroutinefunction(fn):
            return None
    return _QualifiedStorageBinding(
        provider_reference=provider_reference,
        object_reference=object_reference,
        version_reference=version_reference,
        provider=provider,
        stat_private=stat_fn,
        iter_bytes=iter_fn,
        immutability="IMMUTABLE",
        cancellation_supported=True,
    )


def _check_binding_exact(binding: object, *, object_reference: str, version_reference: str) -> list[Diagnostic]:
    """Contrôle du binding exact connu par lecture directe des champs sûrs."""
    if type(binding) is not _QualifiedStorageBinding:
        return [_refusal("binding", _BINDING_RULE)]
    if not _is_opaque_text(binding.provider_reference):
        return [_refusal("binding.provider_reference", _OPAQUE_RULE)]
    if type(binding.object_reference) is not str or binding.object_reference != object_reference:
        return [_refusal("binding.object_reference", _VERSION_RULE)]
    if type(binding.version_reference) is not str or binding.version_reference != version_reference:
        return [_refusal("binding.version_reference", _VERSION_RULE)]
    if type(binding.immutability) is not str or binding.immutability != "IMMUTABLE":
        return [_refusal("binding.immutability", _COOP_RULE)]
    if type(binding.cancellation_supported) is not bool or binding.cancellation_supported is not True:
        return [_refusal("binding.cancellation_supported", _COOP_RULE)]
    if binding.provider is None or type(binding.provider) is type:
        return [_refusal("binding.provider", _BINDING_RULE)]
    for method in (binding.stat_private, binding.iter_bytes):
        if type(method) is not MethodType:
            return [_refusal("binding", _COOP_RULE)]
        if type(method.__func__) is not FunctionType:
            return [_refusal("binding", _COOP_RULE)]
        if method.__self__ is not binding.provider:
            return [_refusal("binding", _BINDING_RULE)]
        if not inspect.iscoroutinefunction(method):
            return [_refusal("binding", _COOP_RULE)]
    return []


async def _run_with_event(coro_factory, *, remaining_fn, cancel_event: asyncio.Event):
    """Exécute une coroutine bornée en surveillant Event ; ne masque rien."""
    budget = max(0.0, float(remaining_fn()))
    if budget <= 0:
        raise asyncio.TimeoutError
    op_task = asyncio.ensure_future(coro_factory())
    ev_task = asyncio.ensure_future(cancel_event.wait())
    try:
        done, _ = await asyncio.wait(
            [op_task, ev_task], timeout=budget, return_when=asyncio.FIRST_COMPLETED
        )
    except asyncio.CancelledError:
        for task in (op_task, ev_task):
            if not task.done():
                task.cancel()
        raise
    try:
        if ev_task in done:
            raise _ServerCancelled("signal serveur")
        if op_task in done:
            return op_task.result()
        raise asyncio.TimeoutError
    finally:
        for task in (op_task, ev_task):
            if not task.done():
                task.cancel()
        budget2 = max(0.0, float(remaining_fn()))
        try:
            await asyncio.wait([op_task, ev_task], timeout=budget2)
        finally:
            for task in (op_task, ev_task):
                if task.done() and not task.cancelled():
                    try:
                        _ = task.result()
                    except _ServerCancelled:
                        pass
                    except asyncio.CancelledError:
                        pass
                    except Exception:
                        pass


async def _close_iterator_bounded(aclose_fn: object, *, remaining_fn) -> bool:
    """Fermeture bornée d'une méthode aclose déjà capturée."""
    if aclose_fn is None:
        return False
    if type(aclose_fn) is not MethodType and type(aclose_fn) is not FunctionType:
        return False
    if not inspect.iscoroutinefunction(aclose_fn):
        return False
    budget = max(0.0, float(remaining_fn()))
    if budget <= 0:
        return False
    task = asyncio.ensure_future(aclose_fn())
    try:
        done, _ = await asyncio.wait([task], timeout=budget)
    except asyncio.CancelledError:
        if not task.done():
            task.cancel()
        raise
    if task in done:
        try:
            task.result()
        except Exception:
            return False
        return True
    if not task.done():
        task.cancel()
        try:
            budget2 = max(0.0, float(remaining_fn()))
            await asyncio.wait([task], timeout=budget2)
        finally:
            if task.done() and not task.cancelled():
                try:
                    task.result()
                except asyncio.CancelledError:
                    pass
                except Exception:
                    pass
            await asyncio.sleep(0)
    return False


@dataclass(frozen=True, slots=True)
class _QualifiedImportUnits:
    """Unités logiques qualifiées, remises seulement après intégrité complète."""

    complete: bool
    accepted_size: int
    sha256: str
    units: tuple
    parser_complete: bool


def _check_import_parser(parser: object) -> list[Diagnostic]:
    """Contrôle exact du parser mécanique serveur, sans invocation."""
    if type(parser).__module__ != "pixs.backend.bulk_streaming_import":
        return [_refusal("parser", _COOP_RULE)]
    if type(parser).__name__ not in ("_CsvImportParser", "_NdjsonImportParser"):
        return [_refusal("parser", _COOP_RULE)]
    for name in ("feed", "finish", "close"):
        if _capture_python_method(parser, name) is None:
            return [_refusal("parser", _COOP_RULE)]
    return []


async def _prepare_qualified_import_units(
    *,
    trusted_ports: object,
    server_context: object,
    operation_reference: object,
    expected_metadata: object,
    policy_reference: object,
    policy_version: object,
    storage_resolver: object,
    expected_policy: object,
    parser: object,
    deadline: object,
    now: object,
    cancel_event: object,
) -> tuple[_QualifiedImportUnits | None, list[Diagnostic]]:
    """Prépare des unités logiques sur le même parcours qualifié, sans owner."""
    if type(trusted_ports) is not _BulkTrustedPorts:
        return None, _pack([_refusal("trusted_ports", _TRUSTED_RULE)])
    if server_context is None:
        return None, _pack([_refusal("server_context", _TRUSTED_RULE)])
    if not _is_opaque_text(operation_reference):
        return None, _pack([_refusal("operation_reference", _OPAQUE_RULE)])
    if type(expected_metadata) is not dict:
        return None, _pack([_refusal("expected_metadata", _OPAQUE_RULE)])
    if not _is_opaque_text(policy_reference):
        return None, _pack([_refusal("policy_reference", _OPAQUE_RULE)])
    if not _is_complete_semver(policy_version):
        return None, _pack([_refusal("policy_version", _OPAQUE_RULE)])
    if type(expected_policy) is not dict:
        return None, _pack([_refusal("expected_policy", _OPAQUE_RULE)])
    if type(deadline) is not datetime or deadline.tzinfo is not timezone.utc:
        return None, _pack([_refusal("deadline", _UTC_RULE)])
    if type(now) is not datetime or now.tzinfo is not timezone.utc:
        return None, _pack([_refusal("now", _UTC_RULE)])
    if type(cancel_event) is not asyncio.Event:
        return None, _pack([_refusal("cancel_event", _EVENT_RULE)])
    parser_refusals = _check_import_parser(parser)
    if parser_refusals:
        return None, _pack(list(parser_refusals))
    metadata_refusals = validate_object_metadata_values(dict(expected_metadata))
    if metadata_refusals:
        return None, _pack(list(metadata_refusals))
    policy_refusals = validate_bulk_policy_values(dict(expected_policy))
    if policy_refusals:
        return None, _pack(list(policy_refusals))
    contract_owned: dict = dict(expected_metadata)
    expected_limits: dict = dict(expected_policy)
    for key, value in tuple(expected_limits.items()):
        if type(value) is list:
            expected_limits[key] = list(value)
    references_owned = (policy_reference, policy_version)
    try:
        expires_at = contract_owned["expires_at"]
    except Exception:
        return None, _pack([_refusal("expected_metadata", _OPAQUE_RULE)])
    effective = deadline if deadline < expires_at else expires_at
    if not now < effective or cancel_event.is_set():
        return None, _pack([_refusal("now", _EXPIRED_RULE)])
    try:
        max_runtime = int(expected_limits["max_runtime_seconds"])
    except Exception:
        return None, _pack([_refusal("policy", _POLICY_RULE)])
    mono_start = time.monotonic()
    utc_start = datetime.now(timezone.utc)

    def _remaining() -> float:
        current_utc = datetime.now(timezone.utc)
        remaining_utc = (effective - current_utc).total_seconds()
        elapsed_mono = time.monotonic() - mono_start
        utc_budget = (deadline - utc_start).total_seconds()
        expiry_budget = (expires_at - utc_start).total_seconds() if isinstance(expires_at, datetime) else utc_budget
        mono_budget = utc_budget if utc_budget < expiry_budget else expiry_budget
        if max_runtime < mono_budget:
            mono_budget = max_runtime
        remaining_mono = mono_budget - elapsed_mono
        return remaining_utc if remaining_utc < remaining_mono else remaining_mono

    try:
        assessment, authority_refusals = trusted_ports.check_authority(
            server_context=server_context,
            action="EXECUTE",
            operation_reference=operation_reference,
            resource_reference=contract_owned["object_reference"],
        )
    except Exception:
        return None, _pack([_refusal("authority", _AUTHORITY_RULE)])
    if assessment is None:
        return None, _pack(list(authority_refusals) or [_refusal("authority", _AUTHORITY_RULE)])
    try:
        expected_context = assessment.resolved_context.as_values()
    except Exception:
        return None, _pack([_refusal("authority", _AUTHORITY_RULE)])
    if contract_owned["tenant_reference"] != expected_context.get("tenant_id"):
        return None, _pack([_refusal("tenant_reference", _TENANT_RULE)])
    try:
        resolution, governance_refusals = trusted_ports._resolve_governance_owned(
            server_context=server_context,
            expected_context=expected_context,
            contract_owned=dict(contract_owned),
            references_owned=(references_owned[0], references_owned[1]),
        )
    except Exception:
        return None, _pack([_refusal("governance", _GOVERNANCE_RULE)])
    if resolution is None:
        return None, _pack(list(governance_refusals) or [_refusal("governance", _GOVERNANCE_RULE)])
    try:
        resolved_limits = dict(resolution.as_values()["policy"]["limits"])
    except Exception:
        return None, _pack([_refusal("governance", _GOVERNANCE_RULE)])
    if resolved_limits != expected_limits:
        return None, _pack([_refusal("policy", _POLICY_RULE)])
    envelope = _capture_storage_resolver(storage_resolver)
    if envelope is None:
        return None, _pack([_refusal("storage_resolver", _RESOLVER_RULE)])
    verifier = None
    iterator = None
    anext_fn = None
    aclose_fn = None
    iterator_clos = False
    buffered: list = []
    parser_done = False
    candidat: _QualifiedImportUnits | None = None
    diags: list[Diagnostic] = []
    externe: asyncio.CancelledError | None = None
    try:
        try:
            binding = await _run_with_event(
                lambda: envelope.qualify(
                    server_context, contract_owned["object_reference"], contract_owned["version_reference"]
                ),
                remaining_fn=_remaining,
                cancel_event=cancel_event,
            )
        except _ServerCancelled:
            raise _ReadRefused([_refusal("cancel_event", _CANCEL_RULE)])
        except asyncio.TimeoutError:
            raise _ReadRefused([_refusal("qualify", _EXPIRED_RULE)])
        except StopAsyncIteration:
            raise _ReadRefused([_refusal("qualify", _PROVIDER_RULE)])
        refused = _check_binding_exact(
            binding,
            object_reference=contract_owned["object_reference"],
            version_reference=contract_owned["version_reference"],
        )
        if refused:
            raise _ReadRefused(refused)
        stat_fn = binding.stat_private
        iter_fn = binding.iter_bytes
        try:
            stat_before = await _run_with_event(
                lambda: stat_fn(server_context, contract_owned["object_reference"], contract_owned["version_reference"]),
                remaining_fn=_remaining,
                cancel_event=cancel_event,
            )
        except _ServerCancelled:
            raise _ReadRefused([_refusal("cancel_event", _CANCEL_RULE)])
        except asyncio.TimeoutError:
            raise _ReadRefused([_refusal("stat_private", _EXPIRED_RULE)])
        except StopAsyncIteration:
            raise _ReadRefused([_refusal("stat_private", _PROVIDER_RULE)])
        if type(stat_before) is not dict or validate_object_metadata_values(dict(stat_before)):
            raise _ReadRefused([_refusal("observed_metadata", _VERSION_RULE)])
        if dict(stat_before) != dict(contract_owned):
            raise _ReadRefused([_refusal("observed_metadata", _VERSION_RULE)])
        if _remaining() <= 0 or cancel_event.is_set():
            raise _ReadRefused([_refusal("now", _EXPIRED_RULE)])
        created, verifier_refusals = new_object_integrity_verifier(
            metadata=dict(stat_before),
            expected_metadata=dict(contract_owned),
            policy=dict(resolved_limits),
            deadline=deadline,
            now=datetime.now(timezone.utc),
            cancelled=bool(cancel_event.is_set()),
        )
        if created is None:
            raise _ReadRefused(list(verifier_refusals))
        verifier = created
        try:
            maybe_iter = await _run_with_event(
                lambda: iter_fn(server_context, contract_owned["object_reference"], contract_owned["version_reference"]),
                remaining_fn=_remaining,
                cancel_event=cancel_event,
            )
        except _ServerCancelled:
            raise _ReadRefused([_refusal("cancel_event", _CANCEL_RULE)])
        except asyncio.TimeoutError:
            raise _ReadRefused([_refusal("iter_bytes", _EXPIRED_RULE)])
        except StopAsyncIteration:
            raise _ReadRefused([_refusal("iter_bytes", _PROVIDER_RULE)])
        iterator = maybe_iter
        anext_fn = _capture_python_method(iterator, "__anext__")
        aclose_fn = _capture_python_method(iterator, "aclose")
        if anext_fn is None or aclose_fn is None:
            raise _ReadRefused([_refusal("iter_bytes", _COOP_RULE)])
        if not inspect.iscoroutinefunction(anext_fn) or not inspect.iscoroutinefunction(aclose_fn):
            raise _ReadRefused([_refusal("iter_bytes", _COOP_RULE)])
        while True:
            if _remaining() <= 0 or cancel_event.is_set():
                raise _ReadRefused([_refusal("now", _EXPIRED_RULE)])
            try:
                chunk = await _run_with_event(anext_fn, remaining_fn=_remaining, cancel_event=cancel_event)
            except StopAsyncIteration:
                break
            except _ServerCancelled:
                raise _ReadRefused([_refusal("cancel_event", _CANCEL_RULE)])
            except asyncio.TimeoutError:
                raise _ReadRefused([_refusal("iter_bytes", _EXPIRED_RULE)])
            if _remaining() <= 0:
                raise _ReadRefused([_refusal("now", _EXPIRED_RULE)])
            feed_refusals = verifier.feed(chunk, now=datetime.now(timezone.utc), cancelled=bool(cancel_event.is_set()))
            if feed_refusals:
                raise _ReadRefused(list(feed_refusals))
            try:
                emitted = parser.feed(chunk)
            except Exception:
                raise _ReadRefused([_refusal("parser", _COOP_RULE)]) from None
            if type(emitted) is tuple and emitted:
                buffered.extend(emitted)
            if len(buffered) > resolved_limits["max_rows"]:
                raise _ReadRefused([_refusal("parser", _POLICY_RULE)])
        try:
            stat_after = await _run_with_event(
                lambda: stat_fn(server_context, contract_owned["object_reference"], contract_owned["version_reference"]),
                remaining_fn=_remaining,
                cancel_event=cancel_event,
            )
        except _ServerCancelled:
            raise _ReadRefused([_refusal("cancel_event", _CANCEL_RULE)])
        except asyncio.TimeoutError:
            raise _ReadRefused([_refusal("stat_private", _EXPIRED_RULE)])
        except StopAsyncIteration:
            raise _ReadRefused([_refusal("stat_private", _PROVIDER_RULE)])
        if type(stat_after) is not dict or validate_object_metadata_values(dict(stat_after)):
            raise _ReadRefused([_refusal("observed_metadata", _VERSION_RULE)])
        if dict(stat_after) != dict(contract_owned):
            raise _ReadRefused([_refusal("observed_metadata", _VERSION_RULE)])
        if _remaining() <= 0 or cancel_event.is_set():
            raise _ReadRefused([_refusal("now", _EXPIRED_RULE)])
        result = verifier.finish(
            observed_metadata=dict(stat_after),
            now=datetime.now(timezone.utc),
            cancelled=bool(cancel_event.is_set()),
        )
        if not result.complete:
            raise _ReadRefused(list(result.diagnostics))
        try:
            tail, summary = parser.finish()
        except Exception:
            raise _ReadRefused([_refusal("parser", _COOP_RULE)]) from None
        if type(tail) is tuple and tail:
            buffered.extend(tail)
        if len(buffered) > resolved_limits["max_rows"]:
            raise _ReadRefused([_refusal("parser", _POLICY_RULE)])
        parser_done = True
        frozen = tuple(buffered)
        candidat = _QualifiedImportUnits(
            complete=True,
            accepted_size=result.accepted_size,
            sha256=result.sha256,
            units=frozen,
            parser_complete=bool(summary.complete),
        )
    except _ReadRefused as failure:
        diags = list(failure.diagnostics)
    except _ServerCancelled:
        diags = [_refusal("cancel_event", _CANCEL_RULE)]
    except asyncio.TimeoutError:
        diags = [_refusal("now", _EXPIRED_RULE)]
    except asyncio.CancelledError as cancelled:
        externe = cancelled
        diags = []
    except Exception:
        diags = [_refusal("provider", _PROVIDER_RULE)]
    finally:
        if verifier is not None:
            try:
                if getattr(verifier, "_result", None) is None:
                    verifier.close("CANCELLED")
            except Exception:
                if externe is None:
                    diags.append(_refusal("verifier", _CLOSE_RULE))
        if not parser_done:
            try:
                parser.close("CANCELLED")
            except Exception:
                pass
        buffered.clear()
        if iterator is not None and not iterator_clos:
            try:
                ok = await _close_iterator_bounded(aclose_fn, remaining_fn=_remaining)
            except asyncio.CancelledError as cancelled:
                externe = externe or cancelled
                ok = False
            except Exception:
                ok = False
            iterator_clos = True
            if not ok and externe is None:
                diags.append(_refusal("aclose", _CLOSE_RULE))
            if not ok:
                candidat = None
    if externe is not None:
        raise externe
    if cancel_event.is_set() or _remaining() <= 0:
        return None, _pack(diags or [_refusal("now", _EXPIRED_RULE)])
    if candidat is not None and not diags:
        return candidat, []
    return None, _pack(diags or [_refusal("stream", _VERSION_RULE)])


async def read_private_object_once(
    *,
    trusted_ports: object,
    server_context: object,
    operation_reference: object,
    expected_metadata: object,
    policy_reference: object,
    policy_version: object,
    storage_resolver: object,
    expected_policy: object,
    deadline: object,
    now: object,
    cancel_event: object,
) -> tuple[_PrivateReadResult | None, list[Diagnostic]]:
    """Lit un objet privé qualifié sous contrôles actuels, sans remettre d'octets."""
    if type(trusted_ports) is not _BulkTrustedPorts:
        return None, _pack([_refusal("trusted_ports", _TRUSTED_RULE)])
    if server_context is None:
        return None, _pack([_refusal("server_context", _TRUSTED_RULE)])
    if not _is_opaque_text(operation_reference):
        return None, _pack([_refusal("operation_reference", _OPAQUE_RULE)])
    if type(expected_metadata) is not dict:
        return None, _pack([_refusal("expected_metadata", _OPAQUE_RULE)])
    if not _is_opaque_text(policy_reference):
        return None, _pack([_refusal("policy_reference", _OPAQUE_RULE)])
    if not _is_complete_semver(policy_version):
        return None, _pack([_refusal("policy_version", _OPAQUE_RULE)])
    if type(expected_policy) is not dict:
        return None, _pack([_refusal("expected_policy", _OPAQUE_RULE)])
    if type(deadline) is not datetime or deadline.tzinfo is not timezone.utc:
        return None, _pack([_refusal("deadline", _UTC_RULE)])
    if type(now) is not datetime or now.tzinfo is not timezone.utc:
        return None, _pack([_refusal("now", _UTC_RULE)])
    if type(cancel_event) is not asyncio.Event:
        return None, _pack([_refusal("cancel_event", _EVENT_RULE)])
    metadata_refusals = validate_object_metadata_values(dict(expected_metadata))
    if metadata_refusals:
        return None, _pack(list(metadata_refusals))
    policy_refusals = validate_bulk_policy_values(dict(expected_policy))
    if policy_refusals:
        return None, _pack(list(policy_refusals))
    contract_owned: dict = dict(expected_metadata)
    expected_limits: dict = dict(expected_policy)
    for key, value in tuple(expected_limits.items()):
        if type(value) is list:
            expected_limits[key] = list(value)
    references_owned = (policy_reference, policy_version)
    try:
        expires_at = contract_owned["expires_at"]
    except Exception:
        return None, _pack([_refusal("expected_metadata", _OPAQUE_RULE)])
    effective = deadline if deadline < expires_at else expires_at
    if not now < effective or cancel_event.is_set():
        return None, _pack([_refusal("now", _EXPIRED_RULE)])
    try:
        max_runtime = int(expected_limits["max_runtime_seconds"])
    except Exception:
        return None, _pack([_refusal("policy", _POLICY_RULE)])
    mono_start = time.monotonic()
    utc_start = datetime.now(timezone.utc)

    def _remaining() -> float:
        current_utc = datetime.now(timezone.utc)
        remaining_utc = (effective - current_utc).total_seconds()
        elapsed_mono = time.monotonic() - mono_start
        utc_budget = (deadline - utc_start).total_seconds()
        expiry_budget = (expires_at - utc_start).total_seconds() if isinstance(expires_at, datetime) else utc_budget
        mono_budget = utc_budget if utc_budget < expiry_budget else expiry_budget
        if max_runtime < mono_budget:
            mono_budget = max_runtime
        remaining_mono = mono_budget - elapsed_mono
        return remaining_utc if remaining_utc < remaining_mono else remaining_mono

    try:
        assessment, authority_refusals = trusted_ports.check_authority(
            server_context=server_context,
            action="EXECUTE",
            operation_reference=operation_reference,
            resource_reference=contract_owned["object_reference"],
        )
    except Exception:
        return None, _pack([_refusal("authority", _AUTHORITY_RULE)])
    if assessment is None:
        return None, _pack(list(authority_refusals) or [_refusal("authority", _AUTHORITY_RULE)])
    try:
        expected_context = assessment.resolved_context.as_values()
    except Exception:
        return None, _pack([_refusal("authority", _AUTHORITY_RULE)])
    if contract_owned["tenant_reference"] != expected_context.get("tenant_id"):
        return None, _pack([_refusal("tenant_reference", _TENANT_RULE)])
    try:
        resolution, governance_refusals = trusted_ports._resolve_governance_owned(
            server_context=server_context,
            expected_context=expected_context,
            contract_owned=dict(contract_owned),
            references_owned=(references_owned[0], references_owned[1]),
        )
    except Exception:
        return None, _pack([_refusal("governance", _GOVERNANCE_RULE)])
    if resolution is None:
        return None, _pack(list(governance_refusals) or [_refusal("governance", _GOVERNANCE_RULE)])
    try:
        resolved_limits = dict(resolution.as_values()["policy"]["limits"])
    except Exception:
        return None, _pack([_refusal("governance", _GOVERNANCE_RULE)])
    if resolved_limits != expected_limits:
        return None, _pack([_refusal("policy", _POLICY_RULE)])
    envelope = _capture_storage_resolver(storage_resolver)
    if envelope is None:
        return None, _pack([_refusal("storage_resolver", _RESOLVER_RULE)])
    verifier = None
    iterator = None
    anext_fn = None
    aclose_fn = None
    iterator_clos = False
    candidat: _PrivateReadResult | None = None
    diags: list[Diagnostic] = []
    externe: asyncio.CancelledError | None = None
    try:
        try:
            binding = await _run_with_event(
                lambda: envelope.qualify(
                    server_context, contract_owned["object_reference"], contract_owned["version_reference"]
                ),
                remaining_fn=_remaining,
                cancel_event=cancel_event,
            )
        except _ServerCancelled:
            raise _ReadRefused([_refusal("cancel_event", _CANCEL_RULE)])
        except asyncio.TimeoutError:
            raise _ReadRefused([_refusal("qualify", _EXPIRED_RULE)])
        except StopAsyncIteration:
            raise _ReadRefused([_refusal("qualify", _PROVIDER_RULE)])
        refused = _check_binding_exact(
            binding,
            object_reference=contract_owned["object_reference"],
            version_reference=contract_owned["version_reference"],
        )
        if refused:
            raise _ReadRefused(refused)
        stat_fn = binding.stat_private
        iter_fn = binding.iter_bytes
        try:
            stat_before = await _run_with_event(
                lambda: stat_fn(server_context, contract_owned["object_reference"], contract_owned["version_reference"]),
                remaining_fn=_remaining,
                cancel_event=cancel_event,
            )
        except _ServerCancelled:
            raise _ReadRefused([_refusal("cancel_event", _CANCEL_RULE)])
        except asyncio.TimeoutError:
            raise _ReadRefused([_refusal("stat_private", _EXPIRED_RULE)])
        except StopAsyncIteration:
            raise _ReadRefused([_refusal("stat_private", _PROVIDER_RULE)])
        if type(stat_before) is not dict or validate_object_metadata_values(dict(stat_before)):
            raise _ReadRefused([_refusal("observed_metadata", _VERSION_RULE)])
        if dict(stat_before) != dict(contract_owned):
            raise _ReadRefused([_refusal("observed_metadata", _VERSION_RULE)])
        if _remaining() <= 0 or cancel_event.is_set():
            raise _ReadRefused([_refusal("now", _EXPIRED_RULE)])
        created, verifier_refusals = new_object_integrity_verifier(
            metadata=dict(stat_before),
            expected_metadata=dict(contract_owned),
            policy=dict(resolved_limits),
            deadline=deadline,
            now=datetime.now(timezone.utc),
            cancelled=bool(cancel_event.is_set()),
        )
        if created is None:
            raise _ReadRefused(list(verifier_refusals))
        verifier = created
        try:
            maybe_iter = await _run_with_event(
                lambda: iter_fn(server_context, contract_owned["object_reference"], contract_owned["version_reference"]),
                remaining_fn=_remaining,
                cancel_event=cancel_event,
            )
        except _ServerCancelled:
            raise _ReadRefused([_refusal("cancel_event", _CANCEL_RULE)])
        except asyncio.TimeoutError:
            raise _ReadRefused([_refusal("iter_bytes", _EXPIRED_RULE)])
        except StopAsyncIteration:
            raise _ReadRefused([_refusal("iter_bytes", _PROVIDER_RULE)])
        iterator = maybe_iter
        anext_fn = _capture_python_method(iterator, "__anext__")
        aclose_fn = _capture_python_method(iterator, "aclose")
        if anext_fn is None or aclose_fn is None:
            raise _ReadRefused([_refusal("iter_bytes", _COOP_RULE)])
        if not inspect.iscoroutinefunction(anext_fn) or not inspect.iscoroutinefunction(aclose_fn):
            raise _ReadRefused([_refusal("iter_bytes", _COOP_RULE)])
        while True:
            if _remaining() <= 0 or cancel_event.is_set():
                raise _ReadRefused([_refusal("now", _EXPIRED_RULE)])
            try:
                chunk = await _run_with_event(anext_fn, remaining_fn=_remaining, cancel_event=cancel_event)
            except StopAsyncIteration:
                break
            except _ServerCancelled:
                raise _ReadRefused([_refusal("cancel_event", _CANCEL_RULE)])
            except asyncio.TimeoutError:
                raise _ReadRefused([_refusal("iter_bytes", _EXPIRED_RULE)])
            if _remaining() <= 0:
                raise _ReadRefused([_refusal("now", _EXPIRED_RULE)])
            feed_refusals = verifier.feed(chunk, now=datetime.now(timezone.utc), cancelled=bool(cancel_event.is_set()))
            if feed_refusals:
                raise _ReadRefused(list(feed_refusals))
        try:
            stat_after = await _run_with_event(
                lambda: stat_fn(server_context, contract_owned["object_reference"], contract_owned["version_reference"]),
                remaining_fn=_remaining,
                cancel_event=cancel_event,
            )
        except _ServerCancelled:
            raise _ReadRefused([_refusal("cancel_event", _CANCEL_RULE)])
        except asyncio.TimeoutError:
            raise _ReadRefused([_refusal("stat_private", _EXPIRED_RULE)])
        except StopAsyncIteration:
            raise _ReadRefused([_refusal("stat_private", _PROVIDER_RULE)])
        if type(stat_after) is not dict or validate_object_metadata_values(dict(stat_after)):
            raise _ReadRefused([_refusal("observed_metadata", _VERSION_RULE)])
        if dict(stat_after) != dict(contract_owned):
            raise _ReadRefused([_refusal("observed_metadata", _VERSION_RULE)])
        if _remaining() <= 0 or cancel_event.is_set():
            raise _ReadRefused([_refusal("now", _EXPIRED_RULE)])
        result = verifier.finish(
            observed_metadata=dict(stat_after),
            now=datetime.now(timezone.utc),
            cancelled=bool(cancel_event.is_set()),
        )
        if not result.complete:
            raise _ReadRefused(list(result.diagnostics))
        candidat = _PrivateReadResult(complete=True, accepted_size=result.accepted_size, sha256=result.sha256)
    except _ReadRefused as failure:
        diags = list(failure.diagnostics)
    except _ServerCancelled:
        diags = [_refusal("cancel_event", _CANCEL_RULE)]
    except asyncio.TimeoutError:
        diags = [_refusal("now", _EXPIRED_RULE)]
    except asyncio.CancelledError as cancelled:
        externe = cancelled
        diags = []
    except Exception:
        diags = [_refusal("provider", _PROVIDER_RULE)]
    finally:
        if verifier is not None:
            try:
                if getattr(verifier, "_result", None) is None:
                    verifier.close("CANCELLED")
            except Exception:
                if externe is None:
                    diags.append(_refusal("verifier", _CLOSE_RULE))
        if iterator is not None and not iterator_clos:
            try:
                ok = await _close_iterator_bounded(aclose_fn, remaining_fn=_remaining)
            except asyncio.CancelledError as cancelled:
                externe = externe or cancelled
                ok = False
            except Exception:
                ok = False
            iterator_clos = True
            if not ok and externe is None:
                diags.append(_refusal("aclose", _CLOSE_RULE))
            if not ok:
                candidat = None
    if externe is not None:
        raise externe
    if cancel_event.is_set() or _remaining() <= 0:
        return None, _pack(diags or [_refusal("now", _EXPIRED_RULE)])
    if candidat is not None and not diags:
        return candidat, []
    return None, _pack(diags or [_refusal("stream", _VERSION_RULE)])
