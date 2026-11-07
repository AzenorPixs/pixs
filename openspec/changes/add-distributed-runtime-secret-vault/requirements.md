# Références normatives — add-distributed-runtime-secret-vault

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| secrets-providers | Références externes sans valeur persistée | 1 | secrets-providers-a6ed5fecbe42 |
| secrets-providers | Accès runtime associé à une identité de workload | 1 | secrets-providers-2ebbe664ce7a |
| secrets-providers | Rotation, durée de vie et révocation contrôlées | 1 | secrets-providers-d95db1d78a2e |
| secrets-providers | Audit minimisé et échec fermé | 1 | secrets-providers-75d3e201aebb |
| secrets-providers | Transport systemd C01 et identité effectivement vérifiée | 2 | secrets-providers-de5908d70afb |
| secrets-providers | Refus C01 sans preuve native d’identité | 2 | secrets-providers-f096e5cf3e07 |
| secrets-providers | Liaison contrôlée et paramètres C01 sans défaut implicite | 1 | secrets-providers-77e78278fe17 |
| secrets-providers | Bornes obligatoires de la politique C01 | 1 | secrets-providers-d82d3af0f697 |
| secrets-providers | Cycle de vie vérifiable des copies systemd chargées | 2 | secrets-providers-72ba32be80fa |
| secrets-providers | Arrêt et redémarrage des copies systemd chargées | 2 | secrets-providers-ee8b22a65e1f |
| secrets-providers | Résolution auditée et branchement runtime séparé | 1 | secrets-providers-fd1df4bff212 |
| secrets-providers | Gabarits purs et disponibilité runtime distincte | 1 | secrets-providers-8366b7e360b7 |
| secrets-providers | Résolution technique après INSTALLER explicitement autorisée | 2 | secrets-providers-96855a768511 |
| secrets-providers | Continuité auditée du démarrage avant PostgreSQL | 2 | secrets-providers-a5f58c6d6b90 |
| secrets-providers | Remise de connexion PBO indépendante de la base à ouvrir | 3 | secrets-providers-dbc3864ba45e |
| secrets-providers | Secrets Docker par fichiers versionnés | 3 | secrets-providers-2df55e1ad593 |
| zt-pki | PKI propre et autorités multiples | 1 | zt-pki-35b43ca99bc1 |
| zt-pki | PG propre et clés opérationnelles répliquées | 1 | zt-pki-4c7ec15b616c |
| zt-pki | Protection individualisée et habilitations séparées | 1 | zt-pki-eb43ece12358 |
| zt-pki | Émetteur unique et secours encadré | 1 | zt-pki-5dd5b9ed6de1 |
| zt-pki | ACME public et génération de clés | 1 | zt-pki-2ae6168f0a0c |
| zt-pki | Challenges et coordination ACME | 1 | zt-pki-e3e8cdbdb3dd |
| zt-pki | Renouvellement anticipé et déploiement vérifié | 1 | zt-pki-ba327c12b293 |
| zt-pki | Remise TLS ciblée aux RPZT | 1 | zt-pki-790b4d1f8594 |
| zt-pki | Récupération par autorité et racine distincte | 1 | zt-pki-829050040a60 |
| zt-pki | Confiance d'amorçage distincte et retrait vérifié | 2 | zt-pki-c23b35888a50 |
| auth-managed-kerberos | KZT obligatoire et backend OpenLDAP | 1 | auth-managed-kerberos-050d7fe34c83 |
| auth-managed-kerberos | Realm propre et mappings explicites | 1 | auth-managed-kerberos-7bb78778c4c7 |
| auth-managed-kerberos | Protection et récupération des clés Kerberos | 1 | auth-managed-kerberos-1760917ff34e |
| auth-managed-kerberos | Verrouillage cohérent du realm | 1 | auth-managed-kerberos-255d8bbfe611 |
| auth-managed-kerberos | Provisionnement progressif par profil | 1 | auth-managed-kerberos-1c0f0ee90eed |
| auth-managed-kerberos | Expiration stricte et état courant | 1 | auth-managed-kerberos-551806d8cd3f |
| auth-managed-kerberos | Temps et confiance inter-realms | 1 | auth-managed-kerberos-72a422092c18 |
| auth-managed-kerberos | Restauration sans résurrection | 1 | auth-managed-kerberos-2916ffe1ae32 |
| auth-managed-kerberos | Reconstruction complète en urgence critique | 3 | auth-managed-kerberos-9dec834a75dd |
| auth-managed-kerberos | État critique distinct du mode d'exploitation | 1 | auth-managed-kerberos-3ea4c587f7b3 |

### Référence courante secrets-providers-a6ed5fecbe42

Source : [secrets-providers](../../specs/secrets-providers/spec.md), ligne 11. SHA-256 : `a6ed5fecbe42fc76a68286a635d2296200dd519aafb86fe1a6902409db549ef2`.

Scénarios : Diagnostic de référence indisponible.

~~~~text
### Requirement: Références externes sans valeur persistée

La configuration, les manifests, les rapports, les diagnostics et les artefacts
MUST contenir uniquement des références de secrets autorisées. Une valeur de
secret, credential ou jeton MUST NOT être sérialisée, journalisée ou publiée.

#### Scenario: Diagnostic de référence indisponible

- **WHEN** un fournisseur ne peut pas résoudre une référence obligatoire
- **THEN** il signale la référence et l'erreur sans révéler de valeur attendue
~~~~

### Référence courante secrets-providers-2ebbe664ce7a

