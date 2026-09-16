## 1. Composition P0 initiale

- [x] 1.1 Décrire la conformité de la composition initiale à
  `reference-composition`, y compris son composant d'exemple technique non
  métier.
- [x] 1.2 Vérifier que les exigences de composition préservent Django,
  PostgreSQL, `pixs.kernel`, `pixs.core`, les contrats publics et l'absence de
  valeur sensible distribuée.

## 2. Surface et shell initialement spécifiés

- [x] 2.1 Définir les frontières documentaires des routes de santé, du shell et
  de l'API versionnée sans introduire de ressource métier fictive.
- [x] 2.2 Vérifier la cohérence de ces frontières avec les capacités API,
  frontend, sécurité et contrats publics existantes.

## 3. Profil local de référence

- [x] 3.1 Décrire le profil local comme cible de validation future, ses
  dépendances, son adresse d'écoute, son cycle et ses limites non productives.
- [x] 3.2 Vérifier qu'aucune exigence du profil ne requiert de secret, de
  donnée métier permanente ou de dépendance de production.

## 4. Installation et administration spécifiées

- [x] 4.1 Vérifier les transitions documentées entre INSTALLER,
  FIRST_CONFIGURATION, NORMAL et MAINTENANCE ainsi que les marqueurs externes.
- [x] 4.2 Vérifier que le Super Admin est l'opérateur initial doté d'une
  identité numérique vérifiée et d'une politique d'autorisation déclarée, avec
  un bypass ACL limité au panneau d'administration.
- [x] 4.3 Vérifier que toute valeur PostgreSQL saisie par l'installateur devient
  une référence `SecretProvider` sans persistance ni exposition de credential.

## 5. Audit, maintenance et conformité documentaire

- [x] 5.1 Vérifier les exigences de maintenance hiérarchisée et d'audit
  persistant des interactions administratives contre les capacités actives.
- [x] 5.2 Exécuter les validations OpenSpec strictes applicables et vérifier
  que ce change ne requiert ni code, ni dépendance, ni configuration
  exécutable.
- [x] 5.3 Présenter les spécifications consolidées au développeur avant toute
  demande d'archivage ; toute implémentation future relèvera d'un change
  distinct autorisé.
