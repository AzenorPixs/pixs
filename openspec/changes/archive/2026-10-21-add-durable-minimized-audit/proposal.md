# C05 — Audit durable

## Pourquoi

Les structures AuditEvent, AuditDecisionProjectionV1 et invoke_audit_projection ne prouvent pas une persistance. C05 fournit le propriétaire d’audit PostgreSQL et ses interfaces de participation, consultation et maintenance contrôlée.

## Réalisation

Stockage séparant generic Kernel et PDP, append-only ORM/SQL ordinaire, politique explicite et minimisation avant écriture. Participation au bloc transactionnel propriétaire, preuve de stage liée au xid réel et réconciliation indépendante sans rejouer les effets.

Les services de lecture appliquent autorité, plan source, contexte, gouvernance et audit requis avant exposition. Les sources de références minimales permettent une composition C4 explicite sans lire une table privée ni créer de boucle. Anonymisation/purge exigent mandat Job, contrôles courants et audit propre ; les tombstones empêchent la résurrection.

Le transfert du journal C01 scellé conserve ordre, identités et empreintes et vérifie le commit indépendamment. C05 ne supprime pas ce journal. Les dérogations Super Admin restent issues du propriétaire C4, sans audit fictif.

## Capacités

Aucune capacité normative nouvelle. Le delta `specs/audit/spec.md` déjà adopté au canon le 20 octobre 2026 est conservé avec `skip_specs` désactivé : transaction commune Auth/C05 et retrait d’accès Auth prioritaire si seul l’audit échoue, sans nouvel accès ni extension de privilège. D14 côté Auth reste propriété C03.

## Dépendances et composition

C00 fournit le profil validé et C02 les modèles/services PostgreSQL existants. C05 réutilise Django et psycopg déjà retenus. Aucun nouveau paquet ou paramètre d’environnement.

C03, C04, C06, C08, C09, C10, C13 et C16 gardent leurs implémentations et qualifications propres. Le caller compose les ports vérifiés et les politiques explicites. Une fixture synthétique ne vaut pas leur runtime livré ; C17/C18/C19 conservent la qualification de la composition P0.

## Autorisation, preuves et clôture

`/prompts 1CISMP2` puis la demande de reprise du même RUN autorisent la réalisation C05, son archivage, les statistiques puis l’arrêt ciblé. Toutes les écritures/tests source passent dans la même session native OpenCode par décisions CAB unitaires et permissions once corrélées ; les approbations consommées ne sont pas rejouées.

`VALIDATION.md` expose les commandes exécutées, résultats, empreintes et limites ; `design.md` les contrats exacts. Les cases de tâches portent uniquement des preuves acquises. Le RUN n’est terminal qu’après archivage réussi, rapport postarchive `STATISTIQUES.md` vérifié et gate. Aucun Git, déploiement, nouveau change ou arrêt de service partagé.
