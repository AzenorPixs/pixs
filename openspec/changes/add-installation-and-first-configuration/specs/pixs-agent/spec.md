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

### Requirement: Retrait irréversible de la préparation initiale PA

Le PA système MUST retirer irréversiblement sa préparation initiale par withdraw_initial_authority, classe Critique, domaine PA_POSTGRESQL_WITHDRAWAL, permission WITHDRAW_PA_INITIAL. Le mandat MUST être nouveau distinct de R01 et E4, avec signature, clé, politique et validité courantes vérifiées.

#### Scenario: Retrait de la préparation initiale attesté

- **WHEN** un mandat de retrait courant et non consommé est vérifié pour la cible et le plan concernés, avec quiescence constatée
- **THEN** PA ancre durablement et irréversiblement la fin de toute nouvelle préparation initiale et refuse toute nouvelle préparation initiale sous l'autorité retirée
- **AND** la signature, la clé et la politique courantes, la révocation, la validité et la fraîcheur UTC, les identités natives et la relation PZT, la cible, le plan et le contexte, l'anti-rejeu et l'ancrage durable sont vérifiés, sans inventer d'autorité ordinaire déjà admise
- **AND** la remise minimale canonique PBO est conservée

#### Scenario: Retrait rejoué ou étendu

- **WHEN** un mandat déjà consommé est rejoué, ou une inspection est utilisée pour rouvrir une extension ou une préparation
- **THEN** PA refuse sans nouvel effet et conserve l'état de retrait

#### Scenario: Garanties conservées du retrait PA

- **WHEN** le retrait est vérifié pour la cible et le plan concernés
- **THEN** un DTO à l'état RETIRED, un résultat PG_SUCCEEDED, un mode NORMAL ou D6 seul ne prouve pas le retrait
- **AND** le retrait appartient à une famille administrative distincte des trois opérations conservées inspect_postgresql, prepare_postgresql et get_postgresql_result, sans quatrième ajout au catalogue 1.0 et sans inspection administrative via get_postgresql_result
- **AND** les contrats de topologie D8/D6, de wire et de résolveurs restent à fermer en revue commune avant leur code, les qualifications réelles en phase 2 après réalisation, et l'adoption des principes ne vaut pas réalisation

## ADDED Requirements

### Requirement: Préparation confirmée sous enveloppe 1.1 et plan PA

Pour le profil PostgreSQL initial 1.1 E5 sélectionné, la préparation PA MUST suivre OBSERVE, PREPARE_PLAN, confirmation puis PREPARE critique et READ_RESULT, sans modifier les contrats 1.0 ni fallback. Le request_digest MUST engager tous les octets de l'enveloppe. Les bindings MUST être vérifiés par leurs propriétaires. Docker, INITIALIZE_START, RECREATE et DATABASE_DROP MUST être refusés avant tout effet sans conversion silencieuse.

#### Scenario: Enveloppe et confirmation liées avant effet

- **WHEN** une préparation est demandée avec observation et planning vérifiés
- **THEN** PA retourne l'observation puis le planning avant toute confirmation C08, avec projection C08 immuable liée à l'observation et bundle vérifié, et la confirmation C08 seize champs porte le plan, les préconditions et les effets avant l'acte signé, avec request_digest engageant toute l'enveloppe 1.1 et READ_RESULT distincte

#### Scenario: Refus sans conversion silencieuse

- **WHEN** un plan contient RECREATE, DATABASE_DROP ou une branche Docker non sélectionnée
- **THEN** PA refuse le plan entier avant tout effet sans le convertir en CREATE
