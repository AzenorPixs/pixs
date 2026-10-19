# Références normatives — Z14

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 6604 | [Contrat A10i29 — Témoin hors ligne indépendant de progression — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L6604) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 6666 | [Contrat A10i30 — Journal du témoin lié à un ancrage matériel monotone — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L6666) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 6729 | [Contrat A10i31 — Nouvelle protection après perte ou remplacement de l'ancrage du témoin — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L6729) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 6795 | [Contrat A10i32 — Transition par étapes vers la nouvelle protection des sauvegardes — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L6795) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 6866 | [Contrat A10i33 — Assainissement des anciens éléments sans conservation volontaire — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L6866) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 6936 | [Contrat A10i34 — Méthode d’assainissement qualifiée par profil — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L6936) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--e09246d68b

Source : `openspec/specs/pzt/spec.md`, ligne 6604. SHA-256 du bloc : `5ed4a938db19b9773497a5f46a3dcda2eb5d6684f5eb957726bc0a06c0e5cb59`.

~~~~text
### Requirement: Contrat A10i29 — Témoin hors ligne indépendant de progression — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i29 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i29

Témoin hors ligne indépendant de la station racine retenu pour prouver la
progression A10i28 après restauration, changement d'outil ou emploi d'un moyen
A10i26. Allocateur logique unique, préfixe 32 bits/compteur 64 bits et réserve
avant chiffrement conservés. Protection journal/ancrage matériel validée en A10i30, backend,
protocole et reprise à qualifier ; aucune disponibilité garantie.

| Choix validé | Référence de progression | Condition principale |
| --- | --- | --- |
| A | Témoin hors ligne indépendant de la station racine | Dernière réservation conservée hors des domaines de restauration/clonage de la station, progression exclusive qualifiée |

Témoin logique unique, sans clé privée racine ni clé de protection des sauvegardes.
Il conserve références de clé/contexte et plus haute valeur réservée, engagée
durablement avant chiffrement. Échanges de cérémonie hors ligne, authentifiés,
liés à une requête fraîche et à la clé/contexte ; fichier ou reçu ancien isolé
insuffisant. Perte d'accusé après engagement consomme la réservation ; nouvelle
tentative réconcilie l'état sans réattribuer le nonce. Profil de stockage et
contrôle d'accès propres au témoin, indépendants des sauvegardes/snapshots/
clones de la station racine. Append-only, chaînage ou signature seuls ne prouvent
pas qu'un état est le dernier. Retour arrière du témoin lui-même, duplication
active et réemploi de preuve couverts par qualification avant activation.
Témoin éventuellement matériel, backend concret à arbitrer. Ni PostgreSQL
restaurable ni inventaire PBO ne vaut automatiquement témoin admissible ;
aucun témoin online PBO/PA imposé. Dispositif monotone directement substitué
au témoin indépendant non retenu comme architecture alternative automatique.

Seule une réservation de progression prouvée permet un nouveau chiffrement,
sous habilitation/mandat A10i22 B et contrôles courants A05/A10i21/A10i27.
Témoin sans rôle d'autorité métier, émetteur CA ou second signataire racine ;
Django/A07/A12 conserve les effets PZT. Une personne habilitée peut effectuer
la cérémonie ; deux moyens A10i26 ne constituent pas deux témoins actifs.
Perte/inaccessibilité/état incertain bloque les nouveaux chiffrements, sans
empêcher par elle-même la récupération des objets existants sous A10i21/A10i27,
ni déclencher rotation/révocation ou restauration d'anciens droits. Reprise,
réfection/transfert de l'autorité de progression, limites/cadence d'essais et
format des preuves à spécifier ; aucune réinitialisation automatique.
A validée pour permettre un backend adapté sous propriétés qualifiées.
Coûts/ressources de cérémonie à mesurer, aucun classement universel ;
Linux/Windows physiques/VM, Docker/LXC Proxmox qualifiés sans changer
implicitement privilèges, montages ou accès au matériel des PA/PBO.
[NIST SP 800-38D, sections 8 et 9](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf)
pour unicité/reprise des IV ; architecture Pixs validée sans prescription NIST
ou conformité déduite. Recette : ancien état signé, restauration station/témoin,
témoin cloné, preuve rejouée, concurrence, crash/perte d'accusé et état inaccessible,
récupération existante sans nouveau chiffrement ou droit réactivé.
A10i29 A validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i29

- **WHEN** un profil revendique le traitement A10i29 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--115fd84152

Source : `openspec/specs/pzt/spec.md`, ligne 6666. SHA-256 du bloc : `fa9d7766f7988290035aa61241fb06cb6d15b2dbd1570811c38439fabcc8c617`.

~~~~text
### Requirement: Contrat A10i30 — Journal du témoin lié à un ancrage matériel monotone — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i30 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i30

Témoin indépendant A10i29 maintenu ; journal lié à ancrage matériel monotone
qualifié retenu contre retour arrière. Protection du témoin distincte du
déploiement courant des PA et de la protection finale des moyens A10i26.
Un seul témoin logique actif par clé/contexte ; matériel/provider concret,
liaison et protocole à qualifier, reprise A validée en A10i31.

| Choix validé | Protection du témoin | Condition principale |
| --- | --- | --- |
| A | Journal lié à un ancrage matériel monotone qualifié | Liaison protégée entre état du journal, clé/contexte et progression matérielle, hors des snapshots restaurables |

Journal durable/intègre et ancrage matériel de progression indépendants des
états restaurables. Liaison protégée des références de clé, contexte, identité
du témoin, génération d'ancrage, état du journal et valeur réservée ; compteur
matériel seul non associé au journal insuffisant. Réservation exclusive,
progression matérielle et journal réconciliés avant chiffrement ; interruption
ou engagement incertain consomme la valeur sans retour/réattribution. Protocole
ordonné à qualifier pour tous points de crash, preuve actuelle liée à la requête
de cérémonie, anciens reçus inadmissibles. Reset, changement d'identité/dispositif,
disparition de l'ancrage ou incohérence bloque les nouveaux chiffrements sous
la clé concernée, reprise seulement sous procédure explicitement autorisée.
Matériel concret, capacités, endurance, limites, protection administrative et
mécanisme de liaison à arbitrer ; étiquette TPM/HSM/vTPM sans preuve des
propriétés insuffisante. Si le témoin comporte une VM ou un conteneur, l'ancrage
n'est pas restauré/cloné avec cet environnement ; dépendances et accès
explicitement qualifiés, sans pass-through/montage/privilège implicitement autorisés.
Stockage immuable/garde seuls non retenus comme repli de protection du témoin.

A10i28/A10i29, contrôle individuel A10i22 B et clé commune A10i25 conservés,
sans séquence réinitialisée sous la même clé. Journal/progression sans clé
privée racine ou clé de protection ; éventuels secrets d'authentification propres
au témoin protégés, hors journaux/artefacts/PBO/PA. Protection, algorithmes et
format d'authentification du témoin à préciser séparément. Perte/inaccessibilité
bloque les nouveaux chiffrements par ce motif ; récupération d'objets existants
soumise à A10i21/A10i27, A05 prioritaire. Aucun dispositif neuf ne remet le
compteur à zéro sous la même clé. Reprise/remplacement/transfert de l'autorité
de progression selon A10i31 A validé, sans activation implicite.
A validée pour une preuve technique de progression, sous qualification de la
liaison journal/ancrage et des interruptions. Ressources/coûts/délais à mesurer,
aucune supériorité universelle ni matériel exigé sur les PA ordinaires.
Architecture hors ligne à qualifier avec stations Linux/Windows physiques/VM,
Docker/LXC Proxmox ; modèle concret et intégration restent ouverts.
[NIST SP 800-38D, sections 8 et 9](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf)
pour continuité des IV, sans matériel ou architecture du témoin prescrits par
cette référence. Recette : vieux journal authentique, ancrage avancé/journal
ancien, crash à chaque étape, reset/remplacement/clonage, preuve rejouée et
absence de nonce ou droit réactivé. A10i30 A validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i30

- **WHEN** un profil revendique le traitement A10i30 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--8f11faf34e

Source : `openspec/specs/pzt/spec.md`, ligne 6729. SHA-256 du bloc : `deeec062c7f0b8764d0cb5b3fa33d80cbea185a3891b26d5fee1eb544d041f2f`.

~~~~text
### Requirement: Contrat A10i31 — Nouvelle protection après perte ou remplacement de l'ancrage du témoin — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i31 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i31

Périmètre : perte définitive, réinitialisation ou remplacement déclaré de
l'ancrage A10i30. Indisponibilité transitoire/redémarrage avec état intact sans
remplacement ne déclenche pas cette procédure ; reprise normale sous preuves
A10i28–A10i30. Mandat propre A10i22 B, contrôles A05/A10i21/A10i27 et qualification
conservés. Clé de protection des sauvegardes distincte de clé de signature racine.

| Choix validé | Reprise | Condition principale |
| --- | --- | --- |
| A | Nouvelle clé de protection aléatoire et nouvelle génération de témoin/ancrage | Reprotection autorisée des deux sauvegardes, ancienne clé interdite aux nouveaux chiffrements |

Nouvelle clé AES de 256 bits indépendante selon A10i24, dédiée au même
périmètre/racine A10i25 ; nouvelle génération de protection et témoin/ancrage
qualifiés. Deux sauvegardes sous nouvelle clé commune, AES-256-GCM/AAD A10i27,
et deux moyens complets de récupération A10i26 qualifiés. Nouvelle séquence
A10i28 liée à la nouvelle clé ; aucune remise à zéro sous l'ancienne clé ni
ancienne réservation réattribuée. Ancienne protection interdite aux nouveaux
chiffrements ; références/générations courantes et exclusion des anciens
mandats/outils contrôlées, matériel perdu sans destruction présumée.
Conservation de clé avec transfert de progression non retenue pour ce périmètre,
aucun repli automatique. Nouvelle clé/témoin ne sont pas créés ou activés par
simple détection technique de panne, hors procédure et mandat de reprise.

Anciennes sauvegardes déprotégées pour cette cérémonie seulement si admissibles
et récupérables ; source principale racine protégée également possible selon
profil/mandat. Sans source privée racine admissible et moyens nécessaires,
reprotection impossible, pas de racine reconstruite ou provider non exportable
contourné. Suspicion/compromission selon A05/A10i21, re-chiffrement sans confiance
rétablie pour une racine compromise. Même clé de signature racine conservée
seulement si admissible, sans signature CA ou signataire actif supplémentaire
accordés ; dates/âge/ancrages/droits inchangés. Transition, preuves de récupération,
transition et engagement validés A10i32, retrait sans conservation validé A10i33 ; quantités
A10i23/A10i26 décrivent la cible, régime mixte sans autorisation implicite.

Django/A07/A12 gouverne effets PZT, références et mandats courants prouvés ;
une personne habilitée suffit par opération A10i22 B. Aucun secret ajouté aux
journaux/PostgreSQL/PBO/PA ou artefacts. Déchiffrement d'un objet existant sans
dépendance automatique au témoin perdu, sous A10i21/A10i27 ; opération distincte
du droit de signer. A validée pour éviter la reprise de séquence sous même clé
après perte/remplacement ; reprotection et nouveaux moyens à qualifier/mesurer,
sans classement universel des performances ni charge courante PA/PBO ajoutée.
Linux/Windows physiques/VM et Docker/LXC Proxmox qualifiés, protection finale
des moyens et modèle matériel ouverts. Aucune opération réelle de reprise ici.
[NIST SP 800-38D, section 9.1](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf)
pour blocage si génération des IV non récupérable sûrement jusqu'à clé fraîche ;
politique Pixs validée sans obligation NIST de rotation à tout remplacement ni
conformité déclarée. Recette : perte sans historique, remplacement déclaré,
ancienne clé interdite au nouveau chiffrement, nouvelle clé indépendante,
source admissible/altérée/absente, compromission et transition interrompue,
aucun nonce, âge, ancrage ou droit réactivé. A10i31 A validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i31

- **WHEN** un profil revendique le traitement A10i31 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--58fdd8af1e

Source : `openspec/specs/pzt/spec.md`, ligne 6795. SHA-256 du bloc : `80128d38dbc6213e1a15722f2a7404ce88cbc2f966fcb19eaecddc2e03137b79`.

~~~~text
### Requirement: Contrat A10i32 — Transition par étapes vers la nouvelle protection des sauvegardes — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i32 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i32

Application de A10i31 A sous mandat de reprise, même racine admissible,
nouvelle clé commune et nouveau témoin/ancrage A10i28–A10i30. Cible : deux
sauvegardes racine A10i23 et deux moyens complets A10i26 ; contrôle individuel
A10i22 B conservé. Nouveau chiffrement sous ancienne clé déjà interdit.
Déroulement par étapes reprenables retenu ; protocole/provider, durées/budgets,
engagement et preuves à qualifier, retrait sans conservation validé A10i33.

| Choix validé | Déroulement | Gestion d'une interruption de préparation |
| --- | --- | --- |
| A | Préparer, vérifier, engager la nouvelle protection, puis retirer les anciens éléments | Reprise par étapes idempotentes, preuves et habilitations courantes revalidées |

Étapes persistées par références/états/preuves sans secret. Préparation hors
ligne de la nouvelle clé, de ses deux moyens et du témoin/ancrage qualifié,
puis création des deux objets sous réservations A10i28–A10i30. Usage de préparation
strictement mandaté, candidat distinct de protection courante ; témoins/générations
sans autorité concurrente sur la même clé. Deux nouvelles copies identifiées,
intègres, domaine/racine/générations/AAD vérifiés ; chaque moyen A10i26 essayé
sans l'autre dans le périmètre racine qualifié. Preuve de récupération de la
même clé racine admissible, sans export en clair, signature CA ou droits accordés.
Objets scellés déjà prouvés repris seulement après revalidation courante ;
nouveau scellement consomme une nouvelle réservation, jamais celle d'une
tentative précédente ou incertaine. Identifiant d'opération, préconditions/version
et états engagés réconciliés pour éviter doubles effets. Reprise après interruption
sous mandat encore admissible ou nouvelle autorisation explicitement liée,
jamais par restauration de l'ancien mandat ou compteur. Cérémonie unique avec
abandon systématique de préparation non retenue comme mode de transition.

Engagement seulement après preuve courante des deux copies, des deux moyens
complets et de la progression du témoin ; génération de protection courante
unique/versionnée, gouvernance Django/A07/A12 des effets PZT conservée. État
d'engagement incertain réconcilié avant abandon ou nouvelle tentative ; absence
d'accusé sans absence d'engagement présumée. Retrait post-engagement suivi
jusqu'à preuve même si la cérémonie est interrompue. PG seul ne prouve ni
contenu des supports hors ligne ni effacement d'un secret.
Stockage temporaire des anciennes et nouvelles copies/moyens identifié et
mandaté, rôles source/candidat/courant/retiré explicites ; aucune seconde
protection courante, copie découverte automatiquement admise ou retour ancien
implicite. Anciennes sauvegardes seulement sources admissibles pour reprise
avant engagement, sans droit de chiffrer/signer ; validités/A05 prioritaires.
Après engagement, anciens éléments hors profil courant ; assainissement sans
conservation volontaire validé A10i33, sans destruction physique présumée
des supports perdus. Dates/âge/racine/ancrages/droits inchangés. Délais/budgets
finis, format/preuves, détail d'engagement et élimination des secrets à qualifier
avant activation. Incident/révocation bloque la suite et peut imposer A05/A10i21.
A validée pour reprise contrôlée sans refaire les étapes déjà prouvées, avec
revalidation et état durable ; ressources/coûts à mesurer, aucune disponibilité
absolue ou supériorité universelle. Périmètres Linux/Windows physiques/VM,
Docker/LXC Proxmox qualifiés ; aucune clé/secret dans journaux/PostgreSQL/
artefacts/PBO/PA ou charge courante de reprotection imposée aux PA, aucun
matériel/privilège implicitement modifiés. Workflow Pixs validé sans conformité
cryptographique ou prescription externe déclarée. Recette : copie/moyen manquant,
essai individuel échoué, interruption à chaque étape, candidat altéré, nonce
consommé, engagement incertain, ancien mandat/état rejoué et retrait incomplet,
absence de secret/droit réactivé. A10i32 A validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i32

- **WHEN** un profil revendique le traitement A10i32 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--69a59d97aa

Source : `openspec/specs/pzt/spec.md`, ligne 6866. SHA-256 du bloc : `4824062c52ffa8e183ae4f69e39df669b4bf9ab1f9fb90d24c0031b8d065af36`.

~~~~text
### Requirement: Contrat A10i33 — Assainissement des anciens éléments sans conservation volontaire — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i33 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i33

Après engagement vérifié A10i32 de la nouvelle protection A10i31. Deux copies
et deux moyens courants qualifiés A10i23/A10i26 conservés. Cible : anciens
objets de sauvegarde, ancienne clé commune et moyens de récupération associés ;
clé racine conservée et nouveau profil exclus des cibles de destruction.
Retrait logique acquis, assainissement sans conservation volontaire validé ;
méthode par support/provider validée A10i34, aucune opération réelle ici.

| Choix validé | Traitement après engagement vérifié | Conséquence |
| --- | --- | --- |
| A | Assainissement contrôlé des anciens éléments sans conservation volontaire | Exposition résiduelle réduite, preuves de réalisation et d'efficacité requises |

Démarrer le retrait/assainissement sous procédure et mandat admissibles
après preuve d'engagement et de récupération des deux nouvelles copies/moyens.
Aucune destruction anticipée d'un élément encore nécessaire à la préparation.
Pas de délai volontaire de conservation des anciens secrets ; exécution,
transport et qualification sous budgets finis à arbitrer, sans effacement
instantané ou automatique promis. Références et preuve courante d'engagement
contrôlées avant chaque cible irréversible ; résultat incertain bloque la cible,
sans nouvelle génération supposée engagée par un accusé absent. Quarantaine
volontaire non retenue ; garde sécurisée pendant exécution technique sans délai
volontaire de conservation. Incidents/retraits A05 prioritaires.

Inventaire de tous exemplaires/moyens connus par références publiques,
supports et garde ; retrait d'objets privés et clés distinct de conservation des
métadonnées/preuves/audit sans secret. Méthode adaptée au support/provider et
sensibilité, vérification d'exécution puis validation de l'efficacité ; simple
suppression de fichier ou ligne d'inventaire sans preuve d'assainissement.
Effacement cryptographique envisageable seulement sous profil qualifié couvrant
les clés nécessaires et tous leurs exemplaires/moyens récupérables, sans secret
antérieurement exposé déclaré effacé rétroactivement. Autre méthode qualifiée
ou destruction physique selon support et mandat ; sélection validée A10i34,
pas de commande générique de nettoyage ou destruction du volume/hôte partagé.
Périmètre ciblé protégeant clé racine/principal, nouvelles copies/moyens, données
non concernées et preuves nécessaires ; profil non exportable respecté.
Support perdu/inaccessible : état non assaini/invérifiable conservé et incident
traité selon contexte A05/A10i21, pas de destruction déclarée par seul retrait
logique. Perte d'un ancien support ne prouve pas à elle seule une compromission.
Échec/écart d'assainissement empêche clôture du retrait, pas de révocation
collective automatique par ce seul motif ou nouvelle protection supposée compromise.
A validée pour limiter conservation/exposition des anciens secrets après
succès prouvé, sans effacement instantané ou matériel perdu présumé détruit.
Coûts/délais/méthodes/supports et rétention des preuves à qualifier, aucune
supériorité universelle ou charge courante PA/PBO imposée ; Linux/Windows
physiques/VM, Docker/LXC Proxmox pris en compte, snapshots/stockages virtuels
sans disparition de données déduite d'une suppression logique. Une personne
habilitée par opération A10i22 B, effets Django/A07/A12 et A05 conservés.
Référence : [NIST SP 800-88 révision 2, sections 3.2, 4.5 et 4.6](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-88r2.pdf)
pour conditions d'effacement cryptographique, assurance et documentation ;
politique de calendrier Pixs validée sans méthode certifiée ou conformité déclarée.
Recette : nouvelle preuve absente/incertaine, ancien élément encore requis,
exemplaire de clé oublié, objet nouveau ciblé par erreur, support partagé/perdu,
effacement échoué/non validé et absence de droit réactivé.
A10i33 A validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i33

- **WHEN** un profil revendique le traitement A10i33 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--d749b26b0b

Source : `openspec/specs/pzt/spec.md`, ligne 6936. SHA-256 du bloc : `0736b7dc7f3595b1a0697aec52102c968ed6f63d429d2c8a7aacf1982ad4b07b`.

~~~~text
### Requirement: Contrat A10i34 — Méthode d’assainissement qualifiée par profil — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i34 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i34

Assainissement sans conservation volontaire A10i33, transition vérifiée A10i32,
cibles anciennes seulement et contrôle individuel A10i22 B conservés. Politique
de sélection validée, techniques concrètes à qualifier, aucune opération réelle ici.

| Choix validé | Politique | Condition principale |
| --- | --- | --- |
| A | Méthode qualifiée définie par profil : effacement cryptographique si admissible, sinon purge ou destruction adaptées | Conditions prouvées pour chaque cible, même assurance requise et périmètre protégé |

Correspondance cible/support/provider/méthode versionnée et approuvée,
préconditions vérifiées avant opération, aucune méthode moins exigeante choisie
après erreur. Effacement cryptographique (CE) admissible seulement si données
cibles sous chiffrement qualifié, sans ancien clair résiduel et avec couverture
de tous exemplaires/moyens récupérant les anciennes clés nécessaires.
Assainissement des clés selon provider/support qualifié ; révocation métier ou
suppression de référence sans destruction cryptographique présumée. Clé inconnue,
perdue ou hors maîtrise, résultat invérifiable : effacement complet non déclaré.
Les nouvelles copies et le principal conservent la même clé racine admissible ;
objectif CE limité aux anciens objets/moyens ciblés, sans disparition globale
de cette clé privée présumée. AES-256-GCM A10i27 sans qualification CE ou
certification automatiquement déduites. Si préconditions CE absentes, autre
purge/destruction qualifiée prévue par profil/mandat, sans secret exposé ou
repli moins sûr. Équipements/méthodes à préciser selon risque/support ; aucun
écrasement générique supposé adapté à tout SSD, VM ou conteneur.

Références/générations et engagement courant vérifiés, mandat borné
cibles/impacts, une personne habilitée A10i22 B ; vérification d'exécution puis
validation d'efficacité et audit sans secret A10i33. Échec/incompatibilité/écart
empêche clôture ; A05/A10i21 selon faits, aucune méthode non qualifiée ou secret
compromis déclaré effacé. Changement de méthode seulement sous profil/mandat
admissibles. Nouvelle protection/principal et preuves nécessaires préservés,
dossier de preuve/clôture validé A10i35, assurance/réutilisation, techniques
et budgets à qualifier.
A validée pour adapter la méthode au support sous assurance commune et
permettre la réutilisation quand qualifiée ; aucune destruction physique
systématique imposée comme méthode unique. Ressources/coûts à mesurer, aucune sécurité/performance
universellement supérieure. Linux/Windows physiques/VM, Docker/LXC Proxmox
qualifiés sans modification implicite du stockage/hôte ou charge d'assainissement
racine courante sur les PA ordinaires.
[NIST SP 800-88 révision 2, sections 3.1, 3.2 et 4.5](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-88r2.pdf)
pour méthodes, conditions CE et assurance ; politique Pixs validée, aucun
profil concret, certification ou conformité déclarés. Recette : clé copiée,
ancien clair résiduel, clé inconnue, support partagé/virtuel/non destructible,
méthode incompatible, destruction partielle et protection des éléments courants.
A10i34 A validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i34

- **WHEN** un profil revendique le traitement A10i34 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

