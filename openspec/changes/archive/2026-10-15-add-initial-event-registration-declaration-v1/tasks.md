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

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Preuves de réalisation avant cochage ».

### C79-SL01 — Publier le module neuf et ses deux exports, déclaration figée aux trois seuls champs, sans défaut ni conversion implicite.

- Ancien repère et tâche rattachée : tâche 1 ; section « Tâches — Déclaration passive d’enregistrement d’événement v1 », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Preuves de réalisation avant cochage », ligne 19 du texte conservé.
  - Preuves natives et contrôles : Module NFDOC exact écrit sous cismp3-1ac45ad1397448 ; trois champs figés/deux exports vérifiés par les tests publics.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C79-SL02 — Implémenter le refus fermé des types/identifiants invalides et réutiliser exclusivement les deux validateurs de contrats existants, sans recopier leurs champs ni parser SemVer à nouveau.

- Ancien repère et tâche rattachée : tâche 2 ; section « Tâches — Déclaration passive d’enregistrement d’événement v1 », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C79-SL03 — Vérifier diagnostics VALIDATE fixes sans valeur brute, liste fraîche triée/dédupliquée, absence de callback et propagation des exceptions inattendues.

- Ancien repère et tâche rattachée : tâche 3 ; section « Tâches — Déclaration passive d’enregistrement d’événement v1 », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C79-SL04 — Publier les tests unitaires dédiés couvrant les comportements du profil et ses refus, y compris objets et sous-classes hostiles.

- Ancien repère et tâche rattachée : tâche 4 ; section « Tâches — Déclaration passive d’enregistrement d’événement v1 », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Preuves de réalisation avant cochage », ligne 21 du texte conservé.
  - Preuves natives et contrôles : Unitaire NFDOC exact écrit cismp3-ca596be7a55d41 ; compilation effectivement exécutée cismp3-02f3dc02f8fe43, exit 0 ; 12 tests réussis.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C79-SL05 — Publier l’intégration en processus frais avec gardes éprouvées et portée déclarée, sans base de données ni secret.

- Ancien repère et tâche rattachée : tâche 5 ; section « Tâches — Déclaration passive d’enregistrement d’événement v1 », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Preuves de réalisation avant cochage », ligne 22 du texte conservé.
  - Preuves natives et contrôles : Intégration NFDOC exacte écrite cismp3-11dddd3c60e047 ; compilation cismp3-b7866723da6a4c et test frais gardé cismp3-91b81fd543514a, exits 0.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C79-SL06 — Exécuter séparément les trois compilations natives et vérifier les codes de sortie.

- Ancien repère et tâche rattachée : tâche 6 ; section « Tâches — Déclaration passive d’enregistrement d’événement v1 », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Preuves de réalisation avant cochage », ligne 23 du texte conservé.
  - Preuves natives et contrôles : Trois compilations distinctes : module cismp3-98339734499d40, unitaire cismp3-02f3dc02f8fe43, intégration cismp3-b7866723da6a4c, exits natifs 0. Les demandes interrompues/refusées n'ont pas été exécutées.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C79-SL07 — Exécuter les deux modules de tests dédiés et les deux modules de régression EventContract existants, avec résultats natifs et aucun test ignoré présenté comme réussi.

- Ancien repère et tâche rattachée : tâche 7 ; section « Tâches — Déclaration passive d’enregistrement d’événement v1 », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Preuves de réalisation avant cochage », ligne 24 du texte conservé.
  - Preuves natives et contrôles : 13 tests dédiés sous cismp3-27990c7dd1114f/cismp3-91b81fd543514a et 15 régressions EventContract sous cismp3-aa78b017b5c340 : 28 tests dans quatre modules, aucun échec ou test ignoré, exits 0.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C79-SL08 — Vérifier UTF-8/LF, les trois nouveaux chemins seuls, empreintes des dépendances/canon préservées et delta MODIFIED mot pour mot des trois exigences/cinq scénarios validés.

- Ancien repère et tâche rattachée : tâche 8 ; section « Tâches — Déclaration passive d’enregistrement d’événement v1 », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Preuves de réalisation avant cochage », ligne 25 du texte conservé.
  - Preuves natives et contrôles : posttests_scope_proof : trois sources NFDOC exactes UTF-8/LF, huit dépendances/canon inchangés, delta trois exigences/cinq scénarios mot pour mot, aucun autre fichier source modifié par les mandats de cette session. Git non inspecté.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C79-SL09 — Exécuter OpenSpec strict ciblé sur le change et la spécification events avant code et après tests, avec codes natifs et résultats complets.

- Ancien repère et tâche rattachée : tâche 9 ; section « Tâches — Déclaration passive d’enregistrement d’événement v1 », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Preuves de réalisation avant cochage », ligne 26 du texte conservé.
  - Preuves natives et contrôles : Avant code : cismp3-e61fc0a8cdaf43/cismp3-b74d18e5065244 ; après tests : cismp3-cc1fc4a88df34b/cismp3-da622dba3b5148. Change et canon ciblés stricts, 1/1, issues vides et exits natifs 0.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
