# Design — add-initial-identity-assurance-vocabulary-v1

## Contexte
L'existant src/pixs/core/authz/policy.py définit IdentityAssurance avec CLAIMED, VERIFIED, PROOFED. Une façade authz EXISTE déjà et exporte IdentityAssurance. Le canon publié définit déjà exactement le profil : ce change qualifie la conformité de la production existante par tests et traçabilité, sans modification normative nouvelle.

## Réutilisation sans duplication
Réutilisation exclusive de pixs.core.authz.policy.IdentityAssurance existant. Aucun nouvel Enum, aucune copie de valeurs, aucune façade créée ou modifiée, aucun helper de production. Les tests importent l'existant et vérifient le comportement observable.

## Ordre et représentation
Aucun ordre intrinsèque attribué. Tout ordre externe legacy éventuel hors Enum reste inchangé et hors périmètre. Aucun contrat hostile d'égalité ou de représentation inventé : pas de __eq__ ni de __repr__ spécifique, comparaison par identité et littéral existants uniquement.

## Effets exclus
Pas de valeur par défaut, pas de classement ordinal, pas de mapping fournisseur, pas de transition, pas de preuve, pas de calcul d'assurance, pas d'authentification, pas de session, pas d'accès, pas d'audit, pas de persistance.

## Stratégie de test réaliste
Deux seuls fichiers : tests/unit/test_identity_assurance.py et tests/integration/test_identity_assurance_integration.py, avec unittest et stdlib existante. Processus enfant sous -B. Le test frais bloque les imports de modules DB non déjà chargés ainsi que les sockets et écritures observables, sans aucune invocation des ports horloge, audit ou auth. L'import lit nécessairement des modules Python ; aucune absence de toute lecture I/O n'est promise. Vérifications : fermeture aux trois valeurs exactes avec type et littéral, refus FOREIGN, None et absence sans défaut, absence d'ordre intrinsèque, import frais, identité nominale avec consommateurs authz, non-régression identité et authz, production identique par hashes.

## Limites
Aucun Git. Seule alerte de longueur canonique exacte acceptée. Aucune affirmation de résultat strict sans exécution observée.
