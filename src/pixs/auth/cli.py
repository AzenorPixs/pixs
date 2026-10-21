"""Façade CLI interactive serveur : Bearer opaque en mémoire, refresh en trousseau qualifié.

L'hôte fournit les mandats publics et le service ; aucune activation ni CLI
processus n'est installée par cet adaptateur. Aucun jeton n'est renvoyé dans
les résultats destinés à l'affichage.
"""
from __future__ import annotations
from dataclasses import dataclass
from pixs.auth.contracts import AuthResult,AuthOutcome,AuditDisposition,CredentialDisposition,SessionInfo,Facade,LoginInput,AuthServiceError
from pixs.auth.tokens import TokenKind
from pixs.auth.identifiers import identity_reference
from pixs.auth.cli_vault import MemoryRefreshVault,AuthVaultError,_namespace


@dataclass(frozen=True,slots=True)
class CliAuthStatus:
    outcome: AuthOutcome
    audit: AuditDisposition
    operation_id: str
    session: SessionInfo|None
    credential: CredentialDisposition|None
    storage_mode: str
    local_clear_confirmed: bool


class CliAuthFacade:
    def __init__(self,*,service,origin,vault):
        # L'origine ne constitue pas une preuve serveur ; elle isole le trousseau.
        from pixs.auth.identifiers import new_uuid7
        _namespace(origin,identity_reference(new_uuid7()))
        if not isinstance(vault,MemoryRefreshVault): raise AuthServiceError("AUTH_INPUT_INVALID")
        self._service,self._origin,self._vault=service,origin,vault
        self._access,self._identity,self._session_id=None,None,None
    def _forget(self):
        self._access=None
        confirmed=True
        if self._identity is not None:
            try: self._vault.clear(self._origin,self._identity)
            except AuthVaultError: confirmed=False
        self._identity,self._session_id=None,None
        return confirmed
    def _accept(self,result,*,retire_local=True):
        if type(result) is not AuthResult: raise AuthServiceError("AUTH_STATE_UNAVAILABLE")
        result.__post_init__()
        cleared=True
        if result.outcome is AuthOutcome.ISSUED:
            if result.session.facade is not Facade.API or result.emission.access is None or result.emission.refresh is None:
                raise AuthServiceError("AUTH_STATE_UNAVAILABLE")
            identity=identity_reference(result.session.identity_id)
            if self._identity is not None and self._identity!=identity:
                cleared=self._forget()
            self._vault.put(self._origin,identity,result.emission.refresh)
            self._access,self._identity,self._session_id=result.emission.access,identity,result.session.session_id
        elif result.outcome in (AuthOutcome.REAUTH_REQUIRED,AuthOutcome.UNKNOWN) or (result.outcome in (AuthOutcome.WITHDRAWN,AuthOutcome.WITHDRAWN_AUDIT_PENDING) and retire_local):
            cleared=self._forget()
        return CliAuthStatus(result.outcome,result.audit,result.operation_id,result.session,result.credential,self._vault.storage_mode,cleared)
    def login(self,command,supplied):
        if type(supplied) is not LoginInput or supplied.facade is not Facade.API: raise AuthServiceError("AUTH_INPUT_INVALID")
        return self._accept(self._service.login(command,supplied))
    def restore(self,command,identity_ref):
        from pixs.auth.identifiers import parse_identity_reference
        parse_identity_reference(identity_ref)
        if self._identity is not None: raise AuthServiceError("AUTH_INPUT_INVALID")
        self._identity=identity_ref
        return self.renew(command)
    def renew(self,command):
        if self._identity is None: raise AuthServiceError("AUTH_REAUTH_REQUIRED")
        token=self._vault.get(self._origin,self._identity)
        if token is None:
            self._forget()
            raise AuthServiceError("AUTH_REAUTH_REQUIRED")
        try: result=self._service.renew(command,token)
        except AuthServiceError:
            self._forget()
            raise
        return self._accept(result)
    def invoke(self,command,*,operation,**server_arguments):
        if operation not in ("logout","revoke_session","revoke_all","change_password","recover_password","reconcile_audit") or "kind" in server_arguments:
            raise AuthServiceError("AUTH_INPUT_INVALID")
        if self._access is None: raise AuthServiceError("AUTH_REAUTH_REQUIRED")
        retire_local=operation not in ("revoke_session","reconcile_audit") or (operation=="revoke_session" and command.request.resource_id=="pixs.auth.session:"+str(self._session_id))
        return self._accept(getattr(self._service,operation)(command,self._access,kind=TokenKind.ACCESS,**server_arguments),retire_local=retire_local)
    def close(self):
        self._access,self._identity=None,None
        self._vault.close()


__all__=["CliAuthStatus","CliAuthFacade"]
