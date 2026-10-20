# Tâches futures — Forge et enrôlement des identités numériques

Toutes les tâches restent non cochées ; l'ouverture de ce change autorise uniquement sa préparation documentaire.

## 1. Conception

- [ ] 1.1 Revoir et adopter les deltas sous autorisation distincte ; confirmer dépendances, contrats et paramètres ouverts.
- [ ] 1.2 Définir modèles propriétaires, migrations, secrets, reprise et plans de retrait sans déplacer les contrats Core existants.

## 2. Réalisation future sous mandat distinct

- [ ] 2.1 Intégrer les Commands Core de création/rattachement avec les dossiers Auth persistants.
- [ ] 2.2 Ajouter invitations, liaisons bilatérales, vérificateurs extensibles et rétention minimisée.
- [ ] 2.3 Raccorder la reprise au provisionnement C08 sans créer un second chemin d'autorité.

## 3. Qualification future

- [ ] 3.1 Tester interruption à chaque frontière Core/Auth, rejeu et conflit de liaison sans doublon.
- [ ] 3.2 Tester absence de fusion par e-mail, refus inter-tenant, preuve insuffisante et provisionnement de secours.
- [ ] 3.3 Vérifier syntaxe, contrôles configurés, audit sans secret, isolation tenant et limites de révocation sur l'artefact réel.
- [ ] 3.4 Examiner diff et preuves ; synchroniser, archiver, engager Git ou publier seulement sous autorisation distincte.
