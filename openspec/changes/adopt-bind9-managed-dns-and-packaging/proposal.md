# Z27 — Choix BIND 9 pour le DNS géré et sa distribution

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

BIND 9 et sa distribution selon la nouvelle frontière PA/DZT, sans étendre les six tâches cochées historiques au nouveau périmètre.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [pzt](../../specs/pzt/spec.md).
- [deb-package](../../specs/deb-package/spec.md).
- [docker-image](../../specs/docker-image/spec.md).
- [zt-dns-dhcp](../../specs/zt-dns-dhcp/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Statut et autorisation

SPÉCIFICATION_VALIDÉE — CHANGE_OUVERT le 24 octobre 2026, sur validation
explicite du développeur : « Je valide la spécification BIND 9. Tu peux
ouvrir le change sans implémentation ni production de code ».

Le dossier existant reste ouvert sous son identifiant actuel. Après validation
de la spécification, le développeur a autorisé le 24 octobre 2026 la
synchronisation du canon et les renvois vers Z05 et les lots Debian/Docker,
toujours sans implémentation ni production de code. Les trois exigences
et neuf scénarios sont intégrés à pzt, deb-package et docker-image ; la
réalisation, l'installation, la configuration et l'activation restent différées.

## Pourquoi

Le développeur a retenu le 23 octobre 2026 BIND 9 fourni par Debian, installé et configuré par un PA désigné, ainsi que sa présence dans l'image Docker Pixs. Il a confirmé que l'activation du service reste ultérieure et a demandé une spécification distincte de C14.

Le [dossier Z05](../add-pzt-managed-dns-service-and-pa-adapters/proposal.md) porte déjà l'exécution DNS et les adapters PA. Ce change précise le logiciel et sa distribution ; il ne recrée pas ce lot d'exécution.

## Modifications proposées

- Retenir BIND 9 comme fournisseur du service DNS géré sur Debian et dans Docker Pixs.
- Conserver PBO comme propriétaire de la gestion et PA comme exécutant autorisé de l'installation, de la configuration et du lifecycle du service distinct.
- Fournir le logiciel dans l'image Docker sans état d'instance, clé privée ni activation implicite.
- Lier la qualification aux versions Debian, aux artefacts, aux contrats PA/PZT et aux garanties DNS existantes.

## Capacités

### Capacités nouvelles

Aucune nouvelle capacité applicative. Le module de gestion reste pixs.dns.

### Capacités modifiées

- pzt : sélection de BIND 9, séparation des propriétaires et absence d'activation implicite.
- deb-package : installation de BIND 9 par le PA du rôle serveur DNS sélectionné.
- docker-image : présence du logiciel BIND 9 dans l'image Pixs, avec état et activation séparés.

Les trois deltas validés sont synchronisés dans le canon le 24 octobre 2026. Leurs textes restent conservés dans ce change comme trace de la décision ; ils ne représentent pas une seconde réalisation. Le change reste ouvert et non archivé.

## Impact

Z05 réalisera et qualifiera le raccord BIND 9. PA01/PA10 fournissent les garanties d'exécution et de gestion nécessaires ; les lots de distribution Debian et Docker portent leurs artefacts. C14 conserve son profil de gestion sans service DNS actif sélectionné. Les dépendances manquantes ne sont pas remplacées par des doubles réputés qualifiés.

## Non-objectifs

Cette préparation n'installe aucun paquet, ne démarre aucun serveur, n'ouvre aucun port et ne modifie aucun volume, utilisateur, droit ou réseau. Elle ne livre aucun transport PA/PZT, certificat ou binaire et ne sélectionne pas le service DNS actif dans C14.


## Renvois des lots propriétaires

- [Z05 — service DNS et adapters PA](../add-pzt-managed-dns-service-and-pa-adapters/design.md) : réalisation BIND 9 et conformité DNS.
- [C18 — paquet Debian PBO/PFO](../build-first-pbo-pfo-debian-package/design.md) : gestion DNS dans PBO, sans serveur imposé à chaque hôte.
- [PA09 — paquet indépendant PA/PZT](../build-and-publish-independent-pa-debian-package/design.md) : exécutant autorisé du rôle serveur Debian.
- [X01 — image Docker Pixs](../build-and-qualify-pixs-docker-image/design.md) : fourniture logicielle, couches sans état ni secret, activation séparée.

## Statut des deltas antérieurs après contrôle E3

Les anciens fichiers sous specs/ ont été déplacés, avec empreintes conservées, vers [l’historique interne](historique-deltas-avant-e3/README.md). Le [contrôle de couverture](COUVERTURE_DELTAS_E3.md) relie chaque ancienne exigence au contrat courant et aux tâches ouvertes. Le dossier reste actif ; skip_specs évite seulement la réapplication des anciennes prescriptions. Il ne termine ni la réalisation, ni les tests, ni les 49 tâches encore ouvertes dans les sept dossiers concernés.
