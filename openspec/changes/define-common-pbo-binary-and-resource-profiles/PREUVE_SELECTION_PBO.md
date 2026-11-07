# PBO — Établissement et conservation de la sélection officielle datée

Statut : CONTRAT_DOCUMENTAIRE ; AUCUNE_PREUVE_RÉELLE_ÉTABLIE ; NON_IMPLÉMENTÉ.

Le développeur autorise le 27 octobre 2026 la définition de cette procédure,
sans code ni implémentation. Aucun relevé de campagne, téléchargement de
distribution, manifeste de preuve ou décision d'admission réel n'est créé.
Le verrou reste `toolchain.nuitka` des métadonnées de campagne PBO.
L'enveloppe fermée, ses onze champs et les autres choix de chaîne restent
inchangés. Ce contrat reprend la [preuve officielle PA01](../add-pa-native-build-and-component-composition/PREUVE_SELECTION_PA01.md),
sans réutiliser une admission PA01 comme admission PBO.

## Mécanisme retenu et limites

La preuve est un dossier figé après observation directe de la source officielle,
lié par ses empreintes à une revue explicite et à une admission conservée
hors du contrôle du demandeur de construction. Le développeur, ou un
responsable de campagne explicitement délégué, effectue cette revue.
Préparation et admission sont deux opérations distinctes ; cette règle
n'impose pas deux personnes différentes, mais exige que l'autorité de revue
soit établie indépendamment des valeurs fournies dans le dossier candidat.

L'autorité de la preuve repose sur le contexte de collecte contrôlé, la
validation HTTPS, l'horloge UTC utilisée, la revue autorisée et la protection
du registre d'admission. Le dossier atteste une observation et une décision
opérationnelles datées. Il ne constitue ni un horodatage public certifié,
ni une signature de PyPI, ni une garantie contre la compromission du
responsable ou de l'administration du registre. Aucun service de signature,
de PKI ou de temps certifié supplémentaire n'est adopté ici.

## Établir l'observation officielle

1. Ouvrir une nouvelle campagne PBO et relever les identités du responsable,
   du contexte de collecte et de l'autorisation qui lui permet d'admettre la
   sélection. Une campagne historique reproduite ne recommence pas cette sélection.
2. Consulter directement `https://pypi.org/pypi/Nuitka/json` depuis ce contexte
   contrôlé, avec validation HTTPS et nom d'hôte actifs, sans désactivation
   des contrôles TLS, miroir implicite, cache local pris pour une réponse
   officielle ou redirection vers un autre point d'entrée. Exiger une réponse
   HTTP 200 exploitable ; un échec bloque la sélection.
3. Conserver les octets du corps JSON reçu, sans le réécrire. Relever en UTC
   début et fin de collecte, URL demandée et finale, statut HTTP, référence
   du client et de sa politique de validation TLS. Ne conserver aucun secret,
   cookie d'authentification, clé ou contenu de certificat. Les seules
   données de connexion conservées sont ces références non secrètes.
4. Examiner les versions publiées et leurs fichiers. Retenir la version
   publique finale ou `.postN` la plus élevée selon PEP 440, avec au moins un
   fichier publié non retiré ; exclure préversions, développement et versions
   locales. Le nom du projet doit correspondre à Nuitka. Ne pas se limiter
   à `info.version`, ni utiliser un tri lexical ou un filtre de compatibilité
   pour choisir silencieusement une version plus ancienne.
5. Justifier dans la revue la version retenue et les exclusions décisives.
   Vérifier pour chaque distribution prévue nom, URL et SHA-256 officiels,
   état non retiré et empreinte des octets réellement conservés. La collecte
   d'un fichier n'autorise ni son installation ni son exécution.
6. Fixer `selection.verified_at` à la fin de l'observation officielle réussie,
   puis conserver la date de revue séparément. Une horloge indisponible,
   incohérente ou non vérifiable empêche l'admission ; aucune date antérieure
   n'est inventée après coup. Ne pas déduire cette date du seul en-tête HTTP.

