# Couverture et réconciliation des deltas — C20

Reprise documentaire ACSM du 31 octobre 2026. Contrôle effectué avant rangement des sept fichiers sources : 37 exigences relues, dont 34 blocs identiques au canon courant, un ancien modèle de modes remplacé et deux exigences Nuitka encore proposées.

## Dispositions et travail restant

Les 34 blocs identiques sont déjà adoptés ; ils ne sont pas proposés une seconde fois. Leurs corps et scénarios ont été comparés en entier, hors marqueurs de sections de delta. Leur présence au canon ne prouve aucune réalisation. Le modèle historique à deux modes PBO est remplacé par les trois modes de l'Instance Pixs ; la distinction avec Nuitka standalone et le transport PZT est conservée.

Les deux exigences de preuve officielle Nuitka du 27 octobre restent dans le delta actif `reference-runtime`, avec leurs six scénarios inchangés. Elles ne sont ni synchronisées au canon ni abandonnées. Le change conserve son fonctionnement normatif normal : aucun `skip_specs: true` global ne masque ces exigences. Leur adoption/synchronisation et leur réalisation restent soumises aux autorisations applicables.

Les 11 tâches d'origine, leurs six cases cochées historiques et leurs cinq cases ouvertes restent inchangées. Les rattachements ci-dessous désignent les tâches futures existantes, pas de nouvelles tâches ou une nouvelle séquence. Les sous-lots C20-SL07 à SL11 correspondent respectivement à 2.1 à 2.5 ; les anciennes preuves ne qualifient que leur version. Les recettes P01–P06 restent décrites dans [PREUVE_SELECTION_PBO.md](PREUVE_SELECTION_PBO.md), sans modification ni exécution.

## Correspondance complète avant rangement

