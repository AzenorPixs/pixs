# Tâches — vocabulaire initial EventEnvelopeKind

- [x] 1. Vérifier le canon, l’absence de représentation équivalente et les frontières du sous-lot.
- [x] 2. Ajouter EventEnvelopeKind et ses deux valeurs canoniques sans branchement runtime.
- [x] 3. Prouver les recherches exactes, la préservation des gardes existantes et l’import en processus frais sous gardes éprouvées.
- [x] 4. Exécuter syntaxe, tests et régressions pertinents, UTF-8/LF et validations OpenSpec ; conserver leurs résultats réels.
- [x] 5. Vérifier le périmètre et réunir les preuves autorisant l’archivage de ce seul change par CGPT.

L’archivage, la publication et STATISTIQUES.md restent des mandats distincts. Aucune tâche ne peut être cochée avant ses preuves.

## Preuves

- Canon events B11/EventEnvelopeV1 relu ; absence d’Enum équivalent vérifiée.
- Sept fichiers nouveaux relus UTF-8/LF, contenus exacts vérifiés ; 17 références/cadrages/validateurs existants inchangés par empreinte.
- Trois fichiers Python compilés, code 0 ; 47 tests réussis (5 nouveaux et 42 régressions), code 0.
- Import frais -I -B avec gardes éprouvées et préservation de la validation str exacte prouvés par ces tests.
- OpenSpec ciblé strict : valide, code 0. Global standard : 187/187, code 0.
- Global strict : 185/187, code 1 ; exactement quatre WARNING de longueur préexistants dans bulk-operations[6,10,13] et identity-assurance[4], zéro ERROR. Aucun canon hors périmètre corrigé.
- Deux prévols CAB complets exacts et permissions once corrélées prouvés ; une demande de tests mal scopée annulée avant effet et une demande globale sur base périmée refusée avant effet, puis reprises avec identités neuves.
- Archivage, publication et rapport statistique non revendiqués par ces coches ; opérations distinctes à suivre.
