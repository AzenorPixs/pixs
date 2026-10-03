"""Bounded static shell adapter, preloaded bytes, no per-request read.

Contract: `build_shell_views(dist_root)` takes an EXPLICIT build root
(exact non-empty `str` or safe `Path`, portable) and returns a FINITE
mapping `filename -> handler` with preloaded frozen bytes. Only
`index.html` and regular non-hidden `assets` `js`/`css` files without
symlink are read under that root. Each read is bounded (`max 1MiB`),
`max 64 files`, total budget `8MiB` documented as internal choices.
`GET` returns 200 with the exact body, `HEAD` returns 200 without body
and the `Content-Length` of `GET`, other methods return 405 empty with
`Allow: GET, HEAD`. All responses use the exact MIME and
`Cache-Control: no-store`. Bad construction raises fixed
`ShellAdapterError` without raw path or chain. No public URL is
distributed by this module.

Limits: pure module import (no Django import or filesystem read at
import, `dist` access only inside the factory); no `settings.configure`,
`django.setup`, server, DB, socket or secret in this module.
"""

from __future__ import annotations

import os
import stat
from pathlib import Path

__all__ = [
    "ShellAdapterError",
    "build_shell_views",
]

_ERROR = "Invalid shell distribution."
_MAX_FILE_SIZE = 1048576
_MAX_FILE_COUNT = 64
_MAX_TOTAL_SIZE = 8388608
_INDEX_KEY = "index.html"
_ASSETS_DIRNAME = "assets"
_ASSETS_PREFIX = "assets/"
_ALLOW_VALUE = "GET, HEAD"
_NO_STORE = "no-store"
_MIME_BY_SUFFIX = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript",
    ".css": "text/css",
}


class ShellAdapterError(ValueError):
    """Stable shell adapter error, without raw path echo."""

    def __init__(self, message: str = _ERROR) -> None:
        super().__init__(message)


def _invalid_distribution() -> ShellAdapterError:
    return ShellAdapterError(_ERROR)


def _require_dist_root(dist_root: object) -> int:
    if type(dist_root) not in (str, type(Path())):
        raise _invalid_distribution()
    if type(dist_root) is str and dist_root == "":
        raise _invalid_distribution()
    try:
        candidate = Path(dist_root)
        if ".." in candidate.parts:
            raise _invalid_distribution()
        if any(ord(character) < 32 or ord(character) == 127
               for character in str(candidate)):
            raise _invalid_distribution()
        return os.open(candidate, os.O_RDONLY | os.O_DIRECTORY
                       | os.O_NOFOLLOW | os.O_NONBLOCK)
    except ShellAdapterError:
        raise
    except Exception:
        raise _invalid_distribution() from None


def _require_method(request: object) -> str:
    try:
        method = getattr(request, "method", None)
    except Exception:
        raise _invalid_distribution() from None
    if type(method) is not str:
        raise _invalid_distribution()
    return method


def _check_segment_text(segment: str) -> None:
    if segment == "" or segment in (".", ".."):
        raise _invalid_distribution()
    if segment.startswith(".") or segment.endswith("."):
        raise _invalid_distribution()
    if ".." in segment:
        raise _invalid_distribution()
    for character in segment:
        valid = ("A" <= character <= "Z" or "a" <= character <= "z"
                 or "0" <= character <= "9" or character in ("-", "_", "."))
        if not valid:
            raise _invalid_distribution()
    for codepoint in map(ord, segment):
        if codepoint < 32 or codepoint == 127 or codepoint > 127:
            raise _invalid_distribution()


def _read_bounded_nofollow(directory_fd: int, name: str,
                           remaining_total: int) -> bytes:
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                     dir_fd=directory_fd)
    except Exception:
        raise _invalid_distribution() from None
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise _invalid_distribution()
        maximum = min(_MAX_FILE_SIZE, remaining_total)
        chunks: list[bytes] = []
        remaining = maximum + 1
        while remaining > 0:
            chunk = os.read(fd, min(65536, remaining))
            if chunk == b"":
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        data = b"".join(chunks)
        if len(data) > maximum:
            raise _invalid_distribution()
        return data
    except ShellAdapterError:
        raise
    except Exception:
        raise _invalid_distribution() from None
    finally:
        try:
            os.close(fd)
        except Exception:
            raise _invalid_distribution() from None


def _mime_for(relative_key: str) -> str:
    if relative_key == _INDEX_KEY:
        return _MIME_BY_SUFFIX[".html"]
    if relative_key.startswith(_ASSETS_PREFIX):
        stem = relative_key[len(_ASSETS_PREFIX):]
        if stem.endswith(".js"):
            return _MIME_BY_SUFFIX[".js"]
        if stem.endswith(".css"):
            return _MIME_BY_SUFFIX[".css"]
    raise _invalid_distribution()


def _collect_files(root_fd: int) -> dict[str, bytes]:
    try:
        assets_fd = os.open(_ASSETS_DIRNAME, os.O_RDONLY | os.O_DIRECTORY
                            | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=root_fd)
    except Exception:
        raise _invalid_distribution() from None
    try:
        names: list[str] = []
        with os.scandir(assets_fd) as entries:
            for entry in entries:
                if len(names) >= _MAX_FILE_COUNT - 1:
                    raise _invalid_distribution()
                name = entry.name
                _check_segment_text(name)
                if not (name.endswith(".js") or name.endswith(".css")):
                    raise _invalid_distribution()
                names.append(name)
        index_body = _read_bounded_nofollow(root_fd, _INDEX_KEY, _MAX_TOTAL_SIZE)
        collected = {_INDEX_KEY: index_body}
        total = len(index_body)
        for name in sorted(names):
            data = _read_bounded_nofollow(assets_fd, name, _MAX_TOTAL_SIZE - total)
            total += len(data)
            collected[_ASSETS_PREFIX + name] = data
        return collected
    except ShellAdapterError:
        raise
    except Exception:
        raise _invalid_distribution() from None
    finally:
        try:
            os.close(assets_fd)
        except Exception:
            raise _invalid_distribution() from None


def build_shell_views(dist_root: object) -> dict[str, object]:
    """Build the finite filename to handler mapping from one dist root."""
    root_fd = _require_dist_root(dist_root)
    try:
        files = _collect_files(root_fd)
    finally:
        try:
            os.close(root_fd)
        except Exception:
            raise _invalid_distribution() from None
    views: dict[str, object] = {}
    for relative_key, body in files.items():
        mime = _mime_for(relative_key)

        def make_handler(locked_body: bytes = body, locked_mime: str = mime):
            def shell_handler(request: object) -> object:
                method = _require_method(request)
                from django.http import HttpResponse

                if method == "GET":
                    response = HttpResponse(locked_body, status=200, content_type=locked_mime)
                    response["Cache-Control"] = _NO_STORE
                    response["Content-Length"] = str(len(locked_body))
                    return response
                if method == "HEAD":
                    response = HttpResponse(b"", status=200, content_type=locked_mime)
                    response["Cache-Control"] = _NO_STORE
                    response["Content-Length"] = str(len(locked_body))
                    return response
                denied = HttpResponse(b"", status=405, content_type=locked_mime)
                denied["Cache-Control"] = _NO_STORE
                denied["Allow"] = _ALLOW_VALUE
                return denied

            return shell_handler

        views[relative_key] = make_handler()
    return views
