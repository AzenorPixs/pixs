# Conception — C07

## Statut et périmètre autorisé

RÉALISATION EN COURS. La reprise documentaire initiale est appliquée et validée. Les contrats producteurs C03, C04 et C05 sont désormais livrés et recoupés. Le transport ASGI et le raccord serveur ci-dessous possèdent leurs preuves exécutées ; les intégrations restantes conservent leurs critères propres. C00 adopté et le canon demeurent la référence, sans delta normatif ajouté par ce jalon.

## État actuel vérifié

Constat : Le gabarit est toujours non prêt, les profils sont déclaratifs et composition_proof reste partielle ; l’activation réelle intégrée n’est pas démontrée.

Sources consultées et empreintes recoupées avec la matrice :

- [src/pixs/backend/settings.py](../../../src/pixs/backend/settings.py).
- [src/pixs/backend/checks.py](../../../src/pixs/backend/checks.py).
- [src/pixs/backend/composition_proof.py](../../../src/pixs/backend/composition_proof.py).
- [src/pixs/kernel/composition.py](../../../src/pixs/kernel/composition.py).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Fournir l’hôte runtime et les adapters du lifecycle commun, sans remplacer les mécanismes purs. Lier composants/providers/configuration/migrations et preuves authentifiées. L’hôte intermédiaire peut être exercé isolément mais refuse readiness P0 si PZT/DNS ou toute autre obligation manque ; C14 et C17 ferment l’intégration.

### Raccordement au canon adopté le 20 octobre 2026

La composition applicative comprend `pixs.core` et le module essentiel indépendant `pixs.auth`, avec une capacité locale PostgreSQL sélectionnée explicitement. L’absence du module, de sa capacité requise ou d’un état Auth courant empêche de revendiquer une activation applicative valide ; les fixtures structurelles non applicatives restent distinctes. Auth possède ses données et consomme les seuls contrats publics Core, sans cycle ni accès aux tables privées. Ses sous-modules suivent le manifest et le lifecycle communs, sans registre parallèle ; installation et activation de confiance restent distinctes.

Le profil standard ne sélectionne aucun connecteur externe ni service LDAP/KDC/AD implicite. C07 vérifie cette composition et consomme les contrats Auth de C03 ; il ne déplace pas dans le Kernel les sessions ou protocoles Auth. Les exigences et scénarios sources sont reliés dans requirements.md.

Le profil initial conserve `pixs.agent`, `pixs.pzt` et DNS essentiels, même réseau désactivé. Les trois exécutables PA et l’exécutable PZT indépendant, leurs états et leurs topologies restent distincts du runtime PBO. Le raccordement documentaire ne sélectionne ni ne lance ces exécutants ; l’hôte intermédiaire conserve un verdict P0 non prêt tant que les obligations C14/C17 et les autres preuves manquent.

| Interface consommée par C07 | Propriétaire | Condition avant intégration |
|---|---|---|
| Résolution de références de secrets et lifecycle du provider | C01 | Réutiliser les contrats publics livrés et l’exception d’amorçage dans sa seule phase autorisée ; aucun secret dans une preuve. |
| Identités, périmètres et services Core PostgreSQL | C02 | Consommer les contrats publics et leurs preuves, sans accès intercomposant aux tables privées. |
| Module Auth essentiel, capacité locale et état Auth courant | C03 | Contrats publics, données et migrations Auth restent chez leur propriétaire ; aucune disponibilité présumée. |
| Sink d’audit durable et conditions d’amorçage | C05 | Relier les effets aux garanties du sink disponible ; aucun journal local promu en autorité métier parallèle. |

Cette table désigne les responsabilités et conditions ; elle ne valide aucune signature d’interface encore ouverte et ne prouve pas la livraison d’un change actif.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions retenues et intégrations restantes

Le transport retenu est ASGI Django. `HostAsgi` reçoit explicitement le handler déjà configuré et le contexte asynchrone de l’hôte ; il ferme l’admission hors démarrage réussi, traite les événements lifespan et nettoie les contextes effectivement entrés. Les phases de transport restent distinctes de la disponibilité applicative.

`build_auth_server_bundle` raccorde les vrais lecteurs Auth PostgreSQL, `CoreFactSource`, le décideur C04 et le participant C05. Chaque invocation du décideur reçoit son propre store transactionnel et ses faits. La construction est testée sans requête SQL sur les deux alias liés ; le profil approuvé est relu lors des opérations. Cette construction n’est pas un verdict de disponibilité.

Le pont `runtime_resolve` et le provider C01 livré refusent actuellement une résolution hors `INSTALLER`. Le raccord de l’entrée et des phases doit respecter ce contrat. Le contexte de ressources, l’enregistrement des adaptateurs, la configuration et les observations de lifecycle restent à intégrer aux mécanismes communs. Le kit développeur disponible valide les manifests localement ; l’authentification de preuves ne peut pas être déduite de ce seul rapport.

