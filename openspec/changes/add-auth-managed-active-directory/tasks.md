# Tâches futures — pixs.auth.directory.ad

Toutes les tâches restent non cochées. Ce change autorise uniquement la préparation documentaire.

## 1. Conception

- [ ] 1.1 Revoir et adopter les deltas sous autorisation distincte ; confirmer frontières Core/Auth/domaine.
- [ ] 1.2 Qualifier implémentation, plateforme, versions, compatibilité, domaine/realm, DNS, ports et interactions avec OpenLDAP/KDC.
- [ ] 1.3 Définir mappings, stockage natif, secrets, enrôlement, bornes de révocation, sauvegarde et retrait.

## 2. Réalisation future sous mandat distinct

- [ ] 2.1 Déclarer pixs.auth.directory.ad et intégrer plans, lifecycle et santé du service propre.
- [ ] 2.2 Intégrer les opérations de domaine et mappings par contrats publics sans accès aux tables privées Core.
- [ ] 2.3 Intégrer secrets, révocation, reprise et coexistence avec les services sélectionnés.

## 3. Qualification future

- [ ] 3.1 Tester profil autonome sans AD, activation explicite, collisions et refus d'adoption/trust implicite.
- [ ] 3.2 Qualifier clients et mappings, isolation, tickets après retrait et restauration sans résurrection.
- [ ] 3.3 Examiner preuves et périmètre ; synchroniser, archiver, engager Git ou publier uniquement sous autorisation distincte.
