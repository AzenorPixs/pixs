"""Tests du collecteur structurel des dimensions d'idempotence §18.

Aucune capacité d'exécution n'est testée ici : lookup, déduplication, rejou,
rétention, persistance, transaction ou autorisation restent NON PROUVÉS. Le
validateur public de `command_metadata` n'est pas re-testé règle par règle :
seules sa délégation exacte et la traversée de ses résultats sont couvertes.
"""

import dataclasses
import unittest

from pixs.core import idempotency_dimensions as dim
from pixs.core.command_metadata import CommandMetadata
from pixs.core.idempotency_dimensions import (
    CommandIdempotencyDimensions,
    collect_command_idempotency_dimensions,
)
from pixs.core.scope import ScopeContext, ScopeType
from pixs.kernel.diagnostics import VALIDATE, Diagnostic


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


class Boom(BaseException):
    """BaseException inattendue, hors ValueError."""


class Base(unittest.TestCase):
    def setUp(self):
        self._real_validate = dim.validate_command_metadata
        self.spy_calls = []
        self.spy_results = []

    def tearDown(self):
        dim.validate_command_metadata = self._real_validate

    def install_spy(self, behavior=None):
        self.spy_calls.clear()
        self.spy_results.clear()
        original = self._real_validate

        def spy(command):
            self.spy_calls.append(command)
            result = original(command) if behavior is None else behavior(command)
            self.spy_results.append(result)
            return result

        dim.validate_command_metadata = spy

    def make_tenant(self, **overrides):
        fields = {
            "command_id": "cmd-1",
            "correlation_ids": ("corr-1", "corr-1", " "),
            "causation_ids": ("cause-1",),
            "scope_context": ScopeContext(ScopeType.TENANT, "tenant-1", "scope-1"),
            "command_type": "type-1",
            "subject_id": "subject-1",
            "idempotency_key": "key-1",
        }
        fields.update(overrides)
        return CommandMetadata(**fields)


class ExportsStructureTests(unittest.TestCase):
    def test_exports_exactement_deux(self):
        self.assertEqual(
            dim.__all__,
            ["CommandIdempotencyDimensions", "collect_command_idempotency_dimensions"],
        )
        self.assertIs(dim.CommandIdempotencyDimensions, CommandIdempotencyDimensions)
        self.assertIs(
            dim.collect_command_idempotency_dimensions,
            collect_command_idempotency_dimensions,
        )

    def test_quatre_champs_obligatoires_dans_ordre_et_annotations_du_paragraphe18(self):
        champs = dataclasses.fields(CommandIdempotencyDimensions)
        self.assertEqual(
            tuple(champ.name for champ in champs),
            ("tenant_id", "subject_id", "command_type", "idempotency_key"),
        )
        self.assertEqual(
            tuple(champ.type for champ in champs),
            ("str | None", "str", "str", "str"),
        )
        for champ in champs:
            self.assertIs(champ.default, dataclasses.MISSING)
            self.assertIs(champ.default_factory, dataclasses.MISSING)
        self.assertEqual(
            CommandIdempotencyDimensions.__match_args__,
            tuple(champ.name for champ in champs),
        )

    def test_gelee_slots_sans_post_init_ni_methode_applicative(self):
        self.assertTrue(CommandIdempotencyDimensions.__dataclass_params__.frozen)
        self.assertIn("__slots__", CommandIdempotencyDimensions.__dict__)
        self.assertFalse(hasattr(CommandIdempotencyDimensions, "__post_init__"))
        methodes = {
            nom
            for nom, valeur in CommandIdempotencyDimensions.__dict__.items()
            if callable(valeur) and not nom.startswith("__")
        }
        self.assertEqual(methodes, set())
        instance = CommandIdempotencyDimensions(None, "s", "t", "k")
        self.assertFalse(hasattr(instance, "__dict__"))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            instance.subject_id = "autre"

    def test_constructeur_non_validant_sans_callback(self):
        hostile = CallbackStr("SENTINEL_CONSTRUCT")
        self.assertTrue(bool(hostile))
        self.assertEqual(len(hostile), 18)
        self.assertEqual(str(hostile), "SENTINEL_CONSTRUCT")
        self.assertEqual(hostile.calls, ["bool", "len", "str"])
        hostile.calls.clear()
        informe = CommandIdempotencyDimensions(None, hostile, object(), object())
        informe_none = CommandIdempotencyDimensions(None, None, None, None)
        self.assertIsNone(informe_none.tenant_id)
        self.assertIsNone(informe_none.subject_id)
        self.assertIsNone(informe_none.command_type)
        self.assertIsNone(informe_none.idempotency_key)
        self.assertEqual(hostile.calls, [])
        self.assertIs(informe.subject_id, hostile)
        self.assertIsNone(informe.tenant_id)
        informe2 = CommandIdempotencyDimensions(
            "  ", "  ", "  ", "  "
        )
        self.assertEqual(informe2.tenant_id, "  ")


