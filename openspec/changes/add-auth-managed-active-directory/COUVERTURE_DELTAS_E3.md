# Contrôle de couverture avant déplacement — O37

Plan ACL-PIXS-2026-10-31-E3-R1. Complément A explicitement validé : contrôle de couverture avant tout déplacement, conservation de tout travail restant. Relevé du 31 octobre 2026.

## Portée et résultat

6 exigences de l'ancienne préparation sont rattachées au référentiel courant ci-dessous. Chaque ligne indique son devenir, les critères compatibles maintenus et une ou plusieurs tâches encore non cochées. Le classement AU_CANON_IDENTIQUE signifie présence du contrat, jamais réalisation. CIBLE_ACTUALISEE signifie modification décidée du contrat, jamais oubli de son implémentation. RATTACHEMENT_EXPLICITE conserve les détails compatibles comme critères à vérifier sous les contrats courants.

Le classement ne résulte pas de la seule égalité d'un titre : les corps et scénarios ont été relus. Les simples marqueurs de sections de delta ont été exclus de la comparaison. Les clauses remplacées sont indiquées séparément. Aucune exigence résiduelle n'est laissée sans propriétaire de réalisation ; aucun besoin compatible n'est abandonné par son rangement historique.

## Correspondance complète

| Ancienne exigence | Disposition | Référentiel courant | Tâches futures conservées |
|---|---|---|---|
| auth-managed-active-directory — Sous-module Active Directory propre optionnel | RATTACHEMENT_EXPLICITE | [auth-managed-active-directory](../../specs/auth-managed-active-directory/spec.md) — Produit et capacité démontrés avant activation | 1.2, 2.1, 3.1 |
| auth-managed-active-directory — Référentiel PostgreSQL et domaine technique distincts | RATTACHEMENT_EXPLICITE | [auth-managed-directory](../../specs/auth-managed-directory/spec.md) — PG source Core et LDAP opérationnel | 1.3, 2.2, 3.2 |
| auth-managed-active-directory — Identifiants de domaine liés explicitement à Core | RATTACHEMENT_EXPLICITE | [authentication](../../specs/authentication/spec.md) — Identifiant externe canonique et liaison explicite | 1.3, 2.2, 3.2 |
| auth-managed-active-directory — Composition coordonnée des services de domaine | RATTACHEMENT_EXPLICITE | [auth-managed-active-directory](../../specs/auth-managed-active-directory/spec.md) — Domaine Pixs commun et objectif Windows V1 | 1.2, 2.1, 2.3, 3.1 |
| auth-managed-active-directory — Moyens et secrets AD sous contrôle déclaré | RATTACHEMENT_EXPLICITE | [authentication](../../specs/authentication/spec.md) — Propriété des données Auth et protection des justificatifs | 1.3, 2.3, 3.2 |
| auth-managed-active-directory — Révocation et restauration du domaine vérifiables | RATTACHEMENT_EXPLICITE | [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md) — Restauration sans résurrection | 2.3, 3.2 |

## Détails et critères maintenus par exigence

### 1. Sous-module Active Directory propre optionnel

- Source historique prévue : [auth-managed-active-directory](historique-deltas-avant-e3/auth-managed-active-directory/spec.md). Ancien chemin : `specs/auth-managed-active-directory/spec.md`.
- Empreinte du bloc ancien normalisé : `2a61be7f5821adda38463292f8127c09582c9db8a78ee79141d83dab4a6c8a36` ; fichier entier à conserver : `eec67ef656bea8134182a61a34f7202826705e1653066f35db36cf41254d7b07`.
- Contrat courant : `auth-managed-active-directory` — Produit et capacité démontrés avant activation.
- Travail et critères compatibles à maintenir : Conserver la sélection explicite de pixs.auth.directory.ad, le lifecycle et la santé, sans connecteur externe imposé ; le profil pré-domaine PG reste utilisable.
- Clauses remplacées / limites : Aucune clause abandonnée ; détails compatibles conservés comme critères de réalisation.
- Rattachement actif : tâches 1.2, 2.1, 3.1 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 2. Référentiel PostgreSQL et domaine technique distincts

