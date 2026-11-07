# PA/PZT — Décisions A1–A5 validées par le développeur

Date : 26 octobre 2026.

Actualisation du 27 octobre 2026 : [S1, R1 et F1](DECISIONS_S1_R1_F1.md)
sont VALIDÉS et inscrits dans les deltas PA01 ; leurs cinq exigences et douze
scénarios sont synchronisés à l'identique au canon sur demande explicite
complémentaire du développeur du même jour. Les choix de tables privées Agent, d'outbox/relais
PBO vers PZT et de fournisseurs par domaine sont acquis ; schémas exacts,
réalisations et preuves restent manquants.

Les [détails D-S1/D-R1/D-F1/D-SMIG](DETAIL_S1_R1_F1.md) sont validés
séparément le 27 octobre 2026 : huit tables et contraintes, contrat du relais,
interfaces privées et migration physique. Leurs dix-sept exigences et
trente-quatre scénarios sont inscrits dans les deltas PA01, NON SYNCHRONISÉS
au canon par cette inscription. Réalisations, profils opérationnels,
fournisseurs exécutables/versionnés et preuves restent manquants.

## 1. Autorité, portée et statut

Source : validation explicite du développeur dans le présent échange :
« Je valide tes recommandations pour A1–A5. Inscris ces décisions dans les
spécifications et le cadrage PA/PZT, sans implémentation ni production de code,
en distinguant les choix validés des réalisations et preuves encore manquantes. »

Les cinq orientations ci-dessous sont **VALIDÉES**. Leur adoption lève les
arbitrages de principe correspondants ; elle ne livre ni contrat détaillé
complet, ni fournisseur, ni exécutable, ni preuve fonctionnelle. La présente
écriture est exclusivement documentaire, sans code ni recette produit.

Les [détails A1/A2/A3 et de migration](DETAIL_A1_A2_A3.md) complètent le cadrage.
Le développeur valide explicitement D-A1, D-A2, D-A3 et D-MIG le 26 octobre
2026 ; cette nouvelle validation est distincte de celle des orientations.
Le modèle de liaison, les transitions précises, Agent 2.0.0, son codec et la
stratégie de migration sont désormais ADOPTÉS DOCUMENTAIREMENT. Leurs nouvelles
exigences sont inscrites dans le delta PA01 et synchronisées à l'identique
au canon pixs-agent sur demande explicite complémentaire du développeur le
26 octobre 2026, sans réalisation ni preuve produit.

Les exigences ajoutées figurent dans les deltas
[pixs-agent](specs/pixs-agent/spec.md) et [pzt](specs/pzt/spec.md) du dossier
PA01. Sur demande explicite complémentaire du développeur le 26 octobre 2026,
les neuf exigences et treize scénarios A1–A5 sont synchronisés à l'identique
dans les canons [pixs-agent](../../specs/pixs-agent/spec.md) et
[pzt](../../specs/pzt/spec.md). Les six exigences Cython déjà synchronisées
conservent leur contenu et leur statut antérieurs ; elles ne sont ni
réappliquées ni requalifiées ici. Cette synchronisation reste documentaire.

## 2. A1 — Liaison persistante côté serveur

### Choix validé

La gestion ordinaire utilise une liaison persistante côté serveur entre
l'opération et le contexte Agent, d'une part, et les références techniques
PA/C08, d'autre part. Agent conserve la propriété de sa génération ; PA
conserve ses compteurs natifs indépendants. L'opération, la cible, le scope,
la génération et les références techniques sont rapprochés sous contrôle
des propriétaires. Une valeur fournie par le client ne suffit pas à établir
la liaison. Une liaison absente, périmée ou divergente est refusée.

L'amorçage avant PostgreSQL conserve son contexte initial C08/PA, sans créer
de génération Agent fictive. Aucun alias n'est établi entre génération Agent,
`registry_generation_ref`, époque, séquence ou numéro de lecture natif.

### Réalisation et preuves encore manquantes

Le [détail A1 validé D-A1](DETAIL_A1_A2_A3.md) fixe le modèle logique de liaison,
sa persistance propriétaire, son cycle et les règles de concurrence/reprise.
S1 retient les tables PostgreSQL privées dédiées et R1 l'outbox Agent avec
relais PBO vers PZT. Les schémas exacts, intégrations, réalisations et preuves
restent à produire avec PA01/C08/PA10.
Aucun champ n'est ajouté aux messages PA existants par cette décision.
Les cas C05, C18, C20 et C21 attendent ces éléments et leurs preuves réelles.

