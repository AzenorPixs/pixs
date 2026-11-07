# Tasks

## 1. Bootstrap du paquet Python et structure du noyau

- [x] 1.1 Créer `pyproject.toml` conforme PEP 621 déclarant uniquement la stdlib (aucune dépendance externe ajoutée) — vérification : le fichier existe à la racine, est parseable par tomllib, et `python -m compileall src/` sort code 0
- [x] 1.2 Créer l'arborescence `src/pixs/kernel/` avec sous-paquets `manifest`, `registry`, `resolver`, `lifecycle`, `config`, `diagnostics` — vérification : l'arborescence attendue est listée et l'import `pixs.kernel` réussit sans erreur
- [x] 1.3 Mettre en place la découverte de tests stdlib `unittest` avec répertoires séparés `tests/unit` et `tests/integration` — vérification : `python -m unittest discover` s'exécute sans erreur de collection sur les deux niveaux

## 2. Modèles déclaratifs et validation des manifests

- [x] 2.1 Implémenter le modèle déclaratif de manifest (identifiant, type parmi les six, version SemVer, dépendances obligatoires/optionnelles, capacités fournies/requises, contrats, `schema_version`) — preuve à renouveler au schéma 1 : capacités et contrats fournis en tables versionnées (voir 6.5) — vérification : tests unitaires de construction depuis une fixture TOML valide et de rejet champ par champ avec diagnostic nommant le champ manquant
- [x] 2.2 Implémenter le parsing `component.toml` via `tomllib` et le contrôle de `schema_version` — vérification : test unitaire « version de schéma inconnue » passe, le composant reste non validé avec un diagnostic indiquant la version concernée
- [x] 2.3 Implémenter le refus des secrets et logiques exécutables dans les manifests — vérification : tests unitaires sur fixtures « secret embarqué » et « expression à évaluer » passent, composition refusée avec diagnostic explicite
- [x] 2.4 Implémenter les règles d'identifiants namespacés (`pixs.*` réservés) et la détection de collisions — vérification : tests unitaires de rejet d'un composant externe usurpant `pixs.*` et de deux composants au même identifiant bloquant l'activation avant chargement

## 3. Pipeline de composition, graphe déterministe et diagnostics

- [x] 3.1 Implémenter les étapes `discover → validate → resolve → activate` en pipeline ordonné et idempotent — vérification : test d'intégration exécutant deux fois le pipeline sur la même fixture, avec graphe, ordre et diagnostics identiques et absence d'effet dupliqué
- [x] 3.2 Implémenter le tri topologique à départage déterministe par identifiant canonique et la détection de cycles — vérification : tests unitaires A→B→C (ordre stable identique entre exécutions) et A→B→A (composition invalidée, cycle identifié dans le diagnostic)
- [x] 3.3 Implémenter la résolution de fournisseurs : fournisseur configuré, sinon candidat compatible unique, sinon composition invalide — preuve à renouveler sur versions déclarées : configuré compatible sinon refus, évaluation SemVer des capacités (voir 6.6) — vérification : test unitaire du scénario deux fournisseurs sans sélection, refus avec diagnostic d'ambiguïté et absence de dépendance à l'ordre de découverte
- [x] 3.4 Structurer les diagnostics de composition typés (élément, contrainte, étape) — vérification : tests unitaires asserting pour chaque classe d'échec que le message identifie l'élément et la contrainte violés, sans valeur sensible

## 4. Registres génériques, configuration par références et règle data-driven

- [x] 4.1 Implémenter les sept registres génériques (modules, dépendances, cycle de vie, services, événements, configuration, extensions) alimentés uniquement par des modèles validés — vérification : tests unitaires démontrant le refus d'enregistrement d'une contribution non déclarée et l'idempotence d'un double enregistrement
- [x] 4.2 Implémenter la résolution de configuration par priorité déclarée (schéma, défauts, statique, runtime, références de secrets) — vérification : tests unitaires de surcharge d'une même clé avec valeur gagnante reproductible ; le noyau ne résout aucune valeur de secret, test de contrôle de la face publique
- [x] 4.3 Implémenter le jeu de composants requis porté en données de composition validées — preuve à renouveler avec composants requis contraints (`"id [comparateurs]"`, voir 6.6) — vérification : test d'intégration déclarant `pixs.core` comme requis en données seulement ; l'absence invalide l'activation avant chargement avec diagnostic, et un test vérifie l'absence de tout nom de concept métier codé en dur dans le code du noyau

## 5. Cycle de vie mécanique et interfaces publiques

