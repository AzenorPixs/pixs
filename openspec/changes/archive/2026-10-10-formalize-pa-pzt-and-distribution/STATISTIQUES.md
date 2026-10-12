# Statistiques — formalize-pa-pzt-and-distribution

Archive : 2026-10-10-formalize-pa-pzt-and-distribution.
Session SCM directe, limitée à la rédaction et déclaration OpenSpec.
Aucune compétence de statistiques de pilotage, sonde, CAB ou délégation utilisée.

## 1. Statistiques générales et décisions

Fenêtre chronométrée de la phase déclarative : 10 octobre 2026,
17:28:32–17:48:42 UTC, soit 19:28:32–19:48:42 Europe/Paris et 20 min 10 s.
Exploration antérieure et rédaction/vérification de ce rapport exclues.
Cette durée calendaire ne mesure pas le temps de service du modèle.

| Agent | Fournisseur | Version modèle | Raisonnement | TTMT | Tokens/s | Coût |
| --- | --- | --- | --- | --- | --- | --- |
| Codex direct | OpenAI | N/A — version native non collectée | N/A — non collecté | N/A — aucune sonde SCM | N/A — aucune télémétrie collectée | N/A — non exposé |

Un agent direct ; zéro sous-agent et zéro orchestration OpenCode.
Tokens entrée/sortie/cache, nombre global de messages et total global d’outils :
N/A — aucun relevé natif exhaustif n’a été collecté ; aucune estimation.

Décisions conservées : quatre binaires Debian, trois Docker sans utilisateur ;
Nuitka pour démon/événements/utilisateur et Cython pour PZT ; qualification future
Debian/Linux et Docker d’abord ; première livraison envisagée locale,
expérimentale et signée. La rectification finale du développeur impose uniquement
les spécifications, sans implémentation, construction ou publication.

## 2. Types de messages et d’outils

| Catégorie observée | Résultat |
| --- | --- |
| Lectures ciblées | Cadrages, spécifications et conventions OpenSpec |
| Écritures | Markdown normatif/documentaire et métadonnée créée par OpenSpec |
| Validation CLI | 12 invocations observées : 10 exit0, 2 exit1 analysés ci-dessous |
| Contrôles Python | Empreintes, couverture, structure, RFC 2119, identité canon/delta et périmètre |
| Git, Docker, compilateurs, installation | Zéro invocation |
| Tests logiciels et sondes | Zéro ; non pertinents pour ce change documentaire |

Les deux validations exit1 sont distinctes : un delta initial omettait deux
intitulés exacts de scénarios à cause d’apostrophes typographiques ; correction
et revalidation réussies. La validation globale stricte a signalé des textes
trop longs ; les quatre capacités ciblées ont été scindées sans retrait de
clauses/scénarios. Trois WARNING préexistants restent dans bulk-operations,
fichier inchangé. La validation globale standard finale réussit 78/78.

Une invocation Python n’a pas démarré : limite système de longueur d’argument.
Elle n’a produit aucune écriture ; reprise réussie avec paramètres réduits.
Nombre total de lectures et invocations Python : N/A — pas de comptage natif
exhaustif ; les contrôles décrits sont fondés sur les sorties observées.

## 3. Fichiers modifiés

| Groupe | Nombre | Preuve/portée |
| --- | --- | --- |
| Nouvelles capacités canoniques | 2 | pixs-agent : 25 exigences ; pzt : 193 exigences |
| Capacités existantes alignées | 4 | deb-package, docker-image, runtime, reference-runtime |
| Cadrages/documentation modifiés | 5 | PROJECT, TECHNICAL, BUILD, README, CHANGELOG |
| Références antérieures préservées | 383 | Empreintes inchangées hors neuf fichiers modifiés prévus |
| Dont fichiers de code préservés | 307 | Arbres src, tests, frontend, scripts ; aucun ajout/suppression |
| Fiches de décision tracées | 174 | Clauses intégrées et empreintes dans TRACABILITE.md |
| Compléments PA intégrés | 74 | Dans leurs contrats PZT correspondants |
| Critères de recette PA | 68 | R01–R68 conservés, sans exécution annoncée |

