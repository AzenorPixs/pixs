# Conception — transition serveur vers CANCELLED

## Contrat interne

`transition_bulk_to_cancelled(*, trusted_ports, runtime_repository, server_context, operation_id, expected_revision) -> tuple[int | None, list[Diagnostic]]` ne reçoit ni clock, ni callback, ni état cible depuis un payload. Son import reste sans Django/ORM, environnement, réseau ou processus.

`operation_id` est une `str` exacte non vide, UTF-8 strict sans NUL. La révision est un `int` exact, bool et sous-classes exclus, compatible avec N+1 en int64. Les gardes élémentaires précèdent les chargements ORM et tout comportement étranger.

La façade exige les vraies classes `_BulkTrustedPorts` et `BulkRuntimeRepository`, un alias déclaré exact et un vendor PostgreSQL exact. Elle ne substitue ni composant arbitraire, ni faux repository. Les dépendances indisponibles sont refusées statiquement.

## Autorité et effet unique

L'appel à `_BulkTrustedPorts.check_authority` est lié à la vraie classe : action `CANCEL`, opération cible exacte, `resource_reference=None`, contexte serveur opaque. Seul un snapshot effectif exact `ALLOW` sans diagnostic permet de poursuivre ; DENY, UNAVAILABLE, erreur ou résultat mal formé refusent sans SQL Bulk. Aucun acteur n'est comparé implicitement au demandeur initial. L'action porte sur l'état de contrôle de l'opération, sans lecture/transfert/mutation des données propriétaires ; aucun contrôle de gouvernance ou d'audit absent n'est annoncé réalisé.

Après cette autorité, capturer une horloge UTC serveur interne et appeler une seule fois `BulkRuntimeRepository.apply_transition` avec l'opération, la révision attendue, `CANCELLED` fixe et cet instant. Le flag True et le CAS sont contrôlés par la primitive réelle ; la façade ne les simule pas, ne recharge pas pour rebaser et ne retente pas.

Les refus attendus de CAS/transition/valeurs/capacité produisent des diagnostics statiques sans écho. Les erreurs inattendues ne sont pas masquées. Le résultat positif est la révision N+1 réellement retournée.

## Coopérativité et conservation

`protected_unit` et la transition verrouillent les mêmes lignes opération/extension. Les unités déjà engagées conservent leurs effets ; un flag posé ou une opération terminale interdit la nouvelle unité. La transition ne termine ni ne réinitialise un Job et ne change pas liaison, schedule, progression, checkpoint, échéance, flag ou autre donnée de l'extension. Les arcs et la gestion d'expiration restent ceux de la primitive ; aucune priorité nouvelle n'est ajoutée.

## Preuves

Créer seulement le module et les deux tests nommés dans les tâches. Les unitaires utilisent des gardes vérifiées contre I/O, environnement, réseau, processus, ORM précoce et SQL avant ALLOW. Les providers synthétiques déclarés ne prouvent aucune composition de production.

Le harnais PostgreSQL n'est actif qu'en mode réel explicite, charge les variables par son seul processus sécurisé et masque ses sorties. Schéma privé unique, migrations existantes, tables publiques stables, vrais repositories/transactions/SQL, connexions indépendantes pour la compétition, nettoyage garanti et connexion fermée même sur échec. Prouver la demande préalable réelle, le flag absent refusé, l'état terminal et la révision seuls modifiés, les unités/engagements conservés, DENY/UNAVAILABLE avant SQL, révision périmée, deux concurrents et un gagnant, rollback externe et refus des terminaux.

## Périmètre documentaire et clôture

Le delta reprend B06 et ses quatre scénarios actuels verbatim, avec seulement des scénarios de preuve de la transition déjà couverte. Aucun profil préparatoire ou autre requirement n'est modifié. Avant archive, vérifier les artefacts, les tests et la cohérence, cocher seulement les tâches prouvées et obtenir le strict ciblé ; conserver l'exit/les warnings exacts du global. Archiver une seule fois sous mandat distinct. Après publication, libérer l'exclusion puis rédiger uniquement `STATISTIQUES.md` en phase REPORT avant gate individuel et libération. Le parent CISMP poursuit ensuite.
