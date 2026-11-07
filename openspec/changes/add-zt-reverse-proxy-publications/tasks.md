# Tâches — Z32

Plan ACL-PIXS-2026-10-31-E3-R1, validé le 31 octobre 2026. Toutes les tâches ci-dessous sont futures et non lancées. Les vérifications nécessaires appartiennent à chaque unité avant sa validation ; leur présence ne constitue pas une exécution.

- [ ] 1. Publications et autorisations : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 2. HTTP HTTPS WebSocket et modes TLS : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 3. Remise protégée des éléments TLS : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 4. Actifs multiples et orientation : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 5. Conformité sans authentification utilisateur au proxy : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.

## Sous-lots normalisés

Chaque tâche correspond à son sous-lot ; les identifiants sont stables, ne fixent pas seuls l’ordre de réalisation et ne peuvent pas être réutilisés. Aucun alias historique n’existe à la création. Sources : [proposal.md](proposal.md), [design.md](design.md) et [requirements.md](requirements.md).

### Z32-SL01 — Publications et autorisations

- Exigences et version cible propres à cette unité :
  - `zt-network-services` — **RPZT facultatif et actifs multiples**.
  - `zt-network-services` — **Authentification au service cible**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Deux RPZT** : la présence des deux ne prouve pas à elle seule une orientation ou bascule fonctionnelle.
  - **Service public non déclaré** : elle n’est pas admise comme publication protégée par le seul RPZT.

- Tâche rattachée : 1, libellé conservé ci-dessus.
- Objectif et périmètre : Publications et autorisations, limité à Publications HTTP/HTTPS/WebSocket par RPZT, modes TLS et remise protégée des éléments nécessaires à chaque exécutant.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : RPZT reste désactivé par défaut ; plusieurs actifs n’impliquent pas une orientation fonctionnelle ; les modes TLS sont explicites et seuls les destinataires habilités reçoivent les éléments TLS. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### Z32-SL02 — HTTP HTTPS WebSocket et modes TLS

- Exigences et version cible propres à cette unité :
  - `zt-network-services` — **RPZT facultatif et actifs multiples**.
  - `zt-network-services` — **TLS par publication et distribution PKIZT**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Deux RPZT** : la présence des deux ne prouve pas à elle seule une orientation ou bascule fonctionnelle.
  - **TLS passthrough** : le service termine TLS et RPZT ne prétend pas authentifier l’utilisateur.

- Tâche rattachée : 2, libellé conservé ci-dessus.
- Objectif et périmètre : HTTP HTTPS WebSocket et modes TLS, limité à Publications HTTP/HTTPS/WebSocket par RPZT, modes TLS et remise protégée des éléments nécessaires à chaque exécutant.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : RPZT reste désactivé par défaut ; plusieurs actifs n’impliquent pas une orientation fonctionnelle ; les modes TLS sont explicites et seuls les destinataires habilités reçoivent les éléments TLS. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### Z32-SL03 — Remise protégée des éléments TLS

- Exigences et version cible propres à cette unité :
  - `zt-pki` — **Remise TLS ciblée aux RPZT**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Publication partagée explicitement** : chaque destinataire habilité reçoit sa propre protection sans rendre la clé lisible aux autres acteurs.

- Tâche rattachée : 3, libellé conservé ci-dessus.
- Objectif et périmètre : Remise protégée des éléments TLS, limité à Publications HTTP/HTTPS/WebSocket par RPZT, modes TLS et remise protégée des éléments nécessaires à chaque exécutant.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : RPZT reste désactivé par défaut ; plusieurs actifs n’impliquent pas une orientation fonctionnelle ; les modes TLS sont explicites et seuls les destinataires habilités reçoivent les éléments TLS. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### Z32-SL04 — Actifs multiples et orientation

- Exigences et version cible propres à cette unité :
  - `zt-network-services` — **RPZT facultatif et actifs multiples**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Deux RPZT** : la présence des deux ne prouve pas à elle seule une orientation ou bascule fonctionnelle.

- Tâche rattachée : 4, libellé conservé ci-dessus.
- Objectif et périmètre : Actifs multiples et orientation, limité à Publications HTTP/HTTPS/WebSocket par RPZT, modes TLS et remise protégée des éléments nécessaires à chaque exécutant.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : RPZT reste désactivé par défaut ; plusieurs actifs n’impliquent pas une orientation fonctionnelle ; les modes TLS sont explicites et seuls les destinataires habilités reçoivent les éléments TLS. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### Z32-SL05 — Conformité sans authentification utilisateur au proxy

- Exigences et version cible propres à cette unité :
  - `zt-network-services` — **Authentification au service cible**.
  - `zt-network-services` — **TLS par publication et distribution PKIZT**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Service public non déclaré** : elle n’est pas admise comme publication protégée par le seul RPZT.
  - **TLS passthrough** : le service termine TLS et RPZT ne prétend pas authentifier l’utilisateur.

- Tâche rattachée : 5, libellé conservé ci-dessus.
- Objectif et périmètre : Conformité sans authentification utilisateur au proxy, limité à Publications HTTP/HTTPS/WebSocket par RPZT, modes TLS et remise protégée des éléments nécessaires à chaque exécutant.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : RPZT reste désactivé par défaut ; plusieurs actifs n’impliquent pas une orientation fonctionnelle ; les modes TLS sont explicites et seuls les destinataires habilités reçoivent les éléments TLS. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.
