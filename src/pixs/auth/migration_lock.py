"""Verrou et contrat d'application de la migration initiale Auth, Django seul.

Contrat figé validé avant tout effet : propriétaire pixs.auth, origine vierge
(None) seule supportée, cible 0.1.0 seule supportée, aucune contraction ni
rétrogradation ; les métadonnées Migration.pixs_owner/origin/target/effect/
compensation de 0001_auth_initial.py sont lues via importlib (nom de module à
chiffre initiale, import syntaxique impossible) et vérifiées champ par champ
avec types exacts avant comparaison, jamais supposées.
Alias explicite non vide de type str exact, moteur postgresql exigé (SQLite et
tout autre moteur refusés) ; ConnectionDoesNotExist depuis
django.utils.connection (compatibilité explicite). Bloc atomique externe
ambigu refusé avant acquisition ; transaction intérieure durable
(durable=True) ; RuntimeError non requalifiée : les défauts de programmation
et les interruptions se propagent avec rollback.
Namespace courant explicite unique : current_schema() et current_schemas(false)
de cette connexion, une seule entrée effective égale au namespace courant
(aucun mélange silencieux) ; inventaire restreint à ce namespace, sans
inspecter ni refuser les autres schémas hors search_path. OID base/namespace
capturés dans ce périmètre ; clé advisory 64 bits = int.from_bytes(
sha256(constante module + OID base + OID namespace), signé) : même scope même
clé, namespaces indépendants, aucun hash() Python, réduction standard du digest aux 64 bits signés.
Connexion physique capturée après acquire ; _release exige la même, non
remplacée, avant toute tentative curseur (aucune reconnexion suivie d'un unlock
prétendu) ; unlock confirmé True explicite, sinon erreur à réconcilier
(perte de connexion, session remplacée) ; corps et nettoyage conservés ensemble
(ExceptionGroup/BaseExceptionGroup 3.12, aucun masque).
Transaction durable propriétaire englobant ensure_schema + MigrationExecutor +
contrôles recorder/11 tables avant commit (aucune fenêtre DDL commité sans
recorder) ; résultat déterminé seulement après commit. État appliqué exige la
ligne recorder ET les 11 tables ; noms Auth inconnus ou tables partielles =>
refus sans effacement, sans DROP, sans tables voisines. Rejeu du même plan
arrivé à cible = idempotent sans nouvel effet.
Erreurs fixes sans identifiants PG ; causes opérationnelles (DatabaseError,
InterfaceError) chaînées avec précision ; aucun except large.
"""
from __future__ import annotations

import hashlib
import importlib

from django.db import DatabaseError, InterfaceError, connections, transaction
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.recorder import MigrationRecorder
from django.utils.connection import ConnectionDoesNotExist

__all__ = [
    "MigrationLockError",
    "APP_LABEL",
    "MIGRATION_NAME",
    "OWNER",
    "ORIGIN_VIERGE",
    "TARGET",
    "EXPECTED_TABLES",
    "MODULE_SEED",
    "validate_plan",
    "verify_migration_contract",
    "run_auth_initial",
]

FIXED_MESSAGE = "Migration Auth impossible."

APP_LABEL = "pixs_auth"
MIGRATION_NAME = "0001_auth_initial"
OWNER = "pixs.auth"
ORIGIN_VIERGE = None
TARGET = "0.1.0"
# Constante module figée pour la dérivation de clé (jamais hash() Python).
MODULE_SEED = b"pixs-auth-0001-initial-v1:"

EXPECTED_TABLES = frozenset({
    "pixs_auth_account_gate",
    "pixs_auth_binding",
    "pixs_auth_password_credential",
    "pixs_auth_policy_row",
    "pixs_auth_session",
    "pixs_auth_token",
    "pixs_auth_operation",
    "pixs_auth_audit_pending",
    "pixs_auth_bootstrap_authorization",
    "pixs_auth_local_trust_selection",
    "pixs_auth_identity_assurance",
})


class MigrationLockError(ValueError):
    """Refus fixe sans écho de valeur brute ni identifiant PG."""

    def __init__(self, code: str = "MIGRATION_AUTH_IMPOSSIBLE"):
        super().__init__(FIXED_MESSAGE)
        self.code = code
        self.element = "auth_migration"
        self.step = "apply_auth_initial"


def _connection(using: object):
    if type(using) is not str or using == "":
        raise MigrationLockError("ALIAS_INVALIDE") from None
    try:
        conn = connections[using]
    except ConnectionDoesNotExist as error:
        raise MigrationLockError("ALIAS_INCONNU") from error
    if conn.vendor != "postgresql":
        raise MigrationLockError("MOTEUR_NON_PG_REFUSE") from None
    return conn


