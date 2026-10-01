# Design

## Context

Voir proposal.md — Why pour la motivation. État observé en lecture seule : le dépôt
ne déclare aucun projet Python (`pyproject.toml` absent de la racine). Contraintes :
tous les comportements visés sont déjà normés par les specs actives ; aucune dépendance
externe non validée ne doit être présumée ; le noyau reste un mécanisme pur, à refus
fermé et composition déterministe.

## Goals / Non-Goals

**Goals :**
- Moteur de composition générique, sans concept métier ni fournisseur concret.
- Modèles déclaratifs validés avant tout chargement ; pipeline de composition explicite.
- Graphe, ordre de chargement et hooks stables à entrée identique ; diagnostics typés.
- Règle « module obligatoire » portée en données de composition.
- Configuration schématique et secrets exclusivement par références.
- Niveaux de tests unitaire et intégration séparés, reproductibles, sans secret.

**Non-Goals (limites de design, en plus des exclusions du proposal) :**
- Aucune exécution de code déclarée dans un manifest ; aucun chargement distant ou dynamique.
- Pas de persistance d'état de composition en base (résolution en mémoire, preuves rejouables).
- Pas d'implémentation des suites de conformité provider ni des opérations destructives
  du cycle de vie ; interfaces définies, comportement effectif en changes ultérieurs.

## Decisions

- **D1 — Registres génériques et modèles déclaratifs.** Sept registres du noyau
  (modules, dépendances, cycle de vie, services, événements, configuration, extensions)
  alimentés exclusivement par des modèles validés issus des manifests ; aucune
  auto-inspection ni import dynamique avant validation.
  *Alternative écartée* : auto-enregistrement par décorateurs — violerait l'explicite,
  la déterminité de découverte et le refus des contributions non déclarées.
- **D2 — Pipeline `discover → validate → resolve → activate`.** Sous-ensemble mécanique
  obligatoire des opérations de cycle de vie ; chaque étape idempotente, produisant des
  diagnostics nommant l'élément et la contrainte en cause ; `activate` refuse toute
  composition ambiguë, incomplète ou incompatible avant tout chargement.
  *Alternative écartée* : chargement en une phase — empêcherait le refus pré-activation
  et les diagnostics d'étape exigés par lifecycle/modules.
- **D3 — Graphe stable et tri déterministe.** Dépendances indexées par identifiant
  canonique namespacé ; tri topologique avec départage explicite par ordre
  d'identifiants ; cycles et ambiguïtés détectés avant activation.
  *Alternative écartée* : bibliothèque de graphes externe (dépendance non validée,
  non nécessaire) ; ordre filesystem/insertion (interdit par dependencies).
- **D4 — Règle `pixs.core` data-driven.** La composition déclare un jeu de composants
  requis avec contraintes de version ; le noyau valide présence et compatibilité sans
  connaître la sémantique des identifiants.
  *Alternative écartée* : codage en dur dans le noyau — introduirait une connaissance
  fonctionnelle interdite par kernel.
- **D5 — Manifests TOML via `tomllib` (stdlib, Python ≥ 3.11).** Schéma validé par
  `schema_version` déclarée ; version inconnue refusée avant parsing sémantique ;
  valeurs sensibles refusées par validation structurelle ; secrets représentés par
  références résolues hors noyau par une interface de provider non implémentée ici.
  *Alternatives écartées* : YAML/JSON (format normé `component.toml`) ; `tomli`
  (dépendance externe non validée).
- **D6 — Tests : stdlib `unittest` uniquement, arborescence séparée par niveau**
  (`unit` : schémas, graphe, cycles, ambiguïtés, identifiants, états ; `integration` :
  composition complète sur coquille de manifests synthétiques). Fixtures générées
  localement, sans secret ni donnée de production.
  *Alternative documentée* : `pytest`, ergonomique mais dépendance externe soumise à
  validation CGPT ; migrable sans réécriture grâce aux interfaces standard.
- **D7 — Versions distinctes et contraintes (clarification RSMP, sans comportement
  indépendant).** Les versions de composant, capacité, contrat et schéma sont
  distinctes ; les contraintes portent sur la version propre de chaque dimension
  (références normatives : specs `component-model` pour le schéma, `dependencies`
  pour la grammaire et la sémantique, `capabilities` et `compatibility` pour la
  résolution et les preuves). La version du composant ne sert jamais de proxy.
  Les fixtures historiques en chaînes sans version sont adaptées au schéma 1 ;
  les anciennes formes restent refusées avec diagnostic.
- **D8 — Preuves externes et portée P0 (clarification RSMP, sans comportement
  indépendant).** La conformité est établie par des `ConformityAttestation`
  fournies en mémoire par l'appelant de confiance (entrée documentée de
  `compose`, hors manifest) ; couverture exigée de chaque composant activé et
  de chaque capacité ou contrat résolu auprès de son fournisseur exact, refus
  fermé sinon. P0 n'évalue que ses dimensions connues et ne prétend aucune
  compatibilité globale. Les fixtures MAY injecter des doubles de preuves
  clairement nommés ; aucune suite provider effective n'est implémentée
  (exclusion initiale préservée).

## Risks / Trade-offs

- [Réimplémentation d'algorithmes de graphe] → périmètre small et borné (tri
  topologique + détection de cycles), testé sur chaque scénario normé de kernel/dependencies.
- [`unittest` moins ergonomique que `pytest`] → assertions standard et fixtures
  explicites ; migration possible si CGPT valide la dépendance.
- [`tomllib` impose Python ≥ 3.11] → cible Debian supportée ; tout repli (ex. `tomli`)
  constituerait une nouvelle dépendance et requerra une validation CGPT distincte.
- [Dérive du schéma de manifest futur] → `schema_version` obligatoire, version inconnue
  bloquante, compatibilité déclarée dans le validateur.
- [Contournement de la règle « requis » par composition erronée] → échec fermé :
  absence d'un composant requis = invalidation avant activation, diagnostic explicite.

## Migration Plan

Bootstrap purement additif et idempotent : création de `pyproject.toml` (PEP 621,
layout `src/`) et du paquet du noyau ; la re-exécution détecte l'état existant et ne
duplique rien. Aucune donnée migrée (le change n'introduit pas de persistance).
Rollback : suppression du paquet noyau et de la déclaration de projet ajoutés ; aucun
comportement préexistant modifié ; aucune matrice de compatibilité impactée (aucune
version publiée antérieure).
