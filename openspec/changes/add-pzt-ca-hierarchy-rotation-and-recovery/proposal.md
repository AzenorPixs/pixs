# Z12 — PKI et cycle de vie des autorités CA

## Pourquoi

Les contrats PZT et leurs décisions sont spécifiés ; le README ne revendique pas de réseau livré. Les clauses de gestion PBO essentielles restent distinctes des rôles réseau activés et des auxiliaires spécialisés.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

## Modifications proposées

A10i6–A10i20 : PKI dédiée, intermédiaires, protection des clés, secours, exclusion/bascule, algorithmes et successions racine.

## Capacités

### Capacités nouvelles

Aucune capacité nouvelle n’est créée. Les capacités existantes pzt et authorization sont étendues au seul amorçage PKI/PZT de première installation avant PostgreSQL, sous les décisions D4/D5/D6 validées le 23 octobre 2026.

### Capacités modifiées

Deux exigences nouvelles et quatre scénarios sont portés par les deltas pzt et authorization et ajoutés à leurs canons. Ils définissent explicitement la seule exception initiale avant PostgreSQL aux décisions/engagements ordinaires A10i6/A12a. Les blocs canoniques antérieurs restent intacts ; requirements.md conserve leurs copies et ajoute les deux références nouvelles. skip_specs passe à false.

## Sélection et périmètre autorisé

Le développeur étend le périmètre à l’amorçage PKI/PZT nécessaire à la première installation avant PostgreSQL. Z12 en est le producteur unique ; C08 orchestre l’installation et consomme ce contrat. Cette branche ne sélectionne ni ne qualifie implicitement tout le management CA ordinaire dans P0.

La reprise D4/D5/D6 autorisée porte sur les dix fichiers documentaires annoncés. Elle n’exécute aucun code produit, clé, certificat, installation ou effet NV et ne modifie aucun fichier C08. La réalisation Z12 autorisée reprend ensuite ; selon l’instruction explicite du développeur du 23 octobre 2026, les tests produit et validations forment une seconde phase, sans coche anticipée.

## Dépendances

- [add-pbo-runtime-secret-provider](../archive/2026-10-19-add-pbo-runtime-secret-provider/proposal.md).
- [add-core-postgres-services](../archive/2026-10-20-add-core-postgres-services/proposal.md).
- [add-durable-minimized-audit](../archive/2026-10-21-add-durable-minimized-audit/proposal.md).



## Impact de réalisation future

Séparer contrôle métier PBO/Django/PostgreSQL, propriétaire réseau pzt-daemon et adapters système. Implémenter le rôle précisément désigné par les contrats sources, avec schémas fermés, versions et contrôles courants ; conserver toutes bornes, unités, conditions de reprise et alternatives rejetées. La cryptographie WireGuard n’est pas réimplémentée. Les bibliothèques de transport, sources de temps et adapters sont qualifiés, sans confiance supposée.

## Critère de sortie de réalisation future

Signataire exclu avant succession ; perte traitée par nouvelles clés/recertification ; coexistence et durées bornées ; pas de confiance par snapshot.

## Décisions restant à valider

D1/D2/D3 et D4/D5/D6 sont adoptés pour le profil décrit dans design.md. Les mécanismes concrets, paramètres fournis par la politique et preuves de qualification restent à réaliser, sans valeur de production déduite d’une fixture. Le profil d’ancrage TPM NV dédié ne permet aucune écriture NV actuelle : plan d’essai exact et autorisation distincte nécessaires.

## Dépendances de préparation et de qualification

Z12 produit les contrats et le cycle de vie CA A10i6–A10i20 ; Z03 (add-pzt-authoritative-control-and-signed-receipts) consomme ces fondations et porte A12a–A12g. Z06 (add-pzt-public-control-contracts-and-state-streams) porte A07a–A07d/A07c2 et dépend de Z02/Z03. Cet ordre de préparation ne constitue ni une disponibilité runtime ni une autorisation de contourner les contrôles réciproques requis lors de l’activation. Les fondations C01/C02/C05 ne démontrent pas à elles seules les contrôles A07/A12, le canal PZT ou le contrôleur d’exclusion.

