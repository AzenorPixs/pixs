## ADDED Requirements

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
