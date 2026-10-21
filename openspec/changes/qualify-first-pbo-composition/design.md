# Conception — C17

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 a été adopté et archivé le 18 octobre 2026 ; ses précisions normatives sont intégrées au canon. Les arbitrages propres au présent change restent à lever avant réalisation.

## État actuel vérifié

Constat : Le kit valide des manifests locaux et le noyau contrôle des attestations fournies ; aucune recette complète de l’artefact P0 initial n’est établie.

Sources consultées et empreintes recoupées avec la matrice :

- [src/pixs/developer_kit/README.md](../../../src/pixs/developer_kit/README.md).
- [src/pixs/kernel/conformity.py](../../../src/pixs/kernel/conformity.py).
- [src/pixs/backend/composition_proof.py](../../../src/pixs/backend/composition_proof.py).
- [tests/integration/test_composition_conformity.py](../../../tests/integration/test_composition_conformity.py).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Après C18, qualifier la composition réellement distribuée. Authentifier les preuves émises hors manifest par les suites versionnées ; distinguer unités, intégration réelle, conformité et manuel. Relier chaque scénario applicable à un verdict/version/artefact ; dimensions inconnues explicites, sans certificat global.

Le [cadrage Auth essentiel](../define-essential-autonomous-auth-module/design.md) est adopté au canon le 20 octobre 2026 pour ses trois deltas d'architecture. La recette future du profil standard vérifiera pixs.auth essentiel indépendant et le refus de son absence, le local PostgreSQL sans réseau externe, l'absence des connecteurs externes installés et des services LDAP/KDC/AD ou d'émission IdP activés implicitement, ainsi que l'isolation, la révocation et le secours propre sans MFA fictif. Les méthodes locales/MFA et l'enrôlement minimal restent proposés dans leurs dossiers propres et devront être adoptés puis qualifiés avant toute garantie correspondante. Aucun résultat historique n'est étendu à ce périmètre et aucune tâche de réalisation n'est cochée.

## Alternatives et frontière de conception

La sélection de [core-storage](../add-reversible-core-directory-storage/design.md) ajoute une recette optionnelle distincte : PostgreSQL initial, migration utilisateurs/groupes/ACL et relations vers OpenLDAP interne, mutations via Pixs sur LDAP puis retour depuis l'état LDAP courant. Vérifier invariants, décisions ACL, générations, interruption/reprise et absence de repli périmé. Cette sélection ne retire pas PostgreSQL aux autres domaines et ne transforme pas la qualification du profil local initial en preuve de migration.

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Versions actuelles et métadonnées officielles à vérifier avant qualification ; politique des quatre avertissements stricts existants à traiter sans masquer exit 1 ni réécrire le canon hors demande.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

