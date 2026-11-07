# Tâches — C05

Réalisation propriétaire autorisée par `1CISMP2`. Les preuves exécutées figurent dans `VALIDATION.md`. Les cases ci-dessous couvrent le travail source C05 et sa revue ; l’archivage, les statistiques postarchive et le gate sont des conditions de clôture du RUN suivies séparément dans son checkpoint.

## 1. Revue de conception

- [x] 1.1 Revoir les exigences/scénarios de requirements.md et le profil C00 ; recouper les sources et empreintes canoniques avant réalisation.
- [x] 1.2 Lever les barrières techniques de stockage, transactions, droits et cycle de vie ; présenter/valider les fichiers et contrats par délégation ISMP sans nouveau delta normatif.

## 2. Réalisation

- [x] 2.1 Définir le propriétaire C05 et la participation commune D13 ; éprouver D14 avec SyntheticAuthOwner de test, sans revendiquer le runtime C03.
- [x] 2.2 Implémenter écritures durables append-only, consultation filtrée, minimisation, anonymisation et purge contrôlées, tombstones et reprise C01 scellée.
- [x] 2.3 Raccorder le port d’audit aux services Core ordinaires et les sources minimales à la composition C4 ; respecter les waivers explicites sans audit fictif.
- [x] 2.4 Éprouver commit/rollback, réponse perdue, issue UNKNOWN conservatrice, échec d’audit fermé, D13/D14 synthétiques, isolation tenant, gouvernance, legal hold, rétention, collisions et acquittements distincts des preuves.

## 3. Preuves et préparation de clôture

- [x] 3.1 Exécuter syntaxe, suites applicables, recette PostgreSQL réelle et contrôle de cohérence des migrations ; conserver les preuves natives.
- [x] 3.2 Vérifier les scénarios applicables, les nettoyages, les secrets maintenus dans le seul processus PG et les neuf références canoniques ; expliciter les garanties non qualifiées.
- [x] 3.3 Examiner les fichiers et le périmètre sans Git ; préserver le travail des autres RUN et actualiser les documents devenus inexacts, sans annoncer une composition P0 livrée.
- [x] 3.4 Préparer l’archivage explicitement autorisé et le mandat distinct du seul STATISTIQUES.md postarchive ; maintenir la clôture conditionnée à ce rapport, son contrôle UTF-8/LF/six sections et au gate réel.

L’archivage et les statistiques ne sont pas déclarés accomplis par ces cases. Leur résultat terminal est donné dans le rapport réel de l’archive et le checkpoint `output/cismp/cismp2-pixs-968e38f3e27b4bbf/state.json`. Si le rapport échoue, seul le rapport est repris, sans réarchiver. L’arrêt concerne ce RUN après livraison ; les services partagés et les autres RUN restent disponibles.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Preuves et préparation de clôture ».

### C05-SL01 — Revoir les exigences/scénarios de requirements.md et le profil C00 ; recouper les sources et empreintes canoniques avant réalisation.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Revue de conception », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C05-SL02 — Lever les barrières techniques de stockage, transactions, droits et cycle de vie ; présenter/valider les fichiers et contrats par délégation ISMP sans nouveau delta normatif.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Revue de conception », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C05-SL03 — Définir le propriétaire C05 et la participation commune D13 ; éprouver D14 avec SyntheticAuthOwner de test, sans revendiquer le runtime C03.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Réalisation », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C05-SL04 — Implémenter écritures durables append-only, consultation filtrée, minimisation, anonymisation et purge contrôlées, tombstones et reprise C01 scellée.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Réalisation », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C05-SL05 — Raccorder le port d’audit aux services Core ordinaires et les sources minimales à la composition C4 ; respecter les waivers explicites sans audit fictif.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Réalisation », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C05-SL06 — Éprouver commit/rollback, réponse perdue, issue UNKNOWN conservatrice, échec d’audit fermé, D13/D14 synthétiques, isolation tenant, gouvernance, legal hold, rétention, collisions et acquittements distincts des preuves.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Réalisation », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C05-SL07 — Exécuter syntaxe, suites applicables, recette PostgreSQL réelle et contrôle de cohérence des migrations ; conserver les preuves natives.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Preuves et préparation de clôture », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C05-SL08 — Vérifier les scénarios applicables, les nettoyages, les secrets maintenus dans le seul processus PG et les neuf références canoniques ; expliciter les garanties non qualifiées.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Preuves et préparation de clôture », ligne 20 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C05-SL09 — Examiner les fichiers et le périmètre sans Git ; préserver le travail des autres RUN et actualiser les documents devenus inexacts, sans annoncer une composition P0 livrée.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Preuves et préparation de clôture », ligne 21 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C05-SL10 — Préparer l’archivage explicitement autorisé et le mandat distinct du seul STATISTIQUES.md postarchive ; maintenir la clôture conditionnée à ce rapport, son contrôle UTF-8/LF/six sections et au gate réel.

- Ancien repère et tâche rattachée : tâche 3.4 ; section « 3. Preuves et préparation de clôture », ligne 22 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
