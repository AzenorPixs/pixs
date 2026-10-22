# Tâches — C05

Réalisation propriétaire autorisée par `1CISMP2`. Les preuves exécutées figurent dans `VALIDATION.md`. Les cases ci-dessous couvrent le travail source C05 et sa revue ; l’archivage, les statistiques postarchive et le gate sont des conditions de clôture du RUN suivies séparément dans son checkpoint.

## 1. Revue de conception

- [x] 1.1 Revoir les exigences/scénarios de requirements.md et le profil C00 ; recouper les sources et empreintes canoniques avant réalisation.
- [x] 1.2 Lever les barrières techniques de stockage, transactions, droits et cycle de vie ; présenter/valider les fichiers et contrats par délégation ISMP sans nouveau delta normatif.

## 2. Réalisation

- [x] 2.1 Définir le propriétaire C05 et la participation commune D13 ; éprouver D14 avec SyntheticAuthOwner de test, sans revendiquer le runtime C03.
- [x] 2.2 Implémenter écritures durables append-only, consultation filtrée, minimisation, anonymisation et purge contrôlées, tombstones et reprise C01 scellée.
- [x] 2.3 Raccorder le port d’audit aux services Core ordinaires et les sources minimales à la composition C4 ; respecter les waivers explicites sans audit fictif.
- [x] 2.4 Éprouver commit/rollback, réponse perdue, issue UNKNOWN conservatrice, échec d’audit fermé, D13/D14 synthétiques, isolation tenant, gouvernance, legal hold, rétention, collisions et acquittements distincts des preuves.

## 3. Preuves et préparation de clôture

- [x] 3.1 Exécuter syntaxe, suites applicables, recette PostgreSQL réelle et contrôle de cohérence des migrations ; conserver les preuves natives.
- [x] 3.2 Vérifier les scénarios applicables, les nettoyages, les secrets maintenus dans le seul processus PG et les neuf références canoniques ; expliciter les garanties non qualifiées.
- [x] 3.3 Examiner les fichiers et le périmètre sans Git ; préserver le travail des autres RUN et actualiser les documents devenus inexacts, sans annoncer une composition P0 livrée.
- [x] 3.4 Préparer l’archivage explicitement autorisé et le mandat distinct du seul STATISTIQUES.md postarchive ; maintenir la clôture conditionnée à ce rapport, son contrôle UTF-8/LF/six sections et au gate réel.

L’archivage et les statistiques ne sont pas déclarés accomplis par ces cases. Leur résultat terminal est donné dans le rapport réel de l’archive et le checkpoint `output/cismp/cismp2-pixs-968e38f3e27b4bbf/state.json`. Si le rapport échoue, seul le rapport est repris, sans réarchiver. L’arrêt concerne ce RUN après livraison ; les services partagés et les autres RUN restent disponibles.
