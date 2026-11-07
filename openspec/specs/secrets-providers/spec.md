# secrets-providers Specification

## Purpose

Les fournisseurs de secrets résolvent au runtime des références externes avec
rotation, révocation, contrôle d'accès et audit, sans intégrer de secret aux
sources ou artefacts.

## Requirements

### Requirement: Références externes sans valeur persistée

La configuration, les manifests, les rapports, les diagnostics et les artefacts
MUST contenir uniquement des références de secrets autorisées. Une valeur de
secret, credential ou jeton MUST NOT être sérialisée, journalisée ou publiée.

#### Scenario: Diagnostic de référence indisponible

- **WHEN** un fournisseur ne peut pas résoudre une référence obligatoire
- **THEN** il signale la référence et l'erreur sans révéler de valeur attendue

### Requirement: Accès runtime associé à une identité de workload

Un SecretProvider MUST vérifier l'identité de workload, le composant, le tenant
ou scope lorsque requis, la finalité et la politique d'accès avant résolution.
Une référence valide MUST NOT donner accès à un secret hors du contexte autorisé.

#### Scenario: Worker non autorisé

- **WHEN** un worker demande une référence réservée au profil web
- **THEN** la résolution est refusée et auditée

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

### Requirement: Audit minimisé et échec fermé

Les résolutions, refus, rotations et révocations MUST être auditables avec une
identité, une référence et une corrélation. Une indisponibilité ou une politique
non vérifiable MUST échouer fermé pour une capacité protégée.

#### Scenario: Provider indisponible

- **WHEN** un secret requis ne peut pas être résolu au démarrage
- **THEN** le composant concerné ne devient pas prêt

### Requirement: Transport systemd C01 et identité effectivement vérifiée

Le provider C01 du profil Debian local MUST utiliser LoadCredentialEncrypted par service, hors Kernel, avec valeurs seulement dans le processus consommateur. Il MUST vérifier l’UID et le rattachement réel de son processus à l’unité autorisée avant résolution, puis appliquer la politique de confiance versionnée liant rôle, référence, finalité et périmètre.

#### Scenario: Rôle différent du workload réel

- **WHEN** une demande prétend appartenir au rôle web mais que l’identité native ne satisfait pas sa liaison autorisée
- **THEN** la résolution est refusée avant remise de valeur et le refus est audité

#### Scenario: Contexte tenant absent non transformé en permission

- **WHEN** la phase d’amorçage utilise le périmètre PLATFORM sans tenant_id ni scope_id
- **THEN** seules la politique et l’autorisation technique INSTALLER explicites peuvent admettre la référence

### Requirement: Refus C01 sans preuve native d’identité

Une variable d’environnement, un identifiant fourni par l’appelant ou la seule propriété d’un fichier MUST NOT constituer une identité ou une autorisation. Une preuve native indisponible MUST produire un refus fermé.

#### Scenario: Rôle différent du workload réel

- **WHEN** une demande prétend appartenir au rôle web mais que l’identité native ne satisfait pas sa liaison autorisée
- **THEN** la résolution est refusée avant remise de valeur et le refus est audité

#### Scenario: Contexte tenant absent non transformé en permission

- **WHEN** la phase d’amorçage utilise le périmètre PLATFORM sans tenant_id ni scope_id
- **THEN** seules la politique et l’autorisation technique INSTALLER explicites peuvent admettre la référence

### Requirement: Liaison contrôlée et paramètres C01 sans défaut implicite

Les références SecretReference existantes MUST rester opaques et inchangées. La politique C01 MUST déclarer explicitement l’identité et la version de politique, la référence et version du credential, son identifiant systemd, l’unité et l’UID autorisés, le rôle, la finalité et le périmètre. L’identifiant du credential MUST rester un nom autorisé sans chemin, traversée ou joker.

#### Scenario: Politique incomplète

- **WHEN** une identité, une version, une finalité ou une borne obligatoire manque ou est incohérente
- **THEN** la résolution refuse sans choix de valeur par défaut ni secret de substitution

### Requirement: Bornes obligatoires de la politique C01

Les limites de taille, les bornes de validité, la durée de vie maximale, le délai maximal de révocation et le budget d’arrêt/redémarrage MUST être obligatoires et vérifiables, sans défaut numérique. Une valeur de secret MUST NOT être un paramètre distribué.

#### Scenario: Politique incomplète

- **WHEN** une identité, une version, une finalité ou une borne obligatoire manque ou est incohérente
- **THEN** la résolution refuse sans choix de valeur par défaut ni secret de substitution

### Requirement: Cycle de vie vérifiable des copies systemd chargées