- [x] 5.1 Implémenter les états installed, enabled, configured, ready, healthy et les opérations mécaniques `discover`, `validate`, `install`, `enable`, `configure`, `start`, `disable` — vérification : tests unitaires d'états non confondus (installé-désactivé ≠ prêt) et de refus explicite de `migrate`, `upgrade`, `uninstall`, `purge` hors périmètre
- [x] 5.2 Implémenter les hooks de cycle de vie ordonnés par le graphe résolu — vérification : test d'intégration comparant deux exécutions complètes, ordre des hooks et du chargement identiques
- [x] 5.3 Exposer l'interface publique du noyau par les façades de paquet et borner l'export — vérification : un test d'intégration importe exclusivement l'API déclarée et asserte que les modules privés ne figurent pas dans les façades exportées

## 6. Tests et contrôles finaux

- [x] 6.1 Compléter la suite unitaire couvrant chaque scénario normé du périmètre (kernel, component-model, dependencies, capabilities, configuration, compatibility pour la partie déclarative) — preuve à renouveler aux exigences RSMP versions/preuves (voir 6.5–6.7) — vérification : `python -m unittest discover -s tests/unit` passe et la correspondance scénario-test est listée dans le rapport de session
- [x] 6.2 Compléter la suite d'intégration sur compositions synthétiques (résolution complète, ambiguïtés, cycles, composant requis absent, deux ordres de découverte) — vérification : `python -m unittest discover -s tests/integration` passe avec preuves reproductibles
- [x] 6.3 Vérifier l'absence de secret et de donnée de production dans fixtures, rapports et diagnostics — périmètre : scan exclusivement des artefacts synthétiques de tests et diagnostics et des rapports de test autorisés ; AUCUN parcours des sources exclues par AGENTS.md ni lecture de secret ; les fixtures sentinelles (placeholders volontaires prouvant la détection) sont évaluées séparément du contrôle des sorties moteur — vérification : test automatisé de motifs sensibles sur tout artefact de test du périmètre, suite passant sans fuite détectée
- [x] 6.4 Exécuter les contrôles finaux du change : `python -m compileall src/`, suite complète `unittest`, `bash -n` et `shellcheck` sur tout script auxiliaire éventuellement produit — vérification : chaque commande sort code 0 et la sortie est consignée dans le rapport de session
- [x] 6.5 Schéma capacités/contrats versionnés et adaptation des fixtures : manifests `[provides].capabilities` et `[implements].contracts` en tables `{id, version, …}` schéma 1, refus des anciennes chaînes sans version avec diagnostic, fixtures historiques adaptées, version du composant jamais proxy — vérification : tests unitaires de validation (construction valide, rejet sans version nommant champ et entrée) et suite existante adaptée passant
- [x] 6.6 Contraintes composants/capacités/contrats/requis : six comparateurs (`== != >= <= > <`), conjonctions, préversions ordre SemVer standard, métadonnées de build ignorées en précédence, syntaxes malformées refusées, évaluation sur versions propres (jamais la version du composant pour une capacité ou un contrat), composants requis contraints, sélection configurée incompatible refusée — vérification : tests unitaires et d'intégration (contrainte insatisfaite, malformée, mismatch de version, déterminisme deux ordres) passant avec diagnostics nommant consommateur, cible, contrainte et version trouvée
- [x] 6.7 Preuves externes et portée P0 : `ConformityAttestation` en mémoire hors manifest (absence, mismatch de fournisseur/version/build, échec, malformée, ambiguïté refusés ; couverture complète PASS autorisant ; composition déterministe préservée), doubles de preuves clairement nommés limités aux fixtures, exposition P0 limitée aux dimensions connues sans prétention globale — vérification : tests d'intégration de chaque cas passant avec diagnostics non sensibles

Note : les 35 tests d'intégration validés avant RSMP restent acquis comme preuve de déterminisme et de refus fermé, mais ne constituent pas une preuve des nouveaux critères versions/preuves (6.5–6.7).

Hors périmètre (voir proposal.md — Impact) : primitives fonctionnelles de `pixs.core` (utilisateurs, groupes, appartenances, tenants, rôles, ACL, permissions), surface API HTTP, frontend TanStack et graphe frontend récursif, providers concrets, résolution effective de secrets, suites de conformité provider, opérations effectives `migrate`/`upgrade`/`uninstall`/`purge`, et composition de référence intégrale `reference-composition`.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 2. Modèles déclaratifs et validation des manifests » ; « 6. Tests et contrôles finaux ».

