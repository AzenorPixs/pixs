
## ADDED Requirements

### Requirement: Gestion du service de temps par PA et pixs.agent

MUST appliquer intégralement toutes les clauses, bornes et conditions du contrat détaillé ci-dessous, sans retrait ni réinterprétation.

##### Contrat détaillé — Service de temps PA

Le service de temps système MUST être installé, réutilisé, configuré et supervisé par PA sous politique explicite, capacité catalogue fermé et mandat de cible exacte. PA MUST conserver un propriétaire unique par horloge système. pixs.agent MUST gérer les opérations PA hors responsabilité du réseau PZT, et tous les échanges PBO vers PA MUST passer par PZT ; le temps amont demeure un service système selon profil et MUST NOT devenir un canal de commande PBO vers PA. PA MUST NOT modifier l’horloge d’un hôte partagé depuis un conteneur LXC. Sur Linux, chrony demeure retenu avec ses dépendances déclarées. Les autres profils MUST qualifier leurs adaptateurs avant activation. Dans une image isolée, le paquet est fourni par l’image sans mutation de l’hôte. Un service NTP local MAY être utilisé seulement lorsque la topologie l’exige et sous profil déclaré. Aucun montage, aucun changement de privilège et aucune discipline supplémentaire ne sont induits. Les fonctions indépendantes du temps MUST pouvoir continuer pendant une dégradation.

#### Scenario: Mandat de cible exacte pour le service de temps

- **WHEN** PA reçoit un mandat de cible exacte avec un profil valide
- **THEN** PA installe ou réutilise le service déclaré, vérifie l’état appliqué et refuse toute cible étrangère ou capacité hors catalogue
