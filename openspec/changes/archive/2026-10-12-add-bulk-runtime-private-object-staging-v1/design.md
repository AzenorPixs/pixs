## Context

B04 et ObjectMetadataV1 sont normatifs dans object-storage ; les ports serveur sont déclarés dans bulk-operations. Les bibliothèques de contrats, composition, parsing et persistance précédentes restent inchangées. Un provider concrètement capable de versions immuables n'est pas livré par cette fondation.

## Goals / Non-Goals

Implémenter les gardes de métadonnées et l'intégrité mécanique d'un flux en mémoire avant l'assemblage du runtime. Un hash correct ne prouve ni autorisation/gouvernance, ni immuabilité du provider, ni validation métier ou mutation. Aucun objet de stockage n'est créé, lu ou effacé par I/O directe.

## Decisions

- ObjectMetadataV1 conserve exactement onze clés, toutes explicites. Références opaques str exactes non vides UTF-8 sans NUL, scope None explicite possible, size int exact >=0 bool exclu, sha256 hex minuscule64, media text/csv ou application/x-ndjson, is_private bool exact True, expires_at datetime exact timezone.utc sans callback tz étranger.
- Types de toutes clés, valeurs imbriquées, catalogues, politique et horloge avant comportement/comparaisons/hashing/I/O ; snapshots détenus figés seulement après validation, aucune mutation du caller.
- Les métadonnées attendues sont un ObjectMetadataV1 complet explicitement composé côté serveur. Les primitives comparent chaque donnée au contrat attendu ; elles ne dérivent pas tenant_reference/scope_reference depuis tenant_id ni depuis None et n'ajoutent aucun schéma de contexte ou bool d'autorisation.
- Un vérificateur feed(bytes exacts)/finish/close conserve seulement digest et compteurs, jamais le fichier. Les bornes proviennent de PolicyV1, l'échéance est celle du serveur et reste fixe, cancellation/now sont des paramètres serveur typés. Hash et taille ne sont vérifiés qu'après EOF explicite complet ; troncature, divergence, expiry ou annulation donnent un résultat incomplet statique sans écho.
- L'inspection statique des six méthodes ObjectStoragePort ne les invoque pas et ne prouve pas une garantie de version. La capacité du provider reste UNAVAILABLE tant qu'une déclaration serveur et sa qualification applicables ne sont pas réellement composées et prouvées. Aucun bool fourni par payload, copie locale ou fallback ne fabrique cette garantie.
- Les résultats intermédiaires Python sont privés et mécaniques, sans nouvelle donnée normative/wire format, sans Progress métier, permission transférée ou checkpoint engagé.
- Les erreurs sont statiques et minimisées ; aucune valeur, byte, contexte d'authentification ou exception originale n'entre dans diagnostic/journal.

## Validation

Compiler trois Python ; tests de formes/types/hostiles/timezone, stream complet/tronqué, SHA/taille/contexte/version divergents, limites, UTC/deadline/cancellation et bilan terminal sans double comptage ; intégration fraîche sous gardes positives fichiers/réseau/processus/environ/DB/Core concret. Les 292 régressions existantes de 36 modules sont regroupées en une commande <=2000 caractères ; aucun PG réel rejoué puisque ORM/migrations inchangés, preuves antérieures préservées par empreinte. Strict du change sans issue et global qualifié seulement par trois WARNING historiques exacts et aucune nouvelle issue. Périmètre/UTF-8/LF vérifiés avant archive unique --skip-specs et STATISTIQUES sous mandat distinct.

## Risks and Limits

Production indisponible sans provider et garantie de version effectivement qualifiés. La fondation vérifie uniquement les données et le flux explicitement remis par le code serveur ; elle ne valide pas l'authentification ou la gouvernance réelle et n'active aucune purge/rétention.
