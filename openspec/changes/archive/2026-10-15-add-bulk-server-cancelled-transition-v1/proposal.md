# Proposition — add-bulk-server-cancelled-transition-v1

## Pourquoi

La demande d'annulation serveur autorisée pose déjà le flag persistant et sa révision. La primitive PostgreSQL `BulkRuntimeRepository.apply_transition` sait passer à `CANCELLED` sous flag, verrouillage, CAS et refus des terminaux. Il manque la composition serveur de cette transition avec une autorité `CANCEL` courante, dans les règles B03/B06 validées.

## Changement minimal

Ajouter uniquement une façade interne `transition_bulk_to_cancelled` et deux fichiers de tests nouveaux. La façade contrôle les types exacts, la capacité PostgreSQL réelle et l'autorité courante avant toute requête Bulk, puis appelle une seule fois la primitive existante avec `to_status="CANCELLED"` et un instant UTC capturé côté serveur. Seuls l'état de l'opération et sa révision évoluent ; flag, progression, checkpoint, échéance, Job, liaison, schedule et effets déjà engagés restent conservés.

La qualification démontre la coopérativité des verrous existants et le refus de nouvelles unités après pose du flag. Elle ne prétend ni révoquer une unité déjà engagée, ni terminer un Job ou fournir un worker.

## Sources et dépendances

- Canon `bulk-operations` B03, B06, B14, matrice partagée et profils d'exécution validés.
- Runtime PostgreSQL, ports serveur composés et façade `request_bulk_cancellation` existants ; cette dernière a été livrée par `add-bulk-server-cancellation-request-v1`.
- Contraintes `authorization` et `initial-administration` existantes ; aucune exception n'est transférée ou inventée.

## Validation

Import inerte, hostiles avant I/O, refus d'autorité avant SQL, vraie primitive sous PostgreSQL isolé, flag absent, terminaux, CAS/race, rollback, conservation des engagements et champs, fermeture des connexions et nettoyage. Syntaxe des trois fichiers, régressions applicables, strict ciblé, contrôle combiné sous exclusion et résultat global exact avant archive unique ; rapport distinct après publication selon CAB 1.1.

## Exclusions

Aucun code existant, worker, route HTTP, stockage, projection, mutation propriétaire, provider de production, migration, dépendance, configuration, Git ou infrastructure à modifier. Aucune nouvelle priorité entre expiration et annulation, aucun bail ajouté, acteur initial imposé ou retry/rebase automatique. Aucune valeur secrète dans les agents, diagnostics ou preuves.
