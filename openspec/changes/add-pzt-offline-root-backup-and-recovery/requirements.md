# Références normatives — Z13

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 5766 | [Contrat A10i21 — Sauvegarde et récupération de la clé racine hors ligne — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L5766) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 5904 | [Contrat A10i22 — Opérations de sauvegarde et récupération racine par une personne habilitée — option B validée le 7 octobre 2026](../../specs/pzt/spec.md#L5904) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 6014 | [Contrat A10i23 — Deux sauvegardes privées racine sur supports et lieux distincts — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L6014) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 6133 | [Contrat A10i24 — Clé de protection aléatoire indépendante pour les sauvegardes racine — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L6133) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 6242 | [Contrat A10i25 — Clé de protection commune aux deux copies d’une génération racine — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L6242) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 6352 | [Contrat A10i26 — Deux moyens complets de récupération de la clé commune — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L6352) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 6479 | [Contrat A10i27 — Chiffrement des sauvegardes privées racine — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L6479) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 6544 | [Contrat A10i28 — Production déterministe des nonces de sauvegarde racine — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L6544) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--a1709a96cc

Source : `openspec/specs/pzt/spec.md`, ligne 5766. SHA-256 du bloc : `2f5f5d45fadc2c5ee9c3c20eb16d90cf082275637f63e3f80eb1ba407aaa4738`.

~~~~text
### Requirement: Contrat A10i21 — Sauvegarde et récupération de la clé racine hors ligne — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i21 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i21

Choix limité à la clé privée racine A10i6/A10i14. A10i9 reste inchangé pour
les intermédiaires : remplacement par clé indépendante, sans restauration de
leur ancienne clé privée ; A12g, TLS terminal, WireGuard et TPM hors périmètre.
La nouvelle paire de chaque succession normale A10i18 reste obligatoire.

| Choix validé | Sauvegarde de la clé privée racine | Conséquence d'une perte sans compromission |
| --- | --- | --- |
| A | Sauvegarde protégée, chiffrée et hors ligne | Récupération autorisée et bornée, puis succession préparée |

A validée : sauvegarde sous protection cryptographique d'intégrité et de
confidentialité qualifiée, conservée hors ligne et séparée du support racine
principal, sous garde autorisée. Moyens de déprotection séparés de la copie,
accès/cérémonie tracés sans secret ; aucune copie privée en clair dans fichier,
rapport, dépôt, PostgreSQL, image ou snapshot applicatif. Ni clé racine ni
sauvegarde privée accessibles aux processus courants PBO/PZT/PA ; PBO ne suit
que références publiques, état, dates et preuves non sensibles. Contrôle
individuel A10i22 B, deux copies A10i23 A et protection/moyens A10i24–A10i30 A
validés ; support/provider, garde et périodicité des exercices restent à
préciser dans ces limites. Profil racine autorisé requis : sauvegarde/
récupération matériellement qualifiées, sans export en clair ou abaissement
implicite d'une protection non exportable. Incapacité du provider à respecter
le profil bloque sa qualification, sans copie de contournement.

Récupération A uniquement après perte/corruption qualifiée sans compromission
suspectée, sous cérémonie hors ligne et mandat explicite borné. Identité de
clé/certificat, intégrité de copie, possession, protection, admissibilité
courante A10i17 et état public d'émission/retrait réconciliés avant usage.
Original rendu indisponible pour signature sous preuve qualifiée ; copie sans
second signataire actif ou activation automatique après panne. État incertain,
suspicion/compromission, clé retirée ou usage expiré : réutilisation refusée,
A05 et procédure exceptionnelle de nouvelle racine authentifiée à définir.
Récupération sans ancien mandat/droit/ancrage réactivé, date ou cryptopériode
remise à zéro, numéro de certificat réutilisé ou anciennes données réintroduites.
Usage récupéré limité au plan autorisé de reprise et succession préparée avec
nouvelle paire A10i18 ; durée d'usage exceptionnelle à arbitrer, aucune fenêtre
A10i20 de 30 jours ou marge A10i17 de 1460 jours déduite pour cet usage.

Perte privée seule sans invalidation automatique des signatures déjà émises,
mais sans nouvelles signatures racine jusqu'à récupération autorisée.
Chaînes existantes bornées par politique/validités/retraits ; copie absente ou
inadmissible sans reprise forcée, nouvelle racine/reprovisionnement authentifié
sous procédure exceptionnelle à définir. Aucune racine apprise par découverte
ni ancien canal présumé disponible. Si PZT ne permet plus de contrôle courant,
récupération A02 authentifiée sous ancrage préalable admissible ou procédure
exceptionnelle distincte, sans canal de contrôle non autorisé.

Données publiques et audit sauvegardables séparément,
restauration sans recul de l'état de sécurité. Compromission connue/suspectée
sans maintien d'ancienne confiance par sauvegarde ; retrait A05 prioritaire,
aucune fenêtre de grâce. Destruction contrôlée des copies privées devenues
inutilisables pour signature, conservation publique distincte pour audit.
Recette prévue : perte/corruption, copie altérée, gardiens/moyens indisponibles,
provider incompatible, original encore signant, clé expirée/retirée, état ancien,
compromission, contrôle PZT absent et exercice isolé sans droits réactivés.
Qualification sur les cibles Linux/Windows physiques/VM, Docker/LXC Proxmox,
sans stockage de sauvegarde racine imposé sur les PA ni RTO/continuité garantis.

A validée pour disposer d'une récupération contrôlée après perte matérielle
pendant le cycle long de la racine, avec copies secrètes sous protections et
garde qualifiées. Ressources courantes
PA/PBO sans charge cryptographique de sauvegarde racine en ligne prévue,
coûts d'exploitation et délais à qualifier. Le [NIST SP 800-57 partie 1,
sections 8.2.2.1 et B.3.1.1](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf)
traite la sauvegarde CA comme une possibilité à évaluer, avec récupération
fortement protégée ; ni obligation universelle ni conformité Pixs déclarée.
A10i21 A validé le 7 octobre 2026.

##### Application au PA — A10i21

Clé privée racine A10i6/A10i14 seule concernée ; A10i9 sans restauration des
clés privées intermédiaires conservé. A12g/TLS terminal/WireGuard/TPM exclus,
succession normale à nouvelle paire A10i18 maintenue.

| Choix validé | Sauvegarde de la clé privée racine | Conséquence d'une perte sans compromission |
| --- | --- | --- |
| A | Sauvegarde protégée, chiffrée et hors ligne | Récupération autorisée et bornée, puis succession préparée |

