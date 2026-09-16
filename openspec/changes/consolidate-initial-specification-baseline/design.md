## Context

Le référentiel actif de Pixs contient 74 capacités. Il est valide en mode
strict, mais la consolidation précédente a seulement établi cette baseline ;
elle n'a pas encore rendu ses relations et sa rédaction homogènes comme si
elles provenaient d'une définition initiale unique.

Le développeur impose de conserver toutes les spécifications, leurs
identifiants et leurs comportements. La consolidation ne peut donc ni
fusionner, ni renommer, ni supprimer une capacité. Elle ne peut pas non plus
introduire une règle fonctionnelle sous couvert d'harmonisation.

## Goals / Non-Goals

**Goals:**

- Obtenir un corpus de 74 capacités cohérent, sans contradiction normative
  confirmée ni frontière implicite.
- Préserver chaque exigence et scénario avant toute réécriture.
- Rendre traçables les dépendances entre la composition P0, le
  provisionnement, l'identité, l'autorisation et les secrets.
- Maintenir la validité `openspec validate --all --strict` à chaque lot.

**Non-Goals:**

- Modifier un comportement fonctionnel, une API, une dépendance ou une
  architecture runtime.
- Fusionner, renommer, déplacer ou supprimer une capacité active.
- Implémenter du code, créer une configuration exécutable ou manipuler des
  secrets.
- Archiver le change sans validation explicite du développeur après revue de
  la matrice de conservation.

## Decisions

### Conservation par matrice avant écriture

Chaque lot de consolidation sera précédé d'une matrice reliant chaque exigence
et scénario source à son emplacement cible. La matrice indiquera si le texte
est conservé textuellement ou reformulé sans changement de sémantique, ainsi
que les dépendances concernées. Une ligne non résolue bloque le lot.

### Capacités stables et frontières explicites

Les 74 répertoires de `openspec/specs/` restent les frontières publiques du
référentiel. Une cohérence inter-capacités s'obtient par des références
croisées normatives et des scénarios compatibles, jamais par l'absorption
silencieuse d'une capacité dans une autre.

### Décisions à reporter vers le change de bootstrap

La composition initiale doit être une composition P0. Le change
`specify-initial-application-bootstrap` devra donc déclarer sa conformité à
`reference-composition`, y compris le composant d'exemple requis, sans
introduire de donnée métier fictive ni de dépendance de production.

### Opérateur initial et secrets externes

Le Super Admin doit être l'opérateur initial. Sa création ou son rattachement
devra exprimer une identité numérique vérifiée et une politique d'autorisation
déclarée ; le bypass ACL administratif reste limité à la frontière explicitée
par la capacité d'administration. Les paramètres PostgreSQL recueillis par
l'INSTALLER devront être convertis en références externes vers un
`SecretProvider`, sans sérialisation durable de leur valeur. Ces exigences
seront ajoutées au change de bootstrap après validation de son périmètre.

## Risks / Trade-offs

- Une reformulation peut altérer involontairement une obligation normative.
  La matrice, les scénarios et la validation stricte constituent le contrôle
  minimal, avec revue explicite des écarts.
- Les interdépendances peuvent révéler une évolution fonctionnelle réelle.
  Celle-ci sera isolée et soumise au développeur, sans être intégrée à ce
  change de consolidation.
- Une consolidation complète est volumineuse. Les lots seront indépendants,
  réversibles et limités à des familles cohérentes de capacités.

## Migration Plan

1. Établir et faire valider la matrice de conservation de toutes les capacités.
2. Isoler les changements fonctionnels nécessaires dans des changes distincts.
3. Soumettre les lots de consolidation documentaire au développeur avant toute
   modification des spécifications actives.
4. Vérifier après chaque lot l'absence de changement fonctionnel, d'API, de
   dépendance ou de code.
5. Présenter la baseline consolidée et la matrice finale au développeur.
6. Archiver uniquement après validation explicite du développeur.
