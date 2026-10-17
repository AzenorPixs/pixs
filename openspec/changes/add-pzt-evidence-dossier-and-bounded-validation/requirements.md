# Références normatives — Z15

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pzt / 6997 | [Contrat A10i35 — Dossier de preuve lié au reçu signé de clôture — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L6997) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 7066 | [Contrat A10i36 — Empreinte documentaire SHA-384 entière — option B validée le 7 octobre 2026](../../specs/pzt/spec.md#L7066) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 7135 | [Contrat A10i37 — Empreinte SHA-384 encodée Base64url sans remplissage — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L7135) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 7196 | [Contrat A10i38 — Dossier JSON avec manifeste de pièces séparées — option A validée le 7 octobre 2026](../../specs/pzt/spec.md#L7196) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 7268 | [Contrat A10i39 — Plafonds configurables de validation du dossier de preuve — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L7268) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |
| pzt / 7341 | [Contrat A10i40 — Budgets séquentiels de validation automatique du dossier — option A validée le 8 octobre 2026](../../specs/pzt/spec.md#L7341) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pzt--0fe01f12e2

Source : `openspec/specs/pzt/spec.md`, ligne 6997. SHA-256 du bloc : `5dcec3c6b163309f82bb2df0b0dc02935d9be8b21227d8c1e7b24efaba683c10`.

~~~~text
### Requirement: Contrat A10i35 — Dossier de preuve lié au reçu signé de clôture — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i35 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i35

Assainissement A10i33/A10i34 et transition A10i32 maintenus. Dossier lié au
reçu signé de clôture retenu, sans preuve absolue de disparition d'un secret.
Décisions/permissions A12 et contrôles courants conservés ; A10i22 B sans
second approbateur humain. Empreinte SHA-384 validée A10i36 B.

| Choix validé | Preuve documentaire | Vérification du dossier |
| --- | --- | --- |
| A | Dossier structuré/versionné lié par empreinte à un reçu de clôture signé A12 | Intégrité du dossier exporté vérifiable, preuves techniques et validation toujours nécessaires |

Dossier par opération/cible ou ensemble explicite avec résultat par
cible ; mandat/transition/générations/supports, profil/méthode, outils/providers/
versions, dates, exécutant/validateur par références d'identité, résultats,
erreurs/limites, évaluation d'efficacité et décision explicite. Garde/couverture
des exemplaires/moyens et protection du profil courant documentées. Données
minimales sans clé, jeton, authentifiant, ancien clair ou diagnostic brut sensible.
Une personne habilitée peut exécuter et valider A10i22 B, validations technique/
métier distinctes sans second humain déduit des champs. Résultat positif seul
insuffisant : profil/couverture/efficacité évalués avant clôture. Cible perdue/
partielle/invérifiable ou risque non traité sans assainissement déclaré par
signature administrative ; résultats négatifs conservés, retrait non clôturé,
A05/A10i21 et Django/A07/A12 maintenus.

Empreinte des octets exacts du dossier versionné et références des pièces
publiques couvertes ; SHA-384 A10i36 B et Base64url A10i37 A validés. Reçu JWS compact
A12d, signature opérationnelle Ed25519 A12e B par signataire habilité A12c/A12f
après décision durable A12a/A12b. Type/usage de clôture distinct des permissions,
époque/version/mandat/cibles/engagement liés ; aucune signature par clé racine,
de sauvegarde ou WireGuard. Signature protège la liaison au dossier, sans
preuve cryptographique d'effacement, de véracité ou de commit PostgreSQL public.
Signataire compromis/mensonger selon limites A12c. Export vérifié avec confiance
admissible et dossier exact ; altération/pièce absente/contexte erroné refusés.
Lecture historique sans nouvelle autorisation, fraîcheur ou conformité présumées.
Constat idempotent lié à opération/version/empreinte ; émission échouée après
engagement réconciliée sans nouvelle destruction/décision. Clôture sans reçu
admissible non déclarée achevée ; émission/contrôle distincts de réalisation
hors ligne de la cérémonie.

A validée pour vérifier l'intégrité des exports et leur traçabilité avec
les reçus existants ; simple consultation autoritative sans liaison portable
non retenue comme preuve alternative. Schémas/tailles,
pièces/empreinte/rétention/vérification historique à qualifier. Preuve absente ou
état courant inconnu bloque la clôture sans repli. PBO références sans clé/
signataire de clôture imposés aux PA ordinaires ; charge par cérémonie à mesurer
sur Linux/Windows physiques/VM, Docker/LXC Proxmox et contrôle, sans gain CPU/RAM
ou coût nul promis.
[NIST SP 800-88 révision 2, sections 4.5 et 4.6](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-88r2.pdf)
pour assurance/documentation ; liaison JWS Pixs validée sans obligation NIST
de signature cryptographique ou certification déclarée. Recette : efficacité
rejetée malgré résultat positif, dossier/pièce altérés ou absents, mauvais mandat/
génération, reçu/signataire invalide, engagement incertain, rejeu et cible perdue,
aucune destruction ou droit réactivés.
A10i35 A validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i35

- **WHEN** un profil revendique le traitement A10i35 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--13b0829ae5

Source : `openspec/specs/pzt/spec.md`, ligne 7066. SHA-256 du bloc : `ef7cd5e4effe143106edc37e567f0f7e36a3d0829667376f1aa7ee4c66fd27dc`.

~~~~text
### Requirement: Contrat A10i36 — Empreinte documentaire SHA-384 entière — option B validée le 7 octobre 2026

Le rôle chargé du traitement A10i36 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i36

Dossier lié au reçu signé A10i35 A, assainissement A10i33/A10i34 et reçus A12
conservés. SHA-384 entier retenu pour liaison documentaire, distinct du chiffrement
AES-256-GCM, des nonces A10i28 et de la signature opérationnelle Ed25519.
Même algorithme du profil pour empreinte du dossier et pièces publiques couvertes ;
structure/encodage de leur liaison à qualifier, aucun hash secret publié.

| Choix validé | Empreinte | Taille du résultat brut |
| --- | --- | --- |
| B | SHA-384 entier | 384 bits, soit 48 octets |

Octets exacts de la version figée du dossier et des
pièces couvertes hachés, sans troncature, réencodage ou normalisation implicites.
Schéma d'entrée/manifestes et référence par pièce à préciser, représentation
textuelle Base64url validée A10i37 A ; digest entier de 48 octets, sans repli SHA-256 ; concaténation ambiguë de plusieurs pièces sans structure refusée.
Références de type/usage/version, opération, racine/protection et pièces couvertes
liées au reçu ; nom/URL d'une pièce sans intégrité de son contenu suffisante.
Dossier comme pièce publics au sens absence de secret, accès et confidentialité
documentaire conservés ; analyse bornée, contenu admissible vérifié sans publier
empreinte de clés, authentifiants ou données privées pour les reconnaître.

Algorithme fixé par profil/version approuvés, identifiant et empreinte liés au
reçu signé ; digest absent/tronqué, mauvais algorithme/longueur, pièce manquante,
contexte ou version incohérents refusés. Algorithme reçu dans un message sans
sélection d'un profil ou confiance automatique ; aucun repli SHA-1/MD5 ou
algorithme différent après échec. Bibliothèque/provider standard qualifiés,
aucune primitive maison ou dépendance installée ici. Encodage exact du digest,
limites de volume et qualification sur toutes cibles restent ouverts.

Empreinte seule sans authenticité : A12d/A12e B lie le dossier à un reçu JWS
signé par signataire habilité, contrôles A12c/A12f et engagement courant maintenus.
L'algorithme du digest ne remplace pas la signature, n'introduit pas Ed25519ph
et ne modifie pas le calcul interne d'Ed25519. Hash/signature concordants sans
preuve d'efficacité de l'assainissement ni véracité absolue du dossier A10i35.
Altération/version/pièce refusées sans nouveau droit ou clôture réactivée.
Restauration/réédition sans remise à zéro des mandats, âges, nonces ou dates ;
algorithme de liaison sans modification des signatures CA/TLS, WireGuard,
protection des sauvegardes, ancrage matériel ou preuve TPM.

B validée pour SHA-384 entier et son résultat de 48 octets, sans sécurité du
système entièrement portée à 384 bits ou garantie de conservation longue.
CPU/RAM/délais dépendent bibliothèque/matériel/tailles, à mesurer sans classement
universel ; Base64url sans remplissage validé A10i37 A, coûts à qualifier, aucun
chiffre de débit présumé. SHA-256 reste propre aux autres usages validés, sans
substitution automatique à l'empreinte documentaire.
PBO suit références et reçus, pas de hachage de dossier courant imposé aux PA
ordinaires ; Linux/Windows physiques/VM et Docker/LXC Proxmox qualifiés.
[FIPS 180-4, figure 1 et sections 6.2/6.5](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf)
définit SHA-384 et taille ; choix Pixs validé sans certification ou
conformité déclarée. Recette : vecteurs standard, altération d'un octet, réencodage,
dossier équivalent avec octets différents, mauvaise longueur/algorithme/type,
pièce remplacée/absente et aucun secret ou droit réactivé.
A10i36 B validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i36

- **WHEN** un profil revendique le traitement A10i36 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--b7c1c6bee0

Source : `openspec/specs/pzt/spec.md`, ligne 7135. SHA-256 du bloc : `e7863899bcaec70db8cfd25c4d457924fae922df5f728f5144ece1f63cb3c487`.

~~~~text
### Requirement: Contrat A10i37 — Empreinte SHA-384 encodée Base64url sans remplissage — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i37 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i37

SHA-384 entier/48 octets validé A10i36 B, dossier/reçu A10i35 A et signature
JWS/Ed25519 A12 conservés. Base64url sans remplissage retenu pour empreintes
du dossier et pièces couvertes, sans nouvel algorithme cryptographique.

| Choix validé | Représentation | Taille pour 48 octets SHA-384 |
| --- | --- | --- |
| A | Base64url sans remplissage | 64 caractères ASCII |

Alphabet Base64url de RFC 4648 section 5, lettres majuscules/minuscules,
chiffres, tiret et soulignement ; aucun remplissage « = », espace ou saut de
ligne. 48 octets forment 16 groupes complets de trois octets, donc 64 caractères
sans remplissage. Encodage sensible à la casse, sans remplacement « + »/« / »
du Base64 classique ni conversion automatique d'un autre alphabet.
Format fixé par profil/version approuvés pour les empreintes couvertes ;
algorithme SHA-384, format et valeur liés au reçu signé, pas de détection
heuristique hex/Base64 ni format choisi depuis un message non fiable.
Chaîne/longueur/alphabet contrôlés, décodage strict en exactement 48 octets,
égalité à l'empreinte recalculée sur les octets exacts avant constat admissible.
Forme invalide/incomplète, format/algorithme incompatibles ou digest différent :
refus sans troncature, normalisation permissive, repli ou réédition automatique.
Bibliothèque standard qualifiée, limites de volume et schémas à préciser ;
structure dossier/manifeste/pièces séparées validée A10i38 ; autres champs à qualifier.

Représentation du digest dans le contenu JSON distincte de l'encodage extérieur
JWS compact A12d ; signature vérifiée sur ses octets reçus, sans réencodage du
payload pour vérifier. Aucun Ed25519ph, changement de SHA-384, nonce GCM,
clé/permission/ancrage modifiés ; encodage réversible sans chiffrement, secret
ou authenticité ajoutés. Affichage dérivé éventuel sans remplacement de la
forme protégée utilisée par le protocole. A10i22 B, A05 et contrôles A12 maintenus,
dossier valide sans efficacité d'assainissement automatiquement démontrée.

A validée pour compacité et cohérence avec Base64url de JWS ; aucun encodage
hexadécimal alternatif admis pour le protocole. Même digest SHA-384 conservé,
sans débit/CPU/RAM universel présumé.
Schémas/identifiants/bibliothèques à qualifier sur Linux/Windows physiques/VM,
Docker/LXC Proxmox et rôles de contrôle ; pas de charge de dossier courant
ou clé de signataire imposés aux PA ordinaires.
[RFC 4648, sections 3, 5 et 8](https://www.rfc-editor.org/rfc/rfc4648.html#section-5)
pour alphabets/contraintes, [RFC 7515, section 2](https://www.rfc-editor.org/rfc/rfc7515.html#section-2)
pour Base64url JWS ; profil Pixs validé, aucun codec installé ou conformité déclarée.
Recette : octets initiaux nuls, round-trip, mauvaise longueur/alphabet/casse,
remplissage ou séparateur interdits, empreinte tronquée, confusion avec payload
JWS et aucune clôture/permission réactivée.
A10i37 A validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i37

- **WHEN** un profil revendique le traitement A10i37 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--9276e5b403

Source : `openspec/specs/pzt/spec.md`, ligne 7196. SHA-256 du bloc : `b5ab267fba2a38e476480b6ed8dfd9f8a929afa0627d516e3f72ec66e537b04e`.

~~~~text
### Requirement: Contrat A10i38 — Dossier JSON avec manifeste de pièces séparées — option A validée le 7 octobre 2026

Le rôle chargé du traitement A10i38 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i38

Dossier/reçu signé A10i35 A, SHA-384 entier A10i36 B et empreintes Base64url
sans remplissage A10i37 A conservés. Dossier JSON/manifeste/pièces séparées
retenu ; contenu
sans secret, accès contrôlés et validation d'assainissement A10i33/A10i34 maintenus.

| Choix validé | Structure | Organisation des pièces |
| --- | --- | --- |
| A | Dossier JSON UTF-8 typé/versionné avec manifeste de pièces séparées | Chaque pièce identifiée, typée, dimensionnée et liée par empreinte SHA-384/Base64url |

Dossier figé contenant constats/décisions A10i35 et manifeste explicite.
Chaque entrée déclare identifiant unique, rôle/type, taille en octets et empreinte
SHA-384 entière/Base64url de la pièce exacte. Champs/identifiants/nombres/ordre
et contraintes à définir par schéma, sans liaison par nom/position seuls.
Pièces conservées séparément ; emplacement de transport sans autorité de
confiance, nom/URL sans remplacement du contenu attendu. Identifiant de pièce
et digest liés au contexte ; même contenu dans des rôles distincts seulement
par entrées explicitement distinctes, duplications d'identifiant refusées.
Déplacement des pièces possible sans modifier le dossier figé si toutes
références et octets attendus sont conservés. Export valide seulement avec
dossier, reçu et pièces requises, aucune preuve complète déclarée sur manifeste
seul. Conteneur de transport/noms de fichiers et rétention à arbitrer.

Octets JSON UTF-8 figés avant calcul de l'empreinte du dossier.
Reçu de clôture extérieur au dossier qu'il référence ; aucune auto-référence
de sa propre empreinte ni inclusion circulaire du reçu. Empreinte du dossier
couvre manifeste et références des pièces ; chaque contenu couvert contrôlé
séparément. A12d/A12e B signe le reçu sur octets reçus, sans réencodage JSON
pour vérifier ; dossier JSON sémantiquement équivalent avec octets différents
sans empreinte présumée identique. Correction/changement de pièce ou manifeste
requiert nouvelle version et décision autorisées, sans nouvelle destruction
automatiquement exécutée ou ancien constat effacé.

Analyse typée/versionnée et bornée ; doublons de clés JSON, version/type inconnus
ou champs obligatoires ambigus refusés. Plafonds de nombre/taille/volume/
profondeur validés A10i39 A, compatibilités à qualifier avant activation. Pièce requise
manquante, altérée, substituée, taille/digest/contexte invalides : refus du constat
complet, preuves négatives conservées. Référence de localisation sans lecture
ou téléchargement automatique arbitraires, contenu de preuve sans commande
exécutable ou configuration à appliquer. Pièce publique au sens absence de
secret, sans publication internet ou droit d'accès implicitement accordés.
A10i22 B, Django/A07/A12, état d'engagement réconcilié, A05 et contrôles courants
maintenus ; intégrité/export sans efficacité d'assainissement présumée.

A validée pour traiter les pièces séparément et limiter la taille du dossier
central ; contenus intégrés au dossier non retenus comme structure alternative.
CPU/RAM/stockage/transport à mesurer selon tailles,
sans performance universelle ni charge de preuve courante imposée aux PA.
Linux/Windows physiques/VM, Docker/LXC Proxmox qualifiés, aucune dépendance,
bibliothèque ou écriture de dossier de preuve réel effectuées ici.
[RFC 8259, sections 4 et 8.1](https://www.rfc-editor.org/rfc/rfc8259.html#section-8.1)
pour JSON/UTF-8 ; manifeste et architecture Pixs validés sans prescription
de la RFC ou conformité déclarée. Recette : pièce manquante/substituée, taille
fausse, identifiant dupliqué, Unicode invalide, réencodage, référence circulaire,
volume dépassé et aucune commande, destruction ou permission déclenchée.
A10i38 A validé le 7 octobre 2026.

#### Scenario: Conformité du traitement A10i38

- **WHEN** un profil revendique le traitement A10i38 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--b34367d9ac

Source : `openspec/specs/pzt/spec.md`, ligne 7268. SHA-256 du bloc : `0c86affdffde26871348ca2cbd6d245e8b315970012c711432952a48235763a2`.

~~~~text
### Requirement: Contrat A10i39 — Plafonds configurables de validation du dossier de preuve — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i39 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i39

Dossier JSON/manifeste/pièces séparées A10i38 A, reçu A10i35 A, SHA-384 A10i36 B
et Base64url A10i37 A conservés. Premier jet de plafonds configurables validé,
à qualifier sans mesure de charge réelle, seuil de performance ou activation ici.

| Choix validé | Dossier JSON UTF-8 | Pièces au maximum | Taille par pièce | Total dossier et pièces | Profondeur JSON |
| --- | --- | --- | --- | --- | --- |
| A | 1 Mio | 64 | 16 Mio | 128 Mio | 16 |

1 Mio = 1 048 576 octets. Plafonds inclusifs, applicables simultanément :
nombre et plafond individuel ne permettent pas de dépasser le plafond cumulé.
Total : octets exacts du dossier plus somme des tailles des pièces couvertes,
comptées par entrée de manifeste, même contenu dans plusieurs rôles inclus.
Reçu extérieur soumis aux limites A12 propres, sans taille illimitée admise.
Profondeur : objet/tableau racine au niveau 1, chaque conteneur imbriqué ajoute
un niveau ; valeurs scalaires n'ajoutent pas de niveau. Schéma/contraintes
métier peuvent être plus stricts ; plafond sans obligation de produire tant
de pièces ou de rendre admissible tout document syntaxiquement valide.

JSON contrôlé en taille avant analyse autant que possible ; longueur déclarée
sans confiance, octets réellement reçus/traités comptés. Prévalidation bornée
du manifeste, somme entière contrôlée sans débordement, profondeur surveillée
pendant analyse. Taille de chaque pièce vérifiée sur octets exacts ; hachage
par flux bornés, une pièce à la fois, sans chargement obligatoire de
tout le dossier et des pièces en RAM. Budgets buffers/temps/concurrence validés
A10i40 A, I/O et exécution à qualifier ; plafond de 128 Mio sans autant de RAM
requis ou mémoire réelle plafonnée par simple taille de fichier présumés.
Transport/conteneur/compression à définir séparément ; limites sur contenus
originaux, pas seulement taille comprimée, aucun codec ou archive adopté ici.
Prévalidation de taille sans signature/empreinte/vérification des pièces omises.

Dépassement, taille inconnue/incohérente ou quantité invalide : traitement arrêté
et constat complet refusé, diagnostic sans secret. Aucune troncature, pièce
obligatoire abandonnée, réencodage ou clôture partielle présentée complète pour
tenir dans les plafonds. Dossier légitime trop grand : réduction autorisée de
la préparation avant scellement ou révision explicite du profil après analyse
des besoins, jamais modification d'un dossier figé sans version/autorisation.
Aucun retrait/droit de communiquer/racine réactivés par erreur documentaire.

Configuration explicite validée/versionnée, administrée via PBO/Django/A07/A12 ;
valeurs finies et compatibilité des vérificateurs qualifiées avant application,
sans plafond relevé automatiquement depuis une entrée, un reçu ou une charge.
Aucun nom de variable, schéma concret, fichier de configuration ou écriture
OpenSpec adoptés ici. Historique selon profil compatible autorisé, pas de retrait
rétroactif de constat par seul changement de limite ; version reçue sans autorité
pour relever budgets locaux. A05 et A10i22 B maintenus.
A validée comme premier jet sobre, valeurs Pixs configurables et à mesurer,
sans charge métier observée justifiant ces nombres ni sécurité/performance
universellement supérieure. Linux/Windows physiques/VM, Docker/LXC Proxmox et
contrôle qualifiés, aucune validation de dossier courante imposée aux PA ordinaires.
[RFC 8259, section 9](https://www.rfc-editor.org/rfc/rfc8259.html#section-9)
autorise des limites d'analyse JSON ; valeurs et stratégie validées par Pixs,
sans prescription RFC ou garantie CPU/RAM/délais. Recette : limite exacte et
plus un, somme dépassée sous plafonds individuels, mêmes contenus multi-rôles,
taille déclarée fausse, JSON trop profond, flux interrompu, pièce requise omise,
ancien profil/valeur reçue non autorisés et refus sans secret/droit réactivé.
A10i39 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i39

- **WHEN** un profil revendique le traitement A10i39 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

### Référence pzt--33a0c4091a

Source : `openspec/specs/pzt/spec.md`, ligne 7341. SHA-256 du bloc : `48dacdde2b1d465b13334dc27a9f7d10965a5b9954237a5a117748642caa4d81`.

~~~~text
### Requirement: Contrat A10i40 — Budgets séquentiels de validation automatique du dossier — option A validée le 8 octobre 2026

Le rôle chargé du traitement A10i40 MUST satisfaire les clauses opératoires,
bornes et conditions du contrat détaillé ci-dessous. Il MUST NOT appliquer
une alternative rejetée, élargir son périmètre ou présenter comme effectué
un contrôle/effet absent. Les règles de lecture normative précédentes,
les contrats structurels et les exceptions applicatives restent applicables.

##### Contrat détaillé A10i40

Plafonds A10i39 A, dossier/manifeste A10i38 A, reçus A10i35 A et empreintes
A10i36 B/A10i37 A conservés. Budgets validés pour validation automatique après
mise à disposition des entrées requises, distincts de durée de cérémonie humaine,
transport des supports, récupération de clé et assainissement matériel.
Valeurs configurables de premier jet validées, à qualifier sans mesure ou activation ici.

| Choix validé | Dossiers actifs par instance de validation | Tampon de lecture par pièce active | Lecture/hachage par pièce | Validation automatique totale par dossier |
| --- | --- | --- | --- | --- |
| A | 1 | 256 Kio | 30 secondes | 180 secondes |

1 Kio = 1024 octets, 1 Mio = 1 048 576 octets. Une pièce lue/hachée à la fois
par dossier selon A10i39 et un dossier actif par instance ; aucune concurrence
de pièces/dossiers implicite, plafonds A10i39 conservés. Tampon de lecture en flux,
pas de plafond RAM totale déduit : parseur JSON, buffers de transport,
bibliothèque cryptographique et état courant à mesurer/budgéter séparément.
Coordination des instances et quotas agrégés d'hôte/autorité à qualifier,
réplication sans ressources infinies ou plafond global présumé.

Temps écoulé monotone pendant traitement engagé, attente I/O incluse, hors
attente humaine avant mise à disposition. Budget par pièce depuis début de
lecture jusqu'au contrôle taille/empreinte ; budget global dès admission au
traitement automatique, analyse JSON, contrôles automatiques et pièces inclus.
Plafonds simultanés, temps par pièce sans multiplication prolongeant le global.
Non-admission sans file lorsque créneau occupé validée A10i41 A ;
aucune accumulation illimitée ou admission silencieuse au-delà de concurrence.
Pauses/crash/reprise sans crédit automatiquement remis à zéro ; preuve de
budget restant et état courant requise, sinon tentative suspendue/refusée.
Nouvelle tentative seulement autorisée, sans prolonger mandat/droits/retraits ;
budgets inter-tentatives et détails de reprise à qualifier avant activation.

Dépassement, annulation ou état de temps invérifiable : traitement arrêté,
ressources libérées, échec diagnostiqué sans secret et constat complet non validé.
Aucune pièce omise, empreinte partielle validée, preuve technique assouplie ou
nouvelle destruction déclenchée pour respecter le délai. Engagement de clôture
incertain réconcilié A12 avant réexécution ; interruption de validation sans
engagement PostgreSQL déjà durable supposé annulé. Profil légitime trop lent :
révision explicite après mesure, sans prolongation automatique, borne indéfinie
ou changement des octets du dossier. A05/habilitations courantes prioritaires.

Configuration validée/versionnée PBO/Django/A07/A12 et compatibilité du profil
d'exécution vérifiées avant activation ; aucun nom de variable, fichier,
OpenSpec, ordonnanceur ou limite système modifiés ici. Validation dédiée au
rôle habilité, pas de traitement de dossier courant exigé des PA ordinaires.
Clé racine/principal/nouvelles sauvegardes, contrôles TPM et garde hors ligne
inchangés ; A10i22 B et toutes plateformes physiques/VM Linux/Windows,
Docker/LXC Proxmox maintenus sans privilège, montage ou ressource hôte ajoutés.

A validée comme premier jet sobre/séquentiel, valeurs et mémoire/CPU/I/O
à qualifier ; profil à quatre dossiers actifs non retenu comme option courante.
Aucune borne de débit, latence garantie, sécurité universellement supérieure
ou mémoire totale égale au tampon annoncées. Recette : pièce lente, plafond
global atteint sous délais par pièce, plus d'admissions que capacité, lecture
interrompue, horloge/reprise incertaines, annulation après commit, profil non
autorisé et refus sans clôture/droit ou opération destructrice réactivés.
Budgets validés par Pixs, sans valeur prescrite par un standard externe.
A10i40 A validé le 8 octobre 2026.

#### Scenario: Conformité du traitement A10i40

- **WHEN** un profil revendique le traitement A10i40 et ses garanties dans un rôle déclaré
- **THEN** ses conditions, bornes et résultats applicables sont vérifiés selon le contrat ci-dessus
- **AND** toute valeur non décidée, preuve indisponible ou qualification manquante est signalée sans garantie inventée
~~~~

