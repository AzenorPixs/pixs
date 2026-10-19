# Audit transversal P0 et révision de préparation

Relevé du 17 octobre 2026. Audit de conception sans implémentation : **17 parcours et interfaces** examinés, références des **717 exigences / 812 scénarios / 78 capacités** revérifiées. L’ancien rattachement de 351 exigences aux lots P0 et de 366 aux autres lots ne prouve ni applicabilité ni conformité. Les 623 exigences hors audit NE ne reçoivent pas ici un nouveau verdict fonctionnel ; les statuts L79/P285/ND353/NE0 restent inchangés.

## Changes supplémentaires validés

| Lot | Dossier | Responsabilité |
|---|---|---|
| N03 | [Confiance avant installation](../add-p0-artifact-trust-and-preinstallation-verification/proposal.md) | Vérificateurs, matériaux publics et contrôles précoces ; C19 conserve publication et support. |
| N04 | [Entrée web P0](../define-p0-web-serving-and-security-boundary/proposal.md) | Assemblage HTTP du bundle et des routes, frontière publique/privée et garanties HTTP ; 3 exigences ADDED proposées. |
| N05 | [Réadmission après restauration](../add-p0-post-restore-reconciliation-and-readmission/proposal.md) | Réconciliation des faits de sécurité/gouvernance et effets avant réadmission ; 1 exigence ADDED proposée. |
| N06 | [Kit minimal de conformité](../add-minimal-p0-contract-conformance-kit/proposal.md) | Suites/preuves et exemple nécessaires au P0, distincts de C17 campagne finale et d’O22 complet. |

Le développeur a validé les trois dossiers N03/N04/N05 avec rédaction des deltas N04/N05, puis N06 dédié. Les 40 tâches ajoutées restent non cochées. Aucun delta synchronisé et aucune implémentation. Les autres écarts complètent les conceptions propriétaires : secrets/marqueurs, administrateur ordinaire, audit du panneau, concurrence UI, transactions/outbox, maintenance, effacement et restauration, migrations, PZT/DNS, langues/accessibilité et options.

## Plan et compteurs

Le [plan global](plan-global-preparation.md) compte désormais **106 changes ouverts, dont 25 P0** ; **135 archivés / 241 au total = 56,02 %**. Les **1 052 tâches de réalisation sont non cochées**. Le graphe ferme est acyclique et les conditions d’activation sont séparées des dépendances de préparation ; C07 ne dépend pas fermement de C17/N06 pour produire son hôte intermédiaire, sans annoncer de readiness P0 prématurée.

Le canon reste **78 capacités, 717 exigences, 812 scénarios**. Les deltas C00/N02/N04/N05 proposent 13 exigences ajoutées, 2 existantes modifiées et 25 scénarios supplémentaires nets : projection théorique **78/730/837** si tous sont adoptés sans modification. README et PROJECT portent le suivi actualisé ; les autres cadrages vérifiés ne contiennent aucun total global à corriger et leurs relevés historiques ne sont pas régénérés.

## Contrôles et limites

95 unités existantes ont réussi sur les primitives ciblées. Les **106 changes** passent le strict natif ; le strict global reste **exit 1**, avec quatre avertissements de longueur préexistants dans bulk-operations et identity-assurance. Aucune qualification d’installation, de restauration ou de service distribué n’en est déduite. Le code et les 78 spécifications canoniques restent inchangés.

[Audit structuré et références](audit-transversal-p0.json), [contrôles conservés](validation-audit-transversal-p0.json), [rapport local et sorties](../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Les choix de technologies, schémas détaillés, paramètres et garanties encore ouverts restent à valider avant réalisation.
