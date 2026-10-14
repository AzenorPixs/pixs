## 1. Préparation

- [x] 1.1 Vérifier les quatre artefacts UTF-8/LF, le delta identique au canon et les validations OpenSpec applicables.

## 2. Implémentation

- [x] 2.1 Ajouter le module interne pur conforme au profil canonique.
- [x] 2.2 Ajouter les tests unitaires du contrat et des valeurs interdites.
- [x] 2.3 Ajouter l'intégration en processus frais avec gardes vérifiés positivement.

## 3. Validation finale

- [x] 3.1 Compiler les trois fichiers Python avec l'interpréteur retenu.
- [x] 3.2 Réussir les tests unitaires, l'intégration et les régressions audit/diagnostics/façades/pureté.
- [x] 3.3 Vérifier la conformité finale OpenSpec, UTF-8/LF, les seuls fichiers attendus et l'absence d'effets.

Archivage et STATISTIQUES.md : mandats distincts après les sept preuves ; aucune tâche cochée avant sa preuve.

## Preuves de clôture des tâches

- Trois fichiers Python compilés séparément, codes natifs 0.
- Tests : 22 unitaires, 1 intégration fraîche gardée et 56 régressions, soit 79 réussis ; aucun échec, erreur ou skip.
- Intégration : gardes positivement vérifiés puis compteurs zéro ; stdout marqueur exact, stderr vide, sous-processus 0, probe absent et temporaire nettoyé.
- Change strict final : 1/1, code natif 0, aucune issue. Global final : 77/77, code natif 0 ; 21 WARNING de longueur seulement, exclus par instruction développeur.
- Canon audit validé en RSMP : non strict 1/1 et code 0 ; strict code 1 pour le seul WARNING de longueur, jamais présenté comme réussite stricte. Delta MODIFIED identique au canon approuvé.
- Sources UTF-8/LF exactes, empreintes préexistantes ciblées inchangées, façade publique/configuration/dépendances préservées.
- Incident : tentative supplémentaire true refusée avant exécution ; session isolée, absence d'effet prouvée, nouvelle session READY et CAB test inédit /usr/bin/true exit 0. Résultats réussis non rejoués.
- Archivage et rapport statistique restent des mandats distincts après cette clôture des tâches.
