# Tâches futures — module essentiel pixs.auth

Toutes les tâches restent non cochées. Les documents et deltas proposés ne constituent ni code ni autorisation de réalisation.

## 1. Adoption et conception
- [ ] 1.1 Revoir les deltas et le catalogue ; confirmer contrats, identifiants, frontières Core/Auth et paramètres avant réalisation.
- [ ] 1.2 Adopter les deltas sous autorisation distincte et aligner la recette P0/C03/C08 sans modifier les archives historiques.

## 2. Réalisation future
- [ ] 2.1 Déclarer le module essentiel, ses capacités et sa dépendance publique vers Core, sans cycle.
- [ ] 2.2 Intégrer le stockage PostgreSQL Auth et les migrations propres avec les services C02, secrets et audit.
- [ ] 2.3 Raccorder C03 et les sous-modules locaux ; conserver les sources externes absentes et les services gérés inactifs par défaut.
- [ ] 2.4 Exposer les politiques et leur origine via contrats publics et administration autorisée.

## 3. Qualification et clôture futures
- [ ] 3.1 Prouver autonomie locale PostgreSQL, refus sans module essentiel et absence de repli permissif.
- [ ] 3.2 Prouver isolation, révocation, reprise, frontières de données et exception Super Admin sans MFA inventé.
- [ ] 3.3 Exécuter contrôles configurés et recette du paquet réellement distribué ; déclarer les capacités non qualifiées.
- [ ] 3.4 N'engager synchronisation, archivage, Git ou publication que sous autorisation distincte.
