# Séparer PA, PZT et les modules de gestion PBO

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