### C24-SL01 — Créer `pyproject.toml` conforme PEP 621 déclarant uniquement la stdlib (aucune dépendance externe ajoutée) — vérification : le fichier existe à la racine, est parseable par tomllib, et `python -m compileall src/` sort code 0

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Bootstrap du paquet Python et structure du noyau », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL02 — Créer l'arborescence `src/pixs/kernel/` avec sous-paquets `manifest`, `registry`, `resolver`, `lifecycle`, `config`, `diagnostics` — vérification : l'arborescence attendue est listée et l'import `pixs.kernel` réussit sans erreur

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Bootstrap du paquet Python et structure du noyau », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL03 — Mettre en place la découverte de tests stdlib `unittest` avec répertoires séparés `tests/unit` et `tests/integration` — vérification : `python -m unittest discover` s'exécute sans erreur de collection sur les deux niveaux

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Bootstrap du paquet Python et structure du noyau », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL04 — Implémenter le modèle déclaratif de manifest (identifiant, type parmi les six, version SemVer, dépendances obligatoires/optionnelles, capacités fournies/requises, contrats, `schema_version`) — preuve à renouveler au schéma 1 : capacités et contrats fournis en tables versionnées (voir 6.5) — vérification : tests unitaires de construction depuis une fixture TOML valide et de rejet champ par champ avec diagnostic nommant le champ manquant

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Modèles déclaratifs et validation des manifests », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL05 — Implémenter le parsing `component.toml` via `tomllib` et le contrôle de `schema_version` — vérification : test unitaire « version de schéma inconnue » passe, le composant reste non validé avec un diagnostic indiquant la version concernée

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Modèles déclaratifs et validation des manifests », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL06 — Implémenter le refus des secrets et logiques exécutables dans les manifests — vérification : tests unitaires sur fixtures « secret embarqué » et « expression à évaluer » passent, composition refusée avec diagnostic explicite

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Modèles déclaratifs et validation des manifests », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL07 — Implémenter les règles d'identifiants namespacés (`pixs.*` réservés) et la détection de collisions — vérification : tests unitaires de rejet d'un composant externe usurpant `pixs.*` et de deux composants au même identifiant bloquant l'activation avant chargement

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Modèles déclaratifs et validation des manifests », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL08 — Implémenter les étapes `discover → validate → resolve → activate` en pipeline ordonné et idempotent — vérification : test d'intégration exécutant deux fois le pipeline sur la même fixture, avec graphe, ordre et diagnostics identiques et absence d'effet dupliqué

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Pipeline de composition, graphe déterministe et diagnostics », ligne 18 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL09 — Implémenter le tri topologique à départage déterministe par identifiant canonique et la détection de cycles — vérification : tests unitaires A→B→C (ordre stable identique entre exécutions) et A→B→A (composition invalidée, cycle identifié dans le diagnostic)

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Pipeline de composition, graphe déterministe et diagnostics », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL10 — Implémenter la résolution de fournisseurs : fournisseur configuré, sinon candidat compatible unique, sinon composition invalide — preuve à renouveler sur versions déclarées : configuré compatible sinon refus, évaluation SemVer des capacités (voir 6.6) — vérification : test unitaire du scénario deux fournisseurs sans sélection, refus avec diagnostic d'ambiguïté et absence de dépendance à l'ordre de découverte

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Pipeline de composition, graphe déterministe et diagnostics », ligne 20 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL11 — Structurer les diagnostics de composition typés (élément, contrainte, étape) — vérification : tests unitaires asserting pour chaque classe d'échec que le message identifie l'élément et la contrainte violés, sans valeur sensible

- Ancien repère et tâche rattachée : tâche 3.4 ; section « 3. Pipeline de composition, graphe déterministe et diagnostics », ligne 21 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL12 — Implémenter les sept registres génériques (modules, dépendances, cycle de vie, services, événements, configuration, extensions) alimentés uniquement par des modèles validés — vérification : tests unitaires démontrant le refus d'enregistrement d'une contribution non déclarée et l'idempotence d'un double enregistrement

- Ancien repère et tâche rattachée : tâche 4.1 ; section « 4. Registres génériques, configuration par références et règle data-driven », ligne 25 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL13 — Implémenter la résolution de configuration par priorité déclarée (schéma, défauts, statique, runtime, références de secrets) — vérification : tests unitaires de surcharge d'une même clé avec valeur gagnante reproductible ; le noyau ne résout aucune valeur de secret, test de contrôle de la face publique

- Ancien repère et tâche rattachée : tâche 4.2 ; section « 4. Registres génériques, configuration par références et règle data-driven », ligne 26 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL14 — Implémenter le jeu de composants requis porté en données de composition validées — preuve à renouveler avec composants requis contraints (`"id [comparateurs]"`, voir 6.6) — vérification : test d'intégration déclarant `pixs.core` comme requis en données seulement ; l'absence invalide l'activation avant chargement avec diagnostic, et un test vérifie l'absence de tout nom de concept métier codé en dur dans le code du noyau

- Ancien repère et tâche rattachée : tâche 4.3 ; section « 4. Registres génériques, configuration par références et règle data-driven », ligne 27 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL15 — Implémenter les états installed, enabled, configured, ready, healthy et les opérations mécaniques `discover`, `validate`, `install`, `enable`, `configure`, `start`, `disable` — vérification : tests unitaires d'états non confondus (installé-désactivé ≠ prêt) et de refus explicite de `migrate`, `upgrade`, `uninstall`, `purge` hors périmètre

