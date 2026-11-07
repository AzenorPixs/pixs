# Conception — O06

## Statut

REPRISE_DOCUMENTAIRE_VALIDÉE_PAR_LE_DÉVELOPPEUR le 22 octobre 2026. Les modalités v1 ci-dessous sont adoptées pour les six documents nommés. Le développeur a ensuite autorisé explicitement la métadonnée .openspec.yaml, uniquement pour skip_specs true vers false, portant la reprise à sept fichiers. Leur validation stricte précède l’implémentation séquentielle déjà autorisée du seul O06 par le parent CISMP5. Aucun test runtime n’est déduit du document.

## Contexte actuel

La capacité est un candidat du canon ; la revue de présence des sources et la matrice ne démontrent pas une réalisation opérationnelle. Lors de la préparation RSMP, les quatre lignes historiques étaient non qualifiées au runtime ; la qualification ultérieure du seul profil v1 est consignée ci-dessous. Les références normatives complètes sont dans requirements.md.

Références du lot : README.md, src/pixs/kernel/composition.py, src/pixs/backend/README.md, DEVOPS.md inventaire 2026-10-22T19:48:20Z, pyproject.toml.

## Architecture et frontières

Composant strictement facultatif au-dessus du Kernel, déclaré par manifest et sélection explicite. Contrats publics versionnés seuls exposés. Écritures seules via le propriétaire. Django et PostgreSQL conservés comme autorités, avec tenant et scope, audit et gouvernance.

Périmètre propre au lot : règles versionnées et déterministes avec explications ; effets par propriétaire ; sécurité distincte.

## Choix déjà fixés et alternatives

Les quatre exigences et leurs cinq titres de scénarios sont conservés ; les scénarios sont précisés par le profil v1 adopté, sans modification des garanties existantes. Aucune bibliothèque, aucun provider, aucune dépendance présente dans DEVOPS n'est sélectionné ni qualifié par cet inventaire. Les plafonds du profil v1 sont : document 65536 octets, profondeur 8, noeuds 256. Opérateurs retenus : all, any, not, eq, ne, lt, lte, gt, gte, in, exists. Types retenus : null, boolean, integer, string, array. Boolean distinct de integer, sans coercition implicite.

## Barrières de conception avant réalisation

Validation avant activation puis évaluation sans mutation. Le moteur fournit une proposition et des motifs minimisés ; le module propriétaire réévalue autorisation, garde et version avant sa Command. Une recommandation favorable ne vaut pas permission. Catalogue et tables versionnés dans les seuls contrats déjà validés. Aucune bibliothèque choisie implicitement.

Les choix du profil v1 ont été explicitement validés pour cette reprise. Tout écart hors de ce profil reste une décision distincte ; les tâches ne commencent qu’après réussite de la validation documentaire.

## Dépendances et interfaces

- integrate-runtime-authorization-and-super-admin.
- add-durable-minimized-audit.
- add-protected-core-http-commands-and-queries.

Les dépendances sont des contrats et preuves attendus. Un dossier créé ne signifie pas que sa dépendance est exécutée ou disponible.

## Grammaire opposable

La définition intégrale de l’enveloppe à sept champs, input_schema, AST {op,args}, opérandes {field:nom}/{literal:valeur}, types, arités, comptage des bornes, corpus cases et résultat fermé figure dans les scénarios du canon et leur delta MODIFIED. requirements.md les reproduit avec empreintes. Aucune arité, coercition, priorité ou valeur implicite ne peut être inventée par l’implémentation. Les cas versionnés sont validés syntaxiquement puis exécutés avant activation stable ; le catalogue refuse une même identité/version de contenu divergent.

## Vérification future

Source de vérité, isolation tenant et scope, refus sans permission, classification et rétention, reprise et révocation ; contrat du provider sur dépendance réelle, tests navigateur si interface web et audit manuel lorsque requis.

Sortie du lot : reproductibilité ; pas de code arbitraire ou non déclaré ; règle sans élévation de droit.

Exercer tous les scénarios et clauses applicables des blocs sources. Un scénario non applicable sera motivé par le profil réel.

## Migrations, reprise et arrêt

Aucun schéma ni état runtime modifié ici. Toute réalisation ultérieure qui persiste des données précisera propriétaire, contrat de migration, concurrence, reprise, durabilité et compensation.

## Limites du dossier

Pas de qualification actuelle ni d'achèvement produit revendiqué. L'autorisation de préparation ne permet ni d'activer la capacité dans P0 ni d'utiliser un compte connecté, publier un artefact ou envoyer une notification réelle.

## Qualification du profil v1 — 23 octobre 2026

La réalisation comprend les six modules de src/pixs/business_rules : codec JSON borné, profil immuable, moteur et catalogue, exports purs, manifest facultatif et raccordement Core explicite. Le manifest du provider pixs.business-rules 1.0.0 déclare la capacité business-rules.evaluate et le contrat business-rules.evaluation 1.0.0, avec Kernel et Core 0.1.0 existants. Son import ne compose ni n'active le provider.

La composition de confiance choisit BusinessRuleCoreBinding, son catalogue et une Command Core existante hors DSL. Le raccordement contrôle les racines publiques et les contextes explicites des DTO qui en possèdent un. Les DTO Core sans contexte restent supportés ; la Request et les gardes de la Command conservent leur autorité. L'autorisation actuelle précède l'évaluation ; la Command réévalue ensuite ses droits, gardes, gouvernance et version sous ses propres verrous.

L'explication contient exactement les sept champs du résultat dans reason_or_error de l'événement C05 PROPOSED. Elle est commise dans une transaction audit distincte avant la tentative de Command. Une proposition ne confirme aucun effet métier ; un refus du propriétaire est propagé intact et laisse cette proposition consultable. Un échec d'audit ou l'effacement des champs indispensables interdit la mutation. Une transaction externe est refusée pour préserver les frontières durables des propriétaires.

La consultation utilise filter_audit et ses contrôles C04/C05 actuels. La composition doit déclarer explicitement le propriétaire audit: dans RuntimeTrustedFactsProvider et RuntimeCandidateSource AUDIT dans RuntimeSourceFilterProvider, avec les ports publics audit_resource_ownership et audit_candidate_references. Aucune corrélation ne confère un droit et aucune source AUDIT n'est découverte implicitement.

Les preuves exécutées et les dix empreintes de sources/tests figurent dans requirements.md : 95 unitaires, 13 critères PostgreSQL réels et six refus explicites avant activation. La recette a observé Django 6.1.2 et PostgreSQL 16.14, puis détruit son seul schéma possédé et fermé les connexions. Auth, C04, C05, Core et C06 sont réels dans cette recette ; C09 et C10 restent des participants explicitement synthétiques. Aucun frontend n'a changé : les contrôles navigateur sont non applicables. Aucune activation P0 ni qualification globale du produit n'est déduite.
