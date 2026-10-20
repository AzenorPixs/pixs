# Tâches futures — Annuaire OpenLDAP propre géré par pixs.auth

Toutes les tâches restent non cochées ; l'ouverture de ce change autorise uniquement sa préparation documentaire.

## 1. Conception

- [ ] 1.1 Revoir et adopter les deltas sous autorisation distincte ; confirmer dépendances, contrats et paramètres ouverts.
- [ ] 1.2 Définir modèles propriétaires, migrations, secrets, reprise et plans de retrait sans déplacer les contrats Core existants.

## 2. Réalisation future sous mandat distinct

- [ ] 2.1 Déclarer le sous-module de gestion, son plan et le service isolé sans imposer sa présence au profil local.
- [ ] 2.2 Intégrer projection sortante sous contrat existant et capacité d'authentification séparée si sélectionnée.
- [ ] 2.3 Intégrer secrets, santé, arrêt, sauvegarde et réconciliation des dérivés depuis PostgreSQL.

## 3. Qualification future

- [ ] 3.1 Tester installation sans service activé, activation autorisée, panne et conflit avec un annuaire existant.
- [ ] 3.2 Qualifier consultation et binds sélectionnés, isolation, retrait, révocation et restauration sans résurrection.
- [ ] 3.3 Vérifier syntaxe, contrôles configurés, audit sans secret, isolation tenant et limites de révocation sur l'artefact réel.
- [ ] 3.4 Examiner diff et preuves ; synchroniser, archiver, engager Git ou publier seulement sous autorisation distincte.
