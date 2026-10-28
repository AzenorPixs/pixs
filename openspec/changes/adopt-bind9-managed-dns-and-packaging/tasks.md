# Tâches — adoption documentaire BIND 9

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
