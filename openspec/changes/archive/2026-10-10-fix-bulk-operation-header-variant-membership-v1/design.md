# Conception — garde de membre canonique Header

La validation conserve d'abord le contrôle de type exact. L'appartenance est
ensuite vérifiée uniquement par identité avec les membres du vocabulaire
BulkOperationVariant. Aucune égalité, conversion, représentation ou lecture
d'attribut d'un objet étranger n'est utilisée.

Le test existant de refus reçoit object.__new__(BulkOperationVariant), dont
le type est exact mais qui n'est ni IMPORT ni EXPORT. Il attend le diagnostic
statique bulk_operation_header.bulk_type déjà défini. Les tests existants
préservent l'acceptation des deux membres, les hooks hostiles, l'immutabilité,
les diagnostics et la pureté en processus frais.

Le delta MODIFIED reproduit à l'identique l'exigence canonique existante
Référence et variante du profil BulkOperationHeader v1. Il ne ferme aucune
nouvelle décision normative. L'archive utilisera --skip-specs après preuve.

Validation : reproduction bornée de la lacune sans écriture, contrôle du delta
et OpenSpec avant code, deux compilations séparées, 11 tests Header et
54 régressions (dont les 11 tests Status), OpenSpec après code, sources exactes,
UTF-8/LF, fichiers existants préservés. Les tâches ne seront cochées qu'après
acceptation CGPT. Archivage et STATISTIQUES.md sont des mandats distincts.
