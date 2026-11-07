# PA10 — Séparer PA, PZT et les modules de gestion PBO

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

Raccords Agent/PZT et nouveaux contextes ; préserver les versions et preuves anciennes sans qualification nouvelle par héritage.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [pixs-agent](../../specs/pixs-agent/spec.md).
- [pzt](../../specs/pzt/spec.md).
- [scope-context](../../specs/scope-context/spec.md).
- [managed-device-policies](../../specs/managed-device-policies/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Pourquoi

Le développeur a validé le 17 octobre 2026 la séparation de l'exécutable réseau
PZT de PA et deux propriétaires de gestion PBO : pixs.agent pour PA hors PZT,
pixs.pzt pour PZT. Les schémas généraux omettaient les exécutants et les deux
cas distants, avec ou sans PBO/PFO locaux. Le canon attribuait encore PZT à PA.

## Ce qui change

- Définir PA à trois binaires/six modes et PZT comme exécutable indépendant.
- Formaliser configuration, administration, supervision et contrats PA dans
  pixs.agent ; nommer pixs.pzt le module essentiel de gestion réseau PBO.
- Conserver PZT pour tous les échanges PBO–PA, y compris locaux, et le contrôle
  sécurisé PBO–PZT, avec les garanties d'identité, de mandat et d'attestation.
- Conserver le paquet commun Debian à trois binaires PA plus PZT, séparé du
  paquet PBO/PFO ; conserver Docker à PBO/PFO, deux binaires PA et PZT.
- Représenter les hôtes distants PA/PZT seuls ou avec PBO/PFO facultatifs.
- Aligner les cadrages, le README et les dossiers préparatoires concernés.

## Capacités

### Capacités modifiées

- pixs-agent : trois binaires, six modes et gestion par pixs.agent hors PZT.
- pzt : exécutable indépendant, gestion essentielle pixs.pzt et interfaces.
- deb-package : paquet commun PA/PZT séparé de PBO/PFO, contenu inchangé.
- docker-image : deux binaires PA plus PZT indépendant, sessions PA exclues.
- reference-runtime : modules PBO distincts et exécutants hors autorité métier.
- runtime : états propres PA/PZT et topologies locales/distantes autorisées.

Aucune nouvelle capacité canonique. Les deltas tracent la décision approuvée ;
le canon est mis à jour dans cette session sur demande explicite. Ils ne sont
pas des ajouts normatifs encore en attente et ne doivent pas être comptés deux fois.

## Impact et autorisation

La présente session réalise uniquement documentation, spécifications et contrôles
documentaires. Elle ne réalise aucun code, manifest produit, migration, test
runtime, installation, build, déploiement, publication, commit, push ou archivage.
Les tâches d'implémentation restent non cochées et nécessitent un mandat distinct.
La sélection du premier P0 et les profils non encore qualifiés restent inchangés.

## Coordination

Ce change possède la définition et la future réalisation de pixs.agent ainsi que
la coordination de séparation PA/PZT. Les dossiers existants conservent leur
propriété sur compilation, lifecycle, module réseau, distributions et recettes ;
ils sont relus contre le nouveau canon avant toute implémentation.

## Statut des deltas antérieurs après contrôle E3

Les anciens fichiers sous specs/ ont été déplacés, avec empreintes conservées, vers [l’historique interne](historique-deltas-avant-e3/README.md). Le [contrôle de couverture](COUVERTURE_DELTAS_E3.md) relie chaque ancienne exigence au contrat courant et aux tâches ouvertes. Le dossier reste actif ; skip_specs évite seulement la réapplication des anciennes prescriptions. Il ne termine ni la réalisation, ni les tests, ni les 49 tâches encore ouvertes dans les sept dossiers concernés.
