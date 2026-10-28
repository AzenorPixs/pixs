# PA01 — Préparation du raccord de l'enveloppe de campagne

Statut : PRÉPARATION_DOCUMENTAIRE ; RACCORD_NON_IMPLÉMENTÉ ; RECETTES_NON_EXÉCUTÉES.

Le développeur a confirmé le 26 octobre 2026 : préparation documentaire
uniquement, sans code ni implémentation. Ce document décrit le travail futur
et ses critères de revue. Il ne crée aucun module, fichier de test, enveloppe
réelle, sélection courante ou preuve de qualification.

## Références et périmètre

Les quatre exigences d'enveloppe du [canon pixs-agent](../../specs/pixs-agent/spec.md),
leur [delta](specs/pixs-agent/spec.md) et le [contrat du design](design.md#enveloppe-de-métadonnées-de-campagne-pa01--complément-du-26-octobre-2026)
restent la référence. La présente préparation ne les modifie pas et ne
resynchronise aucun delta.

Le raccord conserve le profil fermé v1, son verrou `toolchain.cython`, les
choix CPython/GIL/ABI/cibles adoptés et les quatre exécutables. Le profil de
build et l'enveloppe sont deux documents distincts, même si chacun déclare
un schéma `1.0.0`. Aucune clé d'enveloppe n'est ajoutée au profil existant.
La copie du verrou dans l'enveloppe ne devient pas une autorité concurrente.

## État du code observé

| Élément existant | Observation | Travail restant pour ce raccord |
| --- | --- | --- |
| [build_profile.py](../../../src/pixs/pa_native/build_profile.py) | `parse_profile` conserve le verrou dans `BuildProfile.cython_version` et refuse les formes de version interdites. | Conserver ce contrat et son schéma ; valider séparément l'enveloppe. |
| [builder.py](../../../src/pixs/pa_native/builder.py) | `compile_objects` reçoit le profil, les sources, la chaîne et les budgets ; il ne reçoit pas encore l'enveloppe ni le manifeste pour ce rapprochement. | Ajouter des entrées explicites et les contrôles de campagne, sans valeur implicite ni chemin de repli. |
| Sonde et rapport existants | Le constructeur compare la version Cython observée au profil et trace `profile_sha256` et `cython_version.locked/observed`. | Conserver ces champs et ajouter identité, empreinte d'enveloppe, distributions vérifiées et issue du rapprochement. |
| Recettes existantes | Les tests unitaires du profil et du constructeur, ainsi que les recettes natives de construction et de liaison, appellent les interfaces actuelles. | Adapter leurs entrées lors de la réalisation ; leur existence ne couvre pas le nouveau raccord. |

Les observations ci-dessus proviennent d'une lecture des sources. Aucun
test produit ni import du code produit n'est exécuté pour cette préparation.

## Contrat d'entrée du raccord à réaliser

Les entrées suivantes sont fournies explicitement par l'appelant. Les noms
définitifs des paramètres et l'emplacement d'un éventuel module dédié seront
arrêtés dans le lot de réalisation ; aucune signature exécutable n'est écrite ici.

| Entrée | Contrat et responsabilité |
| --- | --- |
| Profil de build existant | Conserver son texte et son traitement actuels ; `toolchain.cython` du profil reste le verrou de référence. |
| Octets de l'enveloppe | Lire et conserver les octets UTF-8/LF effectivement validés, sans interpolation ni réécriture ; leur empreinte est celle portée par le rapport. |
| Dossier de l'enveloppe | Fournir la racine explicite de résolution de `selection.snapshot` ; aucune recherche implicite depuis le répertoire courant ou l'environnement. |
| Octets du manifeste | Fournir le `pyproject.toml` de la construction, puis en extraire l'unique déclaration exacte Cython de `[build-system].requires`. Ne pas remplacer cette déclaration par la version installée. |
| Relevé et fichiers de distribution | Résoudre les fichiers locaux déclarés et comparer leurs octets, noms, URL et empreintes aux métadonnées et au relevé figé. Le contrôle ne télécharge rien. |
| Dossier de sélection vérifiée | Conserver la vérification officielle datée avec les preuves de campagne. Un relevé local ou son SHA-256 seul ne démontre pas son origine officielle. |
| Sources, chaîne et budgets existants | Conserver les entrées et contrôles actuels ; l'enveloppe ne change pas implicitement les outils, budgets, sources ou cibles. |

Une enveloppe manquante n'est pas reconstruite depuis le profil. Un manifeste
manquant n'est pas remplacé par une recherche de paquet installé. Aucune
ancienne voie d'appel ne contourne le contrôle en omettant l'enveloppe.
L'adaptation des appelants et des fixtures fait partie du même lot futur.

## Découpage et ordre des contrôles

| Étape | Travail à réaliser | Barrière et preuve attendue |
| --- | --- | --- |
| 1 — Structure | Analyser le profil existant, l'enveloppe fermée et la déclaration du manifeste ; préserver leurs octets effectifs. | Aucun sous-processus ni compilation. Un schéma invalide ferme le contrôle ; aucune entrée n'est corrigée automatiquement. |
| 2 — Preuves locales | Vérifier le chemin du relevé, son intégrité, la sélection datée et les distributions déclarées. Séparer cohérence du relevé et preuve de son origine officielle. | Aucun réseau, téléchargement ou installation. Une preuve absente, altérée ou non concluante ferme le contrôle. |
| 3 — Rapprochement des déclarations | Comparer le verrou du profil, sa copie dans l'enveloppe et la déclaration exacte du manifeste. | Toute divergence refuse la construction avant lancement des outils. |
| 4 — Admission du contexte de construction | Conserver les contrôles existants du dossier de sortie, des sources, des outils et des budgets. Préparer le rapport seulement dans un dossier de sortie admis. | Aucun écrasement d'une sortie existante ni création de rapport dans un chemin refusé. Une erreur avant admission est restituée comme diagnostic, sans rapport inventé. |
| 5 — Observation | Exécuter les sondes locales admises avec la chaîne réellement utilisée, puis comparer la version observée aux trois déclarations déjà rapprochées. | Aucune génération Cython ni compilation C avant concordance. Une stable plus récente que le verrou reste un écart. |
| 6 — Construction et rapport | Autoriser la construction d'objets seulement après les contrôles précédents ; rattacher les entrées et distributions vérifiées au rapport. | Le rapport conserve refus ou résultat observés ; sa présence ne qualifie pas les exécutables PA/PZT. |

Les fichiers vérifiés doivent rester ceux effectivement utilisés. Un
remplacement ou une altération entre vérification et utilisation invalide
la preuve et ferme la construction ; aucune empreinte ancienne n'est recyclée.
Les moyens de conservation et de revalidation des fichiers seront examinés
avec la réalisation, sans ajout de dépendance imposé par cette préparation.

## Refus et compte rendu

Les quatre codes du contrat sont conservés :

| Code | Situation attendue |
| --- | --- |
| `PA01_CAMPAIGN_METADATA_INVALID` | Schéma d'enveloppe invalide, mauvaise identité de composant, champ absent/inconnu/dupliqué/mal typé ou verrou de forme interdite. |
| `PA01_CAMPAIGN_EVIDENCE_INVALID` | Relevé ou distribution absent, altéré, non déclaré ou incompatible avec les preuves de sélection. |
| `PA01_BUILD_CYTHON_METADATA_INVALID` | Sonde absente, inexploitable, ambiguë ou mal typée. |
| `PA01_BUILD_CYTHON_MISMATCH` | Divergence de version entre profil, enveloppe, déclaration exacte ou observation. |

Les autres erreurs existantes du profil, des chemins, des outils ou des
budgets gardent leur cause et leurs diagnostics ; elles ne sont pas masquées
par un code générique d'enveloppe.

Dans un contexte de sortie admis, le rapport conserve `profile_sha256` et
`cython_version` avec `locked` et `observed`, et ajoute `campaign_id` et
`campaign_metadata_sha256`. Il trace les distributions réellement vérifiées
et l'issue du rapprochement. Si aucune version exploitable n'est obtenue,
`observed` reste `null` ; une version exploitable mais différente reste tracée
avec une issue de refus. Le rapport ne participe pas aux empreintes de ses
propres entrées et ne présente pas une entrée non vérifiée comme vérifiée.

## Recettes préparées — aucune exécution

Les identifiants ci-dessous représentent 19 groupes de recettes. Chaque
groupe peut nécessiter plusieurs cas. Ils sont tous NON EXÉCUTÉS ; aucune
méthode de test, aucun résultat PASS et aucun nombre de tests exécutés n'est
déduit de cette matrice.

Références : M = métadonnées fermées ; S = preuve de sélection ;
D = distributions ; R = rapport lié au verrou. Ces lettres désignent les
quatre exigences d'enveloppe existantes, sans ajouter d'exigence normative.

| Groupe | Référence | Déclencheur et résultat attendu | Preuve à recueillir lors de la réalisation |
| --- | --- | --- | --- |
| V01 | M | Enveloppe PA01 fermée nominale : conserver identité et verrou sans modifier le profil de build. | Valeurs analysées, empreinte d'entrée et absence de sous-processus. |
| V02 | M | Champ inconnu, absent, dupliqué ou mal typé : refus de métadonnées. | Cas séparés et code exact, sans sous-processus. |
| V03 | M | Enveloppe PBO, mauvais composant ou version de schéma : refus, sans conversion vers PA01. | Identité du cas et refus, sans valeur de remplacement. |
| V04 | M | Contrainte ouverte, préversion, développement, version locale ou non normalisée : refus ; formes finales et `.postN` admises seulement structurellement. | Cas de forme et distinction explicite avec publication/qualification. |
| V05 | S | Date invalide, non textuelle ou sans UTC, ou source différente : refus selon schéma ou preuve. | Code correspondant à la phase effectivement refusée. |
| V06 | S | Relevé absent, sortant, symbolique ou à empreinte erronée : refus avant outils. | Fichier de fixture identifié, empreinte et compteur de sous-processus nul. |
| V07 | S | Relevé avec préversion plus récente, stable retirée ou preuve ne démontrant pas la sélection : ne pas admettre une version interdite ni considérer le SHA seul comme origine officielle. | Décision comparée aux données figées ; portée de fixture clairement indiquée. |
| V08 | D | Liste vide, doublon, nom/URL invalide, distribution retirée, non déclarée ou altérée : refus avant outils. | Sous-cas distincts, octets contrôlés et absence de compilation. |
| R01 | R | Copie d'enveloppe différente du profil : refus de version avant outils. | Profil, enveloppe, code de refus et compteur de sous-processus nul. |
| R02 | R | Déclaration Cython manquante, ambiguë ou non exacte, ou différente du verrou : refus sans recherche de remplacement. | Manifeste de fixture et refus ; aucune installation ou réécriture. |
| R03 | R | Sonde absente, JSON inexploitable, champ supplémentaire, mauvaise valeur typée ou ambiguë : refus de sonde. | Reçu de sonde, diagnostic et `observed=null` si inexploitable. |
| R04 | R | Sonde exploitable avec version stable différente, y compris plus récente : refus avant génération Cython et compilation C. | Versions verrouillée/observée, rapport de refus et compteurs de compilation nuls. |
| R05 | R | Quatre versions identiques et preuves admises : franchir le contrôle, sans qualifier le produit par la seule sonde. | Rapport lié aux entrées ; frontière exacte atteinte dans le constructeur. |
| R06 | S/D/R | Remplacement du relevé ou d'une distribution après vérification : invalider la preuve, sans réutiliser l'ancienne empreinte. | Observation avant/après et refus sans compilation sur la donnée remplacée. |
| R07 | R | Échec avant admission du dossier de sortie, puis échec après admission : distinguer diagnostic sans rapport et rapport de refus sûr. | Absence de sortie étrangère/écrasée ; rapport uniquement dans le contexte admis. |
| R08 | M/R | Reproduction puis campagne suivante : conserver les premières entrées, sans nouvelle sélection pour reproduire ni réécriture des preuves historiques. | Identifiants et empreintes avant/après ; aucun accès réseau du constructeur. |
| N01 | M/S/D/R | Chaîne native autorisée avec enveloppe et distributions réelles admises : contrôler puis construire des objets de fixture. | Versions, sources, empreintes, commandes, objets et rapport réel ; pas de qualification des exécutables PA/PZT. |
| N02 | R | Version réelle Cython différente du verrou : refus sans génération/compilation. | Sonde réelle et absence effective des étapes de compilation. |
| N03 | M/S/D/R | Reproduire la même campagne native avec les mêmes entrées et conserver ses preuves ; une nouvelle campagne reste distincte. | Comparaison des entrées, rapports et artefacts selon la recette de reproductibilité retenue. |

V et R peuvent utiliser des fixtures et sondes simulées ; elles ne démontrent
ni origine réseau officielle ni compilation native. N exige les outils,
distributions, environnement et autorisations réels du lot futur. Aucune
installation, recette conteneurisée, opération TPM/SQL/PZT ou exécution d'un
exécutable PA n'est autorisée par ce document.

## Fichiers et appelants à examiner dans le lot de réalisation

| Périmètre proposé | Travail futur |
| --- | --- |
| Nouveau module de validation dédié sous `src/pixs/pa_native/` | Séparer analyse pure de l'enveloppe et contrôle de ses preuves locales ; réutiliser les types d'erreur et règles du projet. Aucun fichier n'est créé ici. |
| [builder.py](../../../src/pixs/pa_native/builder.py) | Raccorder les entrées et phases ci-dessus ; préserver le contrôle Cython existant et compléter le rapport. |
| [Tests du profil](../../../tests/unit/test_pa_native_build_profile.py) | Vérifier que le schéma fermé v1 et le verrou de référence restent inchangés. |
| [Tests du constructeur](../../../tests/unit/test_pa_native_builder.py) et futur module de tests d'enveloppe | Adapter les fixtures et couvrir V/R, sans présenter les sondes simulées comme qualification native. |
| [Recette native du constructeur](../../../tests/native/test_object_builder.py) | Adapter tous les appels à `compile_objects` et préparer N avec les vraies entrées de campagne. |
| [Recette native du lieur](../../../tests/native/test_object_linker.py) | Adapter son appel existant au constructeur ; ne pas casser le prérequis de liaison en laissant une ancienne voie sans enveloppe. |

Le relevé ciblé actuel ne trouve pas d'autre appel à `compile_objects` dans
`src/pixs/pa_native/` et `tests/native/`. Cet inventaire est à revérifier avant
la réalisation. Tout appelant supplémentaire découvert doit être examiné,
sans voie de compatibilité qui omette les contrôles de campagne.

## Conditions à fermer et validation future

La [procédure de preuve officielle datée](PREUVE_SELECTION_PA01.md) définit
désormais la collecte contrôlée, le manifeste figé et l'admission explicite
dans un registre protégé distinct du candidat. Le raccord futur vérifie cette
admission et son état courant par le lecteur de confiance du contexte de
build, sans accepter un booléen ou une admission fournis comme leur propre
preuve par le demandeur. Les groupes P01–P06 complètent les 19 groupes V/R/N,
sans les réécrire ni les déclarer exécutés.

La réalisation devra qualifier l'emplacement, le propriétaire, les permissions
et la conservation du registre avant toute admission réelle. Cette mise en
place et le raccord restent non implémentés ; une protection ou une preuve
indispensable manquante reste bloquante. Aucun service de signature ou
d'horodatage certifié supplémentaire n'est sélectionné.

Avant de cocher une tâche, relier chaque groupe applicable aux sources et
empreintes finales, commandes réellement exécutées, compte rendu natif,
postconditions et nettoyage. Les recettes de raccord restent distinctes
de la qualification de la chaîne, des exécutables, des plateformes et du
parcours intégré PA/PZT. Les preuves historiques ne sont pas réattribuées
au raccord à réaliser.

## Vérifications de cette préparation documentaire

Trois documents sont écrits par cette intervention : le présent dossier,
`design.md` et `tasks.md` pour leurs renvois. Les 19 groupes V/R/N sont
préparés, non exécutés ; aucun fichier de source ou de test n'est écrit.
Les états des tâches sont conservés. Les empreintes surveillées des sources
Python PA01, des deux modules de tests unitaires du profil et du constructeur,
des capacités canoniques, des deltas, du change PBO et de `pyproject.toml`
restent inchangées. Des évolutions concurrentes de `proposal.md` et
`DETAIL_A1_A2_A3.md` sont observées et laissées intactes par cette intervention.

Avec OpenSpec 1.15.0, le contrôle
`openspec validate --all --strict --json --no-interactive` retourne le code
natif 0 : 185 éléments valides sur 185, soit 107 changes et 78 capacités,
sans erreur ni avertissement. Les 86 diagnostics INFO restent identiques
au relevé précédant cette préparation. Les contrôles des trois documents
réussissent : UTF-8/LF, espaces, liens et ancres, correspondance des champs
et codes, ainsi qu'unicité des 19 identifiants de groupes de recettes.
Ces résultats sont des validations documentaires, sans test du raccord,
qualification native, installation, archivage, commit ou push.
