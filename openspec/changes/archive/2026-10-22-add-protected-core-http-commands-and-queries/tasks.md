# Tâches — C06

La réalisation est autorisée par CISMP5 et la conception validée par CGPT.
Les coches ci-dessous sont adossées aux preuves natives, sans remplacer le
gate terminal. Archivage, publication et rapport post-archive sont encore
une séquence distincte obligatoire avant toute déclaration TERMINÉ.

## 1. Revue de conception

- [x] 1.1 Revoir requirements.md et le profil C00, puis recouper le canon courant : empreintes historiques distinguées de la relecture du 22 octobre ; aucune règle canonique modifiée.
- [x] 1.2 Lever les barrières de conception avant code et valider les compléments nécessaires : sérialiseur/curseur/idempotence, Auth contextuelle sans réétiquetage, horloge réelle C03, réutilisation immuable des permissions C04, fichiers et limites documentés.

## 2. Réalisation

- [x] 2.1 Déclarer routes publiques/protégées et schémas réellement exposés : 156 opérations, OpenAPI 3.1.0 / contrat 1.0.0, index et documents bornés, garde structurelle exécutée avant construction des fabriques.
- [x] 2.2 Relier les Commands/Queries propriétaires, C03/C04/C05 réels, contexte canonique et keyset SQL après filtrage/gouvernance ; aucune promotion de contexte par token ou header.
- [x] 2.3 Relier idempotence durable et migration additive 0003, résultat initial complet, conflit/rollback/réconciliation sans second effet, erreurs stables et localisation français/anglais.
- [x] 2.4 Tester sans frontend : rejeu, divergence, refus privés/inter-tenant, ordonnance SQL, cookie/CSRF/Bearer, activité C03 et renouvellement, tenant/scope/Root, ACL et concordance contrat-serveur.

## 3. Preuves et garde de clôture

- [x] 3.1 Exécuter les vérifications applicables : 166 unitaires OK, 192 cas PostgreSQL sur neuf recettes OK, cleanup/conns_closed vrais, 33 fichiers Python compilés ; strict C06 valide avant alignement documentaire. Les contrôles stricts et documentaires finaux restent à consigner avant archive.
- [x] 3.2 Vérifier isolation et refus ; bilans masqués sans valeurs Auth brutes ; identifier les doubles C09/C10, le setup C08 et les non-applicables Jobs/Bulk/Frontend/TLS réseau/P0 complet dans requirements.md et design.md.
- [x] 3.3 Examiner le périmètre et les effets exacts par mandats natifs et SHA, préserver les changements préexistants ; aucune opération Git ni changement de configuration, aucun frontend ni déploiement.
- [x] 3.4 Vérifier les autorisations avant les seules opérations engagées et cadrer la séquence terminale CISMP5 : archive C06, publication CAB et rapport distinct STATISTIQUES.md sont autorisés sous leurs mandats ; Git, déploiement et prochain change restent hors périmètre.

## Séquence terminale post-archive — obligation distincte

Le rapport STATISTIQUES.md n'est pas déclaré produit par ces coches.
Après preuve d'archive, sa création et sa vérification UTF-8/LF, six sections,
totaux et quotas restent obligatoires, puis publication/gate individuel,
désarmement et libération. Le checkpoint et le rapport réel font foi de
cette clôture ; aucune archive seule ne vaut TERMINÉ.

## Preuves de réalisation

- Neuf recettes PG, 192 cas : call_01a1612c0a267426b2a7213b01d628b0.
- Unitaires finaux, 166 tests : call_01a1612dc5ca722cbd04fc7b39425507.
- py_compile, 33 fichiers : call_01a1612f3f457159936f1edc70d3509c.
- Strict C06 avant alignement : call_01a161311fd4740682a8e9bf65c6c538.
- Détails, versions et limites : design.md et requirements.md ; sorties natives dans le checkpoint scopé du RUN.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Preuves et garde de clôture » ; « Preuves de réalisation ».

### C06-SL01 — Revoir requirements.md et le profil C00, puis recouper le canon courant : empreintes historiques distinguées de la relecture du 22 octobre ; aucune règle canonique modifiée.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Revue de conception », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C06-SL02 — Lever les barrières de conception avant code et valider les compléments nécessaires : sérialiseur/curseur/idempotence, Auth contextuelle sans réétiquetage, horloge réelle C03, réutilisation immuable des permissions C04, fichiers et limites documentés.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Revue de conception », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C06-SL03 — Déclarer routes publiques/protégées et schémas réellement exposés : 156 opérations, OpenAPI 3.1.0 / contrat 1.0.0, index et documents bornés, garde structurelle exécutée avant construction des fabriques.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Réalisation », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C06-SL04 — Relier les Commands/Queries propriétaires, C03/C04/C05 réels, contexte canonique et keyset SQL après filtrage/gouvernance ; aucune promotion de contexte par token ou header.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Réalisation », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C06-SL05 — Relier idempotence durable et migration additive 0003, résultat initial complet, conflit/rollback/réconciliation sans second effet, erreurs stables et localisation français/anglais.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Réalisation », ligne 17 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C06-SL06 — Tester sans frontend : rejeu, divergence, refus privés/inter-tenant, ordonnance SQL, cookie/CSRF/Bearer, activité C03 et renouvellement, tenant/scope/Root, ACL et concordance contrat-serveur.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Réalisation », ligne 18 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C06-SL07 — Exécuter les vérifications applicables : 166 unitaires OK, 192 cas PostgreSQL sur neuf recettes OK, cleanup/conns_closed vrais, 33 fichiers Python compilés ; strict C06 valide avant alignement documentaire. Les contrôles stricts et documentaires finaux restent à consigner avant archive.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Preuves et garde de clôture », ligne 22 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C06-SL08 — Vérifier isolation et refus ; bilans masqués sans valeurs Auth brutes ; identifier les doubles C09/C10, le setup C08 et les non-applicables Jobs/Bulk/Frontend/TLS réseau/P0 complet dans requirements.md et design.md.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Preuves et garde de clôture », ligne 23 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C06-SL09 — Examiner le périmètre et les effets exacts par mandats natifs et SHA, préserver les changements préexistants ; aucune opération Git ni changement de configuration, aucun frontend ni déploiement.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Preuves et garde de clôture », ligne 24 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C06-SL10 — Vérifier les autorisations avant les seules opérations engagées et cadrer la séquence terminale CISMP5 : archive C06, publication CAB et rapport distinct STATISTIQUES.md sont autorisés sous leurs mandats ; Git, déploiement et prochain change restent hors périmètre.

- Ancien repère et tâche rattachée : tâche 3.4 ; section « 3. Preuves et garde de clôture », ligne 25 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
