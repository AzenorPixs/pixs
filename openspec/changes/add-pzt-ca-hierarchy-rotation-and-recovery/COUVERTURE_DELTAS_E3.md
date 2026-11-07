# Contrôle de couverture avant déplacement — Z12

Plan ACL-PIXS-2026-10-31-E3-R1. Complément A explicitement validé : contrôle de couverture avant tout déplacement, conservation de tout travail restant. Relevé du 31 octobre 2026.

## Portée et résultat

11 exigences de l'ancienne préparation sont rattachées au référentiel courant ci-dessous. Chaque ligne indique son devenir, les critères compatibles maintenus et une ou plusieurs tâches encore non cochées. Le classement AU_CANON_IDENTIQUE signifie présence du contrat, jamais réalisation. CIBLE_ACTUALISEE signifie modification décidée du contrat, jamais oubli de son implémentation. RATTACHEMENT_EXPLICITE conserve les détails compatibles comme critères à vérifier sous les contrats courants.

Le classement ne résulte pas de la seule égalité d'un titre : les corps et scénarios ont été relus. Les simples marqueurs de sections de delta ont été exclus de la comparaison. Les clauses remplacées sont indiquées séparément. Aucune exigence résiduelle n'est laissée sans propriétaire de réalisation ; aucun besoin compatible n'est abandonné par son rangement historique.

## Correspondance complète

| Ancienne exigence | Disposition | Référentiel courant | Tâches futures conservées |
|---|---|---|---|
| authorization — Autorité technique PKI Z12 bornée à la première installation | AU_CANON_IDENTIQUE | [authorization](../../specs/authorization/spec.md) — Autorité technique PKI Z12 bornée à la première installation | 3, 4, 5, 6, 7, 8, 9, 10 |
| authorization — Garde technique du temps indépendante de la base | AU_CANON_IDENTIQUE | [authorization](../../specs/authorization/spec.md) — Garde technique du temps indépendante de la base | 3, 4, 5, 6, 7, 8, 9, 10 |
| installation-provisioning — Amorçage technique borné du temps avant transport protégé | AU_CANON_IDENTIQUE | [installation-provisioning](../../specs/installation-provisioning/spec.md) — Amorçage technique borné du temps avant transport protégé | 3, 4, 5, 6, 7, 8, 9, 10 |
| pixs-agent — Gestion du service de temps par PA et pixs.agent | AU_CANON_IDENTIQUE | [pixs-agent](../../specs/pixs-agent/spec.md) — Gestion du service de temps par PA et pixs.agent | 3, 4, 5, 6, 7, 8, 9, 10 |
| pzt — Amorçage PKI PZT autonome de première installation avant PostgreSQL | CIBLE_ACTUALISEE | [pzt](../../specs/pzt/spec.md) — Amorçage PKI PZT autonome de première installation avant PostgreSQL | 3, 4, 5, 6, 7, 8, 9, 10 |
| pzt — Profil X.509 des terminaux de première installation Z12 | AU_CANON_IDENTIQUE | [pzt](../../specs/pzt/spec.md) — Profil X.509 des terminaux de première installation Z12 | 3, 4, 5, 6, 7, 8, 9, 10 |
| pzt — Résolution locale du matériel TLS sous propriétaire courant Z12 | CIBLE_ACTUALISEE | [pzt](../../specs/pzt/spec.md) — Résolution locale du matériel TLS sous propriétaire courant Z12 | 3, 4, 5, 6, 7, 8, 9, 10 |
| pzt — Procédure exceptionnelle D18 avec UTC perdu | AU_CANON_IDENTIQUE | [pzt](../../specs/pzt/spec.md) — Procédure exceptionnelle D18 avec UTC perdu | 3, 4, 5, 6, 7, 8, 9, 10 |
| pzt — Contrat A10i50 — Adaptateurs système de temps et de qualité par plateforme — option A validée le 8 octobre 2026 | AU_CANON_IDENTIQUE | [pzt](../../specs/pzt/spec.md) — Contrat A10i50 — Adaptateurs système de temps et de qualité par plateforme — option A validée le 8 octobre 2026 | 3, 4, 5, 6, 7, 8, 9, 10 |
| pzt — Contrat A10i52 — Budgets bornés d’acquisition et fraîcheur de preuve de temps — option A validée le 8 octobre 2026 | AU_CANON_IDENTIQUE | [pzt](../../specs/pzt/spec.md) — Contrat A10i52 — Budgets bornés d’acquisition et fraîcheur de preuve de temps — option A validée le 8 octobre 2026 | 3, 4, 5, 6, 7, 8, 9, 10 |
| runtime — Contrat commun runtime et Kernel agnostique du FOURNISSEUR | AU_CANON_IDENTIQUE | [runtime](../../specs/runtime/spec.md) — Contrat commun runtime et Kernel agnostique du FOURNISSEUR | 3, 4, 5, 6, 7, 8, 9, 10 |

