# Références normatives — O26

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| audit-integrity / 11 | [Mécanisme d'intégrité explicitement déclaré](../../specs/audit-integrity/spec.md#L11) | NE | AUDIT_AVANT_CREATION |
| audit-integrity / 25 | [Preuves vérifiables et chaînage résilient](../../specs/audit-integrity/spec.md#L25) | NE | AUDIT_AVANT_CREATION |
| audit-integrity / 37 | [Exports et conservation vérifiables](../../specs/audit-integrity/spec.md#L37) | NE | AUDIT_AVANT_CREATION |
| audit-integrity / 49 | [Confidentialité, rétention et droit d'effacement préservés](../../specs/audit-integrity/spec.md#L49) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence audit-integrity--a4b7de520c

Source : `openspec/specs/audit-integrity/spec.md`, ligne 11. SHA-256 du bloc : `d2814a145a73d6199dea724a07c60ee6ad8543e20bc73f40806f5a00f5d39b94`.

~~~~text
### Requirement: Mécanisme d'intégrité explicitement déclaré

Un mécanisme d'intégrité MUST commencer par un chaînage vérifiable déclaré par
composant ou déploiement avec son algorithme, sa version, son fournisseur, sa
portée et ses politiques de conservation. Un scellement externe MAY compléter
ce chaînage ; une conservation WORM MUST rester une politique explicitement
déclarée par le déploiement. Le système MUST NOT activer un mécanisme
implicitement pour un audit qui ne le requiert pas.

#### Scenario: Audit standard sans mécanisme déclaré

- **WHEN** une installation n'active aucune politique d'intégrité renforcée
- **THEN** son audit conserve les garanties de base sans revendiquer une preuve cryptographique
~~~~

### Référence audit-integrity--661261e8cb

Source : `openspec/specs/audit-integrity/spec.md`, ligne 25. SHA-256 du bloc : `15c5e8ae0326bcf041f802ff4749572dc3587e956816b1a7b0cfd23978567840`.

~~~~text
### Requirement: Preuves vérifiables et chaînage résilient

Les preuves MUST lier les événements, versions, ordres ou fenêtres déclarés et
permettre de détecter une altération, omission ou rupture dans leur portée. Une
preuve invalide MUST être diagnostiquée et ne peut pas être silencieusement
remplacée par une nouvelle chaîne.

#### Scenario: Événement modifié

- **WHEN** un événement couvert est altéré après son scellement
- **THEN** la vérification échoue avec une corrélation vers la preuve concernée
~~~~

### Référence audit-integrity--5bff214cdd

Source : `openspec/specs/audit-integrity/spec.md`, ligne 37. SHA-256 du bloc : `6c7c1016911c637140b3e07be7a1de4b5f0df8592c3c0f89af80a3915d45491c`.

~~~~text
### Requirement: Exports et conservation vérifiables

Un export d'audit doté d'une preuve d'intégrité MUST contenir les métadonnées
nécessaires à sa vérification, sans inclure clé privée ni secret. Une politique
WORM MAY être utilisée lorsqu'elle est compatible avec la résidence, la
rétention et les contrôles d'accès déclarés.

#### Scenario: Export soumis à vérification

- **WHEN** un opérateur autorisé vérifie un export scellé
- **THEN** il peut confirmer son intégrité ou obtenir une erreur explicite sans accéder aux clés privées
~~~~

### Référence audit-integrity--b185441b51

Source : `openspec/specs/audit-integrity/spec.md`, ligne 49. SHA-256 du bloc : `49b277b80d9fdd38e4ff4c4127e4cc18da297600db741c3fba944644e3cd8873`.

~~~~text
### Requirement: Confidentialité, rétention et droit d'effacement préservés

L'intégrité MUST NOT empêcher l'application d'une obligation légale d'effacement
ou de minimisation. Une anonymisation, un tombstone ou une preuve de retrait
MUST préserver la traçabilité déclarée sans conserver une donnée personnelle ou
un secret au-delà de la politique applicable.

#### Scenario: Effacement d'une donnée auditée

- **WHEN** une obligation d'effacement autorisée concerne un événement scellé
- **THEN** le système applique le traitement déclaré et conserve uniquement la preuve autorisée de l'opération
~~~~

