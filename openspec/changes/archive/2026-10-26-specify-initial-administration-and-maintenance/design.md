## Context

Ce lot extrait les décisions d'administration historiques du design du
16 septembre 2026. Il reste documentaire et ne réapplique pas d'ancien
comportement dans le canon courant.

## Goals / Non-Goals

**Goals:** séparer les neuf exigences d'administration, maintenance et audit,
préserver intégralement leurs garanties, puis valider et archiver le lot.

**Non-Goals:** modifier le canon, implémenter un comportement, choisir un
fournisseur, recréer une identité ou toucher à une base ou à un secret.

## Decisions

### Deux états de démarrage indépendants

Le marqueur d'installation est externe à PostgreSQL et contrôle l'éligibilité
du démarrage normal ; l'état de configuration initiale est persistant dans la
base et contrôle le passage de `FIRST_CONFIGURATION` à `NORMAL`. Cette
séparation évite qu'une base seule puisse autoriser l'installation ou
réinitialiser implicitement le parcours installateur. L'alternative d'un état
unique en base est écartée car elle ne satisfait pas l'indépendance demandée
pour le marqueur d'installation.

### Opérateur initial, administration root et ACL

Le Super Admin est l'opérateur initial : il est créé ou rattaché comme identité
numérique vérifiée, soumise à une politique d'autorisation déclarée. Il est
l'autorité root du panneau et n'est pas soumis aux ACL pour son seul accès
administratif ; les Administrateurs ordinaires y restent soumis. La
finalisation de la première configuration est une prérogative exclusive du
root. Cette séparation évite qu'une ACL incomplète empêche la sortie d'une
installation, sans accorder ce pouvoir aux Administrateurs ordinaires ni un
bypass hors de cette frontière.

### Références de secrets après l'installation

Les valeurs PostgreSQL saisies de manière interactive ne servent qu'à la
validation et au provisionnement en cours. Avant tout démarrage ultérieur,
l'installation les remplace par des références externes résolues par un
`SecretProvider` autorisé. Cette décision préserve la configuration runtime
sans sérialiser de credential dans un artefact, un diagnostic ou un fichier de
configuration distribué.

### Marqueurs externes vérifiables et échec fermé

Les marqueurs externes d'installation et de désactivation root doivent être
vérifiables par le runtime. Une indisponibilité ou une incohérence ne déclenche
pas l'installateur : elle empêche le démarrage normal. Cette décision évite
qu'un incident de configuration soit interprété comme une autorisation de
reprovisionner une installation existante.

### Audit de toute interaction administrative

L'audit couvre aussi les lectures et la navigation du panneau, et devient un
prérequis de l'accès à une interaction administrative. Les événements restent
minimisés et sans credential. Ce choix privilégie la traçabilité exhaustive au
prix d'une capacité de traitement explicitement dimensionnée.


## Risks / Trade-offs

Les restrictions historiques ne doivent pas être confondues avec les contrats
canoniques actuels. Le réarchivage utilise `--skip-specs` et les empreintes du
canon sont contrôlées avant et après. Les treize exigences et vingt et un
scénarios initiaux sont répartis une seule fois entre les deux lots.

## Migration Plan

1. Préparer les deux lots documentaires sans code ni synchronisation.
2. Vérifier la partition exacte, puis propositions et deltas stricts.
3. Réarchiver les deux lots avec `--skip-specs`, vérifier le canon et publier
   les rapports par archive, sans modification Git.
