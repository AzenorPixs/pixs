# Contrôle de couverture avant déplacement — O39

Plan ACL-PIXS-2026-10-31-E3-R1. Complément A explicitement validé : contrôle de couverture avant tout déplacement, conservation de tout travail restant. Relevé du 31 octobre 2026.

## Portée et résultat

5 exigences de l'ancienne préparation sont rattachées au référentiel courant ci-dessous. Chaque ligne indique son devenir, les critères compatibles maintenus et une ou plusieurs tâches encore non cochées. Le classement AU_CANON_IDENTIQUE signifie présence du contrat, jamais réalisation. CIBLE_ACTUALISEE signifie modification décidée du contrat, jamais oubli de son implémentation. RATTACHEMENT_EXPLICITE conserve les détails compatibles comme critères à vérifier sous les contrats courants.

Le classement ne résulte pas de la seule égalité d'un titre : les corps et scénarios ont été relus. Les simples marqueurs de sections de delta ont été exclus de la comparaison. Les clauses remplacées sont indiquées séparément. Aucune exigence résiduelle n'est laissée sans propriétaire de réalisation ; aucun besoin compatible n'est abandonné par son rangement historique.

## Correspondance complète

| Ancienne exigence | Disposition | Référentiel courant | Tâches futures conservées |
|---|---|---|---|
| auth-managed-directory — OpenLDAP propre provisionnable et activable | RATTACHEMENT_EXPLICITE | [auth-managed-directory](../../specs/auth-managed-directory/spec.md) — LZT obligatoire par Domaine et exploitation PA | 2.1, 2.3, 3.1 |
| auth-managed-directory — Autorité PostgreSQL et stockage technique déclaré | RATTACHEMENT_EXPLICITE | [auth-managed-directory](../../specs/auth-managed-directory/spec.md) — PG source Core et LDAP opérationnel | 1.2, 2.2, 3.2 |
| auth-managed-directory — Projection et authentification LDAP distinctes | RATTACHEMENT_EXPLICITE | [auth-managed-directory](../../specs/auth-managed-directory/spec.md) — Authentification LDAP déléguée à Auth | 2.2, 3.2 |
| auth-managed-directory — Lifecycle et reprise sécurisés du service LDAP | RATTACHEMENT_EXPLICITE | [auth-managed-directory](../../specs/auth-managed-directory/spec.md) — Réintégration contrôlée des annuaires | 2.3, 3.1, 3.2, 3.3 |
| directory-projections — Service LDAP propre distinct de la projection | RATTACHEMENT_EXPLICITE | [directory-projections](../../specs/directory-projections/spec.md) — Fonctions de sécurité exclues de la projection | 2.2, 3.2 |

## Détails et critères maintenus par exigence

### 1. OpenLDAP propre provisionnable et activable

- Source historique prévue : [auth-managed-directory](historique-deltas-avant-e3/auth-managed-directory/spec.md). Ancien chemin : `specs/auth-managed-directory/spec.md`.
- Empreinte du bloc ancien normalisé : `c6728dc74a44bf805f332ca62dc987ed042a77fc18ad6d06e5d8ec232603b5fb` ; fichier entier à conserver : `32567e7518ba0e38b8f6a70142c8c20bed372a1884e345e5271c39dd8f310ff5`.
- Contrat courant : `auth-managed-directory` — LZT obligatoire par Domaine et exploitation PA.
- Travail et critères compatibles à maintenir : Conserver l’activation explicite, les plans de service, l’absence de connecteur externe requis et le refus d’adopter/modifier un LDAP existant hors mandat. Le lifecycle LDAP reste administré séparément.
- Clauses remplacées / limites : La facultativité générale est limitée au pré-domaine ; en mode Domaine LZT et KZT sont obligatoires et PA exploite les services sous administration PBO/Core/Auth.
- Rattachement actif : tâches 2.1, 2.3, 3.1 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 2. Autorité PostgreSQL et stockage technique déclaré

- Source historique prévue : [auth-managed-directory](historique-deltas-avant-e3/auth-managed-directory/spec.md). Ancien chemin : `specs/auth-managed-directory/spec.md`.
- Empreinte du bloc ancien normalisé : `a446a6e655050b916b9ea0876845e7ec528c3bfc9f7acb2a454e40936a72571f` ; fichier entier à conserver : `32567e7518ba0e38b8f6a70142c8c20bed372a1884e345e5271c39dd8f310ff5`.
- Contrat courant : `auth-managed-directory` — PG source Core et LDAP opérationnel.
- Travail et critères compatibles à maintenir : Conserver la déclaration du stockage technique et de ses protections, aucune double autorité Core et aucune mutation Core importée d’une écriture LDAP directe.
- Clauses remplacées / limites : La possibilité de rendre LDAP souverain pour Core est remplacée par PG souveraine. L’état Kerberos durable normal LDAP reste distinct ; la reconstruction complète est critique.
- Rattachement actif : tâches 1.2, 2.2, 3.2 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 3. Projection et authentification LDAP distinctes

- Source historique prévue : [auth-managed-directory](historique-deltas-avant-e3/auth-managed-directory/spec.md). Ancien chemin : `specs/auth-managed-directory/spec.md`.
- Empreinte du bloc ancien normalisé : `1054c0ad9c4101c3e74b6c9e02a204e94125d9e7809475ec19a64c15754edd88` ; fichier entier à conserver : `32567e7518ba0e38b8f6a70142c8c20bed372a1884e345e5271c39dd8f310ff5`.
- Contrat courant : `auth-managed-directory` — Authentification LDAP déléguée à Auth.
- Travail et critères compatibles à maintenir : Conserver la sélection séparée des capacités, confiance/moyens/assurance/révocation, absence de bind périmé et aucun repli d’authentification depuis un repli de lecture PG.
- Clauses remplacées / limites : Aucune clause abandonnée ; détails compatibles conservés comme critères de réalisation.
- Rattachement actif : tâches 2.2, 3.2 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 4. Lifecycle et reprise sécurisés du service LDAP

