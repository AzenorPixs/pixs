# Conception — Z30

## Statut et décisions

Le périmètre est celui du plan validé ACL-PIXS-2026-10-31-E3-R1. Les exigences et décisions sources restent opposables ; cette conception prépare leur réalisation et ne sélectionne pas de mécanisme absent des sources.

## Résultat et propriétaires

Acteurs ZT, participations, gouvernance, délégations, approbations et représentation sous les droits propres aux Domaines.

Z03 conserve le stockage et service CZT ; Z25 l’enrôlement technique ; Z02 l’application réseau. Les modèles publics d’acteurs doivent précéder leur intégration CZT, sans exiger la gouvernance complète pour les seuls contrats initiaux.

Les règles métier et autorisations applicatives restent dans leurs modules PBO, avec Core/Auth/Agent/PZT par contrats publics. Les exécutants PA/PZT appliquent leurs mandats et rapportent les états réels. Réception, effet technique, confirmation applicative et disponibilité restent distincts.

## Données et contrats

Les données ont un propriétaire canonique Instance, Domaine, Tenant ou rôle technique explicitement déclaré. Les données Core gardent PG souveraine. L'état Kerberos durable normal réside dans LDAP ; la reconstruction complète depuis PG est une procédure d'urgence critique, avec restauration protégée ou recréation/reprovisionnement selon profil et sauvegardes. Les états RAM des rôles déclarés ne deviennent pas une source de droits.

Les références d'acteur, de rôle, de processus, d'opération et de preuve restent distinctes. Les formats, droits, versions, limites et stratégies de concurrence/migration sont à préciser par unité avant son implémentation. Une compatibilité v1 n'est pas déduite du nouveau modèle.

## Dépendances par phase

- [C97](../add-pixs-instance-and-domain-foundations/proposal.md).
- [Z03](../add-pzt-authoritative-control-and-signed-receipts/proposal.md).
- [Z02](../add-pzt-network-mandates-and-fail-closed-revocation/proposal.md).
- [Z25](../add-pzt-pa-admission-and-ephemeral-peer-generation/proposal.md).

Les fondations d'Instance et contrats publics précèdent la transition Domaine. Le ZT doit être entièrement initialisé et vérifié avant la création du premier Domaine ; cette garde ne bloque pas l'amorçage pré-domaine de l'Instance. La PKI technique pré-PG est distincte de la PKI normale ; bascule vérifiée puis retrait irréversible de l'amorçage. Les capacités optionnelles ne sont pas activées par leur présence.

C97-SL01 fournit les fondations requises par C96 et Z30. C96 expose les nouveaux liens et contextes ; Z30-SL01 expose le modèle d'acteurs que le CZT pourra persister. Z03 fournit ensuite le registre opérationnel consommé par les phases de gouvernance suivantes. C97-SL04 attend les rôles ZT et les services Domaine effectivement requis. Il ne s'agit pas de dépendances globales réciproques entre tous les travaux d'un dossier.

N08 définit les profils génériques ; les rôles les implémentent selon leurs garanties. Pour Z29, Z05 n'est requis que par le profil DNS-01 et Z32 par les parcours HTTP-01/TLS-ALPN-01 qui le sélectionnent ; Z32 peut utiliser les certificats privés Z12 sans dépendre du cycle ACME public. O37 reste une qualification de l'assemblage Windows/MIT/OpenLDAP, sans fournisseur AD choisi implicitement. Ces distinctions évitent de déclarer des prérequis livrés ou un cycle global artificiel.

## Sécurité et refus

Approche directionnelle, portée et profondeur bornées ; appartenance non humaine unique ; participations humaines indépendantes ; aucun droit issu de la seule reconnaissance ou d’un mandat expiré.

Refus par défaut, interdictions et exceptions canoniques dans leur seul périmètre, mandat courant, fraîcheur, validité et retraits restent vérifiés. Un hôte ou certificat ne fournit pas de droit implicite. Les données sensibles et secrets ne figurent ni dans les diagnostics ni dans les artefacts.

## Échecs, concurrence et reprise

Les opérations sensibles préparent un plan courant et autorisé, vérifient les préconditions et produisent un état inspectable. Une réponse perdue, un effet inconnu, un conflit de propriétaire ou une application partielle exige réconciliation avant répétition. Les confirmations PG synchrones requises ne sont pas abaissées automatiquement. Aucun démantèlement ni retour arrière destructeur ne se déduit de la préparation.

## Interface et exploitation

Les contributions PBO utilisent les contrats publics, les trois contextes et les droits applicables, avec messages traduisibles, thèmes et accessibilité selon les exigences transverses. Une CLI n'ouvre aucun canal PBO–PA hors PZT. Logs, métriques, audit et états de santé restent distingués et minimisés.

## Vérifications futures et barrières

Les scénarios et clauses exacts sont dans requirements.md. À chaque unité : vérifier contrats, types, périmètres, droits, nominal/refus, concurrence et reprise nécessaires au comportement livré. Les recettes réelles de services, matériel, stockage, réseau, navigateur ou packaging exigent leur environnement autorisé ; elles ne sont pas exécutées ici. Un fournisseur absent ou non qualifié bloque l'usage dépendant, sans faux succès.

- [zt-instances](../../specs/zt-instances/spec.md).
- [pixs-domains](../../specs/pixs-domains/spec.md).

Les preuves archivées ne qualifient que leur version. Les données et historiques hors périmètre doivent être préservés ; la validation documentaire de ce dossier ne coche aucune tâche de réalisation.