Source : [secrets-providers](../../specs/secrets-providers/spec.md), ligne 22. SHA-256 : `2ebbe664ce7acbb0358808565b9fa51ff5d548fa67b776cdce34f21303821246`.

Scénarios : Worker non autorisé.

~~~~text
### Requirement: Accès runtime associé à une identité de workload

Un SecretProvider MUST vérifier l'identité de workload, le composant, le tenant
ou scope lorsque requis, la finalité et la politique d'accès avant résolution.
Une référence valide MUST NOT donner accès à un secret hors du contexte autorisé.

#### Scenario: Worker non autorisé

- **WHEN** un worker demande une référence réservée au profil web
- **THEN** la résolution est refusée et auditée
~~~~

### Référence courante secrets-providers-d95db1d78a2e

Source : [secrets-providers](../../specs/secrets-providers/spec.md), ligne 33. SHA-256 : `d95db1d78a2ed0b7f094240bf3f89f9ddf1cab055485f144efda3e4eeca651a1`.

Scénarios : Secret tourné.

~~~~text
### Requirement: Rotation, durée de vie et révocation contrôlées

Le fournisseur MUST déclarer la durée de vie, la rotation, la révocation et le
comportement de rafraîchissement applicables. Une révocation MUST empêcher les
nouvelles utilisations dans le délai déclaré sans laisser un cache prolonger
silencieusement un accès interdit. Le fournisseur MUST privilégier des
credentials courts associés à une identité de workload ; un secret statique
MUST NOT être utilisé lorsqu'un credential court compatible est disponible.

#### Scenario: Secret tourné

- **WHEN** une référence est remplacée par une version rotée
- **THEN** les consommateurs autorisés rafraîchissent leur accès sans placer la valeur dans un artefact
~~~~

### Référence courante secrets-providers-75d3e201aebb

Source : [secrets-providers](../../specs/secrets-providers/spec.md), ligne 47. SHA-256 : `75d3e201aebbbce99043af412f747d338228c2b1ad1e7b62daf0ab63203d909c`.

Scénarios : Provider indisponible.

~~~~text
### Requirement: Audit minimisé et échec fermé

Les résolutions, refus, rotations et révocations MUST être auditables avec une
identité, une référence et une corrélation. Une indisponibilité ou une politique
non vérifiable MUST échouer fermé pour une capacité protégée.

#### Scenario: Provider indisponible

- **WHEN** un secret requis ne peut pas être résolu au démarrage
- **THEN** le composant concerné ne devient pas prêt
~~~~

### Référence courante secrets-providers-de5908d70afb

Source : [secrets-providers](../../specs/secrets-providers/spec.md), ligne 58. SHA-256 : `de5908d70afb5d452bb9e3ffa9a34eedb87080371287a4982edc27f43f1c40cc`.

Scénarios : Rôle différent du workload réel; Contexte tenant absent non transformé en permission.

~~~~text
### Requirement: Transport systemd C01 et identité effectivement vérifiée

Le provider C01 du profil Debian local MUST utiliser LoadCredentialEncrypted par service, hors Kernel, avec valeurs seulement dans le processus consommateur. Il MUST vérifier l’UID et le rattachement réel de son processus à l’unité autorisée avant résolution, puis appliquer la politique de confiance versionnée liant rôle, référence, finalité et périmètre.

#### Scenario: Rôle différent du workload réel

- **WHEN** une demande prétend appartenir au rôle web mais que l’identité native ne satisfait pas sa liaison autorisée
- **THEN** la résolution est refusée avant remise de valeur et le refus est audité

#### Scenario: Contexte tenant absent non transformé en permission

- **WHEN** la phase d’amorçage utilise le périmètre PLATFORM sans tenant_id ni scope_id
- **THEN** seules la politique et l’autorisation technique INSTALLER explicites peuvent admettre la référence
~~~~

### Référence courante secrets-providers-f096e5cf3e07

Source : [secrets-providers](../../specs/secrets-providers/spec.md), ligne 72. SHA-256 : `f096e5cf3e078689d4870f05faa2d36b09ee685bfeaec377f2985acc6194faf8`.

Scénarios : Rôle différent du workload réel; Contexte tenant absent non transformé en permission.

~~~~text
### Requirement: Refus C01 sans preuve native d’identité

Une variable d’environnement, un identifiant fourni par l’appelant ou la seule propriété d’un fichier MUST NOT constituer une identité ou une autorisation. Une preuve native indisponible MUST produire un refus fermé.

#### Scenario: Rôle différent du workload réel

- **WHEN** une demande prétend appartenir au rôle web mais que l’identité native ne satisfait pas sa liaison autorisée
- **THEN** la résolution est refusée avant remise de valeur et le refus est audité

#### Scenario: Contexte tenant absent non transformé en permission

- **WHEN** la phase d’amorçage utilise le périmètre PLATFORM sans tenant_id ni scope_id
- **THEN** seules la politique et l’autorisation technique INSTALLER explicites peuvent admettre la référence
~~~~

### Référence courante secrets-providers-77e78278fe17

Source : [secrets-providers](../../specs/secrets-providers/spec.md), ligne 86. SHA-256 : `77e78278fe173b8ffb934c999d66b3fa56613a8167d437b3d7409452fb5ead54`.

Scénarios : Politique incomplète.

~~~~text
### Requirement: Liaison contrôlée et paramètres C01 sans défaut implicite

Les références SecretReference existantes MUST rester opaques et inchangées. La politique C01 MUST déclarer explicitement l’identité et la version de politique, la référence et version du credential, son identifiant systemd, l’unité et l’UID autorisés, le rôle, la finalité et le périmètre. L’identifiant du credential MUST rester un nom autorisé sans chemin, traversée ou joker.

