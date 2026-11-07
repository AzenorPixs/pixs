# Contrôle de couverture avant déplacement — O38

Plan ACL-PIXS-2026-10-31-E3-R1. Complément A explicitement validé : contrôle de couverture avant tout déplacement, conservation de tout travail restant. Relevé du 31 octobre 2026.

## Portée et résultat

5 exigences de l'ancienne préparation sont rattachées au référentiel courant ci-dessous. Chaque ligne indique son devenir, les critères compatibles maintenus et une ou plusieurs tâches encore non cochées. Le classement AU_CANON_IDENTIQUE signifie présence du contrat, jamais réalisation. CIBLE_ACTUALISEE signifie modification décidée du contrat, jamais oubli de son implémentation. RATTACHEMENT_EXPLICITE conserve les détails compatibles comme critères à vérifier sous les contrats courants.

Le classement ne résulte pas de la seule égalité d'un titre : les corps et scénarios ont été relus. Les simples marqueurs de sections de delta ont été exclus de la comparaison. Les clauses remplacées sont indiquées séparément. Aucune exigence résiduelle n'est laissée sans propriétaire de réalisation ; aucun besoin compatible n'est abandonné par son rangement historique.

## Correspondance complète

| Ancienne exigence | Disposition | Référentiel courant | Tâches futures conservées |
|---|---|---|---|
| auth-managed-kerberos — KDC propre indépendant des sources externes | RATTACHEMENT_EXPLICITE | [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md) — KZT obligatoire et backend OpenLDAP | 2.1, 2.2, 3.1 |
| auth-managed-kerberos — Principals liés aux identités canoniques | RATTACHEMENT_EXPLICITE | [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md) — Realm propre et mappings explicites | 2.1, 2.3, 3.2 |
| auth-managed-kerberos — Protection et amorçage des clés Kerberos | RATTACHEMENT_EXPLICITE | [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md) — Protection et récupération des clés Kerberos | 1.2, 2.2, 3.2 |
| auth-managed-kerberos — Tickets bornés et limites de révocation explicites | RATTACHEMENT_EXPLICITE | [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md) — Expiration stricte et état courant | 2.2, 2.3, 3.2, 3.3 |
| auth-managed-kerberos — Reprise du KDC sans résurrection des accès | RATTACHEMENT_EXPLICITE | [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md) — Restauration sans résurrection | 1.2, 2.2, 3.2 |

## Détails et critères maintenus par exigence

### 1. KDC propre indépendant des sources externes

- Source historique prévue : [auth-managed-kerberos](historique-deltas-avant-e3/auth-managed-kerberos/spec.md). Ancien chemin : `specs/auth-managed-kerberos/spec.md`.
- Empreinte du bloc ancien normalisé : `c9d4856d0689e177b809facac37ebc580cbbe5f79861f705e7eb16915049b180` ; fichier entier à conserver : `0cfe3178b39dfb04931619b850787ab6c29759c8cb6b3fc14e25675ba2f4477c`.
- Contrat courant : `auth-managed-kerberos` — KZT obligatoire et backend OpenLDAP.
- Travail et critères compatibles à maintenir : Conserver le service propre sans connecteur externe, lifecycle et activation autorisée ; qualifier MIT/OpenLDAP dans le Domaine, jamais changer de backend implicitement.
- Clauses remplacées / limites : Le parcours KDC sans LDAP n’est plus un profil Domaine V1 ; le libellé historique de tâche 3.1 est conservé mais son critère courant exige le backend OpenLDAP choisi.
- Rattachement actif : tâches 2.1, 2.2, 3.1 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 2. Principals liés aux identités canoniques

- Source historique prévue : [auth-managed-kerberos](historique-deltas-avant-e3/auth-managed-kerberos/spec.md). Ancien chemin : `specs/auth-managed-kerberos/spec.md`.
- Empreinte du bloc ancien normalisé : `eb7e9e73fe5121158c2ab11296b22f3af340e16bf84d738ed5a8c11676228caf` ; fichier entier à conserver : `0cfe3178b39dfb04931619b850787ab6c29759c8cb6b3fc14e25675ba2f4477c`.
- Contrat courant : `auth-managed-kerberos` — Realm propre et mappings explicites.
- Travail et critères compatibles à maintenir : Conserver les mappings Auth persistants de principals/services et leur périmètre, sans identité ou droit issu d’un nom ou ticket.
- Clauses remplacées / limites : Aucune clause abandonnée ; détails compatibles conservés comme critères de réalisation.
- Rattachement actif : tâches 2.1, 2.3, 3.2 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 3. Protection et amorçage des clés Kerberos

- Source historique prévue : [auth-managed-kerberos](historique-deltas-avant-e3/auth-managed-kerberos/spec.md). Ancien chemin : `specs/auth-managed-kerberos/spec.md`.
- Empreinte du bloc ancien normalisé : `e2c662a7d1ae7ae7913d45180030f2058e6122ad08b195ff77fa96692899ddc9` ; fichier entier à conserver : `0cfe3178b39dfb04931619b850787ab6c29759c8cb6b3fc14e25675ba2f4477c`.
- Contrat courant : `auth-managed-kerberos` — Protection et récupération des clés Kerberos.
- Travail et critères compatibles à maintenir : Conserver clé maîtresse, clés de principals et keytabs protégées, droits minimaux, absence de dépendance circulaire à un KZT à ouvrir et refus de produire ses clés depuis le seul hash PG.
- Clauses remplacées / limites : Aucune clause abandonnée ; détails compatibles conservés comme critères de réalisation.
- Rattachement actif : tâches 1.2, 2.2, 3.2 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 4. Tickets bornés et limites de révocation explicites

