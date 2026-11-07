# Statistiques — add-p0-tenant-membership

Session maîtresse `ses_f0cd50463ffezWnvxK0kEMln8q`. Historique intégral conservé : 2026-09-30T16:34:35.555Z à 2026-09-30T18:32:13.250Z. Rapport borné avant sa rédaction et son propre mandat. Début des tâches de codage : 2026-09-30T16:48:18.944Z. La suspension terminale précédente et la reprise sont incluses dans la durée calendaire.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| muse-spark-1.3-contributor | N/A — version non publiée | opencode-go | HIGH — métadonnées vérifiées | N/A — aucune sonde valide | N/A — aucune sonde valide | N/A — génération active non isolée |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---|---|---|
| Codex (GPT-6 déclaré) | N/A — télémétrie exacte absente | OpenAI | HIGH demandé ; mesure absente | N/A | N/A | N/A |

Aucun dénominateur de service fiable : les durées des messages incluent les outils et attentes ; elles ne sont pas du temps actif de génération. Chevauchements non mesurables.

## 1. Statistiques générales et décisions

Un outil terminé sans erreur est compté réussi et autorisé techniquement ; cela ne prouve pas une approbation manuelle. Une réponse MCP négative demeure un appel MCP réussi : les décisions CAB sont comptées séparément. Un test exit 1 est une erreur technique, jamais un refus.

| Mesure | Valeur | Part |
|---|---|---|
| Messages | 273 | 100 % |
| Appels outils | 211 | 100 % |
| Appels réussis | 202 | 95.7 % |
| Refus natifs observés | 0 | 0.0 % |
| Erreurs techniques | 9 | 4.3 % |

| Décision CAB finale par requestId unique | Nombre | Part |
|---|---|---|
| APPROVED | 34 | 94.4 % |
| REJECTED | 1 | 2.8 % |
| NEEDS_CLARIFICATION | 1 | 2.8 % |
| Total | 36 | 100 % |

34 opérations Bash/écriture effectivement exécutées (100 % corrélées à 34 approbations uniques), dont deux tests exit 1. Le refus design initial n’a produit aucune écriture ; la commande pip NEEDS_CLARIFICATION n’a pas été exécutée. Les anciennes décisions du contrôleur non retrouvées après redémarrage sont réconciliées par leurs réponses MCP historiques réelles.

| Tokens natifs — production | Nombre | Part du total natif |
|---|---|---|
| Entrée hors cache | 911927 | 3.2 % |
| Sortie | 53671 | 0.2 % |
| Raisonnement | 17925 | 0.1 % |
| Cache lu | 27777481 | 96.6 % |
| Cache écrit | 0 | 0.0 % |
| Total | 28761004 | 100 % |

Coût natif cumulé : 0.161066862 (100 % du coût disponible, unité de l’API). Coût orchestrateur : N/A. Compactages : aucun événement de compaction présent dans cet historique OpenCode ; nombre et durées des compactages Codex N/A.

Résultat : 10/10 tâches prouvées (100 %), 14 tests unitaires dédiés, 4 intégrations dédiées, 547 régressions unitaires et 155 intégrations globales OK. Les tests dédiés sont inclus dans les suites globales : ne pas les additionner comme cas uniques. Les deux intégrations anciennes avaient échoué ; la reprise avec les dépendances déclarées a réussi. AST Python 3.11, UTF-8/LF, exemple README et strictes OpenSpec réussis.

| Sonde | État | Lignes | TTMT / débit exploitable |
|---|---|---|---|
| début | Invalide | 193 | N/A |
| début retry | Invalide | 193 | N/A |
| +30 min | Invalide | 193 | N/A |
| fin avant suspension | Invalide | 193 | N/A |
| fin après archive | Invalide | 193 | N/A |

Quatre relèves effectives prévues : début, +30 min, fin avant suspension et fin après reprise, avec un retry initial distinct. Cinq tentatives exécutées (100 %), 0 valides (0.0 %), 5 invalides (100 %), 0 manquées (0.0 %) sur ces relèves ; aucune relève rétroactive. Le palier +60 min tombait après suspension du codage ; la reprise locale a duré moins de 30 minutes avant archivage. Moyenne/minimum/maximum : N/A. La relève +30 a été tardive et ce retard est conservé. Surcharge de durée séparée : total N/A car les bornes exactes manquent pour certaines tentatives ; début 55.350 s, +30 min 22.240 s et fin après archive 141.311 s observés. Surcharge séparée : 11795 tokens de sortie (100 % des sorties de sondes), 3633 de raisonnement (100 % des raisonnements de sondes) ; coût partiel connu 0.004488226 (total N/A car coûts absents sur certaines sondes). Le chronométrage de certaines sondes a inclus un événement utilisateur et est inexploitable.

