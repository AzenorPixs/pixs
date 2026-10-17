# Conception — C07

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 formalise le profil ; ses précisions normatives restent proposées tant qu’elles ne sont pas approuvées/adoptées.

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

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Entrée de lancement, registre des adapters et limites d’exposition à arrêter sans nouveau runtime ; ne pas transformer globally_compatible=False en certificat global.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [add-pbo-runtime-secret-provider](../add-pbo-runtime-secret-provider/proposal.md).
- [add-core-postgres-services](../add-core-postgres-services/proposal.md).
- [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md).

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

Le serveur/bundle/routage et la frontière HTTP distribuée ne sont pas détaillés par un propriétaire commun. N04 dédié et deltas ciblés validés ; décisions de serveur/session/transport encore ouvertes.

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

Voir [audit transversal durable](../define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.
