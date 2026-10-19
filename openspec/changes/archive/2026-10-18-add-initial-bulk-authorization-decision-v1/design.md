# Conception — add-initial-bulk-authorization-decision-v1

## Référence normative

Le canon bulk-operations (B03, AuthorityAssessmentV1) fixe ALLOW, DENY et UNAVAILABLE. Aucune nouvelle exigence ni modification canonique n’est nécessaire.

## Représentation

Un module backend autonome expose uniquement BulkAuthorizationDecision via __all__. Il importe Enum de la bibliothèque standard et définit ALLOW = "ALLOW", DENY = "DENY", UNAVAILABLE = "UNAVAILABLE" dans cet ordre. Aucun mixin str, alias, défaut, ordre métier, transition ou méthode ajoutée.

## Compatibilité

Les chaînes restent des chaînes dans AuthorityAssessmentV1 et ses validateurs ; aucun consommateur existant ne migre vers Enum. Un membre Enum ne devient pas une chaîne exacte et doit rester refusé par validate_authority_assessment_values. Les décisions GovernanceResolutionV1, dont RESOLVED, restent distinctes. Aucun __init__.py existant modifié.

## Vérification

Tests unitaires du contrat fermé et des valeurs invalides ; régression du validateur existant ; import isolé avec gardes d’effets. Compiler chacun des trois fichiers et exécuter les tests ciblés avec les régressions des contrats Bulk. Validation OpenSpec ciblée stricte, globale standard et globale stricte avec résultats réels et avertissements historiques distingués. Vérifier UTF-8/LF, contenus et empreintes des fichiers existants concernés.

## Limites et retour

Ce vocabulaire ne décide ni ne résout une autorité et ne prouve aucun accès. Aucun runtime, I/O, provider, contexte, stockage, PostgreSQL, frontend ou dépendance ajouté. Trois nouveaux fichiers indépendants, aucune migration. Aucun changement Git autorisé. Archivage sous mandat distinct après examen des preuves ; statistiques obligatoires après archive.
