## ADDED Requirements


### Requirement: Préparation PostgreSQL par le PA système

Le PA système du profil sélectionné MUST préparer PostgreSQL sur hôte physique/VM ou initialiser les ressources manquantes dans Docker, sous mandat technique vérifié et catalogue fermé. Il MUST conserver les données et sa séparation avec les migrations et mutations applicatives PBO. Tous échanges PBO–PA MUST passer par PZT ; reprise et garanties ci-dessous sont obligatoires.

#### Scenario: Garanties de la préparation PA

- **WHEN** le profil sélectionne cette capacité pour le parcours de préparation PostgreSQL
- **THEN** Le PA système MUST posséder une capacité livrée et versionnée de préparation PostgreSQL sélectionnée explicitement par le profil d'installation. Sur hôte physique ou VM elle MUST installer et configurer le service dans son périmètre autorisé ; sous Docker elle MUST utiliser le logiciel fourni dans l'image, initialiser seulement les ressources absentes et conserver les données persistantes. Son mandat MUST lier opérateur préautorisé, exécutant effectivement vérifié, installation, hôte ou conteneur cible, opération et version, plan confirmé, validité, politique courante, corrélation et idempotence. PA MUST limiter ses connexions SQL aux opérations techniques explicitement prévues de service, rôle et base ; les privilèges de préparation MUST être distincts des accès applicatifs et retirés ou rendus inutilisables après leur phase. PA MUST NOT lire ou muter les tables métier, exécuter les migrations à leur place, créer Core/Auth/Super Admin/tenant ni confondre son résultat technique avec un commit applicatif. Tous échanges avec PBO MUST emprunter PZT, y compris locaux. La capacité MUST rester dans le catalogue fermé livré ; aucun code reçu, shell arbitraire ou droit hôte issu du seul conteneur n'est admis.

#### Scenario: Rejeu après préparation technique

- **WHEN** la même opération PA est reprise après une réponse perdue
- **THEN** PA inspecte son résultat durable et la ressource cible avant tout effet ; une issue inconnue est réconciliée, sans recréer ni effacer la base

#### Scenario: Demande hors rôle technique

- **WHEN** un mandat PA de préparation PostgreSQL demande une mutation de table métier ou un code reçu de PBO
- **THEN** PA la refuse sans transférer de privilège ni inventer un résultat applicatif
