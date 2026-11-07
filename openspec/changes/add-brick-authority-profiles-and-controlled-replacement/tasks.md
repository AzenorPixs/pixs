# Tâches — N08

Plan ACL-PIXS-2026-10-31-E3-R1, validé le 31 octobre 2026. Toutes les tâches ci-dessous sont futures et non lancées. Les vérifications nécessaires appartiennent à chaque unité avant sa validation ; leur présence ne constitue pas une exécution.

- [ ] 1. Modes par famille et dérogations : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 2. Synchronisation et prise d’autorité : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 3. Observation secours et démantèlement : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 4. Versions compatibles et conformité : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.

## Sous-lots normalisés

Chaque tâche correspond à son sous-lot ; les identifiants sont stables, ne fixent pas seuls l’ordre de réalisation et ne peuvent pas être réutilisés. Aucun alias historique n’existe à la création. Sources : [proposal.md](proposal.md), [design.md](design.md) et [requirements.md](requirements.md).

### N08-SL01 — Modes par famille et dérogations

- Exigences et version cible propres à cette unité :
  - `brick-redundancy` — **Mode par famille et exceptions**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Exception au mode** : sa justification, sa portée et ses contrôles sont enregistrés avant admission.

- Tâche rattachée : 1, libellé conservé ci-dessus.
- Objectif et périmètre : Modes par famille et dérogations, limité à Contrats transversaux des familles d’autorité, synchronisation, compatibilité et remplacement d’une brique par une nouvelle installation vérifiée.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Une exception est explicite et tracée ; un maître non exclu ne peut pas être doublé ; une règle générique n’abaisse pas les confirmations PG ; le démantèlement respecte les critères déclarés. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### N08-SL02 — Synchronisation et prise d’autorité

- Exigences et version cible propres à cette unité :
  - `brick-redundancy` — **Conditions de reprise propres à la brique**.
  - `brick-redundancy` — **Unicité de l’autorité et automatisation**.
  - `brick-redundancy` — **Références PostgreSQL répliquées et garanties conservées**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Copies requises absentes** : la règle générale d’état partiel ne permet pas de la confirmer.
  - **Ancien maître isolé** : la prise d’autorité reste bloquée selon le contrat du rôle.
  - **Copies distinctes** : elles ne deviennent pas répliques d’une même base par partage de serveur ou de ZT.

- Tâche rattachée : 2, libellé conservé ci-dessus.
- Objectif et périmètre : Synchronisation et prise d’autorité, limité à Contrats transversaux des familles d’autorité, synchronisation, compatibilité et remplacement d’une brique par une nouvelle installation vérifiée.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Une exception est explicite et tracée ; un maître non exclu ne peut pas être doublé ; une règle générique n’abaisse pas les confirmations PG ; le démantèlement respecte les critères déclarés. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### N08-SL03 — Observation secours et démantèlement

- Exigences et version cible propres à cette unité :
  - `brick-redundancy` — **Remplacement sans déplacement direct**.
  - `brick-redundancy` — **Observation et démantèlement**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Second PZT** : il reçoit son identité et son admission propres avant de reprendre le rôle autorisé.
  - **Nouvel actif non vérifié** : le démantèlement n’est pas autorisé sur sa seule activation administrative.

- Tâche rattachée : 3, libellé conservé ci-dessus.
- Objectif et périmètre : Observation secours et démantèlement, limité à Contrats transversaux des familles d’autorité, synchronisation, compatibilité et remplacement d’une brique par une nouvelle installation vérifiée.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Une exception est explicite et tracée ; un maître non exclu ne peut pas être doublé ; une règle générique n’abaisse pas les confirmations PG ; le démantèlement respecte les critères déclarés. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### N08-SL04 — Versions compatibles et conformité

- Exigences et version cible propres à cette unité :
  - `brick-redundancy` — **Unicité de l’autorité et automatisation**.
  - `brick-redundancy` — **Compatibilité de versions par famille**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Ancien maître isolé** : la prise d’autorité reste bloquée selon le contrat du rôle.
  - **Versions hors plage** : la synchronisation protégée ou la reprise concernée reste bloquée avec diagnostic.

- Tâche rattachée : 4, libellé conservé ci-dessus.
- Objectif et périmètre : Versions compatibles et conformité, limité à Contrats transversaux des familles d’autorité, synchronisation, compatibilité et remplacement d’une brique par une nouvelle installation vérifiée.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Une exception est explicite et tracée ; un maître non exclu ne peut pas être doublé ; une règle générique n’abaisse pas les confirmations PG ; le démantèlement respecte les critères déclarés. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.
