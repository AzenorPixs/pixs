# PA01 — Composition et compilation des trois binaires PA et de PZT

## Pourquoi

Le canon distingue trois binaires PA et six modes, plus le binaire indépendant PZT et son mode pzt-daemon ; le README indique que l’implémentation, la qualification et les artefacts restent à réaliser. Le contrôle de présence ciblé des sources n’est pas une recette de plateforme.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

## Modifications proposées

Catalogue fermé au build, quatre exécutables colivrés, six modes PA et un mode PZT, Cython pour les trois binaires PA et pour PZT indépendant ; qualifier versions, ABI et runtime avant installation des outils.

Décision du développeur du 26 octobre 2026 : sélectionner la dernière version stable publiée de Cython au début de chaque campagne de qualification PA01, puis verrouiller sa version exacte pendant cette campagne. Toute actualisation exige un alignement des déclarations, contrôles et tests concernés, puis une qualification de la nouvelle chaîne.

Le complément validé ensuite le 26 octobre 2026 définit une enveloppe TOML de
métadonnées de campagne PA01 équivalente à celle de PBO : identité, sélection
officielle datée, relevé conservé, distributions et empreintes. Le verrou de
référence reste `toolchain.cython` du profil de build existant ; l'enveloppe
doit en reprendre exactement la valeur, sans modifier le schéma de ce profil.

Décisions A1–A5 validées le 26 octobre 2026 : liaison persistante côté serveur, phases natives et issues Agent séparées avec projection conditionnelle, évolution temporelle Agent versionnée à six décimales, interfaces spécialisées d'autorité et qualification progressive avec recette intégrée obligatoire. Le [registre commun](DECISIONS_A1_A5.md) distingue ces orientations adoptées des détails contractuels, réalisations et preuves restant à produire.

Les détails [D-A1/D-A2/D-A3/D-MIG](DETAIL_A1_A2_A3.md) sont validés explicitement le 26 octobre 2026 : AgentPaBinding 1.0.0, transitions et projection précises, Agent 2.0.0 et son codec de contenu, migration additive M0–M5. Leur adoption reste documentaire, sans réalisation ni exécution de migration ou recette produit.

## Capacités

Le développeur valide [D-S1/D-R1/D-F1/D-SMIG](DETAIL_S1_R1_F1.md) le
27 octobre 2026. Le delta pixs-agent reçoit seize exigences et trente-deux
scénarios détaillés ; le delta pzt reçoit une exigence et deux scénarios
sur l'interface privée du transport. Ces seuls nouveaux détails sont
NON SYNCHRONISÉS au canon par cette inscription. Schéma physique, contrat
du relais, interfaces privées et migration sont adoptés documentairement ;
aucune réalisation, DDL, migration exécutée ou preuve produit n'est livrée.

Le 27 octobre 2026, [S1/R1/F1](DECISIONS_S1_R1_F1.md) sont validés :
tables PostgreSQL privées dédiées Agent, outbox transactionnelle et relais
PBO vers PZT, fournisseurs par domaine. Quatre exigences et dix scénarios
sont ajoutés au delta pixs-agent, une exigence et deux scénarios au delta
pzt. Ces seuls nouveaux ajouts sont SYNCHRONISÉS À L'IDENTIQUE aux deux
canons sur demande explicite complémentaire du développeur du même jour,
sans réapplication des autres deltas. Les choix et leurs détails sont acquis ; modèles, intégration, réalisations
et preuves manquantes sont distingués dans le registre et le cadrage.

### Capacités nouvelles

Aucune nouvelle capacité. Ce dossier conserve la réalisation et la qualification des contrats existants, complétées par la politique Cython par campagne et les orientations A1–A5 adoptées le 26 octobre 2026.

### Capacités modifiées

`pixs-agent` : le [delta de spécification](specs/pixs-agent/spec.md) ajoute la sélection de la dernière stable Cython et son verrouillage par campagne PA01. Ses six exigences et six scénarios sont synchronisés au canon sur demande explicite du développeur le 26 octobre 2026, sans réapplication des deltas déjà synchronisés. `requirements.md` conserve les copies et empreintes historiques des blocs sources ; le dossier déclare désormais `skip_specs: false`.

Le complément d'enveloppe ajoute quatre exigences et six scénarios au même
delta pixs-agent. Ces seuls ajouts sont synchronisés au canon sur validation
explicite du développeur le 26 octobre 2026, sans réapplication des deltas déjà
synchronisés ni modification du constructeur, du validateur ou de `pyproject.toml`.