- [add-pbo-security-quarantine-and-revocation](../add-pbo-security-quarantine-and-revocation/proposal.md) — dépendance explicitée après audit du 17 octobre 2026.

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [integrate-runtime-authorization-and-super-admin](../archive/2026-10-21-integrate-runtime-authorization-and-super-admin/proposal.md).
- [add-protected-core-http-commands-and-queries](../add-protected-core-http-commands-and-queries/proposal.md).
- [add-installation-and-first-configuration](../add-installation-and-first-configuration/proposal.md).
- [add-reference-worker-scheduler-and-event-delivery](../add-reference-worker-scheduler-and-event-delivery/proposal.md).
- [enforce-core-data-governance-and-lifecycle](../enforce-core-data-governance-and-lifecycle/proposal.md).
- [complete-shared-ui-i18n-and-accessibility](../complete-shared-ui-i18n-and-accessibility/proposal.md).
- [add-initial-administration-panel](../add-initial-administration-panel/proposal.md).
- [add-essential-pbo-pzt-and-dns-modules](../add-essential-pbo-pzt-and-dns-modules/proposal.md).
- [add-runtime-observability-and-operations](../add-runtime-observability-and-operations/proposal.md).
- [add-upgrade-backup-and-restore-contracts](../add-upgrade-backup-and-restore-contracts/proposal.md).
- [build-first-pbo-pfo-debian-package](../build-first-pbo-pfo-debian-package/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Chaque exigence/scénario applicable dispose d’un verdict et d’une preuve actuelle ; preuves négatives sécurité/tenant/reprise ; versions officielles et métadonnées revérifiées avant release ; strict OpenSpec avec exit natif rapporté ; objectifs déclarés mesurés.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.

## Approfondissement issu de l’audit du 17 octobre 2026

Conception proposée sans implémentation. Ces contrats de travail ne modifient pas le canon ; tout changement normatif requiert son delta approuvé.

Établir un manifeste de campagne attaché au paquet C18 et au profil C00 : versions des composants, configuration non sensible, plateforme, jeux synthétiques, scénarios et résultats reproductibles. Une unité pure, une archive ou un dossier préparé ne couvre pas un scénario intégré.

La campagne P0 comporte isolation de panne optionnelle, refus en dégradé, incident N01 avec propagation/reprise et réactivation, installation/restauration, droits ordinaires et exception canonique Super Admin. Les objectifs déclarés du profil sont mesurés ; O31 approfondit ensuite les charges sélectionnées sans faire dépendre C17 d’O31.

Séparer PASS/FAIL/non exécuté et applicabilité motivée, avec écart, effet observé et preuve. Les capacités optionnelles non sélectionnées restent hors campagne P0 ; Q01 les qualifie par profil. N01 devient un prérequis explicite, sans exiger catalogue O29 ni PA actif.

### Exigences auditées et preuves de sortie futures

| Référence canonique | Statut statique après audit | Critère à démontrer |
|---|---|---|
| [performance #1](../../../openspec/specs/performance/spec.md#L8) | P | Référence initiale, protocole et signal observé conservés avant justification d’une optimisation. |
| [performance #2](../../../openspec/specs/performance/spec.md#L17) | ND | Budgets par surface/profil, seuils déclarés avant mesure, dépassement reproductible signalé. |
| [performance #3](../../../openspec/specs/performance/spec.md#L26) | P | Release/profil, matériel, surface, charge, méthode et validité associés ; hors profil informatif. |
| [performance #4](../../../openspec/specs/performance/spec.md#L38) | P | Aucune suppression d’isolation, d’échec fermé ou d’audit dans le chemin optimisé. |
| [performance #5](../../../openspec/specs/performance/spec.md#L47) | ND | Perte/péremption et repli source observés sans résultat erroné ou obsolète déclaré courant. |
| [resilience #1](../../../openspec/specs/resilience/spec.md#L8) | P | Panne optionnelle injectée sur runtime réel, reste disponible si invariants conservés ; état et reprise observés. |
| [resilience #2](../../../openspec/specs/resilience/spec.md#L17) | P | Signature/contexte/contrôle invérifiable : refus sur HTTP/jobs et aucune readiness permissive. |
| [resilience #3](../../../openspec/specs/resilience/spec.md#L26) | ND | N01 : décision persistante, effets réconciliés, admissions bloquées, audit et réactivation explicite sans faux succès. |
| [service-objectives #1](../../../openspec/specs/service-objectives/spec.md#L10) | P | Objectif lié à version/périmètre/seuil/méthode/période, valeur non inventée par test local. |
| [service-objectives #2](../../../openspec/specs/service-objectives/spec.md#L21) | P | Rapport hors profil informatif ; aucune extrapolation d’un résultat ou d’une borne PZT à tout Pixs. |
| [service-objectives #3](../../../openspec/specs/service-objectives/spec.md#L32) | ND | Campagne synthétique avec versions/charge/méthode, mesure/seuil/écart ; insatisfaction explicitement remontée. |

Voir [audit individuel et limites des preuves](../archive/2026-10-18-define-first-installable-pbo-profile/audit-ne-94.json) et [rapport d’audit](../../../reports/audit-ne-94-2026-10-17/RAPPORT.md). Les tâches de réalisation restent non cochées.

## Dépendances après audit transversal P0

[C04](../archive/2026-10-21-integrate-runtime-authorization-and-super-admin/proposal.md), [C06](../add-protected-core-http-commands-and-queries/proposal.md), [C08](../add-installation-and-first-configuration/proposal.md), [C09](../add-reference-worker-scheduler-and-event-delivery/proposal.md), [C10](../enforce-core-data-governance-and-lifecycle/proposal.md), [C12](../complete-shared-ui-i18n-and-accessibility/proposal.md), [C13](../add-initial-administration-panel/proposal.md), [C14](../add-essential-pbo-pzt-and-dns-modules/proposal.md), [C15](../add-runtime-observability-and-operations/proposal.md), [C16](../add-upgrade-backup-and-restore-contracts/proposal.md), [C18](../build-first-pbo-pfo-debian-package/proposal.md), [N01](../add-pbo-security-quarantine-and-revocation/proposal.md), [N03](../archive/2026-10-20-add-p0-artifact-trust-and-preinstallation-verification/proposal.md), [N04](../define-p0-web-serving-and-security-boundary/proposal.md), [N05](../add-p0-post-restore-reconciliation-and-readmission/proposal.md), [N06](../add-minimal-p0-contract-conformance-kit/proposal.md).

Les conditions d’activation et la construction des résultats sont séparées de cet ordre de préparation ; aucun cycle inverse vers la recette finale.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

### T01 — Confiance avant première installation

C19 réalise tardivement les vérifications nécessaires avant installation par C17. N03 dédié validé ; déplacer les contrats/vérificateurs précoces, conserver publication finale C19.

Contrôles à intégrer : Canal interdit et signature absente/expirée/révoquée refusés avant installation ; Révocation vérifiable publication indisponible ; Paquet qualifié immuable et révalidation si octets ou identité changent.

### T02 — PBO/PFO réellement servi par le paquet

Le serveur/bundle/routage et la frontière HTTP distribuée ne sont pas détaillés par un propriétaire commun. N04 dédié et deltas ciblés validés ; décisions de serveur/session/transport encore ouvertes.

Contrôles à intégrer : Navigation directe du shell via service livré ; Erreur API sans fallback HTML ; Hôtes/origines/en-têtes non fiables, CSRF si cookie ; Management et rôles non publics.

### T03 — Réadmission après état restauré

La restauration cohérente de données ne prouve ni fraîcheur de révocations/incidents ni admissibilité des effets différés. N05 dédié et delta ciblé validés ; faits nécessaires et revalidation détaillée à définir avant code.

Contrôles à intégrer : Snapshot antérieur à révocation/rotation/incident ; Effet déjà engagé dont réponse perdue ; Marqueur externe incohérent ; Interruption puis reprise de réconciliation sans réémission automatique.

### T04 — Kit de conformité versus recette finale

C17 consomme/agrège des suites ; kit réutilisable minimal non détaillé et O22 complet tirerait SDK hors profil. N06 dédié validé ; réutiliser validateurs/exemple, C17 garde campagne finale.

Contrôles à intégrer : Preuve absente/expirée/mauvaise version refusée ; Authentification de preuve par exécuteur réel, pas par manifest ; Exemple P0 synthétique hors dépendances de production.

### T14 — PZT/DNS gérés sans exécution PA

La table 193 clauses reste conditionnelle et exige revue par rôle avant adoption ; classement exécutant ne retire pas les clauses PBO de gestion. Conserver C14 comme propriétaire, contrats/schémas/valeurs administrées explicités avant code ; aucun nouveau change exécutant sélectionné.

Contrôles à intégrer : Modules essentiels présents même réseau désactivé ; État souhaité distinct de mesure/appliqué ; Suffixe/droits/conflits des données gérées conformes ; Aucune publication DNS/réseau ni modification hôte inventée.

### T15 — Langues, thèmes et accessibilité de tous les parcours

Les parcours CLI, erreurs API, management et secours font aussi partie des textes utilisateur ; couverture ne se limite pas à la page du shell. Compléter la matrice C12/C17 et les contrats de messages ; codes stables non localisés.

Contrôles à intégrer : Deux navigateurs déclarés, clavier/zoom/lecteur d’écran ; Erreurs et confirmations d’installation/exploitation localisées ; Thème/session/tenant sans fuite d’état.

### T16 — Options, profils structurels et renvois Bulk

Un rattachement à un lot P0 n’active pas tout le domaine : Bulk, LDAP, flags avancés, quotas, SDK, sandbox et intégrité avancée restent conditionnés. Déclarer sélection/absence et maintenir les profils structurels existants ; ne pas traiter la non-sélection comme dispense d’une clause applicable.

Contrôles à intégrer : Absent représenté sans readiness fictive ; Contrat consommé réutilisé sans activer tout le catalogue ; Aucun code distant ni composant DEVELOPMENT en production ; Pas de promesse universelle de performance/HA.

### T17 — Reproductibilité, versions et dossier de livraison

Les pins observés et unités vertes ne valent pas qualification officielle du graphe ou du paquet ; signatures finales ne doivent pas modifier l’objet déjà qualifié. Contrôles officiels/compatibilité avant build puis sur l’artefact final ; aucune version actualisée ou dépendance installée pendant l’audit.

Contrôles à intégrer : Deux builds contrôlés et graphe identique ; Identité de l’artefact de recette égale à celle livrée ; Budgets/support déclarés avec preuves et limites ; Strict global exit réel conservé, warnings non masqués.

Voir [audit transversal durable](../archive/2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.
