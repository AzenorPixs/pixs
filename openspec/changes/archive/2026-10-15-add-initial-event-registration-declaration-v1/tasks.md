# Tâches — Déclaration passive d’enregistrement d’événement v1

- [x] 1. Publier le module neuf et ses deux exports, déclaration figée aux trois seuls champs, sans défaut ni conversion implicite.
- [x] 2. Implémenter le refus fermé des types/identifiants invalides et réutiliser exclusivement les deux validateurs de contrats existants, sans recopier leurs champs ni parser SemVer à nouveau.
- [x] 3. Vérifier diagnostics VALIDATE fixes sans valeur brute, liste fraîche triée/dédupliquée, absence de callback et propagation des exceptions inattendues.
- [x] 4. Publier les tests unitaires dédiés couvrant les comportements du profil et ses refus, y compris objets et sous-classes hostiles.
- [x] 5. Publier l’intégration en processus frais avec gardes éprouvées et portée déclarée, sans base de données ni secret.
- [x] 6. Exécuter séparément les trois compilations natives et vérifier les codes de sortie.
- [x] 7. Exécuter les deux modules de tests dédiés et les deux modules de régression EventContract existants, avec résultats natifs et aucun test ignoré présenté comme réussi.
- [x] 8. Vérifier UTF-8/LF, les trois nouveaux chemins seuls, empreintes des dépendances/canon préservées et delta MODIFIED mot pour mot des trois exigences/cinq scénarios validés.
- [x] 9. Exécuter OpenSpec strict ciblé sur le change et la spécification events avant code et après tests, avec codes natifs et résultats complets.

Les tâches restent décochées tant que leurs preuves ne sont pas observées. Après leurs preuves et les contrôles post-cochage, obtenir l’exclusion d’intégration, revalider l’état combiné (standard et relevé strict global avec avertissements historiques séparés), archiver une seule fois sous mandat distinct, produire et vérifier STATISTIQUES.md dans cette archive sous un autre mandat, puis publier, gate, désarmer/libérer et revenir à la sélection CISMP. Aucune archive ou statistique n’est revendiquée ici.

## Preuves de réalisation avant cochage

| Tâche | Preuves natives et contrôles |
|---|---|
| 1 | Module NFDOC exact écrit sous cismp3-1ac45ad1397448 ; trois champs figés/deux exports vérifiés par les tests publics. |
| 2–3 | 12 unitaires cismp3-27990c7dd1114f et intégration gardée cismp3-91b81fd543514a : types exacts, identité, diagnostics sans écho/effet et exceptions, exits 0. |
| 4 | Unitaire NFDOC exact écrit cismp3-ca596be7a55d41 ; compilation effectivement exécutée cismp3-02f3dc02f8fe43, exit 0 ; 12 tests réussis. |
| 5 | Intégration NFDOC exacte écrite cismp3-11dddd3c60e047 ; compilation cismp3-b7866723da6a4c et test frais gardé cismp3-91b81fd543514a, exits 0. |
| 6 | Trois compilations distinctes : module cismp3-98339734499d40, unitaire cismp3-02f3dc02f8fe43, intégration cismp3-b7866723da6a4c, exits natifs 0. Les demandes interrompues/refusées n'ont pas été exécutées. |
| 7 | 13 tests dédiés sous cismp3-27990c7dd1114f/cismp3-91b81fd543514a et 15 régressions EventContract sous cismp3-aa78b017b5c340 : 28 tests dans quatre modules, aucun échec ou test ignoré, exits 0. |
| 8 | posttests_scope_proof : trois sources NFDOC exactes UTF-8/LF, huit dépendances/canon inchangés, delta trois exigences/cinq scénarios mot pour mot, aucun autre fichier source modifié par les mandats de cette session. Git non inspecté. |
| 9 | Avant code : cismp3-e61fc0a8cdaf43/cismp3-b74d18e5065244 ; après tests : cismp3-cc1fc4a88df34b/cismp3-da622dba3b5148. Change et canon ciblés stricts, 1/1, issues vides et exits natifs 0. |

La validation post-cochage, l'archivage, la publication et le rapport restent à prouver par leurs mandats distincts ; ils ne sont pas revendiqués par ces coches.