A validée : copie chiffrée/intégrité qualifiée hors ligne, garde autorisée séparée du
support principal et moyens de déprotection séparés. Cérémonie/audit sans secret,
aucune copie privée en clair dans fichier/rapport/dépôt/PostgreSQL/image/snapshot.
Clé et sauvegarde racine hors processus courants PBO/PZT/PA, PBO limité aux
références publiques/états/dates/preuves non sensibles. Contrôle individuel
A10i22 B, deux copies A10i23 A et protection/moyens A10i24–A10i30 A validés ;
support/provider, garde et exercices restent à préciser dans ces limites.
Profil racine autorisé et
sauvegarde/récupération qualifiées sans export clair ou protection non exportable
abaissée ; provider incompatible refusé, aucune copie de contournement.
Reprise après perte/corruption qualifiée sans compromission suspectée, cérémonie
hors ligne/mandat borné, identité/intégrité/possession/protection/admissibilité
A10i17 et état public d'émission/retrait courants réconciliés. Original exclu
de signature avec preuve qualifiée, sans second signataire actif ou activation
par seule panne. Incertitude/suspicion/compromission/retrait/usage expiré :
réutilisation refusée, A05 et procédure exceptionnelle authentifiée à définir.
Sans ancien droit/mandat/ancrage réactivé, date/cryptopériode remise à zéro,
numéro réutilisé ou données anciennes réintroduites. Usage récupéré limité au
plan de reprise autorisé puis succession préparée à nouvelle paire A10i18 ;
durée exceptionnelle à arbitrer, sans 30 jours A10i20 ou 1460 jours A10i17
automatiquement accordés pour cet usage.

Perte privée seule sans signatures passées invalidées automatiquement, mais
nouvelles signatures racine impossibles jusqu'à récupération autorisée.
Chaînes existantes bornées par politique/validités/retraits ; copie absente ou
inadmissible sans reprise forcée, nouvelle racine/reprovisionnement authentifié
sous procédure exceptionnelle à définir. Aucune confiance par découverte ou
ancien canal présumé disponible ; PZT courant absent : A02 authentifiée sous
ancrage préalable admissible ou procédure exceptionnelle distincte, sans
contrôle non autorisé.
Données publiques/audit distincts, aucun état de sécurité ancien restauré.
Compromission/suspicion : A05 sans confiance conservée par copie ou grâce ;
copies privées inutilisables pour signature détruites sous contrôle, audit
public distinct. Recette : perte/copie altérée, gardiens/moyens indisponibles,
provider incompatible, original signant, expiration/retrait/état ancien,
compromission/PZT absent et exercice isolé sans droits réactivés.
Qualification Linux/Windows physiques/VM, Docker/LXC Proxmox, sans sauvegarde
racine placée sur les PA ou RTO/continuité garantis. A validée pour reprise
contrôlée après perte matérielle sur cycle racine long, copies secrètes sous
protection/garde qualifiées. Pas de charge cryptographique
courante de sauvegarde racine en ligne prévue PA/PBO, exploitation à qualifier.
NIST SP 800-57 partie 1 sections 8.2.2.1/B.3.1.1 référencé cadrage PZT : possibilité
CA à évaluer/récupération protégée, sans obligation ou conformité déclarée.
A10i21 A validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i21

- **WHEN** un profil revendique le traitement A10i21 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--833ab7d9b9

Source : `openspec/specs/pzt/spec.md`, ligne 5904. SHA-256 du bloc : `823c586be73063cfbf8afc8cad211a87bf07923a7ee6b6c279d9c569c52be99b`.

~~~~text
### Requirement: Contrat A10i22 — Opérations de sauvegarde et récupération racine par une personne habilitée — option B validée le 7 octobre 2026

Le rôle chargé du traitement A10i22 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i22

Choix de gouvernance pour A10i21, limité aux opérations sensibles sur la
sauvegarde privée racine : création/remplacement, accès aux moyens de
déprotection, récupération et destruction contrôlée. Une personne explicitement
habilitée suffit pour chaque opération autorisée. Plusieurs personnes peuvent
être individuellement habilitées selon politique, sans double approbation
requise ni monopole permanent d'une personne sur toute l'installation.

| Choix validé | Contrôle des opérations sensibles | Conséquence organisationnelle |
| --- | --- | --- |
| B | Une personne habilitée | Intervention plus simple, contrôle concentré |

Personne identifiée/authentifiée, habilitation vérifiée pour l'opération exacte,
la racine, la génération et les copies/supports concernés, mandat à échéance
finie. Titre administrateur ou possession d'un support sans autorisation
implicite. Accord, périmètre et résultat corrélés dans les preuves/audit sans
secret ; modification de cible, génération ou mandat avec nouvel accord
admissible. Duplicata/rejeu/restauration sans ancien accord autorisant une
nouvelle opération. A10i21 conservé : chiffrement/intégrité, copie et moyens
de déprotection séparés, garde qualifiée et clé hors processus courants PBO/PZT/PA.
Exécution par une personne autorisée, contrôle d'accès/déprotection/exécution
qualifié ; aucune exigence de deux personnes, de simple témoin supplémentaire
ou de signatures de deux services A12c pour remplacer l'habilitation humaine.

Cérémonie racine hors ligne, contrôle Django/A07/A12 de l'autorisation et de
l'état public pour les effets PZT. Mandat préalable borné peut permettre une
cérémonie hors ligne qualifiée sans clé racine connectée aux processus courants.
Admissibilité/validités et règles de retrait A05 prioritaires ; preuve ou état
courant invérifiables : opération ou effets dépendants bloqués, réconciliation
sans confiance prolongée. Personne absente ou habilitation expirée : autre
personne seulement si elle dispose de sa propre habilitation et d'un mandat
admissible, sans transfert implicite de compte, moyen d'authentification ou
ancien accord. Refus/retrait de sécurité A05 immédiats et indépendants de la
cérémonie, destruction matérielle distincte. Renouvellements TLS des PA et
émissions intermédiaires en ligne sans intervention humaine ajoutée par A10i22.

Nombre total de personnes habilitées/suppléants, protection et récupération
des moyens de déprotection, outil/provider, preuve d'accord, durée des mandats
et procédure d'urgence restent à arbitrer. Deux copies validées en A10i23.
Ni partage cryptographique de secret, seuil de reconstruction, concaténation
de mots de passe, découpe de clé ou méthode Shamir adoptés. Mécanisme compatible
avec le contrôle individuel validé, à qualifier sur les périmètres Linux/Windows
physiques/VM et Docker/LXC Proxmox ; aucun privilège/matériel imposé aux PA ordinaires.

