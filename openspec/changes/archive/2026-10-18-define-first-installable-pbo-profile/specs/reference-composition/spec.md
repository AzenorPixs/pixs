## ADDED Requirements

### Requirement: Profil initial PBO PFO Debian local v1

La première livraison de profil `pbo-p0-debian-local-v1` MUST identifier PBO/PFO, Debian 13 local, Django, PostgreSQL externe et TanStack. Elle MUST déclarer ses architectures et versions qualifiées avant distribution ; le relevé de développement MUST NOT tenir lieu de qualification.

#### Scenario: Architecture seulement observée

- **WHEN** une architecture apparaît dans l’environnement de développement sans recette correspondante
- **THEN** elle n’est pas annoncée comme supportée par le profil livré

### Requirement: Garanties du socle conservées dans le profil initial

Le profil initial MUST satisfaire les capacités obligatoires P0 et composer les modules de gestion `pixs.agent` (PA hors PZT) et `pixs.pzt` (PZT), ainsi que le module DNS essentiel côté PBO. La désactivation réseau MUST NOT retirer ces modules ni affaiblir identité, périmètre, autorisation, audit, gouvernance ou reprise applicables.

#### Scenario: Module essentiel absent

- **WHEN** le réseau est désactivé mais `pixs.agent`, `pixs.pzt` ou le module DNS essentiel manque à la composition PBO
- **THEN** la qualification du profil échoue avant publication

### Requirement: Parcours installable et utilisable du profil initial

Le profil MUST permettre installation, première configuration, authentification, administration et opérations Core via contrats publics. Les rôles web, worker et scheduler MUST utiliser le même artefact et la persistance de référence ; une composition de test seule MUST NOT prouver ces parcours.

#### Scenario: Démonstration mémoire seule

- **WHEN** les seuls contrôles réussis utilisent des fixtures mémoire sans installation ni dépendance réelle
- **THEN** le profil ne revendique pas un parcours installable et utilisable qualifié

### Requirement: Capacités non sélectionnées du profil initial

Le profil MUST déclarer les capacités non sélectionnées et leurs limites sans annoncer leurs garanties. Une dépendance obligatoire d’une capacité sélectionnée MUST NOT être exclue sous prétexte d’option ; son absence bloque la qualification concernée.

#### Scenario: Option absente sans dépendance obligatoire

- **WHEN** aucun provider de synchronisation n’est sélectionné et aucune capacité retenue ne l’exige
- **THEN** son absence est déclarée sans annoncer de synchronisation ni affaiblir le P0

### Requirement: Preuve de la composition effectivement distribuée

La preuve initiale MUST relier exigences applicables, scénarios exécutés, composants, versions et artefact installé. Elle MUST distinguer code présent, déclarations, dimensions non évaluées et verdicts observés, sans secret ni compatibilité globale supposée.

#### Scenario: Sources et paquet divergents

- **WHEN** la recette porte sur des sources différentes de celles du paquet proposé
- **THEN** elle ne suffit pas à qualifier la composition distribuée