class CollecteurSuccessTests(Base):
    def test_succes_tenant_quatre_valeurs_identiques_liste_du_spy_traversee(self):
        self.install_spy()
        tenant_value = "tenant-1"
        subject_value = "subject-1"
        type_value = "type-1"
        key_value = "key-1"
        command = self.make_tenant(
            subject_id=subject_value,
            command_type=type_value,
            idempotency_key=key_value,
            scope_context=ScopeContext(ScopeType.TENANT, tenant_value, "scope-1"),
        )
        snapshot = dataclasses.asdict(command)
        correlations = command.correlation_ids
        causations = command.causation_ids
        result = collect_command_idempotency_dimensions(command)
        dimensions, diagnostics = result
        self.assertEqual(self.spy_calls, [command])
        self.assertEqual(self.spy_results, [diagnostics])
        self.assertIs(diagnostics, self.spy_results[0])
        self.assertEqual(diagnostics, [])
        self.assertIsInstance(dimensions, CommandIdempotencyDimensions)
        self.assertIs(dimensions.tenant_id, tenant_value)
        self.assertIs(dimensions.subject_id, subject_value)
        self.assertIs(dimensions.command_type, type_value)
        self.assertIs(dimensions.idempotency_key, key_value)
        self.assertEqual(dataclasses.asdict(command), snapshot)
        self.assertIs(command.correlation_ids, correlations)
        self.assertIs(command.causation_ids, causations)

    def test_succes_platform_tenant_none_conserve(self):
        self.install_spy()
        command = self.make_tenant(scope_context=ScopeContext(ScopeType.PLATFORM))
        dimensions, diagnostics = collect_command_idempotency_dimensions(command)
        self.assertEqual(self.spy_calls, [command])
        self.assertIs(diagnostics, self.spy_results[0])
        self.assertEqual(diagnostics, [])
        self.assertIsNone(dimensions.tenant_id)
        self.assertEqual(
            (dimensions.subject_id, dimensions.command_type, dimensions.idempotency_key),
            ("subject-1", "type-1", "key-1"),
        )

    def test_opacites_espaces_collectees_telles_quelles(self):
        self.install_spy()
        tenant = " "
        scope = "  "
        subject = "\t "
        command = self.make_tenant(
            subject_id=subject,
            command_type="  ",
            idempotency_key=" ",
            scope_context=ScopeContext(ScopeType.TENANT, tenant, scope),
        )
        dimensions, diagnostics = collect_command_idempotency_dimensions(command)
        self.assertEqual(diagnostics, [])
        self.assertIs(dimensions.tenant_id, tenant)
        self.assertIs(dimensions.subject_id, subject)
        self.assertIs(dimensions.command_type, command.command_type)
        self.assertIs(dimensions.idempotency_key, command.idempotency_key)

    def test_appels_frais_instances_distinctes_mutation_reelle_isolee(self):
        self.install_spy()
        command = self.make_tenant()
        premier, second = (
            collect_command_idempotency_dimensions(command),
            collect_command_idempotency_dimensions(command),
        )
        dimensions1, listes1 = premier
        dimensions2, listes2 = second
        self.assertIsNot(premier, second)
        self.assertIsNot(dimensions1, dimensions2)
        self.assertIsNot(listes1, listes2)
        self.assertEqual(len(self.spy_calls), 2)
        listes1.append("mutation locale")
        apres = collect_command_idempotency_dimensions(command)
        self.assertEqual(listes2, [])
        self.assertEqual(apres[1], [])
        self.assertIsNot(apres[1], listes1)
        self.assertEqual(len(apres[1]), 0)

    def test_scope_context_jamais_restitue(self):
        self.install_spy()
        command = self.make_tenant()
        dimensions, _ = collect_command_idempotency_dimensions(command)
        rendu = dataclasses.asdict(dimensions)
        self.assertEqual(
            set(rendu),
            {"tenant_id", "subject_id", "command_type", "idempotency_key"},
        )
        self.assertNotIsInstance(rendu["tenant_id"], ScopeContext)