- Source historique prévue : [auth-managed-directory](historique-deltas-avant-e3/auth-managed-directory/spec.md). Ancien chemin : `specs/auth-managed-directory/spec.md`.
- Empreinte du bloc ancien normalisé : `dff7d1d287272ed2b2e8b85400f85ae5ab492ad6371bf75a76d9d9b1d38ea247` ; fichier entier à conserver : `32567e7518ba0e38b8f6a70142c8c20bed372a1884e345e5271c39dd8f310ff5`.
- Contrat courant : `auth-managed-directory` — Réintégration contrôlée des annuaires.
- Travail et critères compatibles à maintenir : Conserver souhaité/appliqué/santé/convergence distincts, transport et credentials protégés, tentatives bornées et réconciliation des retraits avant réadmission, sans secret publié.
- Clauses remplacées / limites : Aucune clause abandonnée ; détails compatibles conservés comme critères de réalisation.
- Rattachement actif : tâches 2.3, 3.1, 3.2, 3.3 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 5. Service LDAP propre distinct de la projection

- Source historique prévue : [directory-projections](historique-deltas-avant-e3/directory-projections/spec.md). Ancien chemin : `specs/directory-projections/spec.md`.
- Empreinte du bloc ancien normalisé : `07ad4a295a982da320bee6592a488da498ac6af0693e08bbee363953493f6bf3` ; fichier entier à conserver : `e10264bcd523500c486887e7bb1e410f09f261beaf28e8ff6c9817860653c873`.
- Contrat courant : `directory-projections` — Fonctions de sécurité exclues de la projection.
- Travail et critères compatibles à maintenir : Conserver le partage possible du même processus entre fonctions explicitement sélectionnées, sans étendre les données/droits de projection ou déduire une confiance d’authentification du repli PG.
- Clauses remplacées / limites : Aucune clause abandonnée ; détails compatibles conservés comme critères de réalisation.
- Rattachement actif : tâches 2.2, 3.2 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

## Travail restant explicitement actif

Sur 9 tâches d’origine, 0 restent cochées historiquement et 9 restent non cochées. Leur contenu et leur état sont préservés. La liste suivante est une vue des tâches sources, pas un nouveau registre ou une deuxième série de cases.

| Tâche | Sous-lot conservé | Libellé source | État |
|---|---|---|---|
| 1.1 | O39-SL01 | 1.1 Revoir et adopter les deltas sous autorisation distincte ; confirmer dépendances, contrats et paramètres ouverts. | À FAIRE ; preuve future requise |
| 1.2 | O39-SL02 | 1.2 Définir modèles propriétaires, migrations, secrets, reprise et plans de retrait sans déplacer les contrats Core existants. | À FAIRE ; preuve future requise |
| 2.1 | O39-SL03 | 2.1 Déclarer le sous-module de gestion, son plan et le service isolé sans imposer sa présence au profil local. | À FAIRE ; preuve future requise |
| 2.2 | O39-SL04 | 2.2 Intégrer projection sortante sous contrat existant et capacité d'authentification séparée si sélectionnée. | À FAIRE ; preuve future requise |
| 2.3 | O39-SL05 | 2.3 Intégrer secrets, santé, arrêt, sauvegarde et réconciliation des dérivés depuis PostgreSQL. | À FAIRE ; preuve future requise |
| 3.1 | O39-SL06 | 3.1 Tester installation sans service activé, activation autorisée, panne et conflit avec un annuaire existant. | À FAIRE ; preuve future requise |
| 3.2 | O39-SL07 | 3.2 Qualifier consultation et binds sélectionnés, isolation, retrait, révocation et restauration sans résurrection. | À FAIRE ; preuve future requise |
| 3.3 | O39-SL08 | 3.3 Vérifier syntaxe, contrôles configurés, audit sans secret, isolation tenant et limites de révocation sur l'artefact réel. | À FAIRE ; preuve future requise |
| 3.4 | O39-SL09 | 3.4 Examiner diff et preuves ; synchroniser, archiver, engager Git ou publier seulement sous autorisation distincte. | À FAIRE ; preuve future requise |

## Contrôles et limites

Avant déplacement : existence des contrats cibles, rattachements à des tâches ouvertes et empreintes des 21 fichiers contrôlés. Après déplacement : égalité des octets, mise à jour des liens, même contenu et mêmes cases des tâches, mêmes identifiants de sous-lots et validation OpenSpec à vérifier. Aucun code, test produit, service, migration, archive ou publication n’est exécuté par ce contrôle documentaire.

## Contrôle après déplacement

Les empreintes des fichiers entiers ont été vérifiées après déplacement et sont identiques aux sources. Les 21 déplacements conservent les octets ; les liens fonctionnels entrants ont été actualisés dans les dossiers concernés. Les tâches, cases et identifiants de sous-lots restent inchangés. Aucun besoin compatible n’est déclaré réalisé par ce rangement.

## Revue restante de la tâche 1.1 — reprise ACSM

La tâche 1.1 conserve son libellé et sa case ouverte. Elle porte sur la revue des contrats canoniques courants, de la présente couverture et des paramètres nécessaires à la suite ; elle ne demande pas l'adoption des fichiers historiques ni une nouvelle synchronisation au canon. Son critère courant et les preuves futures exigées sont précisés dans [tasks.md](tasks.md). Aucun autre travail restant ni état historique n'est modifié.