B validée le 7 octobre 2026 pour simplifier l'intervention, avec responsabilité
concentrée dans chaque opération et protections qualifiées conservées. Aucun
coût CPU/RAM courant de cérémonie imposé aux PA ; effort/délais à qualifier.
Le [NIST SP 800-57 partie 1, sections 9.1 et 9.3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf)
traite identité, autorisation, responsabilités et traçabilité ; contrôle
individuel comme choix Pixs, sans obligation universelle ou conformité déduite.
Recette prévue : personne habilitée/non habilitée, administrateur sans mandat,
mauvaise cible, mandat expiré, accord rejoué, suppléant sans habilitation,
copie altérée, état incertain et retrait A05 immédiat.

##### Application au PA — A10i22

Gouvernance A10i21 : création/remplacement de sauvegarde privée, accès aux
moyens de déprotection, récupération et destruction contrôlée. Une personne
explicitement habilitée suffit par opération ; plusieurs personnes
individuellement habilitables, sans double accord ou monopole permanent imposé.

| Choix validé | Contrôle des opérations sensibles | Conséquence organisationnelle |
| --- | --- | --- |
| B | Une personne habilitée | Intervention plus simple, contrôle concentré |

Personne identifiée/authentifiée/habilitée pour opération/racine/génération/
copies/supports sous mandat fini. Administrateur ou support détenu sans droit
implicite. Accord/périmètre/résultat corrélés sans secret, cible/génération/mandat
modifiés avec nouvel accord ; duplicata/rejeu/restauration sans nouvelle
opération permise par accord ancien. A10i21 conservé : chiffrement/intégrité,
copie/moyens séparés, garde qualifiée, clé hors processus courants PBO/PZT/PA.
Contrôle individuel d'accès/déprotection/exécution qualifié, aucune deuxième
personne/témoin ou signature de services A12c substituée à l'habilitation humaine.
Cérémonie hors ligne, Django/A07/A12 pour autorisation/état public des effets PZT,
mandat préalable fini en cérémonie qualifiée sans racine connectée aux processus
courants. Admissibilité/validités/retrait A05 prioritaires, preuve/état courant
invérifiables bloquent opération ou effets dépendants, réconciliation sans
confiance prolongée. Personne absente/habilitation expirée : suppléant seulement
avec habilitation propre et mandat admissible, sans compte/authentifiant/accord
transférés implicitement. Refus/retrait A05 immédiats indépendants de cérémonie,
destruction matérielle distincte. Renouvellement TLS PA/émission intermédiaire
en ligne sans intervention humaine ajoutée par A10i22.
Personnes habilitées/suppléants totaux, protection/récupération des moyens,
outil/provider/preuves/durée/urgence à arbitrer ; deux copies validées A10i23.
Aucun partage cryptographique/seuil/concaténation/découpe/Shamir adopté ;
mécanisme compatible avec contrôle individuel validé, qualification Linux/
Windows physiques/VM, Docker/LXC Proxmox, sans privilège/matériel imposé aux PA.
B validée le 7 octobre 2026 : intervention simplifiée, responsabilité concentrée
par opération, protections conservées ; pas de coût CPU/RAM courant de cérémonie
imposé aux PA, effort/délais à qualifier. NIST SP 800-57 partie 1 sections 9.1/9.3
référencé cadrage PZT pour identité/autorisation/responsabilités/traçabilité, contrôle
individuel choix Pixs sans obligation/conformité déduite. Recette : habilité/
non habilité, administrateur sans mandat, cible/mandat inadmissibles/rejeu,
suppléant non habilité, copie altérée, état incertain et retrait A05 immédiat.

#### Scenario: Conformité du traitement A10i22

- **WHEN** un profil revendique le traitement A10i22 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--338098f06c

Source : `openspec/specs/pzt/spec.md`, ligne 6014. SHA-256 du bloc : `195abc548c96de098090d07022ec66df669edd19bf43a6bfe6e68c1527ed99da`.

~~~~text
### Requirement: Contrat A10i23 — Deux sauvegardes privées racine sur supports et lieux distincts — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i23 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i23

Premier jet validé pour A10i21, copies privées chiffrées/intègres hors ligne d'une
même génération racine encore admissible, en plus du support principal.
A10i22 B conservé : une personne habilitée suffit à l'opération autorisée ;
deux copies sans deux gardiens, deux accords ou partage cryptographique imposés.
Copies de sauvegarde inactives, sans racine en ligne ou signataires simultanés.

| Choix validé | Copies de sauvegarde privées hors ligne | Placement |
| --- | --- | --- |
| A | Deux copies chiffrées, hors support principal | Supports distincts et lieux de conservation distincts |

A validée : deux copies identifiées/inventoriées, sur supports distincts dans des lieux
distincts, chacune séparée du support principal et des moyens permettant sa
déprotection. Risques communs de sinistre, perte/vol, stockage, alimentation,
contrôle d'accès et dépendance provider identifiés dans le plan ; deux fichiers,
partitions, VM ou snapshots sur même stockage/site sans indépendance physique
prouvée ne satisfont pas le placement A. Chiffrement/hors ligne seuls sans
protection physique générale garantie. Transport et garde sous procédure
autorisée, sans copie dans les processus PBO/PZT/PA ou synchronisation cloud
implicite. Même clé publique/génération attendue, objets de sauvegarde vérifiés
séparément ; ni format identique ni égalité des octets chiffrés présumés.

Sauvegarde valide
sans moyens de déprotection accessibles aux personnes autorisées ne constitue
pas une récupération disponible. Redondance/récupération de ces moyens à arbitrer,
sans les placer avec les copies par défaut ni ignorer leur risque commun.

Copies, références et essais suivis sans secret ; intégrité/lisibilité et
récupération qualifiées par procédure isolée autorisée, sans racine ancienne ou
droits réactivés. Cadence des contrôles, renouvellement des supports, formats,
protection cryptographique et durée de l'usage récupéré restent à arbitrer ;
origine de la clé de protection validée en A10i24 A.
Provider doit permettre copie/récupération selon profil autorisé, sans export
en clair ou protection non exportable abaissée. Racine remplacée/retirée ou
usage expiré : A10i21/A05 prioritaires, copies privées devenues inutilisables
pour signature détruites sous contrôle, références publiques d'audit distinctes.

Perte/corruption d'une copie sans compromission suspectée : état de sauvegarde
dégradé explicite, remplacement sous mandat individuel A10i22 et contrôles
A10i21 ; aucune récupération/signature automatique, droit prolongé ou révocation
collective déduite du seul nombre de copies. Suspicion/compromission connue :
retrait A05 et réconciliation prioritaires, multiplication de copies sans
réhabilitation de la clé. Deux copies ne garantissent ni tolérance aux pannes
indépendantes, ni continuité/RTO, ni récupération après perte de tous les moyens.
Qualification cibles Linux/Windows physiques/VM, Docker/LXC Proxmox sans placement
obligatoire sur les PA ou modification implicite de montages/droits/matériel.

