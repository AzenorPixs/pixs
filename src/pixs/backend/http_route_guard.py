"""Garde Django de déclaration explicite des routes et refus fermé.

Contrat : `build_declared_urlpatterns` reçoit explicitement une séquence
exacte de type `tuple` ou `list` de `RouteDeclaration` exactes et retourne
des `urlpatterns` Django avec un catchall final. Seul `public=True` expose
son handler fourni. `public=False` retourne 403 fixe sans appeler le
handler. L’inconnu retourne 404 fixe sans echo du chemin, secret ou trace.
La racine vide `""` est une déclaration explicite admise et testée.
Les littéraux de fichiers statiques avec points internes (`index.html`,
`assets/index-HASH.js`) sont admis ; aucun wildcard, converter,
dot-segment, chemin caché ou traversal n'est admis.
Aucune route concrète n’est distribuée.

Limites : aucun import/config Django au simple import ; aucun
`settings.configure`, `django.setup`, serveur ou I/O dans ce module ; aucune
lecture externe ; handlers externes et conformité HTTP hors portée.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "HttpRouteGuardError",
    "RouteDeclaration",
    "build_declared_urlpatterns",
]

_ERROR = "Déclaration de route invalide."
_PRIVATE_ROUTE_RESPONSE = "Route non publique."
_UNKNOWN_ROUTE_RESPONSE = "Route inconnue."


class HttpRouteGuardError(ValueError):
    """Erreur stable de garde, sans echo de valeur brute."""

    def __init__(self, message: str = _ERROR) -> None:
        super().__init__(message)


@dataclass(frozen=True)
class RouteDeclaration:
    """Déclaration immuable exacte : path relatif, nom unique, handler, public."""

    path: str
    name: str
    handler: object
    public: bool


def _invalid_declaration() -> HttpRouteGuardError:
    return HttpRouteGuardError(_ERROR)


def _require_exact_string(value: object) -> str:
    if type(value) is not str:
        raise _invalid_declaration()
    return value


def _reject_control_characters(text: str) -> None:
    for character in text:
        codepoint = ord(character)
        if codepoint < 32 or codepoint == 127:
            raise _invalid_declaration()


def _require_path(path: object) -> str:
    text = _require_exact_string(path)
    if text == "":
        return text
    _reject_control_characters(text)
    if text.startswith("/"):
        raise _invalid_declaration()
    if "//" in text:
        raise _invalid_declaration()
    for forbidden in ("?", "#", "*", "<", ">", ":", "(", ")", "[", "]",
                      "{", "}", "^", "$", "+", "|", "\\", "%"):
        if forbidden in text:
            raise _invalid_declaration()
    path_body = text[:-1] if text.endswith("/") else text
    if path_body == "":
        raise _invalid_declaration()
    for segment in path_body.split("/"):
        if segment == "":
            raise _invalid_declaration()
        if segment in (".", ".."):
            raise _invalid_declaration()
        if segment.startswith(".") or segment.endswith("."):
            raise _invalid_declaration()
        if ".." in segment:
            raise _invalid_declaration()
        for character in segment:
            valid = ("A" <= character <= "Z" or "a" <= character <= "z"
                    or "0" <= character <= "9" or character in ("-", "_", "."))
            if not valid:
                raise _invalid_declaration()
    return text


def _require_name(name: object) -> str:
    text = _require_exact_string(name)
    if text == "" or text.strip() != text:
        raise _invalid_declaration()
    _reject_control_characters(text)
    if "/" in text or " " in text or "\t" in text:
        raise _invalid_declaration()
    return text


def _require_handler(handler: object) -> object:
    if not callable(handler):
        raise _invalid_declaration()
    return handler


def _require_public(public: object) -> bool:
    if type(public) is not bool:
        raise _invalid_declaration()
    return public


def _require_declarations(declarations: object) -> tuple:
    if type(declarations) is not tuple and type(declarations) is not list:
        raise _invalid_declaration()
    elements = tuple(declarations)
    seen_paths: set[str] = set()
    seen_names: set[str] = set()
    for element in elements:
        if type(element) is not RouteDeclaration:
            raise _invalid_declaration()
        route_path = _require_path(element.path)
        name = _require_name(element.name)
        _require_handler(element.handler)
        _require_public(element.public)
        if route_path in seen_paths or name in seen_names:
            raise _invalid_declaration()
        seen_paths.add(route_path)
        seen_names.add(name)
    return elements


def build_declared_urlpatterns(declarations: object) -> list:
    """Construit les urlpatterns déclarés avec catchall final 404 fixe."""
    elements = _require_declarations(declarations)
    from django.http import HttpResponse
    from django.urls import path
    from django.urls import re_path

    patterns: list = []
    for element in elements:
        if element.public is True:
            patterns.append(path(element.path, element.handler, name=element.name))
        else:
            def reject_private_route(_request):
                return HttpResponse(_PRIVATE_ROUTE_RESPONSE, status=403,
                                    content_type="text/plain; charset=utf-8")
            patterns.append(path(element.path, reject_private_route, name=element.name))

    def reject_unknown_route(_request):
        return HttpResponse(_UNKNOWN_ROUTE_RESPONSE, status=404,
                            content_type="text/plain; charset=utf-8")

    patterns.append(re_path(r"\A[\s\S]*\Z", reject_unknown_route))
    return patterns
