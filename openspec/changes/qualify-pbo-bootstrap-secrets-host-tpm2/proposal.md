# Protection et reprise des secrets d’amorçage PBO

## Why

C01, archivé le 19 octobre 2026, fournit le transport `LoadCredentialEncrypted`, l’identité native, l’audit et la rotation contrôlée. Son harnais utilise des fixtures publiques avec `--with-key=null` : il ne qualifie ni le chiffrement de production ni une reprise après perte de machine. Le développeur a retenu le 19 octobre 2026 une protection liée au TPM2 et à l’hôte lorsque le matériel le permet, avec récupération testée.

## What Changes

- Spécifier le mode combiné `host+tpm2`, ses préconditions et l’absence de dégradation automatique lorsque le TPM est indisponible.
- Déclarer la politique de démarrage, ses mises à jour et la qualification des plateformes réellement retenues.
- Prévoir une récupération protégée indépendante du TPM d’origine, par réémission ou reprovisionnement autorisé, puis chiffrement pour le nouvel hôte.
- Ajouter les critères de preuve avant admission en production du profil local, sans confondre ces preuves futures et celles de C01.

## Capabilities

### New Capabilities

Aucune nouvelle capacité : les contrats existants restent propriétaires des secrets, de la reprise et de la composition.

### Modified Capabilities

- `secrets-providers` : protection combinée, préconditions matérielles, politique de démarrage et qualification cryptographique.
- `backup-disaster-recovery` : protection du secours, perte du TPM d’origine et réadmission des consommateurs.
- `reference-composition` : preuve de protection et de récupération avant production du profil local.

Les exigences ajoutées sont proposées dans `specs/` de ce change. Le canon courant n’est pas synchronisé pendant cette préparation.

## Impact

Préparation documentaire explicitement demandée le 19 octobre 2026. Aucun code, test produit, clé, secret réel, unité systemd, paramètre TPM/PCR, paquet, dépendance ou service n’est créé ou modifié. Aucun Git, archivage ou déploiement n’est engagé. C01 reste archivé ; CISMP3 reste arrêté.

La réalisation future réutilise le provider C01 et complète les contrats d’installation C08, de restauration C16/N05 et les preuves de packaging/recette C18/C17/C19. Le coffre distribué est préparé séparément dans [add-distributed-runtime-secret-vault](../add-distributed-runtime-secret-vault/proposal.md) ; il n’est pas requis pour le profil initial local.
