# Tâches futures — Méthodes locales modernes et MFA extensible

Toutes les tâches restent non cochées ; l'ouverture de ce change autorise uniquement sa préparation documentaire.

## 1. Conception

- [ ] 1.1 Revoir et adopter les deltas sous autorisation distincte ; confirmer dépendances, contrats et paramètres ouverts.
- [ ] 1.2 Définir modèles propriétaires, migrations, secrets, reprise et plans de retrait sans déplacer les contrats Core existants.

## 2. Réalisation future sous mandat distinct

- [ ] 2.1 Déclarer les sous-modules locaux sous Auth et leurs contrats de moyens et de preuves.
- [ ] 2.2 Intégrer enrôlement/remplacement/retrait, vérification locale, MFA et récupération sans écrire les tables privées Core.
- [ ] 2.3 Intégrer rate limiting, anti-rejeu, audit et invalidation des contextes affectés.

## 3. Qualification future

- [ ] 3.1 Recetter chaque méthode sur la composition PostgreSQL réelle ; tester expirations, rejeux et limites de tentatives.
- [ ] 3.2 Tester changement de facteur, élévation, récupération concurrente et absence de MFA artificiel ou exigé au secours.
- [ ] 3.3 Vérifier syntaxe, contrôles configurés, audit sans secret, isolation tenant et limites de révocation sur l'artefact réel.
- [ ] 3.4 Examiner diff et preuves ; synchroniser, archiver, engager Git ou publier seulement sous autorisation distincte.
