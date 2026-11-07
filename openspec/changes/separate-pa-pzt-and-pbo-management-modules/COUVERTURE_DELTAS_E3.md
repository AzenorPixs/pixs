# Contrôle de couverture avant déplacement — PA10

Plan ACL-PIXS-2026-10-31-E3-R1. Complément A explicitement validé : contrôle de couverture avant tout déplacement, conservation de tout travail restant. Relevé du 31 octobre 2026.

## Portée et résultat

26 exigences de l'ancienne préparation sont rattachées au référentiel courant ci-dessous. Chaque ligne indique son devenir, les critères compatibles maintenus et une ou plusieurs tâches encore non cochées. Le classement AU_CANON_IDENTIQUE signifie présence du contrat, jamais réalisation. CIBLE_ACTUALISEE signifie modification décidée du contrat, jamais oubli de son implémentation. RATTACHEMENT_EXPLICITE conserve les détails compatibles comme critères à vérifier sous les contrats courants.

Le classement ne résulte pas de la seule égalité d'un titre : les corps et scénarios ont été relus. Les simples marqueurs de sections de delta ont été exclus de la comparaison. Les clauses remplacées sont indiquées séparément. Aucune exigence résiduelle n'est laissée sans propriétaire de réalisation ; aucun besoin compatible n'est abandonné par son rangement historique.

## Correspondance complète

