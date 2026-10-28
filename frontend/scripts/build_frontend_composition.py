"""Pont de projection frontend : Kernel réel, aucune activation de code client.

L'API pure reçoit les attestations authentifiées par l'appelant. La CLI
n'en fabrique aucune : une composition qui en exige est refusée sans elles.
Les empreintes tracent les textes ; elles ne prouvent pas leur authenticité.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys
from collections.abc import Mapping
import uuid


class BuildError(ValueError):
    def __init__(self, code: str, diagnostics: tuple = ()) -> None:
        super().__init__(code)
        self.code = code
        self.diagnostics = tuple(diagnostics)


def _relative(value: object, *, output: bool = False) -> tuple[str, ...]:
    if type(value) is not str or not value:
        raise BuildError('BUILD_PATH_INVALID')
    try:
        value.encode('utf-8')
    except UnicodeEncodeError as error:
        raise BuildError('BUILD_PATH_INVALID') from error
    parts = value.split('/')
    forbidden = {'.git', '.venv', 'venv', 'env', 'logs', 'node_modules', '.opencode', '.cache', '__pycache__'}
    if ('\\' in value or PurePosixPath(value).is_absolute()
            or PurePosixPath(value).as_posix() != value
            or any(not part or part in {'.', '..'} or part in forbidden for part in parts)
            or any(ord(char) < 32 or ord(char) == 127 for char in value)):
        raise BuildError('BUILD_PATH_INVALID')
    if output:
        if parts[:2] != ['frontend', '.generated'] or len(parts) < 3 or not parts[-1].endswith('.json'):
            raise BuildError('BUILD_OUTPUT_INVALID')
    elif parts[-1] != 'component.toml':
        raise BuildError('BUILD_SOURCE_INVALID')
    return tuple(parts)


@dataclass(frozen=True, slots=True)
class BuildLimits:
    max_manifests: int
    max_manifest_bytes: int
    max_total_bytes: int
    allowed_sources: tuple[str, ...]

    def __post_init__(self) -> None:
        if any(type(value) is not int or value < 1 for value in
               (self.max_manifests, self.max_manifest_bytes, self.max_total_bytes)):
            raise BuildError('BUILD_LIMITS_INVALID')
        if type(self.allowed_sources) is not tuple or not self.allowed_sources:
            raise BuildError('BUILD_LIMITS_INVALID')
        for source in self.allowed_sources:
            _relative(source)
        if len(set(self.allowed_sources)) != len(self.allowed_sources):
            raise BuildError('BUILD_LIMITS_INVALID')


@dataclass(frozen=True, slots=True)
class PlanDiagnostic:
    stage: str
    element: str
    constraint: str
    message: str

    def __post_init__(self) -> None:
        if any(type(value) is not str for value in (self.stage, self.element, self.constraint, self.message)):
            raise BuildError('BUILD_PLAN_INVALID')

    @classmethod
    def from_kernel(cls, value):
        return cls(value.step, value.element, value.constraint, value.message)

    def to_dict(self) -> dict:
        return {'stage': self.stage, 'element': self.element,
                'constraint': self.constraint, 'message': self.message}


@dataclass(frozen=True, slots=True)
class PlanFacet:
    owner: str
    owner_version: str
    type: str
    id: str
    entry: str
    version: str
    requires: tuple[str, ...]
    scope: str

    def __post_init__(self) -> None:
        if any(type(value) is not str or not value for value in
               (self.owner, self.owner_version, self.type, self.id, self.entry, self.version, self.scope)):
            raise BuildError('BUILD_PLAN_INVALID')
        if type(self.requires) is not tuple or any(type(value) is not str for value in self.requires):
            raise BuildError('BUILD_PLAN_INVALID')

    def to_dict(self) -> dict:
        return {'owner': self.owner, 'owner_version': self.owner_version,
                'type': self.type, 'id': self.id, 'entry': self.entry,
                'version': self.version, 'requires': list(self.requires), 'scope': self.scope}


@dataclass(frozen=True, slots=True)
class BuildPlan:
    order: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]
    facets: tuple[PlanFacet, ...]
    warnings: tuple[PlanDiagnostic, ...]
    evaluation_scope: tuple[str, ...]
    unevaluated_dimensions: tuple[str, ...]
    sources_sha256: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        fields = (self.order, self.edges, self.facets, self.warnings, self.evaluation_scope,
                  self.unevaluated_dimensions, self.sources_sha256)
        if any(type(value) is not tuple for value in fields):
            raise BuildError('BUILD_PLAN_INVALID')
        if any(type(value) is not str for value in self.order + self.evaluation_scope + self.unevaluated_dimensions):
            raise BuildError('BUILD_PLAN_INVALID')
        if len(set(self.order)) != len(self.order):
            raise BuildError('BUILD_PLAN_INVALID')
        if any(type(edge) is not tuple or len(edge) != 2 or any(type(value) is not str or value not in self.order for value in edge) for edge in self.edges):
            raise BuildError('BUILD_PLAN_INVALID')
        if any(type(value) is not PlanFacet or value.owner not in self.order for value in self.facets):
            raise BuildError('BUILD_PLAN_INVALID')
        if any(type(value) is not PlanDiagnostic for value in self.warnings):
            raise BuildError('BUILD_PLAN_INVALID')
        if len(self.sources_sha256) != len(self.order):
            raise BuildError('BUILD_PLAN_INVALID')
        for owner, pair in zip(self.order, self.sources_sha256, strict=True):
            if (type(pair) is not tuple or len(pair) != 2 or pair[0] != owner
                    or type(pair[1]) is not str or len(pair[1]) != 64
                    or any(char not in '0123456789abcdef' for char in pair[1])):
                raise BuildError('BUILD_PLAN_INVALID')

    @property
    def globally_compatible(self) -> bool:
        return False

    def to_dict(self) -> dict:
        return {'schema': 'pixs.frontend.build-plan/1', 'order': list(self.order),
                'edges': [list(edge) for edge in self.edges],
                'facets': [facet.to_dict() for facet in self.facets],
                'diagnostics': [], 'warnings': [item.to_dict() for item in self.warnings],
                'evaluation_scope': list(self.evaluation_scope),
                'unevaluated_dimensions': list(self.unevaluated_dimensions),
                'globally_compatible': False,
                'sources_sha256': [{'owner': owner, 'sha256': digest}
                                   for owner, digest in self.sources_sha256]}


def _selection(value: object) -> tuple[str, ...]:
    if type(value) is not tuple or any(type(item) is not str or not item or '\x00' in item for item in value):
        raise BuildError('BUILD_SELECTION_INVALID')
    if len(set(value)) != len(value):
        raise BuildError('BUILD_SELECTION_INVALID')
    return value


def _texts(values: object, limits: BuildLimits) -> tuple[bytes, ...]:
    if type(limits) is not BuildLimits:
        raise BuildError('BUILD_LIMITS_INVALID')
    limits.__post_init__()
    if type(values) is not tuple or not values or len(values) > limits.max_manifests:
        raise BuildError('BUILD_MANIFEST_COUNT_INVALID')
    result = []
    total = 0
    for text in values:
        if type(text) is not str or '\x00' in text:
            raise BuildError('BUILD_TEXT_INVALID')
        try:
            raw = text.encode('utf-8')
        except UnicodeEncodeError as error:
            raise BuildError('BUILD_TEXT_INVALID') from error
        if len(raw) > limits.max_manifest_bytes:
            raise BuildError('BUILD_MANIFEST_TOO_LARGE')
        total += len(raw)
        if total > limits.max_total_bytes:
            raise BuildError('BUILD_TOTAL_TOO_LARGE')
        result.append(raw)
    return tuple(result)


def build_plan(manifest_texts: tuple[str, ...], *, official_ids: tuple[str, ...],
               required_ids: tuple[str, ...], configured_providers: Mapping[str, str] | None,
               attestations: tuple, limits: BuildLimits) -> BuildPlan:
    raw_texts = _texts(manifest_texts, limits)
    official = _selection(official_ids)
    required = _selection(required_ids)
    if configured_providers is not None:
        if not isinstance(configured_providers, Mapping) or any(
            type(key) is not str or not key or type(value) is not str or not value
            or '\x00' in key or '\x00' in value for key, value in configured_providers.items()
        ):
            raise BuildError('BUILD_SELECTION_INVALID')
        providers = dict(configured_providers)
    else:
        providers = None
    if type(attestations) is not tuple:
        raise BuildError('BUILD_ATTESTATIONS_INVALID')
    from pixs.kernel.composition import compose, validate
    validated, diagnostics = validate(manifest_texts, official_ids=official, required_ids=required)
    if diagnostics:
        raise BuildError('BUILD_KERNEL_REJECTED', tuple(PlanDiagnostic.from_kernel(item) for item in diagnostics))
    result = compose(manifest_texts, official_ids=official, required_ids=required,
                     configured_providers=providers, attestations=attestations)
    if not result.activated or result.diagnostics:
        raise BuildError('BUILD_KERNEL_REJECTED', tuple(PlanDiagnostic.from_kernel(item) for item in result.diagnostics))
    by_id = {manifest.id: manifest for manifest in validated}
    digests = {manifest.id: hashlib.sha256(raw).hexdigest()
               for manifest, raw in zip(validated, raw_texts, strict=True)}
    facets = []
    for owner in result.order:
        manifest = by_id[owner]
        if manifest.frontend is not None:
            for item in manifest.frontend.contributions:
                facets.append(PlanFacet(owner, manifest.version, item.type, item.id,
                                        item.entry, item.version, tuple(item.requires), item.scope))
    return BuildPlan(tuple(result.order), tuple(tuple(edge) for edge in result.edges),
                     tuple(facets), tuple(PlanDiagnostic.from_kernel(item) for item in result.warnings),
                     tuple(result.evaluation_scope), tuple(result.unevaluated_dimensions),
                     tuple((owner, digests[owner]) for owner in result.order))


def _project_root(value: object) -> Path:
    try:
        candidate = Path(value)
        expected = Path(__file__).resolve().parents[2]
        if not candidate.is_absolute() or candidate.resolve(strict=True) != expected:
            raise BuildError('BUILD_ROOT_INVALID')
        return expected
    except (OSError, TypeError, ValueError) as error:
        if isinstance(error, BuildError):
            raise
        raise BuildError('BUILD_ROOT_INVALID') from error


@contextmanager
def _directory(root: Path, parts: tuple[str, ...], *, create: bool = False):
    fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in parts:
            if create:
                try:
                    os.mkdir(part, dir_fd=fd)
                except FileExistsError:
                    pass
            next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            previous_fd = fd
            fd = next_fd
            os.close(previous_fd)
        yield fd
    finally:
        os.close(fd)


def read_manifest_texts(paths: tuple[str, ...], *, project_root: Path,
                        limits: BuildLimits) -> tuple[str, ...]:
    root = _project_root(project_root)
    if type(limits) is not BuildLimits:
        raise BuildError('BUILD_LIMITS_INVALID')
    limits.__post_init__()
    if type(paths) is not tuple or not paths or len(paths) > limits.max_manifests:
        raise BuildError('BUILD_MANIFEST_COUNT_INVALID')
    parts = tuple(_relative(path) for path in paths)
    if len(set(paths)) != len(paths) or any(path not in limits.allowed_sources for path in paths):
        raise BuildError('BUILD_SOURCE_FORBIDDEN')
    texts = []
    total = 0
    for names in parts:
        limit = min(limits.max_manifest_bytes, limits.max_total_bytes - total)
        try:
            with _directory(root, names[:-1]) as folder:
                fd = os.open(names[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=folder)
                with os.fdopen(fd, 'rb') as source:
                    if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                        raise BuildError('BUILD_SOURCE_INVALID')
                    raw = source.read(limit + 1)
        except OSError as error:
            raise BuildError('BUILD_SOURCE_UNAVAILABLE') from error
        if len(raw) > limit:
            raise BuildError('BUILD_SOURCE_TOO_LARGE')
        total += len(raw)
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError as error:
            raise BuildError('BUILD_TEXT_INVALID') from error
        texts.append(text)
    result = tuple(texts)
    _texts(result, limits)
    return result


def write_plan(plan: BuildPlan, *, project_root: Path, output: str) -> None:
    root = _project_root(project_root)
    names = _relative(output, output=True)
    if type(plan) is not BuildPlan:
        raise BuildError('BUILD_PLAN_INVALID')
    payload = (json.dumps(plan.to_dict(), ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')
    temporary = '.composition-' + uuid.uuid4().hex + '.tmp'
    try:
        with _directory(root, names[:-1], create=True) as folder:
            try:
                existing = os.stat(names[-1], dir_fd=folder, follow_symlinks=False)
            except FileNotFoundError:
                existing = None
            if existing is not None and not stat.S_ISREG(existing.st_mode):
                raise BuildError('BUILD_OUTPUT_INVALID')
            created = False
            try:
                fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=folder)
                created = True
                with os.fdopen(fd, 'wb') as target:
                    target.write(payload)
                    target.flush()
                    os.fsync(target.fileno())
                os.replace(temporary, names[-1], src_dir_fd=folder, dst_dir_fd=folder)
                created = False
            finally:
                if created:
                    os.unlink(temporary, dir_fd=folder)
    except OSError as error:
        raise BuildError('BUILD_OUTPUT_UNAVAILABLE') from error


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise BuildError('BUILD_SELECTION_INVALID')
        result[key] = value
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='Projeter les facettes sans activer le frontend.')
    parser.add_argument('--manifest', action='append', required=True)
    parser.add_argument('--project-root', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--allowed-sources-json', required=True)
    parser.add_argument('--official-ids-json', required=True)
    parser.add_argument('--required-ids-json', required=True)
    parser.add_argument('--configured-providers-json', required=True)
    parser.add_argument('--max-manifests', type=int, required=True)
    parser.add_argument('--max-manifest-bytes', type=int, required=True)
    parser.add_argument('--max-total-bytes', type=int, required=True)
    args = parser.parse_args(argv)
    try:
        allowed = json.loads(args.allowed_sources_json, object_pairs_hook=_pairs)
        official = json.loads(args.official_ids_json, object_pairs_hook=_pairs)
        required = json.loads(args.required_ids_json, object_pairs_hook=_pairs)
        providers = json.loads(args.configured_providers_json, object_pairs_hook=_pairs)
        if any(type(value) is not list for value in (allowed, official, required)):
            raise BuildError('BUILD_SELECTION_INVALID')
        limits = BuildLimits(args.max_manifests, args.max_manifest_bytes, args.max_total_bytes, tuple(allowed))
        root = _project_root(args.project_root)
        texts = read_manifest_texts(tuple(args.manifest), project_root=root, limits=limits)
        plan = build_plan(texts, official_ids=tuple(official), required_ids=tuple(required),
                          configured_providers=providers, attestations=(), limits=limits)
        write_plan(plan, project_root=root, output=args.out)
        return 0
    except json.JSONDecodeError:
        sys.stderr.write('BUILD_SELECTION_INVALID\n')
        return 2
    except BuildError as error:
        sys.stderr.write(error.code + '\n')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