Chaque étape distingue les contrats producteurs vérifiables indépendamment et les prérequis de réalisation, d’activation puis de qualification intégrée. Une dépendance nécessaire à un effet ou à une preuve reste bloquante tant qu’elle manque. Aucun rôle CA, autorité admissible, mandat courant ou exclusion vérifiée ne peut être remplacé par une promesse d’adapter ou un mock. L’archivage exige toujours toutes les preuves applicables ; la clarification du graphe n’autorise pas une livraison partielle réputée complète.

## Extension initiale et passage au contrôle courant — 23 octobre 2026

Z12 possède la cérémonie locale isolée, son état PKI initial protégé et les cinq ports prepare_initial_trust, inspect_initial_trust, reconcile_initial_trust, adopt_initial_trust et retire_initial_authority. Leurs contrats restent documentaires avant réalisation. La provenance native, l’opérateur, le mandat lié au plan et la politique protégée/versionnée sont vérifiés positivement, sans dépendance à la base cible ni transfert de droits C01/R01. L’ancrage monotone TPM NV dédié contre la restauration est retenu à concevoir et qualifier, avec protection contre l’effacement ou la réinitialisation par les signataires.

Les références publiques et les effets sont adoptés et relus par les propriétaires courants après disponibilité de PostgreSQL. Adoption, retrait attesté et irréversible de l’autorité/canal/mandats initiaux, puis admission ordinaire sont des étapes distinctes, sans atomicité local/PostgreSQL inventée. Le passage seul n’impose pas une seconde PKI ou une recertification systématique ; âges, validités, retraits connus et rotations requises restent opposables. L’absence de PostgreSQL ne rouvrira jamais cette autorité après la première installation.

## Profil terminal et propriétaire local — D7/D8 adoptés le 23 octobre 2026

La première installation PA/PZT/PBO exige aussi des clés terminales P-256 matérielles non exportables, sans repli logiciel. Le profil fermé D7 distingue chaque usage clientAuth/serverAuth par une paire et un certificat propres ; Subject vide, SAN critique avec URI UUIDv7 canonique et, pour le seul serveur, IP IPv4 loopback explicitement liée à l'endpoint au plan. Aucun CN/DNS ou endpoint par défaut n'est ajouté. Le profil CA D2, les durées A10i4 et leurs bornes restent conservés. La conformité d'un certificat ne prouve ni identité native, ni autorité courante, ni mandat PostgreSQL.

D8 adopte la résolution locale privée depuis le propriétaire initial Z12 D4, puis exclusivement depuis le propriétaire ordinaire Django/A07/A12 courant après adoption et retrait attesté D6. Les deux schémas versionnés et le port documentaire sont décrits au §13 de [contracts.md](contracts.md). Politique/version, identité/cible/usage/génération, état/époque, fraîcheur/révocation et ancrage sont vérifiés avant fourniture ; la référence opaque de clé terminale demeure liée au même OSSL_LIB_CTX privé. Référence CA, ancre ou chemin réseau libre, EVP_PKEY/capsule Python publics, état restauré et repli logiciel sont refusés. Une panne PostgreSQL après D6 ne rouvre pas la cérémonie et ne rajeunit pas les références adoptées. Le mandat technique PostgreSQL et l'ancrage technique PA restent distincts.

Le lot documentaire D7/D8 comporte uniquement les six fichiers de cadrage du change, son delta PZT et le canon PZT. Aucun fichier authorization, C08 ou PA01 n'est modifié par ce lot. Réalisation, essais produit, qualification des propriétaires matériels/natifs et recette NV restent à effectuer ; aucune nouvelle coche ou permission d'effet matériel n'en résulte.

## Profils NV et propriétaire initial — D9/D10 adoptés le 23 octobre 2026