A validée pour permettre une récupération après perte d'un exemplaire
si l'autre et les moyens requis restent admissibles, au prix d'un second
support/site à protéger et suivre. Pas de charge cryptographique courante de
sauvegarde privée racine
en ligne imposée aux PA/PBO ; stockage, effort et délais à qualifier.
Le [NIST SP 800-57 partie 1, sections 9.5.1 à 9.5.3](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf)
traite protection, récupération et plan de continuité des clés ; deux copies
et leurs lieux constituent un choix Pixs validé, sans nombre imposé par la
référence ou conformité déclarée. Recette prévue : un exemplaire perdu/corrompu,
copies sur même domaine de panne, moyens absents, mauvaise génération, provider
incompatible, copie expirée/retirée, compromission et remplacement autorisé.
A10i23 A validé le 7 octobre 2026.

##### Application au PA — A10i23

Premier jet validé A10i21 : copies privées chiffrées/intègres hors ligne d'une même
génération racine admissible, hors support principal. A10i22 B conservé,
une personne habilitée par opération, deux copies sans deux gardiens/accords
ou partage cryptographique ; copies inactives sans signataires simultanés.

| Choix validé | Copies de sauvegarde privées hors ligne | Placement |
| --- | --- | --- |
| A | Deux copies chiffrées, hors support principal | Supports distincts et lieux de conservation distincts |

A validée : copies identifiées/inventoriées sur supports/lieux distincts, séparées du
principal et des moyens de déprotection. Risques communs sinistre/perte/vol/
stockage/alimentation/accès/provider déclarés ; fichiers/partitions/VM/snapshots
sur même stockage/site sans indépendance physique prouvée insuffisants.
Chiffrement/hors ligne sans sécurité physique générale garantie. Transport/
garde autorisés, aucune copie PBO/PZT/PA ou synchronisation cloud implicite.
Même clé publique/génération, objets vérifiés séparément sans format/octet
chiffré identique présumé. Moyens de déprotection accessibles aux
personnes autorisées requis ; leur redondance/récupération à arbitrer, sans
moyens stockés avec copies par défaut ou risque commun ignoré.
Copies/références/essais sans secret, intégrité/lisibilité/récupération qualifiées
sous procédure isolée autorisée sans anciens droits/racine réactivés. Cadence/
renouvellement support/formats/protection/durée d'usage récupéré à arbitrer ;
origine de clé de protection validée A10i24 A.
Provider qualifié sans export clair ou protection non exportable abaissée.
Racine remplacée/retirée ou usage expiré : A10i21/A05 prioritaires, destruction
contrôlée des copies privées inutilisables pour signature, audit public distinct.
Perte/corruption d'une copie sans compromission suspectée : état dégradé suivi,
remplacement sous mandat individuel A10i22/A10i21, sans récupération/signature
automatique, droit prolongé ou révocation collective par seul nombre de copies.
Suspicion/compromission : A05/réconciliation, nouvelles copies sans clé réhabilitée.
Aucune indépendance/continuité/RTO/récupération après tous moyens perdus garantis.
Qualification Linux/Windows physiques/VM, Docker/LXC Proxmox sans placement PA
ou montages/droits/matériel implicitement modifiés.
A validée pour perte d'un exemplaire si l'autre/moyens admissibles,
second support/site à protéger et suivre.
Pas de charge cryptographique courante de sauvegarde privée racine en ligne
imposée aux PA/PBO, stockage/effort/délais à qualifier. NIST SP 800-57 partie 1
sections 9.5.1–9.5.3 référencé cadrage PZT : protection/récupération/continuité,
sans nombre de copies/lieux ou conformité Pixs déduits. Recette : copie perdue/
corrompue, panne commune, moyens absents, génération erronée/provider incompatible,
expiration/retrait/compromission/remplacement autorisé. A10i23 A validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i23

- **WHEN** un profil revendique le traitement A10i23 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--1572528364

Source : `openspec/specs/pzt/spec.md`, ligne 6133. SHA-256 du bloc : `f609c44b87ca015c032b11466be8d7787dc142659a781a90951ea43d7bba36ea`.

~~~~text
### Requirement: Contrat A10i24 — Clé de protection aléatoire indépendante pour les sauvegardes racine — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i24 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i24

Choix validé limité à l'origine de la clé protégeant les copies A10i21/A10i23.
A10i22 B conservé : une personne habilitée par opération sous mandat borné.
Deux copies privées racine hors ligne sur supports/lieux distincts ; clé de
protection sans clé de signature racine, TLS, WireGuard, TPM ou signataire A12
réutilisée. Confidentialité et intégrité qualifiées requises.

| Choix validé | Origine de la clé de protection | Moyen à conserver pour récupération |
| --- | --- | --- |
| A | Clé aléatoire indépendante, générée par un mécanisme qualifié | Clé protégée, séparée des sauvegardes racine |

A validée : génération indépendante par source aléatoire cryptographique qualifiée,
force adaptée au profil, protection/garde de cette clé séparée des copies
racine et de leur support principal. Clé non dérivée d'un mot de passe, de la
clé racine ou d'une autre clé de service ; usage réservé à la protection des
sauvegardes. Authentifiant éventuel d'accès au provider/stockage protégé distinct
de l'origine aléatoire de cette clé ; A n'interdit pas un authentifiant humain
pour déverrouiller son moyen de conservation. Récupération de la clé de
protection et dépendances à prévoir : sa perte peut rendre les deux copies
racine inutilisables, même si elles sont intactes. Clé commune aux deux copies
d'une génération validée en A10i25 ; nombre de moyens, support/provider et
rotation restent à arbitrer. Aucune indépendance des deux sauvegardes présumée
face à la perte d'un moyen commun.

Objet protégé et métadonnées nécessaires contrôlés
avant usage : format/version, référence de racine/génération/copie et de
protection, intégrité et possession, état courant et validités A10i21/A05.
Déchiffrement réussi seul sans autorisation de signature ou nouvelle confiance.
Déprotection uniquement dans le périmètre racine qualifié, sans fichier de clé
racine en clair, journal, dépôt, base PostgreSQL, image/snapshot applicatif ou
transfert aux processus courants PBO/PZT/PA. Provider non exportable respecte
son profil ; aucune extraction privée en clair ou bascule de profil pour
contourner une incompatibilité. Clé/paramètres absents, objet altéré ou
état incertain : récupération refusée, sans essayer automatiquement l'autre
mode ou prolonger une validité. Compromission suspectée/connue : A05/A10i21,
sauvegarde re-chiffrée sans racine automatiquement réhabilitée.

