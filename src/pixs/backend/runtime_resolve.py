"""Branchement runtime C01 vers reglages Django, sans muter gabarits."""
from __future__ import annotations
from pixs.backend.checks import check_template
from pixs.backend.settings import SettingsTemplate
from pixs.backend.bootstrap_policy import PolicySource
from pixs.backend.systemd_secret_provider import provider as _provider
from pixs.backend.startup_mode import StartupMode
__all__ = ["RuntimeDjangoSettings", "resolve_runtime_settings"]
_RUNTIME_KEY = object()
def _refus() -> ValueError:
    return ValueError("runtime C01 refuse")
class RuntimeDjangoSettings:
    __slots__ = ("_bundle", "_template")
    def __init__(self, _key: object, bundle, template: SettingsTemplate) -> None:
        if _key is not _RUNTIME_KEY:
            raise _refus() from None
        if type(template) is not SettingsTemplate:
            raise _refus() from None
        object.__setattr__(self, "_bundle", bundle)
        object.__setattr__(self, "_template", template)
    def __repr__(self) -> str:
        return "RuntimeDjangoSettings(<redacted>, ready=False)"
    def __str__(self) -> str:
        return "RuntimeDjangoSettings(<redacted>, ready=False)"
    def __reduce__(self):
        raise _refus() from None
    def __reduce_ex__(self, protocol):
        raise _refus() from None
    @property
    def ready(self) -> bool:
        return False
    def as_dict(self) -> dict:
        template = object.__getattribute__(self, "_template")
        bundle = object.__getattribute__(self, "_bundle")
        try:
            mapping = bundle.consume()
        except (ValueError, OSError, UnicodeError):
            raise _refus() from None
        if type(mapping) is not dict or len(mapping) != 2:
            raise _refus() from None
        k1 = (template.secret_key_ref.owner_id, template.secret_key_ref.entry_id, template.secret_key_ref.source)
        k2 = (template.database_password_ref.owner_id, template.database_password_ref.entry_id, template.database_password_ref.source)
        if k1 == k2:
            raise _refus() from None
        if set(mapping.keys()) != {k1, k2}:
            raise _refus() from None
        v1 = mapping[k1]
        v2 = mapping[k2]
        for v in (v1, v2):
            if type(v) is not str or not v or "\x00" in v:
                raise _refus() from None
        try:
            base = template.non_secret_settings
        except (ValueError, OSError, UnicodeError):
            raise _refus() from None
        if type(base) is not dict:
            raise _refus() from None
        try:
            dbs = base["DATABASES"]
            default = dbs["default"]
            payload_dbs = {"default": dict(default)}
            payload = dict(base)
            payload["DATABASES"] = payload_dbs
        except (KeyError, TypeError, ValueError):
            raise _refus() from None
        payload["SECRET_KEY"] = v1
        payload["DATABASES"]["default"]["PASSWORD"] = v2
        if "READY" in payload or "P0_READY" in payload:
            raise _refus() from None
        return payload
def resolve_runtime_settings(*, template: SettingsTemplate, source: PolicySource, mode: StartupMode, purpose: str):
    if type(template) is not SettingsTemplate:
        raise _refus() from None
    if type(source) is not PolicySource:
        raise _refus() from None
    if mode is not StartupMode.INSTALLER:
        raise _refus() from None
    if type(purpose) is not str or not purpose:
        raise _refus() from None
    try:
        report = check_template(template)
    except (ValueError, OSError, UnicodeError):
        raise _refus() from None
    if type(report) is not dict:
        raise _refus() from None
    if report.get("template_valid") is not True or report.get("ready") is not False or report.get("secrets_resolved") is not False:
        raise _refus() from None
    if report.get("selected_profile") != template.profile:
        raise _refus() from None
    refs = (template.secret_key_ref, template.database_password_ref)
    if refs[0] == refs[1]:
        raise _refus() from None
    try:
        bundle = _provider.resolve_secrets(source, mode=mode, role=template.profile, purpose=purpose, references=refs)
    except (ValueError, OSError, UnicodeError):
        raise _refus() from None
    from pixs.backend.systemd_secret_provider.provider import SecretBundle as _B
    if type(bundle) is not _B:
        raise _refus() from None
    return RuntimeDjangoSettings(_RUNTIME_KEY, bundle, template)
