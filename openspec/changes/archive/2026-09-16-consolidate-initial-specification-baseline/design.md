## Context

Le référentiel actif de Pixs contient 76 capacités. Il est valide en mode
strict, mais la consolidation précédente a seulement établi cette baseline ;
elle n'a pas encore rendu ses relations et sa rédaction homogènes comme si
elles provenaient d'une définition initiale unique.

Le développeur impose de conserver toutes les spécifications, leurs
identifiants et leurs comportements. La consolidation ne peut donc ni
fusionner, ni renommer, ni supprimer une capacité. Elle ne peut pas non plus
introduire une règle fonctionnelle sous couvert d'harmonisation.

## Goals / Non-Goals

**Goals:**

- Établir un corpus documenté de 76 capacités cohérent, sans
  contradiction normative confirmée ni frontière implicite.
- Préserver chaque exigence et scénario avant toute réécriture.
- Rendre traçables les dépendances entre la composition P0, le
  provisionnement, l'identité, l'autorisation et les secrets.
- Maintenir la validité `openspec validate --all --strict` à chaque lot et
  avant la synchronisation finale.

**Non-Goals:**

- Modifier un comportement fonctionnel, une API, une dépendance ou une
  architecture runtime.
- Fusionner, renommer, déplacer ou supprimer une capacité active.
- Implémenter du code, créer une configuration exécutable ou manipuler des
  secrets.
- Archiver le change sans validation explicite du développeur après revue de
  la matrice de conservation.

## Decisions

### Conservation par matrice sans synchronisation

La matrice relie chaque exigence et scénario source à son emplacement cible et
indique leur conservation textuelle ainsi que les dépendances concernées. Une
ligne non résolue bloque la clôture du change. Ce change ne synchronise aucune
modification vers les capacités actives.

### Capacités stables et frontières explicites

Les 76 répertoires de `openspec/specs/` restent les frontières publiques du
référentiel. Une cohérence inter-capacités s'obtient par des références
croisées normatives et des scénarios compatibles, jamais par l'absorption
silencieuse d'une capacité dans une autre.

### Relations déjà portées par le change de bootstrap

La composition initiale est portée par le change
`specify-initial-application-bootstrap`, qui déclare sa conformité à
`reference-composition`, y compris le composant d'exemple requis, sans
introduire de donnée métier fictive ni de dépendance de production.

### Opérateur initial et secrets externes

Le Super Admin est l'opérateur initial. Sa création ou son rattachement doit
exprimer une identité numérique vérifiée et une politique d'autorisation
déclarée ; le bypass ACL administratif reste limité à la frontière explicitée
par la capacité d'administration. Les paramètres PostgreSQL recueillis par
l'INSTALLER doivent être convertis en références externes vers un
`SecretProvider`, sans sérialisation durable de leur valeur. Ces exigences
sont portées par le change de bootstrap et restent hors de toute réécriture
fonctionnelle de la consolidation.

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

1. Établir et valider la matrice de conservation de toutes les capacités.
2. Isoler les changements fonctionnels nécessaires dans des changes distincts.
3. Vérifier que la matrice ne révèle aucun changement fonctionnel, d'API, de
   dépendance ou de code à synchroniser.
4. Valider la cohérence documentaire du change et de la baseline.
5. Présenter la baseline consolidée et la matrice finale au développeur.
7. Archiver uniquement après validation explicite du développeur.