- Source historique prévue : [auth-managed-kerberos](historique-deltas-avant-e3/auth-managed-kerberos/spec.md). Ancien chemin : `specs/auth-managed-kerberos/spec.md`.
- Empreinte du bloc ancien normalisé : `e8d8206aa3393fbb737f3cc57d2b8b61a97b1a7b5e85f10cd0c834cc424d1a83` ; fichier entier à conserver : `0cfe3178b39dfb04931619b850787ab6c29759c8cb6b3fc14e25675ba2f4477c`.
- Contrat courant : `auth-managed-kerberos` — Expiration stricte et état courant.
- Travail et critères compatibles à maintenir : Conserver confiance des realms, temps, durées, renouvellement et effet sur les tiers explicites. Refuser nouvelle émission/renouvellement après retrait et tout accès sensible non admissible malgré un ticket ; qualifier les clients tiers.
- Clauses remplacées / limites : Aucune clause abandonnée ; détails compatibles conservés comme critères de réalisation.
- Rattachement actif : tâches 2.2, 2.3, 3.2, 3.3 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 5. Reprise du KDC sans résurrection des accès

- Source historique prévue : [auth-managed-kerberos](historique-deltas-avant-e3/auth-managed-kerberos/spec.md). Ancien chemin : `specs/auth-managed-kerberos/spec.md`.
- Empreinte du bloc ancien normalisé : `4554a32e112fb096611988781a7dd6b3a531b3c27ba647f4578a1eec4028a514` ; fichier entier à conserver : `0cfe3178b39dfb04931619b850787ab6c29759c8cb6b3fc14e25675ba2f4477c`.
- Contrat courant : `auth-managed-kerberos` — Restauration sans résurrection.
- Travail et critères compatibles à maintenir : Conserver réconciliation clés, mappings et retraits, readiness conditionnée au temps et secrets vérifiables ; compléter par les deux parcours critiques choisis sans recréer de droit retiré.
- Clauses remplacées / limites : Aucune clause abandonnée ; détails compatibles conservés comme critères de réalisation.
- Rattachement actif : tâches 1.2, 2.2, 3.2 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

## Travail restant explicitement actif

Sur 9 tâches d’origine, 0 restent cochées historiquement et 9 restent non cochées. Leur contenu et leur état sont préservés. La liste suivante est une vue des tâches sources, pas un nouveau registre ou une deuxième série de cases.

| Tâche | Sous-lot conservé | Libellé source | État |
|---|---|---|---|
| 1.1 | O38-SL01 | 1.1 Revoir et adopter les deltas sous autorisation distincte ; confirmer dépendances, contrats et paramètres ouverts. | À FAIRE ; preuve future requise |
| 1.2 | O38-SL02 | 1.2 Définir modèles propriétaires, migrations, secrets, reprise et plans de retrait sans déplacer les contrats Core existants. | À FAIRE ; preuve future requise |
| 2.1 | O38-SL03 | 2.1 Déclarer le sous-module, les plans de gestion et les liaisons de principals par contrats publics. | À FAIRE ; preuve future requise |
| 2.2 | O38-SL04 | 2.2 Intégrer le lifecycle du KDC choisi, secrets protégés et contrôles de nouvelle émission/renouvellement. | À FAIRE ; preuve future requise |
| 2.3 | O38-SL05 | 2.3 Intégrer la vérification de tickets et les contrôles courants sans déléguer l'autorisation Pixs. | À FAIRE ; preuve future requise |
| 3.1 | O38-SL06 | 3.1 Qualifier KDC seul puis avec OpenLDAP si ce backend est sélectionné, sans source externe installée. | À FAIRE ; preuve future requise |
| 3.2 | O38-SL07 | 3.2 Tester temps invalide, realm non approuvé, keytab expirée, retrait, ticket encore valide et restauration. | À FAIRE ; preuve future requise |
| 3.3 | O38-SL08 | 3.3 Vérifier syntaxe, contrôles configurés, audit sans secret, isolation tenant et limites de révocation sur l'artefact réel. | À FAIRE ; preuve future requise |
| 3.4 | O38-SL09 | 3.4 Examiner diff et preuves ; synchroniser, archiver, engager Git ou publier seulement sous autorisation distincte. | À FAIRE ; preuve future requise |

Le libellé historique 3.1 « KDC seul puis avec OpenLDAP si sélectionné » reste un repère ; son critère Domaine courant est MIT Kerberos avec backend OpenLDAP obligatoire. Aucun parcours sans LDAP n’est réintroduit.

## Contrôles et limites

Avant déplacement : existence des contrats cibles, rattachements à des tâches ouvertes et empreintes des 21 fichiers contrôlés. Après déplacement : égalité des octets, mise à jour des liens, même contenu et mêmes cases des tâches, mêmes identifiants de sous-lots et validation OpenSpec à vérifier. Aucun code, test produit, service, migration, archive ou publication n’est exécuté par ce contrôle documentaire.

## Contrôle après déplacement

Les empreintes des fichiers entiers ont été vérifiées après déplacement et sont identiques aux sources. Les 21 déplacements conservent les octets ; les liens fonctionnels entrants ont été actualisés dans les dossiers concernés. Les tâches, cases et identifiants de sous-lots restent inchangés. Aucun besoin compatible n’est déclaré réalisé par ce rangement.

## Revue restante de la tâche 1.1 — reprise ACSM

La tâche 1.1 conserve son libellé et sa case ouverte. Elle porte sur la revue des contrats canoniques courants, de la présente couverture et des paramètres nécessaires à la suite ; elle ne demande pas l'adoption des fichiers historiques ni une nouvelle synchronisation au canon. Son critère courant et les preuves futures exigées sont précisés dans [tasks.md](tasks.md). Aucun autre travail restant ni état historique n'est modifié.
