# Conception — PA01

## Statut

RÉALISATION_EN_COURS. D1–D9, le catalogue initial choix 1 et E3/OpenSSL 3 sont explicitement adoptés ; le noyau de build et la CLI sont en réalisation. Les tests sont préparés puis exécutés/validés dans une seconde phase. Les dépendances non livrées et qualifications manquantes restent sans preuve ; ce statut ne vaut pas livraison du change.

## Contexte actuel

Les [détails D-S1/D-R1/D-F1/D-SMIG](DETAIL_S1_R1_F1.md) sont VALIDÉS
DOCUMENTAIREMENT le 27 octobre 2026 : huit tables/contraintes et codecs privés,
contrat du relais et reprise, interfaces des fournisseurs, migration physique
M0–M5 et restauration. Dix-sept exigences et trente-quatre scénarios sont
inscrits dans les deltas PA01 Agent/PZT, NON SYNCHRONISÉS au canon par cette
inscription. Les mentions antérieures de schémas à définir sont complétées
par cette adoption ; modèles/migrations, relais/hébergement/profils,
implémentations/version des fournisseurs et preuves restent à produire.

Les [décisions S1/R1/F1](DECISIONS_S1_R1_F1.md) sont VALIDÉES le 27 octobre
2026 : tables PostgreSQL privées dédiées Agent, outbox/relais PBO vers PZT,
fournisseurs retenus par domaine. Elles sont inscrites dans les deltas
PA01 Agent/PZT et leurs cinq exigences/douze scénarios sont synchronisés à
l'identique aux deux canons sur demande explicite complémentaire du
développeur du même jour, sans réapplication des autres deltas.
Les mentions antérieures de formes physiques ou fournisseurs à choisir
sont complétées par ces décisions et leurs détails validés ; modèles, intégration, réalisations
et preuves restent manquants. Aucun code ni test produit n'est réalisé ici.

Le [détail A1/A2/A3 et de migration](DETAIL_A1_A2_A3.md) est VALIDÉ par le développeur le 26 octobre 2026 sous D-A1/D-A2/D-A3/D-MIG : liaison privée versionnée, transitions précises, Agent 2.0.0, codec et migration additive. Ces détails sont inscrits dans le delta PA01 et SYNCHRONISÉS à l'identique au canon pixs-agent sur sa demande complémentaire du même jour, mais NON RÉALISÉS ; ils ne modifient pas les contrats exécutables Agent 1.0.0. S1/R1/F1 complètent leurs choix ; modèles du schéma adopté, réalisations des fournisseurs et preuves restent à produire.

Les [orientations A1–A5](DECISIONS_A1_A5.md) sont explicitement validées par le développeur le 26 octobre 2026, inscrites dans les deltas Agent/PZT du dossier et synchronisées au canon sur sa demande complémentaire du même jour. Les détails D-A1/D-A2/D-A3/D-MIG sont adoptés séparément et complétés par S1/R1/F1 ; leurs modèles du schéma adopté, réalisations et preuves fonctionnelles restent à produire. Ces validations sont documentaires, sans code ni nouvelle recette produit ; elles ne clôturent pas les tâches de réalisation.

Le canon distingue trois binaires PA et six modes, plus le binaire indépendant PZT et son mode pzt-daemon ; le README indique que l’implémentation, la qualification et les artefacts restent à réaliser. Le contrôle de présence ciblé des sources n’est pas une recette de plateforme.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

Sources et périmètres consultés :

- [README.md](../../../README.md).
- [openspec/specs/pixs-agent/spec.md](../../specs/pixs-agent/spec.md).
- [BUILD.md](../../../BUILD.md).

## Architecture et frontières

Couche locale séparée de Django/PostgreSQL et sans autorité métier. Composer les opérations au build par contrats, dispatch explicite et identité du mode ; isoler comptes/sessions, handles et générations. Lier mandats, contexte, effets et résultats observés ; communiquer avec PBO uniquement via PZT. Les trois binaires PA (Cython) et PZT indépendant (Cython) restent colivrés, sous gestion respective de pixs.agent et pixs.pzt.

Périmètre propre à ce lot : Catalogue fermé au build, quatre exécutables colivrés, six modes PA et un mode PZT, Cython pour les trois binaires PA et pour PZT indépendant ; qualifier versions, ABI et runtime avant installation des outils.

## Choix déjà fixés et alternatives

Les décisions validées dans les contrats sources sont conservées, y compris formats, algorithmes, valeurs, rôles et alternatives rejetées. Elles ne sont pas rouvertes sous prétexte d’un nouveau dossier. Les plafonds d’un auxiliaire, collecteur, validateur ou travail ne deviennent pas un budget général du PA/PBO.

Les modalités concrètes encore ouvertes ne reçoivent pas de valeur de défaut inventée. Une bibliothèque, un provider ou une dépendance présent dans DEVOPS n’est ni sélectionné ni qualifié. Les références normatives complètes sont dans requirements.md ; les mentions historiques qu’elles contiennent ne décrivent pas des effets réalisés pendant cette préparation.

## Premier lot de décisions validé le 22 octobre 2026

Le développeur a validé les trois choix ci-dessous dans le RUN CISMP7. Cette validation fixe les candidats et le périmètre de qualification ; elle ne prouve aucune compatibilité locale, recette ou livraison.

| Décision | Choix acquis | Qualification restant à prouver |
| --- | --- | --- |
| D1 — Chaîne candidate | CPython 3.14.9 avec GIL et Cython 3.3.0. | Graphe des dépendances, runtime et ABI déclarés ; compatibilité de la chaîne et des exécutables selon le canon, avant installation ou construction autorisée. |
| D2 — Distribution | Répertoire contenant les exécutables, le runtime et leurs dépendances ; pas de monofichier. | Contenu exact, fermeture des dépendances et fonctionnement sur la cible, sans confondre construction et recette fonctionnelle. |
| D3 — Première cible | Debian 13 x86_64 : machine physique, VM et Docker local. | Preuves de qualification distinctes pour physique, VM et Docker local ; les autres OS/architectures et profils LXC restent non qualifiés. LXC n’est pas assimilé à Docker. |

Le périmètre de cette reprise reste documentaire : aucun outil installé, aucune dépendance ajoutée, aucun binaire construit et aucune capacité activée dans P0. Les obligations ultérieures des autres plateformes et profils sont conservées. Les identifiants de composants déjà validés ne sont pas rouverts.

## Politique Cython par campagne — décision du développeur du 26 octobre 2026

Le [delta normatif pixs-agent](specs/pixs-agent/spec.md) complète D1 : PA01 sélectionne la dernière version stable publiée de Cython au début de chaque campagne de qualification, après vérification datée de la source officielle PyPI. Les préversions et versions retirées sont exclues. La version sélectionnée, sa provenance et les empreintes des distributions utilisées sont enregistrées avec la chaîne de la campagne.

La version exacte est verrouillée pendant toute la campagne et pour la reproduction de ses artefacts. La publication d'une nouvelle stable ne change ni une campagne en cours ni ses preuves ; la campagne suivante réévalue la dernière stable disponible. Une version courante non vérifiable ou une incompatibilité de la dernière stable bloque la sélection ou la qualification concernée, sans repli implicite vers une ancienne version.

Un changement de version impose de mettre à jour ensemble la déclaration dans `pyproject.toml`, les métadonnées de chaîne, les contrôles de version PA01, les tests concernés et la documentation courante, puis de qualifier la nouvelle chaîne. Le contrôle de construction compare la version effectivement utilisée au verrou de la campagne ; une contrainte ouverte ne remplace pas ce verrou. Les anciennes preuves restent associées à leurs versions et artefacts, sans être attribuées à la nouvelle chaîne.

Le relevé officiel PyPI du 26 octobre 2026 sélectionne Cython 3.3.0 ; cette valeur est celle de la campagne actuelle, pas une exigence permanente. Le choix candidat CPython 3.14.9 avec GIL et les autres décisions D1–D9 restent conservés. Cette évolution documentaire n'installe rien, ne modifie pas le constructeur et ne qualifie aucune nouvelle chaîne.

Les seules six exigences et six scénarios de cette politique sont synchronisés
au [canon pixs-agent](../../specs/pixs-agent/spec.md) sur demande explicite du
développeur le 26 octobre 2026. Les deltas déjà synchronisés ne sont pas
réappliqués ; les copies historiques de `requirements.md`, les preuves produit
et les états des tâches sont conservés. Cette synchronisation ne modifie pas
le statut de réalisation en cours du change et ne vaut pas qualification.

### Vérifications de la synchronisation Cython au canon — 26 octobre 2026

Les six exigences et six scénarios du delta sont ajoutés à la fin du canon
pixs-agent, à l'identique et sans doublon. La comparaison au relevé précédant
cette synchronisation confirme la conservation intégrale du contenu antérieur :
la capacité passe de 32 exigences et 37 scénarios à 38 exigences et 43 scénarios.
Le delta source, les instantanés de `requirements.md`, les preuves de
`VALIDATION.md`, les contrats et les états des tâches restent inchangés par
cette intervention. Aucun delta déjà synchronisé n'est réappliqué.

Cette synchronisation modifie seulement `openspec/specs/pixs-agent/spec.md`,
ainsi que `proposal.md`, `design.md` et `tasks.md` du présent change pour leur
suivi. Une évolution concurrente de `CADRAGE_FONCTIONNEL.md` est observée entre
les deux relevés d'empreintes ; ce fichier est laissé intact par cette
intervention. Les six autres capacités canoniques relevées, dont
reference-runtime avec sa politique Nuitka synchronisée, et `pyproject.toml`
restent inchangés.

Avec OpenSpec 1.15.0, les validations strictes de pixs-agent, du change PA01 et
de l'ensemble par `openspec validate --all --strict --json --no-interactive`
retournent le code natif 0. Le contrôle global valide 185 éléments sur 185,
soit 107 changes et 78 capacités, sans erreur ni avertissement ; les 86
diagnostics INFO sont identiques au relevé précédant la synchronisation.
Les validations ciblées de la capacité et du change ne signalent aucun
diagnostic. UTF-8/LF, clôture des blocs Markdown, liens locaux et
`git diff --check` réussissent sur les quatre fichiers de l'intervention.

Le change reste ouvert et son statut de réalisation est conservé. Cette seule
synchronisation documentaire n'exécute aucun test produit, aucune installation,
compilation, qualification native, archive, publication, commit ou push.

## Enveloppe de métadonnées de campagne PA01 — complément du 26 octobre 2026

Ce contrat transpose à PA01 l'[enveloppe de campagne PBO](../define-common-pbo-binary-and-resource-profiles/design.md#métadonnées-de-campagne-pbo-et-verrou-nuitka--complément-du-26-octobre-2026).
Le document TOML de campagne est une entrée supplémentaire distincte du
profil de build fermé v1 et de `pyproject.toml`. Il n'ajoute aucune clé au
profil existant et ne change ni `schema_version`, ni `profile_version`, ni
les choix CPython/GIL/ABI/cibles, le catalogue ou les quatre exécutables.
Le champ `toolchain.cython` du profil reste le verrou de référence ; sa copie
dans l'enveloppe sert au rapprochement, sans seconde sélection indépendante.
Aucun chemin de fichier ni option CLI par défaut n'est défini ici.

### Schéma fermé de l'enveloppe v1

Les seules clés racines de l'enveloppe sont `schema_version`, `campaign`,
`toolchain`, `selection` et `distributions`, toutes obligatoires. Les trois
tables `campaign`, `toolchain` et `selection` sont uniques ; `distributions`
est une liste non vide de tables TOML `[[distributions]]`. Leurs clés sont
exactement celles indiquées ci-dessous. Les champs inconnus, absents,
dupliqués ou mal typés sont refusés. Les fichiers texte sont UTF-8/LF.
Une valeur textuelle est non vide et sans caractère de contrôle ; aucune
variable d'environnement ni interpolation n'est évaluée.

