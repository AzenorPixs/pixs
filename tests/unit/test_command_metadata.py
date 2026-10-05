"""Tests déclaratifs partiels de pixs.core.command_metadata.

Aucune garantie d'exécution n'est testée ici : comparaison de payload,
restitution, conflit de rejou, déduplication, persistance, transaction,
autorisation et exécution restent NON PROUVÉS.
"""

import dataclasses
import unittest

from pixs.core import command_metadata as cm
from pixs.core.command_metadata import CommandMetadata, validate_command_metadata
from pixs.core.scope import (
    ScopeContext,
    ScopeStructureError,
    ScopeType,
    validate_structure,
)
from pixs.kernel.diagnostics import VALIDATE, Diagnostic

_FIELD_ELEMENTS = (
    "command_metadata.command_id",
    "command_metadata.correlation_ids",
    "command_metadata.causation_ids",
    "command_metadata.scope_context",
    "command_metadata.command_type",
    "command_metadata.subject_id",
    "command_metadata.idempotency_key",
)
_OPAQUE_FIELDS = ("command_id", "command_type", "subject_id", "idempotency_key")
_TUPLE_FIELDS = ("correlation_ids", "causation_ids")


class CallbackStr(str):
    """Sous-classe hostile de str comptant tout callback de valeur."""

    def __init__(self, *args):
        self.calls = []

    def __bool__(self):
        self.calls.append("bool")
        return str.__len__(self) > 0

    def __len__(self):
        self.calls.append("len")
        return str.__len__(self)

    def __str__(self):
        self.calls.append("str")
        return str.__str__(self)


class CallbackTuple(tuple):
    """Sous-classe hostile de tuple comptant conteneur et éléments."""

    def __init__(self, *args):
        self.calls = []

    def __len__(self):
        self.calls.append("len")
        return tuple.__len__(self)

    def __iter__(self):
        self.calls.append("iter")
        return tuple.__iter__(self)

    def __getitem__(self, index):
        self.calls.append("getitem")
        return tuple.__getitem__(self, index)


class NoRead:
    """Objet étranger dont toute lecture d'attribut est une faute."""

    def __init__(self):
        self.calls = []

    def __getattr__(self, name):
        self.calls.append(name)
        raise AssertionError(f"lecture d'attribut interdite : {name}")


class CountingCommand(CommandMetadata):
    """Sous-classe de CommandMetadata comptant toute lecture d'attribut."""

    reads = []

    def __getattribute__(self, name):
        if name != "reads":
            CountingCommand.reads.append(name)
        return object.__getattribute__(self, name)


class Base(unittest.TestCase):
    def setUp(self):
        self._real_validate_structure = cm.validate_structure

    def tearDown(self):
        cm.validate_structure = self._real_validate_structure

    def make_valid(self, **overrides):
        fields = {
            "command_id": "cmd-1",
            "correlation_ids": ("corr-1", "corr-2"),
            "causation_ids": ("cause-1",),
            "scope_context": ScopeContext(ScopeType.TENANT, "tenant-1", "scope-1"),
            "command_type": "type-1",
            "subject_id": "subject-1",
            "idempotency_key": "key-1",
        }
        fields.update(overrides)
        return CommandMetadata(**fields)

    def spy_validate_structure(self):
        calls = []
        original = self._real_validate_structure

        def spy(ctx):
            calls.append(ctx)
            return original(ctx)

        cm.validate_structure = spy
        return calls

    def elements(self, diagnostics):
        return sorted(diagnostic.element for diagnostic in diagnostics)


class ExportsTests(unittest.TestCase):
    def test_exports_exactement_deux(self):
        self.assertEqual(cm.__all__, ["CommandMetadata", "validate_command_metadata"])
        self.assertIs(cm.CommandMetadata, CommandMetadata)
        self.assertIs(cm.validate_command_metadata, validate_command_metadata)