- Source historique prévue : [auth-managed-active-directory](historique-deltas-avant-e3/auth-managed-active-directory/spec.md). Ancien chemin : `specs/auth-managed-active-directory/spec.md`.
- Empreinte du bloc ancien normalisé : `2a5d4b6afa3e3bddab9d61c65dfdde048760f02712aeea8e28bc462fb58b54ee` ; fichier entier à conserver : `eec67ef656bea8134182a61a34f7202826705e1653066f35db36cf41254d7b07`.
- Contrat courant : `auth-managed-directory` — PG source Core et LDAP opérationnel.
- Travail et critères compatibles à maintenir : Conserver la séparation du stockage technique AD et de Core/Auth, les flux déclarés et l’absence de mutation Core par simple observation native.
- Clauses remplacées / limites : Seule l’exception de migration Core vers LDAP souverain est remplacée par PG toujours souveraine Core ; O41 reste non sélectionnable.
- Rattachement actif : tâches 1.3, 2.2, 3.2 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 3. Identifiants de domaine liés explicitement à Core

- Source historique prévue : [auth-managed-active-directory](historique-deltas-avant-e3/auth-managed-active-directory/spec.md). Ancien chemin : `specs/auth-managed-active-directory/spec.md`.
- Empreinte du bloc ancien normalisé : `f8cab5ea1809a7ea6fa072ad54f55df31e7904ac3082b1127dc787f1ae6588f8` ; fichier entier à conserver : `eec67ef656bea8134182a61a34f7202826705e1653066f35db36cf41254d7b07`.
- Contrat courant : `authentication` — Identifiant externe canonique et liaison explicite.
- Travail et critères compatibles à maintenir : Conserver explicitement dans les contrats et tests les mappings persistants SID, objectGUID et principals vers UUID/périmètres Core, sans rôle Pixs issu d’un rôle AD.
- Clauses remplacées / limites : Aucune clause abandonnée ; détails compatibles conservés comme critères de réalisation.
- Rattachement actif : tâches 1.3, 2.2, 3.2 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 4. Composition coordonnée des services de domaine

- Source historique prévue : [auth-managed-active-directory](historique-deltas-avant-e3/auth-managed-active-directory/spec.md). Ancien chemin : `specs/auth-managed-active-directory/spec.md`.
- Empreinte du bloc ancien normalisé : `cc9a4c532dbd97fec6910d9145408b8178be72354b3b9d6b4c7f0cc9d130f1d6` ; fichier entier à conserver : `eec67ef656bea8134182a61a34f7202826705e1653066f35db36cf41254d7b07`.
- Contrat courant : `auth-managed-active-directory` — Domaine Pixs commun et objectif Windows V1.
- Travail et critères compatibles à maintenir : Conserver responsabilités annuaire/Kerberos/DNS, placement, noms et ports déclarés, refus de collisions avant effets, absence d’adoption, trust ou service supplémentaire implicites.
- Clauses remplacées / limites : Aucune clause abandonnée ; détails compatibles conservés comme critères de réalisation.
- Rattachement actif : tâches 1.2, 2.1, 2.3, 3.1 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 5. Moyens et secrets AD sous contrôle déclaré

- Source historique prévue : [auth-managed-active-directory](historique-deltas-avant-e3/auth-managed-active-directory/spec.md). Ancien chemin : `specs/auth-managed-active-directory/spec.md`.
- Empreinte du bloc ancien normalisé : `ce4d905f2e8d69ed219dfeb001e65d917d2645b363daa78ca7b9c1891259ae2d` ; fichier entier à conserver : `eec67ef656bea8134182a61a34f7202826705e1653066f35db36cf41254d7b07`.
- Contrat courant : `authentication` — Propriété des données Auth et protection des justificatifs.
- Travail et critères compatibles à maintenir : Conserver secrets et récupération protégés, identités minimales, enrôlement qualifié et refus de conversion supposée d’un hash Pixs en justificatif AD.
- Clauses remplacées / limites : Aucune clause abandonnée ; détails compatibles conservés comme critères de réalisation.
- Rattachement actif : tâches 1.3, 2.3, 3.2 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 6. Révocation et restauration du domaine vérifiables

