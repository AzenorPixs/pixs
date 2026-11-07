# Tâches — C96

Plan ACL-PIXS-2026-10-31-E3-R1, validé le 31 octobre 2026. Toutes les tâches ci-dessous sont futures et non lancées. Les vérifications nécessaires appartiennent à chaque unité avant sa validation ; leur présence ne constitue pas une exécution.

- [ ] 1. Individus et identités multiples : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 2. Contextes Instance Domaine Tenant : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 3. Habilitations globales et locales : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 4. Transferts et retrait de domaine : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 5. Migration et conformité : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.

## Sous-lots normalisés

Chaque tâche correspond à son sous-lot ; les identifiants sont stables, ne fixent pas seuls l’ordre de réalisation et ne peuvent pas être réutilisés. Aucun alias historique n’existe à la création. Sources : [proposal.md](proposal.md), [design.md](design.md) et [requirements.md](requirements.md).

### C96-SL01 — Individus et identités multiples

- Exigences et version cible propres à cette unité :
  - `core` — **Profil minimal des utilisateurs et identités numériques v1**.
  - `core` — **Liaison utilisateur identité explicite et unique**.
  - `core` — **Représentation minimale des comptes de service**.
  - `core` — **Moyens multiples sans multiplication implicite des identités**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Identité minimale valide** : leurs représentations minimales sont acceptées sans exiger une authentification ou une liaison entre eux
  - **Identifiant ou vocabulaire invalide** : la validation refuse la représentation concernée
  - **Plusieurs identités du même individu** : les deux liaisons sont admises avec profils et droits distincts.
  - **Identité liée à deux individus** : la liaison est refusée.
  - **Compte de service sans utilisateur** : sa représentation de compte de service est acceptée sans établir une authentification ni une autorisation
  - **Passkey et principal pour une identité** : son UUID et ses habilitations restent inchangés sans compte supplémentaire.

- Tâche rattachée : 1, libellé conservé ci-dessus.
- Objectif et périmètre : Individus et identités multiples, limité à Individu commun, identités multiples par Domaine, contextes propriétaires, habilitations et transferts fonctionnels contrôlés.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Plusieurs identités du même individu restent indépendantes ; une identité n’est pas liée à deux individus ; le propriétaire est unique et aucune permission n’est copiée automatiquement. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### C96-SL02 — Contextes Instance Domaine Tenant

- Exigences et version cible propres à cette unité :
  - `scope-context` — **Tenant racine et parenté unique**.
  - `scope-context` — **Propriété canonique unique**.
  - `scope-context` — **Contexte immuable propagé avant autorisation**.
  - `scope-context` — **Propagation et frontière d'autorisation du ScopeContext**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Cycle de scopes refusé** : la déclaration est refusée avant activation.
  - **Scope sans tenant cohérent refusé** : la mutation est refusée sans accès à un autre périmètre.
  - **Contexte TENANT sans tenant refusé** : sa structure est refusée.
  - **Contexte PLATFORM avec identifiants refusé** : sa structure est refusée.
  - **Nouveau parcours Domaine sur contexte incomplet** : l’accès est bloqué sans l’inférer d’un champ client ou d’une plateforme implicite.
  - **Élargissement implicite refusé** : le contexte canonique prévaut et tout accès hors périmètre est refusé et audité
  - **Contexte PLATFORM sans identifiants accepté sans octroyer permission** : sa structure est acceptée sans octroyer aucune permission implicite
  - **Accès plateforme sans permission refusé et audité** : l'accès est refusé et audité

- Tâche rattachée : 2, libellé conservé ci-dessus.
- Objectif et périmètre : Contextes Instance Domaine Tenant, limité à Individu commun, identités multiples par Domaine, contextes propriétaires, habilitations et transferts fonctionnels contrôlés.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Plusieurs identités du même individu restent indépendantes ; une identité n’est pas liée à deux individus ; le propriétaire est unique et aucune permission n’est copiée automatiquement. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### C96-SL03 — Habilitations globales et locales

- Exigences et version cible propres à cette unité :
  - `scope-context` — **Périmètre explicite du Super Admin**.
  - `pixs-instance` — **Administration globale par identités habilitées**.
  - `pixs-instance` — **Habilitations Instance et domaines**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Accord tenant sans changement de propriété** : le ScopeContext reste TENANT avec le tenant A et la ressource conserve sa propriété canonique
  - **Domaine d’authentification non habilité** : la demande est refusée malgré la validité de son authentification.
  - **PBO mutualisé** : son action reste limitée aux périmètres explicitement autorisés.

- Tâche rattachée : 3, libellé conservé ci-dessus.
- Objectif et périmètre : Habilitations globales et locales, limité à Individu commun, identités multiples par Domaine, contextes propriétaires, habilitations et transferts fonctionnels contrôlés.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Plusieurs identités du même individu restent indépendantes ; une identité n’est pas liée à deux individus ; le propriétaire est unique et aucune permission n’est copiée automatiquement. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### C96-SL04 — Transferts et retrait de domaine

- Exigences et version cible propres à cette unité :
  - `pixs-domains` — **Transferts fonctionnels contrôlés V1**.
  - `pixs-domains` — **Structures organisationnelles non transférables V1**.
  - `pixs-domains` — **Retrait du premier Domaine**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Tenant transféré** : son identité est conservée, son propriétaire est unique et les habilitations de destination sont réévaluées.
  - **Transfert de département** : elle est refusée comme hors périmètre sans modifier les structures source ou cible.
  - **Dernier Domaine** : il est refusé sans retour implicite en Standalone.

- Tâche rattachée : 4, libellé conservé ci-dessus.
- Objectif et périmètre : Transferts et retrait de domaine, limité à Individu commun, identités multiples par Domaine, contextes propriétaires, habilitations et transferts fonctionnels contrôlés.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Plusieurs identités du même individu restent indépendantes ; une identité n’est pas liée à deux individus ; le propriétaire est unique et aucune permission n’est copiée automatiquement. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### C96-SL05 — Migration et conformité

- Exigences et version cible propres à cette unité :
  - `core` — **Liaison utilisateur identité explicite et unique**.
  - `core` — **Évolution versionnée du lien individu identités**.
  - `pixs-instance` — **Références PG avant et après Domaine**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Plusieurs identités du même individu** : les deux liaisons sont admises avec profils et droits distincts.
  - **Identité liée à deux individus** : la liaison est refusée.
  - **Contrat v1 existant** : sa preuve reste bornée à cette version et ne démontre pas la nouvelle cardinalité Domaine
  - **Activation du premier Domaine** : l’identité de Domaine devient utilisable selon son profil et l’ancienne identité d’Instance ne reste pas une autre voie de connexion.

- Tâche rattachée : 5, libellé conservé ci-dessus.
- Objectif et périmètre : Migration et conformité, limité à Individu commun, identités multiples par Domaine, contextes propriétaires, habilitations et transferts fonctionnels contrôlés.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Plusieurs identités du même individu restent indépendantes ; une identité n’est pas liée à deux individus ; le propriétaire est unique et aucune permission n’est copiée automatiquement. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.
