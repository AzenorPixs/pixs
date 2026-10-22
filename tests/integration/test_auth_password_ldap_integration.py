"""Qualification D11 réelle, explicitement activée par --qualify.

Le banc Debian 13 reste privé et éphémère dans le projet. Seules les empreintes
nécessaires au rootpw sont écrites dans sa configuration privée puis supprimées.
Aucun mot de passe brut ni empreinte n'est affiché ou transmis en argument.
"""
from __future__ import annotations

import concurrent.futures
import contextlib
import hashlib
import json
import lzma
import os
import re
import secrets
import signal
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.parse
import urllib.request
from importlib import metadata
from pathlib import Path

from pixs.auth.passwords import (
    envelope_to_django, envelope_to_ldap, hash_password, verify_password,
)

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "tests/runtime/c03-ldap"
QUALIFY = "--qualify" in sys.argv
PACKAGES_URL = "https://deb.debian.org/debian/dists/trixie/main/binary-amd64/Packages.xz"
PINNED = {"slapd": "2.6.10+dfsg-1", "libldap2": "2.6.10+dfsg-1"}
NATIVE_PACKAGES = {
    "libargon2.so.1": "libargon2-1", "libltdl.so.7": "libltdl7",
    "libsasl2.so.2": "libsasl2-2", "libwrap.so.0": "libwrap0",
    "libodbc.so.2": "libodbc2", "libperl.so.5.40": "libperl5.40",
    "libgnutls.so.30": "libgnutls30t64", "libnettle.so.8": "libnettle8t64",
    "libhogweed.so.6": "libhogweed6t64", "libgmp.so.10": "libgmp10",
    "libtasn1.so.6": "libtasn1-6", "libidn2.so.0": "libidn2-0",
    "libunistring.so.5": "libunistring5",
}


class QualificationError(RuntimeError):
    """Diagnostic fixe qui n'inclut aucune donnée du banc."""


def fetch_public(url: str, target: Path, limit: int) -> None:
    if not url.startswith("https://deb.debian.org/debian/"):
        raise QualificationError("Origine Debian non autorisée.")
    with urllib.request.urlopen(url, timeout=40) as response:
        if not response.url.startswith("https://deb.debian.org/debian/"):
            raise QualificationError("Redirection Debian non autorisée.")
        with target.open("xb") as stream:
            size = 0
            while chunk := response.read(65536):
                size += len(chunk)
                if size > limit:
                    raise QualificationError("Téléchargement hors limite.")
                stream.write(chunk)


def package_records(index: Path) -> dict[str, dict[str, str]]:
    wanted = set(PINNED) | set(NATIVE_PACKAGES.values())
    records: dict[str, dict[str, str]] = {}
    current: dict[str, str] = {}
    size = 0
    with lzma.open(index, "rt", encoding="utf-8") as stream:
        for line in stream:
            size += len(line)
            if size > 256 * 1024 * 1024:
                raise QualificationError("Index décompressé hors limite.")
            if line == "\n":
                if current.get("Package") in wanted:
                    records[current["Package"]] = current
                current = {}
            elif not line.startswith(" ") and ": " in line:
                key, value = line.rstrip("\n").split(": ", 1)
                if key in ("Package", "Version", "Filename", "SHA256"):
                    current[key] = value
        if current.get("Package") in wanted:
            records[current["Package"]] = current
    return records


def stage_package(name: str, records: dict, work: Path, destination: Path, staged: dict) -> None:
    if name in staged:
        raise QualificationError("Dépendance native toujours absente après extraction.")
    info = records.get(name)
    if not info or set(info) != {"Package", "Version", "Filename", "SHA256"}:
        raise QualificationError("Métadonnées Debian incomplètes.")
    if name in PINNED and info["Version"] != PINNED[name]:
        raise QualificationError("Version Debian différente du profil approuvé.")
    filename = info["Filename"]
    if not filename.startswith("pool/main/") or ".." in Path(filename).parts:
        raise QualificationError("Chemin de paquet non autorisé.")
    if re.fullmatch(r"[0-9a-f]{64}", info["SHA256"]) is None:
        raise QualificationError("Empreinte de paquet invalide.")
    archive = work / Path(filename).name
    fetch_public("https://deb.debian.org/debian/" + filename, archive, 64 * 1024 * 1024)
    if hashlib.sha256(archive.read_bytes()).hexdigest() != info["SHA256"]:
        raise QualificationError("Empreinte de paquet non conforme.")
    result = subprocess.run(
        ["/usr/bin/dpkg-deb", "-x", str(archive), str(destination)],
        capture_output=True, timeout=30, env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"},
    )
    if result.returncode:
        raise QualificationError("Extraction du paquet impossible.")
    staged[name] = {key: info[key] for key in ("Version", "Filename", "SHA256")}