def validate_plan(origin: object, target: object) -> bool:
    """Valide le plan réellement fourni : None -> 0.1.0 uniquement."""
    if origin is not None:
        raise MigrationLockError("ORIGINE_NON_SUPPORTEE") from None
    if type(target) is not str or target != TARGET:
        raise MigrationLockError("CIBLE_NON_SUPPORTEE") from None
    return True


def verify_migration_contract(origin: object, target: object) -> bool:
    """Vérifie les métadonnées Migration présentes contre le plan fourni."""
    try:
        module = importlib.import_module("pixs.auth.migrations.0001_auth_initial")
    except ImportError as error:
        raise MigrationLockError("CONTRAT_INTROUVABLE") from error
    try:
        migration_cls = module.Migration
    except AttributeError as error:
        raise MigrationLockError("CONTRAT_INCOMPLET") from error
    try:
        owner = migration_cls.pixs_owner
        m_origin = migration_cls.pixs_origin
        m_target = migration_cls.pixs_target
        effect = migration_cls.pixs_effect
        compensation = migration_cls.pixs_compensation
    except AttributeError as error:
        raise MigrationLockError("CONTRAT_INCOMPLET") from error
    if type(owner) is not str or owner != OWNER:
        raise MigrationLockError("CONTRAT_DIVERGENT") from None
    if m_origin is not None or m_origin is not origin:
        raise MigrationLockError("CONTRAT_DIVERGENT") from None
    if type(m_target) is not str or m_target != target:
        raise MigrationLockError("CONTRAT_DIVERGENT") from None
    if type(effect) is not str or effect == "":
        raise MigrationLockError("CONTRAT_INCOMPLET") from None
    if type(compensation) is not str or compensation == "":
        raise MigrationLockError("CONTRAT_INCOMPLET") from None
    return True


def _effective_namespace(conn) -> str:
    # Une seule entrée effective, égale au namespace courant ; le reste du
    # search_path hors périmètre n'est ni inspecté ni refusé.
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT current_schema();")
            row = cursor.fetchone()
        with conn.cursor() as cursor:
            cursor.execute("SELECT current_schemas(false);")
            paths = cursor.fetchone()
    except (DatabaseError, InterfaceError) as error:
        raise MigrationLockError("NAMESPACE_INVERIFIABLE") from error
    if row is None or type(row[0]) is not str or row[0] == "":
        raise MigrationLockError("NAMESPACE_INDETERMINE") from None
    namespace = row[0]
    if paths is None or type(paths[0]) is not list or len(paths[0]) != 1:
        raise MigrationLockError("NAMESPACE_AMBIGU") from None
    entry = paths[0][0]
    if type(entry) is not str or entry == "" or entry != namespace:
        raise MigrationLockError("NAMESPACE_AMBIGU") from None
    return namespace


def _scope_key(conn) -> int:
    # Dérivation déterministe : sha256 signed 64 bits, sans hash() Python.
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT oid FROM pg_database WHERE datname = current_database();")
            db_row = cursor.fetchone()
        with conn.cursor() as cursor:
            cursor.execute("SELECT oid FROM pg_namespace WHERE nspname = current_schema();")
            nsp_row = cursor.fetchone()
    except (DatabaseError, InterfaceError) as error:
        raise MigrationLockError("CLE_INCALCULABLE") from error
    if db_row is None or type(db_row[0]) is not int:
        raise MigrationLockError("BASE_INDETERMINEE") from None
    if nsp_row is None or type(nsp_row[0]) is not int:
        raise MigrationLockError("NAMESPACE_INDETERMINE") from None
    raw = (
        MODULE_SEED
        + str(db_row[0]).encode("ascii")
        + b":"
        + str(nsp_row[0]).encode("ascii")
    )
    digest = hashlib.sha256(raw).digest()
    return int.from_bytes(digest[:8], "big", signed=True)


def _namespace_tables(conn) -> set[str]:
    # Inventaire restreint au namespace courant : les autres schémas sont ignorés.
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT tablename FROM pg_tables WHERE schemaname = current_schema();"
            )
            rows = cursor.fetchall()
    except (DatabaseError, InterfaceError) as error:
        raise MigrationLockError("INVENTAIRE_INVERIFIABLE") from error
    tables: set[str] = set()
    for row in rows:
        if type(row[0]) is not str or row[0] == "":
            raise MigrationLockError("INVENTAIRE_INATTENDU") from None
        tables.add(row[0])
    return tables