class StructureTests(Base):
    def test_champs_obligatoires_dans_ordre_fige_sans_defaut(self):
        champs = dataclasses.fields(CommandMetadata)
        self.assertEqual(
            tuple(champ.name for champ in champs),
            (
                "command_id",
                "correlation_ids",
                "causation_ids",
                "scope_context",
                "command_type",
                "subject_id",
                "idempotency_key",
            ),
        )
        for champ in champs:
            self.assertIs(champ.default, dataclasses.MISSING)
            self.assertIs(champ.default_factory, dataclasses.MISSING)
            self.assertIsInstance(champ.type, str)
        self.assertEqual(
            CommandMetadata.__match_args__,
            tuple(champ.name for champ in champs),
        )

    def test_gelee_slots_sans_post_init_ni_methode_applicative(self):
        self.assertTrue(CommandMetadata.__dataclass_params__.frozen)
        self.assertIn("__slots__", CommandMetadata.__dict__)
        self.assertFalse(hasattr(CommandMetadata, "__post_init__"))
        methodes = {
            nom
            for nom, valeur in CommandMetadata.__dict__.items()
            if callable(valeur) and not nom.startswith("__")
        }
        self.assertEqual(methodes, set())

    def test_constructeur_accepte_valeurs_invalides(self):
        informe = CommandMetadata(
            None, None, None, None, None, None, None
        )
        diagnostics = validate_command_metadata(informe)
        self.assertEqual(self.elements(diagnostics), sorted(_FIELD_ELEMENTS))

    def test_assignation_refusee_et_copie_non_mutables(self):
        command = self.make_valid()
        self.assertFalse(hasattr(command, "__dict__"))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            command.command_id = "autre"


class CommandeEtrangereTests(Base):
    def test_type_etranger_refuse_sans_lecture(self):
        hostile = NoRead()
        with self.assertRaises(AssertionError):
            _ = hostile.command_id
        self.assertEqual(hostile.calls, ["command_id"])
        hostile.calls.clear()
        for etranger in (None, "cmd", 42, (), {}, hostile):
            with self.subTest(type=type(etranger).__name__):
                diagnostics = validate_command_metadata(etranger)
                self.assertEqual(len(diagnostics), 1)
                self.assertEqual(diagnostics[0].element, "command_metadata.command")
                self.assertEqual(diagnostics[0].step, VALIDATE)
                self.assertEqual(diagnostics[0].constraint, diagnostics[0].message)
                self.assertTrue(
                    diagnostics[0].constraint.startswith("command_metadata.command: ")
                )

        self.assertEqual(hostile.calls, [])

    def test_sous_classe_refusee_sans_lecture_de_champ(self):
        compteur = CountingCommand(
            "cmd-1",
            ("corr",),
            ("cause",),
            ScopeContext(ScopeType.TENANT, "t1"),
            "type-1",
            "subject-1",
            "key-1",
        )
        CountingCommand.reads = []
        _ = compteur.command_id
        self.assertEqual(CountingCommand.reads, ["command_id"])
        CountingCommand.reads = []
        diagnostics = validate_command_metadata(compteur)
        self.assertEqual(CountingCommand.reads, [])
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].element, "command_metadata.command")
        CountingCommand.reads = []


class ChampsOpaquesTests(Base):
    def test_valeurs_non_exactes_refusees_sans_callback(self):
        hostiles = (None, "", True, False, 0, 42, [], (), {}, object())
        for nom in _OPAQUE_FIELDS:
            for valeur in hostiles:
                with self.subTest(champ=nom, valeur=type(valeur).__name__):
                    diagnostics = validate_command_metadata(
                        self.make_valid(**{nom: valeur})
                    )
                    attendu = [f"command_metadata.{nom}"]
                    self.assertEqual(self.elements(diagnostics), attendu)

    def test_sous_classe_str_refusee_apres_probe_positif_et_reset(self):
        for nom in _OPAQUE_FIELDS:
            with self.subTest(champ=nom):
                hostile = CallbackStr("SENTINEL_OPAQUE")
                self.assertEqual(len(hostile), 15)
                self.assertTrue(bool(hostile))
                self.assertIsInstance(str(hostile), str)
                self.assertEqual(len(hostile.calls), 3)
                hostile.calls.clear()
                diagnostics = validate_command_metadata(self.make_valid(**{nom: hostile}))
                self.assertEqual(hostile.calls, [])
                self.assertEqual(self.elements(diagnostics), [f"command_metadata.{nom}"])

    def test_espaces_valables_comme_references_opaques(self):
        command = self.make_valid(
            command_id=" ",
            command_type="  ",
            subject_id="\t ",
            idempotency_key="   ",
        )
        self.assertEqual(validate_command_metadata(command), [])


