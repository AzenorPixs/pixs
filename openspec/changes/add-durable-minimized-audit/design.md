# Conception — C05

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 a été adopté et archivé le 18 octobre 2026 ; ses précisions normatives sont intégrées au canon. Les arbitrages propres au présent change restent à lever avant réalisation.

## État actuel vérifié

Constat : AuditEvent, AuditDecisionProjectionV1 et invoke_audit_projection sont structurels ou bornés ; True du port n’est pas une preuve d’audit durable.

Sources consultées et empreintes recoupées avec la matrice :

- [src/pixs/kernel/audit_event.py](../../../src/pixs/kernel/audit_event.py).
- [src/pixs/core/authz/audit_projection_invocation.py](../../../src/pixs/core/authz/audit_projection_invocation.py).
- [src/pixs/core/authz/audit_decision_projection.py](../../../src/pixs/core/authz/audit_decision_projection.py).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Fournir un sink persistant propriétaire et append-only. Corréler acteur/contexte/action/résultat avec minimisation et rétention distincte des logs. Lier effets et preuves selon frontière transactionnelle déclarée, et diagnostiquer sans fuite les échecs ; respecter la dérogation du Super Admin sans fabriquer un audit absent.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Schéma et transaction d’audit des effets/refus, autorisation d’accès et réécriture contrôlée ; règles de rétention avec C10/C16. Aucun mécanisme d’intégrité avancée optionnel imposé ici.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [define-first-installable-pbo-profile](../archive/2026-10-18-define-first-installable-pbo-profile/proposal.md).
- [add-core-postgres-services](../add-core-postgres-services/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Commit et panne avant/après écriture testés ; consultation autorisée et isolation ; interdiction de réécriture ordinaire ; acquittement mémoire distinct de la preuve persistante ; rétention/minimisation exercées.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

### T05 — SecretProvider et opérateur avant première session

L’opérateur initial, le workload et la conversion des saisies en références ne doivent dépendre ni d’une session inexistante ni d’une base déjà initialisée. Compléter le contrat d’amorçage C01/C08 ; pas de nouveau provider imposé.

Contrôles à intégrer : Provider en lecture seule : procédure explicite de fourniture de référence ; Panne entre saisie et référence confirmée sans fuite ; Opérateur non vérifiable refusé avant mise en service.

### T08 — Audit exhaustif du panneau et navigation SPA

L’audit de chaque activité du panneau inclut navigation/lecture ; des logs ou un acquittement mémoire n’en prouvent pas la persistance. Compléter protocole C05/C13 et critères de volumétrie/minimisation C15 ; préserver exception Super Admin.

Contrôles à intégrer : Panne sink avant affichage/action ordinaire refusée selon contrat ; Dérogation root sans audit annoncé à tort ; Navigation SPA reliée à une preuve serveur et aucune donnée sensible copiée.

### T10 — Mutation, audit, idempotence et outbox

Les composants prévoient chacun leur partie ; la frontière transactionnelle et l’échec avant/après commit doivent être explicitement communs. Compléter contrats C05/C06/C09 avec refus distincts et résultat réconcilié ; pas de nouveau broker.

Contrôles à intégrer : Rollback sans événement publié ; Commit puis réponse perdue restituant résultat idempotent ; Double livraison sans double effet propriétaire ; Refus auditable sans mutation métier.

Voir [audit transversal durable](../archive/2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.