L'[API JSON PyPI](https://docs.pypi.org/api/json/#get-a-project) décrit les
versions, fichiers, URL et condensats retournés. Sa clé `releases` est
dépréciée : si l'information nécessaire pour établir la dernière stable
n'est plus disponible ou complète, la procédure reste bloquée. Elle ne
bascule pas implicitement vers une autre API ; une évolution du contrat
de collecte doit alors être explicitement adoptée.

## Figer le dossier et son manifeste

Le dossier candidat contient les octets effectivement utilisés : profil de
build, enveloppe, `pyproject.toml`, relevé JSON et chaque distribution prévue.
Les chemins sont relatifs au dossier, canoniques, sans remontée ni lien
symbolique. Les noms de fichier concrets ne sont pas des chemins d'installation
ou des options CLI nouveaux. Une copie de travail mutable n'est jamais
confondue avec le dossier admis.

Le manifeste de preuve est un document JSON fermé. Il a exactement les
champs ci-dessous ; tout champ absent, inconnu, dupliqué ou mal typé est refusé.
Les textes sont non vides et sans caractères de contrôle ; les fichiers texte
sont UTF-8/LF, les dates des textes UTC et les SHA-256 des textes hexadécimaux
minuscules de 64 caractères.

| Champ du manifeste | Valeur et liaison |
| --- | --- |
| `schema_version` | Texte exact `1.0.0`, version de ce seul manifeste de preuve. |
| `campaign_id` | Identique à `campaign.id` de l'enveloppe. |
| `component` | Texte exact `pbo`. |
| `nuitka_version` | Identique à `toolchain.nuitka` des métadonnées de campagne et à la déclaration Nuitka exacte de `pyproject.toml`. |
| `verified_at` | Identique à `selection.verified_at` et à la fin de collecte admise. |
| `source_url` | Texte exact `https://pypi.org/pypi/Nuitka/json`. |
| `acquisition` | Table fermée : `requested_url`, `final_url`, `started_at`, `finished_at`, `http_status`, `client_ref`, `tls_policy_ref`. Les URL sont celles attendues, le statut entier vaut 200, début précède ou égale fin. Les références décrivent le contexte observé ; elles ne valent pas preuve par leur seul contenu. |
| `files` | Liste non vide de tables fermées `role`, `path`, `sha256`. Exactement une entrée pour chacun des rôles `build_profile`, `campaign_metadata`, `pyproject`, `pypi_snapshot`, et une ou plusieurs entrées `distribution`. Les chemins sont uniques et chaque distribution utilisée est couverte. |

Le relevé et son empreinte correspondent aussi à `selection.snapshot` et
`selection.snapshot_sha256` ; les distributions correspondent à celles de
l'enveloppe. Le manifeste ne s'inclut pas lui-même et n'inclut ni décision
d'admission ni rapport dérivé. Son SHA-256 porte sur ses octets figés et
sert de référence à la décision extérieure, sans cycle d'empreintes.

## Revue explicite et admission indépendante

Le responsable observe la collecte dans le contexte contrôlé, examine le
relevé, le calcul de sélection et les fichiers du dossier, puis approuve le
manifeste exact par son empreinte. La décision doit être explicite et liée
à l'autorisation vérifiable du responsable. Une chaîne de caractères donnant
son nom, une capture d'écran seule ou un booléen du demandeur ne suffisent pas.
Si le dossier n'a pas été observé dans ce contexte ou si son origine reste
invérifiable, refaire une observation contrôlée avant admission ; ne pas
transformer une copie locale antérieure en collecte officielle rétroactive.

L'enregistrement d'admission est conservé dans un registre de référence
protégé, distinct du dossier candidat. Le constructeur et son appelant de
construction n'ont pas le droit de modifier ce registre, ses décisions ou
ses références d'autorité. Seul le responsable autorisé peut y admettre ou
retirer une décision. Le demandeur peut indiquer une référence d'admission,
mais ne peut choisir un autre registre ni fournir son propre lecteur de confiance.

L'enregistrement d'admission JSON a exactement les champs suivants :

