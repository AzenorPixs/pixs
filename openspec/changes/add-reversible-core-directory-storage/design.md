# Conception — stockage Core réversible

## Statut et constat

PROPOSITION_DOCUMENTAIRE du 19 octobre 2026. Le canon [Core](../../specs/core/spec.md) impose PostgreSQL comme source de vérité ; [directory-projections](../../specs/directory-projections/spec.md) interdit à son rôle de projection de stocker ACL ou de devenir autoritatif. Les changes O08 et de lecture fraîche préparent une projection, pas une migration de stockage. Le présent dossier ajoute ce choix explicitement, avec deltas proposés non synchronisés. Aucun code, donnée ou service n'est modifié.

## Portée retenue

À l'installation, utilisateurs, groupes et ACL sont stockés dans PostgreSQL. Après installation, une opération administrée peut déplacer leur stockage de référence vers l'OpenLDAP interne de `pixs.auth.directory.openldap`. L'opération inverse est obligatoire et porte sur les données LDAP courantes, y compris les modifications réalisées depuis l'aller.

Le périmètre inclut la fermeture des relations nécessaires aux invariants : DigitalIdentity et liens si requis, appartenances, rôles, permissions, références tenant/scope, versions, tombstones et révocations applicables. Il ne s'agit pas d'une sélection indépendante d'objets qui permettrait de casser leurs liens. L'unité de migration exacte est décidée dans le plan, avec refus d'une coupure incohérente. Un DN n'est jamais un nouvel UUID canonique.

Les sessions, justificatifs et politiques propres Auth, l'audit, les Jobs, l'outbox et la coordination conservent leur stockage déclaré, PostgreSQL par défaut. Aucun mot de passe ou secret n'est déplacé par cette demande. Le besoin d'un domaine de support PostgreSQL subsiste ; ce choix ne promet pas de supprimer PostgreSQL de Pixs. Le déplacement vers AD ou un LDAP tiers n'est pas autorisé par cette option.

## Propriété et contrats

Core demeure le propriétaire logique des données, schémas, validations et Commands publiques. Auth gère le service OpenLDAP, ses accès techniques et son lifecycle. Le provider de stockage implémente un contrat Core versionné, résolu par le graphe commun ; aucune dépendance privée Core vers Auth ni cycle Core/Auth n'est introduit. Les contrats et leur liaison doivent être détaillés avant code si l'ordre de composition ne permet pas cette injection.

Les ACL Pixs sont des données de politique stockées sous schéma versionné ; le moteur Pixs les évalue avec ses règles existantes. Les ACL techniques LDAP protègent l'accès au stockage, elles ne remplacent pas les règles Pixs. Les écritures métier restent des Commands Django ; un accès LDAP direct ne devient pas une API de mutation alternative.

Le modèle LDAP doit préserver les politiques complètes (DENY/ALLOW, selectors, conditions, obligations, périodes), scopes et relations. Une représentation opaque n'est admise que si elle reste typée, versionnée, contrôlable, migrable et compatible avec les garanties de lecture et de filtrage. Le choix de schéma et d'indexation reste à qualifier.

## Trois rôles distincts

| Rôle | Autorité des données | Comportement |
| --- | --- | --- |
| PostgreSQL Core par défaut | PostgreSQL | Commands Core et lectures de référence ; projection LDAP facultative. |
| Projection LDAP de consultation | PostgreSQL | Copie dérivée sans ACL Pixs ; repli de lecture PostgreSQL selon contrat existant. |
| Stockage Core OpenLDAP interne | OpenLDAP pour le périmètre engagé | Lectures et écritures Core sur le provider LDAP ; aucune utilisation autoritative d'une ancienne copie PostgreSQL. |

Le même serveur peut avoir plusieurs responsabilités déclarées mais un même ensemble de données ne peut être simultanément projection et stockage de référence. Les namespaces, comptes et flux doivent empêcher une boucle de projection PostgreSQL vers un périmètre désormais autoritatif LDAP.

## Aller PostgreSQL vers OpenLDAP

1. Construire un plan versionné autorisé : acteurs, périmètre cohérent, source/cible, mappings, versions, sauvegardes, impacts et contrôles.
2. Vérifier les capacités et protections du service cible, ainsi que la recette de retour.
3. Préparer une copie protégée non autoritative, avec contrôles d'identités, contenu, relations et versions ; le volume seul ne prouve pas la fidélité.
4. Établir une barrière finale sur les écritures concernées, drainer les opérations admises et refuser les anciens écrivains. Une maintenance bornée du périmètre est une première stratégie possible ; aucune migration sans interruption n'est promise.
5. Réconcilier les derniers changements, révocations, suppressions et tombstones ; vérifier les invariants et l'audit applicables.
6. Engager durablement la génération de stockage et la cible unique ; propager l'invalidation des caches/contextes affectés avant réadmission.
7. Reprendre les accès sur la cible vérifiée ; conserver l'ancienne copie protégée et non autoritative selon politique, sans purge implicite.

