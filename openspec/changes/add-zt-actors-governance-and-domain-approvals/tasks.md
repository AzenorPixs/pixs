# Tâches — Z30

Plan ACL-PIXS-2026-10-31-E3-R1, validé le 31 octobre 2026. Toutes les tâches ci-dessous sont futures et non lancées. Les vérifications nécessaires appartiennent à chaque unité avant sa validation ; leur présence ne constitue pas une exécution.

- [ ] 1. Acteurs et participations : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 2. Gouvernance et délégations : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 3. Approbations directionnelles et transitivité : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 4. Représentation mandats et états Core Auth : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 5. Domaines partagés et conformité : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.

## Sous-lots normalisés

Chaque tâche correspond à son sous-lot ; les identifiants sont stables, ne fixent pas seuls l’ordre de réalisation et ne peuvent pas être réutilisés. Aucun alias historique n’existe à la création. Sources : [proposal.md](proposal.md), [design.md](design.md) et [requirements.md](requirements.md).

### Z30-SL01 — Acteurs et participations

- Exigences et version cible propres à cette unité :
  - `zt-instances` — **Acteurs et identité persistante**.
  - `zt-instances` — **Appartenances selon la catégorie**.
  - `zt-instances` — **Participations permanentes et temporaires**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Plusieurs composants sur un hôte** : leur cohébergement ne fusionne ni identités ni habilitations.
  - **Individu dans deux ZT** : chaque ZT décide séparément de ses droits sans copie automatique.
  - **Admission expirée après restauration** : aucun accès n’est réarmé et les données/hôtes ne sont pas supprimés par déduction.

- Tâche rattachée : 1, libellé conservé ci-dessus.
- Objectif et périmètre : Acteurs et participations, limité à Acteurs ZT, participations, gouvernance, délégations, approbations et représentation sous les droits propres aux Domaines.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Approche directionnelle, portée et profondeur bornées ; appartenance non humaine unique ; participations humaines indépendantes ; aucun droit issu de la seule reconnaissance ou d’un mandat expiré. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### Z30-SL02 — Gouvernance et délégations

- Exigences et version cible propres à cette unité :
  - `zt-instances` — **Gouvernance commune et délégations**.
  - `zt-instances` — **Admission administrative et préautorisation**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Délégation limitée** : la création ou modification hors mandat est refusée.
  - **Rejeu d’enrôlement** : il ne crée pas de seconde admission.

- Tâche rattachée : 2, libellé conservé ci-dessus.
- Objectif et périmètre : Gouvernance et délégations, limité à Acteurs ZT, participations, gouvernance, délégations, approbations et représentation sous les droits propres aux Domaines.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Approche directionnelle, portée et profondeur bornées ; appartenance non humaine unique ; participations humaines indépendantes ; aucun droit issu de la seule reconnaissance ou d’un mandat expiré. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### Z30-SL03 — Approbations directionnelles et transitivité

- Exigences et version cible propres à cette unité :
  - `zt-instances` — **Approbations directionnelles et bornées**.
  - `pixs-domains` — **Approbations internes et externes**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Chaîne trop profonde** : la reconnaissance indirecte est refusée même si les autres maillons l’acceptent.
  - **Individu externe reconnu** : la reconnaissance ne crée pas d’identité locale indépendante ou de droits automatiques.

- Tâche rattachée : 3, libellé conservé ci-dessus.
- Objectif et périmètre : Approbations directionnelles et transitivité, limité à Acteurs ZT, participations, gouvernance, délégations, approbations et représentation sous les droits propres aux Domaines.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Approche directionnelle, portée et profondeur bornées ; appartenance non humaine unique ; participations humaines indépendantes ; aucun droit issu de la seule reconnaissance ou d’un mandat expiré. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### Z30-SL04 — Représentation mandats et états Core Auth

- Exigences et version cible propres à cette unité :
  - `zt-instances` — **Représentation explicite et indépendante**.
  - `zt-instances` — **Mandats et session**.
  - `zt-instances` — **Propagation des états autoritatifs**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Relais non mandaté** : ce relais n’établit pas le droit d’agir au nom de l’individu.
  - **Tâche longue** : il reste limité à sa durée et cesse si ses droits ou son mandat sont révoqués.
  - **Auth indisponible** : seules les opérations encore admissibles dans leur continuité bornée restent possibles.

- Tâche rattachée : 4, libellé conservé ci-dessus.
- Objectif et périmètre : Représentation mandats et états Core Auth, limité à Acteurs ZT, participations, gouvernance, délégations, approbations et représentation sous les droits propres aux Domaines.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Approche directionnelle, portée et profondeur bornées ; appartenance non humaine unique ; participations humaines indépendantes ; aucun droit issu de la seule reconnaissance ou d’un mandat expiré. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### Z30-SL05 — Domaines partagés et conformité

- Exigences et version cible propres à cette unité :
  - `zt-instances` — **Politiques durables et autorisations bornées**.
  - `zt-instances` — **Appartenance et preuve sans permission implicite**.
  - `zt-instances` — **Socle et minima opérationnels ZT**.
  - `zt-instances` — **Existence et disponibilité distinctes**.
  - `zt-instances` — **Sortie et révocation séparées**.
  - `pixs-domains` — **Isolation dans un ZT partagé**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Sens inverse** : cette initiation est refusée sans permission distincte.
  - **Logiciel sans droit** : l’action nécessitant les deux permissions est refusée.
  - **Minima partagés** : les minima sont évalués sur ce ZT réel et les périmètres restent séparés.
  - **Rôle déclaré sans exécutant** : la gestion expose l’indisponibilité au lieu d’un DNS actif fictif.
  - **Révocation d’un PZT** : ses accès sont retirés selon le contrat sans bascule automatique de l’Instance en Standalone.
  - **Même ZT sans politique** : l’initiation inter-domaines est refusée.

- Tâche rattachée : 5, libellé conservé ci-dessus.
- Objectif et périmètre : Domaines partagés et conformité, limité à Acteurs ZT, participations, gouvernance, délégations, approbations et représentation sous les droits propres aux Domaines.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Approche directionnelle, portée et profondeur bornées ; appartenance non humaine unique ; participations humaines indépendantes ; aucun droit issu de la seule reconnaissance ou d’un mandat expiré. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.
