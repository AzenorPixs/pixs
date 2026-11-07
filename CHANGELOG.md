# Changelog — Pixs

Toutes les évolutions significatives de Pixs et de son outillage de contribution versionné sont documentées dans ce fichier.

## Unreleased

- Réalisation C11 du shell frontend composé : sélection opérateur épinglée,
  imports et graphe contrôlés, rendu des contributions déclarées, contexte WEB
  Auth, états Query/Command et cinq champs typés. Le mode autonome est conservé.
  Les garanties sont documentées ; recettes, qualification du bundle/transport
  et validation globale restent à exécuter avant livraison de ce change.

- Ajout de la gestion PBO Agent : contrats publics 1.0.0, persistance PostgreSQL
  séparant souhaité, observé et confirmé, autorisation et audit Core, adaptateur
  de composition et supervision avec péremption et réconciliation sans réémission.
  L’absence de transport PZT est refusée explicitement ; les preuves exécutant
  et les qualifications locales/distantes restent aux lots propriétaires.

- Ajout de la gestion propriétaire PZT/DNS : contrats versionnés, persistance
  et idempotence PostgreSQL auditées, configuration souhaitée, routes HTTP et
  contributions de gestion frontend. Les issues inconnues restent explicites ;
  aucun état réseau appliqué ou mesuré n’est fabriqué. Les exécutants et le
  service DNS actif restent à qualifier séparément.


- Déclaration documentaire OpenSpec de pixs-agent et pzt, avec les 174 contrats
  validés et les 68 critères de recette PA ; alignement de deb-package,
  docker-image, runtime et reference-runtime. Compilation prévue : Nuitka pour
  trois binaires PA système/utilisateur, Cython pour PZT. Aucun code, installation,
  test logiciel, build, signature ou publication réalisé par ce change.

- Intégration des cadrages Pixs Agent et PZT dans PROJECT.md, TECHNICAL.md et
  BUILD.md : conservation des 174 références de décision, des 68 critères de
  recette PA et des paramètres ouverts ; retrait des deux documents sources
  après vérification de couverture.
- Cible de distribution précisée : paquet Debian PA indépendant à quatre
  binaires ; paquet PBO/PFO distinct ; image Docker PBO/PFO avec trois binaires
  PA système/PZT, sans binaire utilisateur ni fonctions de session. PZT est un
  module essentiel de PBO et s’exécute par son binaire PA lorsqu’il est activé.
  Implémentation, qualification des artefacts et publication restent à réaliser.