def missing_libraries(paths: tuple[Path, ...], environment: dict[str, str]) -> set[str]:
    missing: set[str] = set()
    for path in paths:
        if not path.is_file():
            raise QualificationError("Composant du profil Debian absent.")
        result = subprocess.run(
            ["/usr/bin/ldd", str(path)], capture_output=True, text=True,
            timeout=15, env=environment,
        )
        if result.returncode:
            raise QualificationError("Contrôle des bibliothèques impossible.")
        for line in result.stdout.splitlines():
            if "=> not found" in line:
                missing.add(line.strip().split()[0])
    return missing


def ber(tag: int, payload: bytes) -> bytes:
    length = len(payload)
    if length < 128:
        prefix = bytes([length])
    else:
        raw = length.to_bytes((length.bit_length() + 7) // 8, "big")
        prefix = bytes([128 | len(raw)]) + raw
    return bytes([tag]) + prefix + payload


def receive_exact(connection: socket.socket, count: int) -> bytes:
    if not 0 <= count <= 4096:
        raise QualificationError("Réponse LDAP hors limite.")
    result = bytearray()
    while len(result) < count:
        chunk = connection.recv(count - len(result))
        if not chunk:
            raise QualificationError("Réponse LDAP interrompue.")
        result.extend(chunk)
    return bytes(result)


def take_tlv(data: bytes, position: int = 0) -> tuple[int, bytes, int]:
    if position + 2 > len(data):
        raise QualificationError("TLV LDAP tronqué.")
    tag, length = data[position:position + 2]
    position += 2
    if length & 128:
        count = length & 127
        if count == 0 or count > 4 or position + count > len(data):
            raise QualificationError("Longueur LDAP invalide.")
        length = int.from_bytes(data[position:position + count], "big")
        position += count
        if length < 128:
            raise QualificationError("Longueur LDAP non canonique.")
    end = position + length
    if length > 4096 or end > len(data):
        raise QualificationError("Contenu LDAP hors limite.")
    return tag, data[position:end], end


def bind_result(path: Path, password: bytes) -> int:
    request = ber(0x30, ber(0x02, b"\x01") + ber(
        0x60, ber(0x02, b"\x03") + ber(0x04, b"cn=operator,dc=qualification") + ber(0x80, password),
    ))
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.settimeout(5)
        connection.connect(str(path))
        connection.sendall(request)
        header = receive_exact(connection, 2)
        if header[0] != 0x30:
            raise QualificationError("LDAPMessage attendu.")
        length = header[1]
        if length & 128:
            count = length & 127
            if count == 0 or count > 4:
                raise QualificationError("Longueur LDAP invalide.")
            length = int.from_bytes(receive_exact(connection, count), "big")
        payload = receive_exact(connection, length)
    tag, message_id, position = take_tlv(payload)
    if tag != 0x02 or message_id != b"\x01":
        raise QualificationError("Identité de réponse LDAP divergente.")
    tag, body, position = take_tlv(payload, position)
    if tag != 0x61 or position != len(payload):
        raise QualificationError("BindResponse attendue.")
    tag, code, position = take_tlv(body)
    if tag != 0x0A or len(code) != 1 or code[0] not in (0, 49):
        raise QualificationError("Résultat LDAP inattendu.")
    for _ in range(2):
        tag, _, position = take_tlv(body, position)
        if tag != 0x04:
            raise QualificationError("Structure du résultat LDAP invalide.")
    if position != len(body):
        raise QualificationError("Champs LDAP inattendus.")
    return code[0]


@contextlib.contextmanager
def private_server(work: Path, staged: Path, environment: dict[str, str], encoded: str):
    with tempfile.TemporaryDirectory(prefix="serve-", dir=work) as name:
        directory = Path(name)
        os.chmod(directory, 0o700)
        (directory / "data").mkdir(mode=0o700)
        path = directory / "ldap.sock"
        if len(os.fsencode(path)) >= 104:
            raise QualificationError("Chemin de socket Unix trop long.")
        configuration = directory / "slapd.conf"
        content = (
            f'pidfile {directory}/slapd.pid\nargsfile {directory}/slapd.args\n'
            f'modulepath {staged}/usr/lib/ldap\nmoduleload back_mdb\nmoduleload argon2\n'
            f'include {staged}/etc/ldap/schema/core.schema\n'
            'database mdb\nsuffix "dc=qualification"\nrootdn "cn=operator,dc=qualification"\n'
            f'rootpw "{encoded}"\ndirectory "{directory}/data"\nloglevel 0\n'
        )
        descriptor = os.open(configuration, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
        process = subprocess.Popen(
            [str(staged / "usr/sbin/slapd"), "-d", "0", "-f", str(configuration),
             "-h", "ldapi://" + urllib.parse.quote(str(path), safe="")],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=environment,
        )
        try:
            deadline = time.monotonic() + 8
            while True:
                if process.poll() is not None:
                    raise QualificationError("Le banc LDAP n'a pas démarré.")
                if time.monotonic() >= deadline:
                    raise QualificationError("Délai de démarrage du banc LDAP dépassé.")
                try:
                    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as probe:
                        probe.settimeout(0.2)
                        probe.connect(str(path))
                except (FileNotFoundError, ConnectionRefusedError):
                    time.sleep(0.02)
                else:
                    break
            if process.poll() is not None:
                raise QualificationError("Le banc LDAP s'est arrêté prématurément.")
            yield path
        finally:
            try:
                if process.poll() is None:
                    process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
            finally:
                if process.stdout is not None:
                    process.stdout.close()
                if process.stderr is not None:
                    process.stderr.close()


class DjangoArgon2Qualification(unittest.TestCase):
    def test_costs_and_refusals(self):
        from argon2.exceptions import VerificationError
        from django.contrib.auth.hashers import Argon2PasswordHasher
        hasher = Argon2PasswordHasher()
        password = secrets.token_urlsafe(24)

        def measured(_):
            started = time.perf_counter()
            encoded = hasher.encode(password, hasher.salt())
            return time.perf_counter() - started, encoded

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(measured, (0, 1)))
        for duration, encoded in results:
            self.assertGreater(duration, 0)
            self.assertTrue(encoded.startswith("argon2$argon2id$v=19$"))
            self.assertTrue(hasher.verify(password, encoded))
            self.assertFalse(hasher.verify(password + "!", encoded))
        malformed = results[0][1].replace(f"m={hasher.memory_cost},", "m=0,", 1)
        try:
            accepted = hasher.verify(password, malformed)
        except (ValueError, VerificationError):
            accepted = False
        self.assertIs(accepted, False)
        print("C03_COSTS " + json.dumps({
            "python": sys.version.split()[0],
            "versions": {name: metadata.version(name) for name in (
                "Django", "argon2-cffi", "argon2-cffi-bindings", "cryptography", "cffi", "pycparser",
            )},
            "memory_kib": hasher.memory_cost, "time_cost": hasher.time_cost,
            "parallelism": hasher.parallelism, "concurrent_workers": 2,
            "hash_durations_s": [round(item[0], 6) for item in results],
        }, sort_keys=True))


@unittest.skipUnless(QUALIFY, "Qualification LDAP non activée : --qualify requis.")
class OpenLdapQualification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        for executable in ("/usr/bin/dpkg-deb", "/usr/bin/ldd"):
            if not Path(executable).is_file():
                raise QualificationError("Outil Debian requis absent.")
        if RUNTIME.is_symlink():
            raise QualificationError("Répertoire runtime symbolique interdit.")
        RUNTIME.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(RUNTIME, 0o700)
        cls.temporary = tempfile.TemporaryDirectory(prefix="c03-", dir=RUNTIME)
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.work = Path(cls.temporary.name)
        cls.staged = cls.work / "root"
        cls.staged.mkdir(mode=0o700)
        index = cls.work / "Packages.xz"
        fetch_public(PACKAGES_URL, index, 32 * 1024 * 1024)
        records = package_records(index)
        staged = {}
        for package in PINNED:
            stage_package(package, records, cls.work, cls.staged, staged)
        cls.environment = {
            "PATH": "/usr/bin:/bin", "LC_ALL": "C",
            "LD_LIBRARY_PATH": ":".join(str(cls.staged / name) for name in (
                "usr/lib/x86_64-linux-gnu", "lib/x86_64-linux-gnu",
            )),
        }
        binaries = tuple(cls.staged / name for name in (
            "usr/sbin/slapd", "usr/lib/ldap/argon2.so", "usr/lib/ldap/back_mdb.so",
        ))
        for _ in range(4):
            missing = missing_libraries(binaries, cls.environment)
            if not missing:
                break
            if any(library not in NATIVE_PACKAGES for library in missing):
                raise QualificationError("Bibliothèque manquante hors périmètre approuvé.")
            for package in sorted({NATIVE_PACKAGES[library] for library in missing}):
                stage_package(package, records, cls.work, cls.staged, staged)
        if missing_libraries(binaries, cls.environment):
            raise QualificationError("Bibliothèques encore absentes après quatre passes.")
        print("C03_DEBIAN_PACKAGES " + json.dumps(staged, sort_keys=True))

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()
        if cls.work.exists():
            raise QualificationError("Nettoyage du banc incomplet.")
        print('C03_LDAP_CLEANUP {"temporary_removed": true, "owned_processes_stopped": true}')

    def test_01_django_hash_verified_by_ldap(self):
        from django.contrib.auth.hashers import Argon2PasswordHasher
        hasher = Argon2PasswordHasher()
        password = secrets.token_urlsafe(24)
        encoded = hash_password(password)
        adapted = envelope_to_ldap(encoded)
        self.assertTrue(encoded[len("argon2"):] == adapted[len("{ARGON2}"):])
        with private_server(self.work, self.staged, self.environment, adapted) as path:
            self.assertEqual(bind_result(path, password.encode()), 0)
            self.assertEqual(bind_result(path, (password + "!").encode()), 49)

    def test_02_ldap_hash_verified_by_django(self):
        from argon2 import extract_parameters
        from django.contrib.auth.hashers import Argon2PasswordHasher
        hasher = Argon2PasswordHasher()
        password = secrets.token_urlsafe(24)
        module = f"module-load=argon2 m={hasher.memory_cost} t={hasher.time_cost} p={hasher.parallelism}"
        result = subprocess.run(
            [str(self.staged / "usr/sbin/slapd"), "-T", "passwd", "-o",
             "module-path=" + str(self.staged / "usr/lib/ldap"), "-o", module,
             "-h", "{ARGON2}", "-T", "/dev/stdin"],
            input=password.encode(), capture_output=True, timeout=15, env=self.environment,
        )
        if result.returncode:
            raise QualificationError("Génération Argon2id du module LDAP impossible.")
        ldap_value = result.stdout.decode("ascii").strip()
        adapted = envelope_to_django(ldap_value)
        parameters = extract_parameters(adapted[len("argon2"):])
        self.assertTrue(parameters.memory_cost == hasher.memory_cost)
        self.assertTrue(parameters.time_cost == hasher.time_cost)
        self.assertTrue(parameters.parallelism == hasher.parallelism)
        self.assertTrue(verify_password(password, adapted))
        self.assertFalse(verify_password(password + "!", adapted))

    def test_03_ldap_refuses_incompatible_parameters(self):
        from django.contrib.auth.hashers import Argon2PasswordHasher
        hasher = Argon2PasswordHasher()
        password = secrets.token_urlsafe(24)
        encoded = hash_password(password)
        malformed = envelope_to_ldap(encoded).replace(f"m={hasher.memory_cost},", "m=0,", 1)
        with private_server(self.work, self.staged, self.environment, malformed) as path:
            self.assertEqual(bind_result(path, password.encode()), 49)


def deadline_expired(_signum, _frame):
    raise QualificationError("Délai global de qualification dépassé.")


if __name__ == "__main__":
    if QUALIFY:
        sys.argv.remove("--qualify")
        signal.signal(signal.SIGALRM, deadline_expired)
        signal.alarm(240)
    try:
        unittest.main()
    finally:
        signal.alarm(0)
