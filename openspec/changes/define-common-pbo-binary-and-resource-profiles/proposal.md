# Binaire PBO commun et profils de processus selon les ressources

## Pourquoi

La décision du 21 octobre 2026 retient une même application PBO regroupant
Kernel, Core, Auth, Agent et module PZT, distribuée par un binaire commun.
Les profils web, worker et scheduler existent au canon ; leur dimensionnement
et celui des exécutants PA/PZT doivent être explicitement liés aux ressources
réellement accordées à chaque environnement.

## Ce qui change

- Définir le binaire PBO commun Nuitka standalone et préserver les contrats des modules.
- Distinguer compilation standalone et exploitation Standalone ou ZT du même binaire.
- Réserver Cython dans PBO aux optimisations ciblées justifiées par profilage, mesures de gain et non-régression ; retenir Cython pour les trois binaires PA et le binaire PZT indépendant.
- Configurer rôles, processus, concurrence et budgets PBO selon l'environnement.
- Conserver les trois binaires/six modes PA et le binaire indépendant PZT,
  avec leurs propres plans de processus et ressources locales ou distantes.
- Distinguer ressources détectées, budget accordé, configuration demandée,
  configuration effective et état appliqué ; encadrer toute adaptation.
- Préserver sécurité, reprise, sessions, baux scheduler et propriétaire réseau
  unique PZT par périmètre, sous supervision déclarée.
- Harmoniser cadrages, README, schémas et distributions Debian/Docker.

## Capacités

### Capacités modifiées

- reference-runtime : binaire PBO commun et qualification de sa construction.
- runtime : rôles, dimensionnement, supervision et qualification des ressources.
- pixs-agent : compilation Cython, processus par rôle/session et coordination des opérations PA.
- pzt : processus configurables avec propriétaire réseau unique et garanties.
- deb-package : livraison du binaire PBO et configuration externe des profils.
- docker-image : même binaire, quotas effectifs et réplication contrôlée.
- reference-composition : preuve du binaire et du plan de ressources du P0.

Aucune nouvelle capacité. Les deltas sont adoptés et synchronisés au canon
dans cette décision documentaire ; ils ne doivent pas être comptés ou rejoués
comme des ajouts encore proposés.

## Impact

La réalisation produit, les builds, l'installation, les mesures de performance,
le déploiement et la publication restent à engager sous mandat distinct.
Nuitka en mode standalone est retenu pour PBO ; versions/options, schémas/CLI,
nombres de processus et seuils restent à qualifier. Aucun outil ni dépendance
n'est installé. Les trois binaires PA et le binaire PZT utilisent Cython.
Le profil P0 conserve ses autres exigences ; aucune qualification n'est déduite
de cette adoption. Aucun archivage n'est effectué.