def _snapshot_state(conn) -> str:
    # vierge : rien ; applique : ligne recorder ET 11 tables ; sinon refus.
    tables = _namespace_tables(conn)
    unknown_auth = {t for t in tables if t.startswith("pixs_auth_")} - EXPECTED_TABLES
    if unknown_auth:
        raise MigrationLockError("TABLES_INCONNUES") from None
    auth_present = tables & EXPECTED_TABLES
    auth_names: list[str] = []
    if "django_migrations" in tables:
        try:
            applied = MigrationRecorder(conn).applied_migrations()
        except (DatabaseError, InterfaceError) as error:
            raise MigrationLockError("RECORDER_ILLISIBLE") from error
        auth_names = sorted(name for (app, name) in applied if app == APP_LABEL)
        for name in auth_names:
            if type(name) is not str or name == "":
                raise MigrationLockError("RECORDER_INATTENDU") from None
        if MIGRATION_NAME in auth_names and len(auth_names) != 1:
            raise MigrationLockError("MIGRATION_INCONNUE") from None
    if MIGRATION_NAME in auth_names:
        if auth_present != EXPECTED_TABLES:
            raise MigrationLockError("ETAT_PARTIEL_REFUSE") from None
        return "applique"
    if auth_names:
        raise MigrationLockError("MIGRATION_INCONNUE") from None
    if auth_present:
        raise MigrationLockError("ETAT_PARTIEL_REFUSE") from None
    return "vierge"


def _acquire(conn, key: int) -> bool:
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT pg_try_advisory_lock(%s);", [key])
            row = cursor.fetchone()
    except (DatabaseError, InterfaceError) as error:
        raise MigrationLockError("VERROU_INACQUIS") from error
    if row is None or row[0] is not True:
        raise MigrationLockError("EXECUTEUR_CONCURRENT") from None
    return True


def _release(conn, key: int, physical: object) -> bool:
    # Même connexion physique exigée avant toute tentative curseur : aucune
    # reconnexion suivie d'un unlock prétendu. True confirmé ou réconciliation.
    if physical is None:
        raise MigrationLockError("VERROU_NON_LIBERE") from None
    try:
        current = conn.connection
    except (DatabaseError, InterfaceError) as error:
        raise MigrationLockError("VERROU_NON_LIBERE") from error
    if current is not physical:
        raise MigrationLockError("VERROU_NON_LIBERE") from None
    try:
        with conn.cursor() as cursor:
            if conn.connection is not physical:
                raise MigrationLockError("VERROU_NON_LIBERE")
            cursor.execute("SELECT pg_advisory_unlock(%s);", [key])
            row = cursor.fetchone()
    except (DatabaseError, InterfaceError) as error:
        raise MigrationLockError("VERROU_NON_LIBERE") from error
    if row is None or row[0] is not True:
        raise MigrationLockError("VERROU_NON_LIBERE") from None
    return True


def _apply_locked(conn, using: str) -> str:
    state = _snapshot_state(conn)
    if state == "applique":
        return "already_applied"
    with transaction.atomic(using=using, durable=True):
        try:
            MigrationRecorder(conn).ensure_schema()
            executor = MigrationExecutor(conn)
            executor.migrate([(APP_LABEL, MIGRATION_NAME)])
        except (DatabaseError, InterfaceError) as error:
            raise MigrationLockError("APPLICATION_IMPOSSIBLE") from error
        try:
            applied = MigrationRecorder(conn).applied_migrations()
        except (DatabaseError, InterfaceError) as error:
            raise MigrationLockError("RECORDER_ILLISIBLE") from error
        if (APP_LABEL, MIGRATION_NAME) not in applied:
            raise MigrationLockError("AVANCEMENT_DIVERGENT") from None
        if (_namespace_tables(conn) & EXPECTED_TABLES) != EXPECTED_TABLES:
            raise MigrationLockError("AVANCEMENT_DIVERGENT") from None
    return "applied"


def run_auth_initial(using: object, *, origin: object, target: object) -> str:
    """Applique 0001_auth_initial sous verrou : idempotent, sans effacement."""
    conn = _connection(using)
    if conn.in_atomic_block:
        raise MigrationLockError("BLOC_EXTERNE_AMBIGU") from None
    validate_plan(origin, target)
    verify_migration_contract(origin, target)
    _effective_namespace(conn)
    key = _scope_key(conn)
    acquired = False
    physical: object = None
    failed: BaseException | None = None
    try:
        _acquire(conn, key)
        acquired = True
        physical = conn.connection
        outcome = _apply_locked(conn, using)
    except BaseException as exc:
        # Conservé uniquement pour grouper avec une erreur de nettoyage
        # simultanée ; sinon re-levée pure avec rollback (aucun masque).
        failed = exc
        raise
    finally:
        if acquired:
            try:
                _release(conn, key, physical)
            except BaseException as release_error:
                if failed is not None:
                    if isinstance(failed, Exception) and isinstance(release_error, Exception):
                        raise ExceptionGroup(FIXED_MESSAGE, [failed, release_error]) from None
                    raise BaseExceptionGroup(FIXED_MESSAGE, [failed, release_error]) from None
                raise
    return outcome