## Détails et critères maintenus par exigence

### 1. Autorité technique PKI Z12 bornée à la première installation

- Source historique prévue : [authorization](historique-deltas-avant-e3/authorization/spec.md). Ancien chemin : `specs/authorization/spec.md`.
- Empreinte du bloc ancien normalisé : `9fbe5eb1cd876845ac35cb3eebe635b05be4fc5815e324af0b295c940b8802bc` ; fichier entier à conserver : `f0a1243e5ddc1443cee4b5ba52684c5278b43a01dbb10729d696851e9dd79021`.
- Contrat courant : `authorization` — Autorité technique PKI Z12 bornée à la première installation.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 3, 4, 5, 6, 7, 8, 9, 10 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 2. Garde technique du temps indépendante de la base

- Source historique prévue : [authorization](historique-deltas-avant-e3/authorization/spec.md). Ancien chemin : `specs/authorization/spec.md`.
- Empreinte du bloc ancien normalisé : `472b24607b7f17ea95364b446b9d97996a6bbbbcf28c64c3fd9e58d5d96c835e` ; fichier entier à conserver : `f0a1243e5ddc1443cee4b5ba52684c5278b43a01dbb10729d696851e9dd79021`.
- Contrat courant : `authorization` — Garde technique du temps indépendante de la base.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 3, 4, 5, 6, 7, 8, 9, 10 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 3. Amorçage technique borné du temps avant transport protégé

- Source historique prévue : [installation-provisioning](historique-deltas-avant-e3/installation-provisioning/spec.md). Ancien chemin : `specs/installation-provisioning/spec.md`.
- Empreinte du bloc ancien normalisé : `de99b01fd663ea299aa8f716f511cd3ac8f48b89c6adc3b2b9da5e6839707f88` ; fichier entier à conserver : `5b6943640a5a8e826ac2674e81cd2cdff4a1d433861b07860d60301251e7ce36`.
- Contrat courant : `installation-provisioning` — Amorçage technique borné du temps avant transport protégé.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 3, 4, 5, 6, 7, 8, 9, 10 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 4. Gestion du service de temps par PA et pixs.agent

- Source historique prévue : [pixs-agent](historique-deltas-avant-e3/pixs-agent/spec.md). Ancien chemin : `specs/pixs-agent/spec.md`.
- Empreinte du bloc ancien normalisé : `6335a8f585422d8cacbee23a3a252c8d5681a17232d44a67c976d8a8c42643b4` ; fichier entier à conserver : `a7b5044e7f4e72be7f955624915b0b3703c6ede670aa0bd38e48821113be35b7`.
- Contrat courant : `pixs-agent` — Gestion du service de temps par PA et pixs.agent.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 3, 4, 5, 6, 7, 8, 9, 10 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 5. Amorçage PKI PZT autonome de première installation avant PostgreSQL

- Source historique prévue : [pzt](historique-deltas-avant-e3/pzt/spec.md). Ancien chemin : `specs/pzt/spec.md`.
- Empreinte du bloc ancien normalisé : `d3acd0198eb81b93950c1ef183921a641bff90575277973dc6613a6c94a4190a` ; fichier entier à conserver : `1185602c82432ad2537f11e84157fed9b883c53153aadc188bed59ac330b287c`.
- Contrat courant : `pzt` — Amorçage PKI PZT autonome de première installation avant PostgreSQL.
- Travail et critères compatibles à maintenir : Choix A validé : confiance initiale distincte et bornée, puis PKI normale vérifiée avant retrait irréversible ; aucune promotion implicite des clés initiales.
- Clauses remplacées / limites : Choix A validé : confiance initiale distincte et bornée, puis PKI normale vérifiée avant retrait irréversible ; aucune promotion implicite des clés initiales.
- Rattachement actif : tâches 3, 4, 5, 6, 7, 8, 9, 10 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 6. Profil X.509 des terminaux de première installation Z12

