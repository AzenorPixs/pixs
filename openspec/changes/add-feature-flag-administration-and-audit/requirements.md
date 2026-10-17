# Références normatives — O13

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| feature-flags / 8 | [Application de l'exception Super Admin](../../specs/feature-flags/spec.md#L8) | P | INTEGRER_EXISTANT_SI_SELECTION |
| feature-flags / 113 | [Affectations hors artefacts](../../specs/feature-flags/spec.md#L113) | P | INTEGRER_EXISTANT_SI_SELECTION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence feature-flags--5a10834a86

Source : `openspec/specs/feature-flags/spec.md`, ligne 8. SHA-256 du bloc : `f8682d3983c629615bc903f81c6a9d22b2a6477d3403c8383ed718335b502b65`.

~~~~text
### Requirement: Application de l'exception Super Admin

Les exigences et scénarios de contrôle applicatif de cette capacité MUST s'appliquer sous réserve de l'exception définie par `authorization`, dans le périmètre du seul compte décrit par `initial-administration`. Les comptes ordinaires MUST conserver leurs contrôles. Les profils structurels préparatoires MUST rester inchangés.

#### Scenario: Garde de fanion dérogée

- **WHEN** un fanion bloque une opération du Super Admin dans son périmètre autorisé et ce compte utilise une dérogation
- **THEN** la garde applicative dérogée ne bloque pas l'opération
- **AND** la dérogation ne fabrique pas une valeur de fanion ni une capacité implémentée absente
~~~~

### Référence feature-flags--a29810cb32

Source : `openspec/specs/feature-flags/spec.md`, ligne 113. SHA-256 du bloc : `d502472158a077c9bfc22db194c232cd1fd73cafd61f3603657c6387da27b9c6`.

~~~~text
### Requirement: Affectations hors artefacts

Le système MUST respecter les garanties suivantes.

Les affectations runtime proviennent d'une source persistante versionnée ; aucun paquet, image ni bundle n'embarque d'affectation ; les changements sont administrés, corrélés et audités.

#### Scenario: Affectation embarquée rejetée

- **WHEN** un artefact contient une affectation d'installation ou de production
- **THEN** le build refuse la composition
~~~~

