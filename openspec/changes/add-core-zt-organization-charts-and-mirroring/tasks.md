# Tâches — C95

Plan ACL-PIXS-2026-10-31-E3-R1, validé le 31 octobre 2026. Toutes les tâches ci-dessous sont futures et non lancées. Les vérifications nécessaires appartiennent à chaque unité avant sa validation ; leur présence ne constitue pas une exécution.

- [ ] 1. Référentiels et hiérarchies : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 2. Source et périmètres des miroirs : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 3. Affiliations et réévaluation des droits : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 4. Trois volets PBO et conformité : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.

## Sous-lots normalisés

Chaque tâche correspond à son sous-lot ; les identifiants sont stables, ne fixent pas seuls l’ordre de réalisation et ne peuvent pas être réutilisés. Aucun alias historique n’existe à la création. Sources : [proposal.md](proposal.md), [design.md](design.md) et [requirements.md](requirements.md).

### C95-SL01 — Référentiels et hiérarchies

- Exigences et version cible propres à cette unité :
  - `organization-charts` — **Trois référentiels propriétaires**.
  - `organization-charts` — **Hiérarchie structurelle et affiliations**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **ZT partagé** : leurs volets Core restent propres et les périmètres structurels sont présentés dans le ZT commun.
  - **Deux parents structurels** : la mutation est refusée sans empêcher les affiliations transversales autorisées.

- Tâche rattachée : 1, libellé conservé ci-dessus.
- Objectif et périmètre : Référentiels et hiérarchies, limité à Organigrammes organisationnel et fonctionnel Core, structure ZT et miroitage gouverné, présentés en trois volets distincts.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Une source explicite est vérifiée par périmètre de miroir ; les cycles et parents multiples sont refusés ; structure seule est le défaut ; aucun droit ou admission n’est copié implicitement. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### C95-SL02 — Source et périmètres des miroirs

- Exigences et version cible propres à cette unité :
  - `organization-charts` — **Source explicite de chaque miroir**.
  - `organization-charts` — **Structure seule par défaut**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Écriture sur miroir** : l’interface applique le contrat de la source ou refuse l’écriture concurrente.
  - **Miroir standard** : les seules structures et relations hiérarchiques autorisées sont reprises.

- Tâche rattachée : 2, libellé conservé ci-dessus.
- Objectif et périmètre : Source et périmètres des miroirs, limité à Organigrammes organisationnel et fonctionnel Core, structure ZT et miroitage gouverné, présentés en trois volets distincts.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Une source explicite est vérifiée par périmètre de miroir ; les cycles et parents multiples sont refusés ; structure seule est le défaut ; aucun droit ou admission n’est copié implicitement. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### C95-SL03 — Affiliations et réévaluation des droits

- Exigences et version cible propres à cette unité :
  - `organization-charts` — **Hiérarchie structurelle et affiliations**.
  - `organization-charts` — **Admission et droits séparés du miroir**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Deux parents structurels** : la mutation est refusée sans empêcher les affiliations transversales autorisées.
  - **Affiliation vers un ZT** : aucune participation effective ni autorisation ZT n’est déduite.

- Tâche rattachée : 3, libellé conservé ci-dessus.
- Objectif et périmètre : Affiliations et réévaluation des droits, limité à Organigrammes organisationnel et fonctionnel Core, structure ZT et miroitage gouverné, présentés en trois volets distincts.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Une source explicite est vérifiée par périmètre de miroir ; les cycles et parents multiples sont refusés ; structure seule est le défaut ; aucun droit ou admission n’est copié implicitement. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### C95-SL04 — Trois volets PBO et conformité

- Exigences et version cible propres à cette unité :
  - `organization-charts` — **Trois référentiels propriétaires**.
  - `organization-charts` — **Admission et droits séparés du miroir**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **ZT partagé** : leurs volets Core restent propres et les périmètres structurels sont présentés dans le ZT commun.
  - **Affiliation vers un ZT** : aucune participation effective ni autorisation ZT n’est déduite.

- Tâche rattachée : 4, libellé conservé ci-dessus.
- Objectif et périmètre : Trois volets PBO et conformité, limité à Organigrammes organisationnel et fonctionnel Core, structure ZT et miroitage gouverné, présentés en trois volets distincts.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Une source explicite est vérifiée par périmètre de miroir ; les cycles et parents multiples sont refusés ; structure seule est le défaut ; aucun droit ou admission n’est copié implicitement. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.
