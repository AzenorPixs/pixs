# Tâches futures — Sous-modules installables de sources d'authentification externes

Toutes les tâches restent non cochées ; l'ouverture de ce change autorise uniquement sa préparation documentaire.

## 1. Conception

- [ ] 1.1 Revoir et adopter les deltas sous autorisation distincte ; confirmer dépendances, contrats et paramètres ouverts.
- [ ] 1.2 Définir modèles propriétaires, migrations, secrets, reprise et plans de retrait sans déplacer les contrats Core existants.

## 2. Réalisation future sous mandat distinct

- [ ] 2.1 Déclarer et distribuer séparément les sous-modules de sources sélectionnés et leurs dépendances.
- [ ] 2.2 Intégrer validation de confiance, mapping canonique et preuves par contrat Auth sans muter les tables Core.
- [ ] 2.3 Intégrer isolation, indisponibilité, retraits et déprovisionnement explicite des liaisons.

## 3. Qualification future

- [ ] 3.1 Vérifier l'absence des connecteurs dans le profil standard et l'impossibilité d'authentifier avant activation explicite.
- [ ] 3.2 Tester multi-source, collisions, mauvais issuer/realm, panne, absence de repli local et refus d'attributs hors périmètre.
- [ ] 3.3 Vérifier syntaxe, contrôles configurés, audit sans secret, isolation tenant et limites de révocation sur l'artefact réel.
- [ ] 3.4 Examiner diff et preuves ; synchroniser, archiver, engager Git ou publier seulement sous autorisation distincte.
