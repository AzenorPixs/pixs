# Exigences de réalisation — C19

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 proposé ajoute les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| artifact-publication / 8 | [Canaux comme contextes de confiance distincts](../../specs/artifact-publication/spec.md#L8) | ND | Artefact du mauvais canal |
| artifact-publication / 17 | [Immuabilité et corrélation des corrections](../../specs/artifact-publication/spec.md#L17) | ND | Écrasement d'un artefact publié |
| artifact-publication / 26 | [Identité vérifiable avant installation](../../specs/artifact-publication/spec.md#L26) | ND | Emprunte discordante |
| artifact-publication / 35 | [Signature, provenance et inventaire bloquants](../../specs/artifact-publication/spec.md#L35) | ND | Signature révoquée |
| artifact-publication / 44 | [Autorités distinctes et gestion des clés](../../specs/artifact-publication/spec.md#L44) | ND | Dépôt de publication indisponible |
| deb-package / 8 | [Paquet corrélé à la release](../../specs/deb-package/spec.md#L8) | ND | Version de paquet incohérente ; Deux paquets indépendants |
| deb-package / 22 | [Configuration et secrets hors paquet](../../specs/deb-package/spec.md#L22) | ND | Secret trouvé dans le paquet |
| deb-package / 31 | [Services alignés sur le lifecycle Pixs](../../specs/deb-package/spec.md#L31) | ND | Redémarrage par le gestionnaire de services |
| deb-package / 40 | [Mise à niveau du paquet sous validation](../../specs/deb-package/spec.md#L40) | ND | Mise à niveau interrompue |
| deb-package / 49 | [Aucune installation de code distant implicite](../../specs/deb-package/spec.md#L49) | ND | Téléchargement proposé à l'installation |
| deb-package / 58 | [Distribution Debian indépendante PA et PBO PFO](../../specs/deb-package/spec.md#L58) | ND | Distribution Debian indépendante PA et PBO PFO |
| deb-package / 67 | [Quatre binaires dans le paquet PA](../../specs/deb-package/spec.md#L67) | ND | Quatre binaires dans le paquet PA |
| release-management / 8 | [Définition et support d'une release](../../specs/release-management/spec.md#L8) | ND | Release sans déclaration de support |
| release-management / 17 | [Chemin de migration vérifiable](../../specs/release-management/spec.md#L17) | ND | Saut non prouvé |
| release-management / 26 | [Mise à niveau orchestrée par prévalidations](../../specs/release-management/spec.md#L26) | ND | Étape de prévalidation échouée |
| release-management / 35 | [Coexistence transitoire N et N+1](../../specs/release-management/spec.md#L35) | ND | Contraction pendant la fenêtre |
| release-management / 44 | [Retour arrière soumis à la matrice](../../specs/release-management/spec.md#L44) | ND | Retour arrière non garanti |
| release-management / 55 | [Activation, retrait et instance non valide](../../specs/release-management/spec.md#L55) | ND | Instance échouant aux contrôles |

## Empreintes SHA-256 du canon

- `openspec/specs/artifact-publication/spec.md` : `7888cada73c3beff836fe2bd6dd6a62b166af317e7036680fb6a1f9e248a5b1f`.
- `openspec/specs/deb-package/spec.md` : `46730b2c3505085325539b6ae2386806e5b59bb19aa46adf5f4571335d016e64`.
- `openspec/specs/release-management/spec.md` : `0fd7fc3720214df3741c8eed94e0db460b2fd67101cee3310c08b952672f6e3f`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