## 3. A2 — Deux niveaux et projection conditionnelle

### Choix validé

Les six phases techniques PA restent distinctes des issues de gestion Agent.
La projection est explicite et conditionnelle ; une correspondance nominale
de libellés ne vaut ni preuve d'origine, ni effet, ni confirmation.

| Phase native | Conséquence de principe validée |
| --- | --- |
| RECEIVED | Accusé de réception seul, sans application ni confirmation déduite. |
| RUNNING | Progression technique, sans fait appliqué ni confirmation déduite. |
| SUCCEEDED | Succès technique durable vérifié ; confirmation Agent seulement après ses contrôles propres d'origine et de postcondition. |
| FAILED | Échec connu, à rapprocher du contexte et des preuves propriétaires. |
| IN_DOUBT | Incertitude conservée, avec réconciliation avant tout nouvel effet. |
| BLOCKED | Refus de précondition, sans fabriquer un échec d'exécution. |

### Réalisation et preuves encore manquantes

Le [détail A2 validé D-A2](DETAIL_A1_A2_A3.md) fixe les transitions, conditions
de projection, preuves requises et refus. Les fournisseurs concrets de lecture
et de déduplication restent à raccorder avec PA01/PA10. Les formes existantes
Agent 1.0.0 et les contraintes de ses issues, notamment `unknown`, ne sont
pas modifiées implicitement. Le registre natif et ses preuves ne sont pas
effacés ou réécrits pour convenir à un résumé Agent.
Les cas C14–C19 et les scénarios de reprise attendent leurs producteurs réels.

## 4. A3 — Précision native et évolution versionnée Agent

### Choix validé

La frontière Agent évoluera par une nouvelle version acceptant les six
décimales natives. Les octets signés et les preuves d'origine restent intacts.
Les contrôles utilisent l'instant exact et les preuves temporelles du
fournisseur compétent. Un affichage moins précis ne participe pas aux
décisions de sécurité. Aucun arrondi ni troncature ne remplace l'instant
de contrôle.

Le contrat Agent 1.0.0 reste inchangé jusqu'à une migration explicitement
définie. Le contrat générique de temps et les politiques déjà adoptées
restent ceux de leurs sources propriétaires ; aucun délai, seuil ou
producteur concret n'est choisi par cette décision.

### Réalisation et preuves encore manquantes

Le [détail A3 validé D-A3 et D-MIG](DETAIL_A1_A2_A3.md) fixe Agent 2.0.0,
ses champs temporels, le codec de contenu et la migration additive avec
coexistence et retour arrière. Le schéma physique, le plan exécutable et
les réalisations restent à produire par PA10 avec PA01/C08/Z12. La livraison d'un producteur
temporel utilisable et ses preuves d'acquisition courante restent nécessaires.
Le cas C04 ne devient pas exécutable par la seule adoption de ce principe.

## 5. A4 — Interfaces spécialisées et propriétaires conservés

### Choix validé

Les vérifications d'autorité restent portées par des interfaces spécialisées,
composées explicitement dans le parcours ; aucune façade unique nouvelle
n'est choisie comme autorité.

| Domaine | Propriétaire ou fournisseur compétent |
| --- | --- |
| Confiance cryptographique applicable | Z12 et ses fournisseurs. |
| Canal, relation et routage autorisés | PZT. |
| Admission technique, gardes et préconditions avant effet | PA. |
| Intention et confirmation opérateur | C08. |
| Origine des observations et confirmation de gestion | Agent et les fournisseurs de ses ports de confiance. |
| Condition temporelle au point d'usage | Producteur temporel sélectionné par composition. |

Les conditions requises sont vérifiées à nouveau au point d'usage avant
chaque effet. L'absence d'un fournisseur requis ou d'une preuve courante
entraîne un refus. Une signature correcte ne remplace pas les autres
conditions d'admission. Le Kernel conserve ses mécanismes génériques,
sans devenir une autorité métier ou temporelle.

### Réalisation et preuves encore manquantes

F1 sélectionne les familles de fournisseurs par domaine, décrites dans
[le registre S1/R1/F1](DECISIONS_S1_R1_F1.md). Les symboles exécutables,
versions, sélection authentique, liaisons et fonctionnement effectif restent
à identifier, réaliser, raccorder et qualifier. Les interfaces abstraites existantes ne livrent pas ces
fournisseurs. Le contrôle avant effet, la révocation et les refus sur perte
de source restent à démontrer dans les cas C09–C13 et C17–C24 applicables.

