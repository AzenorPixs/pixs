## Context

Voir `proposal.md`. Le dépôt ne contient à ce stade aucune application
exécutable. La pile de référence déjà spécifiée associe Django, PostgreSQL et
TanStack, tandis que le Kernel reste agnostique et que `pixs.core` est un
module obligatoire. Les exigences de ce change sont portées par
`initial-application-bootstrap`.

## Goals / Non-Goals

**Goals:**

- Définir une frontière d'implémentation minimale et contrôlable pour la
  première application de développement.
- Permettre une validation intégrée backend/frontend future sans transformer
  le profil local en déploiement de production.
- Préserver les contrats publics, la configuration externe et les frontières
  de sécurité dès le premier artefact.

**Non-Goals:**

- Choisir des versions de Django, TanStack, PostgreSQL ou de leurs outils de
  build.
- Définir une donnée métier, un modèle, une migration, un fournisseur
  d'identité, une politique d'autorisation concrète ou des credentials.
- Implémenter ou démarrer une application, un serveur, un conteneur ou une
  base de données.

## Decisions

### Une capacité de bootstrap distincte

La composition initiale est décrite dans une nouvelle capacité plutôt que par
modification des capacités `reference-runtime`, `api`, `frontend` ou
`runtime`. Ces dernières restent les contrats généraux et stables ; la nouvelle
capacité exprime leur première application conjointe. L'alternative consistant
à disperser les exigences dans ces quatre spécifications rendrait le périmètre
initial difficile à valider et à autoriser séparément.

### Django comme point d'entrée, PostgreSQL et modules comme composition

L'implémentation future aura un unique point d'entrée Django (`manage.py`) et
une composition déclarée chargeant `pixs.kernel` puis `pixs.core`. PostgreSQL
reste une dépendance externe configurée au runtime. Cette décision évite une
configuration de développement autonome ou une substitution implicite par une
base locale. L'alternative d'une base embarquée est écartée car elle diverge de
la source de vérité de référence.

### Composition initiale conforme au P0

La première application de développement est une composition P0. Elle doit
donc démontrer les capacités obligatoires de `reference-composition`, y compris
un composant d'exemple technique, sans introduire de donnée métier, de ressource
de démonstration ni de fournisseur concret. Ce composant démontre la
composition et ses contrats ; il ne constitue pas un domaine fonctionnel.

### Surface HTTP sans comportement métier fictif

La première surface comprend seulement les routes nécessaires à la santé, au
shell et à une API versionnée déclarée. Elle ne fournit ni ressource métier de
démonstration ni autorisation feinte. L'alternative d'un CRUD exemple est
écartée : elle introduirait un domaine, des données et des règles hors du
mandat initial.

### Shell TanStack séparé par contrat HTTP

Le frontend futur est un shell TanStack distinct qui utilise les routes
publiques déclarées. Cette frontière rend testables l'intégration et
l'absence d'accès aux détails Django. L'alternative d'un rendu frontend
directement couplé aux objets internes Django est écartée car elle contredirait
l'orientation API-first.

### Profil local explicitement non productif

Le futur serveur de test est un profil de développement local qui orchestre
explicitement backend et frontend et déclare ses limites. Il ne constitue ni
une topologie de production ni une nouvelle forme de déploiement. Cette
séparation évite que les raccourcis de test deviennent des garanties runtime.

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

- [Le terme « route de base » reste trop large] → La capacité borne la surface
  à santé, shell et API déclarée ; toute route métier nécessite une capacité
  ultérieure.
- [Un profil local peut diverger du runtime de référence] → Les dépendances,
  capacités absentes et frontières de sécurité doivent être déclarées et le
  profil ne peut revendiquer la production.
- [Une configuration de test peut exposer une valeur sensible] → Toutes les
  valeurs de connexion restent runtime ou des références de secrets, y compris
  dans les preuves de validation.
- [Une source de marqueur externe devient indisponible] → Le démarrage NORMAL
  échoue fermé sans rouvrir l'installateur.
- [Un volume élevé d'événements d'administration dégrade le panneau] → La
  capacité et la rétention d'audit sont déclarées et dimensionnées avant mise
  en service.

## Migration Plan

1. Valider et archiver ce change documentaire sans générer d'artefact
   applicatif.
2. Ouvrir un change d'implémentation distinct, après autorisation explicite,
   qui déclinera les tâches, dépendances et validations observables.
3. Si l'implémentation future est refusée ou différée, ne pas appliquer ce
   second change : la capacité reste une cible spécifiée, sans état à migrer ni
   retour arrière technique.
