# cython: language_level=3
"""Inspection SQL technique interne, sans mutation ni autorité.

L'appelant de confiance vérifie le profil protégé, la règle HBA peer et le
mandat courant avant connexion. Aucun handler PZT n'est exposé ici.
Un processus possédant une connexion vivante ne doit pas forker.
Les octets du résultat décodé sont bornés ; la mémoire interne libpq ne
l'est pas par ce contrôle et exige la protection de ressources du runtime.
"""
cimport cython
from libc.string cimport strlen, strncmp
import threading
import time
import os

cdef extern from "libpq-fe.h":
    ctypedef struct PGconn:
        pass
    ctypedef struct PGresult:
        pass
    ctypedef unsigned int Oid
    ctypedef enum ConnStatusType:
        CONNECTION_OK
        CONNECTION_BAD
    ctypedef enum PostgresPollingStatusType:
        PGRES_POLLING_FAILED
        PGRES_POLLING_READING
        PGRES_POLLING_WRITING
        PGRES_POLLING_OK
    ctypedef enum ExecStatusType:
        PGRES_EMPTY_QUERY
        PGRES_COMMAND_OK
        PGRES_TUPLES_OK
        PGRES_FATAL_ERROR
    int PQlibVersion()
    int PQserverVersion(const PGconn *)
    PGconn *PQconnectStartParams(const char *const *keywords, const char *const *values, int expand_dbname)
    PostgresPollingStatusType PQconnectPoll(PGconn *)
    ConnStatusType PQstatus(const PGconn *)
    int PQsocket(const PGconn *)
    int PQsetnonblocking(PGconn *, int)
    void PQfinish(PGconn *)
    char *PQhost(const PGconn *)
    char *PQport(const PGconn *)
    char *PQdb(const PGconn *)
    char *PQuser(const PGconn *)
    char *PQparameterStatus(const PGconn *, const char *)
    int PQsendQueryParams(PGconn *, const char *, int, const Oid *, const char *const *, const int *, const int *, int)
    int PQflush(PGconn *)
    int PQconsumeInput(PGconn *)
    int PQisBusy(PGconn *)
    PGresult *PQgetResult(PGconn *)
    void PQclear(PGresult *)
    ExecStatusType PQresultStatus(const PGresult *)
    int PQntuples(const PGresult *)
    int PQnfields(const PGresult *)
    char *PQgetvalue(const PGresult *, int, int)
    int PQgetlength(const PGresult *, int, int)
    char *PQfname(const PGresult *, int)

cdef extern from "unistd.h":
    char **environ

cdef extern from *:
    """
    #include "libpq-fe.h"
    #include "pg_config.h"
    #if !defined(PG_VERSION_NUM) || (PG_VERSION_NUM != 170011)
    #error "PA01_LIBPQ_HEADERS_170011_REQUIRED"
    #endif
    """

LIBPQ_REQUIRED_VERSION_NUM = 170011
cdef bytes _Q_ROLE_DB = b"SELECT $1::text = CURRENT_USER::text AS is_role, $2::text = pg_catalog.current_database()::text AS is_db"
cdef bytes _Q_TARGET_ROLE = b"SELECT oid::text, rolcanlogin::text, rolsuper::text, rolcreatedb::text, rolcreaterole::text, rolreplication::text, rolbypassrls::text, rolinherit::text, rolconnlimit::text FROM pg_catalog.pg_roles WHERE rolname = $1::text"
cdef bytes _Q_TARGET_DATABASE = b"SELECT oid::text, pg_catalog.pg_get_userbyid(datdba)::text, pg_catalog.pg_encoding_to_char(encoding)::text, datallowconn::text, datistemplate::text, datconnlimit::text FROM pg_catalog.pg_database WHERE datname = $1::text"
cdef bytes _Q_SETTINGS = b"SELECT pg_catalog.current_setting('default_transaction_read_only')::text AS ro, pg_catalog.current_setting('search_path')::text AS sp, pg_catalog.current_setting('client_encoding')::text AS enc"

class InspectionError(RuntimeError):
    pass

