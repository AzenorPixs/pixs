# Conception — C18

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 formalise le profil ; ses précisions normatives restent proposées tant qu’elles ne sont pas approuvées/adoptées.

## État actuel vérifié

Constat : Aucun répertoire de packaging Debian initial ni paquet PBO/PFO qualifié n’est identifié ; le README déclare les distributions non livrées.

Sources consultées et empreintes recoupées avec la matrice :

- [BUILD.md](../../../BUILD.md).
- [README.md](../../../README.md).
- [openspec/specs/deb-package/spec.md](../../specs/deb-package/spec.md).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Construire depuis sources versionnées le paquet PBO/PFO incluant modules PZT/DNS mais aucun binaire PA ; services par rôle, code immuable et configuration administrée externe préservée. Installation, mise à niveau, désinstallation et purge explicite distinctes ; aucun code distant téléchargé implicitement.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Noms/versions du paquet et exécutables, architecture qualifiée, dépendances et comptes d’exécution ; qualification requise avant sélection d’outil supplémentaire.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

- [add-pbo-security-quarantine-and-revocation](../add-pbo-security-quarantine-and-revocation/proposal.md) — dépendance explicitée après audit du 17 octobre 2026.

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [activate-reference-runtime-composition](../activate-reference-runtime-composition/proposal.md).
- [add-installation-and-first-configuration](../add-installation-and-first-configuration/proposal.md).
- [add-reference-worker-scheduler-and-event-delivery](../add-reference-worker-scheduler-and-event-delivery/proposal.md).
- [compose-modular-frontend-with-core-api](../compose-modular-frontend-with-core-api/proposal.md).
- [add-initial-administration-panel](../add-initial-administration-panel/proposal.md).
- [add-essential-pbo-pzt-and-dns-modules](../add-essential-pbo-pzt-and-dns-modules/proposal.md).
- [add-runtime-observability-and-operations](../add-runtime-observability-and-operations/proposal.md).
- [add-upgrade-backup-and-restore-contracts](../add-upgrade-backup-and-restore-contracts/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Construire/install/mise à niveau/désinstallation sur environnement isolé ; configuration préservée et données non purgées ; pas de téléchargement implicite ; services avec même lifecycle ; qualification de l’artefact final en C17/C19, pas seulement des sources.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.

## Dépendances après audit transversal P0

[C07](../activate-reference-runtime-composition/proposal.md), [C08](../add-installation-and-first-configuration/proposal.md), [C09](../add-reference-worker-scheduler-and-event-delivery/proposal.md), [C11](../compose-modular-frontend-with-core-api/proposal.md), [C13](../add-initial-administration-panel/proposal.md), [C14](../add-essential-pbo-pzt-and-dns-modules/proposal.md), [C15](../add-runtime-observability-and-operations/proposal.md), [C16](../add-upgrade-backup-and-restore-contracts/proposal.md), [N01](../add-pbo-security-quarantine-and-revocation/proposal.md), [N03](../add-p0-artifact-trust-and-preinstallation-verification/proposal.md), [N04](../define-p0-web-serving-and-security-boundary/proposal.md), [N05](../add-p0-post-restore-reconciliation-and-readmission/proposal.md).

Les conditions d’activation et la construction des résultats sont séparées de cet ordre de préparation ; aucun cycle inverse vers la recette finale.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

### T01 — Confiance avant première installation

C19 réalise tardivement les vérifications nécessaires avant installation par C17. N03 dédié validé ; déplacer les contrats/vérificateurs précoces, conserver publication finale C19.

Contrôles à intégrer : Canal interdit et signature absente/expirée/révoquée refusés avant installation ; Révocation vérifiable publication indisponible ; Paquet qualifié immuable et révalidation si octets ou identité changent.

### T02 — PBO/PFO réellement servi par le paquet

Le serveur/bundle/routage et la frontière HTTP distribuée ne sont pas détaillés par un propriétaire commun. N04 dédié et deltas ciblés validés ; décisions de serveur/session/transport encore ouvertes.

Contrôles à intégrer : Navigation directe du shell via service livré ; Erreur API sans fallback HTML ; Hôtes/origines/en-têtes non fiables, CSRF si cookie ; Management et rôles non publics.

### T11 — Arrêt, maintenance et ancien détenteur de lease

Le séquencement des nouvelles admissions, du drain et des reprises est une interaction ; un timeout du processus ne prouve pas la fin d’un effet. Compléter recette commune C09/C15/C18 ; pas de nouvel orchestrateur.

Contrôles à intégrer : Lease expiré empêchant une nouvelle action ; Maintenance ciblée et install entière distinguées ; Signal pendant effet, sortie explicite sans perte silencieuse ; Worker non public.

### T13 — Première livraison et origines de mise à niveau

Une première version n’a pas nécessairement d’origine distribuée supportée ; un numéro source ancien ne prouve pas une migration autorisée. Déclarer les origines réellement supportées dans C16/C19 ; cas sans origine explicite et sauts non prouvés refusés.

Contrôles à intégrer : Installation vierge distincte d’une mise à niveau ; Interruption de migration et contraction prématurée refusées ; Retour arrière seulement si matrice accepte schéma/données ; Aucun downgrade automatique.

### T17 — Reproductibilité, versions et dossier de livraison

Les pins observés et unités vertes ne valent pas qualification officielle du graphe ou du paquet ; signatures finales ne doivent pas modifier l’objet déjà qualifié. Contrôles officiels/compatibilité avant build puis sur l’artefact final ; aucune version actualisée ou dépendance installée pendant l’audit.

Contrôles à intégrer : Deux builds contrôlés et graphe identique ; Identité de l’artefact de recette égale à celle livrée ; Budgets/support déclarés avec preuves et limites ; Strict global exit réel conservé, warnings non masqués.

Voir [audit transversal durable](../define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.


## Gestion PBO et séparation PA/PZT — décision du 17 octobre 2026

Le [canon adopté](../separate-pa-pzt-and-pbo-management-modules/design.md) définit
pixs.agent pour PA hors PZT et pixs.pzt pour le composant réseau indépendant.
La composition PBO inclut ces modules ; la présence des exécutables PA/PZT
ne vaut pas activation. L'exécution PA/PZT n'est pas sélectionnée dans le
premier P0 par cette mise à jour. Les obligations PBO de gestion restent à
satisfaire et à recouper avant qualification du profil et du paquet.
Les contrats de transport/contrôle et leurs garanties restent dans les lots
propriétaires ; réconcilier deltas proposés, copies et empreintes de préparation
avec le canon actuel avant réalisation. Aucune tâche produit n'est réalisée.
