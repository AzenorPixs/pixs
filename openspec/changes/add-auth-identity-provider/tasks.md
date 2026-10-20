# Tâches futures — Pixs fournisseur d'identité pour les applications clientes

Toutes les tâches restent non cochées ; l'ouverture de ce change autorise uniquement sa préparation documentaire.

## 1. Conception

- [ ] 1.1 Revoir et adopter les deltas sous autorisation distincte ; confirmer dépendances, contrats et paramètres ouverts.
- [ ] 1.2 Définir modèles propriétaires, migrations, secrets, reprise et plans de retrait sans déplacer les contrats Core existants.

## 2. Réalisation future sous mandat distinct

- [ ] 2.1 Déclarer les sous-modules émetteurs et enregistrer les clients/confiances par API autorisée.
- [ ] 2.2 Intégrer émission, validation des destinations, mappings minimisés et protection des clés.
- [ ] 2.3 Intégrer rotation, révocation, logout et suivi des garanties réellement tenues chez les clients.

## 3. Qualification future

- [ ] 3.1 Tester clients non approuvés, confusion d'issuer/audience, destinations invalides, rejeu et isolation.
- [ ] 3.2 Qualifier interopérabilité OIDC/SAML effectivement sélectionnée et bornes de révocation sur des clients réels.
- [ ] 3.3 Vérifier syntaxe, contrôles configurés, audit sans secret, isolation tenant et limites de révocation sur l'artefact réel.
- [ ] 3.4 Examiner diff et preuves ; synchroniser, archiver, engager Git ou publier seulement sous autorisation distincte.
