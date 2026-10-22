# C03 — Authentification et sessions

## Pourquoi

Le code expose des identités structurelles et mappings d’assurance ; il ne démontre pas une authentification de session réellement utilisable.

## Modifications proposées

Réaliser, sous mandat ultérieur, la connexion/déconnexion et les sessions du module essentiel `pixs.auth`, avec provider local autonome et PostgreSQL par défaut selon le [cadrage Auth adopté pour l'architecture essentielle](../../define-essential-autonomous-auth-module/proposal.md). Préserver l’authentification propre du Super Admin, sessions/jetons bornés, rotation, révocation et niveaux d’assurance obtenus. Les émetteurs IdP, services propres OpenLDAP/KDC et connecteurs externes ont des dossiers distincts ; ces derniers sont absents de l’installation standard.

## Capacités

### Capacités nouvelles

Aucune nouvelle capacité. Les dix-sept décisions du 20 octobre 2026 précisent le profil local dans la capacité existante `authentication`.

### Capacités modifiées

`authentication` : [delta adopté le 20 octobre 2026](specs/authentication/spec.md) pour contrats spécialisés, sessions côté serveur, jetons opaques, durées, fraîcheur, rotation, réutilisation, concurrence, changement de mot de passe, Argon2id et conservation CLI. `requirements.md` relie les décisions aux exigences désormais canoniques. `skip_specs` reste désactivé et le delta source est conservé pour traçabilité.

Les raccordements restent propriétaires : C04 pour le sujet d’amorçage pré-session, C05 pour la transaction d’audit et l’exception limitée au retrait d’accès, N04 pour la façade web à cookie distincte de l’API Bearer, C06 pour les contrats HTTP et C08 pour R01. Les deltas liés aux dix-sept décisions sont adoptés au canon le 20 octobre 2026, dont les seules deux clauses de transport ajoutées à N04 ; les autres propositions N04 restent distinctes.

## Dépendances

- `define-essential-autonomous-auth-module` : trois deltas d'architecture adoptés au canon le 20 octobre 2026 ; C03 ne les duplique pas.
- [add-pbo-runtime-secret-provider](../2026-10-19-add-pbo-runtime-secret-provider/proposal.md).
- [add-core-postgres-services](../2026-10-20-add-core-postgres-services/proposal.md).

- `add-durable-minimized-audit` : audit durable des authentifications, refus et décisions runtime.

## Impact

Périmètre de réalisation futur : Authentifier une DigitalIdentity par un provider explicitement approuvé, établir un contexte canonique et des sessions/jetons persistants bornés. Ne jamais rapprocher par courriel. L’authentification propre du Super Admin reste distincte de l’exemption de MFA ; le navigateur ne persiste pas de justificatif par défaut.

Le périmètre documentaire du 20 octobre 2026 couvre ce dossier, les raccordements C04/C05/C06/C08/N04 et TECHNICAL.md. Aucun code, test produit, migration, manifeste de dépendances, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches de réalisation ne sont pas lancées. Argon2-cffi et cryptography sont sélectionnés pour ajout futur, avec versions stables à qualifier et épingler.

## Critères de sortie de réalisation future

Connexion/déconnexion et révocation réelles ; jeton ou session expiré refusé ; aucune fusion par courriel ; aucun MFA fictif ni exigence MFA interdite au premier démarrage/secours.

## Barrière de conception

Le cadrage conserve le local autonome PostgreSQL dans `pixs.auth`. Les [décisions D01–D17](design.md#décisions-d01d17-du-20-octobre-2026) fixent transports, paramètres et mécanismes. Les contrats détaillés, schémas, versions et profils restent à qualifier avant réalisation. La précision D11 conserve Argon2id et exige la qualification de réutilisation avec OpenLDAP par adaptation du format, sans affaiblissement ni activation implicite d’un annuaire.

Les [arbitrages de réalisation](design.md#arbitrages-de-réalisation-à-valider) distinguent décisions acquises et qualifications restantes. Les deltas des dix-sept décisions sont adoptés ; les qualifications restantes précèdent toute réalisation ultérieure autorisée. Les trois deltas d’architecture déjà canoniques et les autres changes Auth restent distincts.