## 2. Types de messages et d’outils

| Rôle | Nombre | Part |
|---|---|---|
| user | 54 | 19.8 % |
| assistant | 219 | 80.2 % |
| Total | 273 | 100 % |

| Type de partie | Nombre | Part |
|---|---|---|
| text | 106 | 10.2 % |
| step-start | 218 | 21.0 % |
| reasoning | 287 | 27.6 % |
| tool | 211 | 20.3 % |
| step-finish | 217 | 20.9 % |
| Total | 1039 | 100 % |

| Terminaison assistant | Nombre | Part |
|---|---|---|
| tool-calls | 165 | 75.3 % |
| stop | 52 | 23.7 % |
| incomplete | 2 | 0.9 % |
| Total | 219 | 100 % |

| Outil | Nombre / part | Réussis / taux | Refus / taux | Erreurs / taux |
|---|---|---|---|---|
| cgpt-validation_broker_readiness | 52 (24.6 %) | 52 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_request_validation | 36 (17.1 %) | 35 (97.2 %) | 0 (0.0 %) | 1 (2.8 %) |
| cgpt-validation_get_approval | 9 (4.3 %) | 9 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| bash | 23 (10.9 %) | 21 (91.3 %) | 0 (0.0 %) | 2 (8.7 %) |
| read | 57 (27.0 %) | 53 (93.0 %) | 0 (0.0 %) | 4 (7.0 %) |
| glob | 4 (1.9 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| grep | 4 (1.9 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_poll_approval | 4 (1.9 %) | 2 (50.0 %) | 0 (0.0 %) | 2 (50.0 %) |
| write | 11 (5.2 %) | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_list_pending | 10 (4.7 %) | 10 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| cgpt-validation_broker_health | 1 (0.5 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 211 (100 %) | 202 (95.7 %) | 0 (0.0 %) | 9 (4.3 %) |

## 3. Fichiers modifiés

Tentatives d’écriture natives et mandat de fichier explicitement refusé ; dénominateur : 12 tentatives (11 exécutées, 1 refusée). Le mandat de ce rapport est postérieur à la borne et n’est pas inclus.

| Chemin absolu complet avant archive | Tentatives / part | Approuvées exécutées / taux | Refusées / taux | Erreurs / taux |
|---|---|---|---|---|
| /home/devops/datas/pixs/openspec/changes/add-p0-tenant-membership/proposal.md | 1 (8.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-tenant-membership/design.md | 2 (16.7 %) | 1 (50.0 %) | 1 (50.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-tenant-membership/tasks.md | 2 (16.7 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/openspec/changes/add-p0-tenant-membership/specs/core/spec.md | 1 (8.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/identity/tenant_membership.py | 1 (8.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/identity/__init__.py | 1 (8.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/src/pixs/core/identity/README.md | 1 (8.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/unit/test_tenant_membership.py | 1 (8.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_tenant_membership_integration.py | 1 (8.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| /home/devops/datas/pixs/tests/integration/test_identity_facade.py | 1 (8.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 12 (100 %) | 11 (91.7 %) | 1 (8.3 %) | 0 (0.0 %) |

Le dossier du change est déplacé par la commande d’archive vers `/home/devops/datas/pixs/openspec/changes/archive/2026-09-30-add-p0-tenant-membership`. `.openspec.yaml` préexistait et n’a pas été réécrit. Les onze références hors cible sont inchangées ; la façade originale est conservée avec ajouts seuls. La norme core est byte-identique après archive. Les écritures orchestrateur du checkpoint `/home/devops/datas/pixs/output/cismp-state.json` sont hors télémétrie native : nombre N/A. L’environnement `.venv/` contient les seuls artefacts locaux autorisés, sans lecture/indexation de ses sources par le modèle.

## 4. Commandes

| Famille | Exécutées / part | Réussies / taux | Refusées / taux | Erreurs / taux |
|---|---|---|---|---|
| Prévol true | 6 (26.1 %) | 6 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec validate | 4 (17.4 %) | 4 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Tests unittest | 7 (30.4 %) | 5 (71.4 %) | 0 (0.0 %) | 2 (28.6 %) |
| Contrôles Python | 2 (8.7 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Création venv | 1 (4.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Installation déclarée | 1 (4.3 %) | 1 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| OpenSpec archive/aide | 2 (8.7 %) | 2 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Total | 23 (100 %) | 21 (91.3 %) | 0 (0.0 %) | 2 (8.7 %) |

Commandes refusées : aucune (0/24 mandats de commande, 0.0 %). Une commande clarifiée sans exécution (1/24, 4.2 %) : `/home/devops/python/current/bin/pip3 --python /home/devops/datas/pixs/.venv/bin/python install Djan…`. Les 23 autres mandats ont été exécutés (95.8 %) ; deux validations ont exit 1, puis une nouvelle intégration en venv a exit 0. Aucun mandat n’a été réutilisé.

## 5. Accès web

Agent de codage : aucun appel webfetch/websearch (0/211 outils, 0.0 %), aucune URL visitée ou refusée. Taux par résultat N/A, dénominateur zéro. L’installation pip autorisée a téléchargé les distributions ; les sorties conservées donnent les noms, pas les URL complètes de téléchargement : URL N/A, ne pas en inventer.

Accès externes orchestrateur connus, hors compte des outils OpenCode : quotas HTTPS réussis et consultation officielle du comportement d’authentification. URL approuvées effectivement consultées :

- `https://opencode.ai/zen/go/v1/usage`
- `https://raw.githubusercontent.com/anomalyco/opencode/v1.18.33/packages/opencode/src/auth/index.ts`
- `https://raw.githubusercontent.com/anomalyco/opencode/v1.18.33/packages/opencode/src/server/routes/i…`

Effectifs exacts globaux des accès orchestrateur et taux : N/A ; aucune URL refusée observée. Les API de contrôle loopback sont des communications locales CAB/OpenCode, pas des visites web de l’agent.

## 6. Synthèse globale

| Durée de la session de codage | Valeur |
|---|---|
| Début | 2026-09-30T16:34:35.555Z |
| Fin — après archivage | 2026-09-30T18:32:13.250Z |
| Durée globale (pauses et attentes incluses) | 1 h 57 min 37 s |

| Mesure du quota Codex sur 7 jours | Horodatage du relevé | Quota utilisé | Réinitialisation |
|---|---|---|---|
| Avant — début de session | 2026-09-30T16:46:25.578Z | N/A | N/A |
| Après — après archivage de la spécification | 2026-09-30T18:32:13.250Z | N/A | N/A |
| Différence après − avant | — | N/A | — |

L’outil natif mcp__codex_app__get_usage_limits n’est pas exposé ; aucune identité codex/10080 minutes ni fenêtre comparable disponible. N/A n’est pas zéro. Les quotas sont partagés par le compte ; aucune consommation exclusive n’est attribuée au RUN.

| Domaine outils exécutés | Nombre / part globale | Réussis / taux | Refus / taux | Erreurs / taux |
|---|---|---|---|---|
| Fichiers | 11 (5.2 %) | 11 (100.0 %) | 0 (0.0 %) | 0 (0.0 %) |
| Commandes | 23 (10.9 %) | 21 (91.3 %) | 0 (0.0 %) | 2 (8.7 %) |
| Web | 0 (0.0 %) | 0 (N/A) | 0 (N/A) | 0 (N/A) |
| Autres | 177 (83.9 %) | 170 (96.0 %) | 0 (0.0 %) | 7 (4.0 %) |
| Global | 211 (100 %) | 202 (95.7 %) | 0 (0.0 %) | 9 (4.3 %) |

Les 36 décisions CAB (34 approbations, 1 refus de fichier et 1 clarification) sont un autre dénominateur ; ne pas les additionner aux 211 appels. Les 34 opérations mutantes/système sont corrélées à 34 mandats approuvés (100 %). Rapport produit ensuite sous mandat distinct. Tests et archive réussis ; avertissement non bloquant sur les titres français de proposal.md conservé, sans contournement des validations. Aucun Git, commit ou push exécuté dans le RUN ; état Git non inspecté.

Incident de secrets : PUT /auth a initialement fait persister la clé par OpenCode, contrairement à la contrainte sans fichier. Cette erreur est reconnue ; l’entrée persistée Go a ensuite été retirée par API DELETE autorisée, sans lire le fichier sensible. Le fournisseur Go est conservé et son authentification mémoire a réussi en HIGH. Aucune valeur de secret n’a été affichée ni transmise au modèle. La règle permanente interdit désormais PUT /auth pour l’injection ; elle ne constitue pas une preuve de remplacement du skill installé. Le projet cab et ses publications n’ont pas été modifiés.
