# Tâches — binaire PBO commun et ressources

## 1. Formalisation documentaire

- [x] 1.1 Relire cadrages, canon, séparation PA/PZT et baseline OpenSpec strict.
- [x] 1.2 Aligner les cadrages, README et schémas sur le binaire commun et les plans de ressources.
- [x] 1.3 Synchroniser les sept capacités canoniques et produire les deltas de traçabilité.
- [x] 1.4 Vérifier cohérence, compteurs, liens, UTF-8/LF, schémas et strict global incluant les capacités ciblées ; consigner les résultats.

- [x] 1.5 Intégrer Nuitka standalone pour PBO, distinguer les deux modes d'exploitation et Cython ciblé dans PBO des chaînes Cython PA/PZT ; vérifier canon, deltas, compteurs et contrôles documentaires.
- [x] 1.6 Vérifier la cohérence finale : nommer les modes Standalone/ZT, distinguer autonomie de gouvernance et activation PZT, ajouter le scénario Standalone avec PA, harmoniser les schémas et contrôler canon/deltas et strict global.

## 2. Réalisation future — non engagée

- [ ] 2.1 Qualifier la chaîne Nuitka standalone PBO, ses versions/options, dépendances et ressources, chargement des extensions, noms/CLI, schémas et valeurs des profils ; distinguer exploitation Standalone/ZT sans nouvelle dépendance implicite.
- [ ] 2.2 Réaliser le binaire PBO et ses rôles/processus configurables avec les propriétaires existants et la persistance de référence.
- [ ] 2.3 Réaliser plans et suivi de ressources PA/PZT avec sessions, idempotence, propriétaire réseau et garanties de sécurité conservés.
- [ ] 2.4 Adapter et qualifier superviseurs, paquets et image, limites effectives et états demandé/appliqué sans élargissement des privilèges.
- [ ] 2.5 Qualifier mémoire, CPU, latence, débit, saturation, reconfiguration, révocation et reprise par cible ; n'admettre Cython dans PBO que pour des optimisations ciblées mesurées, avec non-régression ; conserver les preuves avant publication.