#### Scenario: Politique incomplète

- **WHEN** une identité, une version, une finalité ou une borne obligatoire manque ou est incohérente
- **THEN** la résolution refuse sans choix de valeur par défaut ni secret de substitution
~~~~

### Référence courante secrets-providers-d82d3af0f697

Source : [secrets-providers](../../specs/secrets-providers/spec.md), ligne 95. SHA-256 : `d82d3af0f697131bb1afcc54a837421b2c76d18e3935c814541733539ae5e4c7`.

Scénarios : Politique incomplète.

~~~~text
### Requirement: Bornes obligatoires de la politique C01

Les limites de taille, les bornes de validité, la durée de vie maximale, le délai maximal de révocation et le budget d’arrêt/redémarrage MUST être obligatoires et vérifiables, sans défaut numérique. Une valeur de secret MUST NOT être un paramètre distribué.

#### Scenario: Politique incomplète

- **WHEN** une identité, une version, une finalité ou une borne obligatoire manque ou est incohérente
- **THEN** la résolution refuse sans choix de valeur par défaut ni secret de substitution
~~~~

### Référence courante secrets-providers-72ba32be80fa

Source : [secrets-providers](../../specs/secrets-providers/spec.md), ligne 104. SHA-256 : `72ba32be80facb0e39d1f4f4bc9fe3a858764aa614e599343cf676885faa9917`.

Scénarios : Ancien consommateur encore actif; Nouvelle version au redémarrage.

~~~~text
### Requirement: Cycle de vie vérifiable des copies systemd chargées

Un secret absent, expiré, révoqué ou associé à une politique non vérifiable MUST être refusé. La durée de vie et le délai de révocation déclarés MUST être respectés par les nouvelles utilisations ; une copie ou un cache MUST NOT prolonger l’accès. Pour une copie déjà chargée, la rotation ou révocation MUST exiger l’arrêt attesté des consommateurs concernés avant remplacement puis redémarrage contrôlé dans les bornes déclarées.

#### Scenario: Ancien consommateur encore actif

- **WHEN** une version est révoquée et que l’arrêt de tous les consommateurs concernés n’est pas prouvé
- **THEN** aucune rotation achevée ni disponibilité conforme n’est annoncée

#### Scenario: Nouvelle version au redémarrage

- **WHEN** l’arrêt, le remplacement et le redémarrage contrôlés sont prouvés sous la politique courante
- **THEN** le consommateur utilise la nouvelle version et ne réutilise pas la copie antérieure
~~~~

### Référence courante secrets-providers-ee8b22a65e1f

Source : [secrets-providers](../../specs/secrets-providers/spec.md), ligne 118. SHA-256 : `ee8b22a65e1fa89e655a24509f32d00e72e2d138a6fc5fcf80d828189f8f0bd8`.

Scénarios : Ancien consommateur encore actif; Nouvelle version au redémarrage.

~~~~text
### Requirement: Arrêt et redémarrage des copies systemd chargées

Supprimer la source ou recharger seulement la configuration MUST NOT valoir révocation. Une garantie non prouvée MUST conserver le composant non prêt. La préférence canonique pour les credentials courts compatibles MUST rester applicable.

#### Scenario: Ancien consommateur encore actif

- **WHEN** une version est révoquée et que l’arrêt de tous les consommateurs concernés n’est pas prouvé
- **THEN** aucune rotation achevée ni disponibilité conforme n’est annoncée

#### Scenario: Nouvelle version au redémarrage

- **WHEN** l’arrêt, le remplacement et le redémarrage contrôlés sont prouvés sous la politique courante
- **THEN** le consommateur utilise la nouvelle version et ne réutilise pas la copie antérieure
~~~~

### Référence courante secrets-providers-fd1df4bff212

Source : [secrets-providers](../../specs/secrets-providers/spec.md), ligne 132. SHA-256 : `fd1df4bff2129a05e4bbc3f811afec592db149e3ccc92a8631c3d939af74e8c8`.

Scénarios : Provider disponible et P0 incomplet.

~~~~text
### Requirement: Résolution auditée et branchement runtime séparé

Le backend MUST produire les événements et vérifier les reçus d’audit requis avant remise d’une valeur, selon le journal d’amorçage autorisé ou le sink propriétaire applicable après reprise. Un callback retournant True MUST NOT prouver l’audit persistant. Les diagnostics MUST rester statiques sans valeur ni exception brute sensible.

#### Scenario: Provider disponible et P0 incomplet

- **WHEN** une résolution runtime conforme réussit mais que les autres obligations du profil ne sont pas prouvées
- **THEN** les gabarits préparatoires restent inchangés et aucune disponibilité globale P0 n’est annoncée
~~~~

### Référence courante secrets-providers-8366b7e360b7

Source : [secrets-providers](../../specs/secrets-providers/spec.md), ligne 141. SHA-256 : `8366b7e360b764927e5d5dd7c15279b63e810235d6843826c58bb28ee2608b45`.

Scénarios : Provider disponible et P0 incomplet.

~~~~text
### Requirement: Gabarits purs et disponibilité runtime distincte

Le branchement runtime MUST rester séparé de SettingsTemplate, build_settings_template et check_template, dont les contrats purs, secrets_resolved=False et ready=False MUST rester inchangés. La disponibilité du provider MUST NOT être présentée comme celle de la composition P0.

#### Scenario: Provider disponible et P0 incomplet

