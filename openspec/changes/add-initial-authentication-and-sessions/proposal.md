# C03 — Authentification et sessions

## Pourquoi

Le code expose des identités structurelles et mappings d’assurance ; il ne démontre pas une authentification de session réellement utilisable.

## Modifications proposées

Implémenter le provider choisi en C00, l’authentification propre du Super Admin, sessions/jetons bornés, rotation, révocation et niveaux d’assurance obtenus. OIDC/SAML restent non sélectionnés si inutiles.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions du profil C00 adoptées le 18 octobre 2026 et intégrées au canon.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `add-pbo-runtime-secret-provider`.
- `add-core-postgres-services`.

- `add-durable-minimized-audit` : audit durable des authentifications, refus et décisions runtime.

## Impact

Périmètre de réalisation futur : Authentifier une DigitalIdentity par un provider explicitement approuvé, établir un contexte canonique et des sessions/jetons persistants bornés. Ne jamais rapprocher par courriel. L’authentification propre du Super Admin reste distincte de l’exemption de MFA ; le navigateur ne persiste pas de justificatif par défaut.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Connexion/déconnexion et révocation réelles ; jeton ou session expiré refusé ; aucune fusion par courriel ; aucun MFA fictif ni exigence MFA interdite au premier démarrage/secours.

## Barrière de conception

Provider initial, choix sessions/cookies/Bearer par façade, rotation/révocation et durées. Ces arbitrages modifient sécurité et contrats : revue avant réalisation, sans valeurs arbitraires.
