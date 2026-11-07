# Tâches — Z31

Plan ACL-PIXS-2026-10-31-E3-R1, validé le 31 octobre 2026. Toutes les tâches ci-dessous sont futures et non lancées. Les vérifications nécessaires appartiennent à chaque unité avant sa validation ; leur présence ne constitue pas une exécution.

- [ ] 1. Rôle et politiques de sortie : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 2. Groupes priorités et poids : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 3. Santé bascule et réadmission : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 4. Connexions et absence de fuite : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.

## Sous-lots normalisés

Chaque tâche correspond à son sous-lot ; les identifiants sont stables, ne fixent pas seuls l’ordre de réalisation et ne peuvent pas être réutilisés. Aucun alias historique n’existe à la création. Sources : [proposal.md](proposal.md), [design.md](design.md) et [requirements.md](requirements.md).

### Z31-SL01 — Rôle et politiques de sortie

- Exigences et version cible propres à cette unité :
  - `zt-network-services` — **EZT distinct facultatif et groupes**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **EZT externe** : son inclusion et son usage exigent les autorisations applicables sans le rendre membre local.

- Tâche rattachée : 1, libellé conservé ci-dessus.
- Objectif et périmètre : Rôle et politiques de sortie, limité à Sorties EZT, groupes, priorités, poids, santé par chemin/famille IP, bascule et maintien des connexions.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Aucun EZT admissible signifie trafic bloqué ; les poids ne concernent que le meilleur niveau admissible ; la santé IPv4 ne prouve pas IPv6 ; un EZT externe reste dans son ZT. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### Z31-SL02 — Groupes priorités et poids

- Exigences et version cible propres à cette unité :
  - `zt-network-services` — **Répartition et continuité EZT**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Groupe indisponible** : le trafic concerné reste bloqué sans utiliser une sortie non autorisée.

- Tâche rattachée : 2, libellé conservé ci-dessus.
- Objectif et périmètre : Groupes priorités et poids, limité à Sorties EZT, groupes, priorités, poids, santé par chemin/famille IP, bascule et maintien des connexions.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Aucun EZT admissible signifie trafic bloqué ; les poids ne concernent que le meilleur niveau admissible ; la santé IPv4 ne prouve pas IPv6 ; un EZT externe reste dans son ZT. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### Z31-SL03 — Santé bascule et réadmission

- Exigences et version cible propres à cette unité :
  - `zt-network-services` — **Santé par chemin et famille IP**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Sortie IPv6 rompue** : son admissibilité IPv6 est traitée séparément.

- Tâche rattachée : 3, libellé conservé ci-dessus.
- Objectif et périmètre : Santé bascule et réadmission, limité à Sorties EZT, groupes, priorités, poids, santé par chemin/famille IP, bascule et maintien des connexions.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Aucun EZT admissible signifie trafic bloqué ; les poids ne concernent que le meilleur niveau admissible ; la santé IPv4 ne prouve pas IPv6 ; un EZT externe reste dans son ZT. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### Z31-SL04 — Connexions et absence de fuite

- Exigences et version cible propres à cette unité :
  - `zt-network-services` — **Répartition et continuité EZT**.
  - `zt-network-services` — **Santé par chemin et famille IP**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Groupe indisponible** : le trafic concerné reste bloqué sans utiliser une sortie non autorisée.
  - **Sortie IPv6 rompue** : son admissibilité IPv6 est traitée séparément.

- Tâche rattachée : 4, libellé conservé ci-dessus.
- Objectif et périmètre : Connexions et absence de fuite, limité à Sorties EZT, groupes, priorités, poids, santé par chemin/famille IP, bascule et maintien des connexions.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Aucun EZT admissible signifie trafic bloqué ; les poids ne concernent que le meilleur niveau admissible ; la santé IPv4 ne prouve pas IPv6 ; un EZT externe reste dans son ZT. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.
