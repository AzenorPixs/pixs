"""Trousseau CLI : mémoire seule et protocoles Secret Service sans secret en arguments."""
import subprocess
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from pixs.auth.cli_vault import MemoryRefreshVault,SecretServiceBackend,AuthVaultError,select_refresh_vault,_QualifiedRefreshVault,_namespace
from pixs.auth.tokens import new_token
from pixs.auth.identifiers import new_uuid7,identity_reference

class VaultTests(unittest.TestCase):
    def setUp(self):
        self.origin="https://auth.example.test"
        self.identity=identity_reference(new_uuid7())
        self.token=new_token()
    def backend(self):
        backend=object.__new__(SecretServiceBackend)
        backend._binary="/usr/bin/secret-tool"
        backend._timeout=2
        return backend
    def test_memory_lifetime_is_per_instance(self):
        vault=MemoryRefreshVault();vault.put(self.origin,self.identity,self.token)
        self.assertIs(vault.get(self.origin,self.identity),self.token)
        self.assertIsNone(MemoryRefreshVault().get(self.origin,self.identity))
        vault.close();self.assertIsNone(vault.get(self.origin,self.identity))
    def test_memory_clear_and_namespaces(self):
        vault=MemoryRefreshVault();vault.put(self.origin,self.identity,self.token)
        self.assertIsNone(vault.get("https://other.example.test",self.identity))
        self.assertIsNone(vault.get(self.origin,identity_reference(new_uuid7())))
        vault.clear(self.origin,self.identity);self.assertIsNone(vault.get(self.origin,self.identity))
    def test_memory_has_no_plaintext_representation(self):
        vault=MemoryRefreshVault();vault.put(self.origin,self.identity,self.token)
        self.assertNotIn(self.token.value,repr(vault))
    def test_invalid_namespace_refused(self):
        for origin,identity in (("http://auth.example.test",self.identity),("https://user@auth.example.test",self.identity),(self.origin,"raw-user")):
            with self.subTest(origin=origin):
                with self.assertRaises(AuthVaultError):MemoryRefreshVault().put(origin,identity,self.token)
    def test_store_secret_is_only_stdin(self):
        with patch("pixs.auth.cli_vault.subprocess.run",return_value=SimpleNamespace(returncode=0,stdout="",stderr="")) as runner:
            self.backend().put(_namespace(self.origin,self.identity),self.token)
        args,kwargs=runner.call_args
        self.assertNotIn(self.token.value," ".join(args[0]))
        self.assertEqual(kwargs["input"],self.token.value)
        self.assertTrue(kwargs["capture_output"])
    def test_lookup_is_captured_and_validated(self):
        with patch("pixs.auth.cli_vault.subprocess.run",return_value=SimpleNamespace(returncode=0,stdout=self.token.value+"\n",stderr="")):
            result=self.backend().get("a"*64)
        self.assertEqual(result.value,self.token.value)
    def test_lookup_rejects_malformed_output(self):
        with patch("pixs.auth.cli_vault.subprocess.run",return_value=SimpleNamespace(returncode=0,stdout="not-a-token",stderr="")):
            with self.assertRaises(AuthVaultError):self.backend().get("a"*64)
    def test_error_never_exposes_captured_secret(self):
        with patch("pixs.auth.cli_vault.subprocess.run",return_value=SimpleNamespace(returncode=1,stdout=self.token.value,stderr=self.token.value)):
            with self.assertRaises(AuthVaultError) as raised:self.backend().get("a"*64)
        self.assertNotIn(self.token.value,str(raised.exception))
    def test_timeout_is_sanitized(self):
        with patch("pixs.auth.cli_vault.subprocess.run",side_effect=subprocess.TimeoutExpired("synthetic",1,output=self.token.value)):
            with self.assertRaises(AuthVaultError) as raised:self.backend().get("a"*64)
        self.assertNotIn(self.token.value,str(raised.exception))
    def test_qualification_uses_new_namespace_and_cleans(self):
        backend=self.backend();stored={};cleared=[]
        with patch.object(backend,"put",side_effect=lambda n,t:stored.update({n:t})),patch.object(backend,"get",side_effect=lambda n:stored[n]),patch.object(backend,"clear",side_effect=lambda n:cleared.append(n)):
            self.assertTrue(backend.qualify())
        self.assertEqual(list(stored),cleared)
        self.assertNotEqual(cleared[0],_namespace(self.origin,self.identity))
    def test_qualification_cleanup_failure_rejects_backend(self):
        backend=self.backend();stored={}
        with patch.object(backend,"put",side_effect=lambda n,t:stored.update({n:t})),patch.object(backend,"get",side_effect=lambda n:stored[n]),patch.object(backend,"clear",side_effect=AuthVaultError()):
            self.assertFalse(backend.qualify())
    def test_missing_binary_selects_memory(self):
        vault=select_refresh_vault(binary="/path/absent/pixs-secret-tool")
        self.assertIs(type(vault),MemoryRefreshVault)
    def test_unqualified_backend_selects_memory(self):
        with patch("pixs.auth.cli_vault.SecretServiceBackend") as constructor:
            constructor.return_value.qualify.return_value=False
            self.assertIs(type(select_refresh_vault()),MemoryRefreshVault)
    def test_qualified_backend_is_used_and_falls_back_in_memory(self):
        with patch("pixs.auth.cli_vault.SecretServiceBackend") as constructor:
            backend=constructor.return_value;backend.qualify.return_value=True
            vault=select_refresh_vault();self.assertEqual(vault.storage_mode,"SECRET_SERVICE")
            backend.put.side_effect=AuthVaultError()
            vault.put(self.origin,self.identity,self.token)
            self.assertEqual(vault.storage_mode,"MEMORY")
            self.assertIs(vault.get(self.origin,self.identity),self.token)
    def test_failed_persistent_clear_is_not_claimed_successful(self):
        with patch("pixs.auth.cli_vault.SecretServiceBackend") as constructor:
            backend=constructor.return_value;backend.qualify.return_value=True
            vault=select_refresh_vault();vault.put(self.origin,self.identity,self.token)
            backend.clear.side_effect=AuthVaultError()
            with self.assertRaises(AuthVaultError):vault.clear(self.origin,self.identity)
            self.assertIsNone(vault.get(self.origin,self.identity))

if __name__=="__main__":unittest.main()
