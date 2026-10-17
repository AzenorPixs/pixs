# Références normatives — Z18

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 8311 | [Contrat A10i54 — Auxiliaire local isolé pour les acquisitions temporelles — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L8311) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 8385 | [Contrat A10i55 — Auxiliaire créé à la demande, réutilisé et arrêté après repos — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L8385) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 8432 | [Contrat A10i56 — Messages IPC JSON UTF-8 typés/versionnés, plafond 16 Kio — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L8432) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 8485 | [Contrat A10i57 — Compte système dédié à la collecte, droits minimaux — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L8485) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 8533 | [Contrat A10i58 — Transport local natif parent/auxiliaire, accès et identités contrôlés — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L8533) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 8585 | [Contrat A10i59 — Plafonds auxiliaire de premier jet 64 Mio et 50 % d’un cœur — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L8585) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 8639 | [Contrat A10i60 — Journalisation technique agrégée, transitions et erreurs — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L8639) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 8692 | [Contrat A10i61 — Messages IPC préfixés par une longueur sur 4 octets — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L8692) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 8742 | [Contrat A10i62 — Schéma JSON IPC fermé par version, champs inconnus refusés — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L8742) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 8790 | [Contrat A10i63 — Recréation technique à la demande, 3 tentatives sur 600 secondes — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L8790) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 8849 | [Contrat A10i64 — Grands entiers IPC en chaînes décimales canoniques — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L8849) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 8897 | [Contrat A10i65 — Complexité JSON IPC plafonnée à 8 niveaux, 32 membres et 32 éléments — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L8897) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--8a99885f28

Source : `openspec/specs/pzt/spec.md`, ligne 8311. SHA-256 du bloc : `39bdefbeeb40244c28a48a14d0954a5a25d93f8a1391861560561acaac18db79`.

~~~~text
### Requirement: Contrat A10i54 — Auxiliaire local isolé pour les acquisitions temporelles — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i54 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i54

API/IPC structurée en lecture A10i53 A et budgets A10i52 A conservés. Auxiliaire
local isolé retenu, sans nouveau serveur de synchronisation A10i50,
outil CLI, interpréteur ou autorité de décision introduits.

| Choix validé | Exécution | Condition de maîtrise du blocage |
| --- | --- | --- |
| A | Processus auxiliaire local isolé du processus de décision, une acquisition active au maximum | Résultat tardif refusé, arrêt/fin effective du lecteur vérifiés avant remplacement, aucune accumulation de workers |

Auxiliaire exécutant uniquement adaptateurs de lecture qualifiés A10i53,
canal local structuré/versionné et identité d'exécution/profil contrôlés.
Un auxiliaire de collecte actif au maximum par instance de validation, une
requête d'acquisition à la fois ; réutilisation/repos 300 s validés A10i55 A,
placement et quotas agrégés d'hôte/autorité à préciser avant activation.
Aucun cache de mesure entre décisions A10i51, même si le processus persiste.
Lancement/communication/lecture/analyse/annulation inclus dans budgets A10i52,
aucun lancement anticipé non mandaté réputé gratuit ou réinitialisant budget.

Processus principal contrôle délais/résultats sans attendre indéfiniment une
API du lecteur. Dépassement ou résultat après échéance : donnée inutilisable,
décision refusée et arrêt du seul auxiliaire possédé demandé sous profil autorisé.
Confirmation de terminaison/ressources libérées requise avant créneau réutilisé,
handles/PID/génération et périmètre d'arrêt qualifiés pour éviter processus
non concerné. Arrêt demandé ou simple timeout sans fin effective présumée.
Si fin non prouvée, collecte indisponible diagnostiquée, aucune création de
remplaçants ni acquisitions supplémentaires accumulées ; intervention sous
autorisation si nécessaire, aucune terminaison du PBO, CA, hôte ou service de
synchronisation pour récupérer le créneau. Pas de garantie d'arrêt instantané
du noyau/API, contrat d'indisponibilité sans résultat admissible de secours.

Association de réponse à requête/époque/génération/provider et contexte
courants, ancienne réponse/doublon d'incarnation sans nouvelle décision.
D et compteurs A10i52 conservés, nouvelle acquisition seulement après état
réconcilié et budget admissible. Auxiliaire sans accès SQL, clé racine/backup,
signature CA ou capacité de modifier horloge/mandat ; données minimales en lecture.
Compte dédié A10i57 A et JSON 16 Kio A10i56 A validés ; processus/
environnement/transport local à qualifier, aucune commande
reçue transformée en code exécuté. PBO–PA garde PZT/mTLS A03/A07 ; auxiliaire
de collecte local distinct d'un service de temps ou nouveau canal de pilotage.
Absence de collecteur disponible ne devient pas automatiquement non-admission
de capacité A10i41 autorisant relances A10i42 ; traitement selon statut/contrat
de qualité A10i49/A10i52, sans état inconnu présenté comme sûr.
A05 et A10i22 B maintenus ; API/langage/bibliothèque/modèle d'isolement exacts et
budgets mémoire/message/cycle de vie à qualifier sur Linux/Windows physiques/VM,
Docker/LXC Proxmox, aucune ressource hôte/montage/droit implicitement modifiés.

