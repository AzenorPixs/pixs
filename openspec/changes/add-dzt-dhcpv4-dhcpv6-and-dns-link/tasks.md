# Tâches — Z28

Plan ACL-PIXS-2026-10-31-E3-R1, validé le 31 octobre 2026. Toutes les tâches ci-dessous sont futures et non lancées. Les vérifications nécessaires appartiennent à chaque unité avant sa validation ; leur présence ne constitue pas une exécution.

- [ ] 1. Référence DZT et génération DHCP : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 2. Baux et propriétaire unique par pool : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 3. Publication DNS liée aux baux : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 4. Activation et reprise qualifiées : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.

## Sous-lots normalisés

Chaque tâche correspond à son sous-lot ; les identifiants sont stables, ne fixent pas seuls l’ordre de réalisation et ne peuvent pas être réutilisés. Aucun alias historique n’existe à la création. Sources : [proposal.md](proposal.md), [design.md](design.md) et [requirements.md](requirements.md).

### Z28-SL01 — Référence DZT et génération DHCP

- Exigences et version cible propres à cette unité :
  - `zt-dns-dhcp` — **DZT obligatoire et base commune indépendante**.
  - `zt-dns-dhcp` — **Préparation et mise à jour PA configuration PZT**.
  - `zt-dns-dhcp` — **Configuration entièrement régénérable**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Plusieurs DZT** : elle rejoint le même référentiel logique sans source de configuration concurrente.
  - **Mise à jour BIND** : DZT revalide la compatibilité, réapplique si nécessaire la configuration et vérifie le fonctionnement avant succès du service.
  - **Régénération après panne** : l’état natif durable n’est ni effacé ni supposé recréé par la configuration seule.

- Tâche rattachée : 1, libellé conservé ci-dessus.
- Objectif et périmètre : Référence DZT et génération DHCP, limité à DHCPv4/v6 du DZT, référence commune DNS/DHCP, conservation des baux, propriétaire par pool et liaison DHCP–DNS.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : DHCP est désactivé par défaut ; un pool n’a qu’un allocateur actif ; une reprise sans baux fiables est refusée ; réussite du bail et publication DNS restent distinctes. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### Z28-SL02 — Baux et propriétaire unique par pool

- Exigences et version cible propres à cette unité :
  - `zt-dns-dhcp` — **Adressage coordonné et propriétaire par pool**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Reprise sans baux fiables** : il ne devient pas allocateur actif sur la seule panne de l’ancien DZT.

- Tâche rattachée : 2, libellé conservé ci-dessus.
- Objectif et périmètre : Baux et propriétaire unique par pool, limité à DHCPv4/v6 du DZT, référence commune DNS/DHCP, conservation des baux, propriétaire par pool et liaison DHCP–DNS.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : DHCP est désactivé par défaut ; un pool n’a qu’un allocateur actif ; une reprise sans baux fiables est refusée ; réussite du bail et publication DNS restent distinctes. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### Z28-SL03 — Publication DNS liée aux baux

- Exigences et version cible propres à cette unité :
  - `zt-dns-dhcp` — **Liaison DHCP DNS configurable**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Publication échouée** : les deux états sont visibles et la reprise ne réattribue pas aveuglément le bail.

- Tâche rattachée : 3, libellé conservé ci-dessus.
- Objectif et périmètre : Publication DNS liée aux baux, limité à DHCPv4/v6 du DZT, référence commune DNS/DHCP, conservation des baux, propriétaire par pool et liaison DHCP–DNS.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : DHCP est désactivé par défaut ; un pool n’a qu’un allocateur actif ; une reprise sans baux fiables est refusée ; réussite du bail et publication DNS restent distinctes. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### Z28-SL04 — Activation et reprise qualifiées

- Exigences et version cible propres à cette unité :
  - `zt-dns-dhcp` — **Configuration entièrement régénérable**.
  - `zt-dns-dhcp` — **Activation DHCP indépendante et désactivée par défaut**.
  - `zt-dns-dhcp` — **Adressage coordonné et propriétaire par pool**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Régénération après panne** : l’état natif durable n’est ni effacé ni supposé recréé par la configuration seule.
  - **DZT initialisé** : aucun bail DHCPv4 ou DHCPv6 n’est attribué.
  - **Reprise sans baux fiables** : il ne devient pas allocateur actif sur la seule panne de l’ancien DZT.

- Tâche rattachée : 4, libellé conservé ci-dessus.
- Objectif et périmètre : Activation et reprise qualifiées, limité à DHCPv4/v6 du DZT, référence commune DNS/DHCP, conservation des baux, propriétaire par pool et liaison DHCP–DNS.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats sources, propriétaires et dépendances de phase vérifiés ; choix indispensables validés avant effets. Les références de dépendance sont dans design.md ; une phase ultérieure dépend seulement des résultats qu'elle consomme réellement.
- Critères observables : DHCP est désactivé par défaut ; un pool n’a qu’un allocateur actif ; une reprise sans baux fiables est refusée ; réussite du bail et publication DNS restent distinctes. Pour cette unité, relier explicitement les exigences et scénarios applicables de requirements.md, en motivant les cas non applicables.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.