Algorithme de chiffrement/enveloppement, longueur de clé, format, gestion des
nonces si applicable, contrôle des métadonnées, protection/récupération des
moyens et cryptopériodes à préciser après arbitrage. Choix TLS PBO A10h sans
choix automatique d'algorithme de sauvegarde ; aucun logiciel/bibliothèque,
HSM/TPM ou nouvelle dépendance adopté. Qualification sur cibles Linux/Windows
physiques/VM, Docker/LXC Proxmox sans clé de protection placée sur PA ordinaire
ou modification implicite de privilèges. CPU/RAM concernent les cérémonies
hors ligne, sans travail de sauvegarde racine en ligne ajouté au PA/PBO.

A validée pour une clé indépendante d'un secret mémorisé, avec gestion et
récupération explicites. Sécurité/ressources/délais dépendent des moyens qualifiés, sans
classement universel ou récupération garantie. Le [NIST SP 800-57 partie 1,
section B.3.5](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf)
traite les clés de protection et leur récupération ; référence pour les
principes, sans algorithme ou conformité déclarée. Recette : moyen perdu, mauvaise clé/paramètres,
objet/métadonnées altérés, génération erronée, provider incompatible, état
expiré/compromis, absence de repli et récupération autorisée sans droits réactivés.
A10i24 A validé le 7 octobre 2026.

##### Application au PA — A10i24

Origine de la clé protégeant copies A10i21/A10i23 validée ; A10i22 B
conservé, une personne habilitée/mandat borné, deux copies racine hors ligne
sur supports/lieux distincts. Clé de protection sans clé racine/TLS/WireGuard/
TPM/signataire A12 réutilisée ; confidentialité/intégrité qualifiées requises.

| Choix validé | Origine de la clé de protection | Moyen à conserver pour récupération |
| --- | --- | --- |
| A | Clé aléatoire indépendante, générée par un mécanisme qualifié | Clé protégée, séparée des sauvegardes racine |

A validée : clé indépendante générée par aléa cryptographique qualifié, force adaptée,
usage dédié sauvegardes, protection/garde séparées des copies et du principal.
Ni phrase, clé racine ou autre clé de service à l'origine ; authentifiant humain
éventuel d'accès au stockage/provider distinct et permis. Récupération de ce
moyen requise : perte peut rendre deux copies intactes inutilisables. Clé commune
aux deux copies d'une génération validée A10i25 ; redondance des moyens/support/
provider/rotation à arbitrer, sans indépendance présumée face à perte d'un moyen commun.
Objet/métadonnées contrôlés avant usage : format/version/racine/génération/copie/
protection/intégrité/possession/état courant/validités A10i21/A05. Déchiffrement
sans droit de signature ou nouvelle confiance. Périmètre racine qualifié sans
clé racine en clair dans fichier/journal/dépôt/PostgreSQL/image/snapshot ou
processus PBO/PZT/PA. Profil non exportable respecté, incompatibilité sans
extraction privée en clair ou profil abaissé. Moyen/paramètres absents, copie
altérée/état incertain : refus sans autre mode automatique ou validité prolongée.
Compromission : A05/A10i21, re-chiffrement sans clé racine réhabilitée.
Chiffrement/enveloppement/longueur/format/nonces/métadonnées/protection et
récupération des moyens/cryptopériodes à préciser ; TLS A10h sans algorithme de
sauvegarde déduit. Aucun logiciel/bibliothèque/HSM/TPM/dépendance adopté,
qualification Linux/Windows physiques/VM, Docker/LXC Proxmox sans moyen placé
sur PA ordinaire/privilège modifié. CPU/RAM de cérémonie hors ligne, aucune
sauvegarde racine en ligne ajoutée PA/PBO. A validée pour clé indépendante
d'un secret mémorisé avec gestion/récupération, sans classement universel ou
reprise garantie. NIST SP 800-57 B.3.5
référencé cadrage PZT pour protection/récupération, sans algorithme/conformité adoptés. Recette : moyen perdu,
clé/paramètres erronés, objet/métadonnées altérés, génération/provider invalides,
expiration/compromission, aucun repli ou droit réactivé. A10i24 A validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i24

- **WHEN** un profil revendique le traitement A10i24 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--bd4f7394d5

Source : `openspec/specs/pzt/spec.md`, ligne 6242. SHA-256 du bloc : `4212b7b41c80badcb5deeeb75be73bcb3caa721af6b3edc2cb2a7f22c565b746`.

~~~~text
### Requirement: Contrat A10i25 — Clé de protection commune aux deux copies d’une génération racine — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i25 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i25

Choix validé pour les deux copies A10i23 et l'origine aléatoire indépendante validée
A10i24. A10i22 B conservé : une personne habilitée suffit par opération sous
mandat borné. Même clé de signature racine sauvegardée dans les deux objets ;
clé de protection sans clé de signature/TLS/WireGuard/TPM/A12 réutilisée.

| Choix validé | Répartition des clés de protection | Gestion et dépendances |
| --- | --- | --- |
| A | Une clé commune aux deux copies d'une même génération racine | Gestion simplifiée, récupération redondante de cette clé requise |

A validée : clé dédiée au périmètre et à une génération racine, commune aux deux copies
admissibles de cette génération. Aucun usage global pour toutes les racines,
autorités, générations ou secrets applicatifs. Copies identifiées et vérifiées
séparément, chiffrement/intégrité qualifiés, métadonnées et règles de nonces
éventuelles respectées sur tout l'usage de cette clé. Nombre/placement/protection
des exemplaires ou moyens de récupération de la clé commune à arbitrer ;
deux moyens validés en A10i26,
redondance de récupération requise et qualifiée, hors copies racine/support
principal. Clé commune avec exemplaire unique irremplaçable sans satisfaction
du choix validé. Deux copies chiffrées seules ne rendent pas la clé commune
récupérable : perte de tous ses moyens peut rendre les deux inutilisables.

Copie et moyens de déprotection séparés, garde
hors ligne, provider/profil qualifiés et opérations A10i21/A10i22 autorisées.
Possession de clé ou déchiffrement seul sans droit de signature, ancrage
réactivé ou validité prolongée. Clé absente, objet altéré ou état invérifiable :
refus de récupération concernée, autre copie seulement sous procédure et
mandat admissibles, aucun repli implicite. État/métadonnées courants réconciliés
Django/A07/A12 pour effets PZT, A05 prioritaire. Copie de clé de protection sans
second signataire racine actif. Changement de clé ou ré-enveloppement sous plan
autorisé, correspondances/essais prouvés avant retrait d'un moyen encore requis ;
calendrier, cryptopériodes et procédure détaillée à arbitrer.

