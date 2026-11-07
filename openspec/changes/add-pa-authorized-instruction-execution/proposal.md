# PA04 — Instructions, mandats et exécution locale

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

Instructions et mandats contextualisés, opérations multi-rôles, revalidation, résultats observés et reprise sans double effet.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [pixs-agent](../../specs/pixs-agent/spec.md).
- [scope-context](../../specs/scope-context/spec.md).
- [zt-controller](../../specs/zt-controller/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Pourquoi

Le canon distingue trois binaires PA et six modes, plus le binaire indépendant PZT et son mode pzt-daemon ; le README indique que l’implémentation, la qualification et les artefacts restent à réaliser. Le contrôle de présence ciblé des sources n’est pas une recette de plateforme.

Les références de la matrice et les fichiers présents ne constituent pas une preuve fonctionnelle actuelle. Relire le code concerné et ses preuves avant de décider le complément à réaliser.

## Modifications proposées

Contrats publics des instructions, fraîcheur, scopes, idempotence, revalidation, compensation préautorisée et réconciliation après résultat incertain ; aucun code distant implicite.

## Capacités

### Capacités nouvelles

Aucune nouvelle capacité indépendante. Les cinq opérations OBSERVE, PREPARE_PLAN, START, STOP, READ_RESULT modifient la capacité existante pixs-agent dans le profil 1A-2B-3A. Voir specs/pixs-agent/spec.md et contracts.md proposés.

### Capacités modifiées

Capacité existante pixs-agent modifiée par delta conditionnel 1A-2B-3A. `requirements.md` référence et reproduit les blocs sources, avec empreintes et scénarios. Formats wire, identifiants API, versions, ports, paramètres, confiance, durabilité, bornes et budgets restent ouverts et à mesurer.

## Sélection et périmètre autorisé

Le profil `pbo-p0-debian-local-v1` sélectionne le sous-ensemble nécessaire à
la préparation PostgreSQL par PA système via PZT local, selon le
[canon de composition](../../specs/reference-composition/spec.md) et le parcours
[C08](../add-installation-and-first-configuration/proposal.md). Les obligations
de ce dossier applicables à ce parcours doivent être réalisées et qualifiées.
Les autres rôles PA et le réseau PZT distant restent conditionnés au profil
sélectionné ; cette préparation documentaire ne les active ni ne les qualifie.

La demande actuelle porte exclusivement sur les documents de préparation. Aucun code, test produit, serveur, accès fournisseur, secret, migration, dépendance, configuration système, publication, Git ou archivage n’est exécuté par ce dossier.

## Dépendances

- [add-pa-system-session-lifecycle](../add-pa-system-session-lifecycle/proposal.md).
- [add-pzt-wireguard-local-transport-and-filtering](../add-pzt-wireguard-local-transport-and-filtering/proposal.md).
- [add-pzt-network-mandates-and-fail-closed-revocation](../add-pzt-network-mandates-and-fail-closed-revocation/proposal.md).
- [add-pzt-public-control-contracts-and-state-streams](../add-pzt-public-control-contracts-and-state-streams/proposal.md).
- [add-pzt-pa-admission-and-ephemeral-peer-generation](../add-pzt-pa-admission-and-ephemeral-peer-generation/proposal.md).
- [integrate-runtime-authorization-and-super-admin](../archive/2026-10-21-integrate-runtime-authorization-and-super-admin/proposal.md).
- [add-durable-minimized-audit](../archive/2026-10-21-add-durable-minimized-audit/proposal.md).



## Impact de réalisation future

Couche locale séparée de Django/PostgreSQL et sans autorité métier. Composer les opérations au build par contrats, dispatch explicite et identité du mode ; isoler comptes/sessions, handles et générations. Lier mandats, contexte, effets et résultats observés ; communiquer avec PBO uniquement via PZT. Les trois binaires PA (Cython) et PZT indépendant (Cython) restent colivrés, sous gestion respective de pixs.agent et pixs.pzt.

## Critère de sortie de réalisation future

Mandat périmé/révoqué bloqué ; crash entre effet et résultat réconcilié ; acteur initial conservé sans credentials Super Admin transférés.

## Décisions restant à valider

Catalogue exact des opérations, schémas d’instructions/mandats et preuves de postconditions ; aucun shell arbitraire ou compensation hors plan.