| Ancienne exigence | Disposition | Référentiel courant | Tâches futures conservées |
|---|---|---|---|
| deb-package — Paquet corrélé à la release | AU_CANON_IDENTIQUE | [deb-package](../../specs/deb-package/spec.md) — Paquet corrélé à la release | 2.2, 2.3, 2.4 |
| deb-package — Distribution Debian indépendante PA et PBO PFO | CIBLE_ACTUALISEE | [deb-package](../../specs/deb-package/spec.md) — Distribution Debian indépendante PA et PBO PFO | 2.2, 2.3, 2.4 |
| deb-package — Trois binaires PA et PZT dans le paquet commun | AU_CANON_IDENTIQUE | [deb-package](../../specs/deb-package/spec.md) — Trois binaires PA et PZT dans le paquet commun | 2.2, 2.3, 2.4 |
| docker-image — Composition reproductible corrélée à la release | AU_CANON_IDENTIQUE | [docker-image](../../specs/docker-image/spec.md) — Composition reproductible corrélée à la release | 2.2, 2.3, 2.4 |
| docker-image — Composition image PBO PFO deux binaires PA et PZT | CIBLE_ACTUALISEE | [docker-image](../../specs/docker-image/spec.md) — Composition image PBO PFO deux binaires PA et PZT | 2.2, 2.3, 2.4 |
| pixs-agent — Trois binaires PA et six modes distincts de PZT | AU_CANON_IDENTIQUE | [pixs-agent](../../specs/pixs-agent/spec.md) — Trois binaires PA et six modes distincts de PZT | 2.2, 2.3, 2.4 |
| pixs-agent — Compilation différenciée validée | AU_CANON_IDENTIQUE | [pixs-agent](../../specs/pixs-agent/spec.md) — Compilation différenciée validée | 2.2, 2.3, 2.4 |
| pixs-agent — Démarrage système et session borné | AU_CANON_IDENTIQUE | [pixs-agent](../../specs/pixs-agent/spec.md) — Démarrage système et session borné | 2.2, 2.3, 2.4 |
| pixs-agent — Supervision PBO et collecte PA | AU_CANON_IDENTIQUE | [pixs-agent](../../specs/pixs-agent/spec.md) — Supervision PBO et collecte PA | 2.2, 2.3, 2.4 |
| pixs-agent — Qualification des binaires PA et PZT et de la composition | AU_CANON_IDENTIQUE | [pixs-agent](../../specs/pixs-agent/spec.md) — Qualification des binaires PA et PZT et de la composition | 2.2, 2.3, 2.4 |
| pixs-agent — Paramètres ouverts et absence d'implémentation implicite | AU_CANON_IDENTIQUE | [pixs-agent](../../specs/pixs-agent/spec.md) — Paramètres ouverts et absence d'implémentation implicite | 2.2, 2.3, 2.4 |
| pixs-agent — Matrice de recette PA PZT complète par profil | AU_CANON_IDENTIQUE | [pixs-agent](../../specs/pixs-agent/spec.md) — Matrice de recette PA PZT complète par profil | 2.2, 2.3, 2.4 |
| pixs-agent — Contrats publics de pixs.agent et propriété des opérations | AU_CANON_IDENTIQUE | [pixs-agent](../../specs/pixs-agent/spec.md) — Contrats publics de pixs.agent et propriété des opérations | 2.2, 2.3, 2.4 |
| pixs-agent — Interfaces de gestion PA au-dessus du socle | AU_CANON_IDENTIQUE | [pixs-agent](../../specs/pixs-agent/spec.md) — Interfaces de gestion PA au-dessus du socle | 2.2, 2.3, 2.4 |
| pzt — Module essentiel pixs.pzt et exécutable PZT indépendant | AU_CANON_IDENTIQUE | [pzt](../../specs/pzt/spec.md) — Module essentiel pixs.pzt et exécutable PZT indépendant | 2.2, 2.3, 2.4 |
| pzt — Expiration, révocation et protection indépendante | AU_CANON_IDENTIQUE | [pzt](../../specs/pzt/spec.md) — Expiration, révocation et protection indépendante | 2.2, 2.3, 2.4 |
| pzt — Contrat A08a — Socle initial puis profil passerelle ultérieur, option A validée | AU_CANON_IDENTIQUE | [pzt](../../specs/pzt/spec.md) — Contrat A08a — Socle initial puis profil passerelle ultérieur, option A validée | 2.2, 2.3, 2.4 |
| pzt — Cycle de vie propre du composant PZT | AU_CANON_IDENTIQUE | [pzt](../../specs/pzt/spec.md) — Cycle de vie propre du composant PZT | 2.2, 2.3, 2.4 |
| pzt — Contrôle de PZT et séparation de pixs.agent | AU_CANON_IDENTIQUE | [pzt](../../specs/pzt/spec.md) — Contrôle de PZT et séparation de pixs.agent | 2.2, 2.3, 2.4 |
| pzt — Frontières et identités PA PZT explicites | AU_CANON_IDENTIQUE | [pzt](../../specs/pzt/spec.md) — Frontières et identités PA PZT explicites | 2.2, 2.3, 2.4 |
| pzt — Correspondance des rôles réseau dans les contrats intégrés | AU_CANON_IDENTIQUE | [pzt](../../specs/pzt/spec.md) — Correspondance des rôles réseau dans les contrats intégrés | 2.2, 2.3, 2.4 |
| reference-runtime — Pile de référence unique | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Pile de référence unique | 2.2, 2.3, 2.4 |
| reference-runtime — Couche exécutable PA séparée | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Couche exécutable PA séparée | 2.2, 2.3, 2.4 |
| reference-runtime — Modules de gestion pixs.agent et pixs.pzt dans PBO | AU_CANON_IDENTIQUE | [reference-runtime](../../specs/reference-runtime/spec.md) — Modules de gestion pixs.agent et pixs.pzt dans PBO | 2.2, 2.3, 2.4 |
| runtime — États techniques PA et PZT distincts du runtime PBO | AU_CANON_IDENTIQUE | [runtime](../../specs/runtime/spec.md) — États techniques PA et PZT distincts du runtime PBO | 2.2, 2.3, 2.4 |
| runtime — Topologies locales et distantes PA PZT | AU_CANON_IDENTIQUE | [runtime](../../specs/runtime/spec.md) — Topologies locales et distantes PA PZT | 2.2, 2.3, 2.4 |

## Détails et critères maintenus par exigence

### 1. Paquet corrélé à la release

- Source historique prévue : [deb-package](historique-deltas-avant-e3/deb-package/spec.md). Ancien chemin : `specs/deb-package/spec.md`.
- Empreinte du bloc ancien normalisé : `cd7dc4d654f204278a52d0735068fe76e38fb2258c7c67dc6508760da8114ec5` ; fichier entier à conserver : `65a89a9b2108b41d719f1878d489706093bad401addd2d3c31483f6ac7055679`.
- Contrat courant : `deb-package` — Paquet corrélé à la release.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 2. Distribution Debian indépendante PA et PBO PFO