Le support PostgreSQL peut conserver le journal de plan et le registre de génération sous protection déclarée ; cela ne fait pas de ses anciennes lignes Core une seconde source de vérité. Le mécanisme précis d'engagement et de fencing reste à choisir et prouver pour toutes les instances web/worker/scheduler.

## Retour OpenLDAP vers PostgreSQL

Le retour est une nouvelle migration depuis le LDAP courant. Il réutilise les contrôles précédents en inversant source et cible : copie, conservation de tous les changements intervenus, barrière finale, contrôle complet, engagement d'une nouvelle génération puis reprise. L'ancienne copie PostgreSQL ne peut pas être simplement dégelée.

Une panne LDAP ne vaut pas autorisation de retour : si l'état courant ne peut pas être acquis ou prouvé, la procédure ordinaire est suspendue. Une restauration de sinistre relève d'un plan séparé avec limites de perte reconnues ; elle ne peut annoncer une migration fidèle sans preuve.

## Concurrence et limites à qualifier

C02 D03-A conserve les transactions Django/contraintes PostgreSQL pour le provider initial. Le provider LDAP ne peut pas être déclaré équivalent par simple traduction de requêtes. Il doit démontrer unicité, relations, versionnement, exclusion, mutations multi-objets requises, audit avant confirmation, idempotence et publication durable compatibles avec les contrats voisins.

Les opérations LDAP et extensions transactionnelles doivent être qualifiées sur la version sélectionnée ; leur disponibilité et leurs garanties ne sont pas déduites d'une RFC. Si une garantie impérative ne peut être tenue, le provider ou la capacité reste non admissible ; aucun contournement ni double écriture non maîtrisée n'est ajouté.

Les commandes qui combinent données Core LDAP et mutations métier PostgreSQL requièrent un contrat explicite de cohérence, d'audit et de reprise. Aucune transaction atomique inter-stores ni contrainte SQL inter-store n'est supposée. Le filtrage autorisé, les références, la restauration et la réadmission doivent traiter les changements de génération.

## Dépendances et raccordements

- [C02 — données Core PostgreSQL](../archive/2026-10-20-add-core-postgres-services/design.md) : provider initial, contrat public et invariants.
- [OpenLDAP propre](../add-auth-managed-openldap/design.md) : service interne géré ; le rôle de stockage est explicitement distinct du rôle de projection.
- [Architecture Auth](../define-essential-autonomous-auth-module/design.md) : périmètre Core/Auth et maintien du stockage Auth PostgreSQL par défaut.
- [Autorisation runtime](../archive/2026-10-21-integrate-runtime-authorization-and-super-admin/proposal.md), [audit](../archive/2026-10-21-add-durable-minimized-audit/proposal.md), [migrations](../../specs/migrations/spec.md) et [réadmission](../add-p0-post-restore-reconciliation-and-readmission/proposal.md) : garanties impératives applicables.
- [Projection sortante](../add-ldap-outbound-directory-projections/design.md) et [lecture fraîche](../add-directory-read-freshness-and-postgres-fallback/design.md) : restent limités au mode projection.

L'exception Super Admin est conservée dans son périmètre canonique pour les contrôles applicatifs ; elle ne transforme pas une copie incomplète, un état d'engagement inconnu ou une double autorité en preuve technique acquise. Aucun résultat absent n'est fabriqué.

## Arbitrages avant réalisation

Définir contrat de provider, schémas et index LDAP, unités migrables, versionnement/générations, acteur et autorisation du plan, barrière et budgets, exclusion des accès directs, journal de reprise et preuve d'engagement, interactions outbox/audit/SQL, sauvegardes et rétention de l'ancienne copie. Conserver les garanties C02 avant toute sélection de l'option ; aucun code ni dépendance n'est autorisé ici.

## Recette future

Aller puis mutations via Pixs sur LDAP puis retour ; comparer identifiants, données, relations et décisions ALLOW/DENY avant/après. Tester copie incomplète, attribut non représentable, révocation pendant préparation, worker obsolète, réponse d'engagement perdue, interruption/reprise, panne LDAP sans repli et refus de désactivation avant retour. Tester isolation tenant, audit, effets différés et reprise après restauration sur une composition réelle.

## Références techniques

- [RFC 4511 — protocole LDAP](https://www.rfc-editor.org/rfc/rfc4511).
- [RFC 5805 — transactions LDAP](https://www.rfc-editor.org/rfc/rfc5805) : extension expérimentale à qualifier, sans supposer un support natif ou une équivalence avec PostgreSQL.
