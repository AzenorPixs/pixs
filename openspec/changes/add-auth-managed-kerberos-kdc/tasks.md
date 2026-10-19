# Tâches futures — KDC Kerberos propre géré par pixs.auth

Toutes les tâches restent non cochées ; l'ouverture de ce change autorise uniquement sa préparation documentaire.

## 1. Conception

- [ ] 1.1 Revoir et adopter les deltas sous autorisation distincte ; confirmer dépendances, contrats et paramètres ouverts.
- [ ] 1.2 Définir modèles propriétaires, migrations, secrets, reprise et plans de retrait sans déplacer les contrats Core existants.

## 2. Réalisation future sous mandat distinct

- [ ] 2.1 Déclarer le sous-module, les plans de gestion et les liaisons de principals par contrats publics.
- [ ] 2.2 Intégrer le lifecycle du KDC choisi, secrets protégés et contrôles de nouvelle émission/renouvellement.
- [ ] 2.3 Intégrer la vérification de tickets et les contrôles courants sans déléguer l'autorisation Pixs.

## 3. Qualification future

- [ ] 3.1 Qualifier KDC seul puis avec OpenLDAP si ce backend est sélectionné, sans source externe installée.
- [ ] 3.2 Tester temps invalide, realm non approuvé, keytab expirée, retrait, ticket encore valide et restauration.
- [ ] 3.3 Vérifier syntaxe, contrôles configurés, audit sans secret, isolation tenant et limites de révocation sur l'artefact réel.
- [ ] 3.4 Examiner diff et preuves ; synchroniser, archiver, engager Git ou publier seulement sous autorisation distincte.
