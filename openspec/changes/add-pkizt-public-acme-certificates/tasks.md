# Tâches — Z29

Plan ACL-PIXS-2026-10-31-E3-R1, validé le 31 octobre 2026. Toutes les tâches ci-dessous sont futures et non lancées. Les vérifications nécessaires appartiennent à chaque unité avant sa validation ; leur présence ne constitue pas une exécution.

- [ ] 1. Comptes certificats et clés protégées : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 2. Challenges DNS HTTP et TLS : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 3. Coordonnateur unique et reprise : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 4. Renouvellement ARI et déploiement vérifié : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.

## Sous-lots normalisés

Chaque tâche correspond à son sous-lot ; les identifiants sont stables, ne fixent pas seuls l’ordre de réalisation et ne peuvent pas être réutilisés. Aucun alias historique n’existe à la création. Sources : [proposal.md](proposal.md), [design.md](design.md) et [requirements.md](requirements.md).

### Z29-SL01 — Comptes certificats et clés protégées

- Exigences et version cible propres à cette unité :
  - `zt-pki` — **ACME public et génération de clés**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Demande publique** : PKIZT conserve la clé privée et soumet la demande contenant la clé publique à signer.

- Tâche rattachée : 1, libellé conservé ci-dessus.
- Objectif et périmètre : Comptes certificats et clés protégées, limité à Cycle des certificats publics ACME, challenges, coordination unique, reprise et renouvellement anticipé avec preuve de déploiement.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Un seul coordonnateur est actif par certificat ; la clé est générée côté PKIZT ; certificat obtenu et certificat effectivement servi sont vérifiés séparément. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### Z29-SL02 — Challenges DNS HTTP et TLS

- Exigences et version cible propres à cette unité :
  - `zt-pki` — **Challenges et coordination ACME**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Deux coordonnateurs** : un seul est admissible à coordonner les opérations courantes.

- Tâche rattachée : 2, libellé conservé ci-dessus.
- Objectif et périmètre : Challenges DNS HTTP et TLS, limité à Cycle des certificats publics ACME, challenges, coordination unique, reprise et renouvellement anticipé avec preuve de déploiement.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Un seul coordonnateur est actif par certificat ; la clé est générée côté PKIZT ; certificat obtenu et certificat effectivement servi sont vérifiés séparément. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### Z29-SL03 — Coordonnateur unique et reprise

- Exigences et version cible propres à cette unité :
  - `zt-pki` — **Challenges et coordination ACME**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Deux coordonnateurs** : un seul est admissible à coordonner les opérations courantes.

- Tâche rattachée : 3, libellé conservé ci-dessus.
- Objectif et périmètre : Coordonnateur unique et reprise, limité à Cycle des certificats publics ACME, challenges, coordination unique, reprise et renouvellement anticipé avec preuve de déploiement.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Un seul coordonnateur est actif par certificat ; la clé est générée côté PKIZT ; certificat obtenu et certificat effectivement servi sont vérifiés séparément. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### Z29-SL04 — Renouvellement ARI et déploiement vérifié

- Exigences et version cible propres à cette unité :
  - `zt-pki` — **Renouvellement anticipé et déploiement vérifié**.
  - `zt-pki` — **Remise TLS ciblée aux RPZT**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Certificat non servi** : le déploiement reste incomplet et ne peut être annoncé réussi.
  - **Publication partagée explicitement** : chaque destinataire habilité reçoit sa propre protection sans rendre la clé lisible aux autres acteurs.

- Tâche rattachée : 4, libellé conservé ci-dessus.
- Objectif et périmètre : Renouvellement ARI et déploiement vérifié, limité à Cycle des certificats publics ACME, challenges, coordination unique, reprise et renouvellement anticipé avec preuve de déploiement.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : Un seul coordonnateur est actif par certificat ; la clé est générée côté PKIZT ; certificat obtenu et certificat effectivement servi sont vérifiés séparément. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.