Le sous-total des fichiers préexistants modifiés est 4 + 5 = 9.
Les 307 fichiers de code sont inclus dans les 383 préservés, non additionnés.
Les nouveaux fichiers d’archive sont proposal.md, design.md, tasks.md,
TRACABILITE.md, six deltas, .openspec.yaml et ce STATISTIQUES.md.
Deux canons nouveaux sont déclarés hors archive. Aucune production de binaire,
image, paquet, clé, donnée métier ou artefact de publication.

Les autres spécifications, AGENTS.md, DEVOPS.md, openspec/config.yaml et
pyproject.toml restent inchangés. Les scripts Python de contrôle ont été
exécutés en heredoc ; aucun nouveau fichier de code/test n’a été écrit.

## 4. Commandes

Chemin OpenSpec utilisé : /home/devops/.local/npm/bin/openspec, relevé dans DEVOPS.md.

| Commande ou contrôle | État réellement observé |
| --- | --- |
| openspec new change formalize-pa-pzt-and-distribution --schema spec-driven --json | Réussi, un seul change créé |
| openspec validate formalize-pa-pzt-and-distribution --type change --strict --json --no-interactive | Échec initial corrigé ; contrôles suivants réussis, issues[] |
| openspec validate --all --strict --json --no-interactive --report findings | Échoué sur avertissements de longueur ; portée ciblée corrigée, préexistants hors périmètre qualifiés |
| openspec validate NAME --type spec --strict --json --no-interactive, pour chacune des six capacités ciblées | Six réussites, issues[] |
| openspec validate --all --json --no-interactive --report findings, avant archivage | Réussi 79/79, trois WARNING préexistants |
| openspec list --specs --json | pixs-agent et pzt reconnus, 25 et 193 exigences |
| openspec archive formalize-pa-pzt-and-distribution --skip-specs --json | Réussi ; specsUpdated=false, canons déjà synchronisés et prouvés identiques |
| openspec validate --all --json --no-interactive --report findings, après archivage | Réussi 78/78, mêmes trois WARNING préexistants |
| Contrôle documentaire Python | Réussi : 174 contrats, 74 compléments, 68 recettes et identité canon/deltas |
| Contrôle d’empreintes et inventaire de code | Réussi : 383 fichiers antérieurs préservés dont 307 de code |

Le total des validations CLI inclut trois validations ciblées du change
(initiale échouée, correction puis contrôle final), six des capacités et
trois globales (stricte initiale, standard avant et standard après archive) :
3 + 6 + 3 = 12 ; réussites 2 + 6 + 2 = 10 ; échecs 1 + 0 + 1 = 2.
L’archivage ne réapplique pas les deltas, dont la synchronisation manuelle a
été vérifiée. Les aides CLI et lectures ne sont pas des validations.

## 5. Accès web

Zéro consultation web pendant la fenêtre de formalisation chronométrée.
Les URL présentes dans les contrats étaient déjà dans les cadrages validés.
Les liens documentaires Nuitka/Cython sont repris des choix et sources
discutés précédemment ; aucun téléchargement ou installation effectué.
Accès aux secrets, endpoints de production et dépôts distants : zéro.

## 6. Synthèse globale

Résultat : rédaction et déclaration des deux capacités, alignement de quatre
capacités transverses, traçabilité complète et archivage documentaire réussi.
Le périmètre ciblé passe la validation stricte ; la validation globale standard
réussit avec trois WARNING de longueur inchangés dans bulk-operations.
La validation globale stricte n’est pas annoncée réussie.

Bilan documentaire : PROJECT, TECHNICAL, BUILD, README et CHANGELOG mis à jour ;
AGENTS inchangé car ses règles sont préservées ; DEVOPS inchangé car aucun
environnement n’est modifié ; OpenSpec déclare les exigences sans réalisation
runtime. Toute implémentation, qualification, signature et publication reste
hors de cette session et nécessite son propre travail autorisé.

Les métriques indisponibles sont explicitement N/A, sans pourcentage ou coût
inventé. Le rapport couvre cette archive seulement et ne mesure pas les
sessions de cadrage précédentes.
