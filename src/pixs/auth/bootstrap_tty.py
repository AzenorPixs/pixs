"""Saisie locale privee du compte initial Auth sur /dev/tty, sans creation ni preuve.

Raccord fin avec AuthBootstrapSession reservee : demande l'identifiant et les
deux mots de passe sur le terminal de controle local, puis appelle le
proprietaire prepare_initial. Seule la reference d'intention opaque est
retournee. Aucun compte cree, aucune identite ni autorisation prouvee.

Choix fixes ici car design muet sur le mecanisme exact, sans SDK fabrique :
premier plan via tcgetpgrp, exclusion locale non reentrante non bloquante via
threading.Lock + flock NB, echo coupe aussi pour l'identifiant, bornes
min(PC_MAX_CANON-1, session._max_password) sans defaut invente, prompts
constants sur /dev/tty, restauration TCSAFLUSH + vidange TCIFLUSH,
quarantaine par session.close sur echec. Stdlib seule, sans getpass,
sans signaux ni filtres warning modifies. Nettoyage des bytearray locaux
tente, sans promettre d'effacement des str Python immuables ; aucune
garantie apres signal non interceptable.
"""
from __future__ import annotations
import os
import stat
import threading
from pixs.auth.bootstrap_session import AuthBootstrapSession, AuthBootstrapSessionError, BootstrapDraft
from pixs.auth.configuration import InitialLocalAuthSelection
from pixs.core.ports import CorePortError
__all__ = ["BootstrapTtyError", "prepare_initial_from_tty"]
_TTY_LOCK = threading.Lock()
_PROMPT_IDENTIFIER = b"Identifiant: "
_PROMPT_PASSWORD1 = b"Mot de passe: "
_PROMPT_PASSWORD2 = b"Confirmer le mot de passe: "
def _masked(step, exc):
    name = type(exc).__name__
    if name == "BootstrapTtyError":
        code = "AUTH_BOOTSTRAP_TTY_INVALID"
    elif name == "AuthBootstrapSessionError":
        code = "AUTH_BOOTSTRAP_SESSION_INVALID"
    elif name == "CorePortError":
        code = "CORE_PORT_INVALID"
    elif isinstance(exc, OSError):
        code = "OSError"
    elif isinstance(exc, EOFError):
        code = "EOFError"
    elif isinstance(exc, KeyboardInterrupt):
        code = "KeyboardInterrupt"
    elif isinstance(exc, SystemExit):
        code = "SystemExit"
    else:
        code = "UNEXPECTED"
    safe_step = step if type(step) is str and step != "" else "etape-inconnue"
    return {"step": safe_step, "type": name, "code": code}
def _is_cancellation(exc):
    return isinstance(exc, (KeyboardInterrupt, SystemExit))
def _is_expected_ordinary(exc):
    return isinstance(exc, (BootstrapTtyError, AuthBootstrapSessionError, CorePortError, OSError, EOFError))
class BootstrapTtyError(CorePortError):
    def __init__(self, failures=()):
        ValueError.__init__(self, "Saisie locale R01 non realisable.")
        self.code = "AUTH_BOOTSTRAP_TTY_INVALID"
        self.element = "auth_bootstrap_tty"
        self.step = "prepare_initial_from_tty"
        kept = []
        for item in tuple(failures):
            if type(item) is dict and set(item.keys()) == {"step", "type", "code"}:
                if all(type(item[key]) is str and item[key] != "" for key in ("step", "type", "code")):
                    kept.append({"step": item["step"], "type": item["type"], "code": item["code"]})
                else:
                    kept.append({"step": "entree-invalide", "type": "InvalidFailure", "code": "INVALID_FAILURE"})
            else:
                kept.append({"step": "entree-invalide", "type": "InvalidFailure", "code": "INVALID_FAILURE"})
        self.failures = tuple(kept)
    def __str__(self):
        return "Saisie locale R01 non realisable."
    def __repr__(self):
        return "BootstrapTtyError(failures=" + str(len(self.failures)) + ")"