- **WHEN** une résolution runtime conforme réussit mais que les autres obligations du profil ne sont pas prouvées
- **THEN** les gabarits préparatoires restent inchangés et aucune disponibilité globale P0 n’est annoncée
~~~~

### Référence courante secrets-providers-96855a768511

Source : [secrets-providers](../../specs/secrets-providers/spec.md), ligne 150. SHA-256 : `96855a768511203e8ad492b3e089132e509aae208d564afc785c2d84871d6af3`.

Scénarios : Mode et workload courants autorisés; Mode ou finalité absent de la politique.

~~~~text
### Requirement: Résolution technique après INSTALLER explicitement autorisée

Après INSTALLER, le provider systemd C01 MUST résoudre les références uniquement pour les modes FIRST_CONFIGURATION, NORMAL ou MAINTENANCE expressément autorisés par une politique versionnée liant workload, UID, unité, rôle, finalité, scope, références, versions et bornes. Il MUST conserver les preuves natives, le transport LoadCredentialEncrypted et les règles de rotation/révocation. Un mode MUST NOT être réétiqueté INSTALLER.

#### Scenario: Mode et workload courants autorisés

- **WHEN** un workload dont les preuves natives sont valides demande une référence dans un mode, rôle et finalité autorisés par sa politique courante
- **THEN** la résolution suit cette politique et conserve ses contrôles de validité, de révocation et d’audit

#### Scenario: Mode ou finalité absent de la politique

- **WHEN** une référence existe mais que le mode, le workload ou la finalité ne correspond pas à la politique vérifiée
- **THEN** la remise de valeur est refusée sans secret ni repli vers INSTALLER
~~~~

### Référence courante secrets-providers-a5f58c6d6b90

Source : [secrets-providers](../../specs/secrets-providers/spec.md), ligne 164. SHA-256 : `a5f58c6d6b901e06b5b4d89055ce8320e9efe7e0ed2d234cabb2c8aa78c21369`.

Scénarios : Audit requis indisponible avant base; Crash pendant le relais vers C05.

~~~~text
### Requirement: Continuité auditée du démarrage avant PostgreSQL

Avant disponibilité de PostgreSQL, la résolution technique MUST disposer d’un audit durable indépendant de cette base, lié à l’invocation et au workload vérifiés. Après ouverture, le relais vers C05 MUST être idempotent et rapproché avant disponibilité applicative. Une preuve absente ou une issue inconnue MUST garder le composant non prêt. Cet audit MUST NOT conférer de droit métier ou R01.

#### Scenario: Audit requis indisponible avant base

- **WHEN** une résolution de démarrage ne peut pas confirmer son audit durable avant disponibilité de PostgreSQL
- **THEN** aucune valeur ni disponibilité applicative n’est annoncée

#### Scenario: Crash pendant le relais vers C05

- **WHEN** un démarrage reprend après un import partiel des événements de son invocation
- **THEN** il inspecte et réconcilie le relais sans événement dupliqué ni disponibilité avant confirmation
~~~~

### Référence courante secrets-providers-dbc3864ba45e

Source : [secrets-providers](../../specs/secrets-providers/spec.md), ligne 178. SHA-256 : `dbc3864ba45e770eed9d7055401b7f85b4ae78c12941857f1dd088ffe9502112`.

Scénarios : Garanties de la remise technique de connexion; Redémarrage sans Auth disponible; Référence présente sans remise admissible.

~~~~text
### Requirement: Remise de connexion PBO indépendante de la base à ouvrir

La remise de connexion au workload PBO MUST être vérifiée sans dépendance circulaire à Auth PostgreSQL, sous la branche technique explicite de authorization. Le provider MUST contrôler identité native, politique courante, mode, cible, références, versions, validité, révocation et audit. La publication externe et les garanties de non-divulgation et de cycle de vie ci-dessous MUST rester obligatoires.

#### Scenario: Garanties de la remise technique de connexion

- **WHEN** le profil sélectionne cette capacité pour le parcours de préparation PostgreSQL
- **THEN** Pour le parcours PA/PZT PostgreSQL, la remise des secrets de connexion au workload PBO MUST suivre la branche technique explicite de authorization et être vérifiable sans dépendre de la base Pixs à ouvrir. Le provider MUST vérifier les preuves natives d'identité du consommateur et la politique protégée courante liant mode, rôle, finalité de connexion, cible, références, versions et bornes. Le provisionnement opérateur et PA MUST utiliser une publication externe contrôlée distincte du provider de lecture ; PA MUST NOT devenir writer générique par sa seule capacité de préparation. Les credentials MUST NOT transiter dans les messages de management PBO–PA ; ils MUST porter seulement références et métadonnées minimisées. Les valeurs MUST être remises par le mécanisme de secrets sélectionné au seul consommateur autorisé, sans persistance dans artefact, journal ou checkpoint. Une indisponibilité, rotation ou révocation MUST conserver l'échec fermé et le cycle de vie des copies. L'audit durable pré-base et son relais C05 idempotent MUST être rapprochés avant disponibilité. LoadCredentialEncrypted reste le choix du profil Debian local ; cette règle MUST NOT déclarer le transport Docker qualifié ni choisir silencieusement un nouveau provider.

#### Scenario: Redémarrage sans Auth disponible

- **WHEN** PBO redémarre avec sa base fermée et des références de connexion publiées pour son workload courant
- **THEN** le provider évalue la politique native sans appel préalable à Auth sur cette base et remet seulement les valeurs autorisées au consommateur vérifié