Les deux objets contiennent la même clé privée racine ; le déchiffrement
illicite d'une seule sauvegarde expose cette clé et affecte sa
confiance dans tout le périmètre dépendant. Suspicion/compromission selon
A05/A10i21, sans déclarer la racine saine parce que l'autre protection est intacte
ou les sauvegardes ont été re-chiffrées. Redondance de clés sans tolérance aux
sinistres, continuité/RTO ou sécurité universelle garanties.

A validée pour simplifier inventaire et opérations concernant deux copies
d'une même génération, avec récupération redondante qualifiée et dépendance
commune explicitée. Pas de charge cryptographique de sauvegarde racine en ligne imposée
aux PA/PBO ; stockage, effort, délais et ressources de cérémonie à qualifier
sur Linux/Windows physiques/VM, Docker/LXC Proxmox sans nouveau privilège.
Algorithme/longueur/format/provider et disposition des moyens restent ouverts.
Le [NIST SP 800-57 partie 1, section B.3.5](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf)
traite protection de plusieurs objets et récupération des clés de protection ;
répartition commune comme choix Pixs validé, sans obligation ou conformité déduite.
Recette : perte d'un/tous moyens, mauvaise correspondance, risque commun,
copie altérée, génération erronée, retrait/expiration, compromission d'une
copie et changement de protection sans droits réactivés.
A10i25 A validé le 7 octobre 2026.

##### Application au PA — A10i25

Deux copies A10i23/origine aléatoire indépendante A10i24, contrôle individuel
A10i22 B/mandat borné conservés. Même clé de signature racine dans les objets,
clé de protection sans racine/TLS/WireGuard/TPM/A12 réutilisée.

| Choix validé | Répartition des clés de protection | Gestion et dépendances |
| --- | --- | --- |
| A | Une clé commune aux deux copies d'une même génération racine | Gestion simplifiée, récupération redondante de cette clé requise |

A validée : une clé dédiée à génération/périmètre racine pour ses deux copies, sans
usage global entre racines/autorités/générations/secrets. Objets identifiés/
vérifiés séparément, intégrité/métadonnées/nonces applicables contrôlés sur
tout l'usage de cette clé. Nombre/placement/protection des exemplaires ou moyens
à arbitrer, deux moyens validés A10i26, récupération redondante qualifiée requise
hors copies/principal ;
exemplaire unique irremplaçable insuffisant. Deux sauvegardes seules sans clé
récupérable, perte de tous moyens pouvant rendre les deux inutilisables.
Copie/moyens séparés/hors ligne, provider/profil qualifiés, A10i21/A10i22
conservés. Possession/déchiffrement sans signature autorisée/ancrage réactivé/
validité prolongée. Clé absente/objet altéré/état invérifiable : refus concerné,
autre copie seulement sous procédure/mandat admissibles, sans repli implicite.
État/métadonnées courants réconciliés Django/A07/A12 pour effets PZT, A05
prioritaire, copies de protection sans signataire racine supplémentaire.
Changement de clé/ré-enveloppement sous plan autorisé, mappings/essais prouvés
avant retrait d'un moyen nécessaire, calendrier/cryptopériodes/procédure ouverts.
Même clé racine dans les deux objets : une copie déchiffrée
illicitement expose même clé racine, A05/A10i21 pour tout périmètre dépendant,
autre copie intacte/re-chiffrement sans confiance rétablie. Aucune tolérance
aux sinistres/continuité/RTO/sécurité universelle garantie par redondance.
A validée pour gestion simplifiée avec récupération redondante qualifiée et
dépendance commune explicitée. Pas de
sauvegarde racine en ligne ajoutée PA/PBO ; stockage/effort/délais/ressources de
cérémonie à qualifier Linux/Windows physiques/VM, Docker/LXC Proxmox sans privilège
nouveau. Algorithme/longueur/format/provider/disposition des moyens ouverts.
NIST SP 800-57 B.3.5 référencé cadrage PZT : protection de plusieurs objets et
récupération des clés, répartition commune choix Pixs validé sans obligation/conformité.
Recette : perte d'un/tous moyens, mauvais mapping/risque commun/copie altérée,
génération/retrait/expiration, compromission d'une copie, changement sans droits
réactivés. A10i25 A validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i25

- **WHEN** un profil revendique le traitement A10i25 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--503c3dff0a

Source : `openspec/specs/pzt/spec.md`, ligne 6352. SHA-256 du bloc : `74e2bedea641f71a390eec37d14055f15caea374521958163562e5a647654519`.

~~~~text
### Requirement: Contrat A10i26 — Deux moyens complets de récupération de la clé commune — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i26 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i26

Premier jet validé pour la clé de protection commune A10i25, origine aléatoire A10i24,
et les deux sauvegardes racine A10i23. A10i22 B maintenu : une personne habilitée
suffit par opération autorisée ; deux moyens ne signifient ni deux
personnes ni quorum de reconstruction. Nombre validé par clé de protection
admissible ; support principal et copies privées racine exclus du comptage.

| Choix validé | Moyens complets de récupération de la clé commune | Organisation |
| --- | --- | --- |
| A | Deux moyens protégés hors ligne | Chacun utilisable sans l'autre, supports et lieux distincts |

Moyen complet : exemplaire ou dispositif protégé permettant de récupérer la
même clé de protection dans le périmètre qualifié, avec format/métadonnées,
outil/provider compatible et moyens d'accès requis disponibles ou récupérables
selon plan autorisé. Fichier chiffré sans son moyen de déprotection, fragment
nécessitant les autres exemplaires, ou duplicata dépendant d'un unique dispositif
irremplaçable ne constitue pas un moyen complet indépendant. Chaque moyen
évalué avec l'autre indisponible, sans reconstitution par
partage de secret ni présence d'un second opérateur imposées.

Supports et lieux distincts entre moyens, garde séparée des deux
copies racine et du support principal, protection de confidentialité/intégrité
et d'accès qualifiée. Risques communs physiques, stockage, provider/format,
authentifiants et disponibilité des personnes habilitées déclarés. Deux fichiers
ou VM d'un même stockage sans séparation physique qualifiée ne suffisent pas.
Lieu signifie séparation de garde qualifiée, sans distance géographique ou
nombre de bâtiments implicitement choisis ; plan et domaines de panne à vérifier.
Reprise depuis le second moyen après perte d'un seul si admissible.
Aucune indépendance face à tous risques communs ou tolérance aux sinistres garantie.