- Source historique prévue : [deb-package](historique-deltas-avant-e3/deb-package/spec.md). Ancien chemin : `specs/deb-package/spec.md`.
- Empreinte du bloc ancien normalisé : `1e1f6cf05d5eecf521089c0c095d1c13f4a7cc2a264e21dcc925928e6b9a8a3d` ; fichier entier à conserver : `65a89a9b2108b41d719f1878d489706093bad401addd2d3c31483f6ac7055679`.
- Contrat courant : `deb-package` — Distribution Debian indépendante PA et PBO PFO.
- Travail et critères compatibles à maintenir : Le binaire PBO commun et Core/Auth obligatoires complètent la composition ; indépendance des paquets conservée.
- Clauses remplacées / limites : Le binaire PBO commun et Core/Auth obligatoires complètent la composition ; indépendance des paquets conservée.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 3. Trois binaires PA et PZT dans le paquet commun

- Source historique prévue : [deb-package](historique-deltas-avant-e3/deb-package/spec.md). Ancien chemin : `specs/deb-package/spec.md`.
- Empreinte du bloc ancien normalisé : `754778ae0810a916b0c46f37c2a419ed3d7eacc5a553002d25f6e41c1ba24c87` ; fichier entier à conserver : `65a89a9b2108b41d719f1878d489706093bad401addd2d3c31483f6ac7055679`.
- Contrat courant : `deb-package` — Trois binaires PA et PZT dans le paquet commun.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 4. Composition reproductible corrélée à la release

- Source historique prévue : [docker-image](historique-deltas-avant-e3/docker-image/spec.md). Ancien chemin : `specs/docker-image/spec.md`.
- Empreinte du bloc ancien normalisé : `ad34820c19dd2946fdc81e7b040e9df95e838ed6c4ecebd884d3874f1ab7ccd8` ; fichier entier à conserver : `5ed2e74f8055f0493ebb4a4b1731a3a9c089aac79b1a47c7a634a6f01fd9abd6`.
- Contrat courant : `docker-image` — Composition reproductible corrélée à la release.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 5. Composition image PBO PFO deux binaires PA et PZT

- Source historique prévue : [docker-image](historique-deltas-avant-e3/docker-image/spec.md). Ancien chemin : `specs/docker-image/spec.md`.
- Empreinte du bloc ancien normalisé : `88797d9f4f94b24b4d84bbb90ebc8800c0647e2f0d9d0ea2ae2edbbb3decc1f7` ; fichier entier à conserver : `5ed2e74f8055f0493ebb4a4b1731a3a9c089aac79b1a47c7a634a6f01fd9abd6`.
- Contrat courant : `docker-image` — Composition image PBO PFO deux binaires PA et PZT.
- Travail et critères compatibles à maintenir : Le binaire PBO commun et Core/Auth sont explicités ; exclusion des sessions PA utilisateur et séparation PZT conservées.
- Clauses remplacées / limites : Le binaire PBO commun et Core/Auth sont explicités ; exclusion des sessions PA utilisateur et séparation PZT conservées.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 6. Trois binaires PA et six modes distincts de PZT

- Source historique prévue : [pixs-agent](historique-deltas-avant-e3/pixs-agent/spec.md). Ancien chemin : `specs/pixs-agent/spec.md`.
- Empreinte du bloc ancien normalisé : `265ecb7e7213f993d28d56801c5b79ef00ed936bad1a9f91ac69a12ce96abb95` ; fichier entier à conserver : `7b683a9d897c2f1c158be7e43f80397ec094385af29139c053af37e804c91987`.
- Contrat courant : `pixs-agent` — Trois binaires PA et six modes distincts de PZT.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 7. Compilation différenciée validée

- Source historique prévue : [pixs-agent](historique-deltas-avant-e3/pixs-agent/spec.md). Ancien chemin : `specs/pixs-agent/spec.md`.
- Empreinte du bloc ancien normalisé : `3281d04edfada74e5681cdc2e936ae8c97faac815cb95df7d5c42d4026f96306` ; fichier entier à conserver : `7b683a9d897c2f1c158be7e43f80397ec094385af29139c053af37e804c91987`.
- Contrat courant : `pixs-agent` — Compilation différenciée validée.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 8. Démarrage système et session borné

- Source historique prévue : [pixs-agent](historique-deltas-avant-e3/pixs-agent/spec.md). Ancien chemin : `specs/pixs-agent/spec.md`.
- Empreinte du bloc ancien normalisé : `3cae69b470006de7742776fc6cabe0f4319cc8881db44bbd6307c84aa27057c7` ; fichier entier à conserver : `7b683a9d897c2f1c158be7e43f80397ec094385af29139c053af37e804c91987`.
- Contrat courant : `pixs-agent` — Démarrage système et session borné.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 9. Supervision PBO et collecte PA