| Champ | Type et règle |
| --- | --- |
| `schema_version` | Texte exact `1.0.0`, version du seul schéma de l'enveloppe ; ce document n'est pas le profil de build, même si leurs versions de schéma coïncident. |
| `campaign.id` | Texte identifiant une campagne PA01 de manière unique dans son historique, sans valeur implicite. Une reproduction conserve cet identifiant et les métadonnées figées. |
| `campaign.component` | Texte exact `pa01`, désignant la campagne de construction PA01 sans renommer PA/PZT ni modifier leurs responsabilités ; une enveloppe PBO est refusée. |
| `toolchain.cython` | Texte identique au verrou du profil de build PA01 : version publique PEP 440 normalisée, finale ou `.postN`. Refuser contraintes ouvertes, préversions, développement, versions locales et formes non normalisées. Sa forme ne prouve ni publication ni qualification. Aucun autre champ de la table toolchain du profil de build n'est copié dans cette table fermée d'enveloppe. |
| `selection.verified_at` | Texte horodaté en UTC `YYYY-MM-DDTHH:MM:SS[.fraction]Z`, date civile valide de la vérification officielle ; pas de date TOML native, de date sans fuseau ni de valeur calculée implicitement. |
| `selection.source_url` | Texte exact `https://pypi.org/pypi/Cython/json`, source du relevé de sélection. |
| `selection.snapshot` | Chemin relatif POSIX, canonique et sans remontée, vers le relevé JSON conservé relativement à l'enveloppe. Le fichier réellement lu reste dans son dossier, sans lien symbolique. |
| `selection.snapshot_sha256` | Texte de 64 caractères hexadécimaux minuscules, SHA-256 des octets du relevé conservé ; vérifié sur le fichier réel. |
| `distributions[].filename` | Nom simple du fichier Cython utilisé, sans chemin ni doublon. |
| `distributions[].url` | URL HTTPS de cette distribution, exactement celle déclarée dans le relevé officiel pour la version verrouillée ; aucune information d'authentification embarquée. |
| `distributions[].sha256` | Texte de 64 caractères hexadécimaux minuscules, égal au SHA-256 officiel et à celui des octets effectivement utilisés. |

La validation de structure de l'enveloppe reste distincte de celle du profil
et n'effectue ni accès réseau ni installation. Avant de figer l'enveloppe,
la vérification officielle datée doit établir que le verrou est la dernière
stable Cython publiée et non retirée à `selection.verified_at`, sans préversion
ni développement. Les distributions retenues doivent être non retirées dans
ce relevé et chaque fichier utilisé doit correspondre à un nom, une URL et
un condensat déclarés. Un fichier utilisé mais non déclaré est refusé.
Le relevé figé permet la revue ultérieure de la sélection ; son empreinte
seule ne prouve ni l'origine officielle ni la réalisation de cette vérification.

### Rapprochement avec le profil, le manifeste et la version observée

Les quatre valeurs doivent être strictement identiques avant toute compilation :
`toolchain.cython` du profil de build, sa copie dans l'enveloppe, la déclaration
unique `Cython==<version exacte>` de `[build-system].requires` dans
`pyproject.toml`, et la version réellement observée. La construction ne
choisit aucun verrou de remplacement, ne réécrit aucune entrée et n'installe
aucun paquet implicitement. Une entrée absente ou invérifiable ferme le contrôle.

Le raccord à réaliser conserve la sonde locale Cython avec le même interpréteur
et le même compilateur que la construction. Son objet structuré possède
exactement `{"version": "<version observée>"}`. Une sortie absente, mal typée,
ambiguë ou non normalisée est refusée. Même une stable observée plus récente
que le verrou est refusée. Le constructeur ne consulte pas PyPI et ne
sélectionne aucune autre version.

Le compte rendu `build-report.json` conserve `profile_sha256` et le champ
`cython_version` avec `locked` et `observed`. Le raccord de campagne ajoute
`campaign_id` et `campaign_metadata_sha256`, puis trace les distributions
vérifiées et l'issue du rapprochement. Les empreintes portent sur les octets
du profil de build et de l'enveloppe effectivement utilisés, entrées figées
indépendantes du rapport dérivé, sans auto-condensat ni cycle. Une sonde
inexploitable laisse `observed=null` ; une sonde exploitable avec un écart
conserve les deux versions avec une issue de refus. Aucune entrée non vérifiée
n'est présentée comme vérifiée et aucun diagnostic n'expose de secret.

Les refus de l'enveloppe sont `PA01_CAMPAIGN_METADATA_INVALID` pour le schéma
et `PA01_CAMPAIGN_EVIDENCE_INVALID` pour une preuve absente ou incohérente.
Les codes existants `PA01_BUILD_CYTHON_METADATA_INVALID` et
`PA01_BUILD_CYTHON_MISMATCH` sont conservés pour la sonde inexploitable et les
divergences, y compris entre profil, enveloppe et manifeste dans le raccord
futur. Cette définition n'affirme pas que ces contrôles d'enveloppe sont déjà
réalisés par le constructeur ou le validateur existants.

### Immutabilité et portée du complément

Après sélection validée, identité, verrou, date et preuves de campagne sont
figés. Une nouvelle sélection exige une nouvelle campagne et sa qualification,
sans réécrire les métadonnées, rapports ou preuves historiques. Une reproduction
réutilise ses entrées figées et vérifiées sans nouvelle sélection de la dernière
stable ni remplacement de l'horodatage de sélection.

Les six exigences Cython initiales restent inchangées et historiquement
synchronisées. Ce complément ajoute quatre exigences et six scénarios au
delta pixs-agent ; ces seuls ajouts sont synchronisés au canon sur validation
explicite du développeur le 26 octobre 2026, sans réapplication des deltas déjà
synchronisés. Il ne modifie pas les orientations A1–A5, le contrat du profil
fermé v1, les preuves produit ni les états des tâches.
Aucune enveloppe réelle, sélection courante, installation, modification de
constructeur ou de validateur, compilation ou qualification n'est produite
par cette définition documentaire.

### Vérifications du complément d'enveloppe PA01 — 26 octobre 2026 avant synchronisation

La validation du développeur autorise la définition de l'enveloppe dans ce
change, en conservant `toolchain.cython`. Quatre fichiers sont modifiés par
cette intervention : `proposal.md`, `design.md`, `tasks.md` et
`specs/pixs-agent/spec.md`. Le delta reçoit quatre exigences et six scénarios ;
tous ses blocs antérieurs, dont les six exigences Cython et les orientations
A1–A5, restent inchangés. Le contrat textuel du profil de build fermé v1,
ses racines, les états des tâches et les preuves historiques sont conservés.

OpenSpec 1.15.0 valide le change en mode strict sans diagnostic et la commande
`openspec validate --all --strict --json --no-interactive` retourne le code
natif 0 : 185 éléments valides sur 185, soit 107 changes et 78 capacités,
sans erreur ni avertissement. Les 86 diagnostics INFO globaux restent
identiques au relevé précédant ce complément. Une formulation initialement
trop longue a été raccourcie avant la validation stricte finale, sans retrait
d'obligation.

Les contrôles statiques réussissent sur les quatre fichiers : UTF-8/LF,
blocs Markdown, liens et ancres, concordance des champs et codes de refus
entre design et delta, ainsi que `git diff --check`. Les empreintes des
78 capacités canoniques, du change PBO, de `pyproject.toml`, du constructeur
et du validateur de profil existants restent inchangées. Ces contrôles
documentaires ne sont ni des recettes du raccord d'enveloppe ni une preuve
de fonctionnement d'un nouveau validateur.

Le complément reste adopté dans le change, non synchronisé au canon. Aucune
enveloppe réelle, sélection courante, installation, modification de code,
compilation, qualification, recette produit, archive, publication, commit
ou push n'est produit par cette rédaction ; le statut de réalisation en cours
du change et les limites des preuves produit restent conservés.

### Synchronisation ciblée de l'enveloppe PA01 au canon — 26 octobre 2026

Sur validation explicite du développeur, les seules quatre exigences de
l'enveloppe et leurs six scénarios sont ajoutés au
[canon pixs-agent](../../specs/pixs-agent/spec.md), à l'identique du delta validé.
La comparaison au relevé précédant cette synchronisation confirme la
conservation intégrale du contenu antérieur : les 45 exigences et 53 scénarios
existants restent inchangés ; la capacité compte désormais 49 exigences et
59 scénarios. Aucun delta déjà synchronisé, Cython ou A1–A5, n'est réappliqué.

Les dix-sept blocs normatifs du delta pixs-agent concordent exactement avec
le canon, chacun en un exemplaire. Le delta source reste inchangé par cette
opération. Quatre fichiers sont modifiés : le canon
`openspec/specs/pixs-agent/spec.md`, ainsi que `proposal.md`, `design.md` et
`tasks.md` du change pour leur suivi. Les empreintes des autres fichiers
surveillés, dont les 77 autres capacités, le change PBO, `pyproject.toml`,
le constructeur et le validateur de profil, sont inchangées. Les identifiants
et états des tâches restent conservés, sans nouvelle coche produit.

Avec OpenSpec 1.15.0, les validations strictes de pixs-agent, du change PA01
et de l'ensemble par `openspec validate --all --strict --json --no-interactive`
retournent le code natif 0. Le contrôle global valide 185 éléments sur 185,
soit 107 changes et 78 capacités, sans erreur ni avertissement ; les 86
diagnostics INFO restent identiques au relevé précédant la synchronisation.
Les deux validations ciblées ne signalent aucun diagnostic. UTF-8/LF,
blocs Markdown, liens et ancres, ainsi que `git diff --check`, réussissent
sur les quatre fichiers concernés.

Le complément d'enveloppe est synchronisé ; le change reste ouvert et son
statut de réalisation est conservé. Aucune enveloppe réelle, nouvelle sélection,
installation, modification du constructeur ou du validateur, compilation,
qualification, recette produit, archive, publication, commit ou push n'est
produit par cette synchronisation documentaire.

## Préparation documentaire du raccord d'enveloppe — clarification du 26 octobre 2026

Le développeur a confirmé une préparation documentaire uniquement, sans
code ni implémentation. Le [dossier de raccord et de recettes](RACCORD_ENVELOPPE_PA01.md)
décrit les entrées explicites, la séparation entre analyse et contrôle de
preuves, l'ordre des barrières avant compilation, le rapport et les appelants
à adapter lors d'un lot futur. Il prépare 19 groupes de recettes, tous non
exécutés ; aucun module ou fichier de test n'est créé.

Le verrou reste `toolchain.cython` du profil fermé v1 ; l'enveloppe en reprend
une copie strictement identique. Cette préparation conserve le canon, les
deltas, le profil de build, les sources, les tests et `pyproject.toml`. Elle
ne clôture aucune tâche et ne qualifie aucun raccord ni binaire.

## Preuve officielle datée de sélection — complément du 26 octobre 2026

Le développeur autorise une définition documentaire, sans code ni
implémentation. La [procédure de preuve](PREUVE_SELECTION_PA01.md) établit
comment observer directement PyPI en HTTPS vérifié, figer les entrées et
les empreintes, puis faire admettre le manifeste exact par le développeur
ou un responsable explicitement délégué. La décision est conservée dans un
registre protégé distinct du candidat, non modifiable par le constructeur
ou son appelant. Le raccord vérifie ensuite cette admission et les octets
du dossier hors ligne ; un booléen du demandeur ou le seul SHA-256 ne suffit pas.

Le manifeste de preuve et la décision d'admission sont distincts de
l'enveloppe fermée v1 ; aucune clé n'y est ajoutée et le verrou reste
`toolchain.cython` du profil. Le rapport ajoute les références et empreintes
de l'admission et du manifeste vérifiés, sans auto-condensat. La procédure
préserve les décisions retirées, les preuves historiques et la reproduction
sur les mêmes entrées, sans nouvelle sélection implicite.

Le mécanisme repose sur la collecte contrôlée, l'autorité du responsable,
l'horloge UTC et le registre protégé ; il ne prétend pas fournir un horodatage
public certifié ou une signature de PyPI. Emplacement, propriétaire et droits
effectifs du registre seront qualifiés avant toute admission réelle, sans
valeur implicite ni changement de permissions effectué par cette rédaction.

Deux exigences et six scénarios sont ajoutés au delta pixs-agent ; ces seuls
ajouts sont synchronisés au canon sur validation explicite du développeur le
26 octobre 2026, sans réapplication des autres deltas. Les six
groupes P01–P06 complètent les 19 groupes V/R/N, tous non exécutés. Aucun
code, test exécutable, relevé courant, admission ou stockage protégé réel
n'est produit ; les états des tâches restent conservés.

## Second lot de décisions validé le 22 octobre 2026

Le développeur a explicitement validé D4–D6 et leur inscription dans design.md et tasks.md. D1–D3 restent acquis ; les six décisions fixent le périmètre du lot à qualifier, sans preuve de construction, d’installation ou de fonctionnement.

| Décision | Choix acquis | Portée et limite |
| --- | --- | --- |
| D4 — Fichiers exécutables | `pixs-pa-system`, `pixs-pa-events`, `pixs-pa-session`, `pzt`. | Trois fichiers exécutables PA et le fichier du PZT indépendant ; identifiants de composants et responsabilités déjà validés conservés. |
| D5 — Arborescence relative | `bin/` pour les quatre exécutables, `runtime/` pour CPython, `lib/` pour les dépendances livrées. | Disposition interne du répertoire de qualification ; aucun chemin absolu d’installation système fixé par ce choix. |
| D6 — Sélection du mode | Argument `--mode` obligatoire et limité aux valeurs canoniques du rôle. | Absence de mode, mode inconnu ou mode appartenant à un autre exécutable refusés ; aucun mode implicite. |