Protection/garde des moyens à définir dans un plan fini de récupération, avec
toutes dépendances jusqu'aux dispositifs, authentifiants et procédures utilisables.
Aucune chaîne circulaire, clé seulement déchiffrable avec elle-même ou succession
indéfinie de sauvegardes de clés acceptée. Aucun stockage en clair de clé racine
ou de protection dans fichier/journal/dépôt/PostgreSQL/image/snapshot applicatif,
processus courants PBO/PZT/PA ou avec une copie racine. Provider non exportable
respecté, duplication seulement par mécanisme compatible qualifié sans
extraction en clair ou abaissement implicite du profil. Algorithme, longueur,
format, support concret et protection finale du moyen à arbitrer séparément ;
chiffrement AES-256-GCM des sauvegardes racine validé en A10i27.

Inventaire de références/générations/moyens et preuves sans secret ; admissibilité,
intégrité, possession, contexte courant A10i21/A10i22 vérifiés avant récupération.
Django/A07/A12 gouverne les effets PZT, A05 prioritaire ; déchiffrement réussi
sans ancien mandat/droit/ancrage réactivé ou second signataire racine actif.
Perte/corruption sans compromission suspectée : état dégradé diagnostiqué,
remplacement sous mandat et qualification, sans récupération/signature automatique
ou révocation collective par seul nombre d'exemplaires. Suspicion/compromission
A05/A10i21, exemplaires intacts sans clé déclarée saine automatiquement.
Tous moyens perdus/inadmissibles : récupération impossible, pas de repli par
phrase secrète ou validité prolongée ; procédure exceptionnelle à définir.
Retrait/destruction sous contrôle lorsque moyens inutilisables pour l'usage,
audit public distinct. Cadence d'essai isolé et réfection des moyens à arbitrer.

A validée pour redondance avec deux supports à protéger et qualifier.
Pas de charge cryptographique courante de sauvegarde racine ajoutée aux PA/PBO ;
stockage, effort, délais et ressources de cérémonie à qualifier sur Linux/Windows
physiques/VM, Docker/LXC Proxmox sans privilège ou matériel implicitement imposé.
Le [NIST SP 800-57 partie 1, section B.3.5](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf)
traite la récupération des clés de protection ; nombre/placement validés
comme choix Pixs, sans obligation universelle ou conformité déduite. Recette : moyen
isolé avec autres absents, dépendance unique indisponible, perte/corruption,
génération erronée, profil non exportable, chaîne circulaire, clé retirée/
compromise et absence de droits réactivés. A10i26 A validé le 7 octobre 2026.

##### Application au PA — A10i26

Premier jet validé clé commune A10i25/aléatoire A10i24/deux sauvegardes racine A10i23.
A10i22 B : une personne habilitée suffit par opération, sans quorum/personnes
supplémentaires. Nombre par clé de protection admissible, support principal
et copies privées racine exclus.

| Choix validé | Moyens complets de récupération de la clé commune | Organisation |
| --- | --- | --- |
| A | Deux moyens protégés hors ligne | Chacun utilisable sans l'autre, supports et lieux distincts |

Moyen complet : exemplaire/dispositif protégé restituant même clé dans périmètre
qualifié, métadonnées/format/provider/outil et accès disponibles ou récupérables
selon plan. Objet sans déprotection, fragment nécessitant autres exemplaires,
duplicata dépendant d'un dispositif unique irremplaçable insuffisants. Chaque
moyen évalué sans l'autre, ni partage de secret ou second opérateur imposés.
Supports/lieux distincts, garde séparée copies racine/principal, confidentialité/
intégrité/accès qualifiés. Risques communs physiques/stockage/provider/format/
authentifiants/personnes déclarés ; fichiers/VM même stockage sans séparation
physique qualifiée insuffisants. Lieux selon garde qualifiée, distance/bâtiments
non choisis, plan/domaines de panne vérifiés. Second moyen si premier perdu,
sans tolérance universelle aux risques communs/sinistres garantie.
Plan fini de récupération avec toutes dépendances/dispositifs/authentifiants/
procédures, aucune chaîne circulaire/auto-déprotection ou sauvegarde de clés
indéfinie. Aucune clé racine/protection en clair dans fichier/journal/dépôt/
PostgreSQL/image/snapshot/processus PBO/PZT/PA ou avec copie racine. Profil non
exportable respecté, duplication compatible qualifiée sans extraction claire
ou profil abaissé. Algorithme/longueur/format/support/protection finale ouverts ;
chiffrement AES-256-GCM des sauvegardes racine validé en A10i27.
Références/générations/moyens/preuves sans secret, admissibilité/intégrité/
possession/contexte A10i21/A10i22 contrôlés ; Django/A07/A12 pour effets PZT,
A05 prioritaire. Déchiffrement sans ancien mandat/droit/ancrage réactivé ou
signataire racine supplémentaire. Perte/corruption sans suspicion : dégradation
suivie, remplacement autorisé/qualifié sans récupération/signature automatique
ou révocation collective par nombre. Compromission : A05/A10i21, copie intacte
sans clé déclarée saine. Tous moyens absents/inadmissibles : reprise impossible
sans phrase secrète/validité prolongée, procédure exceptionnelle à définir.
Retrait/destruction contrôlés des moyens inutilisables pour usage, audit public
distinct, cadence d'essai isolé/réfection ouvertes.
A validée pour redondance avec deux supports à protéger/qualifier. Pas de charge courante de sauvegarde racine PA/PBO,
stockage/effort/délais/ressources qualifiés Linux/Windows physiques/VM, Docker/LXC
Proxmox sans privilège/matériel imposés. NIST SP 800-57 B.3.5 référencé cadrage PZT
pour récupération, nombre/placement validés comme choix Pixs sans obligation/conformité déduite.
Recette : moyen seul/autres absents, dépendance unique perdue, perte/corruption,
génération/profil non exportable/chaîne circulaire/retrait/compromission,
aucun droit réactivé. A10i26 A validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i26

- **WHEN** un profil revendique le traitement A10i26 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--b52a2fbee0

Source : `openspec/specs/pzt/spec.md`, ligne 6479. SHA-256 du bloc : `6e485c39daf3c3d071df2003cea90ebc7a348bb216b1e49b017b08910d741e03`.

~~~~text
### Requirement: Contrat A10i27 — Chiffrement des sauvegardes privées racine — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i27 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i27

Deux objets de sauvegarde privée racine A10i21/A10i23, clé commune dédiée
par génération/périmètre A10i25, origine aléatoire indépendante A10i24,
contrôle individuel A10i22 B et deux moyens complets A10i26 conservés.
Protection finale de ces moyens, garde, format/provider et outillage restent
à préciser séparément. Choix TLS PBO A10h distinct, WireGuard inchangé.

