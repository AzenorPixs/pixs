# Conception — C14

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 a été adopté et archivé le 18 octobre 2026 ; ses précisions normatives sont intégrées au canon. Les arbitrages propres au présent change restent à lever avant réalisation.

## État actuel vérifié

Constat : Le canon impose les modules PZT et DNS essentiels ; aucun module produit PZT/DNS n’est identifié aux emplacements consultés. La spécification seule ne les fournit pas.

Sources consultées et empreintes recoupées avec la matrice :

- [openspec/specs/pzt/spec.md](../../specs/pzt/spec.md).
- [openspec/specs/reference-runtime/spec.md](../../specs/reference-runtime/spec.md).
- [README.md](../../../README.md).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Composer deux responsabilités de gestion PBO propriétaires via les mécanismes communs ; identifiant pixs.pzt validé, identifiant DNS et manifests/contrats exacts restant à préciser. Conserver configuration souhaitée, versions et états d’absence d’exécutant ; appliquer les choix validés pertinents à la configuration. N’engager aucun PA, service DNS ou réseau non sélectionné, ni canal de substitution.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Identifiants canoniques et contrats de gestion, sous-modules et schémas ; recouper chaque clause applicable de la table C00. Toute obligation active non conditionnelle rejoint le chemin critique ; aucune exemption supposée.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [define-first-installable-pbo-profile](../archive/2026-10-18-define-first-installable-pbo-profile/proposal.md).
- [add-core-postgres-services](../add-core-postgres-services/proposal.md).
- [integrate-runtime-authorization-and-super-admin](../integrate-runtime-authorization-and-super-admin/proposal.md).
- [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md).
- [add-protected-core-http-commands-and-queries](../add-protected-core-http-commands-and-queries/proposal.md).
- [compose-modular-frontend-with-core-api](../compose-modular-frontend-with-core-api/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Modules composés même réseau désactivé ; absence essentielle bloquante ; configuration/visualisation/supervision honnêtes ; aucune mesure ni application réseau inventée ; aucun canal PBO–PA de substitution ; chaque clause conservée, motivée ou renvoyée vers évolution normative approuvée.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

### T14 — PZT/DNS gérés sans exécution PA

La table 193 clauses reste conditionnelle et exige revue par rôle avant adoption ; classement exécutant ne retire pas les clauses PBO de gestion. Conserver C14 comme propriétaire, contrats/schémas/valeurs administrées explicités avant code ; aucun nouveau change exécutant sélectionné.

Contrôles à intégrer : Modules essentiels présents même réseau désactivé ; État souhaité distinct de mesure/appliqué ; Suffixe/droits/conflits des données gérées conformes ; Aucune publication DNS/réseau ni modification hôte inventée.

Voir [audit transversal durable](../archive/2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.

## Identifiant et séparation validés le 17 octobre 2026

pixs.pzt est le nom canonique adopté du module essentiel PZT. Ce lot conserve
sa gestion réseau et DNS ; le nouveau lot [PA10](../separate-pa-pzt-and-pbo-management-modules/design.md)
porte pixs.agent, qui gère PA hors PZT. L'exécutant réseau est PZT indépendant,
colivré avec PA. Le nom pixs.pzt n'est plus un arbitrage ouvert ; les contrats
concrets et le nom du module DNS restent à qualifier. Relire les instantanés
requirements.md contre le canon actuel avant reprise ; aucune tâche produit
n'est réalisée par cet alignement documentaire.
