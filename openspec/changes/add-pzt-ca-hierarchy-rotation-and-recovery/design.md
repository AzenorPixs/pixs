# Conception — Z12

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

PKIZT et même clé d’autorité chiffrée répliquée, droits séparés, émetteur unique et confiance d’amorçage distincte retirée après bascule vérifiée.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [pzt](../../specs/pzt/spec.md).
- [zt-pki](../../specs/zt-pki/spec.md).
- [brick-redundancy](../../specs/brick-redundancy/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Statut

CONCEPTION_DOCUMENTAIRE_DU_PROFIL_ET_DE_SON_AMORÇAGE_INITIAL. D1/D2/D3 et D4/D5/D6 sont validés par le développeur le 23 octobre 2026. La réalisation et la qualification restent distinctes. Les preuves du périmètre antérieur sont conservées ; conception et contrats sont réexaminés pour l’extension. Le développeur demande ensuite réalisation puis phase séparée de tests/validation, sans coche avant preuve.

## Contexte actuel

Les contrats PZT et leurs décisions sont spécifiés ; le README ne revendique pas de réseau livré. Les clauses de gestion PBO essentielles restent distinctes des rôles réseau activés et des auxiliaires spécialisés.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

Sources et périmètres consultés :

- [README.md](../../../README.md).
- [openspec/specs/pzt/spec.md](../../specs/pzt/spec.md).
- [TECHNICAL.md](../../../TECHNICAL.md).

## Architecture et frontières

Séparer contrôle métier PBO/Django/PostgreSQL, propriétaire réseau pzt-daemon et adapters système. Implémenter le rôle précisément désigné par les contrats sources, avec schémas fermés, versions et contrôles courants ; conserver toutes bornes, unités, conditions de reprise et alternatives rejetées. La cryptographie WireGuard n’est pas réimplémentée. Les bibliothèques de transport, sources de temps et adapters sont qualifiés, sans confiance supposée.

Périmètre propre à ce lot : A10i6–A10i20 : PKI dédiée, intermédiaires, protection des clés, secours, exclusion/bascule, algorithmes et successions racine.

## Choix déjà fixés et alternatives

Les décisions validées dans les contrats sources sont conservées, y compris formats, algorithmes, valeurs, rôles et alternatives rejetées. Elles ne sont pas rouvertes sous prétexte d’un nouveau dossier. Les plafonds d’un auxiliaire, collecteur, validateur ou travail ne deviennent pas un budget général du PA/PBO.

Les modalités concrètes encore ouvertes ne reçoivent pas de valeur de défaut inventée. Une bibliothèque, un provider ou une dépendance présent dans DEVOPS n’est ni sélectionné ni qualifié. Les références normatives complètes sont dans requirements.md ; les mentions historiques qu’elles contiennent ne décrivent pas des effets réalisés pendant cette préparation.

## Barrières de conception avant réalisation

Profils de protection des CA, topologie, mécanismes d’exclusion et procédures de récupération ; algorithmes et durées validés restent opposables.

Ces barrières n’empêchent pas la rédaction conditionnelle du dossier. Avant tout code, les choix ayant un impact réel sur sécurité, périmètre, compatibilité, exploitation ou ressources devront être soumis avec conséquences et recommandation ; pour PA/PZT, respecter TECHNICAL §45.4 et ses lots de trois arbitrages. Les paramètres déjà décidés sont à qualifier, pas à remplacer par une nouvelle décision supposée.

## Dépendances et interfaces

- [add-pbo-runtime-secret-provider](../archive/2026-10-19-add-pbo-runtime-secret-provider/proposal.md).
- [add-core-postgres-services](../archive/2026-10-20-add-core-postgres-services/proposal.md).
- [add-durable-minimized-audit](../archive/2026-10-21-add-durable-minimized-audit/proposal.md).



Les dépendances sont des contrats et preuves attendus. Un dossier créé ne signifie pas que sa dépendance est exécutée, disponible ou autorisée à démarrer. Les interfaces intermédiaires restent explicitement incomplètes tant que les obligations manquent.

## Vérification future

Bornes exactes et juste au-delà, types/champs étrangers, rôle/contexte/mandat inadmissibles, échéance/révocation, concurrence, réponse perdue, crash/reprise, état ancien et ressources réellement libérées. Mesurer seulement le traitement concerné et ne pas extrapoler ses plafonds au PA/PBO entier.

Sortie du lot : Signataire exclu avant succession ; perte traitée par nouvelles clés/recertification ; coexistence et durées bornées ; pas de confiance par snapshot.

Exercer tous les scénarios et clauses applicables des blocs sources, y compris renvois normatifs ; un scénario non applicable doit être motivé par le profil réel. Les contrôles applicatifs suivent l’exception Super Admin du canon dans son seul périmètre, sans fabriquer audit, mesure, signature ou effet absent.

## Migrations, reprise et arrêt

Aucun schéma ni état runtime modifié ici. Toute réalisation ultérieure qui persiste des données/états doit préciser propriétaire, contrat de migration, concurrence, reprise, durabilité et compensation/restauration. Aucun retour arrière destructeur, remise à zéro, arrêt de service ou changement de droits implicites.

## Limites du dossier

Pas de PASS actuel ni d’achèvement produit revendiqué. L’autorisation de préparation ne permet ni d’activer la capacité dans P0 ni d’utiliser un compte connecté, publier un artefact ou envoyer une notification réelle.

## Profil retenu pour la réalisation — 22 octobre 2026

Le développeur sélectionne Debian 13 et une protection matérielle non exportable obligatoire pour les clés CA. Aucun repli logiciel n’est permis. Chaque autorité logique habilitée dispose d’un émetteur principal et d’un secours pré-certifié, aux clés et générations indépendantes. L’exclusion retenue est un arrêt vérifié par un contrôleur extérieur au signataire, avec interdiction persistante de redémarrage ; une preuve actuelle vérifiée par Django reste requise avant bascule. La procédure racine reste hors ligne, sous mandat opérateur explicite. Les algorithmes, durées et bornes déjà validés par A10i6–A10i20 sont conservés.

Le même TPM peut porter les clés indépendantes de la première qualification : ce placement partage son hôte, son fournisseur et son domaine de panne. Il ne démontre aucune tolérance à leur perte ni indépendance de compromission. La réserve reste inactive sans mandat d’émission et engagement autoritatif courants. Une clé logicielle exportée puis scellée ne vaut pas preuve de non-exportabilité matérielle.

Le développeur autorise le fournisseur candidat tpm2-openssl 1.3.0-1, les outils tpm2-tools, tpm2-abrmd et libtss2-tcti-tabrmd0 avec leurs dépendances, uniquement dans une image Docker de test Debian 13. La base debian:stable-slim téléchargée est identifiée par sha256:a717a33469731894e77e912ea7d714e27c2dc38ee6554fd1a3102e92999cfc66. Le conteneur peut accéder au seul /dev/tpmrm0 pour des clés éphémères de test. Aucun paquet hôte, clé existante, effacement TPM, changement des hiérarchies ou NV, ni déploiement de production n’est couvert. Chaque commande et édition garde son mandat CAB unitaire.

Complément autorisé le 23 octobre 2026 : dbus-daemon=1.16.2-2 et ses dépendances sont ajoutés uniquement dans l’image Docker de test pour permettre le démarrage de tpm2-abrmd sur un bus D-Bus privé au conteneur éphémère, sans persistance. Aucun paquet ou service hôte ni socket D-Bus hôte n’est installé, démarré ou exposé. Les essais TPM2 éphémères restent à exécuter ; cet ajout ne qualifie ni les clés ni la PKI.

L’inventaire observé expose TPM 2.0 par tpm_crb ; le compte utilisateur ne peut pas ouvrir /dev/tpm0 ou /dev/tpmrm0. Le fournisseur tpm2.so est absent et OpenSSL 3.5.7 charge uniquement son fournisseur default. Docker 29.9.2 est accessible. La régénération de DEVOPS.md décrit un environnement Proxmox ; elle ne qualifie ni la protection des clés ni une plateforme matérielle. Sources techniques : [paquet Debian](https://packages.debian.org/trixie/tpm2-openssl), [documentation du fournisseur distribué](https://sources.debian.org/src/tpm2-openssl/1.3.0-1/README.md/).

La tâche 2 vérifie sélection, rôles, ressources et graphe des dépendances ; son prévol contrôle disponibilité et capacités du fournisseur sans revendiquer une PKI opérationnelle. C01/C02/C05 fournissent des fondations et preuves historiques à recouper. Le rôle CA nécessite des contrats A07/A12, le canal PZT, un contrôleur d’exclusion compétent, le registre et les décisions Django ainsi que des mandats courants : leur absence observée ne devient pas une readiness ni une intégration prouvée. Les contrats à produire, branchements et qualifications réels restent soumis aux tâches suivantes, réalisées et validées une par une.

## État du graphe et conditions de progression — 22 octobre 2026

La sélection matérielle et les prévols TPM2/P-256/fournisseur sont acquis au titre de l’environnement de test ; aucune signature CA, non-exportabilité, exclusion, succession ou intégration PZT n’est encore qualifiée. Le graphe distingue Z12 producteur CA, Z03 propriétaire A12 et Z06 propriétaire A07 ; Z03 référence lui-même Z12. C14 (add-essential-pbo-pzt-and-dns-modules) prévoit la gestion PZT/DNS, sans livrer les rôles CA ni le canal/exécutant PZT. Les noms de modules et le mécanisme de composition C07 ne constituent pas ces implémentations.

La préparation de contrats ne prouve pas l’activation du rôle. La tâche courante reste non validée tant que ses propres prérequis et contrôles ne sont pas démontrés ; aucun test ou intégration obligatoire n’est reporté pour rendre artificiellement admissible une tâche antérieure. Les phases de réalisation/activation/qualification conservent A07/A12, la politique matérielle, le contrôle courant et l’exclusion effective avant tout effet concerné. Les dépendances manquantes restent visibles et ne sont pas marquées non applicables pour débloquer le cycle.

Le retour au cycle après reprise documentaire exige les références réparées, les copies normatives inchangées, l’état des tâches exact et la validation OpenSpec stricte. La reprise du 22 octobre a été effectuée par réexamen de la seule tâche 2 au premier critère alors non prouvé. Cette tâche a depuis été validée comme sélection inactive ; la conception est reprise à la tâche 3 après les décisions du 23 octobre. Cette reprise ne crée ni rôle, ni canal, ni contrôleur et ne suffit pas à lever leurs dépendances de qualification ; aucune tâche suivante, archive ou readiness ne peut être déclarée par le seul succès documentaire.


## Choix de conception — tâche 3, rédigés le 22 octobre 2026, adoptés le 23 octobre 2026

Statut : CHOIX_ADOPTÉS le 23 octobre 2026 par validation du développeur « Tu peux poursuivre », limitée aux trois recommandations D1/D2/D3 déjà écrites, conformément à TECHNICAL §45.4. Cette adoption ne remplace pas la revue et le contrôle strict requis pour valider techniquement la tâche 3 ; sa case reste soumise à un mandat distinct. Les décisions déjà prises — Debian 13, protection matérielle non exportable sans repli, principal/secours dédiés et indépendants, arrêt extérieur vérifié avec interdiction persistante, racine hors ligne sous mandat opérateur — ne sont pas rouvertes. Aucun code CA, activation, installation hôte ou déploiement de production n’est autorisé par cette section.

### D1 — Frontière du signataire et contrôleur d’exclusion

Proposition recommandée : concevoir et qualifier sur le seul profil de test Debian 13 un signataire isolé dans un conteneur Docker et un contrôleur extérieur de confiance, seul propriétaire des chemins gérés de création, démarrage et restauration de ce signataire. Le signataire ne reçoit aucun socket Docker, pouvoir de gestion de l’hôte, ni accès aux clés du secours. Les processus et sessions capables d’utiliser une même génération sont inventoriés dans le périmètre de retrait. Le contrôleur arrête ce périmètre, constate la fin de tous ces processus/sessions et conserve un retrait durable de la génération dans le registre autoritatif Django/PostgreSQL, hors du signataire et opposable après redémarrage du contrôleur, du daemon ou de l’hôte. Django décide et détient le registre ; le contrôleur exécute les seules opérations système autorisées et consulte une autorité/version courante avant tout lancement. Une indisponibilité, une restauration ancienne du registre ou une époque non réconciliée n’autorise aucun lancement. Le contrat public de contrôle reste explicitement autorisé et toute communication PBO–PA passe par PZT, sans voie locale de secours. Il refuse tout lancement, recréation, rattachement de clé ou restauration de la génération retirée. La politique Docker de redémarrage désactivée complète cette interdiction ; elle ne la constitue pas à elle seule.

Django vérifie avant engagement du secours une preuve actuelle du contrôleur compétent, liée à la demande courante, l’identité du signataire, la clé/génération, les cibles exactes, l’opération et sa version, l’état effectivement appliqué et le maintien de l’interdiction. Les mécanismes d’identité/preuve opérationnels A12 restent distincts des clés CA. Une preuve ancienne rejouée, un simple ACK, un arrêt partiel, un contrôleur ou registre indisponible, une protection contournable ou un état contradictoire bloque la bascule. Aucun seuil de fraîcheur chiffré n’est inventé : demande, mandat et contexte courants restent opposables ; la vérification doit couvrir l’instant d’activation.

Conséquences et limites : le contrôleur et l’administration de l’hôte font partie du périmètre de confiance ; la compromission d’un administrateur hôte ou une restauration contournant ce contrôleur ne sont pas couvertes. Toute voie de redémarrage non médiatisée interdit la qualification. Principal et secours sur le TPM local partagent leur domaine de panne ; leur exclusion doit néanmoins rester séparée. Les redémarrages du daemon Docker partagé ou de l’hôte ne sont pas autorisés par ce choix : leur recette nécessitera un environnement isolé autorisé. Alternative : placer le contrôleur au niveau VM/hyperviseur avec séparation matérielle ou VM des signataires ; cela requiert d’autres ressources, droits et essais, sans garantie supplémentaire présumée.

Propriétaires proposés : service CA et adapter TPM2 sous le futur espace distinct src/pixs/pzt_ca/ ; contrôleur système extérieur au service CA ; décisions, registre courant et références publiques détenus par Django/PostgreSQL. Aucun composant de C14, A07, A12 ou contrôleur existant n’est réputé fournir ces effets. Recette : mauvaise cible/génération, clé déjà utilisable dans plusieurs sessions, arrêt partiel, réponse perdue, concurrence, arrêt et reprise du contrôleur, création/restauration d’une ancienne génération et maintien du secours ; effet et refus observés réellement avant toute qualification revendiquée.

### D2 — Profil X.509 des autorités de certification

Proposition recommandée : fixer pour ce profil une chaîne racine PZT vers intermédiaire dédié vers terminal, sans CA subordonnée à un intermédiaire. Principal et secours sont deux intermédiaires frères sous la même racine, aux clés indépendantes ; aucun ne certifie l’autre. Les certificats CA utilisent X.509 v3, ECDSA P-256 et ecdsa-with-SHA256 conformément à A10i14. BasicConstraints est critique avec CA=true ; pathLenConstraint vaut 1 pour la racine et 0 pour les intermédiaires. L’application impose également cette topologie à son ancrage explicite ; le certificat de racine ne suffit pas à imposer une politique de confiance. KeyUsage est critique et réservé à keyCertSign pour ce profil sans CRL proposé en D3. SubjectKeyIdentifier et AuthorityKeyIdentifier suivent RFC 5280 ; l’exception de racine auto-signée est explicitée au contrat. Les autres usages et extensions apportés par une demande ne sont jamais copiés automatiquement. Aucun usage TLS, WireGuard ou signature opérationnelle A12 n’est ajouté aux clés CA.

Les références d’autorité, domaine, émetteur, clé et génération sont associées explicitement à la politique courante par Django ; le nom du sujet ou d’issuer ne sélectionne aucune autorisation. Les émetteurs frères, chemins alternatifs, certifications croisées et délégations non admises sont refusés même sous la même racine. Les durées A10i16/A10i17, la validité résiduelle de la chaîne, les nouvelles paires à chaque renouvellement et l’admission terminale restent inchangées. L’outillage OpenSSL/provider TPM2 autorisé réalise les signatures de test ; la bibliothèque cryptography déjà présente peut vérifier les objets publics sans extraire de clé privée. La signature ne prouve jamais l’engagement PostgreSQL.

Conséquences : profil strict et testable, sans délégation CA supplémentaire ni interopérabilité avec une PKI externe revendiquée. Alternative : permettre une profondeur CA configurable et des extensions d’usage supplémentaires ; cela élargit la topologie et les cas de qualification et exige un profil distinct. Si la publication de CRL était choisie en D3, l’usage cRLSign et son mandat propre devraient être spécifiés avant réalisation ; OCSP n’ajoute aucun usage de signature opérationnelle à une clé CA par défaut. Recette : chaîne nominale, CA=false, KeyUsage absent/inadmissible, profondeur supplémentaire, extension critique inconnue, mauvais algorithme, émetteur frère, ancrage non provisionné, dates exactes et juste au-delà, sans autorisation déduite du seul certificat.

### D3 — Publication de l’état CA et traitement de la révocation

Proposition recommandée : pour ce premier profil privé PZT, publier les états et retraits CA par le registre autoritatif Django/PostgreSQL et les contrats publics versionnés A07/A12, sans ajouter CRL ni OCSP. Chaque état relie domaine, autorité, émetteur, clé/génération, certificat/empreinte publique, version/époque et décision courantes. Les décisions distinguent admissibilité de chaîne, permission d’émettre, retrait du signataire et admissibilité des certificats déjà émis. La vérification de chaîne X.509 reste nécessaire et ne prouve pas seule l’absence de révocation ou l’autorisation PZT. Le mécanisme public doit être réellement disponible et qualifié avant activation : aucun stub, cache de réussite, snapshot ou simple certificat ne le remplace.

La perte ou corruption impose une nouvelle paire et une recertification selon A10i9 ; le renouvellement normal et la succession racine suivent A10i15–A10i20. La cérémonie racine reste hors ligne sous mandat opérateur explicite, sans imposer un nombre d’opérateurs, un support ni un nouveau fournisseur non décidés. Le PBO suit les seuls éléments publics, étapes et décisions courantes ; jamais la clé racine. Les états de retrait/compromission connus sont appliqués suivant A05 sans grâce ; une indisponibilité suit les classes et bornes A05 déjà validées, sans prolongation de droit. L’incertitude d’émission ou de réponse impose réconciliation avant nouvelle tentative. Le changement de signataire exige une preuve d’exclusion avant engagement ; le retour à l’ancien n’est pas automatique. Les durées sont celles du canon : intermédiaires 365/240/125 jours, racine 7300/5840/1460 jours, coexistence au plus 30 jours dès l’engagement commun et chevauchement terminal individuel au plus 5 minutes.

Conséquences : la révocation dépend du mécanisme autoritatif PZT, qui doit être mis en œuvre et éprouvé avec ses dépendances ; un client X.509 générique ne peut pas déduire ces états en vérifiant seulement la chaîne. Alternative : ajouter publication CRL et/ou OCSP, avec contrats de fraîcheur, disponibilité et cérémonie racine à décider et qualifier ; ces protocoles ne remplaceraient pas les décisions PZT courantes. Recette : retrait ciblé d’un émetteur, compromission racine, état obsolète/rejoué, panne/reconnexion/clone/restauration, absence d’A07/A12, migration tardive et retrait à échéance sans résurrection de droit.

### Conditions communes et prochaine étape

L’adoption du 23 octobre 2026 permet de terminer la conception documentaire de la tâche 3 après revue et contrôle strict, puis de définir les contrats versionnés de la seule tâche 4. Elle ne rendrait disponibles ni A07/A12, ni canal PZT, ni contrôleur, ni registre et ne suffirait pas à valider le branchement réel des tâches suivantes. Chaque tâche conserve ses prérequis et contrôles propres. Le graphe circulaire Z12/Z03 est traité par contrats explicites, sans masquer l’intégration non prouvée ni étendre ce RUN à d’autres changes.

Sources : [Docker — politiques de redémarrage](https://docs.docker.com/engine/containers/start-containers-automatically/) ; [RFC 5280 §4.2.1.3](https://www.rfc-editor.org/rfc/rfc5280.html#section-4.2.1.3), [§4.2.1.9](https://www.rfc-editor.org/rfc/rfc5280.html#section-4.2.1.9) et [§5](https://www.rfc-editor.org/rfc/rfc5280.html#section-5). Le registre PZT proposé en D3 est un choix Pixs ; il n’est pas fourni par la RFC.

## Amorçage PKI initial avant PostgreSQL — D4/D5/D6 adoptés le 23 octobre 2026

### D4 — Cérémonie locale isolée sous mandat opérateur

La première installation crée localement la confiance PKI/PZT nécessaire au parcours PA système/PZT/PBO de préparation PostgreSQL, sans autre Pixs, PKI opérationnelle ou lot PZT préémis ailleurs. Z12 possède la cérémonie et son état initial ; C08 consomme ses ports et orchestre le parcours. L’opérateur et la provenance du lanceur sont effectivement vérifiés sous une politique d’installation protégée/versionnée indépendante de la base cible, avec mandat lié à l’installation, la cible, les exécutants, le plan/digest et l’opération. UID 0, proximité, premier PBO, booléen client, certificat ou fichier présent ne suffisent pas. Le contexte reste PLATFORM sans tenant_id ni scope_id.

Pour Debian 13, la preuve native UID/unité/manager observée et le chargement strict de politique depuis la composition de confiance sont des motifs techniques disponibles dans C01. Ils ne sont ni une autorité PKI déjà livrée ni une permission d’élargir ses actions resolve/rotate/revoke. Une politique propriétaire Z12 et la preuve positive du lancement opérateur restent à définir et qualifier. C01 et R01, ses preuves Ed25519 et sa fenêtre de dix minutes conservent leurs usages distincts.

Les clés CA restent matérielles non exportables sans repli ; hiérarchie, ECDSA P-256/SHA-256, usages, principal/secours indépendants et bornes canoniques sont conservés. La racine n’est employée que dans la cérémonie sous mandat opérateur et reste hors des processus courants. Le PA ordinaire et le PBO ne reçoivent aucune clé CA. La branche initiale n’autorise ni renouvellement/bascule/gestion ordinaires ni effet Core/Auth, droit métier ou exception Super Admin.

### D5 — Ancrage TPM NV dédié contre la restauration

Un ancrage monotone TPM NV dédié est retenu à concevoir et qualifier, hors du domaine de restauration du journal logiciel, lié à l’installation, la cible matérielle et l’étape fencée. Il doit être protégé contre l’effacement, la réinitialisation et l’accès non autorisé des signataires. Un fichier local restaurable seul ne remplace pas cet ancrage. La preuve de clôture reste durable et irréversible ; une absence, une ancienne valeur, un clone ou une protection invérifiable ferme l’admission sans réinitialisation automatique.

Aucun index, attribut, politique de commande, mécanisme d’authentification NV ou valeur d’exploitation n’est implicitement adopté. Les cinq handles publics inventoriés sur le TPM de développement ne sont pas des ressources attribuées à Z12 : aucun contenu lu ni index existant utilisé. Cette décision documentaire n’autorise aucune écriture NV, aucun clear, changement de hiérarchie ou handle persistant sur l’hôte courant. Un plan exact et une autorisation distincte précèdent toute recette NV. Les propriétés de protection, concurrence, durabilité et reprise doivent être éprouvées avant activation.

### D6 — Adoption publique, retrait initial puis admission ordinaire

Les ports documentaires et leur état sont définis au §12 de contracts.md. La préparation et les effets sont journalisés sous la même identité d’opération et le plan courant ; réponse perdue ou effet incertain impose inspection et réconciliation, sans seconde création aveugle. Un état PREPARED n’est pas une preuve d’effet. Ni la signature CA ni un résultat structurel ne prouvent un engagement PostgreSQL.

Après disponibilité des propriétaires PKI/Core/Auth/C05 et de PostgreSQL, les références publiques, octets et résultats initiaux sont adoptés et relus indépendamment sous autorité courante. Aucun matériau privé ni credential PG n’est placé dans ce transfert. La création locale, l’adoption transactionnelle PG, le retrait de l’autorité/canal/mandats initiaux et l’admission ordinaire sont prouvés séparément : aucune transaction atomique entre système/TPM et PostgreSQL n’est supposée. Toute étape partielle reste inspectable et non prête.

Le contrôleur compétent retire irréversiblement les capacités et voies d’administration initiales, leurs mandats et sessions privilégiées ; sa preuve actuelle et l’ancrage de clôture sont vérifiés indépendamment avant admission ordinaire Django/A07/A12. Les références publiques adoptables ne sont pas remplacées par principe ; âges de clés, validités, retrait connu, révocation et rotations canoniques ne sont pas remis à zéro. Une panne de PostgreSQL après passage ne peut rouvrir la cérémonie. Le graphe ordinaire Z12/Z03/Z06 reste à réaliser et qualifier, il n’est pas résolu par la seule PKI initiale.

### Critères et limites de preuve

Deux exigences et quatre scénarios des deltas pzt/authorization ajoutent la seule exception initiale explicite A10i6/A12a. Les textes et renvois canoniques antérieurs sont préservés. Le contrat exige paramètres réels de politique, validité/fraîcheur, audit/budgets, identité native, plan et ancrage sans valeur inventée ; chaque absence bloque l’effet concerné. Les fixtures d’une journée et les 53 unités historiques n’établissent pas ces paramètres. L’essai éphémère TPM2 réussi prouve génération/signature/autovérification de test et nettoyage, pas protection NV, non-exportabilité globale, bootstrap ou admission.

Le lot RSMP est documentaire. Après sa vérification et publication ciblées, les réalisations autorisées sont effectuées, puis les tests produit et validations sont exécutés dans une phase distincte selon la dernière instruction du développeur. Aucune tâche n’est cochée avant ses preuves ; les restrictions d’effets et mandats CAB restent opposables.

## Profil terminal et composition locale — D7/D8 adoptés le 23 octobre 2026

### D7 — Identité TLS terminale initiale

La portée est la première installation PA/PZT/PBO avant PostgreSQL. Chaque usage TLS client ou serveur possède sa propre paire matérielle non exportable P-256 et son certificat ; aucune réutilisation d'une clé CA ou de mandat personnel. Le profil fermé et les quatre scénarios D7/D8 sont normatifs dans [profil terminal courant du canon PZT](../../specs/pzt/spec.md#requirement-profil-x509-des-terminaux-de-première-installation-z12) et [requirements.md](requirements.md). Le schéma terminal du §13.2 de [contracts.md](contracts.md) explicite les liaisons et contrôles : Subject vide, six extensions seulement, SAN critique URI canonique urn:uuid:<UUIDv7 d'instance>, IP IPv4 loopback exacte du plan pour le seul serveur, CA=false, KU digitalSignature seul, exactement un EKU clientAuth ou serverAuth. La chaîne CA D2 reste distincte avec ses quatre seules extensions ; toute NameConstraints ou autre extension étrangère la rend inadmissible.

Chaîne, usage, URI d'instance et IP attendue sont vérifiés séparément. La provenance native et l'autorité courante ne découlent ni d'un UUIDv7 ni de loopback. Les dates et limites A10i4, le renouvellement aux deux tiers de la validité effective et le chevauchement maximal A10i3 de cinq minutes restent conservés ; aucune durée ou adresse/port par défaut n'est introduite. Propriétaires de l'identité, de la politique et du plan vérifient la possession et la protection matérielle réelles ; un DTO ou un certificat valide ne les remplace pas.

### D8 — Résolution propriétaire et contexte OpenSSL privé

Le §13.3/13.4 de contracts.md définit le second schéma et le port local privé de composition, sans les présenter comme des API déjà livrées. Le propriétaire compétent est constaté dans l'état protégé : Z12 initial D4 avant passage, puis propriétaire ordinaire Django/A07/A12 courant seulement après adoption et retrait attesté D6. L'appelant ne le sélectionne pas par un booléen ou une étiquette. L'absence de PostgreSQL est compatible avec la seule cérémonie D4 autorisée ; sa panne après D6 ne réactive aucune autorité initiale.

La résolution vérifie provenance/mandat, plan/politique/version, installation/cible/instance/rôle/usage/clé/génération, état/époque, validité/fraîcheur, révocation/retrait et ancrage avant chargement. Elle lie matériaux publics authentifiés, référence opaque de la seule clé terminale et durée de vie au même OSSL_LIB_CTX privé. Elle refuse clés CA, chemins/ancres libres réseau, état périmé ou restauré, blobs privés et EVP_PKEY/capsules Python publics. Aucun chargement partiel n'ouvre de transport ; les ressources natives acquises sont libérées à l'échec. Une révocation, un retrait, une perte de preuve ou d'autorité ferme l'utilisation courante sans attendre une échéance locale mise en cache.

Le passage D6 adopte les mêmes références publiques et conserve clés, âges, validités et retraits connus ; il retire les capacités et sessions privilégiées initiales avant admission ordinaire. Il ne crée ni nouvelle PKI ni mandat PostgreSQL. Le mandat technique PA et son ancrage anti-restauration demeurent distincts de Z12 ; un matériel partagé impose coordination du plan exact, sans partage implicite d'index NV, de clé ou d'autorité.

### Réalisation et limites de qualification D7/D8

Les mécanismes concrets et preuves des propriétaires, la composition native, la protection matérielle et l'ancrage sont réalisés puis testés dans la seconde phase demandée. Aucune adresse, aucun port, budget ou seuil de fraîcheur nouveau n'est déduit d'une fixture. Les références et noms de ports ne prouvent pas l'existence du propriétaire. L'indisponibilité d'une preuve requise ferme l'opération concernée et interdit de déclarer la tâche qualifiée. La présente extension ne modifie aucun fichier C08/PA01/authorization, ne crée aucune clé et n'autorise aucun effet TPM/NV ni installation.

## Profils de réalisation D9/D10 — adoptés le 23 octobre 2026

### D9 — Index PKI étendu, provisionnement et garde natifs

L’ancrage est un index de type extend SHA-256 dédié à Z12. Son numéro exact, son aire publique, sa politique de suppression et sa cible sont fixés par le plan de provisionnement extérieur ; aucune recherche d’index libre ou adoption d’un index préexistant n’est admise. Les attributs PLATFORMCREATE et POLICY_DELETE séparent ce provisionnement de l’usage runtime. ORDERLY et les variantes STCLEAR incompatibles avec la persistance requise sont refusés. L’index n’est pas un compteur ni un fichier restaurable ; ses extensions successives lient les événements au journal protégé de l’installation. Une valeur lue seule ne prouve ni sa provenance ni sa protection.

L’autorité de suppression est une clé matérielle P-256 non exportable indépendante des clés CA, TLS, personnelles opérateur et techniques PA. Les droits de plateforme et cette capacité restent hors des processus de signature et du runtime Z12. La politique publique réellement relue doit interdire aux signataires la suppression/redéfinition et ne pas offrir de branche équivalente par un mot de passe ou une hiérarchie qu’ils contrôlent. Le placement, les domaines de panne, l’administration de plateforme et la récupération de cette autorité sont explicités dans le plan exact avant tout effet ; leur sécurité n’est pas déduite de leur nom. Une lecture des spécifications TPM ne qualifie pas le firmware de hvp1, notamment après effacement, réinitialisation ou coupure.

Le gardien PKI natif reçoit le secret NV de 256 bits par un FD privé de la composition de confiance, vérifie sa provenance et sa portée, puis réalise les autorisations TSS2 dans des sessions HMAC SHA-256 liées à l’index et à son Name courant. Le numéro du FD ou un booléen fourni par Python ne constitue pas une preuve. Le secret ne passe ni dans argv, environnement, fichier temporaire, journal, objet/callback Python ni capsule publique. Les sessions mot de passe sont interdites. Les ressources natives et secrets sont fermés/effacés à la fin, après erreur et au retrait D6 ; les limites réelles de protection mémoire et de canal sont vérifiées par la recette. La simple vérification de l’aire publique sans autorisation ne remplace pas la vérification authentifiée de la valeur courante.

Le provisionneur écrit réellement l’événement initial lié à l’installation, la cible, la politique/version et au plan exact. Il relève les attributs, le Name applicable après WRITTEN et la valeur initiale effectivement écrite ; un index absent, non écrit ou zéro arbitraire ne vaut pas première installation. Les liaisons de politique/Name et l’événement initial évitent toute dépendance circulaire ; leurs octets exacts sont arrêtés et vérifiés dans le plan de recette. Les opérations courantes vérifient aire publique, Name, valeur et journal attendu avant effet, puis rapprochent intention, effet constaté et extension durable. Le fencing et l’ordre de reprise empêchent deux confirmations incompatibles. Une réponse perdue ou un crash entre effets place l’opération en IN_DOUBT jusqu’à réconciliation sur faits réels ; aucun retour à PREPARED, effacement d’historique ou rejeu aveugle n’est permis.

Les index, secrets, politiques, journaux et mandats PA/PKI restent distincts. Leur partage éventuel de TPM impose une coordination des effets plateforme ; aucun plan PA ne donne une autorisation NV PKI, et inversement. Le plan D5 doit identifier précisément cible, index, commandes, attributs, autorisations, effets, récupération et contrôles avant toute exécution. hvp1 désigne l’hôte courant ; aucun essai destructif sur un TPM distinct n’est couvert ou réputé disponible à partir de cette information.

### D10 — Propriétaire initial et fournisseur CA privés

Le composant Z12 Cython/OpenSSL 3/TSS2 est construit séparément des trois PA. Sa composition de confiance possède le contexte CA privé et le fournisseur TPM2 retenu ; elle n’insère pas le service CA dans les exécutables PA et ne transfère aucune clé CA au contexte TLS. D8 reste un port privé de résolution terminale dans le même OSSL_LIB_CTX du consommateur TLS. Les chemins de réalisation, dépendances exactes, ABI privée et contrôles de compilation sont consignés avant leur exécution ; leur présence documentaire ne prouve pas leur disponibilité. Aucun ajout de dépendance, installation ou build n’est autorisé par ce lot documentaire.

L’autorité initiale procède de la cérémonie locale isolée D4 et de ses observations natives, avec politique protégée/versionnée et mandat PKI courant. L’identité du lanceur, de l’installation, de la cible et des exécutants est obtenue auprès des mécanismes natifs de confiance puis recoupée avec le plan ; elle ne vient pas d’un DTO, d’UID 0 seul ou d’un identifiant auto-déclaré. La preuve personnelle Ed25519 utilise exclusivement une clé publique préautorisée par cette politique PKI. La clé privée personnelle reste sous le contrôle de l’opérateur ; aucune clé CA/TLS ou preuve PG/R01/C01 ne remplace cette admission.

Le propriétaire produit le challenge PKI dans son état courant protégé, vérifie la signature, le domaine, tous les liens du mandat et la fraîcheur auprès de sa source de temps compétente, puis consomme le challenge sous fencing et ancrage avant les effets autorisés. Il contrôle à nouveau politique, révocation, époque, état et ancrage aux frontières d’effet et de reprise. Une signature valable cryptographiquement avec politique périmée, challenge ancien, contexte étranger ou état invérifiable est refusée. Les limites de temps viennent de la politique réellement admise, sans durée de grâce ni TTL inventé. Le mandat, sa signature et un reçu ne sont ni un engagement A12 ni la preuve d’un effet système ou PG.

Les opérations des cinq ports initiaux du §12 et la résolution du §13 restent fermées par leurs propres préconditions. Le fournisseur natif vérifie les faits matériels et la possession des seules clés admises, sans repli logiciel et sans secret/EVP_PKEY/capsule Python public. Les objets de preuve, FD, sessions et capacités sont privés, liés à leur propriétaire et leur durée de vie ; les données publiques de traçabilité ne permettent pas de les recréer. Le contrat du §14 fixe les frontières et les refus, sans attribuer à A07/A12 une API qui n’existe pas.

D6 conserve adoption publique sous l’autorité courante puis retrait attesté et ancré des pouvoirs, voies, mandats et sessions initiales avant admission ordinaire. Seul le propriétaire ordinaire Django/A07/A12 courant peut ensuite fournir le matériel ; une panne PG ne réactive pas la cérémonie. Les références, âges, validités et retraits sont conservés sans nouvelle PKI systématique. La recette doit prouver la fermeture effective des capacités, y compris les ressources natives déjà ouvertes ; un statut écrit ne suffit pas.

### Preuves requises et limites du complément

La seconde phase vérifie build indépendant, provenance native, preuve personnelle et politiques courantes, domaine/challenge et anti-rejeu, chaque liaison du mandat, protection des FD/secrets/sessions, faits matériels des clés et absence d’export ou de repli. Elle vérifie en environnement autorisé provisionnement et genesis réels, authentification HMAC, refus des chemins de suppression/redéfinition par les signataires, ancien journal/restauration/clone, concurrence, coupure/réponse perdue et réconciliation, puis adoption/retrait D6 et refus PG indisponible. Aucun mock ne qualifie ces propriétés. Les essais matériels, effets NV et dépendances de build gardent leurs autorisations et plans distincts ; les contrôles documentaires ne les remplacent pas.

## Réalisation des profils D14/D15 — 24 octobre 2026

### D14 — faits natifs, temps vérifié et séparation des propriétaires

Les vérificateurs privés Cython/C observent directement via les API publiques libsystemd les UID/EUID/PID, unité et manager compétents, MainPID et InvocationID. Ils recoupent ces faits et les artefacts réellement chargés avec installation, cible, plan et politique protégée/versionnée. La composition native conserve les ressources et références privées ; aucun objet Python, UID 0, nom d’unité fourni par un client ou copie de rapport ne constitue une preuve. Un redémarrage, une substitution de processus, d’artefact, de manager ou de politique impose une nouvelle observation. Le profil est commun à PA01 système et Z12, sans ABI commune présumée, import d’inclusions privées, construction partagée ou transfert de mandat. PA01 possède ses propres écritures et qualifications.

Avant PostgreSQL, Z12 résout ces attentes dans les sources locales protégées de D4/D10 ; il ne dépend pas de Django ou de la base cible pour créer sa première observation. Après adoption et retrait D6, le propriétaire ordinaire courant les résout selon ses contrats. Les observations servent à assembler le contexte ; elles ne prouvent à elles seules ni le mandat, ni l’opérateur, ni l’anti-restauration. Les vérifications complètes de D4/D9/D10 et le fencing restent nécessaires avant admission ou effet.

Le service système de temps est réutilisé, installé, configuré et supervisé par PA système sous pixs.agent, pour un catalogue fermé avec cible, mandat, politique et ressources explicitement autorisés ; un propriétaire et un service par horloge, pas par module. Tous les échanges PBO–PA passent par PZT et pixs.agent gère les opérations PA hors responsabilités réseau PZT, avec l’interface runtime commune Kernel/Core/Auth/PA/PZT et un noyau agnostique du fournisseur. Sous Linux, chrony reste retenu, avec des références NTS amont authentifiées et qualifiées selon le profil et un serveur NTP local conditionnel, sans nouveau démon ni protocole Pixs. Le contrat applicable est sélectionné explicitement et en version : C.Z12_CHRONY_OBS/v1 historique inchangé ou C.Z12_TIME_OBS/v2 documentaire à réaliser et qualifier ; ce lot ne réalise ni ne livre de port, d’API ou d’ABI. Le raccord natif vérifie provenance du service, source sélectionnée et autorisée, authentification, rapports courants, incertitude totale et âge réel de la preuve amont, sans rajeunissement par lecture. Les trois modes exacts sont SYNCHRONISE, HORS_LIGNE et INVERIFIABLE. En SYNCHRONISE, l’âge amont est au plus 600 secondes. En HORS_LIGNE, un âge supérieur n’est admissible qu’avec modèle, provenance et continuité qualifiés, profil valide, acquisition actuelle et U(t) ≤ 1 s au point d’usage, sans durée magique ni réarmement de budget, d’échéance ou de droits. En INVERIFIABLE, les opérations exigeant un UTC qualifié sont refusées. Une indisponibilité amont compatible avec HORS_LIGNE qualifié ne vaut pas refus automatique, tandis que la perte de provenance, la rupture de continuité, l’absence de borne démontrable, la mesure incohérente ou le dépassement des bornes entraînent un refus. Les TTL, mandats, états, politiques et révocations restent opposables. Les budgets 250 ms, 2 acquisitions et 1 s ainsi que A10i49 et A10i51 sont conservés, sans troncature favorable et avec propagation conservatrice jusqu’à l’usage. Une indication synchronized ou le seul CLOCK_REALTIME ne suffisent pas. Le graphe d’amorçage du temps est acyclique avant PZT et PG, sous politique locale protégée indépendante, avec opérateur mandaté et catalogue, cible et exécutant vérifiés, sans auto-autorité ni recours à R01, au Super Admin, au métier ou au renouvellement PKI. Le logiciel de temps est disponible avant les étapes dépendantes, préfourni par l’image Docker et, pour Debian et VM, par un plan PA conforme ; aucun prérequis téléchargé par TLS n’est admis tant que l’heure et le TLS admissibles ne sont pas établis. Depuis un conteneur LXC, l’horloge de l’hôte n’est jamais réglée et aucun privilège, montage ou volume implicite n’est accordé.

Le résultat UTC vérifié et son incertitude sont appliqués aux mandats et à TLS/X509, à leur utilisation réelle, sans prolonger une validité ou créer une grâce. Les échéances d’opération utilisent une horloge monotone distincte et un budget explicite de politique ; une observation ne redémarre pas ce budget. Dans le LXC, chronyd -x est proposé pour observer sans corriger l’horloge partagée de hvp1. La validation TLS initiale de NTS reste active ; si l’environnement ne permet pas de vérifier cette chaîne de confiance et les bornes UTC, l’opération est refusée. Aucun compte, unité, chemin, socket, endpoint ou budget de production par défaut n’est déduit de cette proposition.

### D15 — garde du secret PKI et remise native

Le gardien Z12 est natif et appartient à une unité distincte du signataire CA. Un credential systemd dédié au secret NV PKI de 256 bits exige les deux facteurs effectifs host+tpm2 ; aucun facteur manquant ne permet un repli logiciel ou une création implicite de host key, de configuration TPM ou de secret. Le provisionnement, les facteurs, la récupération et leur protection font partie du plan et de la recette autorisés. Le mécanisme ne prétend pas protéger contre un administrateur hôte compromis.

Lecture du credential déchiffré, vérification du canal et effacement en mémoire sont exclusivement natifs. Le gardien vérifie réellement destinataire, installation/cible, politique/version et état courants avant de remettre un FD privé scellé, en lecture seule, contenant exactement 32 octets à la garde NV compétente. Une référence, un entier de FD ou un nom de credential ne suffit pas. L’état est rapproché nativement avec D9 ; la lecture interne nécessaire reste dans la frontière native du gardien et ne vaut pas autorisation d’un effet. Une dépendance circulaire ou une preuve manquante ne sont jamais converties en admission.

La remise porte uniquement le secret au composant NV authentifié ; elle ne signe pas, ne consomme pas de challenge métier et n’exécute pas elle-même une extension ou une suppression NV. C.Z12_NV_GUARD/v1 conserve ces opérations et recontrôle toutes ses préconditions. Le fournisseur CA ne reçoit pas le secret NV. Aucun secret, FD de secret, EVP_PKEY ou capsule public Python, argv, environnement ou journal ne transporte cette capacité. Secrets, credentials, services et journaux PA/PG/CA/PKI restent distincts. Succès, refus, échec partiel, arrêt, redémarrage et retrait D6 ont une gestion explicite des ressources ; les anciens FD, sessions ou capacités ne rouvrent pas une autorité initiale retirée.

### Construction, environnement et ordre de qualification

Le plan historique de construction adopté, non exécuté, a pour digest a7475b39fc528f27b36566aaa4b706b6315908ae30557f241489ae48dfcd20d4 et pour base debian@sha256:a717a33469731894e77e912ea7d714e27c2dc38ee6554fd1a3102e92999cfc66, architecture linux/amd64. Il retient les versions directes suivantes :

| Paquet | Version adoptée |
| --- | --- |
| gcc | 4:14.2.0-1 |
| libc6-dev | 2.41-12+deb13u4 |
| python3-dev | 3.13.5-1 |
| cython3 | 3.0.11+dfsg-2+b1 |
| pkgconf | 1.8.1-4 |
| libssl-dev | 3.5.7-1~deb13u3 |
| libtss2-dev | 4.1.3-1.2 |
| libsystemd-dev | 257.13-1~deb13u1 |
| libsystemd0 | 257.13-1~deb13u1 |

Les deux paquets libsystemd sont l’ajout explicitement adopté par D14 avec leurs dépendances Debian signées, pour les images isolées de construction/test PA01 et Z12 en seconde phase. Les versions et ABI effectives, dépendances transitives, sources, empreintes et artefacts doivent être consignés avant qualification. La liste historique de sept inclusions et cinq programmes ne couvre pas les huit inclusions et les tests modifiés au moment de cette reprise ; le manifeste exact doit être actualisé avant toute construction et encore après les réalisations suivantes. L’ancien digest n’atteste ni le nouvel ensemble de sources, ni un build exécuté. Aucun paquet hôte ou venv hôte n’est autorisé par ces choix.

Le développeur préfère le LXC Debian 13 CT 100, hostname cismp, sur hvp1 ; la méthode d’accès annoncée est SSH root à 10.0.0.1:22. L’identité effective et les capacités y sont vérifiées avant mutation. L’accord humain récent pour ce seul conteneur autorise ses opérations internes, y compris paquets, services et tests, sans nouvelle approbation humaine/NFDOC/CAB ; il étend ce périmètre de laboratoire sans transférer de droits à l’hôte. Les changements de services communs, tests incompatibles et remises à zéro sont coordonnés techniquement entre RUN. Aucune création ou administration Proxmox n’en découle. Root interne ne vaut pas autorité de plateforme TPM ; le TPM exposé reste physique et partagé, hors restauration par snapshot. Les effets TPM/NV conservent leurs plans et autorisations distincts D5. Un résultat LXC ne qualifie pas implicitement une machine physique, VM ou autre plateforme.

Les sources restent réalisées en première phase ; les constructions, tests et validations produit sont exécutés en seconde phase. Les contrôles documentaires stricts restent applicables pendant la rédaction. Les contrats privés et recettes sont au §15 de [contracts.md](contracts.md). Aucune nouvelle coche, qualification, installation ou utilisation actuelle de secret ne résulte du présent lot.


## Réalisation du profil D16 — secrets CA/parent/terminaux

### Sources et propriétaires

Z12 résout la clé, son parent réellement sélectionné, le périmètre d’autorité et l’usage depuis le plan et la politique protégée/versionnée. Les références ne donnent aucun droit d’obtenir un secret. Les secrets CA/parent/terminaux restent distincts par périmètre et usage ; aucune référence, valeur, credential ou capacité NV PKI D15, PA ou PG n’est réutilisée.

Pour les intermédiaires et terminaux, la source est un credential systemd dédié exigeant réellement host+tpm2. Lecture, vérification du canal et effacement des copies sont exclusivement natifs. Le destinataire CA reste dans son contexte CA privé ; le destinataire terminal appartient à la composition du consommateur TLS D8 et conserve le même OSSL_LIB_CTX pour résolution et utilisation. Ce choix ne crée ni bibliothèque commune, ni nouveau binaire, ni ABI partagée avec PA01.

Pour la racine hors ligne, la source est une remise de cérémonie mandatée par FD natif privé, scellé contre écriture, croissance, réduction et retrait des sceaux, et ouvert en lecture seule. Le contexte de parent de cette racine suit cette frontière hors ligne. Aucun service permanent ne charge ces autorisations. Le profil n’impose pas de recréer les clés lors du passage D6.

### Séquence, octets et durée de vie

Le propriétaire constate l’étape et l’autorité compétentes, vérifie nativement identité/destinataire, plan/politique/version, clé/parent/usage, opération/époque, mandat applicable, temps, état et ancrage avant toute remise. Une identité UID 0, un nom de credential, un entier de FD ou une déclaration de facteur ne suffit pas. Après D6, seule l’autorité ordinaire courante peut admettre l’utilisation ; une panne PostgreSQL ne rouvre pas la cérémonie.

La politique fixe explicitement la source, la taille non vide et l’encodage admis. Aucun format, chemin, nom de credential ou secret vide par défaut n’est choisi. Le raccord natif vérifie les longueurs avant lecture et avant callback, conserve les octets autorisés sans troncature ou transformation implicite, et refuse une interface incompatible. Une étiquette de paramètre fournisseur ne prouve pas la conservation des octets.

La propriété et le transfert des FD, buffers et références sont explicites. Les objets restent privés, sont effacés/libérés après succès, refus, échec partiel, arrêt et retrait, et ne circulent jamais dans Python, argv, environnement ou journaux. Une issue inconnue n’est pas convertie en remise favorable. Les anciennes capacités ne restaurent pas l’autorité initiale ; retrait D6, révocation ou changement de contexte/politique imposent les contrôles et fermetures réels. D15 continue de réserver le secret NV au seul composant NV authentifié ; le fournisseur CA n’en reçoit aucune copie.

Les contrats privés fermés/versionnés et recettes figurent au §16 de [contracts.md](contracts.md). Ce lot documentaire ne provisionne aucun facteur/credential, ne lit aucun secret actuel et ne produit aucun effet de clé, installation ou TPM/NV. Les dépendances et effets d’essai restent bornés avant exécution ; aucune qualification n’est acquise par le choix du profil.


## Attente M1 et transcription D17 — 25 octobre 2026

Ordre causal complet, sans effet dans ce lot.

Première attente et installation TCB : artefact natif authentiquement installé sous procédure locale extérieure, avec identité, domaine et version constatés nativement. La clé administrative réelle vient exclusivement de cette attente native ; aucune politique, aucun manifeste, aucun DTO et aucun champ client ne la choisissent. Revue administrative extérieure distincte de l'admission runtime.

Données candidates, politique indépendante portant les préautorisations réelles, puis plan d'amorçage et provisionnement PKI Z12 la référençant, distinct du TechnicalPlan PostgreSQL et E5. Prépublication signée éventuelle AVANT l'effet dont elle doit engager les données, jamais après pour fabriquer son propre fondement ; elle n'accorde aucun droit et permet seulement assemblage et observation préliminaire, dont NTS, sans prétendre fraîcheur, heure ni admission. D5 humaine exacte avant tout effet couvert.

Provisionnement extérieur avec autorité de suppression indépendante. WRITTEN puis genesis et événement initial réellement écrits. Constat extérieur du binding attendu, attributs, Name après écriture, valeur et journaux. Signature finale liant le binding attendu constaté et les digests de plan et politique. Genesis, événement et état-journal constatés antérieurement engagés par la publication ne contiennent ni son digest ni sa signature. Un événement ultérieur peut référencer une publication antérieure seulement sans entrer dans ses propres octets engagés et sous préconditions existantes. Plan et politique ne se hachent pas réciproquement.

Vérification cryptographique publique préliminaire sans admission. Admission complète seulement après D9, D11, état et identité natifs actuels, puis D10 avec fencing et consommation durable avant opérations. Mises à jour et interruptions : état antérieur, intention et transition fencées, résultat relu et rapprochement courant NV et journal, sans calcul auto-référent ni réutilisation naïve d'ancienne époque consommée. Pas de nouvelle genèse, index, compteur, ni replay après résultat perdu.

Adoption publique conservant clés, chaînes et âges. Retrait initial attesté et ancré. Admission ordinaire seule après D6. Remplacement et révocation du pin uniquement sous procédure extérieure explicitement mandatée ; procédure à réaliser et qualifier, avec refus et propriétaires définis sans DTO de preuve. TCB initial explicite et limites face à l'administrateur ou OS privilégié compromis. Observation, réalisation et qualification séparées ; aucun succès produit acquis. Aucun binaire, ABI, port transversal, secret réel, installation, test produit ou effet TPM et NV dans ce lot.

## Cérémonie UTC extérieure — conception D18 du 25 octobre 2026

La voie normale utilise le temps courant qualifié selon le contrat D11 applicable ; D18 reste exceptionnel, seulement lorsque l’UTC fiable est indémontrable, sans poste extérieur imposé à chaque démarrage. Quand une cérémonie est nécessaire, le provisionneur extérieur compétent qualifie réellement la source indépendante et documente traces, incertitude et dérive, sans autorité conférée par la seule signature. L’ordre reste défi volatile frais issu d’une source CSPRNG native, puis mesure extérieure après le défi, puis signature personnelle D10 à l’extérieur, puis réception native, sans ordre inversé. Depuis un conteneur LXC, l’horloge de l’hôte n’est jamais ajustée. Le format des 22 champs, de l’enveloppe et de D6 reste inchangé.

Le cycle natif est frais → émis → vérification → consommé ou invalidé, avec invalidation avant toute utilisation, atomicité et protection contre la concurrence. Redémarrage, suspension ou perte de contexte détruisent la capacité et imposent un nouveau défi. Aucun fichier restaurable ne recharge une preuve, aucun mandat CA, PG ou NV n’en découle, aucun effet TPM ou NV n’est requis pour la fraîcheur. La cérémonie D18 reste exceptionnelle, lorsque l’UTC fiable est indémontrable, et non une routine à chaque démarrage ; une source fiable préexistante ou un temps qualifié courant sont utilisés lorsqu’ils sont disponibles, sans poste extérieur, GNSS ou Netnod imposé. Les 22 champs, l’enveloppe à quatre champs, la signature de 64 octets et les domaines du §18 restent inchangés, avec dates TLS toujours contrôlées et sans contournement. Après réparation, seul le contrat D11 explicitement choisi s’applique, sans NTS ou Internet neuf obligatoire en HORS_LIGNE qualifié, puis seules les gardes existantes s’appliquent sans mandat conféré. D6 n’est jamais rouvert et la fenêtre R01 de 600 secondes ainsi que les durées de certificats restent inchangées.

L’intervalle est élargi par la durée écoulée, les incertitudes relevées et une borne de dérive réellement qualifiée, avec les bornes de délai du profil, jamais un choix client. Si la continuité, le taux ou le temps d’attente sont indémontrables, le chemin est refusé. L’observation reste cohérente et actuelle, avec invalidation sur perte d’origine, rupture de continuité, suspension, reprise, restauration ou retour Internet incohérent, sans renouveler budget, échéance ou droits. L’intervalle entier est ensuite comparé aux `notBefore` et `notAfter` de chaque certificat admissible, avec les contrôles TLS normaux et l’horloge réellement utilisée. Aucune API `chrony` n’est inventée ; tout raccord concret non démontré reste une condition de qualification bloquante explicite, sans qualification acquise.

## Complément temps v2 T0 — modèle, propriétaires et cycle

Le modèle affine conservateur identifié et versionné porte la propagation, avec `Uref`, erreurs de collecte et conversion, borne de fréquence rationnelle et `max_elapsed_ns` obligatoire. Le producteur natif local par horloge observe, vérifie et consomme sous composition authentique ; PA gère le service sous `pixs.agent`, échanges PBO et PA par PZT seulement. Budgets D11 `250ms`, `2` acquisitions, global `1s` avec parent prioritaire ; budget cérémonie D18 distinct selon profil `§18.3` sans `1s` imposé. D18 conserve 22 champs, enveloppe 4, nonce 32, signature D10 distincte M1, `TLS` à dates actives. Référence maîtresse en [RACCORDS_TEMPS_V2.md](RACCORDS_TEMPS_V2.md). Cycle : T1, T2, T3 réaliser, tester, corriger, retester et valider par unité avant suivante, avec sources et tests de l'unité ; T4 qualification intégrée et contrôle global final distinct.

## Statut des deltas antérieurs après contrôle E3

Les anciens fichiers sous specs/ ont été déplacés, avec empreintes conservées, vers [l’historique interne](historique-deltas-avant-e3/README.md). Le [contrôle de couverture](COUVERTURE_DELTAS_E3.md) relie chaque ancienne exigence au contrat courant et aux tâches ouvertes. Le dossier reste actif ; skip_specs évite seulement la réapplication des anciennes prescriptions. Il ne termine ni la réalisation, ni les tests, ni les 49 tâches encore ouvertes dans les sept dossiers concernés.
