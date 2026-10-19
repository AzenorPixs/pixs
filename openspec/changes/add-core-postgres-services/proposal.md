# C02 — Primitives Core persistantes

## Pourquoi

User, DigitalIdentity, liaisons, groupes et appartenances sont des représentations mémoire. Les modèles backend persistants existants ne constituent pas les services Core complets.

## Modifications proposées

Ajouter modèles, contraintes et migrations propriétaires pour utilisateurs, identités, groupes, appartenances, tenants/scopes, rôles, ACL et permissions ; exposer les services publics requis. Préserver les profils structurels existants.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions du profil C00 adoptées le 18 octobre 2026 et intégrées au canon.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `define-first-installable-pbo-profile`.

## Impact

Périmètre de réalisation futur : Conserver la distinction User/DigitalIdentity et les UUIDv7 ; porter les données Core dans PostgreSQL avec propriétaire explicite, contraintes et services publics. Séparer scopes/platform/tenant, rôles, ACL et permissions ; créer les migrations après revue du schéma, sans écrire les tables d’un autre composant.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Contraintes UUIDv7 et cardinalités exercées sur PostgreSQL ; séparation tenants/scopes ; accès inter-module par contrats ; migrations et concurrence testées.

## Barrière de conception

Schéma/table propriétaire, contrats de services et concurrence ; modèle de persistance des accords tenant du Super Admin à coordonner avec C04. Aucune réutilisation implicite du modèle User de Django comme fusion de l’identité Pixs.
