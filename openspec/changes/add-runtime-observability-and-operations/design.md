# Conception — C15

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 formalise le profil ; ses précisions normatives restent proposées tant qu’elles ne sont pas approuvées/adoptées.

## État actuel vérifié

Constat : correlated_log et health_classifier sont bornés/purs ; ils ne démontrent ni métriques/traces globales ni opérations de maintenance persistantes.

Sources consultées et empreintes recoupées avec la matrice :

- [src/pixs/backend/correlated_log.py](../../../src/pixs/backend/correlated_log.py).
- [src/pixs/backend/health_classifier.py](../../../src/pixs/backend/health_classifier.py).
- [src/pixs/backend/liveness_view.py](../../../src/pixs/backend/liveness_view.py).
- [src/pixs/backend/runtime_profiles.py](../../../src/pixs/backend/runtime_profiles.py).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Brancher signaux/santé sur faits runtime réellement sondés, avec bornes et corrélation. Management distinct non public, plans et résultats persistés, confirmation des effets sensibles, maintenance générale/composant/route et drainage. Le diagnostic reste sans effet de réparation.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Surfaces et identités de management, objectifs/limites, méthodes de mesure et rétentions ; aucun seuil arbitraire ou privilège système nouveau.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [integrate-runtime-authorization-and-super-admin](../integrate-runtime-authorization-and-super-admin/proposal.md).
- [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md).
- [activate-reference-runtime-composition](../activate-reference-runtime-composition/proposal.md).
- [add-reference-worker-scheduler-and-event-delivery](../add-reference-worker-scheduler-and-event-delivery/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

PG indisponible → readiness fausse avec liveness distincte ; panne optionnelle isolée ; opération non autorisée refusée ; maintenance générale/composant/route ; arrêt/reprise observés sans perte silencieuse.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.

## Approfondissement issu de l’audit du 17 octobre 2026

Conception proposée sans implémentation. Ces contrats de travail ne modifient pas le canon ; tout changement normatif requiert son delta approuvé.

Isoler collecte de faits, classification de santé et actions de maintenance. Une sonde porte propriétaire, instant/version, périmètre et résultat observé ; le classificateur pur existant consomme ces faits, sans en inventer ni déclencher une réparation.

Les adaptateurs d’exécution doivent borner délais/concurrence et isoler les erreurs des providers optionnels. Un composant essentiel ou un contrôle invérifiable bloque la readiness concernée. Le résultat DEGRADED d’une fonction pure ne prouve ni isolation du processus ni arrêt effectif ; la liveness reste distincte.

C15 possède plans de maintenance, drainage et diagnostic ; N01 possède décisions d’incident, révocation/quarantaine et réactivation d’urgence. Réutiliser les mêmes contrats propriétaires et corrélations, avec opérations distinctes. Arrêter surfaces de management, budgets, rétention et méthodes de sonde avant code.

### Exigences auditées et preuves de sortie futures

| Référence canonique | Statut statique après audit | Critère à démontrer |
|---|---|---|
| [resilience #1](../../../openspec/specs/resilience/spec.md#L8) | P | Panne optionnelle injectée sur runtime réel, reste disponible si invariants conservés ; état et reprise observés. |
| [resilience #2](../../../openspec/specs/resilience/spec.md#L17) | P | Signature/contexte/contrôle invérifiable : refus sur HTTP/jobs et aucune readiness permissive. |
| [resilience #3](../../../openspec/specs/resilience/spec.md#L26) | ND | N01 : décision persistante, effets réconciliés, admissions bloquées, audit et réactivation explicite sans faux succès. |

Voir [audit individuel et limites des preuves](../define-first-installable-pbo-profile/audit-ne-94.json) et [rapport d’audit](../../../reports/audit-ne-94-2026-10-17/RAPPORT.md). Les tâches de réalisation restent non cochées.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

### T02 — PBO/PFO réellement servi par le paquet

Le serveur/bundle/routage et la frontière HTTP distribuée ne sont pas détaillés par un propriétaire commun. N04 dédié et deltas ciblés validés ; décisions de serveur/session/transport encore ouvertes.

Contrôles à intégrer : Navigation directe du shell via service livré ; Erreur API sans fallback HTML ; Hôtes/origines/en-têtes non fiables, CSRF si cookie ; Management et rôles non publics.

### T03 — Réadmission après état restauré

La restauration cohérente de données ne prouve ni fraîcheur de révocations/incidents ni admissibilité des effets différés. N05 dédié et delta ciblé validés ; faits nécessaires et revalidation détaillée à définir avant code.

Contrôles à intégrer : Snapshot antérieur à révocation/rotation/incident ; Effet déjà engagé dont réponse perdue ; Marqueur externe incohérent ; Interruption puis reprise de réconciliation sans réémission automatique.

### T08 — Audit exhaustif du panneau et navigation SPA

L’audit de chaque activité du panneau inclut navigation/lecture ; des logs ou un acquittement mémoire n’en prouvent pas la persistance. Compléter protocole C05/C13 et critères de volumétrie/minimisation C15 ; préserver exception Super Admin.

Contrôles à intégrer : Panne sink avant affichage/action ordinaire refusée selon contrat ; Dérogation root sans audit annoncé à tort ; Navigation SPA reliée à une preuve serveur et aucune donnée sensible copiée.

### T11 — Arrêt, maintenance et ancien détenteur de lease

Le séquencement des nouvelles admissions, du drain et des reprises est une interaction ; un timeout du processus ne prouve pas la fin d’un effet. Compléter recette commune C09/C15/C18 ; pas de nouvel orchestrateur.

Contrôles à intégrer : Lease expiré empêchant une nouvelle action ; Maintenance ciblée et install entière distinguées ; Signal pendant effet, sortie explicite sans perte silencieuse ; Worker non public.

### T15 — Langues, thèmes et accessibilité de tous les parcours

Les parcours CLI, erreurs API, management et secours font aussi partie des textes utilisateur ; couverture ne se limite pas à la page du shell. Compléter la matrice C12/C17 et les contrats de messages ; codes stables non localisés.

Contrôles à intégrer : Deux navigateurs déclarés, clavier/zoom/lecteur d’écran ; Erreurs et confirmations d’installation/exploitation localisées ; Thème/session/tenant sans fuite d’état.

Voir [audit transversal durable](../define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.
