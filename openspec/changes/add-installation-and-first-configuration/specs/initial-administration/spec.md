## MODIFIED Requirements

### Requirement: Provisionnement interactif de la base

Le parcours INSTALLER MUST être lancé explicitement par l'opérateur et faire préparer PostgreSQL par le PA système de l'hôte selon installation-provisioning, pixs-agent et pzt. Sur hôte physique ou VM, PA MUST installer et configurer le service si nécessaire ; dans l'image Docker Pixs, le logiciel MUST être déjà fourni et PA MUST initialiser seulement le stockage et la configuration manquants, sans réinitialiser l'existant. Les paramètres de cible, port (5432 par défaut), base et références d'accès nécessaires MUST être explicitement recueillis et vérifiés dans ce parcours ; aucun secret MUST transiter par un artefact ou message de management PBO–PA. PA MUST initier la première connexion technique de préparation. PBO MUST vérifier le résultat et conserver l'inspection du schéma, les migrations et l'initialisation applicatives par leurs contrats propriétaires. Base absente : création explicitement confirmée ; base conforme : conservation ; base migrable : plan de migration confirmé ; base incompatible : suppression et recréation seulement après confirmations distinctes, fraîches et liées à la cible. Une préparation technique PA MUST NOT créer un Super Admin, une identité Core, un tenant ou une autorisation métier.

#### Scenario: Base migrable

- **WHEN** la base demandée nécessite une migration compatible
- **THEN** PBO affiche le plan et ne fait appliquer la migration par son propriétaire qu’après confirmation explicite ; le reçu PA ne tient pas lieu de migration

#### Scenario: Premier accès technique PostgreSQL

- **WHEN** un opérateur lance INSTALLER sur un hôte physique ou une VM sans PostgreSQL préparé
- **THEN** PA prépare le service et initie la première connexion technique sous son mandat borné ; PBO n’effectue ses opérations applicatives qu’après vérification des prérequis

#### Scenario: Stockage Docker existant

- **WHEN** un conteneur Pixs démarre avec un stockage PostgreSQL déjà initialisé
- **THEN** PA le conserve et vérifie sa compatibilité sans réinitialisation ; une incompatibilité maintient l’installation non prête jusqu’au plan autorisé
