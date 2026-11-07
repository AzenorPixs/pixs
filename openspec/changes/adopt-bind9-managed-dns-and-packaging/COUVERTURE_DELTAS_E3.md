# Contrôle de couverture avant déplacement — Z27

Plan ACL-PIXS-2026-10-31-E3-R1. Complément A explicitement validé : contrôle de couverture avant tout déplacement, conservation de tout travail restant. Relevé du 31 octobre 2026.

## Portée et résultat

3 exigences de l'ancienne préparation sont rattachées au référentiel courant ci-dessous. Chaque ligne indique son devenir, les critères compatibles maintenus et une ou plusieurs tâches encore non cochées. Le classement AU_CANON_IDENTIQUE signifie présence du contrat, jamais réalisation. CIBLE_ACTUALISEE signifie modification décidée du contrat, jamais oubli de son implémentation. RATTACHEMENT_EXPLICITE conserve les détails compatibles comme critères à vérifier sous les contrats courants.

Le classement ne résulte pas de la seule égalité d'un titre : les corps et scénarios ont été relus. Les simples marqueurs de sections de delta ont été exclus de la comparaison. Les clauses remplacées sont indiquées séparément. Aucune exigence résiduelle n'est laissée sans propriétaire de réalisation ; aucun besoin compatible n'est abandonné par son rangement historique.

## Correspondance complète

| Ancienne exigence | Disposition | Référentiel courant | Tâches futures conservées |
|---|---|---|---|
| deb-package — Installation BIND 9 par le PA du rôle serveur DNS Debian | AU_CANON_IDENTIQUE | [deb-package](../../specs/deb-package/spec.md) — Installation BIND 9 par le PA du rôle serveur DNS Debian | 3.2 |
| docker-image — Logiciel BIND 9 fourni dans Docker Pixs sans activation implicite | AU_CANON_IDENTIQUE | [docker-image](../../specs/docker-image/spec.md) — Logiciel BIND 9 fourni dans Docker Pixs sans activation implicite | 3.2 |
| pzt — Fournisseur BIND 9 du DNS géré sur Debian et Docker Pixs | CIBLE_ACTUALISEE | [pzt](../../specs/pzt/spec.md) — Fournisseur BIND 9 du DNS géré sur Debian et Docker Pixs | 3.2 |

## Détails et critères maintenus par exigence

### 1. Installation BIND 9 par le PA du rôle serveur DNS Debian

- Source historique prévue : [deb-package](historique-deltas-avant-e3/deb-package/spec.md). Ancien chemin : `specs/deb-package/spec.md`.
- Empreinte du bloc ancien normalisé : `d506f436c51e1784726915c42a35582361e74d00fffb0004442f8458f89dc489` ; fichier entier à conserver : `b69cef765884a009d17d6da7f7095f988df270735a6c5c00becb99f2b68beb57`.
- Contrat courant : `deb-package` — Installation BIND 9 par le PA du rôle serveur DNS Debian.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 3.2 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 2. Logiciel BIND 9 fourni dans Docker Pixs sans activation implicite

- Source historique prévue : [docker-image](historique-deltas-avant-e3/docker-image/spec.md). Ancien chemin : `specs/docker-image/spec.md`.
- Empreinte du bloc ancien normalisé : `e80ccafc2dfecdf3528aff300a20574b367a2d96e05805640d3b553cbaa57165` ; fichier entier à conserver : `049f4f492ee07ccd9668f2a1252a7d024a2b7f53df4d95a3004af3a7c62c0cac`.
- Contrat courant : `docker-image` — Logiciel BIND 9 fourni dans Docker Pixs sans activation implicite.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 3.2 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 3. Fournisseur BIND 9 du DNS géré sur Debian et Docker Pixs

- Source historique prévue : [pzt](historique-deltas-avant-e3/pzt/spec.md). Ancien chemin : `specs/pzt/spec.md`.
- Empreinte du bloc ancien normalisé : `c2e1f5dabb30344d1f20f5d11f02cf3b45409362b40f87ef36966939241fb731` ; fichier entier à conserver : `bbf9485949b19bd5eaac1f8c0fd712150dd719a904b5c96adda360d36ef00d8f`.
- Contrat courant : `pzt` — Fournisseur BIND 9 du DNS géré sur Debian et Docker Pixs.
- Travail et critères compatibles à maintenir : PA conserve préparation, maintenance système et mises à jour ; DZT configure et maintient le fonctionnement logiciel, sans activation implicite.
- Clauses remplacées / limites : PA conserve préparation, maintenance système et mises à jour ; DZT configure et maintient le fonctionnement logiciel, sans activation implicite.
- Rattachement actif : tâches 3.2 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

## Travail restant explicitement actif

Sur 7 tâches d’origine, 6 restent cochées historiquement et 1 restent non cochées. Leur contenu et leur état sont préservés. La liste suivante est une vue des tâches sources, pas un nouveau registre ou une deuxième série de cases.

| Tâche | Sous-lot conservé | Libellé source | État |
|---|---|---|---|
| 3.2 | Z27-SL07 | 3.2 Examiner le périmètre et les limites puis n'engager l'archive documentaire que si elle est explicitement autorisée ; produire STATISTIQUES.md après une archive réussie. | À FAIRE ; preuve future requise |

La tâche 3.2 reste la clôture documentaire future du choix logiciel ; elle ne porte pas seule l’exécution DNS. Les réalisations restent ouvertes dans Z05, PA09, C18 et X01. Les six coches antérieures ne qualifient pas la nouvelle frontière PA/DZT.

## Contrôles et limites

Avant déplacement : existence des contrats cibles, rattachements à des tâches ouvertes et empreintes des 21 fichiers contrôlés. Après déplacement : égalité des octets, mise à jour des liens, même contenu et mêmes cases des tâches, mêmes identifiants de sous-lots et validation OpenSpec à vérifier. Aucun code, test produit, service, migration, archive ou publication n’est exécuté par ce contrôle documentaire.

## Contrôle après déplacement

Les empreintes des fichiers entiers ont été vérifiées après déplacement et sont identiques aux sources. Les 21 déplacements conservent les octets ; les liens fonctionnels entrants ont été actualisés dans les dossiers concernés. Les tâches, cases et identifiants de sous-lots restent inchangés. Aucun besoin compatible n’est déclaré réalisé par ce rangement.