D9 concrétise D5 par un index PKI dédié NV_Extend SHA-256, préprovisionné extérieurement au runtime sous PLATFORMCREATE/POLICY_DELETE. La suppression relève d’une autorité matérielle P-256 non exportable indépendante des CA, des terminaux, de l’opérateur personnel et de PA01. Le runtime ne détient ni autorisation de plateforme ni capacité de suppression ou de redéfinition. Un secret NV PKI de 256 bits est remis uniquement par FD natif protégé ; les autorisations emploient des sessions HMAC SHA-256 liées à l’index, sans session mot de passe ni secret ou calcul HMAC Python. L’état initial réellement écrit lie installation, cible et politique ; aucun index libre n’est choisi automatiquement. PA et PKI conservent index, secrets et journaux distincts.

D10 retient un composant CA natif privé Cython/OpenSSL 3/TSS2, construit séparément des trois PA et utilisant le fournisseur TPM2 retenu. La preuve opérateur initiale est une signature personnelle Ed25519 dont la clé publique est préautorisée par la politique PKI protégée/versionnée. Son domaine et son challenge PKI courants lient plan/digest, installation, cible, exécutants, opération/version et époque ; les preuves PG/R01/C01 ne sont pas réutilisées. Le propriétaire vérifie réellement provenance native, temps, politique, état et ancrage avant effet. UID 0, un DTO ou une signature isolée ne suffisent pas. Aucun secret, EVP_PKEY ou capsule Python public ne sort de cette frontière. Le contexte CA est distinct du contexte TLS : l’exigence du même OSSL_LIB_CTX de D8 s’applique à la résolution et à l’utilisation terminales chez le consommateur TLS.

Les contrats privés fermés/versionnés, propriétaires et séquences sont détaillés au §14 de [contracts.md](contracts.md) et dans [design.md](design.md). Ce complément conserve D1–D8, les deux canons, les deltas et requirements.md. Il ajoute des critères aux tâches existantes sans créer de tâche ni modifier de coche. Il ne livre ni ne qualifie un propriétaire, fournisseur, build ou ancrage par sa seule rédaction. Les dépendances de build et les essais seront bornés avant exécution. Aucun effet NV, installation, utilisation actuelle de clé, changement de hiérarchie ou clear n’est autorisé par ce lot. Le plan exact et l’autorisation distincte D5 restent requis ; hvp1 est l’hôte actuel, et aucun TPM de laboratoire distinct n’est identifié.

## Complément de réalisation D14/D15 — 24 octobre 2026

Le profil natif commun PA01 système et Z12 décrit au présent paragraphe est conservé comme historique v1 : observations directes Cython/C/libsystemd et vérification native de chrony avec NTS vers time.cloudflare.com, incertitude totale au plus une seconde et âge au plus 600 secondes pour le mode SYNCHRONISE, sans validation TLS désactivée et avec chronyd -x en LXC sans correction de l’horloge partagée. La conception adoptée à réaliser et qualifier est désormais C.Z12_TIME_OBS/v2 : un propriétaire et un service par horloge sous PA et pixs.agent, interface runtime commune avec noyau agnostique, références NTS amont authentifiées et qualifiées selon le profil, serveur local conditionnel, trois modes exacts SYNCHRONISE, HORS_LIGNE et INVERIFIABLE, âge réel jamais rajeuni, HORS_LIGNE au-delà de 600 secondes seulement avec modèle, provenance et continuité qualifiés, profil valide, acquisition actuelle et U(t) ≤ 1 s au point d’usage, et INVERIFIABLE fermant les opérations exigeant un UTC qualifié. Les politiques, mandats, constructions et réalisations PA01 et Z12 restent distincts.

D15 retient pour Z12 un gardien natif dans une unité distincte du signataire CA, alimenté par un credential systemd chiffré avec les deux facteurs host+tpm2. Le secret NV PKI de 256 bits reste dans la frontière native ; seule une remise par FD privé scellé et en lecture seule au destinataire NV réellement vérifié est admise. Ce gardien ne devient pas un second propriétaire des opérations NV ; C.Z12_NV_GUARD/v1 (§14.2) conserve ces opérations. Le fournisseur CA ne reçoit jamais le secret NV. Les secrets et services PA/PG restent distincts. Les contrats, séquences, refus et critères sont précisés au §15 de [contracts.md](contracts.md), dans [design.md](design.md) et [tasks.md](tasks.md).

