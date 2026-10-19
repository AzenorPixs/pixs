# Conception — Z26

## Statut

PRÉPARATION_DOCUMENTAIRE_CONDITIONNELLE. Le dossier est demandé ; ses choix encore ouverts et son implémentation ne sont pas approuvés implicitement. La présence des fichiers ne signifie pas prêt à coder.

## Contexte actuel

Les contrats PZT et leurs décisions sont spécifiés ; le README ne revendique pas de réseau livré. Les clauses de gestion PBO essentielles restent distinctes des rôles réseau activés et des auxiliaires spécialisés.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

Sources et périmètres consultés :

- [README.md](../../../README.md).
- [openspec/specs/pzt/spec.md](../../specs/pzt/spec.md).
- [TECHNICAL.md](../../../TECHNICAL.md).

## Architecture et frontières

Séparer contrôle métier PBO/Django/PostgreSQL, propriétaire réseau pzt-daemon et adapters système. Implémenter le rôle précisément désigné par les contrats sources, avec schémas fermés, versions et contrôles courants ; conserver toutes bornes, unités, conditions de reprise et alternatives rejetées. La cryptographie WireGuard n’est pas réimplémentée. Les bibliothèques de transport, sources de temps et adapters sont qualifiés, sans confiance supposée.

Périmètre propre à ce lot : Recettes contrat/sécurité/reprise/ressources/isolation/autorité/transport/administration A05b–A12g ; qualification initiale sans passerelle, puis profils suivants.

## Choix déjà fixés et alternatives

Les décisions validées dans les contrats sources sont conservées, y compris formats, algorithmes, valeurs, rôles et alternatives rejetées. Elles ne sont pas rouvertes sous prétexte d’un nouveau dossier. Les plafonds d’un auxiliaire, collecteur, validateur ou travail ne deviennent pas un budget général du PA/PBO.

Les modalités concrètes encore ouvertes ne reçoivent pas de valeur de défaut inventée. Une bibliothèque, un provider ou une dépendance présent dans DEVOPS n’est ni sélectionné ni qualifié. Les références normatives complètes sont dans requirements.md ; les mentions historiques qu’elles contiennent ne décrivent pas des effets réalisés pendant cette préparation.

## Barrières de conception avant réalisation

Composition de recette, OS/CPU/providers/charges et scénarios applicables ; passage au profil passerelle seulement après première qualification du socle.

Ces barrières n’empêchent pas la rédaction conditionnelle du dossier. Avant tout code, les choix ayant un impact réel sur sécurité, périmètre, compatibilité, exploitation ou ressources devront être soumis avec conséquences et recommandation ; pour PA/PZT, respecter TECHNICAL §45.4 et ses lots de trois arbitrages. Les paramètres déjà décidés sont à qualifier, pas à remplacer par une nouvelle décision supposée.

## Dépendances et interfaces

