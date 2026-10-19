# Conception préparatoire — séparation amorçage et coffre distribué

## Statut et autorisation

PRÉPARATION_DOCUMENTAIRE, 19 octobre 2026. L’orientation et sa formalisation sont autorisées ; aucun provider supplémentaire n’est implémenté, installé ou activé. Les tâches restent non cochées. Aucun RUN de codage n’est repris.

## Couverture existante et manque constaté

| Source vérifiée | Couverture actuelle | Complément |
| --- | --- | --- |
| [secrets-providers](../../specs/secrets-providers/spec.md) | Références, identité, finalité/périmètre, credentials courts, rotation/révocation, audit, refus fermé | Séparation locale/distribuée et coffre indépendant de la base métier |
| [reference-composition](../../specs/reference-composition/spec.md) | Sélection explicite, capacités obligatoires, preuves et profil initial local | Condition d’admission d’un profil distribué avec coffre |
| [backup-disaster-recovery](../../specs/backup-disaster-recovery/spec.md) | Objectifs, périmètres, protection des références, restauration isolée et contrôlée | Application au coffre et à sa chaîne de déverrouillage, sans nouvel outil imposé |
| [TECHNICAL.md §21](../../../TECHNICAL.md#21-secrets) | Abstraction indépendante du mécanisme de stockage | Responsabilités du stockage d’exploitation et minimum local |

Les changes actifs consacrés au coffre natif, à LDAP ou aux clés PA/PZT ne préparent pas ce provider d’exploitation PBO. Le présent change complète le canon sans recréer ces domaines.

## Architecture retenue

Le plan d’amorçage conserve localement uniquement les credentials explicitement nécessaires au démarrage et à l’authentification initiale du workload. Pour le profil Debian retenu, il s’appuie sur C01 et sur [la protection host+tpm2 préparée séparément](../qualify-pbo-bootstrap-secrets-host-tpm2/proposal.md). L’inventaire doit justifier chaque secret local ; une indisponibilité du réseau ne permet pas de recopier le coffre entier sur les hôtes.

Le plan d’exploitation résout au runtime les références de secrets auprès d’un coffre dédié, séparé de la base métier Pixs. Ni son ouverture, ni son autorisation initiale, ni sa récupération ne nécessitent un secret conservé uniquement dans la base Pixs qu’ils doivent permettre d’ouvrir. Le coffre conserve ses propres mécanismes de stockage, de protection des clés, de sauvegarde et de reprise. L’indépendance ne signifie pas qu’un simple schéma SQL séparé suffit : la réalisation doit justifier les frontières de contrôle et les dépendances réelles. Elle n’impose pas un fournisseur matériel ou un backend précis par anticipation.

Le contrat `SecretProvider`, les références opaques et les contrats de consommation restent communs. LDAP peut fournir des identités ou groupes et Kerberos peut authentifier certains services ; ils ne remplacent pas le cycle de vie du coffre. Le choix de PostgreSQL comme autorité métier n’oblige pas à en faire le stockage du coffre ni à y placer ses clés de déverrouillage.

## Identité, droits et durée de vie

Chaque rôle/instance de service est authentifié avec des droits limités à ses références, finalités et périmètres autorisés. Un jeton administrateur global partagé entre web, workers et schedulers est incompatible avec cette séparation. L’identité de workload ne devient ni Subject métier ni Super Admin par sa seule existence.

Les credentials courts compatibles sont privilégiés conformément au canon, notamment les accès base dynamiques lorsque le provider retenu les permet. Les bornes de vie, renouvellement, révocation et arrêt des copies déjà consommées sont explicites ; la durée d’un cache ne prolonge pas une autorisation. Les paramètres et les capacités effectives des consommateurs seront qualifiés avant activation. Aucune valeur numérique de production n’est choisie ici.

## Protection et indisponibilité

Les accès réseau vérifient l’identité du coffre et la confidentialité/intégrité du transport. Le stockage du coffre, ses sauvegardes et ses clés de déverrouillage disposent de protections et d’accès séparés. La solution doit expliquer la perte/compromission des clés et le redémarrage sans dépendance circulaire ; HSM/KMS ou partage de secours ne sont pas sélectionnés implicitement.

Si le coffre est indisponible, une nouvelle résolution obligatoire échoue fermée. Une valeur déjà délivrée ne reste utilisable que dans ses bornes et sous les garanties de révocation réellement démontrées ; le mode dégradé doit expliciter cette limite. Il n’existe pas de repli implicite vers LDAP, une table métier Pixs, un fichier en clair ou une copie locale durable. Les consommateurs s’arrêtent ou perdent leur readiness selon leur contrat lorsque leurs garanties ne peuvent plus être tenues.

Un coffre réduit l’étendue et la durée d’exposition, mais ne garantit pas la confidentialité d’un secret déjà remis à un processus compromis. Les limites face aux administrateurs de l’hôte, aux dumps et à la lecture mémoire sont déclarées sans attribuer au produit une protection qu’il ne fournit pas.

## Audit, disponibilité et récupération

L’audit relie les résolutions, refus, rotations et révocations au workload, à la référence et à la corrélation sans valeur de secret. Le reçu et le sink suivent les contrats canoniques applicables ; un journal technique ou le simple retour d’une API ne remplace pas la preuve requise. L’audit d’amorçage C01 ne devient pas un second audit métier permanent.

Avant admission du profil distribué, la stratégie déclare disponibilité, sauvegarde/restauration du coffre, récupération des clés et du matériel d’amorçage, RPO/RTO et traitement des révocations postérieures aux snapshots. Elle teste perte d’instance, interruption réseau, expiration, révocation, redémarrage et restauration isolée. [C16](../add-upgrade-backup-and-restore-contracts/proposal.md) et [N05](../add-p0-post-restore-reconciliation-and-readmission/proposal.md) gardent leurs responsabilités de reprise/réadmission ; aucune dépendance inverse vers une recette finale n’empêche la préparation de ces contrats.

## Décisions ouvertes avant réalisation

Produit/version et backend du coffre ; identité initiale des workloads ; périmètres et droits par service ; méthode de protection/déverrouillage des clés ; durées et budgets ; topologie/haute disponibilité ; résidence/rétention ; procédure de récupération ; comportement des consommateurs et autorisations d’essais. Le développeur a validé l’architecture, pas le choix automatique d’OpenBao ou d’un outil supplémentaire.

Le profil initial local ne dépend pas de ce change. Une composition distribuée ne devient pas sélectionnée par sa préparation : sa recette et sa distribution, notamment [les compositions étendues](../qualify-selected-extended-pixs-compositions/proposal.md), devront consommer les preuves de ce coffre et des autres capacités effectivement retenues. La procédure de secours d’amorçage reste indépendante de la disponibilité du coffre qu’elle doit permettre de redémarrer.

## Sources primaires

Consultation du 19 octobre 2026 : [modèle de sécurité OpenBao](https://openbao.org/docs/internals/security/) pour les frontières de confiance, l’audit activé et les limites face à la mémoire compromise ; [moteur de secrets de bases de données](https://openbao.org/docs/secrets/databases/) pour les credentials dynamiques, baux et révocations. Ces capacités documentées ne prouvent ni sélection ni qualification d’une installation Pixs.