| Champ d'admission | Valeur et liaison |
| --- | --- |
| `schema_version` | Texte exact `1.0.0`, version de ce seul enregistrement. |
| `admission_id` | Identifiant unique, non vide, de la décision conservée. |
| `campaign_id` | Identique à l'enveloppe et au manifeste approuvés. |
| `manifest_sha256` | Empreinte des octets exacts du manifeste approuvé. |
| `reviewer_ref` | Identité non secrète du responsable dont l'autorité est vérifiée par le registre, sans la déduire de ce seul champ. |
| `authorization_ref` | Référence durable à sa délégation ou à la décision explicite du développeur ; l'événement d'autorisation est conservé séparément du candidat. |
| `reviewed_at` | Texte UTC de la revue, postérieur ou égal à l'observation officielle. |
| `decision` | Texte exact `ADMITTED`. Une absence d'admission ne vaut jamais admission. |

Le registre conserve les décisions sans les réécrire et expose leur état
courant. Un retrait est un événement distinct, daté, motivé et lié à la
décision originale ; il laisse ses preuves historiques consultables mais
bloque une nouvelle utilisation de cette admission. Une restauration de
sauvegarde ne doit pas effacer ce retrait. Si l'état courant est ambigu,
le contrôle reste bloqué au lieu de réutiliser une copie historique favorable.

L'événement de retrait est un document JSON fermé avec exactement
`schema_version=1.0.0`, `withdrawal_id` unique, `admission_id` visé,
`withdrawn_at` UTC, `reviewer_ref`, `authorization_ref` et `reason` non secret.
Il est émis par la même autorité de registre, sans modification de la décision
originale. Une admission est utilisable seulement si son enregistrement est
unique, autorisé et cohérent et si la vue complète du registre courant ne
contient aucun retrait la visant. Une vue partielle ou une lecture en échec
ne permet pas de conclure à l'absence de retrait. Une nouvelle décision
possède un autre identifiant et ne réactive pas l'ancienne par écrasement.

La réalisation devra déclarer l'emplacement du registre, son propriétaire,
les permissions de lecture/écriture et la conservation de l'autorisation,
puis prouver leur séparation vis-à-vis du constructeur et de son appelant.
Aucun chemin, UID, service ou droit d'accès réel n'est créé ou modifié ici.
Tant que cette protection n'est pas établie, aucune admission n'est utilisable.

## Vérification hors ligne avant construction

Le futur raccord lit l'admission depuis le registre configuré par le contexte
de build autorisé, vérifie son état courant et son autorisation, puis compare
identité de campagne, empreinte du manifeste et empreintes de tous les fichiers
effectivement utilisés. Il contrôle leur cohérence avec `toolchain.nuitka` des métadonnées de
campagne et la déclaration Nuitka exacte du manifeste Python avant la sonde
Nuitka et la compilation.
Il ne consulte pas PyPI et ne télécharge rien.

Admission absente, retirée, inaccessible, non autorisée ou ne correspondant
pas exactement au dossier : refus `PBO_CAMPAIGN_EVIDENCE_INVALID`, sans
compilation. Les schémas invalides et les divergences de version gardent
leurs codes spécifiques existants. Le contrôle n'accepte pas un enregistrement
copié dans le candidat, même si ses champs et son SHA-256 paraissent valides.

Le rapport ajoute aux champs de campagne déjà définis
`selection_admission_ref`, `selection_admission_sha256` et
`selection_manifest_sha256`, issus des enregistrements réellement vérifiés.
L'empreinte d'admission porte sur les octets conservés par le registre.
Une preuve non vérifiée n'est pas enregistrée comme admise dans le rapport.
Le rapport reste dérivé et n'entre pas dans ses propres entrées d'empreinte.

## Conservation et reproduction

Conserver ensemble le dossier figé, le manifeste, l'admission, l'événement
d'autorisation et les éventuels retraits tant que des artefacts de cette
campagne doivent rester qualifiables ou reproductibles. Les copies de
sauvegarde préservent ces liens et l'état courant ; aucune durée arbitraire
ni purge automatique n'est introduite. Le constructeur ne dispose pas de
droits d'écriture sur les exemplaires de référence.

