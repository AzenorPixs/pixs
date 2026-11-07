# PA/PZT — Décisions S1, R1 et F1

Date : 27 octobre 2026.

Actualisation après validation explicite complémentaire :
[D-S1/D-R1/D-F1/D-SMIG](DETAIL_S1_R1_F1.md) sont désormais ADOPTÉS
DOCUMENTAIREMENT. Les huit tables et leurs définitions, le contrat du relais,
les interfaces privées et la migration physique M0–M5 sont validés. Dix-sept
exigences et trente-quatre scénarios détaillés sont inscrits dans les deltas
PA01 Agent/PZT, NON SYNCHRONISÉS au canon par cette inscription.
Les réalisations exécutables et preuves restent manquantes.

## 1. Autorité et portée

**S1, R1 ET F1 VALIDÉS PAR LE DÉVELOPPEUR — DOCUMENTATION UNIQUEMENT.**

Source : « Je valide tes recommandations S1, R1 et F1. Inscris ces décisions
dans les spécifications et le cadrage PA/PZT, sans implémentation ni
production de code, en distinguant les choix validés des réalisations
et preuves manquantes. »

Ces décisions complètent les [orientations A1–A5](DECISIONS_A1_A5.md) et les
[détails D-A1/D-A2/D-A3/D-MIG](DETAIL_A1_A2_A3.md), sans les rouvrir.
Leurs nouvelles exigences sont inscrites dans les deltas PA01
[pixs-agent](specs/pixs-agent/spec.md) et [pzt](specs/pzt/spec.md).
L'inscription initiale était distincte de leur synchronisation. Sur demande
explicite complémentaire du développeur le 27 octobre 2026, ces cinq exigences
et douze scénarios sont désormais SYNCHRONISÉS À L'IDENTIQUE dans les canons
[pixs-agent](../../specs/pixs-agent/spec.md) et
[pzt](../../specs/pzt/spec.md). Les exigences antérieures conservent leur
contenu ; aucun autre delta n'est réappliqué. Cette synchronisation ne livre
aucune réalisation ou preuve fonctionnelle.

La validation sélectionne le stockage, le mécanisme de remise et les familles
de fournisseurs ci-dessous. Elle ne livre ni schéma physique exécutable,
relais, adaptateur, producteur temporel ou preuve fonctionnelle. Aucun
endpoint, port, compte, budget, délai, nouveau broker ou contrat public
supplémentaire n'est choisi. La qualification future reprend la politique
Cython existante : dernière stable admissible au début de campagne,
puis version exacte verrouillée, sans actualisation de chaîne ici.

## 2. S1 — Tables PostgreSQL privées dédiées à Agent

### Choix validé

Le stockage retenu utilise des tables privées dédiées à Agent, via Django
et PostgreSQL, dans la même base et la même transaction propriétaire que
l'opération Agent concernée. Il couvre :

- la liaison AgentPaBinding 1.0.0 et l'historique de ses révisions ;
- les intentions durables de remise à PZT et les tentatives ;
- la version et la provenance distinctes des payloads historiques D-MIG.

L'identité, le scope, la génération et la révision utilisent des colonnes
typées et des contraintes explicites. Le payload de rapprochement demeure
immuable ; l'état courant et sa révision restent séparés et suivent le cycle
D-A1. La révision de liaison ne devient ni une génération Agent ni un compteur PA.

Les documents non secrets engagés par signature ou digest conservent leurs
octets exacts. Une projection JSONB peut faciliter la recherche ; elle ne
remplace jamais ces octets ni le codec propriétaire. Les preuves natives
restent chez leurs propriétaires ; leurs références ne deviennent pas des
copies d'autorité dans Agent.

La migration reste additive suivant M0–M5 : version et provenance sont
explicites, les payloads historiques ne sont pas réécrits. Les identités,
générations, digests, signatures et précisions de source restent conservés.

### Réalisation et preuves manquantes

Les noms de tables, colonnes, contraintes et liens de stockage sont désormais
définis dans le détail validé D-S1. Les modèles Django, dépôts et contrôles
de concurrence, migrations et plan de retour exécutable restent à réaliser. Il faut encore
prouver atomicité locale, isolation, conflits de génération/révision,
conservation exacte des octets, classification des lignes anciennes,
compatibilité de lecture et restauration sans perte. Aucun DDL ni migration
n'est produit ou exécuté par cette décision.

## 3. R1 — Outbox Agent transactionnelle et relais PBO vers PZT

