## 1. Établissement de la baseline

- [x] 1.1 Inventorier les capacités actives et vérifier que le référentiel contient 74 spécifications.
- [x] 1.2 Vérifier pour chaque exigence active la présence d'au moins un scénario et d'un mot-clé RFC 2119 conforme.
- [x] 1.3 Identifier la provenance disponible des capacités et consigner les 18 capacités sans change historique associé.

## 2. Consolidation documentaire

- [x] 2.1 Confirmer que les 74 chemins de capacités, leurs exigences et leurs scénarios restent inchangés en vérifiant l'absence de delta fonctionnel dans le change.
- [x] 2.2 Établir le référentiel actif comme baseline unique et vérifier que les changes archivés ne sont pas traités comme des spécifications actives.

## 3. Validation

- [x] 3.1 Exécuter `openspec validate consolidate-specifications --strict` et vérifier l'absence d'erreur.
- [x] 3.2 Exécuter `openspec validate --all --strict` et vérifier que toutes les spécifications actives restent valides.
- [x] 3.3 Vérifier que le change ne modifie aucun code, API, dépendance ou spécification active avant son éventuel archivage.
