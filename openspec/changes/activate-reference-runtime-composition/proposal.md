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

- [C01 — provider de secrets runtime](../archive/2026-10-19-add-pbo-runtime-secret-provider/proposal.md), archivé.
- [C02 — services Core PostgreSQL](../archive/2026-10-20-add-core-postgres-services/proposal.md), archivé.
- [C03 — authentification locale et sessions](../archive/2026-10-21-add-initial-authentication-and-sessions/proposal.md), producteur des contrats publics Auth.
- [C05 — audit durable minimisé](../archive/2026-10-21-add-durable-minimized-audit/proposal.md), producteur du sink d’audit.

Le canon adopté le 20 octobre 2026 impose `pixs.auth` essentiel et sa capacité locale PostgreSQL, avec dépendance vers les seuls contrats publics Core. C07 consomme les interfaces C03 et C05 ; il ne réalise pas leurs services à leur place. Les preuves de ces dépendances sont requises avant l’intégration correspondante.

## Impact

Périmètre de réalisation : Fournir l’hôte runtime et les adapters du lifecycle commun, sans remplacer les mécanismes purs. Lier composants/providers/configuration/migrations et preuves authentifiées. L’hôte intermédiaire peut être exercé isolément mais refuse readiness P0 si PZT/DNS ou toute autre obligation manque ; C14 et C17 ferment l’intégration.

La reprise documentaire validée le 20 octobre 2026 a actualisé proposal.md, design.md et requirements.md sur le canon adopté. La réalisation C07 se poursuit avec les jalons exécutés ci-dessous. Les tâches restent conditionnées à la preuve de leur critère complet ; le contexte de composition, les adaptateurs et l’entrée applicative restent à achever.

## Critères de sortie de réalisation future

Ordre de composition déterministe, entrée runtime réelle en environnement isolé ; composant essentiel absent, fournisseur ambigu ou preuve manquante → P0 hors service. L’hôte intermédiaire ne certifie pas le produit ; intégration complète de PZT en C14 et recette installable en C17.

## Barrière de conception

Entrée de lancement, registre des adapters et limites d’exposition à arrêter sans nouveau runtime ; ne pas transformer globally_compatible=False en certificat global.

## Jalons exécutés du 21 octobre 2026

- Le [transport ASGI](../../../src/pixs/backend/host_asgi.py) utilise un vrai handler Django, le protocole lifespan et une garde de phase. Ses [huit cas enfant](../../../tests/integration/test_backend_host_asgi_closed.py) réussissent dans un processus Django isolé.
- Le [raccord serveur Auth/Core/audit](../../../src/pixs/backend/host_composition.py) utilise les producteurs publics, avec un store et des faits propres à chaque invocation. Ses [cinq contrôles PostgreSQL](../../../tests/integration/test_backend_host_composition_postgres.py) réussissent sur PostgreSQL 16.14 et Django 6.1.2 : connexion et retrait confirmés avec audit, jeton refusé après retrait, nettoyage du schéma et connexions fermées.
- Les 24 cas de préparation du banc propriétaire C03 sont réutilisés séparément. Les plans et clés C08 ainsi que la classification C10 demeurent des fixtures explicitement bornées dans ces recettes.

Le contexte de ressources, les registres/configuration/lifecycle, les observations de disponibilité et l’entrée applicative protégée restent à intégrer avant clôture de C07. La qualification du P0 installé reste portée par les obligations C14/C17/C19.
