# Conception — C17

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 formalise le profil ; ses précisions normatives restent proposées tant qu’elles ne sont pas approuvées/adoptées.

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

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Versions actuelles et métadonnées officielles à vérifier avant qualification ; politique des quatre avertissements stricts existants à traiter sans masquer exit 1 ni réécrire le canon hors demande.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

- [add-pbo-security-quarantine-and-revocation](../add-pbo-security-quarantine-and-revocation/proposal.md) — dépendance explicitée après audit du 17 octobre 2026.

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [integrate-runtime-authorization-and-super-admin](../integrate-runtime-authorization-and-super-admin/proposal.md).
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

Voir [audit individuel et limites des preuves](../define-first-installable-pbo-profile/audit-ne-94.json) et [rapport d’audit](../../../reports/audit-ne-94-2026-10-17/RAPPORT.md). Les tâches de réalisation restent non cochées.
