# Exigences de réalisation — C16

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 adopté le 18 octobre 2026 et intégré au canon apporte les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| artifact-publication / 8 | [Canaux comme contextes de confiance distincts](../../specs/artifact-publication/spec.md#L8) | ND | Artefact du mauvais canal |
| artifact-publication / 17 | [Immuabilité et corrélation des corrections](../../specs/artifact-publication/spec.md#L17) | ND | Écrasement d'un artefact publié |
| artifact-publication / 26 | [Identité vérifiable avant installation](../../specs/artifact-publication/spec.md#L26) | ND | Emprunte discordante |
| artifact-publication / 35 | [Signature, provenance et inventaire bloquants](../../specs/artifact-publication/spec.md#L35) | ND | Signature révoquée |
| artifact-publication / 44 | [Autorités distinctes et gestion des clés](../../specs/artifact-publication/spec.md#L44) | ND | Dépôt de publication indisponible |
| backup-disaster-recovery / 8 | [Stratégie déclarée par déploiement](../../specs/backup-disaster-recovery/spec.md#L8) | ND | Procédure sans objectifs déclarés |
| backup-disaster-recovery / 17 | [Périmètres de sauvegarde distincts](../../specs/backup-disaster-recovery/spec.md#L17) | ND | Sauvegarde partielle |
| backup-disaster-recovery / 26 | [Restauration cohérente et réapplication des gouvernances](../../specs/backup-disaster-recovery/spec.md#L26) | ND | Objet restauré après suppression validée |
| backup-disaster-recovery / 35 | [Tests de restauration isolés et preuves](../../specs/backup-disaster-recovery/spec.md#L35) | ND | Démarrage après restauration |
| backup-disaster-recovery / 44 | [Restauration destructive autorisée et auditée](../../specs/backup-disaster-recovery/spec.md#L44) | ND | Suppression implicite refusée |
| compatibility / 8 | [Contraintes de version déclarées et vérifiées](../../specs/compatibility/spec.md#L8) | P | Contrainte insatisfaite à l'activation |
| compatibility / 17 | [Aucune compatibilité présumée](../../specs/compatibility/spec.md#L17) | P | Version supérieure non testée |
| compatibility / 26 | [Matrice de compatibilité globale](../../specs/compatibility/spec.md#L26) | P | État bloqué déterministe |
| compatibility / 35 | [Compatibilité déclarative distincte de la conformité comportementale](../../specs/compatibility/spec.md#L35) | P | Déclaration sans conformité |
| compatibility / 44 | [Coexistence pendant les montées de version](../../specs/compatibility/spec.md#L44) | P | Suppression prématurée |
| compatibility / 123 | [Responsabilités de l'appelant et du noyau pour les preuves](../../specs/compatibility/spec.md#L123) | P | Preuve authentifiée par l'appelant |
| data-governance / 8 | [Application de l'exception Super Admin](../../specs/data-governance/spec.md#L8) | P | Dérogation de gouvernance dans un tenant accordé |
| data-governance / 18 | [Profil de gouvernance versionné par composant](../../specs/data-governance/spec.md#L18) | P | Flux sortant sans consommateur refusé |
| data-governance / 27 | [Classification restrictive par défaut](../../specs/data-governance/spec.md#L27) | P | Export non classifié refusé |
| data-governance / 38 | [Demandes relatives aux données tracées](../../specs/data-governance/spec.md#L38) | P | Effacement propagé |
| data-lifecycle / 8 | [Application de l'exception Super Admin](../../specs/data-lifecycle/spec.md#L8) | P | Purge demandée malgré un legal hold |
| data-lifecycle / 18 | [Dimensions et états distincts](../../specs/data-lifecycle/spec.md#L18) | P | Suppression logique tracée ; Vocabulaire commun de rétention fermé |
| data-lifecycle / 43 | [Purge autorisée, auditée et idempotente](../../specs/data-lifecycle/spec.md#L43) | P | Purge prématurée refusée |
| data-lifecycle / 52 | [Tombstones contre la résurrection](../../specs/data-lifecycle/spec.md#L52) | P | Restauration sans résurrection |
| deb-package / 8 | [Paquet corrélé à la release](../../specs/deb-package/spec.md#L8) | ND | Version de paquet incohérente ; Deux paquets indépendants |
| deb-package / 22 | [Configuration et secrets hors paquet](../../specs/deb-package/spec.md#L22) | ND | Secret trouvé dans le paquet |
| deb-package / 31 | [Services alignés sur le lifecycle Pixs](../../specs/deb-package/spec.md#L31) | ND | Redémarrage par le gestionnaire de services |
| deb-package / 40 | [Mise à niveau du paquet sous validation](../../specs/deb-package/spec.md#L40) | ND | Mise à niveau interrompue |
| deb-package / 49 | [Aucune installation de code distant implicite](../../specs/deb-package/spec.md#L49) | ND | Téléchargement proposé à l'installation |
| deb-package / 58 | [Distribution Debian indépendante PA et PBO PFO](../../specs/deb-package/spec.md#L58) | ND | Distribution Debian indépendante PA et PBO PFO |
| deb-package / 67 | [Quatre binaires dans le paquet PA](../../specs/deb-package/spec.md#L67) | ND | Quatre binaires dans le paquet PA |
| lifecycle / 8 | [États de cycle de vie distincts](../../specs/lifecycle/spec.md#L8) | P | États non confondus |
| lifecycle / 17 | [Transitions autorisées et refusées](../../specs/lifecycle/spec.md#L17) | P | Désactivation sans perte et purge explicite |
| lifecycle / 26 | [Ordre déterministe des hooks](../../specs/lifecycle/spec.md#L26) | P | Double résolution identique |
| lifecycle / 35 | [Idempotence des opérations](../../specs/lifecycle/spec.md#L35) | P | Rejeu sans double effet |
| lifecycle / 44 | [Diagnostic des échecs](../../specs/lifecycle/spec.md#L44) | P | Activation invalide bloquée |
| migrations / 8 | [Contrat de migration](../../specs/migrations/spec.md#L8) | P | Migration sans version cible |
| migrations / 17 | [Planification et ordre déterministes](../../specs/migrations/spec.md#L17) | P | Deux migrations concurrentes |
| migrations / 26 | [Compatibilité pendant l'application](../../specs/migrations/spec.md#L26) | P | Coexistence pendant migration |
| migrations / 35 | [Reprise idempotente](../../specs/migrations/spec.md#L35) | P | Interruption puis reprise |
| migrations / 44 | [Contraction contrôlée](../../specs/migrations/spec.md#L44) | P | Contraction prématurée |
| modules / 8 | [Manifest lisible obligatoire](../../specs/modules/spec.md#L8) | P | Manifest incomplet |
| modules / 17 | [Frontière API publique et privée](../../specs/modules/spec.md#L17) | P | Accès à une API non déclarée |
| modules / 26 | [Propriété des données et migrations associées](../../specs/modules/spec.md#L26) | P | Changement de schéma non migré |
| modules / 35 | [Chargement contrôlé déterministe](../../specs/modules/spec.md#L35) | P | Cycle de dépendances |
| modules / 44 | [Propriété des contributions frontend modulaires](../../specs/modules/spec.md#L44) | P | Sous-module autonome intégré |
| observability / 8 | [Signaux structurés et corrélés](../../specs/observability/spec.md#L8) | P | Corrélation bout en bout |
| observability / 17 | [Santé distinguée et sondes bornées](../../specs/observability/spec.md#L17) | P | Dépendance optionnelle dégradée |
| observability / 26 | [Objectifs de service déclarés](../../specs/observability/spec.md#L26) | P | Objectif sans méthode de mesure |
| observability / 38 | [Rétention et minimisation séparées](../../specs/observability/spec.md#L38) | P | Accès inter-tenant tracé |
| operations / 8 | [Application de l'exception Super Admin](../../specs/operations/spec.md#L8) | P | Intervention de secours pendant une maintenance |
| operations / 17 | [Interface de management distincte et non publique](../../specs/operations/spec.md#L17) | P | Façades convergeant sur le même contrat |
| operations / 26 | [Opérations persistantes avec plan et idempotence](../../specs/operations/spec.md#L26) | P | Rejeu d'une opération annulée |
| operations / 35 | [Sorties sans secret et codes stables](../../specs/operations/spec.md#L35) | P | Commande non autorisée |
| operations / 44 | [État de maintenance avec drainage borné](../../specs/operations/spec.md#L44) | P | Requête reçue pendant le drainage |
| operations / 53 | [Health, diagnostic et audit opérateur](../../specs/operations/spec.md#L53) | P | Réparation via le diagnostic |
| operations / 62 | [Maintenance hiérarchisée](../../specs/operations/spec.md#L62) | P | Maintenance d'une route |
| release-management / 8 | [Définition et support d'une release](../../specs/release-management/spec.md#L8) | ND | Release sans déclaration de support |
| release-management / 17 | [Chemin de migration vérifiable](../../specs/release-management/spec.md#L17) | ND | Saut non prouvé |
| release-management / 26 | [Mise à niveau orchestrée par prévalidations](../../specs/release-management/spec.md#L26) | ND | Étape de prévalidation échouée |
| release-management / 35 | [Coexistence transitoire N et N+1](../../specs/release-management/spec.md#L35) | ND | Contraction pendant la fenêtre |
| release-management / 44 | [Retour arrière soumis à la matrice](../../specs/release-management/spec.md#L44) | ND | Retour arrière non garanti |
| release-management / 55 | [Activation, retrait et instance non valide](../../specs/release-management/spec.md#L55) | ND | Instance échouant aux contrôles |

## Empreintes SHA-256 du canon

- `openspec/specs/artifact-publication/spec.md` : `7888cada73c3beff836fe2bd6dd6a62b166af317e7036680fb6a1f9e248a5b1f`.
- `openspec/specs/backup-disaster-recovery/spec.md` : `3b129f2e8fd899d2e1992296d7c5c6a93b2336873335584fa837270ce4545954`.
- `openspec/specs/compatibility/spec.md` : `aee6de57607e95e8442b59155cf893f4ef7454db6a0ba60fbfbd9abe360eb544`.
- `openspec/specs/data-governance/spec.md` : `85c5176f49270a9eb45a51329fc200f8d1cb293bfa6bc93e62eb7fe88999ddfe`.
- `openspec/specs/data-lifecycle/spec.md` : `a3498cc4d3622d569fc9e3f8251a5c5324a9b3d1c612fe014618146297083426`.
- `openspec/specs/deb-package/spec.md` : `46730b2c3505085325539b6ae2386806e5b59bb19aa46adf5f4571335d016e64`.
- `openspec/specs/lifecycle/spec.md` : `e4f8fb1bc340000c2fafed0a6d2862b9ad033d668e89691bfdeb3bf6dc8215d3`.
- `openspec/specs/migrations/spec.md` : `9b3ced385afbeaa7414a1d58752078482e57efa242064e21e7fb4b6fde451efe`.
- `openspec/specs/modules/spec.md` : `7ea4899dff68afd31f22a501e587da4dcad9c911d1689583672678cf108ff37b`.
- `openspec/specs/observability/spec.md` : `4793cf6252768ea2673a4eb843caf027fb850b586a8fcfee877b5d37d1e6ff98`.
- `openspec/specs/operations/spec.md` : `13835ff9b1d97cf4196a66f2f991f25f0d5c0357ccc54c7bcd1d56dffe38d5f1`.
- `openspec/specs/release-management/spec.md` : `0fd7fc3720214df3741c8eed94e0db460b2fd67101cee3310c08b952672f6e3f`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
