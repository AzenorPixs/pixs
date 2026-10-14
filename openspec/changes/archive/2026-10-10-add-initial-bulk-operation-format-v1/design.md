## Context

Le profil interne BulkOperationFormat v1 lie seulement une référence opaque au vocabulaire BulkReferenceFormat existant. Les contrats généraux bulk, les formats étendus et les cadrages PA/PZT restent applicables, sans comportement déduit de cette représentation.

## Goals / Non-Goals

Goals : deux champs obligatoires sans défaut, dataclass gelée, conservation exacte de la référence et du membre canonique, validation pure et diagnostics statiques.

Non-Goals : parsing, lecture/écriture de fichier métier, conversion ou choix de format, activation/résolution d'adaptateur, validité de contenu, encodage, mapping, compatibilité, autorisation, persistance ou import/export effectif. Aucun travail PA/PZT.

## Decisions

1. Module bulk_operation_format.py avec BulkOperationFormat et validate_bulk_operation_format; aucun registre ni export de façade modifié.
2. Refuser type(candidate) différent du profil exact avant ses attributs. Une sentinelle interne explicite représente un attribut absent, sans valeur de repli des données. Vérifier le type exact str avant vérité de operation_id et conserver tout contenu non vide sans normalisation.
3. Vérifier le type exact BulkReferenceFormat puis l'identité avec l'un de ses deux membres canoniques; une instance forgée du bon type reste refusée, sans égalité ou conversion étrangère.
4. Construire des Diagnostic VALIDATE uniquement à partir de champs et messages statiques; trier/dédupliquer et rendre une liste indépendante.
5. Neuf tests unitaires comportementaux : deux formats, références opaques, champs obligatoires et immutabilité, étrangers/dérivés, types hostiles, chaînes/enums étrangers/forgés, champs absents, diagnostics et absence de mutation.
6. Un test en processus Python frais avec environnement minimal, timeout et gardes à contrôles positifs sur fichiers, réseau, processus, environnement, base de données et import concret pixs.core; garder explicites les limites des surfaces surveillées.

## Risks / Trade-offs

Un format structurellement accepté ne prouve aucun contenu de fichier ni droit. Aucun adaptateur n'est activé. La bibliothèque standard et les diagnostics existants suffisent, avec compatibilité Python >=3.12 conservée.

## Migration Plan

Aucune migration, configuration, dépendance ou activation runtime. Delta identique au canon, archive --skip-specs seulement après preuves et décision distincte. STATISTIQUES.md ensuite sous mandat propre; les travaux PA/PZT restent intacts.