def _assert_no_postgres_c_environ():
    cdef char **env = environ
    cdef int index = 0
    if env == NULL:
        return
    while env[index] != NULL:
        if strncmp(env[index], "PG", 2) == 0:
            raise InspectionError("PA01_SQL_ENVIRONMENT_FORBIDDEN")
        index += 1

def _strict_text(value):
    if type(value) is not bytes or len(value) == 0 or b"\x00" in value:
        raise InspectionError("PA01_SQL_ARGUMENT_INVALID")
    try:
        text = value.decode("utf-8")
    except UnicodeDecodeError as error:
        raise InspectionError("PA01_SQL_ARGUMENT_INVALID") from error
    for character in text:
        point = ord(character)
        if point < 32 or point == 127:
            raise InspectionError("PA01_SQL_ARGUMENT_INVALID")
    return text

def _strict_socket(value):
    from pathlib import PurePosixPath
    text = _strict_text(value)
    if "," in text or "\\" in text:
        raise InspectionError("PA01_SQL_ARGUMENT_INVALID")
    path = PurePosixPath(text)
    if not path.is_absolute() or str(path) != text:
        raise InspectionError("PA01_SQL_ARGUMENT_INVALID")
    if text != "/" and any(part in (".", "..", "") for part in text.split("/")[1:]):
        raise InspectionError("PA01_SQL_ARGUMENT_INVALID")
    return text

def _strict_digits(value, minimum, maximum):
    if type(value) is not bytes or len(value) == 0:
        raise InspectionError("PA01_SQL_ARGUMENT_INVALID")
    for byte in value:
        if byte < 48 or byte > 57:
            raise InspectionError("PA01_SQL_ARGUMENT_INVALID")
    number = int(value.decode("ascii"))
    if not minimum <= number <= maximum:
        raise InspectionError("PA01_SQL_ARGUMENT_INVALID")
    if str(number).encode("ascii") != value:
        raise InspectionError("PA01_SQL_ARGUMENT_INVALID")
    return number

def _strict_max_result_bytes(value):
    if type(value) is not int or not 1 <= value <= 2147483647:
        raise InspectionError("PA01_SQL_ARGUMENT_INVALID")
    return value

