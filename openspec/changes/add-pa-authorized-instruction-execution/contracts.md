# Contrats proposés — PA04 profil 1A-2B-3A

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

Proposition révisable, sans code. OBSERVE, PREPARE_PLAN, START, STOP, READ_RESULT : noms de travail, pas identifiants API livrés. Choix 1A-2B-3A acquis ; invariants et exception Super Admin canonique conservés dans son seul périmètre.

## Règles communes

Aucune permission par seule identité. Mandat, confirmation, plan et provenance réellement vérifiés. PBO-PA via PZT, pas de SQL direct. En profil connecté, perte du contrôle bloque nouveaux effets. Une compensation hors profil ou plan MUST NOT être tentée. Une permission révoquée MUST NOT être restaurée.

## OBSERVE

Entrées : mandat courant, cible allowlistée, génération. Effet : aucun. Sortie : observation réellement lue avec cible et génération. Refus : mandat périmé, cible hors allowlist, PZT indisponible. Rejeu idempotent par clé sans double effet. Incertain réinterrogé sans effet. Propriétaire : PA système, supervision pixs.agent.

## PREPARE_PLAN

Entrées : mandat, cible, paramètres bornés à fermer. Effet : aucun. Sortie : plan versionné à confirmer. Refus : plan hors mandat, cible non autorisée, mandat expiré. Rejeu idempotent. Propriétaire : PA système, supervision pixs.agent.

## START

Entrées : mandat et plan courants, service produit explicitement autorisé inscrit au livré, génération courante. Essais seuls sur factice dédié. Effet borné autorisé. Postcondition native vraiment observée par propriétaire courant liée à cible, génération et artefact ; reçu seul insuffisant. Refus : nom libre, RESTART, ENABLE, DISABLE, comptes, fichiers, installation, réseau, services PA/PZT/CAB/SSH/PostgreSQL, mandat périmé, hors ligne. Idempotence ne garantit pas exactement une fois après crash : issue incertaine exige postcondition fiable ou intervention autorisée avant nouvel effet. Propriétaire effet : PA système ; preuve : propriétaire courant.

## STOP

Entrées : mandat et plan courants, service produit explicitement autorisé inscrit au livré, génération courante. Essais seuls sur factice dédié. Effet borné d’arrêt. Postcondition native vraiment observée liée à cible, génération et artefact. Mêmes exclusions de cible et d’opérations que START, sans interdire des contrôles de sécurité supplémentaires. Incertain réconcilié sans double effet, avec intervention autorisée si postcondition invérifiable. Propriétaire effet : PA système ; preuve : propriétaire courant.

## READ_RESULT

Entrée : opération et mandat courants. Sortie : état réellement durable succès, échec ou inconnu, distinct du reçu, sans rejouer. Si preuve durable manque, rapporter inconnu avec références, sans preuve inventée. Propriétaire : PA système, supervision pixs.agent.

## Interface et preuves

Interface : mandats, contexte, générations, handles, résultats observés. Matrice : mandat périmé bloqué, crash réconcilié, acteur initial conservé. Distinguer schéma déclaré, port livré et runtime qualifié. Formats wire, identifiants, versions, confiance, durabilité, bornes et budgets à mesurer restent barrières explicites. Aucune valeur, bibliothèque, rôle, compte, service réel, architecture, provider ou preuve inventés.

## Unite locale integree catalogue PA04 — logique exacte a examiner

Champs par operation, tous service_ref sauf precision : OBSERVE service_ref seul ; PREPARE_PLAN service_ref plus action limitee a START ou STOP ; START service_ref plus plan_ref ; STOP service_ref plus plan_ref ; READ_RESULT service_ref plus operation_ref. Aucune autre combinaison admise, parametres inconnus refuses.

Bornes en octets UTF-8, appliquees uniformement apres validation generique qui compte en caracteres : un champ valide generiquement mais hors borne locale est refuse ici. Refus : vide, controles C0/DEL/C1, Unicode invalide, hors borne, nom libre hors allowlist, action interdite dont CONFIGURE/RESTART/ENABLE/DISABLE. Version catalogue SemVer fournie par profil serveur, aucune constante produit. Comparaison et forme seulement, jamais preuve d existence, actualite ou confirmation de plan.

Precisions profil contre instruction : profil serveur mal forme leve ValueError a message fixe sans valeur sensible ; instruction non conforme retourne tuple Diagnostic VALIDATE sans valeur sensible. Version SemVer exigee fournie par serveur, aucun defaut version produit.
