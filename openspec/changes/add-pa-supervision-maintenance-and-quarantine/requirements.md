# Références normatives — PA07

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pixs-agent / 164 | [Supervision PBO et collecte PA](../../specs/pixs-agent/spec.md#L164) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 173 | [Maintenance et quarantaine sans nouveaux droits](../../specs/pixs-agent/spec.md#L173) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 191 | [Interfaces et messages cohérents](../../specs/pixs-agent/spec.md#L191) | ND | CANDIDAT_PROFIL_PA |
| pzt / 147 | [Audit applicable et faits réellement établis](../../specs/pzt/spec.md#L147) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pixs-agent--9c56e42aad

Source : `openspec/specs/pixs-agent/spec.md`, ligne 164. SHA-256 du bloc : `aa149c5fbf55f46a5c6f96edd12c63fb92994dc70c95b1b47283cacd23ccbef3`.

~~~~text
### Requirement: Supervision PBO et collecte PA

Configuration, visualisation, supervision et monitoring PZT MUST toujours relever de PBO. PA MUST collecter et remonter les mesures et états réellement observés via PZT. Vivacité, disponibilité, démarrage, diagnostic et résultat métier MUST rester distincts ; une mesure ancienne MUST être datée et MUST NOT devenir un état courant par absence de nouvelle information.

#### Scenario: Supervision PBO et collecte PA

- **WHEN** la collecte est interrompue alors que le dernier état était sain
- **THEN** PBO signale les mesures périmées et ne déduit pas une disponibilité actuelle
~~~~

### Référence pixs-agent--5b1af8f5b9

Source : `openspec/specs/pixs-agent/spec.md`, ligne 173. SHA-256 du bloc : `22837bf1d6a8eaad369b982b893a18f8cfd30af14efc62e6f8674dd89abe30d8`.

~~~~text
### Requirement: Maintenance et quarantaine sans nouveaux droits

Les profils MUST déclarer états normal, surveillance seule, maintenance et quarantaine avec portées, actions permises/interdites et conditions de sortie. Drainage et arrêt MUST être bornés ; les nouvelles modifications incompatibles MUST être refusées. Ces états MUST NOT accorder de droit supplémentaire ni supprimer les contrôles applicables.

#### Scenario: Maintenance et quarantaine sans nouveaux droits

- **WHEN** la cible entre en maintenance pendant une opération
- **THEN** son drainage suit le contrat et les nouvelles mutations incompatibles sont refusées
~~~~

### Référence pixs-agent--df6fedb5de

Source : `openspec/specs/pixs-agent/spec.md`, ligne 191. SHA-256 du bloc : `e32fa647dde73362fa0d805f8baa9b8f7b888563b7ebdd92de397deda7bbd06c`.

~~~~text
### Requirement: Interfaces et messages cohérents

Les interfaces CLI et les contributions PBO/PFO MUST utiliser les contrats publics, des erreurs stables et les traductions des composants propriétaires ; codes et champs MUST rester non localisés. PFO MUST adresser ses demandes à PBO ; aucune liaison directe PFO–PA MUST être introduite par ces spécifications. Les interfaces MUST respecter accessibilité, thèmes et confidentialité déclarés.

#### Scenario: Interfaces et messages cohérents

- **WHEN** une action est présentée dans PFO
- **THEN** son autorisation reste évaluée par PBO avant transmission éventuelle à PA via PZT
~~~~

### Référence pzt--82a0e6c439

Source : `openspec/specs/pzt/spec.md`, ligne 147. SHA-256 du bloc : `bc7545fffd89f97f8278ddfd75e3a0e388c7291bebe64612552dc59554458b29`.

~~~~text
### Requirement: Audit applicable et faits réellement établis

Les contrôles applicatifs PZT MUST suivre security, authorization, initial-administration et audit, y compris l'exception Super Admin dans son seul périmètre reconnu. Aucun worker MUST recevoir ses credentials ou devenir Super Admin. Une dérogation MUST NOT fabriquer un dossier, audit, contrôle, signature, mesure ou effet absent ; les contrats structurels et d'exécution MUST rester distincts.

#### Scenario: Audit applicable et faits réellement établis

- **WHEN** une opération utilise une dérogation sans audit persistant
- **THEN** l'absence est déclarée et aucune preuve d'audit effectuée n'est annoncée
~~~~