### Choix validé

Une outbox durable privée Agent porte les intentions de remise, avec un
relais exécuté dans PBO vers l'adaptateur PZT. Aucun broker externe n'est ajouté.

Pour une MUTATION, opération Agent, liaison et intention sont persistées dans
la même transaction locale propriétaire. Après commit local vérifié seulement,
le relais peut soumettre la demande au contrat PZT. Une intention n'est pas
une preuve de remise ; cette atomicité locale ne promet aucune transaction
distribuée avec PA. Les lectures conservent la séparation READ/MUTATION
D-A1 et n'incrémentent pas la génération du souhaité.

PZT conserve admission et routage vers PA. Il n'existe aucun canal direct
PBO–PA. Avant chaque émission ou reprise, le relais recontrôle génération,
état de liaison, mandat, expiration, relation et identité attendue auprès
des sources compétentes. Ces contrôles ne remplacent pas les gardes courantes
PZT/PA au point d'usage avant effet.

Un résultat de commit ou d'envoi incertain impose une réconciliation avant
réémission ; une permission consommée n'est pas rejouée. Les tentatives et
résultats connus restent traçables. Un ACK PZT atteste une réception selon
son contrat ; il ne vaut ni succès technique PA, ni confirmation Agent.
La remise répétée ne garantit pas à elle seule l'absence de double effet :
idempotence, journal et réconciliation natifs restent nécessaires.

Les mécanismes compatibles C09 peuvent être réutilisés via une frontière
d'intégration explicitement définie. Le participant existant
[C09CoreOutboxParticipant](../../../src/pixs/core/c09_outbox_participant.py)
porte les mutations Core ; il ne constitue pas un raccord Agent directement
utilisable. Aucune dépendance aux implémentations privées Core n'est adoptée
par cette décision.

### Réalisation et preuves manquantes

Le schéma d'outbox, les interfaces du relais, la concurrence, la reprise et
les diagnostics sont détaillés et validés par D-S1/D-R1/D-F1. L'hébergement
PBO et les profils opérationnels restent à sélectionner ; les implémentations
et raccordements restent à réaliser avec leurs bornes explicites.
Il faut encore prouver absence d'émission avant commit, rollback sans envoi,
commit connu après perte de réponse, contrôles courants à la reprise,
incertitude conservée et absence de double effet natif. Aucun relais,
transport, calendrier de tentative ou nouveau statut public n'est livré ici.

## 4. F1 — Fournisseurs retenus et frontières

La sélection suivante attribue les réalisations futures ; elle n'atteste pas
leur disponibilité actuelle. Chaque fournisseur devra être identifié par
son implémentation exécutable, sa version, son propriétaire, sa sélection
authentique dans la composition et ses preuves applicables.

| Besoin | Fournisseur ou mécanisme validé | Réalisation et preuve encore manquantes |
| --- | --- | --- |
| Liaison et provenance | Dépôt privé Agent via Django/PostgreSQL selon S1. | Modèles, contraintes, transactions, migration et retour. |
| Remise et transport | Outbox/relais Agent dans PBO selon R1, vers l'adaptateur PZT ; pour E3 local, adaptateur Cython/OpenSSL 3 mTLS déjà retenu. | Relais, client/serveur, admission, routage et parcours réel ; ni Protocol ni contexte TLS ne livrent le transport. |
| Mandats et autorisation | Fournisseurs des contrats publics Core/Auth pour la gestion ordinaire ; fournisseurs PA/C08/Z12 du parcours initial. | Ports concrets, sélection et contrôles au point d'usage ; aucune autorité Core fictive avant PostgreSQL. |
| Résultat technique | Résolveur natif PA, adossé au résultat durable, au journal/ancre et aux postconditions réelles. | Lecture causale, résolution et rapprochement effectifs ; codec ou ancre seuls ne prouvent pas un effet PostgreSQL. |
| Origine et confirmation Agent | Adaptateurs des ports AgentOriginTrustPort et AgentConfirmationTrustPort consommant les preuves propriétaires. | Résolution réelle, bindings et contrôles d'origine, de postcondition et de confirmation ; aucune confirmation automatique depuis SUCCEEDED. |
| Temps | Producteurs propres aux processus PBO, PA et PZT, enregistrés par composition authentique derrière TimeProducer 2.0.0, avec les sources du profil adopté. | Producteurs concrets et gardes qualifiées à chaque point d'usage ; l'interface abstraite ne fournit pas la preuve temporelle. |

