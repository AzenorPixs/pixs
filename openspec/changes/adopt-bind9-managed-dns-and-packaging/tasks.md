# Tâches — adoption documentaire BIND 9

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Maintien ciblé des unités — ACL-PIXS-2026-10-31-E3-R1

Périmètre courant : BIND 9 et sa distribution selon la nouvelle frontière PA/DZT, sans étendre les six tâches cochées historiques au nouveau périmètre.

Les tâches, libellés, cases et sous-lots existants sont conservés. Lorsque leur texte mentionne une orientation remplacée, il reste un repère historique ; la réalisation future suit la cible courante indiquée ci-dessus et ses scénarios. Une ancienne case cochée n'est pas une validation de cette nouvelle version. Chaque unité future vérifie ses contrats, nominal/refus, persistance, autorisation et reprise nécessaires avant sa propre validation ; aucun test produit n'est exécuté par ce maintien.

Sources : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md).

| Unité existante | Correspondance | Critères à relier lors de la réalisation future |
|---|---|---|
| Z27-SL01 | Repère et libellé conservés | Cible et scénarios courants du périmètre Z27, sans nouvelle qualification de la case historique |
| Z27-SL02 | Repère et libellé conservés | Cible et scénarios courants du périmètre Z27, sans nouvelle qualification de la case historique |
| Z27-SL03 | Repère et libellé conservés | Cible et scénarios courants du périmètre Z27, sans nouvelle qualification de la case historique |
| Z27-SL04 | Repère et libellé conservés | Cible et scénarios courants du périmètre Z27, sans nouvelle qualification de la case historique |
| Z27-SL05 | Repère et libellé conservés | Cible et scénarios courants du périmètre Z27, sans nouvelle qualification de la case historique |
| Z27-SL06 | Repère et libellé conservés | Cible et scénarios courants du périmètre Z27, sans nouvelle qualification de la case historique |
| Z27-SL07 | Repère et libellé conservés | Cible et scénarios courants du périmètre Z27, sans nouvelle qualification de la case historique |

La liste ci-dessus n'est pas une nouvelle séquence : les anciens rattachements aux tâches et alias restent ceux des sections conservées. Aucun identifiant n'est attribué à une unité historique absente ou ambiguë.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

La spécification est validée et le change est ouvert depuis le 24 octobre
2026. Le développeur a ensuite autorisé explicitement la synchronisation
du canon et les renvois vers Z05 et les lots Debian/Docker, toujours sans
implémentation ni production de code. Les tâches documentaires sont cochées
sur leurs preuves ; la réalisation et l'activation restent ultérieures.

- [x] 1.1 Relire les trois deltas avec le développeur, confirmer leur correspondance au choix BIND 9/Debian/Docker/PA et conserver l'activation ultérieure.
- [x] 1.2 Vérifier les versions courantes des canons pzt, deb-package et docker-image, les liens et les empreintes avant toute adoption.
- [x] 1.3 Présenter puis faire autoriser les seules mises à jour de canon, de cadrage et de renvois nécessaires ; ne synchroniser aucun canon par la simple préparation.
- [x] 2.1 Reporter la sélection adoptée dans Z05 et les lots Debian/Docker concernés, sans recréer leur réalisation ni cocher leurs tâches.
- [x] 2.2 Consolider la matrice des qualifications futures et des paramètres encore ouverts ; conserver les garanties A06c–A06k et les dépendances réelles.
- [x] 3.1 Exécuter les contrôles documentaires, OpenSpec strict, références et UTF-8/LF sur les sources finales adoptées.
- [ ] 3.2 Examiner le périmètre et les limites puis n'engager l'archive documentaire que si elle est explicitement autorisée ; produire STATISTIQUES.md après une archive réussie.

| Tâche | Prérequis | Preuve attendue |
|---|---|---|
| 1.1 | Dossier préparé | Choix et portée relus, aucun serveur actif annoncé |
| 1.2 | 1.1 | Titres/références courants et SHA des trois canons contrôlés |
| 1.3 | 1.2 | Périmètre exact autorisé et adoption corrélée, sans delta étranger |
| 2.1 | 1.3 | Renvois des lots propriétaires résolus et absence de double réalisation |
| 2.2 | 2.1 | Matrice complète : version/artefact, rôle, isolement, panne/reprise, données/secrets et limites |
| 3.1 | 2.2 | Commandes réellement exécutées, résultats et encodage prouvés |
| 3.2 | 3.1 | Revue et autorisation finales, archive/statistiques seulement si demandées |

## Preuves de l'ouverture documentaire

- 1.1 : présentation de la spécification puis validation humaine explicite du
  24 octobre 2026, avec ouverture autorisée sans implémentation ni code.
- 1.2 : trois canons relus dans leur périmètre applicable, trois empreintes
  recoupées et quinze liens internes résolus ; dérive PZT limitée aux ajouts
  Z12, ancien préfixe identique, détails dans requirements.md.

Les résultats d'ouverture restent distincts de la synchronisation autorisée
ensuite. Le change demeure actif et non archivé ; les contrôles finaux et
la clôture conservent leurs propres preuves.