UTC, dépendances de construction et préférence LXC déjà adoptées sont transcrites dans ce complément. La cible de test est le LXC Debian 13 CT 100, nommé cismp, sur hvp1 ; son accès et ses propriétés restent à vérifier réellement. L’autorisation humaine récente couvre ses seules opérations internes sans nouvelle approbation humaine, NFDOC ou CAB ; la coordination technique entre RUN reste obligatoire. Le dépôt hôte, Git/OpenSpec sur l’hôte, Proxmox et les effets sur le TPM physique partagé conservent leurs autorisations propres. Le snapshot LXC ne restaure pas le TPM ; le plan exact D5 et son autorisation d’effets restent distincts.

Ce lot porte sur les cinq seuls fichiers annoncés. D1–D10, canons, deltas, requirements.md et les seules coches 1–2 sont conservés. Réalisation des sources en première phase, puis construction/tests/validation produit en seconde phase ; les contrôles documentaires stricts sont exécutés pendant la rédaction. Aucun document, nom de port, manifeste ou accord de dépendance ne constitue une preuve de compilation, d’effet matériel ou de qualification.


## Secrets des clés matérielles — D16 adopté le 24 octobre 2026

Les secrets d’autorisation des clés CA, de leurs parents et des clés terminales restent distincts par périmètre et usage, et ne réutilisent jamais le secret NV PKI D15 ni un secret PA/PG. Pour les intermédiaires et terminaux, le profil retient des credentials systemd dédiés chiffrés avec les deux facteurs effectifs host+tpm2, lus et effacés exclusivement en natif. Pour la racine hors ligne et son contexte de parent, la remise se limite à la cérémonie mandatée par FD natif privé, scellé et en lecture seule ; aucun accès permanent de service n’en découle.

Chaque remise vérifie destinataire et contexte courants, sans Python, argv, environnement ou journaux, et sans secret vide implicite. Les références, tailles et encodages sont résolus par la politique protégée/versionnée ; les callbacks du fournisseur doivent préserver les octets réellement admis et être qualifiés. Les frontières et refus sont précisés au §16 de [contracts.md](contracts.md) et dans [design.md](design.md).

Ce lot modifie uniquement .openspec.yaml, proposal.md, design.md, contracts.md et tasks.md. Il conserve D1–D15, canons/deltas, requirements.md et les seules coches 1–2. Il n’autorise ni génération ou lecture de secret actuel, ni installation, test produit ou opération TPM/NV. Réalisation autorisée des sources puis qualification en seconde phase demeurent distinctes ; le plan exact et l’autorisation D5 restent requis avant leurs effets.


## Attente administrative M1 — D17 adopté le 25 octobre 2026

M1 vaut pour Z12 seul : clé publique administrative Ed25519 dédiée, fixée avec identité, domaine et version constatés dans le composant natif authentiquement installé sous procédure locale extérieure. Hypothèse TCB initial explicite sur code, procédure et OS ; pas de preuve de provenance par stat, SHA, UID0 ou signature Debian de Pixs ; aucune résistance affirmée à compromission privilégiée OS. Clé privée dédiée hors runtime et agents, distincte opérateur, CA, TLS, suppression, PA et PG ; aucune obligation matérielle admin. CA et terminales restent matériels.

Politique indépendante, puis plan d'amorçage et provisionnement PKI Z12 la référençant, distinct du TechnicalPlan PostgreSQL et E5. Journal, index et secret PKI propres, sans état PA requis. D5 humaine exacte AVANT tout effet couvert. Aucun effet autorisé par ce lot.

Le §17 de contracts.md, fourni dans ce lot, définit le contrat cohérent dérivé du principe validé. Il utilise les types du §1 de contracts.md et réutilise les primitives du §14.3 de contracts.md. Aucun wire de brouillon antérieur n'est adopté.

Binding attendu constaté extérieurement après WRITTEN et genesis, puis publication finale signée. Vérification publique préliminaire sans admission, puis admission complète après D9, D11, état et identité natifs actuels, puis D10 pour opérations. Non-retour D6 : après adoption et retrait attesté, seule l'autorité ordinaire courante selon ses contrats, sans recréation de l'initial par vieux manifeste, artefact, snapshot, index absent ou Clear. Adoption publique conserve clés, chaînes et âges.

