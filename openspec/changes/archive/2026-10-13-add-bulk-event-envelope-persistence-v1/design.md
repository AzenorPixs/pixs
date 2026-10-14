# Design — add-bulk-event-envelope-persistence-v1

## Fondation partielle
Persistance seule de l'enveloppe, sans lecture de séquence ni publication. Les annexes B11 et les schémas logiques EventEnvelopeV1 et JSONValueV1 restent la référence, sans nouveau format public.

## Données et codec
- Treize clés : event_id, kind, event_type, event_version, producer_reference, schema_reference, order_scope_reference, occurred_at, subject_reference, tenant_context_reference, correlation_id, causation_id, payload.
- event_id clé primaire textuelle explicite de sa table, sans clé étrangère.
- Colonne payload en TEXT portant le JSON du codec privé. Le codec reste interne à la persistance, sans valeur canonique exposée.
- NUL d'un payload texte échappé à l'écriture et restitué à l'identique en lecture. Scalaires JSON conservés à l'identique selon la capacité réelle du codec, sans coercition ni modification de limite globale Python.
- Limites max_depth, max_members et autorisation non-tenant fournies explicitement par le producteur serveur à la fabrique et aux lectures ; aucune valeur logique par défaut. L’instance fabriquée conserve privément le tuple immuable déjà validé pour ses validations ultérieures et ses exports. Les lectures d’une instance hydratée exigent les limites explicites ; ce contexte technique n’est ni persisté ni une clé logique ou une autorité nouvelle.

## Validation et copies
- Validation par la garde pure existante avant tout accès ORM ou entrée/sortie.
- Contrôle des types exacts avant comparaison, UTC avec tzinfo timezone.utc exact, garde non-tenant explicite.
- Capture vers snapshot frozen, copies owned en entrée et en sortie. Exports owned des treize valeurs logiques seulement ; aucune référence interne mutable partagée.
- Diagnostics statiques existants, sans reproduction de valeur.

## Modèle
- Fabrique from_values qui valide le dict explicite avant construction et rend une instance non sauvegardée, adding préservé.
- full_clean qui contrôle les treize attributs avant conversion ORM, même avec exclude, et convertit les échecs en ValidationError statique préservant la cause.
- save surchargé insert-only : instance fraîche adding=True avec event_id fourni, force_insert=True obligatoire ; UPDATE/update_fields, sauvegarde d’une instance hydratée et seconde sauvegarde refusés avant ORM. La fabrique fixe le contexte privé des limites validées ; save vérifie la forme et les valeurs actuelles avant I/O, sans confiance dans un dict externe. full_clean applicatif reste complet même avec exclude, sans requête de validation d’unicité. QuerySet.update/rawSQL et contournements ORM bas niveau ne sont pas couverts ; aucune immutabilité globale DB annoncée sans mécanisme dédié.
- Contraintes persistantes : non-vacuité des textes obligatoires, appartenance de kind, format SemVer applicatif, garde non-tenant applicative, unicité de la clé primaire.
- Refus technique de capacité entière avant entrée/sortie.
- Aucune mutation après création dans ce périmètre. save exige aussi un alias explicite et une transaction active sur cet alias, après validation avant I/O.

## Repository
- Insert et get seuls, sans update, replay ou upsert.
- Alias unique validé comme texte runtime non vide sans NUL, conservé par instance.
- Insert validé par la fabrique puis force_insert dans atomic(savepoint=False) rejoignant la transaction propriétaire active du même alias, sans commit autonome.
- Seul le duplicata SQL23505 portant la contrainte de clé primaire donne le refus stable. Tout autre intégrité se propage. Le rollback du propriétaire est demandé même lorsque le duplicata est capturé par l’appelant.
- Get avec clés validées avant requête, retour d'une copie owned ou None, sans assertion d’autorisation ni résolution des références.
- Frontière d'échec qui marque le rollback propriétaire et propage à l'identique, interruption comprise.

## Migration 0007
- Dépend de 0006_bulk_command_idempotency, une seule création de modèle, miroir exact des champs et contraintes du modèle validé.
- Réversible vers 0006 sans toucher aux tables existantes.

## Ports et préconditions
- Aucun appel aux ports de confiance, aucun callback, aucun provider.
- L'appelant fournit contexte, dates et bornes. Les garanties métier restent ses préconditions documentées.

## Capacité et non-objectifs
JSONValueV1 accepte les scalaires racine et NUL dans chaînes/clés payload. dumps/loads stdlib privés ; refus statique de capacité avant I/O pour ValueError/RecursionError constaté, aucun nouveau maximum normatif ni changement global int_max_str_digits. Schéma propriétaire, déclarations, minimisation et absence de secrets ne sont pas établis par le validateur structurel et restent préconditions appelant. Aucun Outbox/Inbox, publisher, séquence, autorité, provider concret, rétention active, HTTP, frontend, Git ou infrastructure.