@cython.final
cdef class LibpqInspection:
    cdef PGconn *_conn
    cdef object _arguments
    cdef object _owner_thread
    cdef object _owner_pid
    cdef bint _closed
    cdef bint _failed
    cdef bint _busy
    cdef object _socket_dir
    cdef object _port
    cdef object _database
    cdef object _database_user
    cdef object _server_user
    cdef object _connect_s
    cdef object _statement_ms
    cdef object _lock_ms
    cdef object _io_ms
    cdef object _expected_version

    def __cinit__(self, arguments):
        self._conn = NULL
        self._closed = True
        self._failed = False
        self._busy = False
        self._owner_thread = threading.get_ident()
        self._owner_pid = os.getpid()
        _assert_no_postgres_c_environ()
        if type(arguments) is not tuple or len(arguments) != 10:
            raise InspectionError("PA01_SQL_ARGUMENT_INVALID")
        for item in arguments:
            if type(item) is not bytes:
                raise InspectionError("PA01_SQL_ARGUMENT_INVALID")
        socket_dir = _strict_socket(arguments[0])
        port = _strict_digits(arguments[1], 1, 65535)
        database = _strict_text(arguments[2])
        database_user = _strict_text(arguments[3])
        server_user = _strict_text(arguments[4])
        connect_s = _strict_digits(arguments[5], 1, 2147483647)
        statement_ms = _strict_digits(arguments[6], 1, 2147483647)
        lock_ms = _strict_digits(arguments[7], 1, 2147483647)
        io_ms = _strict_digits(arguments[8], 1, 2147483647)
        expected = _strict_digits(arguments[9], 1, 2147483647)
        self._arguments = arguments
        self._socket_dir = socket_dir
        self._port = port
        self._database = database
        self._database_user = database_user
        self._server_user = server_user
        self._connect_s = connect_s
        self._statement_ms = statement_ms
        self._lock_ms = lock_ms
        self._io_ms = io_ms
        self._expected_version = expected
        self._closed = False

    cdef void _require_owner_open(self):
        if self._closed or self._failed:
            raise InspectionError("PA01_SQL_CLOSED")
        if threading.get_ident() != self._owner_thread or os.getpid() != self._owner_pid:
            raise InspectionError("PA01_SQL_OWNER_REQUIRED")

    cdef void _condemn(self):
        if self._conn != NULL:
            PQfinish(self._conn)
            self._conn = NULL
        self._failed = True
        self._busy = False

    def connect(self):
        cdef const char *keywords[15]
        cdef const char *values[15]
        cdef const char *encoding
        cdef bytes key_item, value_item
        cdef PostgresPollingStatusType polling
        cdef int socket_fd
        cdef double deadline
        self._require_owner_open()
        _assert_no_postgres_c_environ()
        if self._busy:
            raise InspectionError("PA01_SQL_BUSY")
        if self._conn != NULL:
            raise InspectionError("PA01_SQL_ALREADY_CONNECTED")
        if PQlibVersion() != 170011:
            self._condemn()
            raise InspectionError("PA01_SQL_VERSION_MISMATCH")
        deadline = time.monotonic() + float(self._connect_s)
        b_host = self._arguments[0]
        b_port = self._arguments[1]
        b_db = self._arguments[2]
        b_user = self._arguments[3]
        b_timeout = self._arguments[5]
        b_options = b"-c search_path= -c default_transaction_read_only=on -c statement_timeout=" + self._arguments[6] + b" -c lock_timeout=" + self._arguments[7]
        b_peer = self._arguments[4]
        b_pass = b"/dev/null"
        b_auth = b"none"
        b_off = b"disable"
        k = (b"host", b"port", b"dbname", b"user", b"connect_timeout", b"options", b"requirepeer", b"passfile", b"require_auth", b"sslmode", b"gssencmode", b"sslcertmode", b"channel_binding", b"client_encoding")
        v = (b_host, b_port, b_db, b_user, b_timeout, b_options, b_peer, b_pass, b_auth, b_off, b_off, b_off, b_off, b"UTF8")
        for index in range(14):
            key_item, value_item = k[index], v[index]
            keywords[index] = key_item
            values[index] = value_item
        keywords[14] = NULL
        values[14] = NULL
        self._busy = True
        self._conn = PQconnectStartParams(keywords, values, 0)
        if self._conn == NULL:
            self._condemn()
            raise InspectionError("PA01_SQL_CONNECT_FAILED")
        try:
            while True:
                if time.monotonic() >= deadline:
                    raise InspectionError("PA01_SQL_CONNECT_TIMEOUT")
                polling = PQconnectPoll(self._conn)
                if polling == PGRES_POLLING_OK:
                    break
                if polling == PGRES_POLLING_FAILED:
                    raise InspectionError("PA01_SQL_CONNECT_FAILED")
                socket_fd = PQsocket(self._conn)
                if socket_fd < 0 or time.monotonic() >= deadline:
                    raise InspectionError("PA01_SQL_CONNECT_TIMEOUT")
                import select as pyselect
                remaining = deadline - time.monotonic()
                if polling == PGRES_POLLING_READING:
                    pyselect.select([socket_fd], [], [], max(0.0, remaining))
                elif polling == PGRES_POLLING_WRITING:
                    pyselect.select([], [socket_fd], [], max(0.0, remaining))
                else:
                    raise InspectionError("PA01_SQL_CONNECT_FAILED")
            if PQstatus(self._conn) != CONNECTION_OK:
                raise InspectionError("PA01_SQL_CONNECT_FAILED")
            if PQsetnonblocking(self._conn, 1) != 0:
                raise InspectionError("PA01_SQL_CONNECT_FAILED")
            if PQserverVersion(self._conn) != self._expected_version:
                raise InspectionError("PA01_SQL_VERSION_MISMATCH")
            if PQhost(self._conn) == NULL or PQport(self._conn) == NULL or PQdb(self._conn) == NULL or PQuser(self._conn) == NULL:
                raise InspectionError("PA01_SQL_CONNECT_FAILED")
            host = PQhost(self._conn).decode("utf-8", "strict")
            port = PQport(self._conn).decode("utf-8", "strict")
            database = PQdb(self._conn).decode("utf-8", "strict")
            user = PQuser(self._conn).decode("utf-8", "strict")
            if host != self._socket_dir or port != str(self._port) or database != self._database or user != self._database_user:
                raise InspectionError("PA01_SQL_CONNECT_FAILED")
            encoding = PQparameterStatus(self._conn, "client_encoding")
            if encoding == NULL or encoding.decode("utf-8", "strict") != "UTF8":
                raise InspectionError("PA01_SQL_CONNECT_FAILED")
            self._busy = False
        except UnicodeDecodeError as error:
            self._condemn()
            raise InspectionError("PA01_SQL_RESULT_ENCODING_INVALID") from error
        except OSError as error:
            self._condemn()
            raise InspectionError("PA01_SQL_TRANSPORT_INVALID") from error
        except BaseException:
            self._condemn()
            raise

    cdef list _exec_private(self, bytes statement, list byte_params, double deadline, int max_result_bytes, int expected_cols):
        cdef PGresult *result = NULL
        cdef int socket_fd
        cdef int rows, cols, row, col, length, total = 0
        cdef int result_count = 0
        cdef char *cell
        cdef char *name
        cdef const char *c_params[2]
        cdef bytes held0
        cdef bytes held1
        self._require_owner_open()
        if self._conn == NULL:
            raise InspectionError("PA01_SQL_NOT_CONNECTED")
        if time.monotonic() >= deadline:
            self._condemn()
            raise InspectionError("PA01_SQL_QUERY_TIMEOUT")
        if len(byte_params) == 2:
            held0 = byte_params[0]
            held1 = byte_params[1]
            c_params[0] = held0
            c_params[1] = held1
            sent = PQsendQueryParams(self._conn, statement, 2, NULL, c_params, NULL, NULL, 0)
        elif len(byte_params) == 1:
            held0 = byte_params[0]
            c_params[0] = held0
            sent = PQsendQueryParams(self._conn, statement, 1, NULL, c_params, NULL, NULL, 0)
        elif len(byte_params) == 0:
            sent = PQsendQueryParams(self._conn, statement, 0, NULL, NULL, NULL, NULL, 0)
        else:
            raise InspectionError("PA01_SQL_ARGUMENT_INVALID")
        if sent != 1:
            self._condemn()
            raise InspectionError("PA01_SQL_QUERY_FAILED")
        socket_fd = PQsocket(self._conn)
        rows_out = []
        try:
            import select as pyselect
            while PQflush(self._conn) == 1:
                if time.monotonic() >= deadline:
                    raise InspectionError("PA01_SQL_QUERY_TIMEOUT")
                pyselect.select([], [socket_fd], [], max(0.0, deadline - time.monotonic()))
            if PQflush(self._conn) == -1:
                raise InspectionError("PA01_SQL_QUERY_FAILED")
            while True:
                if time.monotonic() >= deadline:
                    raise InspectionError("PA01_SQL_QUERY_TIMEOUT")
                if PQconsumeInput(self._conn) != 1:
                    raise InspectionError("PA01_SQL_QUERY_FAILED")
                if PQisBusy(self._conn) == 0:
                    break
                if time.monotonic() >= deadline:
                    raise InspectionError("PA01_SQL_QUERY_TIMEOUT")
                pyselect.select([socket_fd], [], [], max(0.0, deadline - time.monotonic()))
            while True:
                if time.monotonic() >= deadline:
                    raise InspectionError("PA01_SQL_QUERY_TIMEOUT")
                if PQconsumeInput(self._conn) != 1:
                    raise InspectionError("PA01_SQL_QUERY_FAILED")
                if PQisBusy(self._conn) != 0:
                    if time.monotonic() >= deadline:
                        raise InspectionError("PA01_SQL_QUERY_TIMEOUT")
                    pyselect.select([socket_fd], [], [], max(0.0, deadline - time.monotonic()))
                    continue
                result = PQgetResult(self._conn)
                if result == NULL:
                    break
                try:
                    result_count += 1
                    if result_count != 1 or PQresultStatus(result) != PGRES_TUPLES_OK:
                        raise InspectionError("PA01_SQL_RESULT_INVALID")
                    rows = PQntuples(result)
                    cols = PQnfields(result)
                    if rows not in (0, 1) or cols != expected_cols:
                        raise InspectionError("PA01_SQL_RESULT_INVALID")
                    record = []
                    for col in range(cols) if rows else ():
                        cell = PQgetvalue(result, 0, col)
                        length = PQgetlength(result, 0, col)
                        if cell == NULL or length < 0:
                            raise InspectionError("PA01_SQL_RESULT_INVALID")
                        total += length
                        if total > max_result_bytes:
                            raise InspectionError("PA01_SQL_RESULT_LIMIT")
                        name = PQfname(result, col)
                        if name == NULL or strlen(name) == 0:
                            raise InspectionError("PA01_SQL_RESULT_INVALID")
                        record.append(bytes(cell[:length]).decode("utf-8", "strict"))
                    rows_out.extend(record)
                finally:
                    PQclear(result)
                    result = NULL
        except BaseException:
            if result != NULL:
                PQclear(result)
            self._condemn()
            raise
        if result_count != 1:
            self._condemn()
            raise InspectionError("PA01_SQL_RESULT_INVALID")
        return rows_out

    def inspect_technical(self, role_name, database_name, max_result_bytes):
        self._require_owner_open()
        if self._busy:
            raise InspectionError("PA01_SQL_BUSY")
        _assert_no_postgres_c_environ()
        _strict_text(role_name)
        _strict_text(database_name)
        remaining = _strict_max_result_bytes(max_result_bytes)
        deadline = time.monotonic() + float(self._io_ms) / 1000.0
        collected = []
        # Les seules requêtes et leurs colonnes sont fixées dans le module.
        recipes = (
            (_Q_ROLE_DB, [self._arguments[3], self._arguments[2]], 2),
            (_Q_SETTINGS, [], 3),
            (_Q_TARGET_ROLE, [role_name], 9),
            (_Q_TARGET_DATABASE, [database_name], 6))
        self._busy = True
        try:
            for statement, params, columns in recipes:
                values = self._exec_private(statement, params, deadline, remaining, columns)
                remaining -= sum(len(value.encode("utf-8")) for value in values)
                collected.append(values)
            identity, settings, target_role, target_database = collected
            if identity != ["t", "t"] or settings != ["on", "", "UTF8"]:
                raise InspectionError("PA01_SQL_SESSION_MISMATCH")
            if time.monotonic() >= deadline:
                raise InspectionError("PA01_SQL_QUERY_TIMEOUT")
            self._busy = False
            return {"role_attributes": tuple(target_role) if target_role else None,
                    "database_attributes": tuple(target_database) if target_database else None,
                    "authority_proven": False, "peer_hba_verified": False}
        except UnicodeDecodeError as error:
            self._condemn()
            raise InspectionError("PA01_SQL_RESULT_ENCODING_INVALID") from error
        except OSError as error:
            self._condemn()
            raise InspectionError("PA01_SQL_TRANSPORT_INVALID") from error
        except BaseException:
            self._condemn()
            raise

    def close(self):
        if self._busy:
            raise InspectionError("PA01_SQL_BUSY")
        if threading.get_ident() != self._owner_thread or os.getpid() != self._owner_pid:
            raise InspectionError("PA01_SQL_OWNER_REQUIRED")
        if self._conn != NULL:
            PQfinish(self._conn)
            self._conn = NULL
        self._closed = True

    def __enter__(self):
        self._require_owner_open()
        return self

    def __exit__(self, *ignored):
        self.close()

    def __dealloc__(self):
        if self._conn != NULL:
            PQfinish(self._conn)
            self._conn = NULL

    def __reduce__(self):
        raise TypeError("PA01_SQL_NOT_SERIALIZABLE")

    def __reduce_ex__(self, protocol):
        raise TypeError("PA01_SQL_NOT_SERIALIZABLE")

    def __copy__(self, *ignored):
        raise TypeError("PA01_SQL_NOT_COPYABLE")

    def __deepcopy__(self, *ignored):
        raise TypeError("PA01_SQL_NOT_COPYABLE")

    def __repr__(self):
        return "LibpqInspection(<redacted>)"
