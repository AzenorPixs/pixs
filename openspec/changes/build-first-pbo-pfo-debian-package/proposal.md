# C18 — Paquet Debian et services

## Pourquoi

Aucun répertoire de packaging Debian initial ni paquet PBO/PFO qualifié n’est identifié ; le README déclare les distributions non livrées.

## Modifications proposées

Construire le paquet PBO/PFO indépendant, incluant PZT essentiel mais aucun binaire PA ; services par rôle, contenu immuable et configuration administrée séparée. Noms/versions à décider, aucune dépendance installée pour cet audit.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions de profil proposées dans C00.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- [add-pbo-security-quarantine-and-revocation](../add-pbo-security-quarantine-and-revocation/proposal.md) — dépendance explicitée après audit du 17 octobre 2026.

- `activate-reference-runtime-composition`.
- `add-installation-and-first-configuration`.
- `add-reference-worker-scheduler-and-event-delivery`.
- `compose-modular-frontend-with-core-api`.
- `add-initial-administration-panel`.
- `add-essential-pbo-pzt-and-dns-modules`.
- `add-runtime-observability-and-operations`.
- `add-upgrade-backup-and-restore-contracts`.

## Impact

Périmètre de réalisation futur : Construire depuis sources versionnées le paquet PBO/PFO incluant modules PZT/DNS mais aucun binaire PA ; services par rôle, code immuable et configuration administrée externe préservée. Installation, mise à niveau, désinstallation et purge explicite distinctes ; aucun code distant téléchargé implicitement.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Construire/install/mise à niveau/désinstallation sur environnement isolé ; configuration préservée et données non purgées ; pas de téléchargement implicite ; services avec même lifecycle ; qualification de l’artefact final en C17/C19, pas seulement des sources.

## Barrière de conception

Noms/versions du paquet et exécutables, architecture qualifiée, dépendances et comptes d’exécution ; qualification requise avant sélection d’outil supplémentaire.

## Dépendances après audit transversal P0

[C07](../activate-reference-runtime-composition/proposal.md), [C08](../add-installation-and-first-configuration/proposal.md), [C09](../add-reference-worker-scheduler-and-event-delivery/proposal.md), [C11](../compose-modular-frontend-with-core-api/proposal.md), [C13](../add-initial-administration-panel/proposal.md), [C14](../add-essential-pbo-pzt-and-dns-modules/proposal.md), [C15](../add-runtime-observability-and-operations/proposal.md), [C16](../add-upgrade-backup-and-restore-contracts/proposal.md), [N01](../add-pbo-security-quarantine-and-revocation/proposal.md), [N03](../add-p0-artifact-trust-and-preinstallation-verification/proposal.md), [N04](../define-p0-web-serving-and-security-boundary/proposal.md), [N05](../add-p0-post-restore-reconciliation-and-readmission/proposal.md).

Les conditions d’activation et la construction des résultats sont séparées de cet ordre de préparation ; aucun cycle inverse vers la recette finale.
