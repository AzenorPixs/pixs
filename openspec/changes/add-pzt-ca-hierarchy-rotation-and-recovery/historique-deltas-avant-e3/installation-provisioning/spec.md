
## ADDED Requirements

### Requirement: Amorçage technique borné du temps avant transport protégé

MUST appliquer intégralement toutes les clauses, bornes et conditions du contrat détaillé ci-dessous, sans retrait ni réinterprétation.

##### Contrat détaillé — Amorçage temps borné

L’amorçage du temps avant PZT et avant la base applicative MUST demeurer borné, acyclique et autorisé hors base applicative, sans droit métier et sans réseau direct PBO vers PA hors PZT. Le service préfourni, une horloge matérielle qualifiée ou une source indépendante qualifiée MAY être utilisé. Le service NTS MUST NOT prouver à lui seul le temps universel initial. Tout téléchargement des prérequis par un canal chiffré qui exigerait une heure non encore établie MUST NOT être entrepris. Les opérations entre PBO et PA MUST conserver exclusivement le transport protégé existant.

#### Scenario: Amorçage sans heure connue

- **WHEN** aucune heure universelle qualifiée n’est disponible avant le transport protégé
- **THEN** la procédure bornée s’applique ou la branche est refusée sans auto-autorité par statut