def _raise_single(step):
    raise BootstrapTtyError(failures=({"step": step, "type": "BootstrapTtyError", "code": "AUTH_BOOTSTRAP_TTY_INVALID"},)) from None
def prepare_initial_from_tty(session, draft, selection):
    if type(session) is not AuthBootstrapSession:
        _raise_single("precheck:session-type")
    if type(draft) is not BootstrapDraft:
        _raise_single("precheck:draft-type")
    if type(selection) is not InitialLocalAuthSelection:
        _raise_single("precheck:selection-type")
    try:
        closed = draft.closed_effects
    except AttributeError as error:
        raise BootstrapTtyError(failures=(_masked("precheck:draft-closed", error),)) from None
    if type(closed) is not tuple:
        _raise_single("precheck:draft-closed-type")
    if closed == ("REUSE_EXISTING",):
        _raise_single("precheck:reuse-sans-prompt")
    if threading.current_thread() is not threading.main_thread():
        _raise_single("precheck:main-thread")
    acquired = _TTY_LOCK.acquire(blocking=False)
    if not acquired:
        _raise_single("precheck:exclusion-non-bloquante")
    lock_held = True
    fd = None
    saved = None
    bound = None
    intent = None
    primary = None
    cleanup_entries = []
    cleanup_cancellation = None
    raw_chunks = []
    def _zero(buf):
        for index in range(len(buf)):
            buf[index] = 0
    def _record_cleanup(step, error):
        if _is_cancellation(error):
            cleanup_entries.append(_masked(step, error))
            return error
        cleanup_entries.append(_masked(step, error))
        return None
    try:
        try:
            session.describe(draft)
        except (AuthBootstrapSessionError, CorePortError) as error:
            raise BootstrapTtyError(failures=(_masked("propriete:draft-reserve", error),)) from None
        raw_bound = getattr(session, "_max_password", None)
        if type(raw_bound) is not int or isinstance(raw_bound, bool) or raw_bound < 1:
            _raise_single("precheck:borne-privee-auth")
        bound = raw_bound
        import fcntl
        import termios
        flags = os.O_RDWR | getattr(os, "O_NOCTTY", 0) | getattr(os, "O_CLOEXEC", 0)
        try:
            fd = os.open("/dev/tty", flags)
        except OSError as error:
            raise BootstrapTtyError(failures=(_masked("ouverture:/dev/tty", error),)) from None
        try:
            mode = os.fstat(fd).st_mode
        except OSError as error:
            raise BootstrapTtyError(failures=(_masked("controle:fstat", error),)) from None
        if not stat.S_ISCHR(mode):
            _raise_single("controle:caractere-terminal")
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (OSError, ValueError) as error:
            raise BootstrapTtyError(failures=(_masked("controle:flock-nb", error),)) from None
        try:
            if not os.isatty(fd):
                _raise_single("controle:isatty")
        except (OSError, ValueError) as error:
            raise BootstrapTtyError(failures=(_masked("controle:isatty", error),)) from None
        try:
            if os.tcgetpgrp(fd) != os.getpgrp():
                _raise_single("controle:premier-plan")
        except (OSError, ValueError) as error:
            raise BootstrapTtyError(failures=(_masked("controle:premier-plan", error),)) from None
        try:
            saved = termios.tcgetattr(fd)
        except (termios.error, OSError, ValueError) as error:
            raise BootstrapTtyError(failures=(_masked("controle:tcgetattr", error),)) from None
        try:
            lflag = saved[3]
        except (IndexError, TypeError) as error:
            raise BootstrapTtyError(failures=(_masked("controle:lflag", error),)) from None
        if not (lflag & termios.ICANON and lflag & termios.ISIG):
            _raise_single("controle:icanon-isig")
        try:
            pc_max = os.fpathconf(fd, "PC_MAX_CANON")
        except (OSError, ValueError) as error:
            raise BootstrapTtyError(failures=(_masked("controle:pc-max-canon", error),)) from None
        if type(pc_max) is not int or pc_max < 2:
            _raise_single("controle:pc-max-canon-valeur")
        canon_limit = pc_max - 1
        effective = canon_limit if canon_limit < bound else bound
        if effective < 1:
            _raise_single("controle:borne-effective")
        raw = list(saved)
        try:
            raw[3] = raw[3] & ~(termios.ECHO | termios.ECHONL)
        except (IndexError, TypeError) as error:
            raise BootstrapTtyError(failures=(_masked("reglage:sans-echo", error),)) from None
        try:
            termios.tcsetattr(fd, termios.TCSAFLUSH, raw)
        except (termios.error, OSError, ValueError) as error:
            raise BootstrapTtyError(failures=(_masked("reglage:tcsetattr", error),)) from None
        def _prompt(payload):
            view = memoryview(payload)
            while view:
                try:
                    written = os.write(fd, view)
                except (OSError, ValueError) as error:
                    raise BootstrapTtyError(failures=(_masked("prompt:ecriture", error),)) from None
                if written < 1:
                    _raise_single("prompt:ecriture-courte")
                view = view[written:]
        def _read_bounded(limit):
            chunks = bytearray()
            raw_chunks.append(chunks)
            while True:
                remaining = (limit + 1) - len(chunks)
                if remaining <= 0:
                    _raise_single("lecture:borne-depassee")
                want = 256 if remaining > 256 else remaining
                try:
                    part = os.read(fd, want)
                except (OSError, ValueError) as error:
                    raise BootstrapTtyError(failures=(_masked("lecture:os-read", error),)) from None
                if part == b"":
                    _raise_single("lecture:eof-avant-lf")
                if len(part) > want:
                    _raise_single("lecture:au-dela-borne")
                chunks.extend(part)
                if b"\n" in part:
                    break
                if len(chunks) > limit + 1:
                    _raise_single("lecture:borne-depassee")
            if len(chunks) < 1 or chunks[-1:] != b"\n":
                _raise_single("lecture:ligne-incomplete")
            if len(chunks) - 1 > limit:
                _raise_single("lecture:borne-depassee")
            return bytes(chunks[:-1])
        def _read_utf8_strict(limit):
            raw_line = _read_bounded(limit)
            try:
                return raw_line.decode("utf-8", "strict")
            except UnicodeDecodeError as error:
                raise BootstrapTtyError(failures=(_masked("lecture:utf8-strict", error),)) from None
        _prompt(_PROMPT_IDENTIFIER)
        external = _read_utf8_strict(canon_limit)
        _prompt(_PROMPT_PASSWORD1)
        password1 = _read_utf8_strict(effective)
        _prompt(_PROMPT_PASSWORD2)
        password2 = _read_utf8_strict(effective)
        try:
            current = termios.tcgetattr(fd)
        except (termios.error, OSError, ValueError) as error:
            raise BootstrapTtyError(failures=(_masked("recontrole:tcgetattr", error),)) from None
        try:
            if current[3] & termios.ECHO or current[3] & termios.ECHONL:
                _raise_single("recontrole:echo-restaure-trop-tot")
            if not (current[3] & termios.ICANON and current[3] & termios.ISIG):
                _raise_single("recontrole:icanon-isig")
            if not os.isatty(fd):
                _raise_single("recontrole:isatty")
            if os.tcgetpgrp(fd) != os.getpgrp():
                _raise_single("recontrole:premier-plan")
        except (OSError, ValueError) as error:
            raise BootstrapTtyError(failures=(_masked("recontrole:terminal", error),)) from None
        try:
            candidate = session.prepare_initial(draft, password1=password1, password2=password2, selection=selection, external_subject=external)
        except (AuthBootstrapSessionError, CorePortError) as error:
            raise BootstrapTtyError(failures=(_masked("proprietaire:prepare-initial", error),)) from None
        if type(candidate) is not str or not candidate:
            _raise_single("proprietaire:intention-opaque")
        intent = candidate
    except BaseException as error:
        primary = error
    finally:
        password1 = password2 = external = candidate = None
        for buf in raw_chunks:
            try:
                _zero(buf)
            except BaseException as error:
                cleanup_entries.append(_masked("nettoyage:zero-buffer", error))
                if _is_cancellation(error) and cleanup_cancellation is None:
                    cleanup_cancellation = error
        raw_chunks.clear()
        if fd is not None:
            try:
                import termios as _termios
                if saved is not None:
                    try:
                        _termios.tcsetattr(fd, _termios.TCSAFLUSH, saved)
                    except BaseException as error:
                        cleanup_entries.append(_masked("restauration:tcsetattr", error))
                        if _is_cancellation(error) and cleanup_cancellation is None:
                            cleanup_cancellation = error
                    try:
                        _termios.tcflush(fd, _termios.TCIFLUSH)
                    except BaseException as error:
                        cleanup_entries.append(_masked("vidage:tcflush", error))
                        if _is_cancellation(error) and cleanup_cancellation is None:
                            cleanup_cancellation = error
            finally:
                try:
                    os.close(fd)
                except BaseException as error:
                    cleanup_entries.append(_masked("liberation:close-fd", error))
                    if _is_cancellation(error) and cleanup_cancellation is None:
                        cleanup_cancellation = error
                fd = None
        if lock_held:
            try:
                _TTY_LOCK.release()
            except BaseException as error:
                cleanup_entries.append(_masked("liberation:verrou", error))
                if _is_cancellation(error) and cleanup_cancellation is None:
                    cleanup_cancellation = error
            lock_held = False
        failed = primary is not None or bool(cleanup_entries) or cleanup_cancellation is not None
        if failed:
            quarantine_entry = None
            try:
                if type(session) is AuthBootstrapSession:
                    session.close()
            except BaseException as error:
                quarantine_entry = _masked("quarantaine:session-close", error)
                cleanup_entries.append(quarantine_entry)
                if _is_cancellation(error) and cleanup_cancellation is None:
                    cleanup_cancellation = error
            intent = None
            if cleanup_cancellation is not None:
                if primary is not None and primary is not cleanup_cancellation:
                    raise BaseExceptionGroup("tty-cleanup", [primary, cleanup_cancellation, BootstrapTtyError(failures=tuple(cleanup_entries))]) from None
                raise BaseExceptionGroup("tty-cleanup", [cleanup_cancellation, BootstrapTtyError(failures=tuple(cleanup_entries))]) from None
            if primary is not None and _is_cancellation(primary):
                if not cleanup_entries:
                    raise primary
                raise BaseExceptionGroup("tty-cleanup", [primary, BootstrapTtyError(failures=tuple(cleanup_entries))]) from None
            if primary is not None and not _is_expected_ordinary(primary):
                if not cleanup_entries:
                    raise primary
                raise BaseExceptionGroup("tty-cleanup", [primary, BootstrapTtyError(failures=tuple(cleanup_entries))]) from None
            gathered = []
            if primary is not None:
                if isinstance(primary, BootstrapTtyError) and getattr(primary, "failures", ()):
                    gathered.extend(primary.failures)
                else:
                    gathered.append(_masked("operation", primary))
            gathered.extend(cleanup_entries)
            raise BootstrapTtyError(failures=tuple(gathered)) from None
    if type(intent) is not str or not intent:
        try:
            if type(session) is AuthBootstrapSession:
                session.close()
        except BaseException as error:
            raise BootstrapTtyError(failures=(_masked("quarantaine:session-close", error),)) from None
        _raise_single("proprietaire:intention-opaque")
    return intent