| Choix validé | Protection des deux sauvegardes racine | Exigence propre au mode |
| --- | --- | --- |
| A | AES-256-GCM, tag de 128 bits | Nonce de 96 bits unique par chiffrement sous la clé commune, métadonnées authentifiées |

Chiffrement authentifié AES-256-GCM, clé commune de 256 bits, tag entier
128 bits et nonce/IV 96 bits. AAD publiques liées aux références attendues
de domaine/racine/génération/copie/protection/profil/format ; encodage exact
et versionné à définir, sans secret dans les AAD. Chaque nouveau chiffrement
respecte l'unicité du nonce sous la clé commune : seconde copie, remplacement,
tentative, clone/restauration et changement d'outil compris. Production/réservation et coordination hors ligne validées en A10i28 ;
preuve contre retour arrière soumise en A10i29, limites d'invocations et
qualification requises avant activation ; compteur remis à zéro ou aléa cloné insuffisants.
Unicité incertaine : chiffrement refusé sans nonce présumé neuf ou repli.
Reproduction bit à bit d'un objet déjà scellé sans nouvelle invocation,
identité/version conservées ; modification d'AAD exige un nouveau scellement.
AES-256-KWP non retenu, aucun mode alternatif sélectionné automatiquement.

Primitive standard via provider/bibliothèque qualifiés, sans primitive propre
ou dépendance installée ici. Taille, encodage/version et profil contrôlés,
intégrité vérifiée avant utilisation de la clé récupérée. Échec, troncature,
mauvaise clé, contexte/identité/état invérifiables : refus sans clair utilisable,
repli ou droit/ancrage réactivé. Rejeu d'un objet ancien authentique contrôlé
par état/génération/validités courants A10i21/A05 ; authenticité sans fraîcheur
ou autorisation présumées. Déprotection dans le périmètre racine qualifié,
sans secret en clair dans fichier/journal/dépôt/PostgreSQL/image/snapshot
applicatif ou processus courants PBO/PZT/PA. Profil non exportable respecté,
provider incompatible bloquant sans extraction en clair ou abaissement.
Compromission selon A05/A10i21, re-chiffrement sans confiance racine rétablie.

Aucune garantie de sécurité sur 7300 jours A10i17 ; cryptopériodes/reprotection
à qualifier sans âge/validité réinitialisés. PBO suit références publiques,
Django/A07/A12 gouverne mandats/effets, A05 reste prioritaire. Qualification
Linux/Windows physiques/VM, Docker/LXC Proxmox ; aucune charge cryptographique
courante de sauvegarde racine ajoutée aux PA/PBO, aucun matériel/privilège
implicitement imposé. Ressources/délais de cérémonie à mesurer.
A validée pour authentification directe des métadonnées et tag entier de
128 bits, sous unicité qualifiée des nonces, sans classement universel des coûts.
Référence : [NIST SP 800-38D, sections 5 et 8](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf),
profil Pixs validé sans conformité déclarée. Recette prévue : tag/nonce/AAD
altérés, restauration/réutilisation/deux outils, copie ou re-chiffrement,
mauvais contexte/rejeu/provider incompatible/expiration/retrait et absence
de secret ou droit réactivé. A10i27 A validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i27

- **WHEN** un profil revendique le traitement A10i27 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--52ddc3cd15

Source : `openspec/specs/pzt/spec.md`, ligne 6544. SHA-256 du bloc : `d73083a6edb494a20b13e4d3829259d56ada1906cd8ff17e9c7273ee2d22caf3`.

~~~~text
### Requirement: Contrat A10i28 — Production déterministe des nonces de sauvegarde racine — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i28 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i28

AES-256-GCM/tag 128 bits/nonce 96 bits validé A10i27 ; clé commune dédiée
A10i25, contrôle individuel A10i22 B et deux moyens A10i26 conservés.
Construction déterministe retenue pour toute la vie de cette clé, sans mélange
avec tirage aléatoire ni bascule automatique. Provider, mécanisme de preuve
contre retour arrière, format exact et limites opérationnelles à qualifier.

| Choix validé | Production des nonces de 96 bits | Condition principale |
| --- | --- | --- |
| A | Préfixe fixe de 32 bits et compteur de 64 bits | Allocation unique hors ligne, réservation durable et preuve contre le retour arrière |

Un allocateur logique hors ligne par clé commune ; préfixe fixe lié au contexte,
disposition immuable pendant la vie de cette clé. Tous outils et moyens de
récupération utilisent la même séquence qualifiée, sans compteurs locaux
indépendants. Réservation exclusive/durable avant chiffrement ; nonce réservé
abandonné, crash ou résultat incertain jamais réattribués. Compteur croissant
sans débordement/remise à zéro ; maximum opérationnel à définir, sans assimiler
la capacité de 64 bits à une cryptopériode autorisée. Copies, remplacements et
nouvelles tentatives comptés ; copie bit à bit d'un objet scellé sans nouvelle
invocation, identité/version conservées selon A10i27.

Authenticité d'un journal sauvegardé ne prouve pas qu'il est le plus récent.
Preuve de progression indépendante des états susceptibles d'être restaurés
requise, témoin indépendant validé en A10i29. Journal, référence et réservations
réconciliés avant reprise ; identité restaurée, nouvel outil ou moyen A10i26
ne recréent pas une séquence neuve. Sans preuve suffisante, nouveau chiffrement
bloqué ; récupération/déchiffrement des objets existants possible seulement
sous contrôles A10i21/A10i27. Perte de l'état d'allocation distincte de perte
de clé : pas de rotation, compteur neuf ou sauvegarde implicitement autorisés.
Deux moyens A10i26 n'autorisent pas deux allocateurs concurrents.

Mandats/contrôles courants, Django/A07/A12 et A05 conservés. Références
publiques sans secret dans journaux/PBO/PA ; leur présence ne prouve pas la
progression courante. Protection finale des moyens de récupération distincte.
A validée pour rendre l'allocation vérifiable sous preuve de progression
qualifiée ; aucun gain universel sécurité/performance, aucune charge courante
PA/PBO ou matériel/privilège implicitement imposés. Qualification Linux/Windows
physiques/VM et Docker/LXC Proxmox dans le périmètre racine.
Référence : [NIST SP 800-38D, sections 8.2.1, 8.3 et 9](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf),
construction déterministe et continuité des IV, profil Pixs validé sans conformité
déclarée. Recette : concurrence/deux outils, crash avant/après réservation,
journal ancien authentique, clone/restauration, récupération par chaque moyen
A10i26, limite atteinte/état inconnu, aucun nonce/droit réutilisé implicitement.
A10i28 A validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i28

- **WHEN** un profil revendique le traitement A10i28 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

