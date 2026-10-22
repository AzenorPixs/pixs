# Conception — C05

## Statut et périmètre

Réalisation propriétaire autorisée par `/prompts 1CISMP2`, reprise du même RUN `cismp2-pixs-968e38f3e27b4bbf`. Les décisions techniques ISMP concrétisent les exigences déjà validées, dont D13/D14 adoptées au canon le 20 octobre 2026. Aucun delta normatif supplémentaire, nouvelle dépendance ou variable d’environnement.

Les résultats exécutés, identifiants natifs, limites et empreintes sont consignés dans `VALIDATION.md`. Archivage, rapport `STATISTIQUES.md` et gate restent des étapes distinctes du RUN ; une réalisation source ne les prouve pas.

## Stockage propriétaire et formats distincts

`CoreAuditEvent` appartient à `pixs.core`, table `pixs_core_audit`, migration `0002_core_audit` après `0001_core_initial`. Seul le modèle est réexporté par `pixs.core.models`. Les contrats purs restent importables sans Django.

Le discriminant interne sépare le generic Kernel (13 champs exacts, identifiants sources opaques, résultat non limité à ALLOWED/DENIED) et le PDP (10 champs exacts, faits inconnus conservés à None). Aucun format n’est converti implicitement dans l’autre ; les primitives `AuditEvent`, `AuditDecisionProjectionV1` et `invoke_audit_projection` restent inchangées.

Le UUIDv7 du stockage est distinct de l’identité source. Les métadonnées associent contexte tenant/scope, opération, alias, token, xid PostgreSQL réel, origine/version/rétention de la politique et classification. Les importations C01 ajoutent journal, séquence et empreinte source. Unicités et CHECKs empêchent les mélanges de formats, sources C01 partielles et triplets de maintenance partiels.

## Politique explicite et minimisation

`AuditPolicy` est immuable et exige tous ses paramètres : `policy_id`, `policy_version` chaîne, `origin`, `retention_days`, `max_event_bytes`, `max_query_records`, `redactions`, `governance_ref`, `ConfidentialityLevel` et `PersonalDataLevel` exacts. Les bornes sont des entiers positifs exacts. `ExplicitAuditPolicySource(approved_context, policy)` fournit une politique liée au contexte ; une source de composition peut implémenter le même port `resolve(context, alias)`. Absence ou incohérence échoue fermé ; aucun placeholder ou choix implicite de provider.

Les règles qualifiées permettent seulement `generic.actor_reference`, `generic.resource_id`, `generic.reason_or_error`, `pdp.subject_id` et `pdp.resource_id`, selon leurs possibilités de nullité. Elles s’appliquent avant persistance ; identité source, contexte et corrélations restent inchangés. La classification et la préparation de références non sensibles restent la responsabilité du caller de confiance. Il n’existe ni payload avant/après libre, ni duplicateur de lignes métier, ni détection sémantique universelle de secrets.

Le JSON canonique UTF-8 est borné à 65 536 octets, en plus de la borne explicite de politique. Le codec de versions PDP conserve les tuples imbriqués et vides, avec limites techniques profondeur 8, 512 éléments et chaînes de 4 096 caractères. Ces limites internes ne créent aucun vocabulaire normatif nouveau.

## Transaction commune et réconciliation

`PostgresAuditParticipant(policy_source, clock, peer_alias)` implémente le port Core existant :
- `stage(event, *, alias, operation_id, transaction_token, context, decision)` exige PostgreSQL et une transaction propriétaire déjà ouverte. Aucun commit autonome ni bloc durable imbriqué.
- `verify_staged(TransactionProof)` contrôle les mêmes opération/token/contexte et le xid réel de cette transaction. Une ligne d’une transaction précédente ne suffit pas.
- `reconcile_unknown(proof)` inspecte depuis un alias physiquement indépendant vers la même base. Il retourne CONFIRMED pour des lignes committées cohérentes ou leur tombstone exact ; sinon UNKNOWN. Il ne prétend jamais prouver ABSENT par une simple non-visibilité et ne rejoue aucun effet.

Un DENY observé peut conserver des faits inconnus et une décision absente. Un ALLOW nécessite une décision courante cohérente ; les refus métier suivant une décision ALLOW restent traçables comme DENY. Les doublons génériques identiques restituent leur identité ; une collision divergente est refusée sous verrou.

`PostgresAuditSink(participant, alias, context, operation_id).record(event)` sert le contrat PDP d’acquittement booléen. Dans un bloc existant il participe sans le committer ; sinon il possède son bloc durable. True ne constitue pas un reçu de conformité ou la preuve du commit d’une mutation appartenant à un autre module.

`stage_observation(event, *, source, alias, operation_id, transaction_token, context)` reçoit un fait generic déjà committé chez son propriétaire. Le port de confiance `source.verify_committed_observation(event=..., alias=..., operation_id=..., transaction_token=..., context=...) -> None` doit vérifier sous verrous la provenance exacte et l’autorité courante du workload de réconciliation, indépendamment de la session retirée ou d’un ancien ALLOW. L’événement source est déjà minimisé, garde son occurred_at et son event_id stable ; une transformation par la politique est refusée. La source est revérifiée avant sortie. Le résultat reste un StagedRef de la transaction courante.