Prépublication éventuelle sans head et sans binding après WRITTEN ni digest de publication finale ; plan référençant la politique sans hachage circulaire ; signature administrative jamais mandat opérateur, PG, CA ou TLS. Clés et domaines PA indépendants, leur choix B non transposé. Publication, révocation et évolution du pin sous procédure extérieure explicitement mandatée, pas de clé candidate choisie par client. Dates, état et ancrage réellement recontrôlés, pas de booléen transportable. D9 NV_Extend conservé sans compteur, nouvel index ou nouvelle genèse.

## Cérémonie UTC extérieure signée — D18 adopté le 25 octobre 2026

Conception seule, sans effet. Source UTC extérieure indépendamment qualifiée, avec traces et responsable désigné. Défi natif volatile de 32 octets, à usage unique, strictement propriétaire du processus, du démarrage et de la cérémonie. Réponse Ed25519 personnelle D10 pure, dans le domaine nouveau et distinct `pixs.z12.time.ceremony/v1`, sans réemploi du domaine `pixs.z12.initial.operator/v1`. Clé publique attendue compilée sous artefact authentique, avant admission de politique, jamais candidate ni admin M1.

Seulement quand D18 est nécessaire, la mesure extérieure réelle a lieu après réception du défi et avant signature. L’intervalle vérifié `[lower_utc, upper_utc]` contient l’instant mesuré. L’écart entre UTC et horloge hôte est relevé nativement et propagé de façon conservatrice. L’horloge `hvp1` est préparée et vérifiée hors Pixs dans ce seul cas. `chronyd -x` ne modifie pas l’horloge partagée. La signature, le nonce, les dates TLS toujours contrôlées et D6 sans réouverture sont conservés.

Dates TLS toujours pleinement vérifiées, sans `bypass` ni `nocerttimecheck`. Le rappel D11 NTS `time.cloudflare.com` avec bornes `1s` et `600s` vaut pour le profil historique v1 conservé ; la conception adoptée suit C.Z12_TIME_OBS/v2 avec les trois modes exacts et les conditions cumulatives de HORS_LIGNE. D18 reste une exception pour un UTC indémontrable, avec signature D10, nonce et enveloppe conservés, sans poste extérieur, GNSS ou Netnod imposé. Cette preuve ne confère aucune admission CA, PG, NV, ni terminale. D6 interdit toute réouverture ; le non-retour reste une garde réelle extérieure et courante, jamais déduit d’une absence de fichier ou d’une initialisation nouvelle. Aucune clé actuelle, service, installation, heure, TPM ou NV. Détails normatifs au §18 de `contracts.md`.
## Conception temps v2 adoptée à réaliser et qualifier — 26 octobre 2026

Les cinq capacités modifiées sont pzt, pixs-agent, runtime, installation-provisioning et authorization, pour le seul sujet temps. PA constitue un propriétaire unique par horloge et pixs.agent administre PA ; Kernel, Core, Auth, PA et PZT consomment l’interface commune du runtime, et le noyau demeure agnostique du fournisseur. C.Z12_TIME_OBS/v2 est une conception adoptée à réaliser puis à qualifier ; C.Z12_CHRONY_OBS/v1 demeure inchangé.

Le mode SYNCHRONISE exige une preuve amont âgée d’au plus 600 secondes. Le mode HORS_LIGNE peut dépasser 600 secondes uniquement avec un modèle qualifié, une provenance qualifiée, une continuité qualifiée, un profil déclaré valide, une incertitude U(t) ≤ 1 s au point d’usage et une acquisition effective actuelle ; aucune lecture ultérieure ne rajeunit la preuve amont. Le mode INVERIFIABLE refuse les opérations exigeant un UTC qualifié. Les références amont admissibles sont authentifiées par NTS et qualifiées selon le profil. D18 reste une exception pour un UTC indémontrable, avec signature D10, nonce et enveloppe conservés, sans réouverture PKI au titre de D6. R01 conserve sa fenêtre de 600 secondes. Aucun code, installation, activation, archive ou effet matériel ne résulte de ce cadrage.