- Source historique prévue : [auth-managed-active-directory](historique-deltas-avant-e3/auth-managed-active-directory/spec.md). Ancien chemin : `specs/auth-managed-active-directory/spec.md`.
- Empreinte du bloc ancien normalisé : `077d1508530cbe5354ba28cf424187122c5a12e085af690ec9d5443618dd8233` ; fichier entier à conserver : `eec67ef656bea8134182a61a34f7202826705e1653066f35db36cf41254d7b07`.
- Contrat courant : `auth-managed-kerberos` — Restauration sans résurrection.
- Travail et critères compatibles à maintenir : Conserver les bornes de révocation explicites, les effets tiers distingués, le contrôle Core avant action sensible malgré un ticket valide, la réconciliation des mappings/générations/confiances avant réadmission.
- Clauses remplacées / limites : Aucune clause abandonnée ; détails compatibles conservés comme critères de réalisation.
- Rattachement actif : tâches 2.3, 3.2 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

## Travail restant explicitement actif

Sur 9 tâches d’origine, 0 restent cochées historiquement et 9 restent non cochées. Leur contenu et leur état sont préservés. La liste suivante est une vue des tâches sources, pas un nouveau registre ou une deuxième série de cases.

| Tâche | Sous-lot conservé | Libellé source | État |
|---|---|---|---|
| 1.1 | O37-SL01 | 1.1 Revoir et adopter les deltas sous autorisation distincte ; confirmer frontières Core/Auth/domaine. | À FAIRE ; preuve future requise |
| 1.2 | O37-SL02 | 1.2 Qualifier implémentation, plateforme, versions, compatibilité, domaine/realm, DNS, ports et interactions avec OpenLDAP/KDC. | À FAIRE ; preuve future requise |
| 1.3 | O37-SL03 | 1.3 Définir mappings, stockage natif, secrets, enrôlement, bornes de révocation, sauvegarde et retrait. | À FAIRE ; preuve future requise |
| 2.1 | O37-SL04 | 2.1 Déclarer pixs.auth.directory.ad et intégrer plans, lifecycle et santé du service propre. | À FAIRE ; preuve future requise |
| 2.2 | O37-SL05 | 2.2 Intégrer les opérations de domaine et mappings par contrats publics sans accès aux tables privées Core. | À FAIRE ; preuve future requise |
| 2.3 | O37-SL06 | 2.3 Intégrer secrets, révocation, reprise et coexistence avec les services sélectionnés. | À FAIRE ; preuve future requise |
| 3.1 | O37-SL07 | 3.1 Tester profil autonome sans AD, activation explicite, collisions et refus d'adoption/trust implicite. | À FAIRE ; preuve future requise |
| 3.2 | O37-SL08 | 3.2 Qualifier clients et mappings, isolation, tickets après retrait et restauration sans résurrection. | À FAIRE ; preuve future requise |
| 3.3 | O37-SL09 | 3.3 Examiner preuves et périmètre ; synchroniser, archiver, engager Git ou publier uniquement sous autorisation distincte. | À FAIRE ; preuve future requise |

## Contrôles et limites

Avant déplacement : existence des contrats cibles, rattachements à des tâches ouvertes et empreintes des 21 fichiers contrôlés. Après déplacement : égalité des octets, mise à jour des liens, même contenu et mêmes cases des tâches, mêmes identifiants de sous-lots et validation OpenSpec à vérifier. Aucun code, test produit, service, migration, archive ou publication n’est exécuté par ce contrôle documentaire.

## Contrôle après déplacement

Les empreintes des fichiers entiers ont été vérifiées après déplacement et sont identiques aux sources. Les 21 déplacements conservent les octets ; les liens fonctionnels entrants ont été actualisés dans les dossiers concernés. Les tâches, cases et identifiants de sous-lots restent inchangés. Aucun besoin compatible n’est déclaré réalisé par ce rangement.

## Revue restante de la tâche 1.1 — reprise ACSM

La tâche 1.1 conserve son libellé et sa case ouverte. Elle porte sur la revue des contrats canoniques courants, de la présente couverture et des paramètres nécessaires à la suite ; elle ne demande pas l'adoption des fichiers historiques ni une nouvelle synchronisation au canon. Son critère courant et les preuves futures exigées sont précisés dans [tasks.md](tasks.md). Aucun autre travail restant ni état historique n'est modifié.