- Source historique prévue : [pixs-agent](historique-deltas-avant-e3/pixs-agent/spec.md). Ancien chemin : `specs/pixs-agent/spec.md`.
- Empreinte du bloc ancien normalisé : `ee97e221a8512881f6188f9dca81e48290c21a3fefd5ffbe99f0725ccb28e272` ; fichier entier à conserver : `7b683a9d897c2f1c158be7e43f80397ec094385af29139c053af37e804c91987`.
- Contrat courant : `pixs-agent` — Supervision PBO et collecte PA.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 10. Qualification des binaires PA et PZT et de la composition

- Source historique prévue : [pixs-agent](historique-deltas-avant-e3/pixs-agent/spec.md). Ancien chemin : `specs/pixs-agent/spec.md`.
- Empreinte du bloc ancien normalisé : `af862e6a17e5b375915ea8cfc66dd7c507630728effbcec2acd98ca816d61af9` ; fichier entier à conserver : `7b683a9d897c2f1c158be7e43f80397ec094385af29139c053af37e804c91987`.
- Contrat courant : `pixs-agent` — Qualification des binaires PA et PZT et de la composition.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 11. Paramètres ouverts et absence d'implémentation implicite

- Source historique prévue : [pixs-agent](historique-deltas-avant-e3/pixs-agent/spec.md). Ancien chemin : `specs/pixs-agent/spec.md`.
- Empreinte du bloc ancien normalisé : `0ee873122ad37d46c3a66cb229ef5d1bfa2c7f8a11abd0b36fbc7c10308f77b7` ; fichier entier à conserver : `7b683a9d897c2f1c158be7e43f80397ec094385af29139c053af37e804c91987`.
- Contrat courant : `pixs-agent` — Paramètres ouverts et absence d'implémentation implicite.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 12. Matrice de recette PA PZT complète par profil

- Source historique prévue : [pixs-agent](historique-deltas-avant-e3/pixs-agent/spec.md). Ancien chemin : `specs/pixs-agent/spec.md`.
- Empreinte du bloc ancien normalisé : `da46ed4aa4e73d23a85fd618dd56fe748b66e11866b0f7e432530b84175a9145` ; fichier entier à conserver : `7b683a9d897c2f1c158be7e43f80397ec094385af29139c053af37e804c91987`.
- Contrat courant : `pixs-agent` — Matrice de recette PA PZT complète par profil.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 13. Contrats publics de pixs.agent et propriété des opérations

- Source historique prévue : [pixs-agent](historique-deltas-avant-e3/pixs-agent/spec.md). Ancien chemin : `specs/pixs-agent/spec.md`.
- Empreinte du bloc ancien normalisé : `33b63fe5da55d70145d67ba2fe5cb125c5e69d548ef2d8d7ec4c7bd8427206e5` ; fichier entier à conserver : `7b683a9d897c2f1c158be7e43f80397ec094385af29139c053af37e804c91987`.
- Contrat courant : `pixs-agent` — Contrats publics de pixs.agent et propriété des opérations.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 14. Interfaces de gestion PA au-dessus du socle

- Source historique prévue : [pixs-agent](historique-deltas-avant-e3/pixs-agent/spec.md). Ancien chemin : `specs/pixs-agent/spec.md`.
- Empreinte du bloc ancien normalisé : `3b632592e0ea00dcc9b20d46509f2d4ad0c0e7ff176e31b870683f91e5613475` ; fichier entier à conserver : `7b683a9d897c2f1c158be7e43f80397ec094385af29139c053af37e804c91987`.
- Contrat courant : `pixs-agent` — Interfaces de gestion PA au-dessus du socle.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 15. Module essentiel pixs.pzt et exécutable PZT indépendant

- Source historique prévue : [pzt](historique-deltas-avant-e3/pzt/spec.md). Ancien chemin : `specs/pzt/spec.md`.
- Empreinte du bloc ancien normalisé : `c3150796ef377dbd8a57b789824deb40d114a56d1dbc62b2e76dcea8622ec3fc` ; fichier entier à conserver : `0e8d0b972e6abf3831b8ba6902a26df97d146ee5f983efe30d30f5ca6197ea2d`.
- Contrat courant : `pzt` — Module essentiel pixs.pzt et exécutable PZT indépendant.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 16. Expiration, révocation et protection indépendante