#### Scenario: Référence présente sans remise admissible

- **WHEN** une référence existe mais sa publication, son consommateur, sa politique courante ou sa version ne peut être vérifiée
- **THEN** le démarrage reste non prêt sans secret dans un message PZT et sans repli INSTALLER
~~~~

### Référence courante secrets-providers-2df55e1ad593

Source : [secrets-providers](../../specs/secrets-providers/spec.md), ligne 197. SHA-256 : `2df55e1ad5933cde4d61016a16f49bb8ac04ab2209a67ee237f55daa00c1a9c6`.

Scénarios : Workload Docker et politique courants; Fichier présent sans identité fiable; Rotation ou relais non confirmé.

~~~~text
### Requirement: Secrets Docker par fichiers versionnés

Le fournisseur Docker distinct de C01 MUST respecter l’intégralité du contrat normatif du scénario « Workload Docker et politique courants » pour toute résolution, rotation, révocation et reprise. Les garanties de confiance, confidentialité, lifecycle et audit y sont indissociables ; une garantie absente ou inconnue MUST maintenir l’échec fermé.

#### Scenario: Workload Docker et politique courants

- **WHEN** un workload prouvé demande des références et versions autorisées pour son mode, sa finalité et sa cible avec audit durable confirmé
- **THEN** seules les valeurs admissibles sont remises au consommateur vérifié et leur relais C05 reste requis avant disponibilité
- **AND** aucun credential ne transite dans les messages de management PZT
- **AND** Le profil Docker local MUST sélectionner un fournisseur distinct du transport systemd C01 pour résoudre des références par fichiers versionnés montés en lecture seule au runtime. Il MUST vérifier une preuve native du workload et une politique protégée courante liant mode réel, rôle, finalité, cible, références, versions, validité, révocation, bornes et audit. Pour la seule remise technique de connexion PBO, ces contrôles MUST être vérifiables sans Auth dans la base à ouvrir ; les autres résolutions MUST conserver leur autorité applicative courante. UID, présence ou propriété d’un fichier, variable d’environnement et déclaration appelante MUST NOT suffire comme identité ou autorisation. La publication externe MUST rester distincte de la lecture. Les valeurs MUST rester dans le processus consommateur, hors environnement, argv, PZT, artefacts, journaux et checkpoints. Le lifecycle MUST assurer l’arrêt attesté des consommateurs avant remplacement puis remontage ou recréation contrôlée, sans prolongation de copie, perte PostgreSQL ou reconstruction d’image. L’audit durable pré-base et le relais C05 idempotent MUST être rapprochés avant disponibilité ; une garantie absente ou inconnue MUST maintenir l’échec fermé. C01 Debian, SecretReference et les gabarits purs MUST rester inchangés ; une preuve systemd MUST NOT qualifier ce fournisseur Docker ni lui donner un droit métier ou R01.

#### Scenario: Fichier présent sans identité fiable

- **WHEN** un fichier existe mais que la preuve native, la politique, la version ou la fraîcheur du consommateur ne peut être vérifiée
- **THEN** aucune valeur ni disponibilité n’est annoncée, sans repli vers INSTALLER ni autorisation déduite du fichier ou de l’UID

#### Scenario: Rotation ou relais non confirmé

- **WHEN** une version doit être remplacée alors qu’un ancien consommateur n’est pas arrêté ou que le relais d’audit reste inconnu
- **THEN** aucune rotation achevée ni disponibilité conforme n’est annoncée
- **AND** la reprise exige arrêt attesté, remplacement et remontage ou recréation contrôlés, revalidation et rapprochement C05 sans perte du stockage PostgreSQL ni reconstruction de l’image
~~~~

### Référence courante zt-pki-35b43ca99bc1

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 11. SHA-256 : `35b43ca99bc19a1cc2886c63ff2dadf004ebc019e0a1623e1e57607614315e75`.

Scénarios : Deux Domaines partagent ZT.

~~~~text
### Requirement: PKI propre et autorités multiples

Chaque ZT MUST disposer d'une PKI propre avec racine protégée hors ligne et au moins un PKIZT exécuté par PZT. Au moins une autorité opérationnelle MUST être initialisée ; plusieurs autorités MAY être ajoutées explicitement avec identité, clé, périmètre et politiques propres. Ajouter un membre ou une organisation MUST NOT créer implicitement une autorité.

#### Scenario: Deux Domaines partagent ZT

- **WHEN** le même ZT dessert deux Domaines
- **THEN** la PKI reste propre au ZT et les autorités supplémentaires sont créées explicitement selon les besoins.
~~~~

### Référence courante zt-pki-4c7ec15b616c

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 20. SHA-256 : `4c7ec15b616c8b8295e4863f64b3e4a465038f629ad42aed8ba274ea7623d2fb`.

Scénarios : Reprise d’autorité.

~~~~text
### Requirement: PG propre et clés opérationnelles répliquées

PKIZT MUST conserver données et clés privées des autorités opérationnelles chiffrées dans une PG indépendante de PBO/CZT/DZT et bases Instance/Domaine, synchronisée selon les garanties PG zt-controller. Un PKIZT habilité MUST pouvoir reprendre la même autorité avec la même clé et son état courant d'émission/révocation.

#### Scenario: Reprise d’autorité

- **WHEN** le secours habilité reprend une autorité admissible
- **THEN** il retrouve la même clé protégée et l’état cohérent au lieu de créer systématiquement une nouvelle autorité.
~~~~