### Correspondance des fichiers et modes CLI

| Chemin relatif dans le répertoire livré | Valeurs admises pour `--mode` |
| --- | --- |
| `bin/pixs-pa-system` | `system-daemon` |
| `bin/pixs-pa-events` | `system-start`, `system-stop` |
| `bin/pixs-pa-session` | `session-start`, `session-stop`, `session-daemon` |
| `bin/pzt` | `pzt-daemon` |

Cette correspondance conserve exactement six modes PA et le mode du PZT indépendant. Elle ne crée ni cinquième binaire, ni mode supplémentaire, ni compte ou privilège. Les refus CLI sont des critères de la réalisation future, pas des tests déjà exécutés.

## Barrières de conception avant réalisation

Les choix D1–D6 sont acquis. Les fichiers exécutables, l’arborescence relative et la sélection CLI des modes sont fixés ci-dessus ; le détail du runtime/ABI, les dépendances, la fermeture du catalogue et les qualifications des environnements restent à prouver ou préciser selon le canon. Aucun chemin absolu d’installation système ni paramètre non arrêté n’est déduit de D5. Aucune installation n’est autorisée par cette reprise documentaire.

Ces barrières n’empêchent pas la rédaction conditionnelle du dossier. Avant tout code, les choix ayant un impact réel sur sécurité, périmètre, compatibilité, exploitation ou ressources devront être soumis avec conséquences et recommandation ; pour PA/PZT, respecter TECHNICAL §45.4 et ses lots de trois arbitrages. Les paramètres déjà décidés sont à qualifier, pas à remplacer par une nouvelle décision supposée.

## Dépendances et interfaces

- [Cadrage documentaire des exécutables, interfaces manquantes et qualification](CADRAGE_FONCTIONNEL.md) : synthèse des décisions et plan de reprise, sans implémentation ni nouvelle adoption.
- [define-first-installable-pbo-profile](../archive/2026-10-18-define-first-installable-pbo-profile/proposal.md).
- [activate-reference-runtime-composition](../archive/2026-10-21-activate-reference-runtime-composition/proposal.md).



Les dépendances sont des contrats et preuves attendus. Un dossier créé ne signifie pas que sa dépendance est exécutée, disponible ou autorisée à démarrer. Les interfaces intermédiaires restent explicitement incomplètes tant que les obligations manquent.

## Vérification future

Modes et sessions, droits minimaux, mandats périmés, crash entre effet et résultat, concurrence d’autorités, état durable, arrêt et reprise ; recettes R01–R68 par plateforme réellement sélectionnée.

Sortie du lot : Contenu et responsabilités exacts ; construction reproductible par cible ; aucune compilation assimilée à une recette fonctionnelle.

Exercer tous les scénarios et clauses applicables des blocs sources, y compris renvois normatifs ; un scénario non applicable doit être motivé par le profil réel. Les contrôles applicatifs suivent l’exception Super Admin du canon dans son seul périmètre, sans fabriquer audit, mesure, signature ou effet absent.

## Migrations, reprise et arrêt

Aucun schéma ni état runtime modifié ici. Toute réalisation ultérieure qui persiste des données/états doit préciser propriétaire, contrat de migration, concurrence, reprise, durabilité et compensation/restauration. Aucun retour arrière destructeur, remise à zéro, arrêt de service ou changement de droits implicites.

## Limites du dossier

Pas de PASS actuel ni d’achèvement produit revendiqué. L’autorisation de préparation ne permet ni d’activer la capacité dans P0 ni d’utiliser un compte connecté, publier un artefact ou envoyer une notification réelle.

## Alignement PA/PZT validé le 17 octobre 2026

La [décision adoptée](../separate-pa-pzt-and-pbo-management-modules/design.md) fixe pixs.agent pour
la configuration, l'administration et la supervision de PA hors PZT, et
pixs.pzt pour le binaire indépendant PZT. PA/PZT restent colivrés : trois
binaires PA plus PZT dans Debian, deux binaires PA plus PZT dans Docker.
Le présent lot conserve son périmètre de réalisation, sans code engagé ici.
Les copies requirements.md et empreintes de préparation sont historiques et
doivent être réconciliées avec le canon avant réalisation ; le réseau ne
redevient pas une responsabilité PA du fait d'une formulation héritée.

## Troisième lot de décisions validé le 23 octobre 2026 — runtime et catalogue de build

Statut : VALIDÉ_DÉVELOPPEUR pour D7–D9 et leur inscription documentaire. D1–D6 restent acquis. La qualification isolée du 23 octobre 2026 établit uniquement la chaîne minimale sur la VM courante ; elle ne ferme ni le runtime distribué ni les contrats PA/PZT.

### D7 — Runtime distribué Debian 13 x86_64

Choix validé : Conserver comme candidat la liaison statique CPython 3.14.9 avec GIL déjà exercée ; livrer la bibliothèque standard et ses extensions nécessaires sous runtime/, les dépendances tierces déclarées sous lib/, sans Python hôte requis. Inventorier et figer les dépendances natives du profil Debian, sans copier aveuglément libc ou le chargeur système.

Alternative non retenue : Reconstruire CPython avec une libpython partagée puis qualifier cette nouvelle chaîne et sa résolution de bibliothèques.

Conséquences et limites : Le candidat statique évite une nouvelle chaîne de build ; il duplique le code interpréteur dans les quatre exécutables. Taille finale et fermeture des dépendances restent à mesurer, aucune portabilité déjà prouvée.

Contrôles à prouver lors de la réalisation :

- Exécution après déplacement du répertoire sans référence au préfixe DevOps.
- Inventaire des imports, extensions et bibliothèques natives réellement utilisés.
- Versions, ABI, provenance, licences et empreintes de toutes les dépendances du profil.
- Absence de dépendance à un Python système installé séparément.

### D8 — Initialisation et chargement du runtime

Choix validé : Lanceur natif minimal utilisant la configuration isolée CPython (PyConfig), avec champs de chemin explicitement fixés à partir du chemin natif vérifié de l’exécutable et du répertoire livré. Désactiver environnement Python, site utilisateur, import automatique site et ajout du répertoire courant ; désactiver les écritures de bytecode dans le répertoire livré. Enregistrer seulement les modules compilés prévus avant initialisation ; ne pas modifier manuellement le C généré.

Alternative non retenue : Initialisation par défaut dépendant de la découverte système et de variables PYTHONHOME/PYTHONPATH de l’environnement.

Conséquences et limites : Contrôle des chemins au démarrage et maintien des quatre seuls exécutables ; petit lanceur C maintenu et testé par cible. Cette isolation de chargement ne constitue ni un bac à sable ni une vérification complète d’intégrité de l’artefact. Les contrôles de confiance existants restent requis.

Contrôles à prouver lors de la réalisation :

- Lancement depuis un répertoire courant arbitraire et chemin livré contenant des espaces.
- Variables PYTHONHOME/PYTHONPATH, sitecustomize et modules homonymes externes sans influence sur le chargement.
- Échec fermé si runtime requis absent ou incompatible, sans repli vers Python hôte.
- Aucun module de catalogue chargé à partir d’une instruction réseau ; erreurs d’initialisation explicitement propagées.

### D9 — Description de build et fermeture du catalogue

Choix validé : Profil de build TOML versionné distinct de component.toml PBO, à schéma fermé et validé avant génération. Décrire cible, chaîne/runtime/ABI, quatre exécutables D4, modes D6, propriétaires, dépendances et références versionnées des opérations/contrats. Au build, produire un registre embarqué des seules opérations livrées, sans découverte de plugins au runtime ; refuser champs inconnus, doublons, versions ou propriétaires incompatibles et opération non livrée. Conserver les identités existantes et réutiliser les contrôles SemVer adaptés sans embarquer les modules PBO/Django/PostgreSQL dans PA/PZT.

Alternative non retenue : Étendre les manifests component.toml PBO avec les champs natifs et faire dépendre les exécutants de leur chargement au runtime.

Conséquences et limites : Le schéma PBO existant reste conservé et les frontières PBO/PA/PZT distinctes ; un schéma de build et sa validation restent à spécifier puis réaliser. Ce choix ne sélectionne aucune opération privilégiée, capacité PostgreSQL, compte ou permission. Les contrats de gestion existants ne prouvent pas leur exécutant natif.

Contrôles à prouver lors de la réalisation :

- Égalité vérifiée profil de build / registre généré / contenu réellement livré.
- Refus d’opération absente, non compilée, d’un autre mode ou de version incompatible.
- Refus des champs inconnus, collisions, doublons et dépendances manquantes.
- Aucun téléchargement, eval Python ou shell arbitraire déclenché par une instruction ; catalogue initial soumis avec ses propriétaires avant réalisation.

Ces décisions précisent des modalités de réalisation du canon existant sans modifier ses garanties, les quatre fichiers/sept modes, les responsabilités pixs.agent/pixs.pzt ni le passage obligatoire par PZT. Le catalogue initial des opérations PostgreSQL de PA01 est fixé par le choix 1 ci-dessous. Le profil D9 et son registre fermé, l’implémentation des opérations, les dépendances, versions/ABI et qualifications restent à réaliser ou à prouver avant tout effet réel. Aucun seuil de ressource nouveau n’est déduit.


## Catalogue initial adopté — choix 1 validé le 23 octobre 2026

Le développeur a explicitement validé le choix 1 présenté : catalogue minimal de préparation PostgreSQL proposé par C08, version `1.0.0`. Cette sélection complète D9 et autorise sa spécification détaillée puis sa réalisation dans PA01 ; D1–D9 sont conservés.

| Opération livrée | Version | Gestionnaire | Mode autorisé | Classe | Responsabilité |
| --- | --- | --- | --- | --- | --- |
| `inspect_postgresql` | `1.0.0` | `pixs.agent` | `system-daemon` | Protégé | Observer l'état technique et les prérequis sans mutation. |
| `prepare_postgresql` | `1.0.0` | `pixs.agent` | `system-daemon` | Critique | Préparer service, rôle et base techniques selon un plan confirmé, sans effacer les données existantes. |
| `get_postgresql_result` | `1.0.0` | `pixs.agent` | `system-daemon` | Protégé | Consulter le résultat durable d'une préparation et contribuer à sa réconciliation après interruption. |

Les opérations sont les seules du catalogue initial. Une opération absente, une version différente ou un autre mode sont refusés. Aucun shell, SQL ou chemin exécutable arbitraire n'est reçu de l'appelant. Les migrations et les lectures/mutations de tables métier, la création de Core/Auth/Super Admin/tenant restent hors de ces opérations techniques. La préparation exige un mandat technique vérifié et une validation courante avant chaque effet ; aucun mode hors ligne n'est adopté pour elle. Les lectures restent soumises aux contrôles et bornes existants, sans valeur numérique nouvelle.

Le passage par PZT reste obligatoire, même localement. Les paramètres et résultats doivent être typés, versionnés et reliés à l'opérateur, l'exécutant vérifié, la cible, l'installation, l'opération/version, le plan confirmé, la validité, la politique courante, la corrélation et l'idempotence. La conformité à A07 et le raccord C08 sont conservés ; aucune API concurrente de Commands PBO PA10/C14 n'est créée.

Cette validation fixe le catalogue et autorise son inscription dans design.md/tasks.md puis sa réalisation. Elle ne déclenche aucune installation PostgreSQL sur l'hôte courant, n'accorde aucun privilège système supplémentaire et ne sélectionne pas implicitement un mécanisme d'identité, un provider ou un transport encore ouvert. Les profils Docker et autres cibles ne deviennent pas qualifiés du fait de ce choix.

Le noyau de build, le schéma TOML fermé, le registre généré, la CLI et le lanceur isolé restent distincts de l'exécutant privilégié et de l'activation fonctionnelle PZT. Une dépendance manquante bloque son activation concernée sans être remplacée par un adapter permissif ou un résultat simulé. Les tests sont préparés pendant la réalisation et exécutés/validés dans la seconde phase demandée ; aucune nouvelle coche n'est déduite de cette adoption.


## Contrat du profil de build fermé v1 — réalisation D9

Le validateur de build est un outil pur distinct de l'exécutant PA/PZT : `pixs.pa_native.build_profile.parse_profile`. Il réutilise le contrôle SemVer existant ; il n'importe pas les services de gestion Agent/PZT, Django ou un pilote PostgreSQL. La validation de structure ne prouve ni présence/empreinte des sources, compilation, fermeture des bibliothèques, confiance de l'artefact, transport, autorisation ou effet technique.

Le document TOML a exactement les clés racines suivantes, sans champ supplémentaire : `schema_version`, `profile_version`, `target`, `toolchain`, `layout`, `executables`, `operations`, `dependencies`. `schema_version` vaut `1.0.0` et `profile_version` est une version SemVer complète.