class ChampsTuplesTests(Base):
    def test_conteneur_non_exact_refuse_avant_callbacks(self):
        for nom in _TUPLE_FIELDS:
            conteneurs = (
                None,
                "",
                "tuple",
                [],
                ["a"],
                {},
                object(),
            )
            for valeur in conteneurs:
                with self.subTest(champ=nom, valeur=type(valeur).__name__):
                    diagnostics = validate_command_metadata(
                        self.make_valid(**{nom: valeur})
                    )
                    self.assertEqual(self.elements(diagnostics), [f"command_metadata.{nom}"])
            hostile = CallbackTuple(("a", "b"))
            self.assertEqual(len(hostile), 2)
            self.assertEqual(list(iter(hostile)), ["a", "b"])
            self.assertEqual(hostile[0], "a")
            self.assertEqual(len(hostile.calls), 3)
            hostile.calls.clear()
            diagnostics = validate_command_metadata(self.make_valid(**{nom: hostile}))
            self.assertEqual(hostile.calls, [])
            self.assertEqual(self.elements(diagnostics), [f"command_metadata.{nom}"])

    def test_elements_non_str_refuses_apres_probe_et_reset(self):
        for nom in _TUPLE_FIELDS:
            hostile_item = CallbackStr("SENTINEL_ITEM")
            self.assertTrue(bool(hostile_item))
            self.assertEqual(len(hostile_item), 13)
            self.assertEqual(str(hostile_item), "SENTINEL_ITEM")
            self.assertEqual(hostile_item.calls, ["bool", "len", "str"])
            hostile_item.calls.clear()
            for item in (None, "", True, False, 0, 7, [], (), {}, object(), hostile_item):
                with self.subTest(champ=nom, type=type(item).__name__):
                    diagnostics = validate_command_metadata(
                        self.make_valid(**{nom: ("a", item)})
                    )
                    self.assertEqual(hostile_item.calls, [])
                    self.assertEqual(
                        self.elements(diagnostics), [f"command_metadata.{nom}"]
                    )

    def test_tuple_vide_ordre_doublons_et_espaces_conservés(self):
        command = self.make_valid(correlation_ids=(), causation_ids=())
        self.assertEqual(validate_command_metadata(command), [])
        ordre = ("b", "a", "b", " ", "a")
        command = self.make_valid(correlation_ids=ordre)
        self.assertIs(command.correlation_ids, ordre)
        self.assertEqual(validate_command_metadata(command), [])

    def test_au_plus_un_diagnostic_par_champ_multi_invalides(self):
        command = self.make_valid(correlation_ids=("a", 1, "", 2))
        diagnostics = validate_command_metadata(command)
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].element, "command_metadata.correlation_ids")


class ScopeContextTests(Base):
    def test_règles_existantes_acceptees_sans_reinvention(self):
        tenant_espaces = ScopeContext(ScopeType.TENANT, "   ", "  ")
        platform = ScopeContext(ScopeType.PLATFORM)
        for ctx in (tenant_espaces, platform):
            with self.subTest(type=ctx.scope_type.name):
                command = self.make_valid(scope_context=ctx)
                self.assertEqual(validate_command_metadata(command), [])

    def test_type_etranger_refuse_avant_appel_public(self):
        calls = self.spy_validate_structure()
        hostile = NoRead()
        with self.assertRaises(AssertionError):
            _ = hostile.scope_type
        self.assertEqual(hostile.calls, ["scope_type"])
        hostile.calls.clear()
        for etranger in (None, "scope", object(), hostile, ScopeType.TENANT):
            with self.subTest(valeur=type(etranger).__name__):
                diagnostics = validate_command_metadata(
                    self.make_valid(scope_context=etranger)
                )
                self.assertEqual(
                    self.elements(diagnostics), ["command_metadata.scope_context"]
                )
        self.assertEqual(calls, [])
        self.assertEqual(hostile.calls, [])

    def test_sous_classe_scope_refusee_par_type_exact(self):
        class EvilScope(ScopeContext):
            reads = []

            def __getattribute__(self, name):
                if name in ("scope_type", "tenant_id", "scope_id"):
                    EvilScope.reads.append(name)
                return object.__getattribute__(self, name)

        hostile = object.__new__(EvilScope)
        object.__setattr__(hostile, "scope_type", ScopeType.PLATFORM)
        object.__setattr__(hostile, "tenant_id", None)
        object.__setattr__(hostile, "scope_id", None)
        self.assertIs(hostile.scope_type, ScopeType.PLATFORM)
        self.assertEqual(EvilScope.reads, ["scope_type"])
        EvilScope.reads.clear()
        calls = self.spy_validate_structure()
        diagnostics = validate_command_metadata(
            self.make_valid(scope_context=hostile)
        )
        self.assertEqual(calls, [])
        self.assertEqual(EvilScope.reads, [])
        self.assertEqual(
            self.elements(diagnostics), ["command_metadata.scope_context"]
        )

    def test_contexte_exact_malforme_converti_seule_erreur_attendue(self):
        calls = self.spy_validate_structure()
        malformed = object.__new__(ScopeContext)
        object.__setattr__(malformed, "scope_type", ScopeType.TENANT)
        object.__setattr__(malformed, "tenant_id", "")
        object.__setattr__(malformed, "scope_id", None)
        with self.assertRaises(ScopeStructureError):
            validate_structure(malformed)
        diagnostics = validate_command_metadata(self.make_valid(scope_context=malformed))
        self.assertEqual(len(calls), 1)
        self.assertIs(calls[0], malformed)
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].element, "command_metadata.scope_context")
        self.assertEqual(diagnostics[0].step, VALIDATE)
        self.assertEqual(diagnostics[0].constraint, diagnostics[0].message)
        self.assertTrue(
            diagnostics[0].constraint.startswith("command_metadata.scope_context: ")
        )