## 6. A5 — Qualifications progressives et recette intégrée obligatoire

### Choix validé

La qualification progresse par quatre paliers distincts :

1. Chaîne Cython, constructeur et liaison.
2. Véritables exécutables : entrées, modes, lifecycle et isolation.
3. Parcours intégré : transport, autorités, effets et résultats durables réels.
4. Distributions et plateformes effectivement sélectionnées.

Une recette intégrée reste obligatoire. Chaque résultat est lié à ses
sources, versions, empreintes, commandes, postconditions et nettoyage.
Les cas applicables C01–C28 et R01–R68 restent à couvrir. La promotion exige
une revue explicite des preuves ; une réussite partielle ne clôture pas la
recette intégrée ni une autre plateforme.

### Réalisation et preuves encore manquantes

Les preuves historiques de construction restent limitées à leurs artefacts
et à leurs objets ou programmes de fixture. Elles ne qualifient pas les
exécutables fonctionnels. Les cas produit, leurs environnements, effets,
recettes et preuves de distribution restent à préparer puis exécuter sous
leurs autorisations propres. Aucun test nouveau n'est exécuté ici.

## 7. État résultant et traçabilité

| Dimension | État après inscription |
| --- | --- |
| Orientations A1–A5 | VALIDÉES par le développeur. |
| Canon OpenSpec A1–A5 | SYNCHRONISÉ : neuf exigences et treize scénarios, sans réapplication des six exigences Cython antérieures. |
| Détails D-A1/D-A2/D-A3/D-MIG | VALIDÉS DOCUMENTAIREMENT et SYNCHRONISÉS au canon pixs-agent : quatorze exigences et vingt-cinq scénarios, identiques au delta PA01 et aux modèles détaillés. |
| Complément S1/R1/F1 | VALIDÉ DOCUMENTAIREMENT et SYNCHRONISÉ À L'IDENTIQUE au canon le 27 octobre 2026 sur demande explicite complémentaire : cinq exigences et douze scénarios, sans réalisation ni preuve fonctionnelle. |
| Détails D-S1/D-R1/D-F1/D-SMIG | VALIDÉS DOCUMENTAIREMENT le 27 octobre 2026 et INSCRITS dans les deltas PA01 ; NON SYNCHRONISÉS au canon par cette inscription. |
| Éléments restant à réaliser ou qualifier | Modèles/migrations du schéma physique adopté, intégration/hébergement de l'outbox/relais et profils opérationnels, implémentations/versions des fournisseurs, descripteurs/codecs/validateurs et preuves. |
| Nouveaux raccordements fonctionnels et fournisseurs | NON LIVRÉS par cette inscription. |
| Nouvelles preuves fonctionnelles | ABSENTES ; aucun cas produit exécuté ici. |
| Qualification fonctionnelle globale PA/PZT | BLOQUÉE par les réalisations et preuves manquantes. |

Le [cadrage fonctionnel](CADRAGE_FONCTIONNEL.md) et la
[matrice PA10](../separate-pa-pzt-and-pbo-management-modules/RACCORDS.md)
distinguent cet état des constats historiques antérieurs à la validation.
Les [cas PA10](../separate-pa-pzt-and-pbo-management-modules/RECETTE_RACCORDS.md)
restent NON EXÉCUTÉS. Les cases de réalisation, la livraison, l'activation,
Git et l'archivage ne sont pas modifiés par ces décisions documentaires.

## 8. Adoption explicite des détails D-A1, D-A2, D-A3 et D-MIG

Source du 26 octobre 2026 : « Je valide les propositions D-A1, D-A2, D-A3 et
D-MIG. Inscris ces décisions dans les spécifications et le cadrage PA/PZT,
sans implémentation ni production de code. »

Les quatorze exigences et vingt-cinq scénarios détaillés sont inscrits dans
le [delta pixs-agent PA01](specs/pixs-agent/spec.md), avec leurs modèles et
tables de comportement validés. Sur demande explicite complémentaire du
développeur le 26 octobre 2026, ils sont synchronisés à l'identique dans le
[canon pixs-agent](../../specs/pixs-agent/spec.md), sans réapplication des
autres deltas. Les exigences canoniques antérieures, le canon pzt et le
contrat exécutable Agent 1.0.0 restent inchangés ; les cas produit demeurent NON EXÉCUTÉS et les
tâches de réalisation restent ouvertes.
