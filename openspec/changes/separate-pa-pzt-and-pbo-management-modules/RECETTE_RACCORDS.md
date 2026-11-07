# Recette préparatoire des raccords PA10

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

Raccords Agent/PZT et nouveaux contextes ; préserver les versions et preuves anciennes sans qualification nouvelle par héritage.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [pixs-agent](../../specs/pixs-agent/spec.md).
- [pzt](../../specs/pzt/spec.md).
- [scope-context](../../specs/scope-context/spec.md).
- [managed-device-policies](../../specs/managed-device-policies/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Date : 24 octobre 2026. Statut des 28 cas **C01–C28** ci-dessous : **NON EXÉCUTÉ**.
Le palier P1 de frontière pure est rapporté séparément au §7.
Ce plan de recette n’est ni une suite de tests installée ni une qualification.
Il accompagne [la préparation des raccords](RACCORDS.md).

Actualisation du 27 octobre 2026 : A1–A5, D-A1/D-A2/D-A3/D-MIG puis S1/R1/F1 sont validés ; les §9–11 précisent les conditions d'entrée successives. Le tableau historique et ses 28 statuts NON EXÉCUTÉ sont conservés. Les anciennes mentions d'arbitrages ouverts ne valent pas réouverture des décisions adoptées.

## 1. Conditions d’entrée

- Profil, opérations et cible explicitement sélectionnés ; contrats, versions,
  bornes, propriétaires et artefacts exacts disponibles.
- Réponses PA01/C08/Z12 reçues et recoupées dans RACCORDS.md §§11–14.
  A1–A5 restent ouverts : réponse reçue ne vaut pas décision ou raccord livré.
  Aucun champ de confiance créé depuis le client ne remplace un propriétaire.
- Le contrat de projection C08 adopté est la référence documentaire pour
  publication/digest, plan PA/digest, confirmations immuables et contexte
  courant ; son producteur, son bundle et ses résolveurs opérationnels restent
  requis avant les scénarios nominaux d’admission E4.
- Contexte de pilotage CAB réel et permissions nouvelles prouvés avant effet ;
  aucun rejeu de once. Quotas exclus selon instruction du développeur.
- Environnements de test et nettoyages autorisés. Les futurs essais SQL sont
  isolés ; tests TPM/NV, services, réseau, paquets et hôte ont leurs autorisations
  propres. Aucune commande prête à modifier l’hôte n’est fournie ici.
- Les données, actors, politiques et durées de fixture sont explicitement
  synthétiques. Les simulations ne qualifient pas les fournisseurs réels.

## 2. Cas préparés

Chaque ligne attend une preuve native de commande/version/artefact et résultat,
avant qu’un état PASS/FAIL puisse remplacer NON EXÉCUTÉ.

| ID | Scénario | Résultat attendu / preuve à recueillir | Prérequis |
| --- | --- | --- | --- |
| C01 | Les trois opérations du catalogue 1.0.0 | Paramètres exacts, versions et cible rapprochés ; toute opération/version/champ étranger refusé avant effet. | Codecs/profil PA01 et contrat Agent existants. |
| C02 | Références multioctets et bornes | Respect simultané des bornes en caractères et octets ; refus sans troncature, coercition ou plafond implicite. | Bornes protégées publiées. |
| C03 | Encodage du mandat signé | Octets E4 et tableaux ordonnés conservés ; doublons/ordre signés non modifiés ; digest rapproché à la requête exacte. | Codec E4 réel ; test sans secret privé. |
| C04 | Date E4 fractionnaire face au contrat Agent | Conserver UTC E4 à six décimales et les octets de mandate_signed_bytes ; pas d’arrondi, troncature ou réencodage. Nominal suspendu : PA01 et C08 n’adoptent aucune projection vers la seconde. | A3 ouvert confirmé ; décision et projecteur propriétaire requis. |
| C05 | Génération Agent face aux compteurs natifs | NativeRequest/NativeResult ne fournissent aucun champ/producteur de génération Agent. registry_generation_ref, epoch, sequence et read_serial ne sont pas des substituts ; refuser toute liaison déduite du client. | A1 ouvert confirmé PA01/C08 ; binding serveur cible/scope/génération requis. |
| C06 | Lecture get_postgresql_result | Demande de lecture et opération lue distinctes ; autorité courante de lecture sur opération/cible, mandat consommé non réutilisé. | Résolveur/résultat durable PA01. |
| C07 | Amorçage pré-PG et projection C08 | Rapprocher publication/digest, plan PA/digest, confirmations immuables et contexte courant selon projection-contract.md ; aucun Subject/Core/CommandMetadata fictif. Une source PlanSource écrite ne vaut pas producteur E4. | Producteur/résolveur C08, bundle, PA01/Z12/PZT opérationnels ; actuellement non livrés pour ce raccord. |
| C08 | Gestion ordinaire après PG | C03/C04/C05, gouvernance, génération et idempotence réels ; refus et portée Super Admin conservés. | Composition Agent/PBO réelle. |
| C09 | Source de mandat, identité ou transport absente | Refus fermé, aucun envoi ni canal de remplacement ; audit selon autorité et conditions applicables, sans faux audit. | Ports réels absents ou retirés de façon contrôlée. |
| C10 | Signature valide sous clé non autorisée | Admission refusée ; cryptographie correcte ne vaut ni provenance ni permission. | Source de clé/autorité propriétaire, vecteur public ou environnement autorisé. |
| C11 | Identité/révocation/politique/UTC change entre contrôles | Retrait courant bloque l’effet suivant ; aucune réutilisation d’une ancienne décision, fenêtre ou source. | Sources réelles et injection de transition autorisée. |
| C12 | Transport local PBO–PA | Passage PZT/A07 effectivement observé, relation et identités liés ; aucune alternative directe locale. | Provider local qualifiable. |
| C13 | Deux topologies distantes | Hôte PA/PZT sans puis avec PBO/PFO locaux ; isolation d’autorités et absence de dépendance PBO locale imposée. | Providers et plateformes disponibles. |
| C14 | RECEIVED et RUNNING | Conserver reçu seul et progression technique sans fait appliqué ni confirmation Agent ; aucun mapping automatique vers ack/unknown adopté par PA01. | A2 ouvert confirmé ; projection à arrêter et producteur de résultats réel. |
| C15 | SUCCEEDED technique | Vérifier résultat technique durable et observations requises ; ne confirmer ni mode PBO, marqueur C08, commit Core/Auth ou état Agent depuis ce seul statut. Le codec ne livre pas les handlers/résultats durables. | Handlers, journal, postconditions et projection Agent réellement livrés et qualifiables. |
| C16 | FAILED, BLOCKED et IN_DOUBT | Conserver échec connu, précondition/autorité absente sans effet déduit, et réconciliation sans rejeu ; ne pas imposer un mapping Agent universel ou déduire l’issue du commit. | A2 ouvert ; producteur/résultat durable et sources courantes. |
| C17 | Observation référencée mais non vérifiable | Un DTO, digest, signature ou inventaire LXC/TPM ne fournit pas origine/autorité courante ; aucune observation appliquée construite depuis le JSON résultat ou des refs seules. | AgentOriginTrustPort et propriétaire réel des observations ; A4 ouvert. |
| C18 | Confirmation et bindings divergents ou absents | Refuser génération/cible/scope déduits ou incohérents ; lier fait observé, source, origine, postcondition et confirmation immuable au contexte courant ; absence du binding A1 non contournée. | Binding serveur A1 et AgentConfirmationTrustPort réels, confirmations C08 résolues. |
| C19 | Confirmations de domaines différents | CONFIRMED NV, SUCCEEDED technique, confirmation Agent, mode/marqueur C08 et commit Core/Auth restent disjoints ; aucune observation de conteneur ou d’UID n’est une qualification de ces domaines. | Producteurs réels et preuves de chaque domaine ; A4/A5 ouverts. |
| C20 | Réponse perdue et reprise | État inspectable relu ; aucune réémission automatique d’effet ou d’extension NV ; incertitude conservée jusqu’à preuve. | Journal/ancre et transport réels. |
| C21 | Concurrence, fencing et idempotence | Un effet admissible au plus ; conflits et vieille génération refusés ; trace initiale durable conservée. | Deux contextes/connexions réels et propriétaires. |
| C22 | Ancien instantané, cache ou restauration de journal | Source actuelle et ancre réellement recoupées ; copie/clonage/rollback ne restaurent pas une autorité. | Profil matériel isolé autorisé ; aucune qualification par mock. |
| C23 | Péremption ou retrait de collecte | Dernier connu daté ; observation absente/périmée non courante ; ancienne confirmation non réactivée. | PA réel et supervision Agent. |
| C24 | Échec d’acquisition, fermeture et annulation | Ressources libérées ou conservées pour reprise explicitement connue ; aucun handle périmé utilisable ou tâche orpheline. | Adapters/producers réels et profil de fermeture. |
| C25 | Debian PA/PZT indépendant | Quatre exécutables attendus, droits/versions/signatures et arrêt vérifiés ; pas de PBO/PFO imposés. | PA09 et artefact réel. |
| C26 | Docker sans session PA | Deux PA système/événements plus PZT, absence contrôlée du PA utilisateur/session ; état externe et recréation prouvés. | X01 et image réelle. |
| C27 | Qualification du composant et composition | Versions d’ABI, OS/CPU/modes et attestation du périmètre réellement testés ; aucun P0 extrapolé. | PA08/Z26 et artefacts/profils disponibles. |
| C28 | Promotion documentaire puis archive | Vérifier que réponses reçues, décisions adoptées, sources écrites et parcours qualifiés sont séparés ; aucun A1–A5 clos sans preuve. OpenSpec strict/liens ne remplacent pas les cas produit, archive et statistiques viennent seulement après critères applicables complets. | 2.2–2.4 et prérequis réels satisfaits ; préparation actuelle non assimilée à leur clôture. |

## 3. Paliers pour éviter des attentes inutiles

| Palier | Travail préparatoire autorisé maintenant | Ce qui attend encore |
| --- | --- | --- |
| P0 : analyse | Sources, signatures, champs, responsabilités, écarts et scénarios documentés ; coordination A1–A5. | Aucune réussite de test produit n’est annoncée. |
| P1 : contrats isolés | Préparer la matrice C01–C06 sur les codecs réels et réponses adoptées. | Exécution/validation sous prévol et mandats ; pas de résultat de provider simulé présenté comme réel. |
| P2 : gestion/autorité | Préparer C07–C11, C17–C19 et la régression locale affectée. | Producteurs d’autorité, contexte et postconditions consommables. |
| P3 : transport/exécution | Préparer C12–C24, instrumentation corrélée et pannes attendues. | PZT/PA/journal/lifecycle et environnement réellement qualifiables. |
| P4 : distributions | Préparer C25–C28 et matrice de profils. | PA09/X01/PA08/Z26 et autorisations/artefacts réels. |

Les paliers sont un plan de reprise proposé, pas de nouvelles tâches OpenSpec
ni une permission d’ignorer leurs dépendances. Le périmètre d’un cas et ses
autorisations doivent être validés avant exécution.

## 4. Format minimal de preuve à conserver par cas

- Identifiant Cxx, exigence/scénario source et statut NON EXÉCUTÉ/PASS/FAIL/
  BLOQUÉ/NON APPLICABLE motivé.
- Contrat/version, fournisseurs réels ou doubles nommés, profils et empreintes
  des artefacts et entrées pertinents.
- Commande complète réellement exécutée, mandat, permission et outil natifs,
  code de retour et résultats observés sans secret.
- Préconditions, identités/périmètres, corrélations/causalités et génération
  rapprochés ; aucun credential, clé ou contenu sensible consigné.
- Postconditions, état après panne/reprise, visibilité/durabilité, nettoyage
  et ressources éventuellement gardées pour réconciliation.
- Limites exactes : structure, simulation, intégration réelle, matériel et
  distribution distingués. Une compilation n’est pas une qualification.

## 5. Régressions historiques à reconsidérer

Les neuf recettes Agent retenues lors de la validation locale comportaient
211 cas, sur leurs sources et dépendances d’alors. Elles restent des preuves
historiques, non une exécution courante. Comparer les dépendances affectées
puis choisir les suites pertinentes : contrats, manifests, stockage,
C05, autorisation, service, adaptateur et supervision.

Une évolution de documentation n’impose pas de réexécuter tous les tests
produit. Un futur raccord de provider, conversion de données ou composition
réelle impose les contrôles fonctionnels touchés. Le rapport de vérification
de ces brouillons est conservé dans le checkpoint.

## 6. Traçabilité des retours intégrés

| Retour reçu | Cas précisés | État conservé |
| --- | --- | --- |
| PA01 A1 : absence de génération Agent et de binding serveur adopté/livré | C05, C18 | Point ouvert ; aucune formule à partir du journal/NV. |
| PA01 A2 : phases techniques adoptées, projection Agent non adoptée | C14–C16, C19 | Point ouvert ; aucune confirmation depuis SUCCEEDED. |
| PA01 A3 et C08 : aucune conversion UTC six décimales/seconde autorisée | C04 | Point ouvert ; octets signés conservés. |
| C08 : projection adoptée sans producteur/résolveur E4 opérationnel livré | C07, C18, C28 | Nominal différé jusqu’aux fournisseurs et preuves réels. |
| Inventaires PA01/C08/Z12 non assimilables à une qualification courante | C17, C19, C28 | Aucun PASS déduit de sources, métadonnées ou réponses. |

Les 28 identifiants et leur statut NON EXÉCUTÉ sont conservés. Les précisions
de résultat attendu ne constituent ni un nouveau contrat normatif, ni un test
exécuté, ni une décision de projection prise par PA10.

## 7. Preuve séparée P1 : frontières pures, sans provider

La [suite propre PA10](../../../tests/unit/test_agent_pa_native_contract_boundary.py)
comporte 17 méthodes réussies sur les codecs Python publics Agent et PA01.
La compilation est prouvée par msg_16e61eb830013XZxTtuV6RBqNG (exit 0) ;
l’exécution isolée par msg_16e62696f001rdExN2aL3irQJz (exit 0, 17 tests, zéro erreur).
La découverte combinée Agent passe aussi : msg_16e64ab90001YyEaEAnMl7LaX5,
99 tests dont ces 17, exit 0 ; aucun cumul artificiel de ces décomptes.
Ce résultat est distinct des cas C01–C28 : aucune de leurs garanties runtime
n’est déclarée exécutée ou qualifiée.

| Groupe structurel observé | Rapprochement au plan | Limite conservée |
| --- | --- | --- |
| Trois formes de requête, paramètres fermés, versions et types | Aspects structurels de C01 | Contexte et catalogue de fixture ; aucun profil opérationnel ou mandat réel. |
| Champs d’autorité injectés, octets/caractères UTF-8, booléens | Aspects de C02 et frontières d’entrée | Bornes synthétiques explicitement fournies ; pas de défaut production. |
| Requêtes/résultats Agent et natifs non interchangeables, six phases fermées | Garde structurelle liée à C14–C16 | Aucun mapping adopté ni état appliqué/confirmé fabriqué. |
| Génération Agent et deux compteurs d’ancre divergents de fixture | Contre-exemples liés à C05 | Aucun producteur ni binding réel ; valeurs entières identiques ne prouvent pas une autorité. |
| Horodatage AnchorSnapshot à six décimales et format Agent à la seconde | Écart de format lié à C04 | Aucun projecteur E4, signature vérifiée ou arrondi ; nominal C04 toujours différé. |
| Absence d’import des extensions natives, de Django et psycopg | Sous-processus isolé, fiable aussi dans la découverte combinée Agent | Ne constitue aucune qualification des providers absents. |

Commande exacte :

```text
PYTHONPATH=src /home/devops/datas/pixs/.venv/bin/python3 -B -m unittest discover -s tests/unit -p test_agent_pa_native_contract_boundary.py
```

A1–A5 et leurs décisions restent ouverts ; les 28 identifiants C01–C28 et
leur statut NON EXÉCUTÉ sont conservés. Les fixtures d’acteur/scope/génération
sont fournies au validateur de schéma, jamais dérivées comme une autorité
opérationnelle depuis NativeRequest/NativeResult. Aucun port permissif,
Subject fictif pré-PG ou adaptateur de transport n’est livré par cette suite.

## 8. État de coordination du 26 octobre 2026, sans exécution

Cet appendice conserve les 28 cas C01 à C28 NON EXÉCUTÉS et leurs dates. Il précise les conditions d'entrée avec les preuves actuelles, sans suite installée ni qualification.

- Adopté : B, retrait et INIT A avec formes 16, 17, 18 et 7 et contenus fermés ; résolveurs courants à réaliser. Contrat temps pixs.time.evidence 2.0.0 comme interface abstraite, avec SYNCHRONISE à 600 s et HORS_LIGNE conditionnel détaillé dans l'appendice de RACCORDS. Catalogue PA01 et D1A, D2A, D3A PA02.
- Écrit : confirmation C08, réponse d'échange 1.1, design PA01 et design PA10.
- Testé séparément, bilan déclaré par les propriétaires : C6 68 tests cités, C7 219 tests distincts cités avec composition 69 PASS en remplacement de 63, C08 117 tests cités avec F3 non exécuté, C2 44 tests cités ; sans somme entre campagnes différentes.
- Limites : A1 cible et génération, A2 phases, A3 projection conservant les octets signés à coordonner avec les propriétaires, A4 autorité, PZT, handlers et résultat durable ; C01 à C28 restent NON EXÉCUTÉS ; tâches 2.2 à 2.4 ouvertes.

## 9. Conditions actualisées après validation A1–A5 — 26 octobre 2026

Cette annexe conserve l'état antérieur à l'adoption des détails D ; voir le §10 pour les conditions documentaires désormais arrêtées et les réalisations toujours manquantes.

Le [registre des décisions adoptées](../add-pa-native-build-and-component-composition/DECISIONS_A1_A5.md)
remplace le statut d'arbitrage de principe ouvert des sections historiques.
Cette actualisation n'exécute aucun cas et ne modifie aucun résultat antérieur.

| Cas concernés | Décision acquise | Condition restant nécessaire avant exécution nominale |
| --- | --- | --- |
| C05/C18/C20/C21 | A1 : liaison persistante côté serveur, sans génération Agent déduite des compteurs PA ou d'une valeur cliente. | Structure et cycle de liaison spécifiés, producteur/persistance livrés, règles de concurrence et reprise qualifiables. |
| C14–C19 | A2 : deux niveaux et projection conditionnelle ; reçu/progrès et succès technique ne confirment pas automatiquement Agent. | Tableau exact des transitions, contrôles de preuve/refus, résultats et producteurs réels disponibles. |
| C04/C11 et contrôles temporels applicables | A3 : évolution Agent versionnée à six décimales, conservation des preuves signées et contrôle sur l'instant exact. | Numéro/schéma et migration définis puis livrés ; consommateurs compatibles et producteur temporel qualifiable. Le contrat 1.0.0 n'est pas modifié par cette annexe. |
| C07–C13/C17–C24 selon profil | A4 : vérifications spécialisées et autorités propriétaires courantes avant chaque effet. | Fournisseurs concrets et sélection authentique disponibles ; perte de source, révocation, refus et postconditions vérifiables. |
| C01–C28 applicables et promotion C28 | A5 : qualification progressive avec recette intégrée obligatoire, preuves attachées aux artefacts et revue explicite. | Exécutables réels et preuves complètes du périmètre sélectionné ; les paliers sur fixtures restent limités à leurs propres garanties. |

Les 28 cas restent **NON EXÉCUTÉS** dans cette recette. La validation des
orientations ne constitue ni réalisation, ni nouveau résultat de test,
ni livraison, ni activation ; aucune case de tâche n'est cochée ici.

## 10. Conditions après adoption D-A1/D-A2/D-A3/D-MIG — 26 octobre 2026

État conservé avant adoption S1/R1/F1 ; le §11 actualise les choix de
stockage, remise et fournisseurs sans exécution de ces cas.

Le [détail adopté](../add-pa-native-build-and-component-composition/DETAIL_A1_A2_A3.md)
fixe désormais le modèle logique A1, les transitions A2, Agent 2.0.0 et la
stratégie de migration. Il prépare les seize cas D01–D16, tous NON EXÉCUTÉS,
reliés à C01–C28. Les quatorze exigences et vingt-cinq scénarios détaillés
sont dans le delta PA01 et synchronisés à l'identique au
[canon pixs-agent](../../specs/pixs-agent/spec.md) sur demande explicite
complémentaire du développeur le 26 octobre 2026, sans réapplication des
autres deltas. Cette synchronisation reste documentaire.

| Cas concernés | Condition documentaire acquise | Condition de réalisation et de preuve encore requise |
| --- | --- | --- |
| C05/C18/C20/C21 | Modèle fermé et cycle D-A1, distinction lecture/mutation et idempotence. | Persistance physique, remise à PZT, résolveurs, concurrence et reprise réellement qualifiables. |
| C06/C14–C19 | Table D-A2 de transitions/projection, lecture et sujet distincts, unknown sans preuve d'origine embarquée, confirmation séparée. | Résultats durables, preuves d'origine/postcondition, lecteurs et déduplication effectifs. |
| C04/C11/C22/C27 | Agent 2.0.0 et codec validés, migration additive M0–M5, coexistence et retour définis. | Descripteurs, consommateurs, codecs/validateurs et migrations exécutables ; provenance, compatibilité, sources temporelles et restauration démontrées. |

Aucun de ces choix n'est à redemander comme s'il manquait. Les formes
physiques et fournisseurs encore ouverts restent à arrêter dans le cadre
validé. Les 28 cas C et les 16 cas D demeurent NON EXÉCUTÉS ; aucun test,
effet matériel/SQL, changement de contrat exécutable ou migration n'est
réalisé par cette annexe.

## 11. Conditions après adoption S1/R1/F1 — 27 octobre 2026

Le [registre adopté](../add-pa-native-build-and-component-composition/DECISIONS_S1_R1_F1.md)
fixe les choix de stockage et remise, les fournisseurs retenus et les
critères SRF01–SRF08, tous NON EXÉCUTÉS.

| Cas concernés | Choix acquis | Réalisation et preuve requises avant qualification |
| --- | --- | --- |
| C05/C18/C20/C21/C22/C27 ; D01/D02/D13–D15 | S1 : tables privées dédiées, contraintes typées, payload immuable, octets exacts, version/provenance et migration additive. | Schéma/modèles/migrations exacts, concurrence, rollback/restauration et maintien des octets/digests/générations prouvés sur PostgreSQL réel. |
| C09–C21/C23/C24 ; D01/D04–D11 | R1 : intention atomique, relais PBO après commit vérifié, gardes courantes, réconciliation avant réémission incertaine. | Intégration, relais et transport effectifs ; aucune émission avant commit, aucun effet déduit d'un ACK, aucune permission consommée recyclée ni double effet natif. |
| C04/C06/C09–C13/C15–C19/C24/C28 ; D03/D07/D12/D16 | F1 : fournisseurs par responsabilité, parcours ordinaire/initial distincts, producteurs temporels par processus. | Implémentations/versions et sélection authentique, refus sur fournisseur absent, résultats/postconditions/confirmation et temps courant réellement vérifiés. |

Ces cinq nouvelles exigences et douze scénarios sont inscrits dans les
deltas PA01 Agent/PZT et SYNCHRONISÉS À L'IDENTIQUE aux canons sur demande
explicite complémentaire du développeur le 27 octobre 2026, sans réapplication
des autres deltas. Leur validation et synchronisation documentaires ne valent
ni livraison, ni recette, ni autorisation
d'exécution produit. Les 28 cas C et les 16 cas D restent NON EXÉCUTÉS ;
aucune tâche de réalisation n'est cochée. Les critères SRF complètent ces
cas et les recettes intégrées A5, sans les remplacer ou fournir leurs preuves.

## 12. Détails et preuves attendues validés, sans exécution — 27 octobre 2026

Le [détail D-S1/D-R1/D-F1/D-SMIG](../add-pa-native-build-and-component-composition/DETAIL_S1_R1_F1.md)
est VALIDÉ par le développeur le 27 octobre 2026. Il fixe les choix physiques,
contrats et interfaces, la migration et les dix-huit vérifications
P-SRF01–P-SRF18, toutes PRÉVUES et NON EXÉCUTÉES. Dix-sept exigences et
trente-quatre scénarios sont inscrits dans les deltas PA01, NON SYNCHRONISÉS
au canon par cette inscription ; S1/R1/F1 conservent leur statut canonique.

| Conditions documentaires désormais acquises | Réalisations et preuves requises |
| --- | --- |
| D-S1 : huit tables/contraintes/index et codecs privés. | Modèles/dépôts/migrations, concurrence et octets exacts prouvés. |
| D-R1 : opérations du relais, commit, réservation et sept états locaux. | Relais/hébergement/profils, transport et reprise de panne réels ; pas d'effet déduit d'un ACK ou d'une réservation. |
| D-F1 : interfaces nommées et composition, résultat/origine/confirmation/temps. | Implémentations/version et sélection authentique, refus et postconditions réellement vérifiés. |
| D-SMIG : migration physique M0–M5 et retour/restauration. | Migration et classification sur copie autorisée, coexistence, conservation et rapprochement après restauration démontrés. |

Les preuves attendues portent sur schéma/contraintes et concurrence,
octets exacts, commit englobant et notification perdue, workers et callbacks
obsolètes, émission incertaine, mandat consommé, résultat/postconditions,
composition et temps, migration de copie, v1/v2 et restauration après émission.
Les événements d'IO et les réservations locales ne remplacent jamais
l'idempotence et les preuves natives PA/PZT.

Ces repères détaillent SRF01–SRF08 et les cas C/D/R existants ; ils ne les
remplacent pas. Les 28 cas C restent NON EXÉCUTÉS. Aucun test produit,
compilation, migration, effet SQL ou matériel n'est réalisé par ce complément,
aucune tâche cochée et aucune qualification fonctionnelle déduite.