### Référence courante zt-pki-eb43ece12358

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 29. SHA-256 : `eb43ece12358a900332f64387ce6d3505c0aea4c05abefa1268fb77fb1c9ac1c`.

Scénarios : Réplique non habilitée.

~~~~text
### Requirement: Protection individualisée et habilitations séparées

Les enveloppes des clés chiffrées MUST être répliquées avec protection individualisée par PKIZT. Chaque PKIZT MUST conserver son propre moyen protégé de déverrouillage. Les droits d'administration, déchiffrement et émission MUST être séparés par autorité ; l'accès à PG MUST NOT suffire à utiliser une clé.

#### Scenario: Réplique non habilitée

- **WHEN** un membre possède la copie PG mais aucune habilitation de déchiffrement d’une autorité
- **THEN** il ne peut pas déverrouiller ou utiliser sa clé.
~~~~

### Référence courante zt-pki-5dd5b9ed6de1

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 38. SHA-256 : `5dd5b9ed6de180323769cc74609618707446830a9e84aeee09488fa23a677742`.

Scénarios : Ancien signataire non exclu.

~~~~text
### Requirement: Émetteur unique et secours encadré

Une autorité MUST posséder un émetteur actif unique. L'activation du secours MAY être automatique sous politique/mandat, avec contrôles de reprise et exclusion de l'ancien émetteur. L'habilitation d'une autre autorité MUST NOT suffire et un ancien état restauré MUST être réconcilié avant émission.

#### Scenario: Ancien signataire non exclu

- **WHEN** le secours ne peut prouver que l’ancien émetteur est empêché d’émettre
- **THEN** la reprise d’autorité n’est pas engagée.
~~~~

### Référence courante zt-pki-2ae6168f0a0c

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 47. SHA-256 : `2ae6168f0a0c414767a99f8ae8b52c96dcdd3ed4d9b18f73c67870597438d38a`.

Scénarios : Demande publique.

~~~~text
### Requirement: ACME public et génération de clés

PKIZT MUST pouvoir gérer des certificats publiquement reconnus via ACME selon les profils autorisés. La clé privée MUST être générée/protégée côté PKIZT ; compte ACME et clés de certificats MUST suivre leurs protections chiffrées et synchronisées. L'autorité publique MUST NOT être présentée comme fournisseur de la clé privée.

#### Scenario: Demande publique

- **WHEN** un profil autorise un certificat ACME
- **THEN** PKIZT conserve la clé privée et soumet la demande contenant la clé publique à signer.
~~~~

### Référence courante zt-pki-e3e8cdbdb3dd

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 56. SHA-256 : `e3e8cdbdb3dd1c0442050aed5ee076e3f5eb7d4b33694fe76a9a9458c6fe05ac`.

Scénarios : Deux coordonnateurs.

~~~~text
### Requirement: Challenges et coordination ACME

DNS-01, HTTP-01 et TLS-ALPN-01 MUST être sélectionnables par profil avec orchestration autorisée DZT/RPZT. Un certificat MUST avoir un coordonnateur ACME actif unique et un état durable permettant la reprise sans double opération non maîtrisée.

#### Scenario: Deux coordonnateurs

- **WHEN** deux PKIZT tentent de gérer le même certificat
- **THEN** un seul est admissible à coordonner les opérations courantes.
~~~~

### Référence courante zt-pki-ba327c12b293

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 65. SHA-256 : `ba327c12b293ee06bbc12a70370bb17386dd700089e7ab0af38230953b5cec06`.

Scénarios : Certificat non servi.

~~~~text
### Requirement: Renouvellement anticipé et déploiement vérifié

Le renouvellement MUST être automatique et anticipé selon le profil, avec ARI lorsqu'il est disponible. La réussite MUST distinguer obtention du certificat, distribution et activation réellement vérifiée sur les services ; l'émission MUST NOT prouver le déploiement.

#### Scenario: Certificat non servi

- **WHEN** un certificat renouvelé existe mais RPZT sert encore l’ancien
- **THEN** le déploiement reste incomplet et ne peut être annoncé réussi.
~~~~

### Référence courante zt-pki-790b4d1f8594

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 74. SHA-256 : `790b4d1f85949dec88a03d074756efcd37cc36d11652e4dc9e2449f12c9ee58e`.

Scénarios : Publication partagée explicitement.

~~~~text
### Requirement: Remise TLS ciblée aux RPZT

Les éléments TLS MUST être distribués uniquement aux RPZT habilités, avec protection individualisée. Un certificat/clé distinct par RPZT MUST être le défaut ; un partage MAY être choisi explicitement par publication. Les secrets MUST NOT être exposés dans les consultations, diagnostics ou artefacts.

#### Scenario: Publication partagée explicitement

- **WHEN** un profil choisit la même clé pour plusieurs RPZT
- **THEN** chaque destinataire habilité reçoit sa propre protection sans rendre la clé lisible aux autres acteurs.
~~~~

### Référence courante zt-pki-829050040a60

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 83. SHA-256 : `829050040a60bf4f7f751a728f96bd8372220ff0a690f21d6a7bbbf87624e964`.

Scénarios : Clé compromise.

~~~~text
### Requirement: Récupération par autorité et racine distincte

Chaque autorité MUST choisir sa procédure de récupération par profil. Les protections de racine hors ligne et de rotation normale MUST rester distinctes de la reprise d'une autorité opérationnelle. Une compromission suspectée MUST empêcher la réutilisation non vérifiée de la même clé.

#### Scenario: Clé compromise

- **WHEN** une clé de secours est suspectée compromise
- **THEN** la réplication ne la rend pas admissible et la procédure autorisée traite le renouvellement ou retrait nécessaire.
~~~~