- Source historique prévue : [pzt](historique-deltas-avant-e3/pzt/spec.md). Ancien chemin : `specs/pzt/spec.md`.
- Empreinte du bloc ancien normalisé : `293be18a94383cfc7c0daff7811e7d1c66f3bef429cc72903b2a9b68251fe885` ; fichier entier à conserver : `1185602c82432ad2537f11e84157fed9b883c53153aadc188bed59ac330b287c`.
- Contrat courant : `pzt` — Profil X.509 des terminaux de première installation Z12.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 3, 4, 5, 6, 7, 8, 9, 10 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 7. Résolution locale du matériel TLS sous propriétaire courant Z12

- Source historique prévue : [pzt](historique-deltas-avant-e3/pzt/spec.md). Ancien chemin : `specs/pzt/spec.md`.
- Empreinte du bloc ancien normalisé : `7733edccc1bc98d6e7c7cc45feed58c7c61e17f89fa816d94f9c2ce00324c496` ; fichier entier à conserver : `1185602c82432ad2537f11e84157fed9b883c53153aadc188bed59ac330b287c`.
- Contrat courant : `pzt` — Résolution locale du matériel TLS sous propriétaire courant Z12.
- Travail et critères compatibles à maintenir : Le matériel normal relève du propriétaire courant après bascule vers la PKI distincte ; état, âges et retraits ne sont pas réarmés.
- Clauses remplacées / limites : Le matériel normal relève du propriétaire courant après bascule vers la PKI distincte ; état, âges et retraits ne sont pas réarmés.
- Rattachement actif : tâches 3, 4, 5, 6, 7, 8, 9, 10 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 8. Procédure exceptionnelle D18 avec UTC perdu

- Source historique prévue : [pzt](historique-deltas-avant-e3/pzt/spec.md). Ancien chemin : `specs/pzt/spec.md`.
- Empreinte du bloc ancien normalisé : `8f8ab896fd77e60975370562ed946a7891ffbe25a38aa9ff328afae7f14f3675` ; fichier entier à conserver : `1185602c82432ad2537f11e84157fed9b883c53153aadc188bed59ac330b287c`.
- Contrat courant : `pzt` — Procédure exceptionnelle D18 avec UTC perdu.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 3, 4, 5, 6, 7, 8, 9, 10 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 9. Contrat A10i50 — Adaptateurs système de temps et de qualité par plateforme — option A validée le 8 octobre 2026

- Source historique prévue : [pzt](historique-deltas-avant-e3/pzt/spec.md). Ancien chemin : `specs/pzt/spec.md`.
- Empreinte du bloc ancien normalisé : `f2137f7482c9fb0db9838abf659aef87cf0ed80921daff43423f57041ac8783d` ; fichier entier à conserver : `1185602c82432ad2537f11e84157fed9b883c53153aadc188bed59ac330b287c`.
- Contrat courant : `pzt` — Contrat A10i50 — Adaptateurs système de temps et de qualité par plateforme — option A validée le 8 octobre 2026.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 3, 4, 5, 6, 7, 8, 9, 10 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 10. Contrat A10i52 — Budgets bornés d’acquisition et fraîcheur de preuve de temps — option A validée le 8 octobre 2026

- Source historique prévue : [pzt](historique-deltas-avant-e3/pzt/spec.md). Ancien chemin : `specs/pzt/spec.md`.
- Empreinte du bloc ancien normalisé : `a68a337e3541a937352763ed4bcb0598e8410aa2393ea3b8108be6408c0217e9` ; fichier entier à conserver : `1185602c82432ad2537f11e84157fed9b883c53153aadc188bed59ac330b287c`.
- Contrat courant : `pzt` — Contrat A10i52 — Budgets bornés d’acquisition et fraîcheur de preuve de temps — option A validée le 8 octobre 2026.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 3, 4, 5, 6, 7, 8, 9, 10 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 11. Contrat commun runtime et Kernel agnostique du FOURNISSEUR

