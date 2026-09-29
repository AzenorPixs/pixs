# Tasks

## 1. Modèles et contrat

- [x] 1.1 Implémenter Group et Membership immuables avec UUIDv7, contexte explicite et erreurs stables.
- [x] 1.2 Implémenter la validation ensembliste n:m : références, doublons, unicité d'identifiants et non-mutation.
- [x] 1.3 Étendre la façade identity et adapter uniquement les exports attendus du test existant.

## 2. Tests et conformité

- [x] 2.1 Prouver les cas valides et invalides des groupes/appartenances, dont contextes et données hostiles, via la suite unitaire.
- [x] 2.2 Prouver l'usage de la façade avec User et ScopeContext sans accès implicite.
- [x] 2.3 Réussir les suites complètes séparées, AST, UTF-8/LF et OpenSpec strict ; contrôler cohérence et périmètre avant archivage.

## Preuves finales contrôlées par CGPT

- Modèles et contrats relus : Group porte UUIDv7 et ScopeContext explicite ; Membership reste une relation de paire n:m. Réutilisation des validateurs identité/scope, références et unicité dans l'ensemble fourni, aucun état conservé.
- Unités : `groups-unit01`, outil `msg_0eeb054ce001ido650hzodg3Wv` — 316 tests OK, exit 0, dont 12 nouveaux tests groupes.
- Intégration : `groups-integration01`, outil `msg_0eeb1d205001C1KoqA05AtP7mp` — 103 tests OK, exit 0, dont 3 nouveaux tests groupes ; contrat identité existant préservé.
- Syntaxe et encodage : `groups-ast01`, outil `msg_0eeb34555001SScPRfZpw7SuvD` — 5 AST et 9 fichiers UTF-8/LF valides, exit 0.
- OpenSpec : `groups-strict02`, outil `msg_0eeb49602001y74Wbnm1qd0W5j`, rapport `msg_0eeb4a56a001xxidX0u41ZbQwU` — 77 éléments valides, 0 échec, exit 0.
- Périmètre : neuf fichiers attendus réconciliés avec leurs écritures observées ; identity/models.py inchangé (SHA-256 `253bac3be28375e78f8ca406a790e7e504a0b53d480785e5cb319baef2fe1a57`). Cohérence PROJECT §18, TECHNICAL §§11/13, core, scope et cadrages généraux contrôlée.
- Les tests ont été corrigés avant exécution pour employer une vraie sous-classe de tuple et couvrir les contextes incomplets/altérés et la revalidation ensembliste. Toutes les commandes de validation du change ont réussi.
- L'archivage et le rapport STATISTIQUES restent deux mandats distincts. Le développeur a demandé l'arrêt après archivage de ce change ; aucune sélection suivante ne doit être lancée après contrôle du rapport.
- Topologie, autorisation, persistance Django/PostgreSQL, groupes imbriqués et audit durable restent hors périmètre ; le projet global n'est pas déclaré terminé.