| Section | Champs obligatoires et règles |
| --- | --- |
| target | `os=debian`, `release=13` (texte), `arch=x86_64`, `environments=[physical, vm, docker]`. Ces valeurs décrivent les cibles sélectionnées, pas leur qualification ; Docker local, la cible physique et la VM gardent des preuves distinctes, et LXC n’est pas assimilé à Docker. |
| toolchain | `cpython=3.14.9`, `cython=<version stable exacte verrouillée pour la campagne>`, `gil=true` booléen, `soabi=cpython-314-x86_64-linux-gnu`, `linkage=static` : les autres choix D1/D7 et l'ABI candidate sont conservés, sans relever le Python minimal du projet PBO. Le verrou courant reste `3.3.0`. |
| layout | Trois chemins relatifs exacts : `bin=bin`, `runtime=runtime`, `lib=lib`, conformément à D5. |
| executables | Exactement les quatre entrées D4, chacune avec `name`, `owner`, `modes`, `source`. Noms, propriétaires et listes de modes exacts de D4/D6 ; source relative au dépôt, canonique, sans remontée, chemin absolu ni séparateur Windows. |
| operations | Exactement les trois entrées du catalogue adopté, chacune avec `name`, `version`, `owner`, `mode`, `criticality`, `contract`, `source`. Versions/classes/propriétaire/mode selon l'adoption ci-dessus ; référence de contrat `pixs.agent.postgresql.<nom_opération>` en version `1.0.0`, source relative canonique. Les schémas de paramètres/résultats et leur raccord restent à réaliser ; une référence seule ne les livre pas. |
| dependencies | Liste explicite non vide, noms uniques ; chaque entrée porte les textes non vides `name`, `version`, `provenance`, `license`, `sha256` (64 caractères hexadécimaux minuscules). Ces déclarations sont comparées à l'inventaire réel lors de la construction, pas prises comme preuve. |

Le champ existant `toolchain.cython` constitue le verrou de campagne, sans nouvelle clé TOML ni valeur implicite. Le validateur conserve cette version dans `BuildProfile.cython_version` et refuse les contraintes ouvertes, préversions, versions de développement ou locales. Les versions finales et leurs révisions de publication (`.postN`) normalisées sont admises structurellement ; leur publication et leur qualification restent à établir selon la politique de campagne. Le constructeur compare strictement la version observée à ce verrou avant toute compilation et consigne les deux valeurs dans `build-report.json`, lié à l'empreinte du profil. Une sonde Cython mal formée produit `PA01_BUILD_CYTHON_METADATA_INVALID` ; une différence de version produit `PA01_BUILD_CYTHON_MISMATCH`. Le constructeur ne consulte pas PyPI et ne choisit pas lui-même une nouvelle version.

Tout champ inconnu, tableau mal typé, doublon, absence d'exécutable/opération/dépendance, version/propriétaire/mode/classe/contrat incompatible est refusé sans effet ni contenu de valeur brute dans le diagnostic. L'ordre des exécutables, opérations et dépendances est normalisé pour la génération ; il n'étend pas le catalogue. Le registre dérivé des seuls objets effectivement compilés doit correspondre exactement aux entrées validées. Le profil fourni comme son propre registre ne constitue jamais une preuve de livraison.

Fichiers de réalisation prévus pour ce noyau : `src/pixs/pa_native/__init__.py`, `src/pixs/pa_native/build_profile.py` et `tests/unit/test_pa_native_build_profile.py`. Les tests couvrent nominal, champs inconnus, catalogue absent/dupliqué/non adopté, droits/mode/classe/version/contrat incompatibles, chaîne/cible différente, chemins sortants, inventaire invalide et divergence du registre compilé. Leurs données sont synthétiques et ne qualifient aucun exécutant, dépendance, artefact ou environnement. Ils sont préparés en phase de réalisation et restent non exécutés jusqu'à la seconde phase demandée.


## Transport PZT local E3 — adoption explicite du 23 octobre 2026

Le développeur a répondu : « Adopter E3 et l'adaptateur OpenSSL 3 ». Le profil local adopte HTTP/JSON sur TCP IPv4 loopback, exclusivement sous contrôle PZT dans la même frontière hôte/VM/conteneur ; TLS 1.3 avec authentification mutuelle, certificats terminaux ECDSA P-256 selon la PKI adoptée, une suite A10h explicitement fournie par l'opérateur sans valeur initiale inventée, et interdiction de 0-RTT.

L'adaptateur retenu est Cython vers `libssl`/`libcrypto` OpenSSL 3, sans bibliothèque Python TLS supplémentaire. Cette validation autorise la dépendance runtime à inventorier et qualifier. Versions exactes, provenance, licences, empreintes, ABI/providers et fermeture de dépendances doivent être verrouillés avant construction/recette ; OpenSSL 3.5.7 inventorié pour la CLI DevOps ne prouve pas la bibliothèque effectivement liée.

Cette adoption ne crée aucune CA, n'installe aucun logiciel système et ne choisit implicitement ni endpoint/port, budget, provider de clé ou matériel. Le loopback hors PZT, une socket ou un fichier de secours et une liaison directe PBO–PA restent refusés. Les schémas HTTP/JSON/OpenAPI suivent A07 ; leur livraison reste distincte de ce choix de support.

Z12 conserve la propriété de la cérémonie, des primitives CA, des clés CA matérielles non exportables, de la racine hors ligne et de l'état PKI initial. Les cinq ports initiaux publiés au §12 de son contracts.md sont documentaires ; aucun DTO de référence publique ne devient un TrustStore OpenSSL, une poignée privée, une identité terminale mTLS ou une autorisation courante. Le raccord utilise seulement les interfaces réellement livrées et vérifiées de leur propriétaire. Une interface absente bloque le raccord concerné ; ni booléen client, fichier présent ou référence opaque ne la remplace.

### Réalisation CLI D4/D6

`pixs.pa_native.cli.parse_mode(executable, arguments)` valide sans effet le rôle fixe fourni par la construction, jamais déduit d'argv[0]. Les deux formes `--mode valeur` et `--mode=valeur` ont la même sémantique. Absence, autre rôle, mode inconnu, doublon, argument parasite, identité de fichier non canonique et type invalide sont refusés avec diagnostic stable sans valeur reçue. Le parseur ne démarre aucun service et ne prouve ni configuration, autorisation, disponibilité ni exécution. Fichiers : `src/pixs/pa_native/cli.py` et `tests/unit/test_pa_native_cli.py`, tests préparés non exécutés.


## Interface et réalisation du lanceur D8

Fichiers natifs : `native/pa01/launcher.h` et `native/pa01/launcher.c`. Le candidat est borné à Linux x86_64 et aux en-têtes CPython 3.14.9 avec GIL. La table générée de liaison porte une version de schéma C égale à 1, le nom D4, le module d'entrée et sa table `_inittab` ; le générateur doit la dériver des seuls objets réellement produits. Il ne découvre aucun plugin et ne modifie pas le C émis par Cython. L'entrée compilée expose `main(rôle_fixe)` et retourne un entier exact de 0 à 255 ; booléen, exception, absence du module ou de la fonction donnent une erreur explicite. Aucune table ni entrée factice n'est livrée comme exécutant.

Le lanceur lit son identité par `/proc/self/exe`, résout le chemin natif et compare périphérique/inode à l'image en cours, puis exige le nom D4 dans `bin/`. Il construit le préfixe relatif `runtime/`, la bibliothèque standard `runtime/lib/python3.14/` et les extensions `runtime/lib/python3.14/lib-dynload/` ; ces composants de runtime ne sont pas des liens symboliques. Les chemins trop longs, image remplacée/absente, nom/arborescence incompatibles et runtime absent sont refusés, sans repli vers le préfixe DevOps ou un Python hôte.

La préinitialisation est isolée et UTF-8. La configuration fixe explicitement programme/exécutable, home, préfixes et chemins de recherche du répertoire livré ; elle désactive environnement Python, site utilisateur, site automatique, chemin courant et bytecode. Les arguments ne sont jamais interprétés comme ceux de l'interpréteur Python : ils restent ceux de l'entrée CLI compilée. Les gestionnaires de signaux appartiennent au runtime propriétaire, pas à un effet implicite du lanceur. Les erreurs utilisent des codes stables sans restituer de valeur reçue ; références et configuration sont libérées, finalisation contrôlée. Cette initialisation ne prouve ni sandbox, intégrité complète/signature, fermeture de bibliothèque native, provider, mandat ou effet métier.

### Recette du lanceur à exécuter en phase2

| Cas | Preuve attendue et limite |
| --- | --- |
| Construction candidate | Compiler avec le CPython/GIL/ABI et les objets Cython déclarés ; journaliser version, commande, exit, objets et empreintes. Un défaut de table/entrée empêche la construction ou le démarrage. |
| Répertoire déplacé / espaces / Unicode | Déplacer la distribution de test, exécuter depuis un autre répertoire ; sys.prefix et sys.path observés ne désignent que le runtime livré. |
| Environnement Python hostile | PYTHONHOME/PYTHONPATH, sitecustomize/usercustomize et modules homonymes externes sans influence ; aucune écriture de bytecode dans la distribution. |
| Runtime absent / mauvais layout / symlink | Refus avant entrée, sans repli hôte. |
| Nom/registre/entrée invalides | Erreur stable ; aucun succès métier, aucune commande Python arbitraire via les arguments. |
| Exception/type de retour/finalisation | Erreur explicite, état de sortie borné et nettoyage observé. |
| Raccord réel PA/PZT | Répéter sur les vrais objets/artefacts et environnements sélectionnés ; une entrée de test bornée ne qualifie que l'initialisation, jamais PA/PZT, le catalogue PostgreSQL ou le transport. |

La recette est préparée et non exécutée ici. Le générateur, les objets d'entrée et la fermeture du runtime doivent encore être réalisés/vérifiés ; la présence de ce code n'est pas un exécutable livré.


## Répartition du plan technique PostgreSQL — validation du développeur

Le développeur a adopté explicitement la répartition suivante : PA01/`pixs.agent` possède le contrat du plan technique et ses résultats durables, limités au service, au rôle et à la base PostgreSQL. C08 conserve l'intention et la confirmation opérateur ; il fournit seulement une projection technique autorisée et suit références/résultats via PZT. PA vérifie mandat courant, cible et confirmation avant chaque effet. Le plan privé applicatif Core/Auth/tenant reste chez C08 et n'est ni transmis à PA ni utilisé comme son autorité technique.

La présence ou forme d'une référence plan/mandat ne prouve rien. Les sources de confirmation, identités, politique/fraîcheur/fencing et préconditions sont résolues/vérifiées par les propriétaires compétents. Le résultat technique PA reste distinct du marqueur d'installation C08 et d'un commit Core/Auth. La projection ne transporte aucun credential, SQL ou shell arbitraire. Les schémas détaillés et le raccord restent à réaliser ; cette adoption n'invente aucun producteur/résolveur déployé.

## Générateur du lien D8/D9

`pixs.pa_native.generator.render_program` produit en mémoire le C de liaison de `launcher.h`, sans écrire, compiler, lier, charger ou exécuter d'objet. L'inventaire interne de build `ObjectRecord` porte `module_name`, `source`, `object_path`, `source_sha256`, `object_sha256`, `executables`, `operations` ; il vient du build de confiance, jamais d'une instruction réseau. Les noms sont des identifiants C/Python ASCII fermés ; la source est limitée au noyau natif ou au SemVer pur réutilisé, les objets .o aux racines explicitement fournies.

Les chemins sortants, sources PBO/exclues, liens symboliques de fichier et fichiers absents sont refusés. Les octets source/objet sont comparés aux SHA256 et l'en-tête attendu est ELF64 little-endian relogeable x86_64. Les noms de modules/objets, catalogue global puis par rôle, sources, propriétaires, versions et modes sont recoupés sans doublon ni opération omise/ajoutée. Le générateur n'émet que les `PyInit_`, la table `_inittab` et le descripteur de rôle/modules nécessaires. Les trois opérations PostgreSQL ne sont pas liées à PZT, aux événements ou aux sessions.

Ces métadonnées, empreintes et en-têtes ne prouvent ni origine Cython, validité complète d'objet, provenance/confiance ou comportement. Les commandes et résultats réels du compilateur/lieur, le contenu livré et les recettes restent requis. Des objets synthétiques de tests ne les remplacent pas.

Sources prévues : `src/pixs/pa_native/generator.py` et `tests/unit/test_pa_native_generator.py`. Tests préparés en phase1, non exécutés ; fixtures synthétiques sous `output/tests/pa01-generator/` uniquement, nettoyage par répertoire temporaire contrôlé, aucune écriture dans /tmp externe.

### Inventaire E3 observé avant construction