## Réalisation et activation ultérieures

Les tâches de serveur, d'adapter PA, de transport, de packaging et de recette
fonctionnelle restent dans Z05 et les dossiers de distribution. Elles ne
sont pas satisfaites par ce change documentaire. Elles devront prouver :

- paquet et version réels, installation/configuration par le PA admissible ;
- configuration et zones contrôlées avant application, résultat inspecté ;
- droits, vues, DoT, retraits/révocations, absence de fuite et de repli privé ;
- état souhaité/appliqué/observé distinct, panne, concurrence, réponse perdue et reprise ;
- image inspectée dans toutes ses couches, état et secrets d'instance hors image ;
- Debian et Docker qualifiés séparément, sans extrapolation d'une fixture.

Les paramètres ou permissions non décidés restent ouverts. Une non-sélection,
une absence d'exécutant ou un test syntaxique ne vaut jamais qualification
d'un service DNS actif.


## Synchronisation et renvois du 24 octobre 2026

- 1.3 : demande humaine explicite de synchronisation du canon et des renvois,
  toujours sans implémentation ni production de code ; trois exigences et
  neuf scénarios intégrés, sans altération des clauses antérieures.
- 2.1 : renvois ajoutés dans design.md et requirements.md de Z05, C18,
  PA09 et X01 ; leurs tâches de réalisation ne sont pas cochées.
- 2.2 : matrice de design.md consolidée pour versions/artefacts, rôles,
  isolement, données/secrets, panne/reprise et paramètres encore ouverts.

La tâche 3.1 est validée sur les contrôles documentaires, les empreintes,
les renvois et OpenSpec strict courant ; les preuves sont dans VALIDATION.md.
La tâche 3.2 conserve l'archivage documentaire soumis à une autorisation
distincte ; aucune archive ni statistiques d'archive ne sont produites ici.

## Sous-lots normalisés

Relevé documentaire du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « Preuves de l'ouverture documentaire ».

### Z27-SL01 — Relire les trois deltas avec le développeur, confirmer leur correspondance au choix BIND 9/Debian/Docker/PA et conserver l'activation ultérieure.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « Tâches — adoption documentaire BIND 9 », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Tâches — adoption documentaire BIND 9 », ligne 19 du texte conservé.
  - Prérequis : Dossier préparé
  - Preuve attendue : Choix et portée relus, aucun serveur actif annoncé
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### Z27-SL02 — Vérifier les versions courantes des canons pzt, deb-package et docker-image, les liens et les empreintes avant toute adoption.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « Tâches — adoption documentaire BIND 9 », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Tâches — adoption documentaire BIND 9 », ligne 20 du texte conservé.
  - Prérequis : 1.1
  - Preuve attendue : Titres/références courants et SHA des trois canons contrôlés
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### Z27-SL03 — Présenter puis faire autoriser les seules mises à jour de canon, de cadrage et de renvois nécessaires ; ne synchroniser aucun canon par la simple préparation.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « Tâches — adoption documentaire BIND 9 », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Tâches — adoption documentaire BIND 9 », ligne 21 du texte conservé.
  - Prérequis : 1.2
  - Preuve attendue : Périmètre exact autorisé et adoption corrélée, sans delta étranger
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### Z27-SL04 — Reporter la sélection adoptée dans Z05 et les lots Debian/Docker concernés, sans recréer leur réalisation ni cocher leurs tâches.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « Tâches — adoption documentaire BIND 9 », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Tâches — adoption documentaire BIND 9 », ligne 22 du texte conservé.
  - Prérequis : 1.3
  - Preuve attendue : Renvois des lots propriétaires résolus et absence de double réalisation
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### Z27-SL05 — Consolider la matrice des qualifications futures et des paramètres encore ouverts ; conserver les garanties A06c–A06k et les dépendances réelles.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « Tâches — adoption documentaire BIND 9 », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Tâches — adoption documentaire BIND 9 », ligne 23 du texte conservé.
  - Prérequis : 2.1
  - Preuve attendue : Matrice complète : version/artefact, rôle, isolement, panne/reprise, données/secrets et limites
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### Z27-SL06 — Exécuter les contrôles documentaires, OpenSpec strict, références et UTF-8/LF sur les sources finales adoptées.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « Tâches — adoption documentaire BIND 9 », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances, critères et contrôles sourcés : tableau « Tâches — adoption documentaire BIND 9 », ligne 24 du texte conservé.
  - Prérequis : 2.2
  - Preuve attendue : Commandes réellement exécutées, résultats et encodage prouvés
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### Z27-SL07 — Examiner le périmètre et les limites puis n'engager l'archive documentaire que si elle est explicitement autorisée ; produire STATISTIQUES.md après une archive réussie.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « Tâches — adoption documentaire BIND 9 », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : non cochée.
- Dépendances, critères et contrôles sourcés : tableau « Tâches — adoption documentaire BIND 9 », ligne 25 du texte conservé.
  - Prérequis : 3.1
  - Preuve attendue : Revue et autorisation finales, archive/statistiques seulement si demandées
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