A validée pour limiter l'effet d'un lecteur bloqué sur le processus de
décision, sous maîtrise des ressources/arrêts ; appels dans consommateur non
retenus comme exécution alternative. CPU/RAM/latence à mesurer selon
profil, aucune sécurité ou performance universellement supérieure.
[Linux, wait(2)](https://man7.org/linux/man-pages/man2/wait.2.html)
et [Windows, terminaison de processus](https://learn.microsoft.com/en-us/windows/win32/procthread/terminating-a-process)
documentent suivi/terminaison ; mécanismes concrets à qualifier, aucune API
d'arrêt ou procédure exécutée ici. Aucun code, processus réel ou OpenSpec modifié.
Recette : API bloquée, timeout sans fin effective, auxiliaire encore présent,
réponse tardive/ancienne génération, PID réutilisé, arrêt ciblé échoué, budget
épuisé et refus sans nouveau worker, mesure, droit ou destruction réactivés.
A10i54 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i54

- **WHEN** un profil revendique le traitement A10i54 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--7800c6dd7c

Source : `openspec/specs/pzt/spec.md`, ligne 8385. SHA-256 du bloc : `f926f58ef0791ec0e026789ccf0ecbe1e80888e2bb888c526f47d5ab3d82c44f`.

~~~~text
### Requirement: Contrat A10i55 — Auxiliaire créé à la demande, réutilisé et arrêté après repos — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i55 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i55

Auxiliaire isolé A10i54 A, lecture par décision A10i51 A et budgets A10i52 A
maintenus. Réutilisation à demande/repos 300 secondes validée, JSON et compte
dédié A10i56/A10i57 A conservés ; aucun processus réel lancé ici.

| Choix validé | Cycle de vie | Conséquence |
| --- | --- | --- |
| A | Création à la demande, réutilisation du processus, arrêt après 300 secondes sans acquisition active | Moins de démarrages potentiels, mémoire conservée pendant l'inactivité bornée |

Maximum un auxiliaire possédé par instance de validation, une acquisition
active. Délai de repos de premier jet configurable, monotone depuis fin de la
dernière acquisition et retour à état disponible, sans vieillissement nul
après snapshot/reprise. Aucune acquisition de preuve au repos, aucun cache de
mesure entre décisions ; chaque requête lit une mesure cohérente A10i51.
Changement de profil/version/identité du propriétaire, retrait, crash ou timeout
rend l'incarnation inadmissible, arrêt contrôlé A10i54 avant remplacement.
Nouvelle requête pendant arrêt sans réanimation de l'ancienne incarnation.
Premier démarrage à la demande et communication/lecture/arrêt concernés
comptés dans A10i52 ; réutilisation sans nouveau lancement, tout lancement
effectif reste inclus dans les budgets. Indisponibilité/
arrêt non prouvé selon A10i54, aucun remplaçant ou ancienne mesure de secours.
Privilèges/env/limites hôte et frontière locale à qualifier, PBO–PA PZT/mTLS
inchangés ; aucun nouveau serveur de temps ou CLI.
A validée pour amortir des démarrages rapprochés tout en bornant le repos ;
création/arrêt systématiques par acquisition non retenus. Coûts à mesurer selon
fréquence/langage/plateforme, aucun gain RAM/CPU/latence universel.
Linux/Windows physiques/VM et Docker/LXC Proxmox qualifiés sans déploiement,
tâche de redémarrage ou OpenSpec créés ici. Recette : repos exact/au-delà,
requête pendant arrêt, changement de profil, timeout et processus encore
présent, reprise/restauration et aucune mesure/droit réactivés.
A10i55 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i55

- **WHEN** un profil revendique le traitement A10i55 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--43dd13ba2f

Source : `openspec/specs/pzt/spec.md`, ligne 8432. SHA-256 du bloc : `7f2ba97ed7e932a68430d0a48b239c38aeb5f043c2c085e6af6dd6e69a8f7bc3`.

~~~~text
### Requirement: Contrat A10i56 — Messages IPC JSON UTF-8 typés/versionnés, plafond 16 Kio — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i56 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i56

Auxiliaire A10i54 A et API/IPC structurée A10i53 A maintenus. Format propre au
canal local parent/auxiliaire, pas de format imposé à l'API OS amont. Choix
JSON 16 Kio validé, persistance et compte dédié A10i55/A10i57 A conservés ;
transport concret qualifié A10i58 A.

| Choix validé | Message de requête ou réponse | Plafond du contenu par message |
| --- | --- | --- |
| A | JSON UTF-8 typé/versionné | 16 Kio |

1 Kio = 1024 octets ; plafonds inclusifs sur octets UTF-8 exacts du contenu
JSON, indépendants des plafonds du dossier A10i39. Même plafond appliqué
séparément à chaque requête et réponse, enveloppes de transport bornées
séparément à qualifier. Aucun contenu de pièce/dossier, clé, jeton, commande
ou diagnostic brut sensible transmis au collecteur.
Schéma : type/usage/version, identifiant de requête, incarnation/profil du
lecteur et contexte nécessaires liés ; réponse temps/borne/source/qualité/âge/
mesure monotone ou erreur typée. Noms/tailles de champs/transport exacts à définir.
Longueur annoncée non fiable, octets observés comptés avant allocation/analyse
autant que possible ; message trop grand/incomplet/ambigu refusé sans troncature.
Doublons de champs, types/versions/valeurs/unités invalides, réponse de requête
ou incarnation ancienne refusés ; nombres et profondeur bornés à qualifier.
API OS binaire/documents de source mappés par adaptateur qualifié, pas de
données natives opaques implicitement tenues pour contrat PZT.

Pas de compression, batching, exécution de texte ou nouvelle signature IPC
adoptés. Authentification/protection de frontière locale selon profil à qualifier,
JSON sans confiance/permission implicites. Budgets A10i52 et preuve A10i49
appliqués jusqu'au point d'usage ; plafond large ne prolonge aucune échéance.
A validée comme premier jet compact pour métadonnées structurées, plafond
64 Kio alternatif non retenu. Mémoire/coûts à mesurer ; Linux/Windows physiques/VM et Docker/LXC
Proxmox qualifiés, PBO–PA PZT/mTLS et A05/A10i22 B conservés, aucun codec/
bibliothèque/configuration/OpenSpec installés ou modifiés ici.
Recette : taille exacte/plus un, longueur fausse, message partiel, Unicode/type/
unité invalides, ancienne incarnation et refus sans allocation non bornée,
commande ou nouvelle admission.
A10i56 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i56

- **WHEN** un profil revendique le traitement A10i56 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--c23a3eff0f

Source : `openspec/specs/pzt/spec.md`, ligne 8485. SHA-256 du bloc : `e1181cf26fbe445e095de4725d606d443154329992e472ffd1d91ede6dc3515e`.

~~~~text
### Requirement: Contrat A10i57 — Compte système dédié à la collecte, droits minimaux — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i57 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i57

Auxiliaire en lecture A10i54 A, absence de clé/SQL/réglage d'horloge et budgets
maintenus. Compte dédié non administrateur retenu, cycle de vie/JSON
A10i55/A10i56 A conservés ; aucun compte, droit ou confinement créé ici.

| Choix validé | Identité | Condition d'isolation |
| --- | --- | --- |
| A | Compte système dédié à la collecte, non administrateur, avec droits minimaux | Accès aux seules interfaces de lecture qualifiées et canal du propriétaire ; aucun secret ou droit métier hérité |

Compte/identité, groupes, accès IPC/source et exécutables explicitement
approuvés au déploiement, périmètre de collecte seulement. Aucun privilège de
réglage de temps, accès aux clés racine/backup/A12, credentials SQL, données
applicatives ou pilotage d'autres processus. Les droits de collecte insuffisants
rendent le profil inadmissible, sans ajout automatique de rôle administrateur.
Environnement/descripteurs/handles hérités réduits aux besoins déclarés,
aucune connexion SQL, clé privée, jeton ou authentifiant métier transmis.
Exécutable/profil/incarnation et propriétaire du canal contrôlés ; aucune
commande/source/permission choisie depuis message non fiable. Ressources,
confinement et annulation à qualifier, ressources validées A10i59 A ; Linux/Windows
physiques/VM, Docker/LXC
Proxmox, sans changer implicitement utilisateurs/montages/droits conteneur.
Compte dédié sans machine/hôte supplémentaire ou TPM propre automatiquement
requis. Collecte locale sans nouveau canal PBO–PA hors PZT/mTLS.
A validée pour frontière d'identité explicite et moindre privilège ;
identité du consommateur partagée non retenue.
Coûts et compatibilité à mesurer, aucun équivalent de sécurité présumé par
seul nom de compte. Procédures/paramètres/technologies à spécifier, aucune
permission système, identité applicative ou OpenSpec modifiés ici.
Recette : héritage de secret/handle, source non autorisée, droits insuffisants,
identité partagée sans confinement, tentative de réglage/SQL et refus sans
élévation, secret ou droit métier accordés.
A10i57 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i57

- **WHEN** un profil revendique le traitement A10i57 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--db6d63aaea

Source : `openspec/specs/pzt/spec.md`, ligne 8533. SHA-256 du bloc : `94d4c9d0c64875d760638d7438085f71832f22edac295eb0ad39347c10a9ee55`.

~~~~text
### Requirement: Contrat A10i58 — Transport local natif parent/auxiliaire, accès et identités contrôlés — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i58 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i58

Auxiliaire/compte dédié A10i54/A10i57 A et JSON 16 Kio A10i56 A conservés.
L'option A validée retient les mécanismes locaux natifs. Transport interne
au même domaine d'exécution qualifié, distinct du pilotage
PBO–PA qui garde PZT/mTLS A03/A07. Aucun endpoint ou connexion réels créés.

| Choix validé | Transport local | Protection |
| --- | --- | --- |
| A | Socket Unix local sous Linux, pipe nommé local sous Windows | Accès OS restreints et identité des deux extrémités/incarnations vérifiée, accès distant interdit |

Endpoint possédé dans emplacement/namespace approuvés, permissions/ACL
explicites pour seul parent et compte de collecte, vérification des identités
OS et de l'incarnation avant accepter messages. Nom ou PID seuls insuffisants,
substitution d'endpoint et anciens descripteurs refusés ; mécanismes exacts à
qualifier. Socket Linux de chemin protégé retenu, aucun namespace abstrait
déduit sûr par permissions de fichier. Windows refuse connexions distantes
explicitement et ne s'appuie pas sur ACL par défaut ; impersonation et héritage
de handles à maîtriser, pas de droit administrateur obtenu via le pipe.
Loopback TCP/TLS/mTLS B non retenu comme transport alternatif ; aucune
nouvelle PKI de transport ou repli réseau implicites.
Commun : trames/messages bornés, corrélation/version/génération et budgets
A10i52 respectés, rejet du pair non attendu. Même machine physique sans même
frontière d'exécution présumée pour VM/conteneurs ; aucune exposition inter-hôtes,
montage ou canal non qualifiés comme fallback. Cadre du transport/noms/API et
coûts à mesurer sur toutes plateformes, aucune sécurité absolue contre hôte
compromis ou performance universelle. A validée pour mécanismes locaux sans
gestion de certificats de transport
supplémentaires. Cadre des messages A10i61 A et politique de schéma A10i62 A
validés le 8 octobre 2026 ; leur qualification reste requise. Aucun système/OpenSpec modifié ici.
[Linux, unix(7)](https://man7.org/linux/man-pages/man7/unix.7.html) et
[Microsoft, sécurité des pipes](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-security-and-access-rights)
documentent accès/identités ; [CreateNamedPipe](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createnamedpipea)
le contrôle des clients distants, qualification requise sans API adoptée.
Recette : pair incorrect, endpoint remplacé, accès distant, ancienne incarnation,
message partiel, permissions incorrectes et aucun droit/réglage d'horloge accordés.
A10i58 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i58

- **WHEN** un profil revendique le traitement A10i58 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--91a8063175

Source : `openspec/specs/pzt/spec.md`, ligne 8585. SHA-256 du bloc : `2b972f651afcbd9888aed1dce391287ca6b54d30e9ca8fb8c6fe14389e0ff767`.

~~~~text
### Requirement: Contrat A10i59 — Plafonds auxiliaire de premier jet 64 Mio et 50 % d’un cœur — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i59 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i59

Un auxiliaire/une acquisition par instance A10i54 A, repos borné A10i55 A,
messages 16 Kio et délais A10i52 conservés. Budgets configurables de premier
jet validés, sans consommation de runtime observée ni règle système appliquée.
Les plafonds 64 Mio/50 % sont retenus ; 128 Mio/100 % B non adoptés.

| Choix validé | Plafond mémoire par auxiliaire | Plafond CPU |
| --- | --- | --- |
| A | 64 Mio | 50 % d'un cœur |

1 Mio = 1 048 576 octets. Périmètre de mémoire chargée/engagée, bibliothèques,
buffers et descendants autorisés, métriques et mécanismes de limite à qualifier
par OS ; espace d'adressage virtuel ou simple working set sans plafond réel
présumé équivalents. CPU = budget en temps CPU par période qualifiée exprimé
par rapport à un cœur, pas pourcentage arbitraire de tous cœurs d'hôte.
Période/rafales/mesure et applicabilité VM/conteneur à préciser, aucune latence
250 ms réellement garantie par quota ni mémoire entière de l'hôte plafonnée.
Parent/services d'infrastructure et quotas agrégés d'hôte/autorité à budgéter
séparément ; réplication sans ressources infinies ou nouveaux workers admis.
Limites qualifiées avant activation, configurées par rôle autorisé, aucune
modification implicite des droits/montages Docker/LXC, cgroups ou hôte.
Dépassement/incohérence provoque résultat inadmissible et diagnostic, arrêt/
remplacement selon A10i54, aucune hausse automatique, cache ou mesure de secours.
Budget trop bas pour runtime légitime : qualification/revision explicite,
pas de consommation conforme présumée par taille JSON 16 Kio seule.

A validée comme premier jet sobre ; adaptation par configuration/profil
explicitement autorisés et qualifiés, sans hausse automatique sur panne.
Valeurs sans données de mesure les validant à ce stade,
toutes plateformes Linux/Windows physiques/VM, Docker/LXC Proxmox à qualifier.
[Linux, cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html) et
[Windows, Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
décrivent des mécanismes de ressources, sans technologie choisie ici ou
équivalence de métriques/propriétés présumée. Compte A10i57, transport A10i58,
audit/diagnostics A10i60 indépendants ; aucun processus réel ou OpenSpec modifié.
Recette : mémoire/CPU atteints, mécanisme indisponible, quota de conteneur plus
strict, arrêt non prouvé, parent non ciblé et refus sans élévation de budget.
A10i59 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i59

- **WHEN** un profil revendique le traitement A10i59 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--cedc4ee89b

Source : `openspec/specs/pzt/spec.md`, ligne 8639. SHA-256 du bloc : `3c6b566d019f37d5c958d1d4b10d3ab2ba8c18655de337ddd83d5c971b3da762`.

~~~~text
### Requirement: Contrat A10i60 — Journalisation technique agrégée, transitions et erreurs — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i60 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i60

Observabilité et audit OpenSpec restent applicables, flux distincts ; choix
du détail technique par acquisition, indépendant du transport et des quotas.
L’option A validée privilégie métriques agrégées et transitions/erreurs.
Rétentions techniques A10i82–A10i84 A validées le 9 octobre 2026 : logs 7 jours, métriques 30 jours, traces 24 h.
Aucun système de logs créé ici.

| Choix validé | Détail technique | Conservation des obligations d'audit |
| --- | --- | --- |
| A | Métriques agrégées, traces selon politique, journaux de transitions/erreurs | Audit métier/configuration/sécurité requis persistant et distinct, sans échantillonnage déduit |

État de démarrage/vivacité/disponibilité/diagnostic distincts, compteurs de
succès/échecs/timeout, durée et qualité minimales selon profil ; transitions/
erreurs corrélées, pas de copie du message/dossier ni succès détaillé à chaque
lecture exigé par cette seule politique. Compatibilité OpenTelemetry/W3C selon
OpenSpec, schémas/champs/limites et traces à qualifier, aucune observabilité
obligatoire supprimée sous prétexte d'agrégation.
Événement technique systématique par acquisition B non retenu comme
obligation supplémentaire ; diagnostic minimal et traces selon politique
conservés, aucune réponse brute, clé, token ou information sensible loggés.

Commun : audit fonctionnel distinct et persistant pour événements requis, y
compris autorisations sensibles, configuration, opérations destructives et
activités d'administration ; preuve de clôture A10i35 sans reconstruction depuis
logs. Journalisation technique indisponible sans opération métier autrement
conforme bloquée par ce seul motif ; audit obligatoire indisponible ou preuve
de temps manquante selon exigences respectives, pas d'exemption A05.
Minimisation/pseudonymisation, accès et rétentions logs/métriques/traces/audit
séparés, quotas/cardinalité et traitement de répétitions à qualifier.
A validée pour limiter volume technique des succès ; signal requis ou audit
obligatoire sans perte sous prétexte de réduction de volumétrie. Choix Pixs,
pas de backend/outil ou
durée adoptés, aucune nouvelle collecte de clôture sur PA ordinaire imposée.
Toutes plateformes à qualifier ; recettes : erreur répétée, succès sans payload
loggé, audit requis absent, télémétrie technique seule absente, accès inter-périmètre
et absence de secret ou preuve/audit reconstitués implicitement.
A10i60 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i60

- **WHEN** un profil revendique le traitement A10i60 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--adaf0a5bc3

Source : `openspec/specs/pzt/spec.md`, ligne 8692. SHA-256 du bloc : `bfdb49a278ba163e91f36e1d64ece0df48bda9b57eba86e84bc8947056692ead`.

~~~~text
### Requirement: Contrat A10i61 — Messages IPC préfixés par une longueur sur 4 octets — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i61 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i61

JSON UTF-8 16 Kio A10i56 A, transport local natif A10i58 A et schéma fermé
A10i62 A conservés. Cadre de requête/réponse A validé, reprise A10i63 indépendante.

| Choix validé | Cadre applicatif | Conséquence |
| --- | --- | --- |
| A | Préfixe de longueur non signé sur 4 octets en ordre réseau, puis JSON exact | Longueur contrôlée avant lecture du contenu, surcoût fixe de 4 octets |

Longueur du seul JSON entre 1 et 16 384 octets inclus, trame au plus
16 388 octets, sans compression ou extension d'en-tête. En-tête complet puis
validation de longueur avant allocation bornée ; entier sur 32 bits sans
permission d'allouer autant. Un seul objet JSON, pas de valeurs concaténées.
Délimitation par JSON monoligne/LF B non retenue comme cadre alternatif.
Fragments de lecture/écriture/UTF-8 gérés sans frontière de message déduite
d'un appel système. Profil de flux stream Linux et byte Windows retenu pour
le cadre commun ; modes/APIs, buffers et fin effective d'I/O à qualifier.
Une acquisition active, réponse liée à requête/incarnation et état attendu ;
pas de multiplexage, batching, file de requêtes ou exécution d'octets reçus.
Trame partielle, taille invalide, contenu supplémentaire/spontané, fin de canal
ou échéance : résultat refusé et canal invalidé, nettoyage/arrêt A10i54.
Aucun balayage du flux pour retrouver une trame après erreur, aucun résultat
ancien ou repli de cadre par autodétection. A10i52 englobe transport/analyse et
attente sans nouvelle échéance à chaque fragment. Authentification A10i58
indépendante du cadre, aucun en-tête ne prouve identité ou qualité du temps.
A validée pour contrôle précoce et cadre commun, sans supériorité universelle
de sécurité/performance. Coûts à mesurer, mécanismes exacts à qualifier.
[Linux, unix(7)](https://man7.org/linux/man-pages/man7/unix.7.html) et
[Microsoft, modes des pipes](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-type-read-and-wait-modes)
distinguent modes de flux/messages ; cadrage choisi par Pixs, aucun mécanisme
réel ou OpenSpec modifié. Qualification Linux/Windows physiques/VM, Docker/LXC.
Recette : en-tête/UTF-8 fragmentés, tailles limites/plus un, longueur fausse,
JSON concaténé, octets spontanés, fin de flux et timeout sans allocation,
attente ou reprise non bornées.
A10i61 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i61

- **WHEN** un profil revendique le traitement A10i61 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--957066ab0a

Source : `openspec/specs/pzt/spec.md`, ligne 8742. SHA-256 du bloc : `27150d62ea3f8dc82d483babefebf54bca2b990f91d0fcafb3a3a1b58bffcbe9`.

~~~~text
### Requirement: Contrat A10i62 — Schéma JSON IPC fermé par version, champs inconnus refusés — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i62 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i62

Contrat typé/versionné A10i56 A, compte/identités A10i57/A10i58 A, quotas et
audit conservés. Évolution du contenu indépendante du cadre A10i61 A ; forme
des numéros de version et bibliothèque non choisies.

| Choix validé | Politique des champs | Conséquence |
| --- | --- | --- |
| A | Schéma fermé par version admise, tout champ inconnu refusé | Contrat strict, évolution explicite du schéma/version et déploiement compatible |

Chaque clé, même imbriquée, correspond exactement à un champ déclaré pour
le type/version admis. Champ inconnu, requis absent, type/unité invalide ou
doublon après décodage des noms refusés, sans ignorance silencieuse ou défaut
de confiance. Nouveau contenu admis après schéma versionné qualifié et
déploiement autorisé de composants compatibles ; aucune négociation à la baisse
ou conversion entre versions automatiquement depuis une réponse.
Zone d'extensions facultatives B non retenue comme contrat alternatif.
Un objet racine, JSON strict UTF-8 sans BOM émis/accepté par ce profil,
Unicode invalide, NaN/Infinity, commentaires ou données après objet refusés.
Noms décodés comparés sans normalisation ambiguë. Précision/plages/unités
explicites par champ, aucune conversion silencieuse en flottant/chaîne/booléen
ou perte de précision acceptée. Représentation des grands entiers A10i64 et
plafonds de complexité A10i65 validés le 8 octobre 2026.
Syntaxe correcte sans origine admissible ou mesure exacte présumées ;
A10i49/A10i52 toujours requis, aucun champ de message n'accorde de permission.
A validée pour contrat restreint sans ambiguïtés.
[RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) documente
JSON/doublons/représentations ; politique d'évolution choisie par Pixs,
pas prescrite par la RFC. Plateformes à qualifier, aucun codec, provider,
configuration ou OpenSpec modifié. Recette : champs inconnus imbriqués,
noms équivalents après décodage, version non admise, extension critique,
précision perdue et Unicode invalide sans adaptation permissive.
A10i62 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i62

- **WHEN** un profil revendique le traitement A10i62 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--79c4edcf65

Source : `openspec/specs/pzt/spec.md`, ligne 8790. SHA-256 du bloc : `7a24919d35d22607b91b1bd4529ec26a49d9523a2c5fdafa1bbfdc730e9fe89a`.

~~~~text
### Requirement: Contrat A10i63 — Recréation technique à la demande, 3 tentatives sur 600 secondes — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i63 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i63

Création à demande/repos A10i55 A et arrêt effectivement prouvé A10i54 A
conservés. Après panne technique récupérable, option A validée ; aucune relance
d'opération métier, sauvegarde ou acte destructif autorisée par cet arbitrage.

| Choix validé | Reprise technique | Conséquence |
| --- | --- | --- |
| A | Recréation sur acquisition autorisée, au plus 3 tentatives sur 600 secondes, puis blocage à réarmer explicitement | Reprise bornée, aucun redémarrage périodique ou de fond |

Mandat courant couvre la reprise technique du profil ; tentative réelle de
remplacement après panne réservée/comptée avant lancement, même lancement
échoué/incertain. Premier remplacement inclus dans les 3 tentatives, fenêtre
glissante de 600 s par instance logique, profil/provider courant lié au compteur.
Plafond épuisé avant tentative suivante ou troisième tentative échouée :
collecte indisponible et circuit bloqué ; réarmement explicite sous autorisation
courante après diagnostic et preuve d'absence d'ancien auxiliaire. Pas de timer
réarmant un circuit bloqué ni changement opportuniste d'identité/profil/processus
remettant à zéro le compteur. Hors blocage, seules réservations sorties d'une
fenêtre dont l'écoulement monotone est qualifié cessent de compter ; compteur/
durée incertains après reprise/restauration bloquent la recréation automatique
jusqu'à réconciliation autorisée.
Réarmement systématique dès première panne B non retenu comme politique
alternative. Création initiale et retour après repos normal A10i55 sans
réarmement pour seul motif de repos, contrôles courants toujours nécessaires.
Acquisition autorisée nécessaire, jamais redémarrage de fond ou mesure au repos ;
un seul processus possédé, arrêt prouvé avant remplacement, nouvelle incarnation
et contrôles courants compte/endpoint/quotas/temps. Panne de sécurité, pair
inattendu, profil non qualifié, privilèges insuffisants ou compromission suspectée
sans reprise automatique : refus et traitement autorisé distincts.
A10i52 250 ms/2 acquisitions/1 s global conservé, lancement/I/O comptés, aucune
nouvelle lecture après nombre/délai épuisés. Disponibilité ultérieure sans nouveau
cycle métier ouvert ou remise à zéro de D, tentative A10i47 ou fenêtre A10i48 ;
panne du collecteur sans non-admission de capacité A10i41/A10i42 présumée.
Logs A10i60 et audit requis distincts, aucun effacement masquant les échecs.
A validée pour disponibilité sous contrôle ; 3 tentatives/600 s constituent
un premier jet configurable à qualifier, aucune reprise garantie dans les délais.
Support local durable de l'état A10i66 A validé le 8 octobre 2026.
Protection du compteur et réarmement à qualifier sur toutes plateformes,
aucun worker, timer, commande système ou OpenSpec créé ici. Recette : lancement
échoué, fin non prouvée, trois tentatives, fenêtre incertaine, restauration,
budget de lecture épuisé, panne de sécurité et aucune admission/durée/droit
automatiquement réactivés.
A10i63 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i63

- **WHEN** un profil revendique le traitement A10i63 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--2c055f8404

Source : `openspec/specs/pzt/spec.md`, ligne 8849. SHA-256 du bloc : `92ba88da37efd13dd97044896704bacde3b0fd6d6337c39510269dbe4b3869be`.

~~~~text
### Requirement: Contrat A10i64 — Grands entiers IPC en chaînes décimales canoniques — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i64 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i64

Contrat JSON UTF-8 fermé A10i56/A10i62 A conservé. Représentation A validée
des champs explicitement déclarés int64/uint64 du contrat de collecte, sans
changer l'échelle temporelle, les unités, l'origine ni la borne d'erreur A10i49.

| Choix validé | Représentation des champs int64/uint64 | Conséquence |
| --- | --- | --- |
| A | Chaînes décimales canoniques | Transport exact, validation lexicale/plage requise |

ASCII décimal, zéro représenté par « 0 », signe moins seulement pour
int64 négatif ; aucun signe plus, espace, zéro initial, « -0 », exposant,
fraction ou chiffre Unicode. Au plus 20 caractères après décodage, plage
int64 [-9223372036854775808, 9223372036854775807] ou uint64
[0, 18446744073709551615] selon champ ; lexical et plage contrôlés avant usage.
Types obligatoires : nombre JSON à la place de cette chaîne refusé, pas de
coercition automatique. Les chaînes ordinaires/IDs restent leurs propres types ;
aucun identifiant opaque transformé en entier ni champ numérique arbitrairement
retypé. Petits entiers, booléens et autres types suivent leur schéma explicite.
Nombres JSON B non retenus pour les champs int64/uint64 de ce contrat.
Commun : unités/plages métier, origine/domaine monotone et cohérence source
déclarés par champ ; la représentation ne prouve pas qualité/fraîcheur ni
précision réelle à la nanoseconde. Aucune nouvelle unité de temps imposée
ou règle d'arrondi qui rétrécit U, rajeunit l'âge ou étend D.
Toute conversion de source qualifiée refuse débordement/perte d'information,
ou produit une borne conservative explicitement qualifiée par le profil.
A validée pour portabilité des grands entiers. Choix Pixs ; [RFC 8259, nombres](https://www.rfc-editor.org/rfc/rfc8259#section-6)
documente les enjeux de précision, sans prescrire ces chaînes ou un runtime.
Messages 16 Kio/cadre A10i61, schéma fermé, budgets et audit inchangés.
APIs/langage/formes exactes du schéma à qualifier sur toutes plateformes,
aucun codec ou OpenSpec modifié. Recette : bornes 64 bits, plus un,
2 puissance 53 plus un, zéros/signes, mauvais type et refus sans arrondi.
A10i64 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i64

- **WHEN** un profil revendique le traitement A10i64 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--fd54821153

Source : `openspec/specs/pzt/spec.md`, ligne 8897. SHA-256 du bloc : `5d6de360293d9dc0e04badbb6aa92154da4af588e394dd404b38185eb25cf0a3`.

~~~~text
### Requirement: Contrat A10i65 — Complexité JSON IPC plafonnée à 8 niveaux, 32 membres et 32 éléments — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i65 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i65

Plafond 16 Kio par contenu A10i56 A, trame A10i61 A et schéma fermé A10i62 A
conservés. Plafonds A 8/32/32 validés comme premier jet configurable, distinct du dossier
de clôture A10i39 qui conserve sa profondeur 16 et ses autres limites.

| Choix validé | Profondeur maximale | Membres par objet | Éléments par tableau |
| --- | --- | --- | --- |
| A | 8 | 32 | 32 |

Profondeur : objet racine de niveau 1, chaque objet/tableau imbriqué ajoute
1, valeurs primitives sans niveau supplémentaire. Plafonds inclusifs, cumulés
avec 16 Kio, requis du schéma et budgets de temps/mémoire ; quota syntaxique
n'autorise aucun champ supplémentaire, tableau ou type absent du schéma.
Membres comptés sur entrée avant déduplication, doublons toujours refusés ;
éléments comptés par tableau, y compris objet/tableau/vide/null si permis.
Réception et analyse bornées : dépassement détecté au plus tôt par mécanisme
qualifié, pas d'arbre arbitrairement construit puis réduit ou tronqué
silencieusement. Un résultat partiel ne devient pas preuve de temps admissible.
Plafonds de premier jet configurables sous version/profil autorisés et qualifiés,
sans augmentation automatique ou bascule A/B pour faire accepter un message.
Taille de chaîne, nombre total de tokens, coût de décodage et amplification
mémoire restent bornés/qualifiés dans les budgets existants ; ces trois
plafonds ne démontrent pas seuls consommation CPU/RAM ou disponibilité.
A validée pour métadonnées de collecte restreintes et moins de profondeur
admissible ; plafonds B 16/64/64 non retenus. Choix Pixs, pas
de valeur imposée par [RFC 8259, parseurs](https://www.rfc-editor.org/rfc/rfc8259#section-9),
qui permet des limites de taille/profondeur/représentation.
Toutes plateformes qualifiées avant activation ; aucun parseur/configuration
ou OpenSpec modifiés. Recette : profondeur racine/limite/plus un, tableaux
imbriqués, membres/éléments limites, doublons et contenu de 16 Kio avec
complexité excessive, refus sans sortie partielle ou délai prolongé.
A10i65 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i65

- **WHEN** un profil revendique le traitement A10i65 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

