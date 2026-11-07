# Contrôle de couverture avant déplacement — C21

Plan ACL-PIXS-2026-10-31-E3-R1. Complément A explicitement validé : contrôle de couverture avant tout déplacement, conservation de tout travail restant. Relevé du 31 octobre 2026.

## Portée et résultat

10 exigences de l'ancienne préparation sont rattachées au référentiel courant ci-dessous. Chaque ligne indique son devenir, les critères compatibles maintenus et une ou plusieurs tâches encore non cochées. Le classement AU_CANON_IDENTIQUE signifie présence du contrat, jamais réalisation. CIBLE_ACTUALISEE signifie modification décidée du contrat, jamais oubli de son implémentation. RATTACHEMENT_EXPLICITE conserve les détails compatibles comme critères à vérifier sous les contrats courants.

Le classement ne résulte pas de la seule égalité d'un titre : les corps et scénarios ont été relus. Les simples marqueurs de sections de delta ont été exclus de la comparaison. Les clauses remplacées sont indiquées séparément. Aucune exigence résiduelle n'est laissée sans propriétaire de réalisation ; aucun besoin compatible n'est abandonné par son rangement historique.

## Correspondance complète

| Ancienne exigence | Disposition | Référentiel courant | Tâches futures conservées |
|---|---|---|---|
| authentication — Module essentiel autonome pixs.auth | AU_CANON_IDENTIQUE | [authentication](../../specs/authentication/spec.md) — Module essentiel autonome pixs.auth | 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 |
| authentication — Autonomie locale et PostgreSQL par défaut | CIBLE_ACTUALISEE | [authentication](../../specs/authentication/spec.md) — Autonomie locale et PostgreSQL par défaut | 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 |
| authentication — Propriété des données Auth et protection des justificatifs | AU_CANON_IDENTIQUE | [authentication](../../specs/authentication/spec.md) — Propriété des données Auth et protection des justificatifs | 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 |
| authentication — Sous-modules Auth composés par les mécanismes communs | AU_CANON_IDENTIQUE | [authentication](../../specs/authentication/spec.md) — Sous-modules Auth composés par les mécanismes communs | 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 |
| authentication — Politiques Auth déclaratives et contextualisées | CIBLE_ACTUALISEE | [authentication](../../specs/authentication/spec.md) — Politiques Auth déclaratives et contextualisées | 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 |
| authentication — Absence de repli implicite entre méthodes et sources | AU_CANON_IDENTIQUE | [authentication](../../specs/authentication/spec.md) — Absence de repli implicite entre méthodes et sources | 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 |
| core — Frontière Core Auth et dépendance unidirectionnelle | AU_CANON_IDENTIQUE | [core](../../specs/core/spec.md) — Frontière Core Auth et dépendance unidirectionnelle | 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 |
| core — Moyens multiples sans multiplication implicite des identités | CIBLE_ACTUALISEE | [core](../../specs/core/spec.md) — Moyens multiples sans multiplication implicite des identités | 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 |
| reference-composition — Capacités obligatoires du P0 | AU_CANON_IDENTIQUE | [reference-composition](../../specs/reference-composition/spec.md) — Capacités obligatoires du P0 | 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 |
| reference-composition — Profil Auth standard sans connecteur externe installé | CIBLE_ACTUALISEE | [reference-composition](../../specs/reference-composition/spec.md) — Profil Auth standard sans connecteur externe installé | 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 |

## Détails et critères maintenus par exigence

### 1. Module essentiel autonome pixs.auth

- Source historique prévue : [authentication](historique-deltas-avant-e3/authentication/spec.md). Ancien chemin : `specs/authentication/spec.md`.
- Empreinte du bloc ancien normalisé : `d59c8431591860cf112f7d6caabaf924869c465340fd34eb90b90a8165cd120f` ; fichier entier à conserver : `e00cc629317fa3cc74d531137ccaee3ddbbeb0f04b788684cafad56ddad3afa1`.
- Contrat courant : `authentication` — Module essentiel autonome pixs.auth.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 2. Autonomie locale et PostgreSQL par défaut

- Source historique prévue : [authentication](historique-deltas-avant-e3/authentication/spec.md). Ancien chemin : `specs/authentication/spec.md`.
- Empreinte du bloc ancien normalisé : `7454d3d110825a7aebb2e82cd21901e367c20bc437a6476721f1b2dad867a5ec` ; fichier entier à conserver : `e00cc629317fa3cc74d531137ccaee3ddbbeb0f04b788684cafad56ddad3afa1`.
- Contrat courant : `authentication` — Autonomie locale et PostgreSQL par défaut.
- Travail et critères compatibles à maintenir : Précision validée des stockages PG avant/après Domaine, sans identité d’Instance conservée après bascule ; autonomie PG Domaine seulement sous profil explicite.
- Clauses remplacées / limites : Précision validée des stockages PG avant/après Domaine, sans identité d’Instance conservée après bascule ; autonomie PG Domaine seulement sous profil explicite.
- Rattachement actif : tâches 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 3. Propriété des données Auth et protection des justificatifs