- Source historique prévue : [pzt](historique-deltas-avant-e3/pzt/spec.md). Ancien chemin : `specs/pzt/spec.md`.
- Empreinte du bloc ancien normalisé : `d2dbc61816414a53d0b62d807136e953b22db2f13e04f4de92bd0d5388f0a049` ; fichier entier à conserver : `0e8d0b972e6abf3831b8ba6902a26df97d146ee5f983efe30d30f5ca6197ea2d`.
- Contrat courant : `pzt` — Expiration, révocation et protection indépendante.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 17. Contrat A08a — Socle initial puis profil passerelle ultérieur, option A validée

- Source historique prévue : [pzt](historique-deltas-avant-e3/pzt/spec.md). Ancien chemin : `specs/pzt/spec.md`.
- Empreinte du bloc ancien normalisé : `95cf2c402f28c1a8b142e488cdcfd1df7799de589b5c5b19e19958907d074693` ; fichier entier à conserver : `0e8d0b972e6abf3831b8ba6902a26df97d146ee5f983efe30d30f5ca6197ea2d`.
- Contrat courant : `pzt` — Contrat A08a — Socle initial puis profil passerelle ultérieur, option A validée.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 18. Cycle de vie propre du composant PZT

- Source historique prévue : [pzt](historique-deltas-avant-e3/pzt/spec.md). Ancien chemin : `specs/pzt/spec.md`.
- Empreinte du bloc ancien normalisé : `69f6c202888e67abf9a2195070042b1b3ed5e175db2b681791096f24e8e86ee9` ; fichier entier à conserver : `0e8d0b972e6abf3831b8ba6902a26df97d146ee5f983efe30d30f5ca6197ea2d`.
- Contrat courant : `pzt` — Cycle de vie propre du composant PZT.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 19. Contrôle de PZT et séparation de pixs.agent

- Source historique prévue : [pzt](historique-deltas-avant-e3/pzt/spec.md). Ancien chemin : `specs/pzt/spec.md`.
- Empreinte du bloc ancien normalisé : `8e776e09204363dfbc005b336de2e8c935ebafa73da280549f77d384c0afff54` ; fichier entier à conserver : `0e8d0b972e6abf3831b8ba6902a26df97d146ee5f983efe30d30f5ca6197ea2d`.
- Contrat courant : `pzt` — Contrôle de PZT et séparation de pixs.agent.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 20. Frontières et identités PA PZT explicites

- Source historique prévue : [pzt](historique-deltas-avant-e3/pzt/spec.md). Ancien chemin : `specs/pzt/spec.md`.
- Empreinte du bloc ancien normalisé : `023be55518dc9ef387e2e34a34a3f6063a24f344fe18848388fe3680d3301197` ; fichier entier à conserver : `0e8d0b972e6abf3831b8ba6902a26df97d146ee5f983efe30d30f5ca6197ea2d`.
- Contrat courant : `pzt` — Frontières et identités PA PZT explicites.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 21. Correspondance des rôles réseau dans les contrats intégrés

- Source historique prévue : [pzt](historique-deltas-avant-e3/pzt/spec.md). Ancien chemin : `specs/pzt/spec.md`.
- Empreinte du bloc ancien normalisé : `2a0cc983f058588e467be6ff1427b9959e597731c90e1fe2c828821856cceb73` ; fichier entier à conserver : `0e8d0b972e6abf3831b8ba6902a26df97d146ee5f983efe30d30f5ca6197ea2d`.
- Contrat courant : `pzt` — Correspondance des rôles réseau dans les contrats intégrés.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 22. Pile de référence unique

- Source historique prévue : [reference-runtime](historique-deltas-avant-e3/reference-runtime/spec.md). Ancien chemin : `specs/reference-runtime/spec.md`.
- Empreinte du bloc ancien normalisé : `34214874a2c886e91410a2aaf6a4d571769d9c8e934b59016d0f2a22bd9c095b` ; fichier entier à conserver : `be52f5efc03413fb7a32d477ce23f86c6829fd5bf1220886f1780f948d2e87cc`.
- Contrat courant : `reference-runtime` — Pile de référence unique.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 23. Couche exécutable PA séparée

- Source historique prévue : [reference-runtime](historique-deltas-avant-e3/reference-runtime/spec.md). Ancien chemin : `specs/reference-runtime/spec.md`.
- Empreinte du bloc ancien normalisé : `df05fd906228334ebb2a1788bd4479cf593cb6cad2942c10dc88af14bfd50ed5` ; fichier entier à conserver : `be52f5efc03413fb7a32d477ce23f86c6829fd5bf1220886f1780f948d2e87cc`.
- Contrat courant : `reference-runtime` — Couche exécutable PA séparée.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 24. Modules de gestion pixs.agent et pixs.pzt dans PBO