class CollecteurRefusTests(Base):
    def test_objet_etranger_avec_probe_positif_reset_et_zero_lecture(self):
        self.install_spy()
        hostile = NoRead()
        with self.assertRaises(AssertionError):
            _ = hostile.command_id
        self.assertEqual(hostile.calls, ["command_id"])
        hostile.calls.clear()
        for etranger in (None, "cmd", 42, (), {}, hostile):
            with self.subTest(type=type(etranger).__name__):
                before = len(self.spy_calls)
                dimensions, diagnostics = collect_command_idempotency_dimensions(etranger)
                self.assertIsNone(dimensions)
                self.assertEqual(len(diagnostics), 1)
                self.assertEqual(diagnostics[0].element, "command_metadata.command")
                self.assertEqual(diagnostics[0].step, VALIDATE)
                self.assertEqual(diagnostics[0].constraint, diagnostics[0].message)
                self.assertIs(diagnostics, self.spy_results[-1])
                self.assertEqual(len(self.spy_calls), before + 1)
                self.assertIs(self.spy_calls[-1], etranger)
                self.assertIsInstance(diagnostics[0], Diagnostic)
        self.assertEqual(hostile.calls, [])

    def test_sous_classe_refusee_sans_lecture_locale(self):
        self.install_spy()
        compteur = CountingCommand(
            "cmd-1",
            ("corr",),
            ("cause",),
            ScopeContext(ScopeType.TENANT, "t1"),
            "type-1",
            "subject-1",
            "key-1",
        )
        CountingCommand.reads.clear()
        _ = compteur.command_id
        self.assertEqual(CountingCommand.reads, ["command_id"])
        CountingCommand.reads = []
        dimensions, diagnostics = collect_command_idempotency_dimensions(compteur)
        self.assertEqual(CountingCommand.reads, [])
        self.assertIsNone(dimensions)
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].element, "command_metadata.command")
        self.assertIs(diagnostics, self.spy_results[0])
        CountingCommand.reads = []

    def test_multi_refus_public_traverse_sans_alteration(self):
        self.install_spy()
        command = CommandMetadata(
            None,
            ["pas-tuple"],
            object(),
            NoRead(),
            "",
            object(),
            (),
        )
        dimensions, diagnostics = collect_command_idempotency_dimensions(command)
        self.assertIsNone(dimensions)
        self.assertEqual(len(diagnostics), 7)
        elements = [d.element for d in diagnostics]
        self.assertEqual(
            elements,
            sorted(
                [
                    "command_metadata.command_id",
                    "command_metadata.correlation_ids",
                    "command_metadata.causation_ids",
                    "command_metadata.scope_context",
                    "command_metadata.command_type",
                    "command_metadata.subject_id",
                    "command_metadata.idempotency_key",
                ]
            ),
        )
        self.assertIs(diagnostics, self.spy_results[0])
        second = collect_command_idempotency_dimensions(command)
        self.assertIsNot(second[1], diagnostics)
        self.assertEqual(
            [(d.element, d.constraint, d.message) for d in second[1]],
            [(d.element, d.constraint, d.message) for d in diagnostics],
        )
        self.assertIsNone(second[0])
        self.assertEqual(len(self.spy_calls), 2)


class CollecteurPropagationTests(Base):
    def test_erreurs_inattendues_propagees_meme_objet(self):
        exceptions = (
            ValueError("inattendue"),
            RuntimeError("inattendue"),
            KeyboardInterrupt(),
            SystemExit(4),
            Boom("base"),
        )
        command = self.make_tenant()
        for exception in exceptions:
            with self.subTest(exc=type(exception).__name__):
                def leve(_command, _exception=exception):
                    raise _exception

                self.install_spy(behavior=leve)
                with self.assertRaises(type(exception)) as captured:
                    collect_command_idempotency_dimensions(command)
                self.assertIs(captured.exception, exception)
                self.assertEqual(self.spy_calls, [command])


if __name__ == "__main__":
    unittest.main()
