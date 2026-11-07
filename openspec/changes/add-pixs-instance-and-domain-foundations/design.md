# Conception — C97

## Statut et décisions

Le périmètre est celui du plan validé ACL-PIXS-2026-10-31-E3-R1. Les exigences et décisions sources restent opposables ; cette conception prépare leur réalisation et ne sélectionne pas de mécanisme absent des sources.

## Résultat et propriétaires

Identité logique d’Instance, Domaines/FQDN, trois modes, bases et contrôleurs séparés et transition après ZT entièrement initialisé.

Les fondations pré-domaine ne dépendent pas d’un Domaine déjà activé. Les rôles ZT, LDAP et Kerberos restent réalisés dans leurs changes propriétaires.

Les règles métier et autorisations applicatives restent dans leurs modules PBO, avec Core/Auth/Agent/PZT par contrats publics. Les exécutants PA/PZT appliquent leurs mandats et rapportent les états réels. Réception, effet technique, confirmation applicative et disponibilité restent distincts.

## Données et contrats

Les données ont un propriétaire canonique Instance, Domaine, Tenant ou rôle technique explicitement déclaré. Les données Core gardent PG souveraine. L'état Kerberos durable normal réside dans LDAP ; la reconstruction complète depuis PG est une procédure d'urgence critique, avec restauration protégée ou recréation/reprovisionnement selon profil et sauvegardes. Les états RAM des rôles déclarés ne deviennent pas une source de droits.

Les références d'acteur, de rôle, de processus, d'opération et de preuve restent distinctes. Les formats, droits, versions, limites et stratégies de concurrence/migration sont à préciser par unité avant son implémentation. Une compatibilité v1 n'est pas déduite du nouveau modèle.

## Dépendances par phase

- [C08](../add-installation-and-first-configuration/proposal.md).
- [C96](../add-domain-scoped-identities-and-controlled-transfers/proposal.md).
- [Z03](../add-pzt-authoritative-control-and-signed-receipts/proposal.md).
- [Z05](../add-pzt-managed-dns-service-and-pa-adapters/proposal.md).
- [Z07](../add-pzt-path-discovery-and-encrypted-relays/proposal.md).
- [Z12](../add-pzt-ca-hierarchy-rotation-and-recovery/proposal.md).
- [O38](../add-auth-managed-kerberos-kdc/proposal.md).
- [O39](../add-auth-managed-openldap/proposal.md).

Les fondations d'Instance et contrats publics précèdent la transition Domaine. Le ZT doit être entièrement initialisé et vérifié avant la création du premier Domaine ; cette garde ne bloque pas l'amorçage pré-domaine de l'Instance. La PKI technique pré-PG est distincte de la PKI normale ; bascule vérifiée puis retrait irréversible de l'amorçage. Les capacités optionnelles ne sont pas activées par leur présence.

C97-SL01 fournit les fondations requises par C96 et Z30. C96 expose les nouveaux liens et contextes ; Z30-SL01 expose le modèle d'acteurs que le CZT pourra persister. Z03 fournit ensuite le registre opérationnel consommé par les phases de gouvernance suivantes. C97-SL04 vérifie les rôles ZT avant la création du premier Domaine, puis coordonne les propriétaires du transfert et des services de Domaine ; leur disponibilité effective conditionne l'activation. Les services d'un Domaine déjà créé ne sont pas un prérequis de son amorçage pré-domaine. Il ne s'agit pas de dépendances globales réciproques entre tous les travaux d'un dossier.

N08 définit les profils génériques ; les rôles les implémentent selon leurs garanties. Pour Z29, Z05 n'est requis que par le profil DNS-01 et Z32 par les parcours HTTP-01/TLS-ALPN-01 qui le sélectionnent ; Z32 peut utiliser les certificats privés Z12 sans dépendre du cycle ACME public. O37 reste une qualification de l'assemblage Windows/MIT/OpenLDAP, sans fournisseur AD choisi implicitement. Ces distinctions évitent de déclarer des prérequis livrés ou un cycle global artificiel.

## Barrières de C97 et preuves par unité

| Unité | Résultat propre et barrière |
|---|---|
| C97-SL01 | Identité et données pré-domaine, contrats publics consommables par C96/Z30 ; aucun Domaine actif requis. La clause PG après transfert n'est pas un critère de réussite de cette fondation. |
| C97-SL02 | Plans FQDN/rattachement et leurs refus ; aucune création de Domaine par simple préparation. La garde de ZT complet doit être vérifiée au point de création. |
| C97-SL03 | Contrats de séparation des bases/contrôleurs, préparation et refus de disponibilité ; aucune déclaration de services réels sur la seule base d'un schéma ou d'une simulation. |
| C97-SL04 | Preuve du ZT entièrement initialisé avant création du premier Domaine, puis coordination des propriétaires C96/O38/O39 et des autres capacités effectivement requises. Maintenance des écritures, transfert et relations préservés, services et authentification cibles vérifiés avant activation ; les anciennes identités d'Instance sont alors caduques. Réconciliation avant reprise en cas d'issue inconnue. |
| C97-SL05 | Consolidation de continuité et conformité ; les vérifications indispensables restent exécutées dans leur unité d'origine avant validation. |

La préparation d'un plan, de schémas ou de contrats n'est pas la création du Domaine. La garde de création et la disponibilité nécessaire à l'activation restent deux vérifications explicites de C97-SL04. Le scénario **Activation du premier Domaine** de `pixs-instance` est rattaché à cette unité ; il n'est exigé comme réalisation ni en SL01 ni en SL03. Les critères détaillés et les tâches ouvertes sont dans [tasks.md](tasks.md).

## Sécurité et refus

Un ZT incomplet bloque le premier Domaine ; le partage ZT respecte les labels DNS ; les bases restent séparées et aucun retour Domaine vers Standalone n’est introduit.

Refus par défaut, interdictions et exceptions canoniques dans leur seul périmètre, mandat courant, fraîcheur, validité et retraits restent vérifiés. Un hôte ou certificat ne fournit pas de droit implicite. Les données sensibles et secrets ne figurent ni dans les diagnostics ni dans les artefacts.

## Échecs, concurrence et reprise

Les opérations sensibles préparent un plan courant et autorisé, vérifient les préconditions et produisent un état inspectable. Une réponse perdue, un effet inconnu, un conflit de propriétaire ou une application partielle exige réconciliation avant répétition. Les confirmations PG synchrones requises ne sont pas abaissées automatiquement. Aucun démantèlement ni retour arrière destructeur ne se déduit de la préparation.

## Interface et exploitation

Les contributions PBO utilisent les contrats publics, les trois contextes et les droits applicables, avec messages traduisibles, thèmes et accessibilité selon les exigences transverses. Une CLI n'ouvre aucun canal PBO–PA hors PZT. Logs, métriques, audit et états de santé restent distingués et minimisés.

## Vérifications futures et barrières

Les scénarios et clauses exacts sont dans requirements.md. À chaque unité : vérifier contrats, types, périmètres, droits, nominal/refus, concurrence et reprise nécessaires au comportement livré. Les recettes réelles de services, matériel, stockage, réseau, navigateur ou packaging exigent leur environnement autorisé ; elles ne sont pas exécutées ici. Un fournisseur absent ou non qualifié bloque l'usage dépendant, sans faux succès.

- [pixs-instance](../../specs/pixs-instance/spec.md).
- [pixs-domains](../../specs/pixs-domains/spec.md).

Les preuves archivées ne qualifient que leur version. Les données et historiques hors périmètre doivent être préservés ; la validation documentaire de ce dossier ne coche aucune tâche de réalisation.
