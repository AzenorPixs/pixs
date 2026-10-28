# C10 — Gouvernance et cycle de vie effectifs

## Pourquoi

Profils de gouvernance, vocabulaires de rétention et tombstone-v1 sont déclaratifs ; ils ne prouvent ni purge ni propagation durable.

La réconciliation documentaire du 26 octobre 2026 constate également des sources de raccord initial C10 écrites dans le périmètre C08 : catalogue protégé, attestation et reçus transactionnels, ponts de classification Auth et gouvernance des modes. Leur présence ne démontre pas la livraison de C10 ni leur qualification intégrée. L'inventaire, les décisions déjà adoptées et les limites sont distingués dans [design.md](design.md#réconciliation-documentaire-du-26-octobre-2026).

## Modifications proposées

Publier les profils des données réellement livrées ; appliquer classification, demandes d’accès/export/rectification/effacement/restriction, rétention, holds, suppression logique et purge explicite avec tombstones durables. Pas de dépendance implicite au Bulk optionnel pour les demandes exigées.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions du profil C00 adoptées le 18 octobre 2026 et intégrées au canon.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `add-core-postgres-services`.
- `integrate-runtime-authorization-and-super-admin`.
- `add-durable-minimized-audit`.
- `add-reference-worker-scheduler-and-event-delivery`.

Les contrats archivés C03, C06 et C14 et les relations avec les changes actifs C08, C16 et N05 sont explicités dans la [matrice des contrats propriétaires](design.md#matrice-des-contrats-propriétaires). Cette cartographie décrit les raccordements nécessaires aux tâches existantes ; elle ne sélectionne aucune capacité optionnelle et ne crée pas de dépendance circulaire de réalisation entre C08 et C10.

## Impact

Périmètre de réalisation futur : Déclarer les profils des données Core/PZT/DNS et appliquer politiques dans leurs services propriétaires. Demandes d’accès/export/rectification/effacement/restriction et purge restent des Commands autorisées, auditées et idempotentes. Les dérivés présents et les sauvegardes C16 réappliquent tombstones et holds ; pas de dépendance implicite au service Bulk complet.

La validation du 26 octobre 2026 autorise uniquement la réconciliation des quatre documents de ce dossier et la matrice des contrats propriétaires, avec correction du lien C09 et des empreintes. Aucun code, test applicatif, migration, dépendance, configuration runtime, Git, déploiement, publication ou archive n'est modifié ou exécuté par cette réconciliation. Les sources partielles préexistantes sont inventoriées sans validation de tâche ni lancement d'une réalisation supplémentaire.

## Critères de sortie de réalisation future

Donnée non classifiée non exposée ; purge ordinaire prématurée refusée ; demande rejouée sans double effet ; dérivés réellement présents traités ; tombstone préservé à la restauration ; exception Super Admin conforme et distincte des structures.

## Barrière de conception

Rétentions, droits de demandes, contrats des dérivés et procédure de purge à revoir ; valeurs existantes du canon conservées et exception Super Admin distincte des profils purs.
