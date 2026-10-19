# Tâches futures — stockage Core réversible

Toutes les tâches restent non cochées. La préparation n'exécute aucune migration ni modification de données.

## 1. Conception et adoption

- [ ] 1.1 Adopter les deltas et confirmer périmètre cohérent, contrats et frontières Core/Auth/projection.
- [ ] 1.2 Définir schéma LDAP, garanties de mutation, interactions PostgreSQL, générations et barrière de bascule.
- [ ] 1.3 Définir autorisation, sauvegardes, journal, reprise, retour obligatoire et conservation de l'ancienne copie.

## 2. Réalisation future sous mandat distinct

- [ ] 2.1 Intégrer le provider de stockage Core OpenLDAP interne sans déplacer les responsabilités Core ou l'autorisation Pixs.
- [ ] 2.2 Intégrer plan, copie vérifiée, clôture des écritures, réconciliation et engagement durable de génération.
- [ ] 2.3 Intégrer le retour depuis le LDAP courant, l'invalidation des faits/caches et la reprise idempotente.

## 3. Qualification et clôture futures

- [ ] 3.1 Tester aller, mutations LDAP et retour sans perte de données, droits, UUID ou révocations.
- [ ] 3.2 Tester concurrence, indisponibilités, résultats incertains, multi-stores, audit et absence de repli périmé.
- [ ] 3.3 Qualifier conservation/retrait et restauration sur artefact réel, sans annoncer une conformité à partir de mocks.
- [ ] 3.4 Synchroniser, archiver, engager Git ou publier seulement sous autorisation distincte.