L'inventaire natif `req-c50c65761c254a6aae71090aa005fa5c` a retourné 0 le 23 octobre 2026. Bibliothèques/en-têtes observés OpenSSL 3.5.7, SONAME 3 ; paquets Debian `libssl3t64` et `libssl-dev` `3.5.7-1~deb13u3`, amd64. Empreintes, licence, dépendances directes et métadonnées conservées au checkpoint et dans le rapport de qualification `openssl-inventory-e3.json` (SHA256 `cebed7d73cb434f8a7eb38fdda3b4ae4342b2f732dc30ce21798687dd92179d5`).

Dépendances observées : libssl vers libcrypto/libc ; libcrypto vers z/zstd/libc. La fermeture complète, le provider effectif, la liaison Cython, les clés/identités et les handshakes restent non qualifiés. Aucun logiciel système, provider ou clé n'a été installé/créé par cet inventaire.


## Noyau de configuration Cython/OpenSSL E3 — candidat non connecté

Sources : `src/pixs/pa_native/tls_context.pyx` et suite dédiée `tests/native/test_tls_context.py`, à construire/exécuter explicitement en phase2. L'absence du module natif requis doit être une erreur de la recette sélectionnée, jamais un PASS ou skip silencieux.

Le candidat possède un SSL_CTX dans son OSSL_LIB_CTX privé et utilise SSL_CTX_new_ex. OpenSSL permet de fournir ce contexte et ses propriétés ; il exige aussi le nettoyage des ressources locales aux threads avant libération du contexte. [Documentation OSSL_LIB_CTX](https://docs.openssl.org/3.5/man3/OSSL_LIB_CTX/), [documentation SSL_CTX_new](https://docs.openssl.org/3.5/man3/SSL_CTX_new/).

L'initialisation demande NO_LOAD_CONFIG, sans charger de fichier de configuration ni choisir de provider de clé ; un état global déjà initialisé n'est pas présenté comme remis à zéro. Versions majeure/mineure/correctif de la bibliothèque et des en-têtes sont comparées. La disponibilité effective des providers, les propriétés/configurations ambiantes et la fermeture des dépendances restent à qualifier. [Documentation d'initialisation OpenSSL](https://docs.openssl.org/3.5/man3/OPENSSL_init_crypto/).

Le candidat fixe min=max TLS1.3, exige un côté client/serveur explicite et une seule suite A10h explicitement fournie, puis relit la liste effective TLS1.3. Il configure verify-peer, certificat client obligatoire côté serveur et max_early_data=0. SSL_CTX_set_ciphersuites est l'API dédiée TLS1.3 ; le choix demeure borné au canon AES-256-GCM ou ChaCha20-Poly1305. [Documentation des suites OpenSSL](https://docs.openssl.org/3.5/man3/SSL_CTX_set_cipher_list/).

Aucune clé, certificat, ancre, TrustStore, socket, connexion, écoute ou poignée native publique n'est ajouté. Le résultat de configuration expose explicitement ready_for_transport=false : il ne prouve ni handshake PZT, identité terminale ECDSA P-256, confiance matérielle, mandat, autorisation ou readiness. Ce noyau ne contourne pas le raccord Z12/PZT absent et ne choisit pas son provider de clé.

Le contexte est fermé sans sous-classe ni sérialisation/pointeur exporté ; close est idempotent, les exceptions de corps sont propagées après nettoyage, SSL_CTX est libéré avant le contexte de bibliothèque et les ressources locales aux threads sont nettoyées. Les appels restent sérialisés par le GIL du candidat D1. Tests dédiés préparés : politiques effectives des deux suites/deux côtés, aucune clé/certificat/readiness inventée, refus des paramètres absents/interdits, close/contexte/exception, sérialisation interdite, inspection/fermeture depuis un autre thread et diagnostics sans valeur brute. Aucun de ces tests n'est exécuté ni ne qualifie le transport ici.

## Accès SQL technique Cython/libpq — adoption et inventaire

Le développeur a explicitement adopté Cython et libpq pour les accès techniques PA, sans Django ni pilote Python supplémentaire. Cette adoption autorise l'inventaire et la qualification de la dépendance runtime ; elle n'autorise aucune installation système, connexion ou préparation PostgreSQL sur l'hôte actuel.

Inventaire natif du 23 octobre 2026, requête `req-12caaaecb78c4928bfdd0d7f002e1cff`, exit 0 : paquet `libpq5 17.11-0+deb13u1 amd64`, SONAME `libpq.so.5`, fichier `libpq.so.5.17` SHA256 `f64dcec14657e4123621448442cd3d0795744d238e588774f5c864f592f4860d`. Rapport `libpq-inventory.json` SHA256 `e32ea84df3c47cc410b303ff45a1a80c3cffdd08047430e89f03c6be2f52812f`, conservé dans le dossier de qualification du RUN. Les symboles clients nécessaires sont présents ; `libpq-dev`, les en-têtes PostgreSQL et `pg_config` sont absents.

Les dépendances directes observées sont libssl, libcrypto, libgssapi_krb5, libm, libldap et libc. La fermeture transitive, la provenance des en-têtes de build, la compatibilité client/serveur, les licences et la liaison effective restent à qualifier. Aucun numéro de version serveur n'est déduit du SONAME ou du client.

L'adaptateur doit limiter les commandes au service/rôle/base autorisés : paramètres de valeurs séparés par PQexecParams et identifiants échappés par PQescapeIdentifier, avec libération PQfreemem/PQclear/PQfinish. Aucun execute SQL générique ni DSN appelant n'entre dans le catalogue. Le profil de connexion SQL reste une décision distincte du canal PZT E3 ; aucun socket, compte, endpoint, TLS ou mécanisme d'authentification SQL n'est choisi implicitement.

Libpq applique des paramètres d'environnement et des valeurs par défaut aux paramètres non renseignés ; une chaîne dbname peut aussi être interprétée lorsque son expansion est demandée. Le raccord devra donc fournir un profil protégé explicite, interdire l'expansion et traiter les sources ambiantes sans repli silencieux. Cette exigence ne vaut pas réalisation du connecteur. [Connexion libpq 17](https://www.postgresql.org/docs/17/libpq-connect.html), [exécution et échappement libpq 17](https://www.postgresql.org/docs/17/libpq-exec.html).

## Recette dédiée du lanceur — préparation, sans exécution

Fichier nouveau prévu : `tests/native/test_launcher.py`. Le test construit une fixture C bornée avec le lanceur courant, le CPython 3.14.9 GIL statique et le compilateur déjà inventoriés ; les seuls artefacts temporaires vont dans `output/tests/pa01-launcher/`. Il n'installe aucun outil ni service. Son runtime minimal de test contient encodings et un répertoire lib-dynload vide : il ne constitue pas la distribution D7, les modules Cython réels ou une qualification PA/PZT.

La campagne séparée vérifiera les chemins/flags isolés, les arguments non interprétés, l'identité indépendante d'argv[0], la relocalisation avec espaces/Unicode, les variables PYTHON* et le répertoire courant hostiles, les noms incohérents, le runtime manquant/symbolique et les résultats invalides/exceptions de l'entrée. Une absence d'outil/runtime requis échouera explicitement ; aucun skip ou résultat de compilation ne remplacera ces observations. Le compte rendu distingue toujours cette recette du lanceur des scénarios PA/PZT réels et des recettes R01–R68.

## Profil SQL local Unix/peer — adoption explicite du développeur

Le développeur a adopté « Socket Unix et peer (recommandé) ». Le profil SQL technique est local, sans repli TCP/TLS ni mot de passe. Il conserve un compte système explicitement configuré et la vérification du propriétaire OS du serveur par requirepeer. Aucune création de compte, modification PostgreSQL ou connexion sur l'hôte actuel n'est autorisée par ce choix.

requirepeer vérifie l'identité OS du serveur ; il ne prouve pas la règle HBA qui authentifie le client. require_auth=none interdit une demande d'échange d'authentification, mais ne distingue pas peer d'une règle trust. Le propriétaire du profil protégé doit donc fournir et vérifier la règle peer et son éventuel mapping, la liaison à l'identité locale/SQL, la cible et leur fraîcheur avant effet. Une référence peer_rule_ref ou une comparaison de noms ne remplace pas cette preuve. [Contrôle de connexion libpq 17](https://www.postgresql.org/docs/17/libpq-connect.html).

Schéma TOML fermé 1.0.0 prévu dans `src/pixs/pa_native/postgresql_profile.py` :
schema_version, profile_ref, profile_revision, target_ref, peer_rule_ref, socket_directory, port, database, database_user, server_os_user, connect_timeout_seconds, statement_timeout_ms, lock_timeout_ms, io_timeout_ms, expected_server_version_num. Aucun champ, compte, chemin, port ou budget ne possède de valeur de production implicite. Les bornes numériques sont les représentations mécaniques du port et des paramètres entiers, pas des budgets adoptés ; toutes les valeurs sont fournies par le propriétaire du profil protégé.

Le parseur reçoit un texte déjà fourni et des bornes de taille explicites ; il n'ouvre aucun fichier, environnement, socket ou base. Il refuse inconnus/manquants/doublons/types/versions/UTF8/contrôles, les formes réseau/multihôte/relatives ou ambiguës du socket et les valeurs sans borne effective. Le DTO est immuable, son repr masque les valeurs et sa projection native est ordonnée. Le profil ne vaut ni mandat ni confirmation et ne rend aucun connecteur disponible. Suite pure prévue : `tests/unit/test_pa_native_postgresql_profile.py`, à exécuter seulement en phase2.

Le futur raccord Cython doit interdire les PG* ambiants sans en exposer les valeurs, fournir la socket/base/rôle/requirepeer/budgets explicitement, désactiver l'expansion dbname et tout fallback de mot de passe/service/transport. Les délais client et serveur restent distincts. Toute mutation devra être précédée de la vérification courante du plan/mandat/confirmation et suivie d'une observation durable ; une perte de réponse reste incertaine, sans rejeu aveugle.

## Adaptateur Cython d'inspection libpq — réalisation partielle, sans DDL

Fichiers nécessaires et examinés : `src/pixs/pa_native/libpq_inspection.pyx` et `tests/native/test_libpq_inspection.py`. Le premier réalise seulement connexion/inspection technique en lecture seule ; il ne réalise pas encore prepare_postgresql, un service système, un handler PZT ou une autorisation courante. Les deux premières propositions ont été corrigées par revue avant écriture ; aucune compilation ni exécution de tests n'a eu lieu.

Le candidat exige les vrais en-têtes libpq 17.11 (PG_VERSION_NUM 170011) et compare la bibliothèque effective à 170011. Les en-têtes sont actuellement absents : aucun faux en-tête n'est créé pour contourner ce prérequis. Le tuple natif vient du profil Unix/peer adopté, dans l'ordre documenté ; types/UTF8/contrôles, socket canonique et chiffres/bornes mécaniques sont revérifiés. Aucun délai de production n'est inventé.

Connexion via tableaux keywords/values avec expand_dbname=0 ; PG* de l'environnement C refusés sans restituer leurs valeurs ni modifier l'environnement ; passfile=/dev/null, require_auth=none et transports TLS/GSS désactivés sur cette seule socket Unix. Les paramètres imposent UTF8, search_path vide, session en lecture seule et délais serveur explicites. Le raccord PZT E3 conserve séparément TLS1.3/mTLS obligatoire ; le canal SQL n'est pas un canal de communication PBO–PA.

Le candidat utilise PQconnectStartParams/PQconnectPoll, PQsetnonblocking, PQsendQueryParams et select sous échéances monotones de connexion/IO distinctes. La version serveur et les paramètres effectifs sont recoupés. Les seules requêtes internes fixées observent la session et les attributs de rôle/base explicitement visés dans pg_catalog, avec paramètres de valeurs séparés. Elles ne lisent pas de table métier et ne contiennent pas de DDL. Le volume des valeurs décodées est borné par un argument obligatoire ; cela ne borne pas la mémoire interne libpq et ne remplace pas les protections de ressources du runtime.

La connexion possède un thread et un processus ; les appels concurrents/réentrants sont refusés, l'échec condamne la connexion et les résultats sont libérés. close est idempotent pour son propriétaire, repr masqué, copie/sérialisation/sous-classe refusées. Un processus possédant une connexion vivante ne doit pas forker ; ce composant ne qualifie aucun parcours fork ou restauration. La vérification du profil protégé, de la règle HBA peer, de l'identité locale, du mandat, du plan et de la politique courante appartient toujours au vrai propriétaire avant connexion/effet. Aucune référence ou valeur de retour n'accorde cette autorité.

La suite dédiée charge le vrai module natif `libpq_inspection` ; absence du build = erreur explicite. Elle prépare des refus de construction/paramètres, d'API SQL/DDL, de sérialisation/copie/sous-classe, des cas de fermeture/contexte/thread et des environnements C PG* dans des sous-processus contrôlés, dont os.putenv sans mise à jour du mapping Python. Aucun test de cette suite n'appelle connect. Une recette SQL réelle sur une cible explicitement autorisée reste distincte et non réalisée ; elle devra notamment couvrir état observé, résultats absents, Unicode/injection dans les valeurs, délais, rupture et nettoyage. Ce candidat ne remplace pas cette preuve.

## Fournisseur des terminaux initiaux — décision matérielle et adoption TPM2

La décision humaine Z12 sur la portée a été relue dans le message utilisateur `01a1687f-3f83-7211-b2d4-c3ca4fec2bac` : « Matériel non exportable pour les CA et les terminaux initiaux ». Le scénario initial du canon PZT conserve cette obligation pour les clés TLS PA/PZT/PBO. Elle ne sélectionnait pas à elle seule un fournisseur, un matériel ou une interface déjà livrée.

Le développeur a ensuite explicitement adopté ici tpm2-openssl 1.3.0 (candidat Debian 1.3.0-1), la pile tpm2-tss et le gestionnaire de ressources requis à inventorier/qualifier, avec chargement dans le contexte OpenSSL privé et résolution locale de références de clés sous contrôles courants. Les clés terminales ECDSA P-256 restent matérielles non exportables, sans repli logiciel. Cette adoption autorise conception/raccord et qualification préparée ; elle n'autorise aucune installation de service hôte, aucun accès matériel supplémentaire, génération/utilisation de clé hôte ou écriture TPM NV.

Le fournisseur officiel utilise OpenSSL3/ESAPI, admet P-256 et sépare ses opérations de clé des opérations de format/chiffrement fournies par base/default. Sa documentation impose un gestionnaire de ressources adapté pour les usages SSL/X509 complexes ; la seule présence d'un resource manager noyau n'est pas une qualification. Versions exactes, TCTI, module et dépendances, authentifications et permissions devront être explicitement fournis et vérifiés avant activation. Aucun URI/handle, chemin de clé, endpoint TCTI ou secret n'est déduit de la documentation. [Fournisseur 1.3.0](https://github.com/tpm2-software/tpm2-openssl/tree/1.3.0), [opérations de clés](https://github.com/tpm2-software/tpm2-openssl/blob/1.3.0/docs/keys.md).

L'inventaire natif `req-a18ba346e9364c748d74dad7d91b5552` a retourné 0 le 23 octobre 2026, sans charger de provider ni contacter un TPM : tpm2-openssl, tpm2-abrmd, TCTI tabrmd et en-têtes TSS2 absents sur cet hôte ; bibliothèques TSS2 de base présentes et métadonnées 4.1.3-1.2 observées ; dbus-daemon 1.16.2-2 observé. Le rapport `tpm2-terminal-inventory.json` SHA256 `d016d9d2a59395dcd7136f312a1881d47acb66f103fee6ab2e563d44b9bcebef` conserve fichiers/empreintes/dépendances et absences. Les lignes dpkg génériques sans version ne prouvent pas une installation. Fermeture, fournisseur effectif, clé, non-exportabilité, TPM physique/vTPM et handshakes restent non qualifiés ; aucun logiciel/service hôte n'a été modifié.

Le raccord devra lier identité publique/chaîne/ancres, clé matérielle locale, installation, rôle, génération et politique/époque courantes. Une référence, un nom de provider, un type ou un booléen ne prouve ni confiance ni non-exportabilité ; les faits matériels et la possession devront être réellement vérifiés. Aucun pointeur, EVP_PKEY ou clé privée n'entre dans le contrat public. Les ports terminaux/TrustStore courants restent à construire avec leurs vrais propriétaires ; les DTO CA et les cinq ports initiaux documentaires Z12 ne les remplacent pas.

## Construction traçable des objets Cython — outil distinct du runtime

Nouveaux fichiers examinés : `src/pixs/pa_native/builder.py`, `tests/unit/test_pa_native_builder.py`, `tests/native/test_object_builder.py`. Deux propositions ont été écartées avant écriture ; la source reprise ne doit pas être présentée comme testée. L'API build-time compile_objects reçoit le TOML fermé, des ModuleSource explicites, une Toolchain à exécutables SHA256 épinglés, la racine, une sortie relative inédite et des paramètres obligatoires source_date_epoch, timeout_seconds, cleanup_timeout_seconds, max_log_bytes. Aucun n'est un budget de production PA ni un défaut implicite.

Le TOML est toujours reparsé par le propriétaire existant. Types, noms, rôles, sources de chaque entrée, opérations complètes/propriétaires/sources/modes, doublons et SHA sont contrôlés avant sous-processus ou création de sortie. Sources et chemins de sortie symboliques sont refusés, y compris leurs répertoires parents ; les liens de localisation des outils DevOps sont résolus/épinglés tout en conservant leur chemin d'invocation, nécessaire au venv Cython. La sortie est strictement `output/native/pa01/<identifiant>`, inédite et sans effacement de l'existant.

Les sondes isolées vérifient les deux interpréteurs CPython3.14.9 final/GIL/static/SOABI, Linux x86_64/Debian13, l'include réel et Cython3.3.0 ; l'identité du compilateur et les empreintes des outils/en-têtes observés sont consignées. L'environnement est construit explicitement (PATH/LANG/SOURCE_DATE_EPOCH et TMPDIR interne au build) sans recopier l'environnement courant. Cython reçoit des arguments fermés et un module_name explicite ; le C produit est compilé en objet avec dépendances d'en-têtes conservées dans un depfile. Aucune modification du C généré, installation, liaison, exécution d'objet ou création d'entrée factice n'est effectuée par cet outil. [Interface Cython3.3.0](https://raw.githubusercontent.com/cython/cython/3.3.0/Cython/Compiler/CmdLine.py), [incorporation des modules](https://cython.readthedocs.io/en/latest/src/tutorial/embedding.html).

Les commandes possèdent leur groupe de processus. Leurs flux sont drainés sous échéance monotone et budget de journal fournis ; une interruption/erreur/dépassement arrête seulement ce groupe et sa quiescence est vérifiée avant résultat complet. Le leader est observé sans réabsorption anticipée (waitid/WNOWAIT), afin de conserver son identité jusqu'au signal de nettoyage. Quiescence non prouvée = IN_DOUBT, aucun rejeu automatique. Ce mécanisme n'est pas un bac à sable pour outils/sources hostiles et ne qualifie pas des descendants qui échapperaient volontairement au groupe.

Le rapport JSON UTF8/LF est initialisé puis mis à jour avec argv, état/code, journaux bornés encodés, provenance, empreintes source/C/objet/depfile, limites et échecs. Une erreur de rapport ne masque pas l'erreur initiale. Les sources/outils sont recoupés avant le retour d'ObjectRecord et les contrôles de composition existants réutilisés. Les dépendances transitives de cimport/en-têtes, leur confiance et licences, la fermeture, les symboles, la reproductibilité et les recettes restent à examiner : un ELF et des métadonnées ne prouvent pas le comportement des trois opérations.

Les unités préparent de vrais refus avant effet ; les mocks servent uniquement à détecter un sous-processus interdit avant rejet. La recette native exige explicitement `PA01_CYTHON_PYTHON` (chemin du Python Cython qualifié), construit des objets de fixture dans `output/tests/pa01-builder/`, compare deux emplacements, inspecte les vrais symboles et prépare dépassement de délai/journal et nettoyage parent/enfant. Les valeurs numériques de cette fixture restent propres au test, sans valeur de production. Ni ces fixtures ni une compilation ne qualifient PA/PZT/PostgreSQL ; aucun test ni build de cette suite n'est exécuté en phase1.

Après cet outil, la réalisation reste incomplète : quatre entrées runtime et distribution réelle, handlers service/rôle/base, autorité courante et audit/état durable/fencing/réconciliation, transport PZT/mTLS matériel et TrustStore, raccords propriétaires et recettes sélectionnées. Aucun passage à la phase2 ni nouvelle coche n'est justifié par le seul builder.


## Outil de liaison native — réalisation PA01 non testée

La liaison complète le constructeur d'objets sans exécuter les programmes ni qualifier leur runtime. Elle reprend le TOML fermé, tous les ObjectRecord réels, le rapport builder local protégé et épinglé, les outils Python/compilateur/readelf épinglés, l'archive libpython3.14.a épinglée et les deux sources fixes du lanceur. Les modules d'entrée sont dérivés des sources et rôles du profil ; une entrée absente ou ambiguë ferme la liaison.

Le rapport builder est recoupé avec les objets, sources, C et fichiers de dépendances et leurs commandes réussies ; il constitue une trace locale à protéger, pas une signature ni une autorité. Le Python outil doit conserver CPython 3.14.9 final, GIL, ABI et cible Debian 13 x86_64 retenus. LIBDIR/LIBRARY et INCLUDEPY sont recoupés avec l'archive et les en-têtes. L'archive est un fichier de données qui n'a pas besoin du droit d'exécution. Les options système sont fermées ; aucun shell, fichier de réponse ou option de liaison fourni par une requête PA n'est admis.

La liste fermée des bibliothèques natives directement liées couvre les dépendances déjà adoptées OpenSSL/libpq, les familles TSS de D10–D12 et du provider TPM2, ainsi que libsystemd.so.0 du profil commun D14 ; elle est partagée avec l'assembleur. Chaque bibliothèque reste explicitement épinglée par rôle et présente dans l'inventaire du profil. Aucun backend TCTI, provider, secret, instance ou clé n'est sélectionné par cette liste. Leurs SONAME et les dépendances ELF finales sont lus par readelf épinglé, sans ldd ni chargement des programmes. La liaison refuse libpython partagée et utilise le chemin relatif de bibliothèque $ORIGIN/../lib ; la distribution de lib/, du runtime et la fermeture de leurs dépendances restent distinctes et non qualifiées.

La sortie neuve output/native/pa01/<identifiant>/bin contient les quatre noms D4. Les commandes, codes, journaux bornés, empreintes et états sont conservés dans link-report.json. Les budgets de durée, nettoyage et journal sont explicites ; le groupe de processus et IN_DOUBT suivent l'exécuteur borné du constructeur. Un échec ne déclenche aucun rejeu ou écrasement automatique. PROGRAMS_LINKED_UNQUALIFIED ne prouve ni catalogue fonctionnel, ni lifecycle, ni transport, ni recette physique/VM, ni reproductibilité.

Les sources de tests comprennent les refus avant effet et une recette future de vraie compilation/liaison de fixtures pour les quatre rôles, distinctes des entrées produit. Aucun build ou test n'est exécuté pendant cette écriture. L'admission prébase, les handlers PostgreSQL et leur registre durable, le matériel TLS courant, le transport et les entrées produit restent nécessaires avant achèvement de la réalisation.


## Quatrième lot adopté le 23 octobre 2026 — journal PA, D10–D12

Statut : VALIDÉ_DÉVELOPPEUR, réponses humaines directes call_12ea68b4889449f5a3e328e8071f3b6b/0–2. Portée : présente conception, contracts.md/tasks.md et réalisation avec sources de tests PA01 ; aucune écriture NV, installation, création/utilisation de clé, provisionnement, suppression ou modification de hiérarchie sur l'hôte actuel. Le relevé /dev/tpmrm0 communiqué concerne l'hôte Pixs courant ; aucun laboratoire distinct ni recette matérielle n'est déduit de ce relevé.

| Décision | Choix adopté | Conséquences et qualification requise |
| --- | --- | --- |
| D10 — Ancre du journal technique | Index TPM dédié de type NV_Extend, SHA-256 ; adaptateur Cython vers ESAPI tpm2-tss. | Chaque transition durable engage le contenu du journal, installation et cible. La pile TSS déjà adoptée est inventoriée et qualifiée avec ses ABI/outils. Un compteur NV seul n'est pas sélectionné. |
| D11 — Séparation des droits | Provisionnement hors runtime, PLATFORMCREATE + POLICY_DELETE, état conservé au redémarrage ; suppression réservée à une autorité matérielle de maintenance P-256 indépendante des clés CA, terminales TLS et personnelles opérateur. PA n'a aucun droit de création, suppression, Clear ou gestion de hiérarchie. | La séparation réelle et la protection de la plateforme doivent être prouvées ; sinon refus, sans index owner effaçable ou autre repli. La seule absence d'une commande dans le binaire, un UID ou un attribut NV ne prouve pas les droits effectifs. Survie/récupération de l'autorité de maintenance après réinitialisation et limites de firmware restent à qualifier. |
| D12 — Autorisation d'usage | Autorisation aléatoire 256 bits distincte de la maintenance, remise au seul natif par descripteur protégé du lanceur ; sessions HMAC-SHA-256 liées à l'index, sans session mot de passe ni secret remis à Python, aux agents ou au journal. | Le vrai propriétaire de garde/remise au démarrage et l'authentification du contexte sont requis, sinon fermeture. Le descripteur n'est pas un paramètre réseau ou une assertion client d'autorisation. Mémoire native et ressources de session sont libérées ; aucun secret de hiérarchie n'est remis au runtime. |

L'identité de la cible, le périphérique/transport, l'index, son Name et sa zone publique attendus, la politique et leurs versions sont configurés explicitement par les sources protégées compétentes ; aucun numéro d'index, quota, chemin hôte, port, authPolicy ou credential par défaut. Le Name d'un index ne constitue pas à lui seul l'identité d'un TPM. Le provisionnement et l'initialisation vérifiée sont une étape extérieure au runtime, sous plan exact autorisé ; un index absent, non initialisé, recréé, divergent ou inaccessible ne réouvre jamais l'amorçage.

La pile de réalisation runtime n'émet que les commandes nécessaires aux sessions, à l'inspection publique et à la lecture/extension autorisées de cet index PA ; pas de mécanisme de provisionnement/suppression/hiérarchie exposé au PA. Les profils doivent conserver l'état malgré redémarrage et interruption d'alimentation : aucune hypothèse d'état volatile ou de persistance différée ne remplace la qualification. Les interfaces Async/Finish et les budgets protégés bornent l'attente ; une issue incertaine interdit toute nouvelle extension tant que la quiescence et la valeur courante n'ont pas été réconciliées.

Le journal ne revendique pas une transaction atomique entre stockage local, NV, service et SQL. L'intention durable précède l'ancrage, sa vérification courante précède chaque effet, et la postcondition observée précède le résultat durable. Une perte de réponse, une transition partielle ou une panne après effet reste IN_DOUBT/BLOCKED selon les observations ; aucun rejeu aveugle, remise à zéro, résultat réussi forgé ou ancien mandat réutilisé. Les écritures concurrentes sont sérialisées/fencées ; les plafonds et contrôles courants restent propres au profil.

L'ancre et le registre PA, leurs secrets et leur maintenance demeurent distincts de PKI Z12. Les ressources communes TPM/plateforme/hiérarchies et sessions devront faire l'objet d'un plan coordonné exact avant effets, sans autorité de ce RUN sur Z12. L'identité native, mandat personnel E4, politique/révocation, source UTC fiable, confirmation C08, propriétaires des profils/préconditions et état réel doivent toujours être vérifiés positivement. D10–D12 ne rendent aucun de ces propriétaires disponible.

Sources primaires de conception : [TCG TPM 2.0 révision 1.38, partie 3](https://trustedcomputinggroup.org/wp-content/uploads/TPM-Rev-2.0-Part-3-Commands-01.38.pdf), §§24.6, 31.5 et 31.9 ; [ESAPI](https://tpm2-tss.readthedocs.io/en/stable/group___esys___start_auth_session.html). Les propriétés normatives ne constituent pas une recette de la cible ni une autorisation d'y émettre des commandes.


## Assembleur du répertoire D2/D5/D7/D8 — réalisation en cours

La réalisation prévue dans src/pixs/pa_native/bundler.py assemble une sortie neuve sous output/native/pa01/<identifiant> à partir des quatre ProgramRecord réels du linker, de leur rapport local épinglé et d'un inventaire exhaustif de RuntimeAsset(source PinnedFile, destination relative, nom de dépendance). Elle recoupe le profil fermé, les objets/source/registre réels, les rôles, les commandes de liaison et les octets des programmes. Les rapports locaux restent des traces protégées par l'appelant, sans signature ni autorité.

Les assets explicitement inventoriés sont les modules/packages de bibliothèque standard Python 3.14, ses seules extensions ABI cpython-314-x86_64-linux-gnu, les bibliothèques natives déjà adoptées et, s'il est fourni explicitement, le provider terminal dans lib/ossl-modules/tpm2.so. Chaque fichier lie SHA-256, version, provenance et licence du profil ; aucune copie récursive, découverte, installation, téléchargement, Python partagé, libc/chargeur copié aveuglément, fichier sensible, plugin/site externe ou cinquième exécutable. Le chemin interne du provider ne sélectionne pas implicitement son chargement au runtime.

Les sources publiques peuvent provenir d'un préfixe de construction explicitement épinglé ; les programmes/objets et rapports proviennent du workspace de construction protégé. Les chemins, composants symboliques, fichiers spéciaux, liens physiques non maîtrisés, formes de destination et collisions sont refusés. Les lectures sont bornées avant allocation et rapprochées par descripteur/stat/empreinte. Les budgets obligatoires par fichier, total du staging et nombre de fichiers viennent du profil de construction, sans défaut de production. La protection contre une mutation hostile concurrente des sources et de la sortie reste à la charge du processus de construction ; ce code n'est pas un sandbox.

Le layout est bin/runtime/lib ; fichiers exécutables 0755, assets 0644, répertoires 0755, mtimes SOURCE_DATE_EPOCH. Les fichiers et répertoires sont synchronisés, les pins et copies revérifiés avant succès. Une sortie existante reste intacte. Un échec après création conserve un manifeste FAILED/complete=false lorsque possible ; une erreur de persistance reste liée à l'erreur initiale, sans suppression d'arbre ou succès supposé.

STAGED_UNQUALIFIED est seulement le résultat de cet assemblage. Le manifeste local inclut le profil, la trace du linker, les octets/modes/tailles et l'inventaire ; il n'est ni une SBOM signée ni une publication. Les contrôles SONAME/DT_NEEDED transitifs, résolution dynamique des extensions/provider, fermeture des imports et dépendances, exécution après déplacement, influences environnementales, fonctionnalités réelles des quatre entrées, reproductibilité des artefacts distribués, licences et recettes physique/VM restent obligatoires en seconde phase. La présence des trois modules encodings minimaux ne suffit pas à prouver le runtime. Aucun test, construction, chargement ou recette n'est exécuté par cette inscription.


## D13 PA — stockage du secret d'usage NV, adopté par le développeur

Réponse humaine à call_6be0a815ba9647b6a41ae8a093bccee6/0 : « Adopter ce stockage PA dédié (recommandé) ». D13 complète D12 ; il ne modifie pas les secrets/autorités PKI de D15 Z12 ou PBO de C01.

Le secret binaire d'usage NV PA de 256 bits possède une source persistante DÉDIÉE, protégée par LoadCredentialEncrypted avec combinaison explicitement host+tpm2. La garde et la remise restent dans le lanceur natif pixs-pa-system déjà prévu : aucun cinquième exécutable ou mode PA. Le nom/référence/version de credential, sa source chiffrée, les facteurs et éventuelles mesures/PCR, le consommateur, l'installation/cible et les politiques sont explicitement déclarés et qualifiés ; aucun chemin, nom, PCR, identité ou mécanisme de secours de production n'est déduit des fixtures.

Le natif doit vérifier positivement contexte systemd/lanceur, unité/manager/MainPID/InvocationID, artefacts, profil/politique/version, provenance et protection du credential avant sa remise. Une variable d'environnement ou un chemin reçu ne prouve pas ce contexte. Le credential déchiffré reste confiné au natif et n'est remis que par capacité FD privée, hors Python, argv, environnement contenant une valeur secrète, journaux, agents ou contrat réseau. Les références publiques de configuration restent distinctes de la valeur secrète. Un contrôle de forme de fichier/FD n'est pas un propriétaire d'autorité.

Absence, substitution, dérive de version/politique/cible, retrait, délai, erreur de déchiffrement, facteurs indisponibles ou protection mémoire/provenance non démontrée ferment l'usage. Aucun repli host seul, null, fichier en clair ou secret partagé avec PKI/PBO n'est admis. Le profil source chiffré doit réellement engager host+tpm2 ; le seul nom d'une directive ou texte de configuration ne le démontre pas. Rotation, arrêt/effacement et récupération sous facteurs/pertes d'hôte distincts restent à réaliser et qualifier avec leurs propriétaires.

L'adoption couvre conception, sources, documentation et inventaire/qualification à préparer. Elle n'exécute ni génération/lecture de secret, écriture/provisionnement NV, création/utilisation de clé ou modification actuelle de l'hôte. Les effets de qualification sur le TPM physique partagé gardent leur plan exact distinct ; l'autorisation CT100 n'en fait pas un TPM restaurable par snapshot.


## E5 — Échanges techniques 1.1 et retour du plan avant confirmation

Le lot documentaire commun C08/PA01 a été validé humainement par la réponse
« Valider le lot documentaire commun » à
call_0ef16343f01847f698d3411cb89b5cd3/0. La transcription coordonnée couvre
treize documents C08 et les quatre documents PA01. Son écriture ne livre
aucun codec, handler, transport, autorité, effet PostgreSQL ou recette.

Les profils 1.0.0 existants MUST rester inchangés et explicitement distincts
du profil 1.1.0 ci-dessous. Une enveloppe 1.1 non liée ou invalide MUST NOT
être convertie ou acceptée en 1.0. Le catalogue logique conserve exactement
les trois noms, version 1.0.0 et classes déjà adoptées. TechnicalPlan 1.0.0,
ses octets canoniques et son digest propre MUST rester inchangés.

### Parcours et propriétaires

Le parcours est OBSERVE Protégé, publication C08 immuable liée à l'observation,
PREPARE_PLAN Protégé retournant le bundle PA, présentation et consentement
C08, puis nouveau PREPARE Critique signé ; READ_RESULT reste une nouvelle
lecture Protégée. Les trois opérations 1.0 sont conservées sous enveloppes
1.1 distinctes, exclusivement via PZT/A07. Le catalogue et TechnicalPlan/hash
1.0 restent inchangés. La matrice des identifiants/corrélations et les champs
fermés sont spécifiés dans contracts.md E5.

PA possède observation/préconditions/effets/plan/planning et leur résolution
technique actuelle ; C08 possède projection/intention et le seul bundle de
confirmation. Les profils sont protégés réellement utilisés, sans valeurs
de secrets ni digest de credential. Un profil expurgé ne reprend pas
l'identité d'un profil privé. Les preuves de temps et indisponibilité sont
liées explicitement, sans créer une horloge ou autorité déclarative.

Les cinq ressources SOFTWARE/CLUSTER/SERVICE/ROLE/DATABASE sont distinctes.
La garde de phase n'exige pas la lecture SQL avant le démarrage quand une
condition différée valide existe ; elle la rend obligatoire avant chaque
CREATE. Les préconditions et effets exacts sont confirmés avant exécution.
Une dérive arrête le reste sans CREATE vers REUSE ni compensation destructive.
Le cas REUSE/sans effet impose encore les contrôles actuels complets avant
SUCCEEDED. Ni inspect ni persistance du plan ne consomme un mandat Critique,
n'étend NV ou ne prépare PostgreSQL.

La provenance de chaque invocation réelle reste distincte : tableaux de la
projection 1.0 immuables, mandats de lecture liés à leurs propres A07, nouveau
mandat critique lié à son A07 ultérieur. Le nouveau bundle C08 ne contient
pas ces tableaux redondants, afin de ne pas inventer un contexte futur.

Cette transcription ne livre aucun producteur natif ou transport. La
réalisation reste partielle : D14 manager/unité/artefacts/politique/UTC/garde,
client matière TLS/PZT, handlers/résultats, reprise et lifecycles restent.
Les tests et validation produit suivront sur LXC selon l'instruction actuelle.
Aucune primitive RPC systemd, nouvelle dépendance, installation ou effet
n'est autorisé par ce lot documentaire.


## Admission PA B adoptée — principe
B retenu : type/codec d'amorçage distinct du `JournalTransition` PG 1.0, PG/E4/E5/catalogue 3 et D10-D13 intacts. Clé administrative PA Ed25519, pin, identité, domaine `PA_ADMIN_INITIAL`, version fixes hors candidat dans artefact authentiquement installé ; TCB distribution/procédure/OS assumée avec limites si privilège compromis, sans measured boot implicite. Chaîne imposée : prépublication/politique indépendante → vrai plan PA extérieur → constats réels/bootstrap/ancrage → publication finale, acyclique. Signature admin = admission configuration, jamais mandat E4, confirmation, NV ou SQL. Retrait autorité PA distinct D6 Z12, sans réouverture ni migration adoptée. Aucun code B autorisé par cette inscription.


## Retrait initial PA — adoption de principe et lot 12
Adoption humaine `call_f6bf98fe745b4104aa31c80d87a860b7/0` : adoption de principe et lot 12. Signataire : clé PRIVÉE personnelle opérateur Ed25519 hors runtime et hors agents, ni clé admin B ni Z12/CA/TLS. Confirmeur C08 autorisé C03/C04 réellement lié au signataire par propriétaire courant, jamais mapping auto SuperAdmin. Mandat Critique domaine `PA_POSTGRESQL_WITHDRAWAL`, droit `WITHDRAW_PA_INITIAL` de politique PA courante ; PA vérifie positivement puis ancre le retrait irréversible. Signatures, domaine et droit adoptés ; ordre, mapping PZT et wires à fermer en revue commune avant code, sans rouvrir le choix. PG1.0, E4, E5, D10-D13, remise minimale PBO et Z12 inchangés ; aucun binaire, mode, service ou canal nouveau. Contraintes contractuelles seules, aucun provider ni résolveur livré.


### Statut courant du lot documentaire B et du retrait — formats proposés, non adoptés

Le principe B reste acquis : une admission PA initiale distincte du journal PG 1.0, sans confusion avec les mandats E4, les confirmations ni les effets NV/SQL. Cette adoption de principe ne vaut pas adoption des formats, du raccord au journal ou des séquences de réalisation.

Restent des propositions à valider : les enveloppes signées PUB/FIN et leur ancrage ; le plan extérieur ; Plan15, Recipe13, BASE8, l’enregistrement R0, Policy14, Resource24, Context8, INIT_A12 et Provenance28 ; le scanner et l’admission par étapes ; ainsi que le mapping des objets et intentions vers JournalTransition et les séquences de publication. Les formats détaillés du retrait — PLAN16, CONF17, PROOFS18, Intent7, AdminMandate27 et leurs bindings — restent également proposés, sans adoption.

Le choix opérationnel INIT A, acquis séparément le 26 octobre 2026, conserve son périmètre : entrée publique explicite de 32 octets et opérations matérielles extérieures distinctes, sans genèse ni reset implicite. Il n’adopte ni le format INIT_A12, ni le plan ou le raccord au journal. Les alternatives B/C de provisionnement restent non retenues. La compatibilité à la référence 1.38 et la qualification matérielle restent à vérifier.

Les principes de retrait déjà adoptés concernant le signataire, le domaine et le droit courant restent distincts des formats détaillés et du mapping de preuve. C08 a jugé la proposition documentaire de retrait recevable, sans l’adopter (rapport auteur msg_1774aedb2001O1uGQQaB73iuqs). Aucune adoption Z12 n’est déduite de cette relecture.

Les codecs et recettes de forme déjà consignés restent des éléments historiques limités à leur preuve déclarée ; ils n’adoptent pas les formats ni ne qualifient l’admission, la signature courante, le journal, le retrait ou les effets matériels/SQL. Aucun code d’admission B, effet TPM/SQL, port qualifié ou livraison n’est autorisé par le présent statut. La présentation du lot complet demeure un jalon préalable à toute réalisation B.
## Annexe du 26 octobre 2026 — fondations B écrites, non testées

Le lot documentaire B/retrait + INIT A reste adopté sans modification ni revalidation ; les historiques sont conservés. Sous mandats CAB unitaires, le code autorisé a ensuite été écrit (copies fidèles UTF-8/LF) : trois codecs publics de forme — Context8 (huit champs), NV7 (sept champs), INIT12 (douze champs) — et leur graphe optionnel fermé dans le générateur et le constructeur. Quand une source est présente, chaque garde exige : module canonique unique, opérations vides, dépendances PG (plus NV pour INIT12) uniques, canoniques, couvrant tous les rôles du codec ; aucun System-only n'est ajouté à ces codecs publics. Preuves exactes des dix fichiers : voir l'annexe VALIDATION.md du même jour.

État vérifié : 58 fichiers suivis, 25 de réalisation (23 src + 2 native) et 33 de tests ; 131 méthodes préparées (43 Context8 + 37 NV7 + 33 INIT12 + 9 générateur + 9 constructeur), NON EXÉCUTÉES ; seule la coche historique 1 subsiste, tâches 2 à 10 non cochées ; aucune syntaxe, import, compilation, unité ou qualification produit.

Reste dû : Base8, Resource24, Policy14, PUB/FIN, recette et R0, provenance, scanner mixte, admission et retrait effectifs ; vrais producteurs et résolveurs D11/D13/D14/temps/PZT/handlers/résultats/lifecycles, puis campagne LXC et effets matériels sous plan exact distinct. Aucun port livré, admission, NV/SQL, installation, secret, Git ou archive.

## Réalisation partielle Base8 — 26/10/2026, FORME PYTHON seulement

Base8 écrite (8 champs exacts, coords à 2, ContentBinding entiers ; derive publique depuis INIT12/Context8 avec rapprochements installation/cible/binding, attendue dérivée sans TPM/HMAC/autorité) et graphe optionnel fermé (PG/Context/INIT canoniques couvrants, NV transitive conservée, sans Sys-only). Preuves : 37 recettes codec + 69 graphes + syntaxe cumulée 12 fichiers (toutes unités, pas 12 propres Base), VALIDATION.md ; périmètre Python forme/composition, sans mécanisme matériel ni qualification globale.


## Annexe Resource24 — 26/10/2026, FORME PYTHON et métadonnées seulement

Resource24 écrite (24 champs exacts, PayloadLimits PG externe, ContentBinding entier, bornes uint32/uint64/int63, observation >0 sans plafond, couplages époque/séquence/record+58, SIZE_MAX via struct N, sans deadline ni horloge) et graphe optionnel fermé (module canonique unique, opérations vides, un PG canonique unique couvrant tous les rôles Resource, sans System-only ni moteur/admission). Preuves : 55 recettes codec + 75 graphes (34 générateur dont 3 Resource + 41 constructeur dont 3 Resource) + syntaxe 2 + 4 fichiers, voir VALIDATION.md. Corpus courant : 280 méthodes distinctes sur 7 modules en 6 commandes finales (43+37+33+37+55+75, ancien graphe 69 remplacé sans addition), 14 fichiers Python syntaxe validée, 62 fichiers suivis (27 réalisation incl. 2 native + 35 tests). Scope forme Python/métadonnées ; pas Cython/link/builtin positif, 32 bits réel, LXC, TPM, NV/PG effet, PZT, admission, installation, Git, archive. Aucune coche 2-10. Ancien strict Base reste preuve antérieure ; validation ciblée du change PA01 --strict --no-interactive à exécuter après ces 4 écritures.


## Annexe Policy14 — 26/10/2026, FORME PYTHON et graphe seulement

Policy14 écrite FORME PYTHON (14 champs exacts, comparaisons DATA et binding Resource entier, PG/NV/Resource réels, 0<span_ns<=borne profil inclusive, entiers/canon/refus/UTF8/JSON) sans authentification d'origine, admission, retrait, runtime ni production. Revue Root de nature documentaire, aucune signature Root créée.

Graphe facultatif à opérations vides, PG+NV+Resource uniques couvrant les rôles, sans Context direct ni System-only ; gardes produits inchangées, premier refus précis. Preuves : source+recettes 13 PASS et syntaxe 2, graphe 81 PASS (37 générateur+44 builder) et syntaxe 4 ; détail en [VALIDATION.md](VALIDATION.md).

Corpus courant : 481 méthodes distinctes sur 19 modules en 17 commandes finales, soit 43+37+33+37+55+13+81+56+5+10+8+31+12+10+17+19+14=481 ; 50 fichiers Python syntaxe validée, 64 fichiers sources (28 réalisation dont 2 native+36 tests) ; graphe 81 REMPLACE 75 sans additionner 63/69/75 ; détail des 10 unités en VALIDATION.md ; 12 harness natifs syntaxe seule sans exécution.

Reste PUB/FIN, recette R0, plan extérieur, provenance, scanner, admission/retrait opérationnel, providers D11/D13/D14/temps/PZT/handlers/résultats/lifecycles, LXC/natif/qualification ; natif Cython/TPM/PG non qualifié par Python ; D1 candidate 3.14.9/Cython 3.3.0 préservée, hôte 3.14.10 non baseline ; aucun port/TCB/SDK/LXC/builtin/Cython/link/NV/SQL/PZT/install/Git/archive/global prouvé. Prévol hôte LOCAL seul Cython absent et headers partiels, pas CT100.

Snapshot CISMP 1080 / ACSP 880 cohérent ; futur BLOCKERS avant clôture, nettoyage après archive+stats, puis commit GLOBAL par Root seul à 3 clés filtrées et branche stable/quiescence ; aucun Git actuel ni par OC. Indépendants non épuisés, pas de clôture. LXC SSH confirmé, DEVOPS humain à jour sans édition Root/OC ; outils LXC autorisés et conservés, seuls tests propres nettoyés ; sudo pct local refusé non retenté, SSH via infos autorisées ; sur ce lot aucune valeur d'accès LXC ni project.env lue, sans remettre en cause l'extraction filtrée d'identité initiale autorisée. Strict ciblé APRÈS ces 4 écritures, ancien strict Resource historique ; B/INIT_A/C08/Z12 inchangés ; aucune coche 2-10.

## Adoption documentaire du lot B et du retrait — décision développeur du 3 novembre 2026

Le développeur a validé le lot documentaire présenté le 3 novembre 2026. Les définitions détaillées déjà consignées dans les documents PA01 pour les enveloppes signées PUB/FIN et leur ancrage, le plan extérieur, Plan15, Recipe13, BASE8, l’enregistrement R0, Policy14, Resource24, Context8, INIT_A12 et Provenance28, le scanner et l’admission par étapes, le mapping vers JournalTransition et les séquences de publication, ainsi que PLAN16, CONF17, PROOFS18, Intent7, AdminMandate27 et leurs bindings sont adoptés documentairement par PA01 dans leur contenu existant. Cette décision supersède les statuts antérieurs de non-adoption de ces mêmes formats et raccords.

Le choix opérationnel INIT A acquis séparément reste inchangé ; l’adoption documentaire d’INIT_A12 ne déclenche ni initialisation, genèse, reset ou effet matériel. Les principes de retrait relatifs au signataire, au domaine et au droit courant restent ceux déjà adoptés. La revue C08 demeure une appréciation de recevabilité sans adoption formelle par C08 ; aucune adoption Z12 n’est déduite.

Cette adoption est documentaire uniquement. Elle n’autorise ni code B, ni effet TPM/SQL, ni port qualifié, qualification runtime ou Docker, activation, livraison ou archivage. Les cases des tâches restent inchangées ; les preuves historiques de forme et de recette conservent leurs limites déclarées.

## Statut courant du lot B et du retrait — directive développeur confirmée le 3 novembre 2026

Le principe B reste acquis. Les formats détaillés B, le plan extérieur, INIT_A12, les séquences de publication et le raccord à JournalTransition restent NON ADOPTÉS ; le choix opérationnel INIT A n’adopte pas INIT_A12. Les formats détaillés de retrait (PLAN16, CONF17, PROOFS18, Intent7, AdminMandate27 et bindings) restent proposés sans adoption. C08 a jugé la proposition recevable sans adoption formelle ; aucune adoption Z12 n’est déduite.

Les codecs et essais de forme déjà consignés restent des preuves historiques limitées, sans qualification de signature, admission, journal, retrait, TPM/SQL, livraison ou activation. Aucune tâche n’est cochée ; la tâche 3 reste ouverte. Aucun code B ni effet matériel/SQL n’est autorisé.

Ce statut courant supersède les mentions antérieures d’adoption documentaire du lot B et du retrait ; les contenus historiques sont conservés pour la traçabilité.

## Statut courant du lot B et du retrait — décision développeur du 4 novembre 2026

Le principe B reste acquis. Les formats détaillés B — enveloppes signées PUB/FIN et leur ancrage, plan extérieur, Plan15, Recipe13, BASE8, R0, Policy14, Resource24, Context8, INIT_A12, Provenance28, scanner, admission par étapes, mapping vers JournalTransition et séquences de publication — restent NON ADOPTÉS. Le choix opérationnel INIT A, acquis séparément, ne vaut pas adoption de INIT_A12, du plan extérieur, du mapping au journal ou des séquences de publication.

Les formats détaillés du retrait — PLAN16, CONF17, PROOFS18, Intent7, AdminMandate27, claims et bindings — restent proposés sans adoption. C08 a jugé la proposition documentaire recevable sans l’adopter ; aucune adoption Z12 n’est déduite. Les principes déjà adoptés concernant le signataire, le domaine et le droit de retrait restent distincts de ces formats détaillés.

Cette décision du 4 novembre supersède les mentions historiques du 3 novembre qui indiquent l’adoption documentaire de ces formats et raccords, sans les supprimer ni altérer les preuves historiques. Les codecs et essais de forme restent limités à leur portée et ne qualifient ni signature, admission, journal, retrait, effets TPM/SQL, runtime/Docker, livraison ou activation. Aucune tâche n’est cochée ; la tâche 3 reste ouverte. Aucun code B ni effet TPM/SQL n’est autorisé, et aucune qualification nouvelle n’est déduite.
