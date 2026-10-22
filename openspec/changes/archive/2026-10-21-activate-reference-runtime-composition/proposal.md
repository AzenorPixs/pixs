# C07 — Composition et lifecycle réels

## Pourquoi

Le gabarit est toujours non prêt, les profils sont déclaratifs et composition_proof reste partielle ; l’activation réelle intégrée n’est pas démontrée.

## Modifications proposées

Fournir l’hôte Django de composition Kernel/Core/Auth/providers et les adaptateurs de lifecycle ; relier les contrôles de versions et preuves authentifiées aux capacités réellement présentes. Définir le branchement PZT sans le simuler : les tests intermédiaires restent bornés et le passage P0 à ready demeure refusé tant que C14 et les autres obligations manquent.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions du profil C00 adoptées le 18 octobre 2026 et intégrées au canon.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- [C01 — provider de secrets runtime](../2026-10-19-add-pbo-runtime-secret-provider/proposal.md), archivé.
- [C02 — services Core PostgreSQL](../2026-10-20-add-core-postgres-services/proposal.md), archivé.
- [C03 — authentification locale et sessions](../2026-10-21-add-initial-authentication-and-sessions/proposal.md), producteur des contrats publics Auth.
- [C05 — audit durable minimisé](../2026-10-21-add-durable-minimized-audit/proposal.md), producteur du sink d’audit.

Le canon adopté le 20 octobre 2026 impose `pixs.auth` essentiel et sa capacité locale PostgreSQL, avec dépendance vers les seuls contrats publics Core. C07 consomme les interfaces C03 et C05 ; il ne réalise pas leurs services à leur place. Les preuves de ces dépendances sont requises avant l’intégration correspondante.

## Impact

Périmètre de réalisation : Fournir l’hôte runtime et les adapters du lifecycle commun, sans remplacer les mécanismes purs. Lier composants/providers/configuration/migrations et preuves authentifiées. L’hôte intermédiaire peut être exercé isolément mais refuse readiness P0 si PZT/DNS ou toute autre obligation manque ; C14 et C17 ferment l’intégration.

La reprise documentaire validée le 20 octobre 2026 puis la RSMP limitée de tâche 2.4 validée le 21 octobre cadrent le socle hôte intermédiaire C07. Le plan, le contexte, les adapters génériques et l’entrée INSTALLER/web possèdent les preuves bornées réunies dans [VALIDATION.md](VALIDATION.md). Les tâches locales et le cycle d’archive restent soumis à leurs preuves respectives.

## Critères de sortie de réalisation future

Ordre de composition déterministe, entrée runtime réelle en environnement isolé ; composant essentiel absent, fournisseur ambigu ou preuve manquante → P0 hors service. L’hôte intermédiaire ne certifie pas le produit ; intégration complète de PZT en C14 et recette installable en C17.

## Barrière de conception

Entrée de lancement retenue : fabrique INSTALLER/web explicite et routes minimales fermées. Registre : adapters fournis explicitement, identifiés/versionnés et observés avant/après hooks communs. Le verdict `globally_compatible=False` reste distinct de toute disponibilité ou conformité produit.

## Jalons exécutés du 21 octobre 2026

- Le [transport ASGI](../../../../src/pixs/backend/host_asgi.py) utilise un vrai handler Django, le protocole lifespan et une garde de phase. Ses [huit cas enfant](../../../../tests/integration/test_backend_host_asgi_closed.py) réussissent dans un processus Django isolé.
- Le [raccord serveur Auth/Core/audit](../../../../src/pixs/backend/host_composition.py) utilise les producteurs publics, avec un store et des faits propres à chaque invocation. Ses [cinq contrôles PostgreSQL](../../../../tests/integration/test_backend_host_composition_postgres.py) réussissent sur PostgreSQL 16.14 et Django 6.1.2 : connexion et retrait confirmés avec audit, jeton refusé après retrait, nettoyage du schéma et connexions fermées.
- Les 24 cas de préparation du banc propriétaire C03 sont réutilisés séparément. Les plans et clés C08 ainsi que la classification C10 demeurent des fixtures explicitement bornées dans ces recettes.

Le contexte de ressources, le plan et le lifecycle générique sont exercés par les recettes ci-dessous. Les adapters Agent/PZT et les attestations des tests unitaires restent synthétiques. Le drain des requêtes en cours reste non qualifié ; la qualification du P0 installé relève de C14/C17/C19.

## Complément de preuves et limites du 21 octobre 2026

- `host_lifespan.py` et sa recette PostgreSQL : 7 contrôles réussis ; acquisition, annulation et libération dans le thread sensible, préservation des connexions appelantes et refus de table absente. La cible Core `0003_core_idempotence` couvre une recette structurelle ; elle ne livre pas les comportements C06. Le raccord Auth/Core/audit a aussi été requalifié par ses 5 contrôles sur la cible `0002_core_audit` (appel natif `call_01a15f78052b7256b636d4d633ed6687`, exit 0).
- `host_plan.py` : 15 tests réussis (`call_01a15f8805b274dfb9596f717719a21d`, exit 0), plan déterministe et snapshots de configuration, références typées, refus des preuves/ports/manifests absents ou incompatibles. Le port d’attestation est à fournir par un appelant serveur de confiance.
- `host_runtime.py` : 20 tests réussis (`call_01a15f9b8a4870b79548ebc55b8d7840`, exit 0), acquisition ordonnée, fermeture inverse, hooks communs, relecture des observations et erreurs/annulations propagées. Les adapters des recettes sont des doubles explicites.
- `host_entry.py` : 17 gardes et 8 contrôles HTTP réussis en enfants isolés (`call_01a15faf1eca716a8d8517cf9f3200cf`, exit 0). Les gardes utilisent un double du résolveur pour les refus avant effet ; la frontière HTTP utilise une configuration Django de recette sans base ouverte. Aucune entrée C01 positive n’est déduite de ces tests.
- Les premiers essais natifs ont échoué : SGID hérité, chiffrement `null` sans authentification en mode utilisateur, puis journal de recette non initialisé. Ces essais et leurs reçus sont conservés, sans être comptés comme succès.

La recette native C01 a ensuite réussi après autorisation distincte de sudo sur cet hôte. Le contrôleur UID 0 a créé et arrêté la seule unité temporaire `pixs-c07-c4-entry-0593a443.service` (RuntimeMaxSec 45 s), avec consommateur UID 1000 et fixtures publiques. Les 17 contrôles sont vrais : entrée C01 réelle, journal C01 initialisé et audit confirmé, vrai Django/ASGI, frontières HTTP, contexte actif puis arrêt lifespan et attestation native de quiescence. Le mode `null` qualifie le fonctionnement uniquement ; aucune connexion PostgreSQL ni qualification P0 n’est déduite de cette recette. Les reçus sont attestés par CGPT dans [VALIDATION.md](VALIDATION.md), séparément des preuves natives OpenCode.

Le complément canonique du 21 octobre est retracé dans `requirements.md`. Aucun binaire Nuitka standalone, budget CPU/mémoire/concurrence ou mode Standalone/ZT du produit n’a été qualifié par ces recettes. [VALIDATION.md](VALIDATION.md) borne l’éligibilité locale ; l’archive, le rapport statistique et le gate restent des étapes distinctes à prouver.