Références : [ports Agent](../../../src/pixs/agent/ports.py),
[ports PZT](../../../src/pixs/pzt/ports.py),
[contrat de temps](../../../src/pixs/kernel/contracts/time.py) et
[raccord du temps Z12](../add-pzt-ca-hierarchy-rotation-and-recovery/RACCORDS_TEMPS_V2.md).
Le chemin envisagé `src/pixs/core/time_evidence.py` est absent au contrôle
du 27 octobre 2026 ; il ne désigne pas un fournisseur livré.

Les gardes temporelles restent privées à leur propriétaire et courantes ;
aucun pointeur opaque, lease ou autorisation native n'est transféré en preuve
Python réutilisable. Aucun troisième fournisseur implicite de type Clock.now
ne remplace TimeProducer. Les limites et sources du profil existant
restent applicables sans valeur de fixture ou nouveau seuil.

Un fournisseur requis absent, une sélection ambiguë ou une preuve courante
manquante bloque le parcours protégé. La présence d'un symbole, d'un DTO,
d'un Protocol, d'une bibliothèque ou d'une source ne suffit pas à qualifier
la capacité. La disponibilité, les effets, la reprise et la révocation
doivent être démontrés sur la composition réelle.

## 5. Travaux et preuves à préparer

Les repères SRF01–SRF08 sont des critères de recette futurs, tous
**NON EXÉCUTÉS**. Ils complètent les cas D01–D16, C01–C28 et R01–R68 ;
ils ne les remplacent pas et n'ajoutent aucune case de réalisation.

| Repère | Objet et preuve attendue | Raccord aux cas existants |
| --- | --- | --- |
| SRF01 | Tables dédiées, contraintes, payload immuable et concurrence de révisions/générations. | D01/D02/D04 ; C05/C18/C21. |
| SRF02 | Octets exacts séparés d'une projection JSONB, migration additive, provenance et retour sans perte. | D13–D15 ; C04/C18/C22/C27. |
| SRF03 | Opération/liaison/intention atomiques, rollback sans émission et envoi après commit vérifié. | D01/D05 ; C20/C21. |
| SRF04 | Reprise concurrente, mandat expiré/révoqué, relation/cible/génération changées : refus courant sans permission recyclée. | D02/D04/D05 ; C09–C13/C20/C23/C24. |
| SRF05 | Envoi/réponse perdus et ACK seul : réconciliation, pas de succès ni confirmation déduits, pas de double effet natif. | D05–D11 ; C14–C21. |
| SRF06 | Fournisseurs ordinaires et initiaux distincts, sélection authentique, refus sur fournisseur absent ou faux raccord C09. | D03/D16 ; C06/C09–C13/C28. |
| SRF07 | Résultat durable, origine et postconditions réelles : seule la chaîne entièrement vérifiée confirme Agent. | D07/D08/D10/D11 ; C15–C19. |
| SRF08 | Producteurs temporels de chaque processus, acquisition courante et dégradation au point d'usage, sans repli Clock.now. | D12/D16 ; C04/C11/C24/C28. |

La recette utilisera les versions, profils et empreintes réellement
sélectionnés, et distinguera fixtures, preuves propriétaires et intégration.
Les preuves historiques du constructeur ne qualifient aucun de ces raccords.

## 6. État résultant après inscription et synchronisation

| Dimension | État après cette inscription |
| --- | --- |
| S1, R1 et F1 | VALIDÉS DOCUMENTAIREMENT le 27 octobre 2026. |
| Détails D-S1/D-R1/D-F1/D-SMIG | VALIDÉS DOCUMENTAIREMENT ; dix-sept exigences/trente-quatre scénarios dans les deltas PA01, NON SYNCHRONISÉS au canon par cette inscription. |
| Deltas PA01 Agent/PZT | INSCRITS : cinq exigences et douze scénarios S1/R1/F1 au total. |
| Canon pour ces nouveaux deltas | SYNCHRONISÉ À L'IDENTIQUE le 27 octobre 2026 sur demande explicite complémentaire : quatre exigences/dix scénarios pixs-agent et une exigence/deux scénarios pzt ; contenu canonique antérieur conservé. |
| Schémas, migrations, relais et fournisseurs choisis | RÉALISATIONS ET PREUVES MANQUANTES ; migration NON EXÉCUTÉE, Agent 2.0.0 NON LIVRÉ. |
| Recettes produit | NON EXÉCUTÉES par cette inscription ; aucune tâche cochée. |
| Qualification fonctionnelle PA/PZT | BLOQUÉE tant que les réalisations et preuves requises manquent. |