- [qualify-pa-platforms-and-r01-r68-matrix](../qualify-pa-platforms-and-r01-r68-matrix/proposal.md).
- [qualify-first-pbo-composition](../qualify-first-pbo-composition/proposal.md).
- [publish-first-qualified-pbo-release](../publish-first-qualified-pbo-release/proposal.md).
- [add-pzt-wireguard-local-transport-and-filtering](../add-pzt-wireguard-local-transport-and-filtering/proposal.md).
- [add-pzt-network-mandates-and-fail-closed-revocation](../add-pzt-network-mandates-and-fail-closed-revocation/proposal.md).
- [add-pzt-authoritative-control-and-signed-receipts](../add-pzt-authoritative-control-and-signed-receipts/proposal.md).
- [add-pzt-private-address-plan-and-ipv6-lifecycle](../add-pzt-private-address-plan-and-ipv6-lifecycle/proposal.md).
- [add-pzt-managed-dns-service-and-pa-adapters](../add-pzt-managed-dns-service-and-pa-adapters/proposal.md).
- [add-pzt-public-control-contracts-and-state-streams](../add-pzt-public-control-contracts-and-state-streams/proposal.md).
- [add-pzt-path-discovery-and-encrypted-relays](../add-pzt-path-discovery-and-encrypted-relays/proposal.md).
- [add-pzt-service-identities-and-tpm-attestation](../add-pzt-service-identities-and-tpm-attestation/proposal.md).
- [add-pzt-tls-policy-and-bounded-cipher-migration](../add-pzt-tls-policy-and-bounded-cipher-migration/proposal.md).
- [add-pzt-operational-certificate-renewal](../add-pzt-operational-certificate-renewal/proposal.md).
- [add-pzt-ca-hierarchy-rotation-and-recovery](../add-pzt-ca-hierarchy-rotation-and-recovery/proposal.md).
- [add-pzt-offline-root-backup-and-recovery](../add-pzt-offline-root-backup-and-recovery/proposal.md).
- [add-pzt-monotonic-witness-and-key-sanitation](../add-pzt-monotonic-witness-and-key-sanitation/proposal.md).
- [add-pzt-evidence-dossier-and-bounded-validation](../add-pzt-evidence-dossier-and-bounded-validation/proposal.md).
- [add-pzt-proof-admission-and-attempt-reconciliation](../add-pzt-proof-admission-and-attempt-reconciliation/proposal.md).
- [add-pzt-qualified-time-and-freshness-decisions](../add-pzt-qualified-time-and-freshness-decisions/proposal.md).
- [add-pzt-isolated-time-helper-and-ipc](../add-pzt-isolated-time-helper-and-ipc/proposal.md).
- [add-pzt-durable-helper-state-and-writer-exclusion](../add-pzt-durable-helper-state-and-writer-exclusion/proposal.md).
- [add-pzt-bounded-telemetry-export-and-retention](../add-pzt-bounded-telemetry-export-and-retention/proposal.md).
- [add-pzt-telemetry-purge-jobs-and-leases](../add-pzt-telemetry-purge-jobs-and-leases/proposal.md).
- [add-pzt-canonical-purge-manifests-and-integrity](../add-pzt-canonical-purge-manifests-and-integrity/proposal.md).
- [add-pzt-controlled-manifest-incident-rearm](../add-pzt-controlled-manifest-incident-rearm/proposal.md).
- [add-pzt-rearm-status-stream-and-reconciliation](../add-pzt-rearm-status-stream-and-reconciliation/proposal.md).
- [add-pzt-pa-admission-and-ephemeral-peer-generation](../add-pzt-pa-admission-and-ephemeral-peer-generation/proposal.md).

Qualifier d’abord le socle sans passerelle. Z08 est préparé séparément et sa recette vient après cette première preuve ; une seconde recette peut alors intégrer le profil passerelle.

Les dépendances sont des contrats et preuves attendus. Un dossier créé ne signifie pas que sa dépendance est exécutée, disponible ou autorisée à démarrer. Les interfaces intermédiaires restent explicitement incomplètes tant que les obligations manquent.

## Vérification future

Bornes exactes et juste au-delà, types/champs étrangers, rôle/contexte/mandat inadmissibles, échéance/révocation, concurrence, réponse perdue, crash/reprise, état ancien et ressources réellement libérées. Mesurer seulement le traitement concerné et ne pas extrapoler ses plafonds au PA/PBO entier.

Sortie du lot : Preuves actuelles par scénario applicable ; valeurs validées conservées ; alternatives rejetées non activées ; pas de recette de passerelle avant socle.

Exercer tous les scénarios et clauses applicables des blocs sources, y compris renvois normatifs ; un scénario non applicable doit être motivé par le profil réel. Les contrôles applicatifs suivent l’exception Super Admin du canon dans son seul périmètre, sans fabriquer audit, mesure, signature ou effet absent.

## Migrations, reprise et arrêt

Aucun schéma ni état runtime modifié ici. Toute réalisation ultérieure qui persiste des données/états doit préciser propriétaire, contrat de migration, concurrence, reprise, durabilité et compensation/restauration. Aucun retour arrière destructeur, remise à zéro, arrêt de service ou changement de droits implicites.

## Limites du dossier

Pas de PASS actuel ni d’achèvement produit revendiqué. L’autorisation de préparation ne permet ni d’activer la capacité dans P0 ni d’utiliser un compte connecté, publier un artefact ou envoyer une notification réelle.
