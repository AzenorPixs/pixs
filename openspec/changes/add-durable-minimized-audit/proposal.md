# C05 — Audit durable

## Pourquoi

AuditEvent, AuditDecisionProjectionV1 et invoke_audit_projection sont structurels ou bornés ; True du port n’est pas une preuve d’audit durable.

## Modifications proposées

Fournir le stockage et le sink d’audit durables, append-only, corrélés, minimisés, rétention et accès. Intégrer l’audit des opérations ordinaires ; respecter les dérogations Super Admin sans inventer un audit absent.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions de profil proposées dans C00.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `define-first-installable-pbo-profile`.
- `add-core-postgres-services`.

## Impact

Périmètre de réalisation futur : Fournir un sink persistant propriétaire et append-only. Corréler acteur/contexte/action/résultat avec minimisation et rétention distincte des logs. Lier effets et preuves selon frontière transactionnelle déclarée, et diagnostiquer sans fuite les échecs ; respecter la dérogation du Super Admin sans fabriquer un audit absent.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Commit et panne avant/après écriture testés ; consultation autorisée et isolation ; interdiction de réécriture ordinaire ; acquittement mémoire distinct de la preuve persistante ; rétention/minimisation exercées.

## Barrière de conception

Schéma et transaction d’audit des effets/refus, autorisation d’accès et réécriture contrôlée ; règles de rétention avec C10/C16. Aucun mécanisme d’intégrité avancée optionnel imposé ici.
