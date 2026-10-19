# Tasks — add-initial-component-type-vocabulary-v1

## 1. Préparation et implémentation

- [x] 1.1 Vérifier component-model, absence de vocabulaire existant et valider le périmètre NFDOC.
- [x] 1.2 Créer les quatre artefacts OpenSpec cohérents, sans delta normatif artificiel.
- [x] 1.3 Ajouter ComponentType sans effet ni modification des consommateurs, façades ou manifests.
- [x] 1.4 Ajouter les tests unitaires et l’import isolé avec gardes d’effets.

## 2. Validation et clôture

- [x] 2.1 Compiler les trois nouveaux fichiers Python et exécuter les tests ciblés et régressions applicables.
- [x] 2.2 Exécuter la validation OpenSpec ciblée stricte, globale standard et stricte ; distinguer échecs et avertissements historiques.
- [x] 2.3 Vérifier contenu, UTF-8/LF, absence d’écriture hors périmètre et conformité aux cadrages.
- [x] 2.4 Présenter toutes les preuves à CGPT et obtenir son autorisation distincte pour l’archivage unique.

Le rapport STATISTIQUES.md est exigé après archivage, sous mandat distinct, avant gate et livraison. Aucun Git autorisé.

## Preuves examinées par CGPT

- Trois fichiers Python compilés : code 0.
- Tests ciblés et régressions manifest/vocabulaires : 19 tests réussis.
- OpenSpec ciblé strict : code 0.
- OpenSpec global standard : 187/187, code 0.
- OpenSpec global strict : code 1, 185/187 ; quatre avertissements de longueur préexistants (bulk-operations exigences 6, 10, 13 ; identity-assurance exigence 4), aucune ERROR. Aucun canon hors périmètre corrigé.
- Sept fichiers créés relus à l’identique des contenus approuvés ; cadrages, canon component-model, façade, models.py et state.py inchangés par empreintes.
- Archivage unique autorisé explicitement par CGPT après examen de ces preuves ; rapport STATISTIQUES.md obligatoire après archive sous mandat distinct.
- PostgreSQL, frontend et Git : sans objet ou non autorisés pour ce vocabulaire passif. Le cycle P0 global reste incomplet.