Les nouvelles exigences A1/A2/A3/A5 du même delta précisent les orientations validées de liaison, projection, évolution temporelle et qualification ; `pzt` reçoit un [delta A4](specs/pzt/spec.md) sur les vérifications spécialisées et l'autorité courante avant effet. Les neuf exigences et treize scénarios A1–A5 sont synchronisés à l'identique au canon sur demande explicite du développeur le 26 octobre 2026, sans réappliquer les exigences Cython ou d'autres deltas. Cette synchronisation ne modifie pas les contrats exécutables existants et ne fournit aucune réalisation ou preuve fonctionnelle.

Le delta pixs-agent reçoit en outre quatorze exigences et vingt-cinq scénarios détaillés D-A1/D-A2/D-A3/D-MIG, avec les modèles et tables validés. Ces seuls détails sont synchronisés à l'identique au canon pixs-agent sur demande explicite complémentaire du développeur le 26 octobre 2026, sans réapplication des autres deltas ; les orientations A1–A5 et la politique Cython déjà canoniques conservent leur contenu et leur statut.

Le complément de [preuve officielle datée](PREUVE_SELECTION_PA01.md) définit
la collecte contrôlée, le dossier figé et son admission après revue explicite
dans un registre protégé indépendant du demandeur de construction. Il ajoute
deux exigences et six scénarios au delta pixs-agent ; ces seuls ajouts sont
synchronisés au canon sur validation explicite du développeur le 26 octobre
2026, sans réapplication des deltas déjà synchronisés, code, implémentation
ni preuve réelle produite par cette opération documentaire.

## Sélection et périmètre autorisé

Le profil `pbo-p0-debian-local-v1` sélectionne le sous-ensemble nécessaire à
la préparation PostgreSQL par PA système via PZT local, selon le
[canon de composition](../../specs/reference-composition/spec.md) et le parcours
[C08](../add-installation-and-first-configuration/proposal.md). Les obligations
de ce dossier applicables à ce parcours doivent être réalisées et qualifiées.
Les autres rôles PA et le réseau PZT distant restent conditionnés au profil
sélectionné ; cette préparation documentaire ne les active ni ne les qualifie.

La demande actuelle porte exclusivement sur les documents de préparation. Aucun code, test produit, serveur, accès fournisseur, secret, migration, dépendance, configuration système, publication, Git ou archivage n’est exécuté par ce dossier.

## Dépendances

- [define-first-installable-pbo-profile](../archive/2026-10-18-define-first-installable-pbo-profile/proposal.md).
- [activate-reference-runtime-composition](../archive/2026-10-21-activate-reference-runtime-composition/proposal.md).



## Impact de réalisation future

Couche locale séparée de Django/PostgreSQL et sans autorité métier. Composer les opérations au build par contrats, dispatch explicite et identité du mode ; isoler comptes/sessions, handles et générations. Lier mandats, contexte, effets et résultats observés ; communiquer avec PBO uniquement via PZT. Les trois binaires PA (Cython) et PZT indépendant (Cython) restent colivrés, sous gestion respective de pixs.agent et pixs.pzt.

## Critère de sortie de réalisation future

Contenu et responsabilités exacts ; construction reproductible par cible ; aucune compilation assimilée à une recette fonctionnelle.

## Décisions restant à valider

Les choix D1–D9, la politique Cython par campagne, les orientations A1–A5 et les détails D-A1/D-A2/D-A3/D-MIG sont adoptés dans [design.md](design.md), le [registre A1–A5](DECISIONS_A1_A5.md) et le [détail validé](DETAIL_A1_A2_A3.md). Les décisions complémentaires [S1/R1/F1](DECISIONS_S1_R1_F1.md) sont validées et synchronisées au canon le 27 octobre 2026 sur demande explicite complémentaire. Tables privées Agent, outbox/relais vers PZT et fournisseurs par domaine sont donc choisis ; les détails D-S1/D-R1/D-F1/D-SMIG sont désormais validés dans le delta PA01, sans synchronisation de ces nouveaux détails au canon. Modèles, intégration, implémentations exécutables et versions, codecs, validateurs, migrations et preuves restent à produire. Les détails D conservent leur synchronisation au canon du 26 octobre 2026. La chaîne et la distribution restent à qualifier par campagne et cible ; aucune nouvelle version CPython, installation ou réalisation n'est autorisée par cette opération documentaire.