- Ancien repère et tâche rattachée : tâche 5.1 ; section « 5. Cycle de vie mécanique et interfaces publiques », ligne 31 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL16 — Implémenter les hooks de cycle de vie ordonnés par le graphe résolu — vérification : test d'intégration comparant deux exécutions complètes, ordre des hooks et du chargement identiques

- Ancien repère et tâche rattachée : tâche 5.2 ; section « 5. Cycle de vie mécanique et interfaces publiques », ligne 32 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL17 — Exposer l'interface publique du noyau par les façades de paquet et borner l'export — vérification : un test d'intégration importe exclusivement l'API déclarée et asserte que les modules privés ne figurent pas dans les façades exportées

- Ancien repère et tâche rattachée : tâche 5.3 ; section « 5. Cycle de vie mécanique et interfaces publiques », ligne 33 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL18 — Compléter la suite unitaire couvrant chaque scénario normé du périmètre (kernel, component-model, dependencies, capabilities, configuration, compatibility pour la partie déclarative) — preuve à renouveler aux exigences RSMP versions/preuves (voir 6.5–6.7) — vérification : `python -m unittest discover -s tests/unit` passe et la correspondance scénario-test est listée dans le rapport de session

- Ancien repère et tâche rattachée : tâche 6.1 ; section « 6. Tests et contrôles finaux », ligne 37 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL19 — Compléter la suite d'intégration sur compositions synthétiques (résolution complète, ambiguïtés, cycles, composant requis absent, deux ordres de découverte) — vérification : `python -m unittest discover -s tests/integration` passe avec preuves reproductibles

- Ancien repère et tâche rattachée : tâche 6.2 ; section « 6. Tests et contrôles finaux », ligne 38 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL20 — Vérifier l'absence de secret et de donnée de production dans fixtures, rapports et diagnostics — périmètre : scan exclusivement des artefacts synthétiques de tests et diagnostics et des rapports de test autorisés ; AUCUN parcours des sources exclues par AGENTS.md ni lecture de secret ; les fixtures sentinelles (placeholders volontaires prouvant la détection) sont évaluées séparément du contrôle des sorties moteur — vérification : test automatisé de motifs sensibles sur tout artefact de test du périmètre, suite passant sans fuite détectée

- Ancien repère et tâche rattachée : tâche 6.3 ; section « 6. Tests et contrôles finaux », ligne 39 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL21 — Exécuter les contrôles finaux du change : `python -m compileall src/`, suite complète `unittest`, `bash -n` et `shellcheck` sur tout script auxiliaire éventuellement produit — vérification : chaque commande sort code 0 et la sortie est consignée dans le rapport de session

- Ancien repère et tâche rattachée : tâche 6.4 ; section « 6. Tests et contrôles finaux », ligne 40 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL22 — Schéma capacités/contrats versionnés et adaptation des fixtures : manifests `[provides].capabilities` et `[implements].contracts` en tables `{id, version, …}` schéma 1, refus des anciennes chaînes sans version avec diagnostic, fixtures historiques adaptées, version du composant jamais proxy — vérification : tests unitaires de validation (construction valide, rejet sans version nommant champ et entrée) et suite existante adaptée passant

- Ancien repère et tâche rattachée : tâche 6.5 ; section « 6. Tests et contrôles finaux », ligne 41 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL23 — Contraintes composants/capacités/contrats/requis : six comparateurs (`== != >= <= > <`), conjonctions, préversions ordre SemVer standard, métadonnées de build ignorées en précédence, syntaxes malformées refusées, évaluation sur versions propres (jamais la version du composant pour une capacité ou un contrat), composants requis contraints, sélection configurée incompatible refusée — vérification : tests unitaires et d'intégration (contrainte insatisfaite, malformée, mismatch de version, déterminisme deux ordres) passant avec diagnostics nommant consommateur, cible, contrainte et version trouvée

- Ancien repère et tâche rattachée : tâche 6.6 ; section « 6. Tests et contrôles finaux », ligne 42 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C24-SL24 — Preuves externes et portée P0 : `ConformityAttestation` en mémoire hors manifest (absence, mismatch de fournisseur/version/build, échec, malformée, ambiguïté refusés ; couverture complète PASS autorisant ; composition déterministe préservée), doubles de preuves clairement nommés limités aux fixtures, exposition P0 limitée aux dimensions connues sans prétention globale — vérification : tests d'intégration de chaque cas passant avec diagnostics non sensibles

- Ancien repère et tâche rattachée : tâche 6.7 ; section « 6. Tests et contrôles finaux », ligne 43 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