- Source historique prévue : [runtime](historique-deltas-avant-e3/runtime/spec.md). Ancien chemin : `specs/runtime/spec.md`.
- Empreinte du bloc ancien normalisé : `f70a91d28a96fd4eaac7142c280525503ba5ab2245cc3bbbb2e5c4989b8e6708` ; fichier entier à conserver : `bd9669193c7dd020aac067baef2055c5abce4309586c7fdcc75e87d53b8c64af`.
- Contrat courant : `runtime` — Contrat commun runtime et Kernel agnostique du FOURNISSEUR.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 3, 4, 5, 6, 7, 8, 9, 10 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

## Travail restant explicitement actif

Sur 10 tâches d’origine, 2 restent cochées historiquement et 8 restent non cochées. Leur contenu et leur état sont préservés. La liste suivante est une vue des tâches sources, pas un nouveau registre ou une deuxième série de cases.

| Tâche | Sous-lot conservé | Libellé source | État |
|---|---|---|---|
| 3 | Z12-SL03 | 3. Lever les barrières de conception de design.md et faire valider les choix encore ouverts avant réalisation ; présenter tout delta normatif ou dépendance supplémentaire nécessaire. | À FAIRE ; preuve future requise |
| 4 | Z12-SL04 | 4. Définir les contrats, schémas, propriétaires et adapters du périmètre : A10i6–A10i20 : PKI dédiée, intermédiaires, protection des clés, secours, exclusion/bascule, algorithmes et successions racine. | À FAIRE ; preuve future requise |
| 5 | Z12-SL05 | 5. Réaliser le complément ciblé et son branchement aux dépendances, en conservant les structures déjà livrées. | À FAIRE ; preuve future requise |
| 6 | Z12-SL06 | 6. Traiter les échecs, concurrence, limites et interruptions propres au lot ; états incertains explicités et reprise sous autorité/contexte courants. | À FAIRE ; preuve future requise |
| 7 | Z12-SL07 | 7. Exécuter syntaxe, contrôles configurés et unités/négatifs applicables, en rapportant les résultats natifs sans données sensibles. | À FAIRE ; preuve future requise |
| 8 | Z12-SL08 | 8. Exécuter les intégrations/conformités du profil : Bornes exactes et juste au-delà, types/champs étrangers, rôle/contexte/mandat inadmissibles, échéance/révocation, concurrence, réponse perdue, crash/reprise, état ancien et ressources réellement libérées. Mesurer seulement le traitement concerné et ne pas extrapoler ses plafonds au PA/PBO entier. | À FAIRE ; preuve future requise |
| 9 | Z12-SL09 | 9. Vérifier la sortie attendue : Signataire exclu avant succession ; perte traitée par nouvelles clés/recertification ; coexistence et durées bornées ; pas de confiance par snapshot. | À FAIRE ; preuve future requise |
| 10 | Z12-SL10 | 10. Relier chaque scénario applicable aux preuves/version/artefact, examiner le diff et les limites ; Git, synchronisation, archive, installation et publication restent soumis à leur autorisation propre. | À FAIRE ; preuve future requise |

## Contrôles et limites

Avant déplacement : existence des contrats cibles, rattachements à des tâches ouvertes et empreintes des 21 fichiers contrôlés. Après déplacement : égalité des octets, mise à jour des liens, même contenu et mêmes cases des tâches, mêmes identifiants de sous-lots et validation OpenSpec à vérifier. Aucun code, test produit, service, migration, archive ou publication n’est exécuté par ce contrôle documentaire.

## Contrôle après déplacement

Les empreintes des fichiers entiers ont été vérifiées après déplacement et sont identiques aux sources. Les 21 déplacements conservent les octets ; les liens fonctionnels entrants ont été actualisés dans les dossiers concernés. Les tâches, cases et identifiants de sous-lots restent inchangés. Aucun besoin compatible n’est déclaré réalisé par ce rangement.