- Source historique prévue : [authentication](historique-deltas-avant-e3/authentication/spec.md). Ancien chemin : `specs/authentication/spec.md`.
- Empreinte du bloc ancien normalisé : `81144ae4ced977a356b5f4c10bd055cfd7dde6c1a7ede8228393d134b87f8dc3` ; fichier entier à conserver : `e00cc629317fa3cc74d531137ccaee3ddbbeb0f04b788684cafad56ddad3afa1`.
- Contrat courant : `authentication` — Propriété des données Auth et protection des justificatifs.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 4. Sous-modules Auth composés par les mécanismes communs

- Source historique prévue : [authentication](historique-deltas-avant-e3/authentication/spec.md). Ancien chemin : `specs/authentication/spec.md`.
- Empreinte du bloc ancien normalisé : `6bb3f90df1d59d99f0fa70f17ca1a2bb6e5cc507736cb015ac7197382281c66b` ; fichier entier à conserver : `e00cc629317fa3cc74d531137ccaee3ddbbeb0f04b788684cafad56ddad3afa1`.
- Contrat courant : `authentication` — Sous-modules Auth composés par les mécanismes communs.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 5. Politiques Auth déclaratives et contextualisées

- Source historique prévue : [authentication](historique-deltas-avant-e3/authentication/spec.md). Ancien chemin : `specs/authentication/spec.md`.
- Empreinte du bloc ancien normalisé : `1e9089117cf4f4edeb5fb5bb62dd5b0664626a1c907ba506c34bbd49037d00a1` ; fichier entier à conserver : `e00cc629317fa3cc74d531137ccaee3ddbbeb0f04b788684cafad56ddad3afa1`.
- Contrat courant : `authentication` — Politiques Auth déclaratives et contextualisées.
- Travail et critères compatibles à maintenir : Les contextes Instance/Domaine/profil complètent les périmètres ; déterminisme, origine et refus d’assurance insuffisante sont conservés.
- Clauses remplacées / limites : Les contextes Instance/Domaine/profil complètent les périmètres ; déterminisme, origine et refus d’assurance insuffisante sont conservés.
- Rattachement actif : tâches 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 6. Absence de repli implicite entre méthodes et sources

- Source historique prévue : [authentication](historique-deltas-avant-e3/authentication/spec.md). Ancien chemin : `specs/authentication/spec.md`.
- Empreinte du bloc ancien normalisé : `ec275823d239b839a804c40658aac7940add1cce4e29f40582826d4b479b10a9` ; fichier entier à conserver : `e00cc629317fa3cc74d531137ccaee3ddbbeb0f04b788684cafad56ddad3afa1`.
- Contrat courant : `authentication` — Absence de repli implicite entre méthodes et sources.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 7. Frontière Core Auth et dépendance unidirectionnelle

- Source historique prévue : [core](historique-deltas-avant-e3/core/spec.md). Ancien chemin : `specs/core/spec.md`.
- Empreinte du bloc ancien normalisé : `245ff6a4a0fdfd371048730481d578d1133adbc9b3f3cfd551ff5f32f7db8f5c` ; fichier entier à conserver : `7d875c3ed3eb013d9f302168508182974ddd1b604df676f362c572197edd4082`.
- Contrat courant : `core` — Frontière Core Auth et dépendance unidirectionnelle.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 8. Moyens multiples sans multiplication implicite des identités

- Source historique prévue : [core](historique-deltas-avant-e3/core/spec.md). Ancien chemin : `specs/core/spec.md`.
- Empreinte du bloc ancien normalisé : `02fb77399da238089517c01aa6bc10cfed068e930b8c3ad1358593312dda9461` ; fichier entier à conserver : `7d875c3ed3eb013d9f302168508182974ddd1b604df676f362c572197edd4082`.
- Contrat courant : `core` — Moyens multiples sans multiplication implicite des identités.
- Travail et critères compatibles à maintenir : La cardinalité unique par individu est remplacée par plusieurs identités par Domaine ; chaque identité garde ses moyens et son UUID distincts.
- Clauses remplacées / limites : La cardinalité unique par individu est remplacée par plusieurs identités par Domaine ; chaque identité garde ses moyens et son UUID distincts.
- Rattachement actif : tâches 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 9. Capacités obligatoires du P0