Une reproduction reprend les mêmes entrées et dates, avec une admission
toujours utilisable, sans rechercher la dernière stable actuelle. Si la preuve
ou l'admission n'est plus vérifiable, la reproduction concernée reste bloquée.
Une nouvelle décision ou une nouvelle campagne conserve l'ancienne preuve,
ne remplace pas sa date et ne réattribue pas ses résultats aux nouveaux octets.

## Six groupes de recettes à réaliser ultérieurement

Les groupes P01–P06 complètent les tâches existantes de [tasks.md](tasks.md).
Ils sont NON EXÉCUTÉS : aucune méthode de test, collecte officielle, admission
réelle ou qualification n'est produite par cette définition.

| Groupe | Résultat attendu | Preuves futures nécessaires |
| --- | --- | --- |
| P01 | Une observation HTTPS contrôlée de Nuitka, une sélection correcte et une revue autorisée admettent le manifeste PBO exact. | Collecte datée, dossier et empreintes, autorisation et admission du registre ; une fixture ne prouve pas l'observation réelle. |
| P02 | Booléen auto-déclaré, faux responsable, admission copiée dans le candidat, admission PA01 ou registre substitué : refus avant outils. | Origine du lecteur, identité PBO, référence d'autorité et refus sans compilation. |
| P03 | TLS non vérifié, URL différente, source inaccessible, horloge incohérente ou liste de versions inexploitable : aucune sélection admise ni ancien compilateur choisi implicitement. | Échec observé et absence de décision d'admission favorable. |
| P04 | Altération d'un fichier, du manifeste ou échange entre campagnes après admission : refus en conservant la preuve d'origine. | Empreintes avant/après, identité du dossier et absence de compilation. |
| P05 | Admission absente, retirée, inaccessible ou état courant ambigu : refus ; une restauration ne réactive pas un ancien accord. | Événement de retrait, état courant et absence de repli sur une copie historique. |
| P06 | Reproduction avec entrées identiques et admission utilisable : dates et preuve d'origine conservées, références d'admission liées au rapport, sans appel PyPI du constructeur. | Comparaison des empreintes, rapport et absence de nouvelle sélection. |

Le complément ajoute deux exigences et six scénarios au delta
reference-runtime, sans synchronisation du canon. Aucun relevé officiel
courant, manifeste réel, décision d'admission, protection de stockage, code,
implémentation, installation, compilation, recette produit, qualification ou
archive n'est produit par cette rédaction.

## Vérifications de ce complément documentaire — 27 octobre 2026

Cinq fichiers sont écrits par cette intervention : le présent dossier,
`proposal.md`, `design.md`, `tasks.md` et `specs/reference-runtime/spec.md`.
Deux exigences et six scénarios sont ajoutés au delta, sans modification
des blocs normatifs antérieurs ni synchronisation du canon. Leur texte
concorde exactement avec les deux exigences PA01 après adaptation du nom
du compilateur et du périmètre ; les schémas de manifeste et d'admission
concordent aussi après adaptation de la clé de version et du composant.

OpenSpec 1.15.0 valide le change en mode strict et la commande
`openspec validate --all --strict --json --no-interactive` retourne le code
natif 0 : 185 éléments valides sur 185, soit 107 changes et 78 capacités,
sans erreur ni avertissement. Les 86 diagnostics INFO restent identiques
au relevé précédant ce complément, dont le diagnostic d'archivage préexistant
du change sur reference-composition.

Les contrôles des cinq fichiers réussissent : UTF-8/LF, espaces, blocs
Markdown, liens et ancres, schémas de preuve équivalents et unicité des six
groupes P01–P06. Ces groupes restent non exécutés. Les empreintes surveillées
des 78 capacités canoniques, du change PA01, de `pyproject.toml`, des sources
et des deux modules de tests unitaires du profil/constructeur sont inchangées.
Les états des tâches sont conservés, sans nouvelle coche produit.

Ces validations sont documentaires. Aucun relevé courant, sélection réelle,
admission effective, protection de registre, code, implémentation, installation,
compilation, recette produit, qualification, archive, publication, commit ou
push n'est produit par cette rédaction.