| Source intégrale conservée et exigence | Disposition | Contrat courant ou delta restant | Tâches futures dans [tasks.md](tasks.md) |
|---|---|---|---|
| [deb-package](historique-deltas-avant-reprise-acsm/deb-package/spec.md) — Distribution Debian indépendante PA et PBO PFO | AU_CANON_IDENTIQUE | [deb-package](../../specs/deb-package/spec.md) — Distribution Debian indépendante PA et PBO PFO | 2.4, 2.5 |
| [deb-package](historique-deltas-avant-reprise-acsm/deb-package/spec.md) — Installation des profils de processus configurables | AU_CANON_IDENTIQUE | [deb-package](../../specs/deb-package/spec.md) — Installation des profils de processus configurables | 2.4, 2.5 |
| [docker-image](historique-deltas-avant-reprise-acsm/docker-image/spec.md) — Composition image PBO PFO deux binaires PA et PZT | AU_CANON_IDENTIQUE | [docker-image](../../specs/docker-image/spec.md) — Composition image PBO PFO deux binaires PA et PZT | 2.4, 2.5 |
| [docker-image](historique-deltas-avant-reprise-acsm/docker-image/spec.md) — Réplication des profils sous quotas du conteneur | AU_CANON_IDENTIQUE | [docker-image](../../specs/docker-image/spec.md) — Réplication des profils sous quotas du conteneur | 2.4, 2.5 |
| [pixs-agent](historique-deltas-avant-reprise-acsm/pixs-agent/spec.md) — Compilation différenciée validée | AU_CANON_IDENTIQUE | [pixs-agent](../../specs/pixs-agent/spec.md) — Compilation différenciée validée | 2.3, 2.5 |
| [pixs-agent](historique-deltas-avant-reprise-acsm/pixs-agent/spec.md) — Paramètres ouverts et absence d'implémentation implicite | AU_CANON_IDENTIQUE | [pixs-agent](../../specs/pixs-agent/spec.md) — Paramètres ouverts et absence d'implémentation implicite | 2.3, 2.5 |
| [pixs-agent](historique-deltas-avant-reprise-acsm/pixs-agent/spec.md) — Processus PA configurables par rôle et session | AU_CANON_IDENTIQUE | [pixs-agent](../../specs/pixs-agent/spec.md) — Processus PA configurables par rôle et session | 2.3, 2.5 |
| [pixs-agent](historique-deltas-avant-reprise-acsm/pixs-agent/spec.md) — Unicité des opérations PA multiprocessus | AU_CANON_IDENTIQUE | [pixs-agent](../../specs/pixs-agent/spec.md) — Unicité des opérations PA multiprocessus | 2.3, 2.5 |
| [pzt](historique-deltas-avant-reprise-acsm/pzt/spec.md) — Processus PZT configurables sous propriétaire réseau unique | AU_CANON_IDENTIQUE | [pzt](../../specs/pzt/spec.md) — Processus PZT configurables sous propriétaire réseau unique | 2.3, 2.5 |
| [pzt](historique-deltas-avant-reprise-acsm/pzt/spec.md) — Budgets PZT sans affaiblissement des garanties | AU_CANON_IDENTIQUE | [pzt](../../specs/pzt/spec.md) — Budgets PZT sans affaiblissement des garanties | 2.3, 2.5 |
| [reference-composition](historique-deltas-avant-reprise-acsm/reference-composition/spec.md) — Qualification du binaire commun et des profils de ressources P0 | AU_CANON_IDENTIQUE | [reference-composition](../../specs/reference-composition/spec.md) — Qualification du binaire commun et des profils de ressources P0 | 2.4, 2.5 |
| [reference-runtime](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) — Couche exécutable PA séparée | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Couche exécutable PA séparée | 2.1, 2.2, 2.4, 2.5 |
| [reference-runtime](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) — Verrouillage exact de Nuitka pendant la campagne PBO | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Verrouillage exact de Nuitka pendant la campagne PBO | 2.1, 2.2, 2.4, 2.5 |
| [reference-runtime](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) — Binaire PBO commun et socle modulaire | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Binaire PBO commun et socle modulaire | 2.1, 2.2, 2.4, 2.5 |
| [reference-runtime](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) — Compilation PBO Nuitka standalone | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Compilation PBO Nuitka standalone | 2.1, 2.2, 2.4, 2.5 |
| [reference-runtime](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) — Cython ciblé et mesuré dans PBO | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Cython ciblé et mesuré dans PBO | 2.1, 2.2, 2.4, 2.5 |
| [reference-runtime](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) — Qualification du binaire PBO | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Qualification du binaire PBO | 2.1, 2.2, 2.4, 2.5 |
| [reference-runtime](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) — Dernière stable Nuitka au début de chaque campagne PBO | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Dernière stable Nuitka au début de chaque campagne PBO | 2.1, 2.2, 2.4, 2.5 |
| [reference-runtime](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) — Traçabilité de la chaîne Nuitka PBO | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Traçabilité de la chaîne Nuitka PBO | 2.1, 2.2, 2.4, 2.5 |
| [reference-runtime](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) — Actualisation coordonnée de Nuitka pour PBO | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Actualisation coordonnée de Nuitka pour PBO | 2.1, 2.2, 2.4, 2.5 |
| [reference-runtime](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) — Préservation des autres choix de chaîne PBO | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Préservation des autres choix de chaîne PBO | 2.1, 2.2, 2.4, 2.5 |
| [reference-runtime](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) — Blocage si la dernière stable Nuitka ne peut pas être qualifiée | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Blocage si la dernière stable Nuitka ne peut pas être qualifiée | 2.1, 2.2, 2.4, 2.5 |
| [reference-runtime](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) — Métadonnées fermées et identité de campagne PBO | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Métadonnées fermées et identité de campagne PBO | 2.1, 2.2, 2.4, 2.5 |
| [reference-runtime](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) — Preuve de sélection Nuitka dans la campagne PBO | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Preuve de sélection Nuitka dans la campagne PBO | 2.1, 2.2, 2.4, 2.5 |
| [reference-runtime](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) — Distributions Nuitka tracées par campagne PBO | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Distributions Nuitka tracées par campagne PBO | 2.1, 2.2, 2.4, 2.5 |
| [reference-runtime](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) — Rapport de construction lié au verrou Nuitka PBO | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Rapport de construction lié au verrou Nuitka PBO | 2.1, 2.2, 2.4, 2.5 |
| [reference-runtime](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) — Admission indépendante de la sélection officielle Nuitka PBO | DELTA_ACTIF_CONSERVÉ | [reference-runtime — delta restant](specs/reference-runtime/spec.md) — Admission indépendante de la sélection officielle Nuitka PBO | 2.1, 2.2–2.4, 2.5 |
| [reference-runtime](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) — Conservation et rattachement des preuves de sélection PBO | DELTA_ACTIF_CONSERVÉ | [reference-runtime — delta restant](specs/reference-runtime/spec.md) — Conservation et rattachement des preuves de sélection PBO | 2.1, 2.2–2.4, 2.5 |
| [runtime](historique-deltas-avant-reprise-acsm/runtime/spec.md) — Profils distincts d'un même artefact | AU_CANON_IDENTIQUE | [runtime](../../specs/runtime/spec.md) — Profils distincts d'un même artefact | 2.1, 2.2, 2.5 |
| [runtime](historique-deltas-avant-reprise-acsm/runtime/spec.md) — Modes d'exploitation PBO Standalone et ZT | CIBLE_REMPLACÉE | [runtime](../../specs/runtime/spec.md) — Modes d'exploitation de l'Instance Pixs ; [pixs-instance](../../specs/pixs-instance/spec.md) — Modes Standalone ZT et Domaine | 2.1, 2.2, 2.5 |
| [runtime](historique-deltas-avant-reprise-acsm/runtime/spec.md) — Profil de ressources par environnement d'exécution | AU_CANON_IDENTIQUE | [runtime](../../specs/runtime/spec.md) — Profil de ressources par environnement d'exécution | 2.1, 2.2, 2.5 |
| [runtime](historique-deltas-avant-reprise-acsm/runtime/spec.md) — Dimensionnement explicite et borné des processus | AU_CANON_IDENTIQUE | [runtime](../../specs/runtime/spec.md) — Dimensionnement explicite et borné des processus | 2.1, 2.2, 2.5 |
| [runtime](historique-deltas-avant-reprise-acsm/runtime/spec.md) — Proposition de dimensionnement sous configuration | AU_CANON_IDENTIQUE | [runtime](../../specs/runtime/spec.md) — Proposition de dimensionnement sous configuration | 2.1, 2.2, 2.5 |
| [runtime](historique-deltas-avant-reprise-acsm/runtime/spec.md) — Ressources détectées demandées et appliquées distinctes | AU_CANON_IDENTIQUE | [runtime](../../specs/runtime/spec.md) — Ressources détectées demandées et appliquées distinctes | 2.1, 2.2, 2.5 |
| [runtime](historique-deltas-avant-reprise-acsm/runtime/spec.md) — Reconfiguration contrôlée des ressources | AU_CANON_IDENTIQUE | [runtime](../../specs/runtime/spec.md) — Reconfiguration contrôlée des ressources | 2.1, 2.2, 2.5 |
| [runtime](historique-deltas-avant-reprise-acsm/runtime/spec.md) — Budgets compatibles avec les garanties du profil | AU_CANON_IDENTIQUE | [runtime](../../specs/runtime/spec.md) — Budgets compatibles avec les garanties du profil | 2.1, 2.2, 2.5 |
| [runtime](historique-deltas-avant-reprise-acsm/runtime/spec.md) — Supervision et qualification des profils de ressources | AU_CANON_IDENTIQUE | [runtime](../../specs/runtime/spec.md) — Supervision et qualification des profils de ressources | 2.1, 2.2, 2.5 |

