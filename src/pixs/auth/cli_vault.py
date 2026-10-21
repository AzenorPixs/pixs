"""Renouvellement CLI : Secret Service qualifié dans ce processus, sinon mémoire seule.

Aucun fichier clair. Les jetons passent uniquement par stdin et les sorties
capturées du sous-processus ; ils ne figurent jamais dans les arguments.
"""
from __future__ import annotations
import hashlib
import os
import stat
import subprocess
import uuid
from urllib.parse import urlsplit
from pixs.auth.identifiers import parse_identity_reference
from pixs.auth.tokens import OpaqueToken,new_token,parse_token,AuthTokenError

class AuthVaultError(ValueError):
    def __init__(self):
        super().__init__("Trousseau de renouvellement indisponible.")
        self.code="AUTH_VAULT_UNAVAILABLE"


def _namespace(origin,identity_ref):
    if type(origin) is not str:
        raise AuthVaultError()
    parsed=urlsplit(origin)
    if parsed.scheme!="https" or not parsed.netloc or parsed.username is not None or parsed.password is not None or parsed.path or parsed.query or parsed.fragment:
        raise AuthVaultError()
    try: parse_identity_reference(identity_ref)
    except ValueError: raise AuthVaultError() from None
    return hashlib.sha256((origin+"\0"+identity_ref).encode()).hexdigest()


class MemoryRefreshVault:
    storage_mode="MEMORY"
    def __init__(self): self._values={}
    def put(self,origin,identity_ref,token):
        key=_namespace(origin,identity_ref)
        if type(token) is not OpaqueToken: raise AuthVaultError()
        token.__post_init__()
        self._values[key]=token
    def get(self,origin,identity_ref): return self._values.get(_namespace(origin,identity_ref))
    def clear(self,origin,identity_ref): self._values.pop(_namespace(origin,identity_ref),None)
    def close(self): self._values.clear()


class SecretServiceBackend:
    def __init__(self, *, binary="/usr/bin/secret-tool", timeout=5):
        if type(binary) is not str or not os.path.isabs(binary) or type(timeout) not in (int,float) or isinstance(timeout,bool) or not 0<timeout<=10:
            raise AuthVaultError()
        try: info=os.stat(binary)
        except OSError: raise AuthVaultError() from None
        if not stat.S_ISREG(info.st_mode) or info.st_mode & (stat.S_IWGRP|stat.S_IWOTH) or not os.access(binary,os.X_OK):
            raise AuthVaultError()
        self._binary,self._timeout=binary,timeout
    def _run(self,action,namespace,token=None):
        if type(namespace) is not str or len(namespace)!=64 or any(c not in "0123456789abcdef" for c in namespace): raise AuthVaultError()
        args=[self._binary,action]
        if action=="store": args.append("--label=Pixs Auth renouvellement CLI")
        args += ["service","pixs.auth.cli.refresh.v1","namespace",namespace]
        try:
            result=subprocess.run(args,input=token.value if token is not None else None,text=True,capture_output=True,timeout=self._timeout,check=False)
        except (OSError,subprocess.TimeoutExpired): raise AuthVaultError() from None
        if result.returncode!=0: raise AuthVaultError()
        if action=="lookup":
            try: return parse_token(result.stdout.removesuffix("\n"))
            except AuthTokenError: raise AuthVaultError() from None
        return None
    def put(self,namespace,token):
        if type(token) is not OpaqueToken: raise AuthVaultError()
        token.__post_init__()
        self._run("store",namespace,token)
    def get(self,namespace): return self._run("lookup",namespace)
    def clear(self,namespace): self._run("clear",namespace)
    def qualify(self):
        # Espace aléatoire neuf : aucune entrée d'un compte utilisateur n'est écrasée.
        namespace=hashlib.sha256(("qualification:"+uuid.uuid4().hex).encode()).hexdigest()
        token=new_token()
        stored=False
        valid=False
        try:
            self.put(namespace,token)
            stored=True
            actual=self.get(namespace)
            import hmac
            valid=hmac.compare_digest(actual.value,token.value)
        except AuthVaultError:
            valid=False
        finally:
            # Même une issue store inconnue impose une tentative de nettoyage ciblé.
            try: self.clear(namespace)
            except AuthVaultError: valid=False
        return valid and stored


class _QualifiedRefreshVault(MemoryRefreshVault):
    storage_mode="SECRET_SERVICE"
    def __init__(self,backend):
        super().__init__()
        self._backend=backend
    def put(self,origin,identity_ref,token):
        super().put(origin,identity_ref,token)
        if self.storage_mode=="SECRET_SERVICE":
            try: self._backend.put(_namespace(origin,identity_ref),token)
            except AuthVaultError: self.storage_mode="MEMORY"
    def get(self,origin,identity_ref):
        value=super().get(origin,identity_ref)
        if value is not None or self.storage_mode!="SECRET_SERVICE": return value
        try: value=self._backend.get(_namespace(origin,identity_ref))
        except AuthVaultError:
            self.storage_mode="MEMORY"
            return None
        super().put(origin,identity_ref,value)
        return value
    def clear(self,origin,identity_ref):
        super().clear(origin,identity_ref)
        # Une révocation locale ne prétend jamais avoir effacé le trousseau en cas d'échec.
        try: self._backend.clear(_namespace(origin,identity_ref))
        except AuthVaultError:
            self.storage_mode="MEMORY"
            raise


def select_refresh_vault(*,binary="/usr/bin/secret-tool",timeout=5):
    try:
        backend=SecretServiceBackend(binary=binary,timeout=timeout)
        if backend.qualify(): return _QualifiedRefreshVault(backend)
    except AuthVaultError:
        pass
    return MemoryRefreshVault()


__all__=["AuthVaultError","MemoryRefreshVault","SecretServiceBackend","select_refresh_vault"]