`confirm_observation(event, *, alias, context)` constate depuis le peer la même identité, le même hash canonique et le même contexte, y compris un tombstone exact, sans insertion : CONFIRMED ou UNKNOWN. Une observation déjà enregistrée dans une autre transaction est refusée par stage_observation avec AUDIT_OBSERVATION_ALREADY_RECORDED ; aucun ancien stage n’est maquillé en preuve courante. Le propriétaire Auth peut alors confirmer indépendamment l’observation, revalider son autorité et solder sa référence dans une frontière propriétaire sûre. L’absence non prouvée reste UNKNOWN.

D13 utilise ces interfaces dans la transaction Auth propriétaire. D14 impose au propriétaire Auth un rollback de la transaction en erreur puis une nouvelle transaction avec contrôles courants, retrait et références de réconciliation durables ; C05 ne fabrique aucun audit manquant. Les tests `SyntheticAuthOwner` n’implémentent ni ne qualifient le runtime C03.

## Append-only, anonymisation et purge

Manager/QuerySet refusent les mises à jour, suppressions et bulk updates ordinaires, y compris les options de conflits réécrivant une ligne. Le trigger PostgreSQL refuse UPDATE/DELETE ordinaires. Le retour de migration refuse un audit non vide avant toute suppression du modèle.

`maintain_audit` exige une Request, les ports Core propriétaires, un Job identifié, une politique courante et un `AuditLifecyclePort.authorize_maintenance` fourni par Jobs/C10/C16. Le port doit vérifier mandat, holds, références et projections actuels ; un booléen client n’est pas un substitut.

La procédure revalide sous verrous l’autorité, la classification, les waivers C4, la politique et le cycle de vie. Elle persiste son propre audit avant modification, borne la cible par CAS et n’autorise que les champs explicitement minimisables. Empreinte et références d’origine restent conservées ; empreinte courante et version de maintenance distinguent l’anonymisation d’un événement nouveau. La purge ordinaire respecte durée et legal hold, produit un tombstone corrélé et refuse la résurrection. Les reprises d’une même maintenance sont idempotentes.

La dérogation Super Admin vient du decider C4 de confiance, dans son périmètre vérifié ; aucun audit absent n’est annoncé réalisé. La garde SQL ne constitue pas une protection contre un DBA ou un rôle hostile capable de manipuler les paramètres de session : l’intégrité cryptographique avancée C16 reste distincte.

## Lecture et composition C4

`filter_audit` exige décision courante, plan source AUDIT cohérent et non périmé, droits/classification C10 et audit requis. Le SQL applique le contexte et les seules références autorisées avant exposition. Le résultat est immuable, sans instance ORM. La borne respecte FilterConfig et la politique C05 ; plan, politique et dérogations sont revérifiés avant sortie du bloc.

Deux points internes évitent toute boucle entre C4 et `filter_audit` :
- `audit_candidate_references(*, kind, context, alias, limit)` ne retourne que des références `audit:<UUIDv7>`. AUDIT exact, PostgreSQL outerTX, contexte valide, ordre stable. limit est `max_filter_requests`, jamais le limit UI ; lecture limite+1 et refus explicite de surcharge, sans tronquage avant évaluation.
- `audit_resource_ownership(*, resource_id, context, alias)` dérive tenant/scope des seules métadonnées de la ligne. Une cible absente ou un contexte incohérent retourne None.

Ces points sont enregistrés explicitement par la composition propriétaire C4. Ils n’exposent aucun payload, ne donnent aucun droit et ne constituent pas une façade client. La recette teste les points C05 réels avec des owners C4/C10 synthétiques ; elle ne revendique pas leur intégration produit finale.

## Reprise C01 scellée

`SealedBootstrapSource` appelle uniquement le lecteur public C01 de journal scellé. `import_sealed_bootstrap` exige autorité courante sur le journal, lot complet et ordonné, identités et empreintes validées. L’insertion et son audit sont atomiques ; collisions et transformations incompatibles de source sont refusées. Un marqueur déterministe couvre aussi le lot vide.

`verify_committed_import` vérifie marqueur, séquences et empreintes depuis la connexion indépendante ; une réponse perdue après commit ne provoque pas de réexécution. Les références source exactes restent vérifiables après purge contrôlée via tombstone. C05 ne supprime jamais le journal C01 ; sa gestion ultérieure appartient au protocole propriétaire C01/C08.

## Livraison locale et limites de composition

Aucun endpoint, worker, nouvelle configuration runtime, Git, déploiement ni service partagé n’est créé par C05. Les tests temporaires utilisent des ressources possédées et nettoyées. Les preuves sont bornées au propriétaire d’audit et à son raccordement contractuel : elles ne livrent pas C03, C04, C06, C08, C09, C10, C13 ou C16 et ne prouvent pas une composition P0 installable. C17/C18/C19 gardent qualification, paquet et identité de distribution.