- Source historique prévue : [reference-composition](historique-deltas-avant-e3/reference-composition/spec.md). Ancien chemin : `specs/reference-composition/spec.md`.
- Empreinte du bloc ancien normalisé : `876e7256ff57b71c7a1de9838b90403e749a4b80ddd2517c6c80d3970ddb26ed` ; fichier entier à conserver : `c1d0daeb6ac3aa0bc5ac178aca6c902bcf4e4ada9b1b8164ad4bc2ae4f39bff6`.
- Contrat courant : `reference-composition` — Capacités obligatoires du P0.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 10. Profil Auth standard sans connecteur externe installé

- Source historique prévue : [reference-composition](historique-deltas-avant-e3/reference-composition/spec.md). Ancien chemin : `specs/reference-composition/spec.md`.
- Empreinte du bloc ancien normalisé : `fd3762eca92617c32f58328a0349967de92492db1a7f75a8cc2d0a04afe1cc99` ; fichier entier à conserver : `c1d0daeb6ac3aa0bc5ac178aca6c902bcf4e4ada9b1b8164ad4bc2ae4f39bff6`.
- Contrat courant : `reference-composition` — Profil Auth standard sans connecteur externe installé.
- Travail et critères compatibles à maintenir : LDAP/KZT obligatoires en Domaine ; services non imposés au pré-domaine et connecteurs externes toujours distincts.
- Clauses remplacées / limites : LDAP/KZT obligatoires en Domaine ; services non imposés au pré-domaine et connecteurs externes toujours distincts.
- Rattachement actif : tâches 1.1, 1.2, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

## Travail restant explicitement actif

Sur 10 tâches d’origine, 0 restent cochées historiquement et 10 restent non cochées. Leur contenu et leur état sont préservés. La liste suivante est une vue des tâches sources, pas un nouveau registre ou une deuxième série de cases.

| Tâche | Sous-lot conservé | Libellé source | État |
|---|---|---|---|
| 1.1 | C21-SL01 | 1.1 Revoir les deltas et le catalogue ; confirmer contrats, identifiants, frontières Core/Auth et paramètres avant réalisation. | À FAIRE ; preuve future requise |
| 1.2 | C21-SL02 | 1.2 Vérifier les deltas déjà adoptés et aligner la recette P0/C03/C08 sans les appliquer une seconde fois ni modifier les archives historiques ; toute nouvelle modification normative exige son autorisation distincte. | À FAIRE ; preuve future requise |
| 2.1 | C21-SL03 | 2.1 Déclarer le module essentiel, ses capacités et sa dépendance publique vers Core, sans cycle. | À FAIRE ; preuve future requise |
| 2.2 | C21-SL04 | 2.2 Intégrer le stockage PostgreSQL Auth et les migrations propres avec les services C02, secrets et audit. | À FAIRE ; preuve future requise |
| 2.3 | C21-SL05 | 2.3 Raccorder C03 et les sous-modules locaux ; conserver les sources externes absentes et les services gérés inactifs par défaut. | À FAIRE ; preuve future requise |
| 2.4 | C21-SL06 | 2.4 Exposer les politiques et leur origine via contrats publics et administration autorisée. | À FAIRE ; preuve future requise |
| 3.1 | C21-SL07 | 3.1 Prouver autonomie locale PostgreSQL, refus sans module essentiel et absence de repli permissif. | À FAIRE ; preuve future requise |
| 3.2 | C21-SL08 | 3.2 Prouver isolation, révocation, reprise, frontières de données et exception Super Admin sans MFA inventé. | À FAIRE ; preuve future requise |
| 3.3 | C21-SL09 | 3.3 Exécuter contrôles configurés et recette du paquet réellement distribué ; déclarer les capacités non qualifiées. | À FAIRE ; preuve future requise |
| 3.4 | C21-SL10 | 3.4 N'engager synchronisation, archivage, Git ou publication que sous autorisation distincte. | À FAIRE ; preuve future requise |

## Contrôles et limites

Avant déplacement : existence des contrats cibles, rattachements à des tâches ouvertes et empreintes des 21 fichiers contrôlés. Après déplacement : égalité des octets, mise à jour des liens, même contenu et mêmes cases des tâches, mêmes identifiants de sous-lots et validation OpenSpec à vérifier. Aucun code, test produit, service, migration, archive ou publication n’est exécuté par ce contrôle documentaire.

## Contrôle après déplacement

Les empreintes des fichiers entiers ont été vérifiées après déplacement et sont identiques aux sources. Les 21 déplacements conservent les octets ; les liens fonctionnels entrants ont été actualisés dans les dossiers concernés. Les tâches, cases et identifiants de sous-lots restent inchangés. Aucun besoin compatible n’est déclaré réalisé par ce rangement.