- Source historique prévue : [reference-runtime](historique-deltas-avant-e3/reference-runtime/spec.md). Ancien chemin : `specs/reference-runtime/spec.md`.
- Empreinte du bloc ancien normalisé : `f2789f21c411dcd8cb768b9fb3f1dabfa6c465a99b0b635182b68b5fd611b3b6` ; fichier entier à conserver : `be52f5efc03413fb7a32d477ce23f86c6829fd5bf1220886f1780f948d2e87cc`.
- Contrat courant : `reference-runtime` — Modules de gestion pixs.agent et pixs.pzt dans PBO.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 25. États techniques PA et PZT distincts du runtime PBO

- Source historique prévue : [runtime](historique-deltas-avant-e3/runtime/spec.md). Ancien chemin : `specs/runtime/spec.md`.
- Empreinte du bloc ancien normalisé : `bf9a5bd418498946f51e5a6ebd75331deeee119037b87e85ba8cf9dfe3535f3b` ; fichier entier à conserver : `9bc4673b83304c2746a402b5ae8b2ad55b52e88b2e2995fd5f68c69cef0cc776`.
- Contrat courant : `runtime` — États techniques PA et PZT distincts du runtime PBO.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

### 26. Topologies locales et distantes PA PZT

- Source historique prévue : [runtime](historique-deltas-avant-e3/runtime/spec.md). Ancien chemin : `specs/runtime/spec.md`.
- Empreinte du bloc ancien normalisé : `6d7fb92b6868ba5710cdc5046073994dc1356fdb5afd8425c7c1e7d72b3e5954` ; fichier entier à conserver : `9bc4673b83304c2746a402b5ae8b2ad55b52e88b2e2995fd5f68c69cef0cc776`.
- Contrat courant : `runtime` — Topologies locales et distantes PA PZT.
- Travail et critères compatibles à maintenir : Le contrat est repris au canon ; sa réalisation et ses preuves restent à compléter selon les tâches ouvertes.
- Clauses remplacées / limites : Aucune suppression de besoin ; contrat courant référencé.
- Rattachement actif : tâches 2.2, 2.3, 2.4 de [tasks.md](tasks.md), sous-lots d'origine conservés. La réalisation doit relier les scénarios courants et les critères compatibles ci-dessus à des preuves réelles avant validation.

## Travail restant explicitement actif

Sur 13 tâches d’origine, 10 restent cochées historiquement et 3 restent non cochées. Leur contenu et leur état sont préservés. La liste suivante est une vue des tâches sources, pas un nouveau registre ou une deuxième série de cases.

| Tâche | Sous-lot conservé | Libellé source | État |
|---|---|---|---|
| 2.2 | PA10-SL11 | 2.2 Coordonner les contrats PA/PZT avec PA01/PA03 et pixs.pzt avec C14 : exécutants, identités, preuves, lifecycle et canaux ; réconcilier les instantanés de préparation avant code. | À FAIRE ; preuve future requise |
| 2.3 | PA10-SL12 | 2.3 Coordonner PA09/X01 pour conserver les contenus Debian/Docker et les frontières de supervision, sans dépendance PBO locale imposée à PA/PZT. | À FAIRE ; preuve future requise |
| 2.4 | PA10-SL13 | 2.4 Qualifier avec les lots propriétaires les scénarios de gestion séparée, transport local/distant, deux topologies distantes, panne, sécurité et compositions ; conserver les preuves avant toute revendication de livraison. | À FAIRE ; preuve future requise |

## Contrôles et limites

Avant déplacement : existence des contrats cibles, rattachements à des tâches ouvertes et empreintes des 21 fichiers contrôlés. Après déplacement : égalité des octets, mise à jour des liens, même contenu et mêmes cases des tâches, mêmes identifiants de sous-lots et validation OpenSpec à vérifier. Aucun code, test produit, service, migration, archive ou publication n’est exécuté par ce contrôle documentaire.

## Contrôle après déplacement

Les empreintes des fichiers entiers ont été vérifiées après déplacement et sont identiques aux sources. Les 21 déplacements conservent les octets ; les liens fonctionnels entrants ont été actualisés dans les dossiers concernés. Les tâches, cases et identifiants de sous-lots restent inchangés. Aucun besoin compatible n’est déclaré réalisé par ce rangement.