### Référence courante zt-pki-c23b35888a50

Source : [zt-pki](../../specs/zt-pki/spec.md), ligne 92. SHA-256 : `c23b35888a50538a3598c632ec854bde796684c506e6f66d773e44cd8e036346`.

Scénarios : Confiance technique encore seule disponible; Réutilisation après retrait.

~~~~text
### Requirement: Confiance d'amorçage distincte et retrait vérifié

La PKI normale MUST être distincte de la confiance technique pré-PostgreSQL de C08/Z12. Cette confiance initiale MUST rester limitée et bornée, puis être retirée après établissement et vérification de la PKI normale et de ses usages requis. La transition MUST conserver la traçabilité des identités, les retraits connus et des preuves de bascule, sans exporter les clés matérielles initiales pour en faire des clés opérationnelles PG.

#### Scenario: Confiance technique encore seule disponible

- **WHEN** PostgreSQL est disponible mais la PKI normale ou ses usages n'ont pas été vérifiés
- **THEN** la transition reste incomplète dans ses bornes d'amorçage et aucun justificatif initial n'est promu implicitement en justificatif normal

#### Scenario: Réutilisation après retrait

- **WHEN** une ancienne confiance d'amorçage est invoquée après son retrait attesté
- **THEN** elle est refusée même en cas de panne de la PG opérationnelle
~~~~

### Référence courante auth-managed-kerberos-050d7fe34c83

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 11. SHA-256 : `050d7fe34c83001e92768a1d227ad8e8df7e5412165840403ab7355727a71698`.

Scénarios : LDAP normal indisponible.

~~~~text
### Requirement: KZT obligatoire et backend OpenLDAP

Chaque Domaine MUST disposer d'au moins un KZT/MIT Kerberos à backend OpenLDAP et MAY avoir plusieurs KZT actifs. En mode normal, l'état opérationnel Kerberos durable MUST résider dans LDAP ; PG MUST garder les références Pixs. PA MUST installer/configurer/exploiter et Auth piloter les politiques. Un backend PG natif MIT ou un engagement PG préalable de chaque écriture KDC MUST NOT être supposé.

#### Scenario: LDAP normal indisponible

- **WHEN** le backend OpenLDAP exigé devient indisponible
- **THEN** les fonctions dépendantes suivent leur dégradation et aucune base Kerberos PG de remplacement n’est activée implicitement.
~~~~

### Référence courante auth-managed-kerberos-7bb78778c4c7

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 20. SHA-256 : `7bb78778c4c7ca79543e71307f9ddf3cd73f22dfd369945dd576583202a146dd`.

Scénarios : Realm en collision.

~~~~text
### Requirement: Realm propre et mappings explicites

Chaque Domaine MUST déclarer un realm propre partagé par ses KZT et unique dans l'Instance. Les principals et identités de service MUST être liés explicitement aux identités Core et périmètres. Realm, nom ou ticket MUST NOT créer d'identité ou permission par simple correspondance.

#### Scenario: Realm en collision

- **WHEN** un second Domaine demande un realm déjà utilisé dans l’Instance
- **THEN** la déclaration est refusée avant activation.
~~~~

### Référence courante auth-managed-kerberos-1760917ff34e

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 29. SHA-256 : `1760917ff34e9206553c315688562ddfa433ed8c35bd55afcfc957337e279434`.

Scénarios : Moyens locaux perdus.

~~~~text
### Requirement: Protection et récupération des clés Kerberos

Clé maîtresse, clés de principals et keytabs MUST être protégées sous identités minimales, sans secret en clair dans tables métier, artefacts ou journaux. Les clés/états Kerberos durables normaux MUST rester dans le backend LDAP. Chaque Domaine MUST déclarer les moyens protégés et procédures de récupération, distincts des seules références PG et sans dépendance circulaire au KZT à reconstruire.

#### Scenario: Moyens locaux perdus

- **WHEN** les moyens d’ouverture KZT sont perdus malgré une sauvegarde LDAP
- **THEN** la procédure de récupération choisie est requise et LDAP seul ne prouve pas l’ouverture possible.
~~~~

### Référence courante auth-managed-kerberos-255d8bbfe611

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 38. SHA-256 : `255d8bbfe611d38f703a6932a1d6f604ae7e1b010acca6e9612d84b3fe964a2b`.

Scénarios : Partition de contrôleurs.

~~~~text
### Requirement: Verrouillage cohérent du realm

Les KZT actifs MUST partager un verrouillage global par realm cohérent par identité. En partition, la cohérence MUST primer sur la disponibilité des authentifications qui en dépendent. Les chemins PG/LDAP/Kerberos concernés MUST coordonner le verrouillage par identité numérique sans verrouiller les autres identités du même individu par déduction.

#### Scenario: Partition de contrôleurs

- **WHEN** un KZT ne peut vérifier l’état global exigé du verrouillage
- **THEN** il ne confirme pas l’authentification dépendante sur une copie possiblement périmée.
~~~~

### Référence courante auth-managed-kerberos-1c0f0ee90eed

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 47. SHA-256 : `1c0f0ee90eed2d250f4a8253654ae6b38aa6c7bf5994c5ada4186924e4865ba7`.

Scénarios : Hash PG seul.

~~~~text
### Requirement: Provisionnement progressif par profil

Le provisionnement Kerberos MUST pouvoir être progressif, par administration ou libre-service sous profil explicite. Les identités nécessaires à l'administration globale MUST être prêtes avant activation du premier Domaine. Un compte MUST NOT utiliser Kerberos avant vérification de ses clés ; une session d'enrôlement limitée MUST NOT ouvrir les accès non qualifiés.

