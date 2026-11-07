# Tâches — PA12

Plan ACL-PIXS-2026-10-31-E3-R1, validé le 31 octobre 2026. Toutes les tâches ci-dessous sont futures et non lancées. Les vérifications nécessaires appartiennent à chaque unité avant sa validation ; leur présence ne constitue pas une exécution.

- [ ] 1. Résolution et ciblage des politiques : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 2. Application système et utilisateur : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 3. Jonction session hors ligne et redémarrage : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 4. Qualification des profils et conflits : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.

## Sous-lots normalisés

Chaque tâche correspond à son sous-lot ; les identifiants sont stables, ne fixent pas seuls l’ordre de réalisation et ne peuvent pas être réutilisés. Aucun alias historique n’existe à la création. Sources : [proposal.md](proposal.md), [design.md](design.md) et [requirements.md](requirements.md).

### PA12-SL01 — Résolution et ciblage des politiques

- Exigences et version cible propres à cette unité :
  - `managed-device-policies` — **Politiques communes et spécifiques**.
  - `managed-device-policies` — **Priorités et contradictions**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Règle propre à Windows** : l’application Linux ne prétend pas avoir appliqué cette règle native.
  - **Deux valeurs au même niveau** : l’écart est signalé et aucune valeur n’est choisie par ordre d’arrivée.

- Tâche rattachée : 1, libellé conservé ci-dessus.
- Objectif et périmètre : Résolution et ciblage des politiques, limité à Politiques de poste et d’utilisateur pour Linux/Windows, serveurs Linux, gestion ZT distincte de la jonction et parcours hors ligne/redémarrage.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Les contradictions à priorité égale sont signalées ; l’hôte géré dans ZT peut rester sans jonction d’authentification ; hors ligne et redémarrage suivent un profil, avec manuel par défaut. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### PA12-SL02 — Application système et utilisateur

- Exigences et version cible propres à cette unité :
  - `managed-device-policies` — **Cibles V1 et exécutants locaux**.
  - `managed-device-policies` — **Application par PA et état vérifié**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Poste administré** : les exécutants locaux sont vérifiés sans le transformer en LZT ou KZT.
  - **Configuration reçue sans effet** : PBO affiche l’échec sans état appliqué fictif.

- Tâche rattachée : 2, libellé conservé ci-dessus.
- Objectif et périmètre : Application système et utilisateur, limité à Politiques de poste et d’utilisateur pour Linux/Windows, serveurs Linux, gestion ZT distincte de la jonction et parcours hors ligne/redémarrage.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Les contradictions à priorité égale sont signalées ; l’hôte géré dans ZT peut rester sans jonction d’authentification ; hors ligne et redémarrage suivent un profil, avec manuel par défaut. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### PA12-SL03 — Jonction session hors ligne et redémarrage

- Exigences et version cible propres à cette unité :
  - `managed-device-policies` — **Gestion ZT et jonction d’authentification distinctes**.
  - `managed-device-policies` — **Session hors ligne bornée**.
  - `managed-device-policies` — **Rotation des secrets machine et services**.
  - `managed-device-policies` — **Redémarrage par profil et conclusion après reprise**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Hôte tiers géré** : PA peut gérer ses capacités autorisées tandis que les utilisateurs conservent l’authentification configurée sur l’hôte.
  - **Pas de profil hors ligne** : aucune nouvelle permission de connexion locale n’est déduite de la panne.
  - **Rotation native autorisée** : elle suit son profil et sa cohérence contrôleurs sans autoriser un changement natif du mot de passe individuel.
  - **Jonction exigeant redémarrage** : l’opération reste à terminer jusqu’aux contrôles après reprise.

- Tâche rattachée : 3, libellé conservé ci-dessus.
- Objectif et périmètre : Jonction session hors ligne et redémarrage, limité à Politiques de poste et d’utilisateur pour Linux/Windows, serveurs Linux, gestion ZT distincte de la jonction et parcours hors ligne/redémarrage.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Les contradictions à priorité égale sont signalées ; l’hôte géré dans ZT peut rester sans jonction d’authentification ; hors ligne et redémarrage suivent un profil, avec manuel par défaut. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### PA12-SL04 — Qualification des profils et conflits

- Exigences et version cible propres à cette unité :
  - `managed-device-policies` — **Cibles V1 et exécutants locaux**.
  - `managed-device-policies` — **Priorités et contradictions**.
  - `managed-device-policies` — **Application par PA et état vérifié**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Poste administré** : les exécutants locaux sont vérifiés sans le transformer en LZT ou KZT.
  - **Deux valeurs au même niveau** : l’écart est signalé et aucune valeur n’est choisie par ordre d’arrivée.
  - **Configuration reçue sans effet** : PBO affiche l’échec sans état appliqué fictif.

- Tâche rattachée : 4, libellé conservé ci-dessus.
- Objectif et périmètre : Qualification des profils et conflits, limité à Politiques de poste et d’utilisateur pour Linux/Windows, serveurs Linux, gestion ZT distincte de la jonction et parcours hors ligne/redémarrage.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Les contradictions à priorité égale sont signalées ; l’hôte géré dans ZT peut rester sans jonction d’authentification ; hors ligne et redémarrage suivent un profil, avec manuel par défaut. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.