Pour les deux exigences encore proposées : 2.1/C20-SL07 conserve observation officielle HTTPS/UTC, dossier figé, revue et admission indépendante ; 2.2–2.4/C20-SL08 à SL10 conservent la vérification hors ligne, les refus et le rattachement au rapport ; 2.5/C20-SL11 conserve retrait, restauration et reproduction sans réécriture. Les six scénarios actifs et les groupes P01–P06 doivent être reliés aux preuves réelles avant validation de chaque tâche concernée.

## Empreintes des fichiers intégraux

Les anciens fichiers sont conservés octet pour octet sous `historique-deltas-avant-reprise-acsm/`, hors du répertoire normatif `specs/`. La présence dans cet historique n'autorise aucune réapplication.

| Fichier historique | SHA-256 avant rangement |
|---|---|
| [deb-package/spec.md](historique-deltas-avant-reprise-acsm/deb-package/spec.md) | `3292bb67673003c5c211053c507ffac27cce7b729afa5315a3e2e385c3a70c09` |
| [docker-image/spec.md](historique-deltas-avant-reprise-acsm/docker-image/spec.md) | `adc1e2e4c4e15cbf23544958a07e535a913bd725a613d64534a359ebfa4ca3e0` |
| [pixs-agent/spec.md](historique-deltas-avant-reprise-acsm/pixs-agent/spec.md) | `d71fb72786ab5cae835dfce9c7a630d3a908b813993d950faca2d7f42d9fde06` |
| [pzt/spec.md](historique-deltas-avant-reprise-acsm/pzt/spec.md) | `01a852c1b40a16e2c42812b9bac96ccab266139397929ca6ebd37d8ca882c986` |
| [reference-composition/spec.md](historique-deltas-avant-reprise-acsm/reference-composition/spec.md) | `da3ce3b7f4bfc23a814485634f61db9799da8d4f335756ca5c95b149794db11b` |
| [reference-runtime/spec.md](historique-deltas-avant-reprise-acsm/reference-runtime/spec.md) | `fefbf7cd78acb526543239052cdeb23907a4d9ea6bb3fb85891b7e53166f205f` |
| [runtime/spec.md](historique-deltas-avant-reprise-acsm/runtime/spec.md) | `e7aca3fe59ca999502f2d585800b57437f785717effbc4f0d1a21dfec2c4fdfc` |