class EspionValideurPublicTests(Base):
    def test_appel_seulement_sur_contexte_exact_et_independant_des_autres_champs(self):
        ctx = ScopeContext(ScopeType.TENANT, "t1")
        calls = self.spy_validate_structure()
        self.assertEqual(validate_command_metadata(self.make_valid(scope_context=ctx)), [])
        self.assertEqual(calls, [ctx])
        del calls[:]
        command = self.make_valid(
            scope_context=ctx,
            command_id=None,
            correlation_ids="non-tuple",
            causation_ids=7,
            command_type="",
            subject_id=object(),
            idempotency_key=(),
        )
        diagnostics = validate_command_metadata(command)
        self.assertEqual(calls, [ctx])
        self.assertEqual(len(diagnostics), 6)
        self.assertNotIn("command_metadata.scope_context", self.elements(diagnostics))

    def test_exceptions_inattendues_propagees_a_l_identique(self):
        ctx = ScopeContext(ScopeType.TENANT, "t1")
        command = self.make_valid(scope_context=ctx)

        for exception in (
            ValueError("inattendue"),
            RuntimeError("inattendue"),
            KeyboardInterrupt(),
            SystemExit(3),
        ):
            with self.subTest(exc=type(exception).__name__):
                def leve(_ctx, _exc=exception):
                    raise _exc

                cm.validate_structure = leve
                with self.assertRaises(type(exception)) as captured:
                    validate_command_metadata(command)
                self.assertIs(captured.exception, exception)


class AggregationDiagnosticsTests(Base):
    def make_all_invalid(self):
        return CommandMetadata(
            CallbackStr("SENTINEL_ID"),
            ["SENTINEL_COR"],
            object(),
            NoRead(),
            "",
            CallbackStr("SENTINEL_SUBJECT"),
            ("SENTINEL_KEY",),
        )

    def test_sept_champs_invalides_exactement_sept_diagnostics_tries(self):
        command = self.make_all_invalid()
        diagnostics = validate_command_metadata(command)
        self.assertEqual(self.elements(diagnostics), sorted(_FIELD_ELEMENTS))
        self.assertEqual(len(diagnostics), 7)
        keys = [(d.element, d.constraint, d.message) for d in diagnostics]
        self.assertEqual(keys, sorted(keys))
        self.assertEqual(len(keys), len(set(keys)))
        for diagnostic in diagnostics:
            self.assertIsInstance(diagnostic, Diagnostic)
            self.assertEqual(diagnostic.step, VALIDATE)
            self.assertEqual(diagnostic.constraint, diagnostic.message)
            self.assertTrue(diagnostic.constraint.startswith(diagnostic.element + ": "))
            self.assertNotIn("SENTINEL", str(diagnostic))
            self.assertNotIn("SENTINEL", diagnostic.constraint)
            self.assertNotIn("command_metadata.command", self.elements(diagnostics))

    def test_messages_stables_entre_appels(self):
        premier = validate_command_metadata(self.make_all_invalid())
        second = validate_command_metadata(self.make_all_invalid())
        self.assertEqual(
            [(d.element, d.constraint, d.message) for d in premier],
            [(d.element, d.constraint, d.message) for d in second],
        )

    def test_listes_fraiches_independantes_apres_mutation(self):
        premier = validate_command_metadata(self.make_all_invalid())
        second = validate_command_metadata(self.make_all_invalid())
        self.assertIsNot(premier, second)
        self.assertIsNot(premier[0], second[0])
        premier.clear()
        self.assertEqual(len(second), 7)
        neuvieme = validate_command_metadata(self.make_all_invalid())
        self.assertEqual(len(neuvieme), 7)
        vide = validate_command_metadata(self.make_valid())
        self.assertIsInstance(vide, list)
        self.assertEqual(vide, [])
        autre = validate_command_metadata(self.make_valid())
        self.assertIsNot(vide, autre)
        vide.append(object())
        self.assertEqual(autre, [])
        self.assertEqual(validate_command_metadata(self.make_valid()), [])


if __name__ == "__main__":
    unittest.main()
