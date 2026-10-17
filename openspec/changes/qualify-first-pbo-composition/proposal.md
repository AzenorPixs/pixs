# C17 — Recette et preuve de conformité P0

## Pourquoi

Le kit valide des manifests locaux et le noyau contrôle des attestations fournies ; aucune recette complète de l’artefact P0 initial n’est établie.

## Modifications proposées

Après construction du paquet C18, exécuter séparément unités, intégrations PostgreSQL réelles, conformité versionnée et parcours navigateur sur la composition distribuée ; authentifier les attestations, qualifier le graphe Django/Python courant et produire la preuve versionnée avec limites. C19 clôt ensuite les contrôles de distribution signée.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions de profil proposées dans C00.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- [add-pbo-security-quarantine-and-revocation](../add-pbo-security-quarantine-and-revocation/proposal.md) — dépendance explicitée après audit du 17 octobre 2026.

- `integrate-runtime-authorization-and-super-admin`.
- `add-protected-core-http-commands-and-queries`.
- `add-installation-and-first-configuration`.
- `add-reference-worker-scheduler-and-event-delivery`.
- `enforce-core-data-governance-and-lifecycle`.
- `complete-shared-ui-i18n-and-accessibility`.
- `add-initial-administration-panel`.
- `add-essential-pbo-pzt-and-dns-modules`.
- `add-runtime-observability-and-operations`.
- `add-upgrade-backup-and-restore-contracts`.
- `build-first-pbo-pfo-debian-package`.

## Impact

Périmètre de réalisation futur : Après C18, qualifier la composition réellement distribuée. Authentifier les preuves émises hors manifest par les suites versionnées ; distinguer unités, intégration réelle, conformité et manuel. Relier chaque scénario applicable à un verdict/version/artefact ; dimensions inconnues explicites, sans certificat global.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Chaque exigence/scénario applicable dispose d’un verdict et d’une preuve actuelle ; preuves négatives sécurité/tenant/reprise ; versions officielles et métadonnées revérifiées avant release ; strict OpenSpec avec exit natif rapporté ; objectifs déclarés mesurés.

## Barrière de conception

Versions actuelles et métadonnées officielles à vérifier avant qualification ; politique des quatre avertissements stricts existants à traiter sans masquer exit 1 ni réécrire le canon hors demande.

## Dépendances après audit transversal P0

[C04](../integrate-runtime-authorization-and-super-admin/proposal.md), [C06](../add-protected-core-http-commands-and-queries/proposal.md), [C08](../add-installation-and-first-configuration/proposal.md), [C09](../add-reference-worker-scheduler-and-event-delivery/proposal.md), [C10](../enforce-core-data-governance-and-lifecycle/proposal.md), [C12](../complete-shared-ui-i18n-and-accessibility/proposal.md), [C13](../add-initial-administration-panel/proposal.md), [C14](../add-essential-pbo-pzt-and-dns-modules/proposal.md), [C15](../add-runtime-observability-and-operations/proposal.md), [C16](../add-upgrade-backup-and-restore-contracts/proposal.md), [C18](../build-first-pbo-pfo-debian-package/proposal.md), [N01](../add-pbo-security-quarantine-and-revocation/proposal.md), [N03](../add-p0-artifact-trust-and-preinstallation-verification/proposal.md), [N04](../define-p0-web-serving-and-security-boundary/proposal.md), [N05](../add-p0-post-restore-reconciliation-and-readmission/proposal.md), [N06](../add-minimal-p0-contract-conformance-kit/proposal.md).

Les conditions d’activation et la construction des résultats sont séparées de cet ordre de préparation ; aucun cycle inverse vers la recette finale.