#### Scenario: Hash PG seul

- **WHEN** un plan suppose convertir le seul hachage PG en clés Kerberos
- **THEN** il est refusé jusqu’à un parcours de provisionnement compatible et vérifié.
~~~~

### Référence courante auth-managed-kerberos-551806d8cd3f

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 56. SHA-256 : `551806d8cd3f50d3712a590d122c76918252bf71104a0e70406bd4848c8e6400`.

Scénarios : Ticket expiré dans une tolérance native.

~~~~text
### Requirement: Expiration stricte et état courant

Les tickets MUST être bornés et ne plus être utilisables ni renouvelables après leur échéance. Tous les chemins revendiquant cette garantie MUST être qualifiés, sans la déduire du seul réglage de tolérance d'horloge. Retrait MUST empêcher les nouvelles émissions/renouvellements ; les tickets déjà émis MUST rester soumis aux limites documentées et aux contrôles Pixs courants.

#### Scenario: Ticket expiré dans une tolérance native

- **WHEN** un ticket dépasse son échéance mais un composant permettrait encore une tolérance
- **THEN** le chemin ne doit pas accepter cet usage et reste non qualifié s’il ne peut garantir le refus.
~~~~

### Référence courante auth-managed-kerberos-72a422092c18

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 65. SHA-256 : `72a422092c1852f4c79dad57945cc2553528d0d7027fd62cae147da6dc1fa676`.

Scénarios : Approbation sans Kerberos.

~~~~text
### Requirement: Temps et confiance inter-realms

KZT MUST vérifier les exigences de temps du profil commun, sans imposer un serveur supplémentaire par Domaine. La confiance Kerberos inter-domaines MUST être une composante explicitement autorisée des approbations, avec sens, portée et collision de realms contrôlés. Une approbation ZT seule MUST NOT la créer.

#### Scenario: Approbation sans Kerberos

- **WHEN** deux Domaines ont une approbation réseau sans composante Kerberos
- **THEN** aucune confiance inter-realms n’est déduite.
~~~~

### Référence courante auth-managed-kerberos-2916ffe1ae32

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 74. SHA-256 : `2916ffe1ae32cf40ab19b04097e4086d7096189d0b61e05c7a8ceb4f142b7f64`.

Scénarios : Principal retiré restauré.

~~~~text
### Requirement: Restauration sans résurrection

La réadmission KZT MUST vérifier état LDAP, générations de clés, mappings, politiques et retraits courants, en réconciliant les références PG souveraines et les preuves opérationnelles. Une ancienne projection Core MUST NOT remplacer PG ; une restauration LDAP MUST NOT réintroduire un principal retiré. Les garanties de protection, fraîcheur et verrouillage MUST être vérifiées avant readiness.

#### Scenario: Principal retiré restauré

- **WHEN** une ancienne sauvegarde contient un principal retiré depuis sa date
- **THEN** il n’est pas réadmis avant réconciliation courante et vérification du profil.
~~~~

### Référence courante auth-managed-kerberos-9dec834a75dd

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 83. SHA-256 : `9dec834a75ddda1262373b9a35613ba204475cee37c3158184cabaabca0378bb`.

Scénarios : Sauvegarde exploitable; Sauvegarde absente ou inadmissible; Mode normal.

~~~~text
### Requirement: Reconstruction complète en urgence critique

Une reconstruction complète LDAP/Kerberos depuis PG MUST être réservée à une procédure d'urgence en mode critique, explicitement autorisée et tracée. Le profil MUST prévoir restauration de sauvegarde protégée ou recréation depuis les références PG avec nouvelles clés et reprovisionnement nécessaires, selon les copies disponibles. La reprise MUST vérifier les garanties de sécurité avant admission et MUST NOT promettre les mêmes clés depuis de simples métadonnées PG.

#### Scenario: Sauvegarde exploitable

- **WHEN** le profil critique dispose d’un état LDAP/Kerberos protégé et des moyens requis
- **THEN** il restaure puis réconcilie cet état avec PG et les retraits courants avant réadmission.

#### Scenario: Sauvegarde absente ou inadmissible

- **WHEN** le profil choisit la reconstruction depuis les références PG sans clés récupérables
- **THEN** il recrée les clés/états requis et reprovisionne les utilisateurs/services concernés, sans prétendre conserver leurs anciens justificatifs ou tickets.

#### Scenario: Mode normal

- **WHEN** un KZT effectue une écriture native normale dans LDAP
- **THEN** la règle de reconstruction critique n’impose pas un engagement miroir PG avant chaque écriture.
~~~~

### Référence courante auth-managed-kerberos-3ea4c587f7b3

Source : [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md), ligne 102. SHA-256 : `3ea4c587f7b34899a82cc619ce6206e84c6436a4d92c7bfa5abde2c2eef09069`.

Scénarios : Reconstruction dans un Domaine.

~~~~text
### Requirement: État critique distinct du mode d'exploitation

L'état critique de reconstruction MUST rester distinct des modes Standalone/ZT/Domaine et de la classe réseau Critique d'A05. Il MUST NOT provoquer un changement de mode ou une exemption d'autorisation implicite.

#### Scenario: Reconstruction dans un Domaine

- **WHEN** un Domaine entre en état critique pour reconstruire Kerberos
- **THEN** l'Instance reste en mode Domaine et les autorisations et mandats applicables restent requis
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->