Le profil web reste le candidat à une entrée publique explicitement déclarée. Workers, scheduler et management gardent leur frontière privée ou authentifiée, autorisée et auditée. Les choix de serveur, de port et de distribution restent aux lots concernés. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans leur périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [C01 — provider de secrets runtime](../archive/2026-10-19-add-pbo-runtime-secret-provider/proposal.md), archivé.
- [C02 — services Core PostgreSQL](../archive/2026-10-20-add-core-postgres-services/proposal.md), archivé.
- [C03 — authentification locale et sessions](../archive/2026-10-21-add-initial-authentication-and-sessions/proposal.md), producteur des contrats publics Auth.
- [C05 — audit durable minimisé](../archive/2026-10-21-add-durable-minimized-audit/proposal.md), producteur du sink d’audit.

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Ordre de composition déterministe, entrée runtime réelle en environnement isolé ; composant essentiel absent, fournisseur ambigu ou preuve manquante → P0 hors service. L’hôte intermédiaire ne certifie pas le produit ; intégration complète de PZT en C14 et recette installable en C17.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

### T02 — PBO/PFO réellement servi par le paquet

Le serveur/bundle/routage et la frontière HTTP distribuée ne sont pas détaillés par un propriétaire commun. N04 dédié : les clauses API de séparation façade web à cookie/API Bearer et de transport/stockage navigateur sont adoptées au canon le 20 octobre 2026 ; les autres choix de serveur et de frontière d’exposition restent à arrêter.

Contrôles à intégrer : Navigation directe du shell via service livré ; Erreur API sans fallback HTML ; Hôtes/origines/en-têtes non fiables, CSRF si cookie ; Management et rôles non publics.

### T04 — Kit de conformité versus recette finale

C17 consomme/agrège des suites ; kit réutilisable minimal non détaillé et O22 complet tirerait SDK hors profil. N06 dédié validé ; réutiliser validateurs/exemple, C17 garde campagne finale.

Contrôles à intégrer : Preuve absente/expirée/mauvaise version refusée ; Authentification de preuve par exécuteur réel, pas par manifest ; Exemple P0 synthétique hors dépendances de production.

### T06 — Marqueurs externes et états PostgreSQL

Marqueur d’installation et marqueur de désactivation Super Admin ont des fonctions différentes et ne sont pas une transaction atomique avec PostgreSQL. Compléter C08 et les contrats C03/C04/C09 ; N05 vérifie le rapprochement après restauration.

Contrôles à intégrer : Commit base avant marqueur : reprise sans second compte ; Marqueur absent/invalide interdit NORMAL sans relancer INSTALLER ; Désactivation non dérogée refuse nouvelles actions/reprises, transaction engagée préservée ; Secours propre sans MFA imposé.

### T11 — Arrêt, maintenance et ancien détenteur de lease

Le séquencement des nouvelles admissions, du drain et des reprises est une interaction ; un timeout du processus ne prouve pas la fin d’un effet. Compléter recette commune C09/C15/C18 ; pas de nouvel orchestrateur.

Contrôles à intégrer : Lease expiré empêchant une nouvelle action ; Maintenance ciblée et install entière distinguées ; Signal pendant effet, sortie explicite sans perte silencieuse ; Worker non public.

### T16 — Options, profils structurels et renvois Bulk

Un rattachement à un lot P0 n’active pas tout le domaine : Bulk, LDAP, flags avancés, quotas, SDK, sandbox et intégrité avancée restent conditionnés. Déclarer sélection/absence et maintenir les profils structurels existants ; ne pas traiter la non-sélection comme dispense d’une clause applicable.

Contrôles à intégrer : Absent représenté sans readiness fictive ; Contrat consommé réutilisé sans activer tout le catalogue ; Aucun code distant ni composant DEVELOPMENT en production ; Pas de promesse universelle de performance/HA.

Voir [audit transversal durable](../archive/2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.

## Preuves exécutées du socle hôte

| Périmètre | Résultat exécuté | Limite |
|---|---|---|
| Transport ASGI et guards Django existants | 8 cas enfant réussis, appel natif `call_01a15cb19e75756b8513e6d47ecb973f`, exit 0 | Contexte et routes de recette synthétiques ; aucune façade Auth simulée. |
| Raccord Auth/Core/audit | 5 contrôles PG réussis, appel natif `call_01a15cdab582749a94518eb9a77b50e4`, exit 0 ; PostgreSQL 16.14, Django 6.1.2, schéma nettoyé et connexions fermées | Plans/clés C08 et classification C10 fixtures ; hôte installé et P0 restent à qualifier. |
| Sources du jalon | 4 fichiers UTF-8/LF et empreintes vérifiées ; les 2 nouveaux fichiers du raccord compilés lors du contrôle PG | Les résultats portent sur les empreintes alors exécutées. |

La recette positive vérifie le jeton avant le retrait puis exige son refus par une nouvelle lecture de production après retrait. Les états `UNKNOWN`, `PENDING` ou une dérogation d’audit ne sont pas tenus pour un commit confirmé dans cette recette.