## 7. Vérifications de l'inscription initiale avant synchronisation — 27 octobre 2026

- Treize documents contrôlés : UTF-8, LF, fin de fichier, absence d'espaces
  de fin de ligne et 165 liens relatifs existants.
- Ajout de cinq exigences et douze scénarios vérifié ; titres uniques et
  préfixes des deux deltas antérieurs conservés octet pour octet.
- OpenSpec strict ciblé réussi pour PA01, PA10, pixs-agent et pzt.
- OpenSpec global standard et strict réussis : 185/185 éléments
  (107 évolutions, 78 spécifications), zéro avertissement et zéro erreur.
  Les 86 informations sont identiques au relevé préalable.
- Deux canons contrôlés inchangés par empreinte ; aucune synchronisation
  S1/R1/F1 effectuée. Les 83 fichiers de sources/configuration contrôlés
  et les listes de cases des tâches PA01/PA10 sont inchangés.
- Contrôle Git des espaces réussi sur les documents concernés.

Ces vérifications portent sur la documentation et OpenSpec. Aucun test
produit, compilation, migration, effet SQL ou matériel n'a été exécuté ;
aucune preuve fonctionnelle nouvelle n'est revendiquée.

## 8. Synchronisation ciblée et cohérence vérifiées — 27 octobre 2026

Source : demande explicite complémentaire de synchroniser S1, R1 et F1 au
canon OpenSpec puis de vérifier les spécifications et le cadrage PA/PZT,
sans implémentation ni production de code.

Les seuls ajouts canoniques sont les quatre exigences et dix scénarios
pixs-agent et l'exigence et les deux scénarios pzt déjà validés dans les
deltas PA01. Les tableaux détaillés et scénarios sont copiés à l'identique ;
les deux deltas sources restent inchangés par empreinte. Aucun autre delta
n'est réappliqué, aucune évolution archivée et aucun contrat exécutable modifié.

| Vérification exécutée | Résultat observé |
| --- | --- |
| Canon pixs-agent | 65 exigences antérieures conservées octet pour octet ; quatre ajouts, soit 69 exigences. |
| Canon pzt | 211 exigences antérieures conservées octet pour octet ; un ajout, soit 212 exigences. |
| Identité delta/canon | Les 37 exigences du delta Agent et les trois du delta PZT sont identiques à leurs exigences canoniques, y compris les cinq ajouts S1/R1/F1 et leurs douze scénarios. |
| Documentation et renvois | Quinze documents contrôlés, UTF-8/LF, espaces de fin de ligne et 168 liens relatifs existants. Statuts du registre, cadrage PA01 et raccords/recette PA10 alignés sur la synchronisation. |
| OpenSpec strict ciblé | PA01, PA10, pixs-agent et pzt valides. |
| OpenSpec global standard | 185/185 : 107 évolutions et 78 spécifications ; zéro avertissement et zéro erreur. |
| OpenSpec global strict | 185/185 ; mêmes 86 informations qu'avant synchronisation, sans nouveau diagnostic. |
| Conservation du périmètre | 83 fichiers de sources/configuration contrôlés inchangés, deux deltas inchangés, cases de tâches PA01/PA10 inchangées ; contrôle Git des espaces réussi. |

La cohérence contrôlée conserve la séparation READ/MUTATION, générations et
révisions, les octets engagés et la migration additive, le commit local avant
remise, les gardes courantes et la réconciliation, la distinction ACK/succès/
confirmation, les parcours initial et ordinaire et les producteurs temporels
par processus. Les choix S1/R1/F1 sont canoniques ; les noms/contraintes exacts,
intégrations, fournisseurs exécutables/versionnés et preuves restent à produire.

Les frontières PZT_TRANSPORT_UNAVAILABLE, PZT_EXECUTION_UNAVAILABLE et
ready_for_transport=False sont toujours observées dans les sources inchangées.
Agent 2.0.0 reste NON LIVRÉ, migration NON EXÉCUTÉE ; les cas C01–C28,
D01–D16 et critères SRF01–SRF08 ne sont pas exécutés par cette opération.
Aucune compilation, migration, activation, écriture de code ou recette produit
n'a été réalisée. La qualification fonctionnelle PA/PZT reste BLOQUÉE.