Un secret absent, expiré, révoqué ou associé à une politique non vérifiable MUST être refusé. La durée de vie et le délai de révocation déclarés MUST être respectés par les nouvelles utilisations ; une copie ou un cache MUST NOT prolonger l’accès. Pour une copie déjà chargée, la rotation ou révocation MUST exiger l’arrêt attesté des consommateurs concernés avant remplacement puis redémarrage contrôlé dans les bornes déclarées.

#### Scenario: Ancien consommateur encore actif

- **WHEN** une version est révoquée et que l’arrêt de tous les consommateurs concernés n’est pas prouvé
- **THEN** aucune rotation achevée ni disponibilité conforme n’est annoncée

#### Scenario: Nouvelle version au redémarrage

- **WHEN** l’arrêt, le remplacement et le redémarrage contrôlés sont prouvés sous la politique courante
- **THEN** le consommateur utilise la nouvelle version et ne réutilise pas la copie antérieure

### Requirement: Arrêt et redémarrage des copies systemd chargées

Supprimer la source ou recharger seulement la configuration MUST NOT valoir révocation. Une garantie non prouvée MUST conserver le composant non prêt. La préférence canonique pour les credentials courts compatibles MUST rester applicable.

#### Scenario: Ancien consommateur encore actif

- **WHEN** une version est révoquée et que l’arrêt de tous les consommateurs concernés n’est pas prouvé
- **THEN** aucune rotation achevée ni disponibilité conforme n’est annoncée

#### Scenario: Nouvelle version au redémarrage

- **WHEN** l’arrêt, le remplacement et le redémarrage contrôlés sont prouvés sous la politique courante
- **THEN** le consommateur utilise la nouvelle version et ne réutilise pas la copie antérieure

### Requirement: Résolution auditée et branchement runtime séparé

Le backend MUST produire les événements et vérifier les reçus d’audit requis avant remise d’une valeur, selon le journal d’amorçage autorisé ou le sink propriétaire applicable après reprise. Un callback retournant True MUST NOT prouver l’audit persistant. Les diagnostics MUST rester statiques sans valeur ni exception brute sensible.

#### Scenario: Provider disponible et P0 incomplet

- **WHEN** une résolution runtime conforme réussit mais que les autres obligations du profil ne sont pas prouvées
- **THEN** les gabarits préparatoires restent inchangés et aucune disponibilité globale P0 n’est annoncée

### Requirement: Gabarits purs et disponibilité runtime distincte

Le branchement runtime MUST rester séparé de SettingsTemplate, build_settings_template et check_template, dont les contrats purs, secrets_resolved=False et ready=False MUST rester inchangés. La disponibilité du provider MUST NOT être présentée comme celle de la composition P0.

#### Scenario: Provider disponible et P0 incomplet

- **WHEN** une résolution runtime conforme réussit mais que les autres obligations du profil ne sont pas prouvées
- **THEN** les gabarits préparatoires restent inchangés et aucune disponibilité globale P0 n’est annoncée

### Requirement: Résolution technique après INSTALLER explicitement autorisée

Après INSTALLER, le provider systemd C01 MUST résoudre les références uniquement pour les modes FIRST_CONFIGURATION, NORMAL ou MAINTENANCE expressément autorisés par une politique versionnée liant workload, UID, unité, rôle, finalité, scope, références, versions et bornes. Il MUST conserver les preuves natives, le transport LoadCredentialEncrypted et les règles de rotation/révocation. Un mode MUST NOT être réétiqueté INSTALLER.

#### Scenario: Mode et workload courants autorisés

- **WHEN** un workload dont les preuves natives sont valides demande une référence dans un mode, rôle et finalité autorisés par sa politique courante
- **THEN** la résolution suit cette politique et conserve ses contrôles de validité, de révocation et d’audit

#### Scenario: Mode ou finalité absent de la politique

- **WHEN** une référence existe mais que le mode, le workload ou la finalité ne correspond pas à la politique vérifiée
- **THEN** la remise de valeur est refusée sans secret ni repli vers INSTALLER

### Requirement: Continuité auditée du démarrage avant PostgreSQL

Avant disponibilité de PostgreSQL, la résolution technique MUST disposer d’un audit durable indépendant de cette base, lié à l’invocation et au workload vérifiés. Après ouverture, le relais vers C05 MUST être idempotent et rapproché avant disponibilité applicative. Une preuve absente ou une issue inconnue MUST garder le composant non prêt. Cet audit MUST NOT conférer de droit métier ou R01.

#### Scenario: Audit requis indisponible avant base

- **WHEN** une résolution de démarrage ne peut pas confirmer son audit durable avant disponibilité de PostgreSQL
- **THEN** aucune valeur ni disponibilité applicative n’est annoncée

#### Scenario: Crash pendant le relais vers C05

- **WHEN** un démarrage reprend après un import partiel des événements de son invocation
- **THEN** il inspecte et réconcilie le relais sans événement dupliqué ni disponibilité avant confirmation

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
