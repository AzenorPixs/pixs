## 1. Preparation

- [x] 1.1 Prouver perimetre, absence de change actif et perimetre CGPT.
- [x] 1.2 Preparer les cinq artefacts et reussir la validation OpenSpec stricte avant code.

## 2. Fondation declarative des definitions de fanions

- [x] 2.1 Creer src/pixs/kernel/feature_flags.py seul : FeatureFlagDefinition frozen a douze champs canoniques obligatoires sans aucun defaut (flag_id namespacé, flag_version metadonnee opaque sans comparaison ni grammaire SemVer, owner_component, purpose prose jamais executee ni filtree par heuristique, value_schema BOOLEAN ou VARIANT, default_value bool exact pour BOOLEAN ou token litteral pour VARIANT, targeting_dimensions tuple whitelist INSTALLATION/ENVIRONMENT/TENANT/SCOPE sans ciblage effectif, cohort_key value eventuellement None mais champ obligatoire, prerequisites tuple de references sans doublons, fallback_policy et audit_policy declarations bornees sans evaluateur, expires_at obligatoire jamais None) ; aucun champ expression/code/rule/callback, kwargs inconnus reellement refuses a la construction ; validate_feature_flag_definitions en refus aggrégatif a conteneur list/tuple exact avant iteration et items FeatureFlagDefinition exacts avant attributs, identite de type par type(x) is Classe avant toute egalite/tri/hachage/appartenance/analyse, diagnostics constants sans echo de valeur invalide ni index dependant de l'ordre, tri deterministe, flag_id dupliques refuses meme a version differente ; expires_at borne au format ASCII YYYY-MM-DDTHH:MM:SS[.fraction](Z ou +00:00, fraction 1 a 6 chiffres) verifiee par positions caracteres avant datetime.fromisoformat, ValueError date impossible refuse, UTC exige, sans now/time/horloge/environnement ni decision d'expiration runtime ; identifiants nus et namespacés valides par parse_requirement partage (contraintes vides et target_id egal a la valeur), grammaire des composants existants conservee avec points/tirets/majuscules/chiffres, aucune regex parallèle inventee ; module pur stdlib.
- [x] 2.2 Creer tests/unit/test_feature_flag_definitions.py : douze champs requis sans defaut et cohort_key None explicite admis tandis que tout autre None refuse (dont expires_at None refuse) ; BOOLEAN bool exact avec int refuse, VARIANT token borne ; value_schema et dimensions hors whitelist refusées, doublons de dimensions refusés ; entrees permutees produisent diagnostics identiques sans index dependant de l'ordre ; flag_id dupliqué refusé même a version differente ; hostiles (callable, sous-classe non exacte, metaclass, instance etrangere) refuses sans declenchement d'eq/hash sur donnees invalides et sans crash ; conteneur d'entree non list/tuple exact refuse avant iteration ; purpose prose non altéree ; expires_at : Z et +00:00 acceptes, naif +02:00 garbage vide refusés, formats decale hors borne ASCII (espace separateur, date compacte, week-date, fraction plus de 6 chiffres) refusés — sans horloge systeme, import stdlib datetime legitime ; messages constants ne reproduisant aucune valeur invalide.
- [x] 2.3 Creer tests/integration/test_feature_flag_definitions_integration.py : interpreteur enfant frais sans bytecode sous gardes IO causales avant import, aucun I/O metier, construction et validation d'une definition temoin sans diagnostic, refus ferme d'une tentative de champ ou valeur d'expression (callable) avant tout usage, absence d'effet verifiee, marqueur final dedie, perimetre sans Django/PG/reseau, autres sources inchangees.

## 3. Preuves

- [x] 3.1 Reussir py_compile des trois fichiers sous l'interpreteur DEVOPS actuel (min 3.11, runtime 3.14.8) puis tests unitaires et integration sous mandats distincts.
- [x] 3.2 Verifier UTF-8 LF, perimetre feature_flags.py plus deux suites, relecture byte-exacte des fichiers figes, regression ciblée des suites existantes sous runtime actuel, strict valide apres preuves avant tout cochage.
- [x] 3.3 Prouver delta normatif MOTAMOT de la seule exigence R1 sans scenario ajoute, R2-R4 de feature-flags inchangees, baseline nouvelle prise avant preparation par le checker (preservation des 3 sources availability, 6 artefacts archives/stat, 133 hashes y compris la mise a jour developpeur AGENTS, config LLM autorisee) et non un ancien recompte suppose ; declarer explicitement ce qui reste non realise : aucun evaluateur runtime, aucune persistance ni affectation, aucune operation admin ou audit effectif, aucun cycle de vie ni decision d'expiration, aucun lien resolution/gate, R3 de capabilities non déclaré réalisé ; archivage et statistiques distincts apres controle.

Archivage et statistiques distincts apres preuves, conserves dans le RUN parent.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Preuves ».

### O44-SL01 — Prouver perimetre, absence de change actif et perimetre CGPT.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Preparation », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O44-SL02 — Preparer les cinq artefacts et reussir la validation OpenSpec stricte avant code.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Preparation », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O44-SL03 — Creer src/pixs/kernel/feature_flags.py seul : FeatureFlagDefinition frozen a douze champs canoniques obligatoires sans aucun defaut (flag_id namespacé, flag_version metadonnee opaque sans comparaison ni grammaire SemVer, owner_component, purpose prose jamais executee ni filtree par heuristique, value_schema BOOLEAN ou VARIANT, default_value bool exact pour BOOLEAN ou token litteral pour VARIANT, targeting_dimensions tuple whitelist INSTALLATION/ENVIRONMENT/TENANT/SCOPE sans ciblage effectif, cohort_key value eventuellement None mais champ obligatoire, prerequisites tuple de references sans doublons, fallback_policy et audit_policy declarations bornees sans evaluateur, expires_at obligatoire jamais None) ; aucun champ expression/code/rule/callback, kwargs inconnus reellement refuses a la construction ; validate_feature_flag_definitions en refus aggrégatif a conteneur list/tuple exact avant iteration et items FeatureFlagDefinition exacts avant attributs, identite de type par type(x) is Classe avant toute egalite/tri/hachage/appartenance/analyse, diagnostics constants sans echo de valeur invalide ni index dependant de l'ordre, tri deterministe, flag_id dupliques refuses meme a version differente ; expires_at borne au format ASCII YYYY-MM-DDTHH:MM:SS[.fraction](Z ou +00:00, fraction 1 a 6 chiffres) verifiee par positions caracteres avant datetime.fromisoformat, ValueError date impossible refuse, UTC exige, sans now/time/horloge/environnement ni decision d'expiration runtime ; identifiants nus et namespacés valides par parse_requirement partage (contraintes vides et target_id egal a la valeur), grammaire des composants existants conservee avec points/tirets/majuscules/chiffres, aucune regex parallèle inventee ; module pur stdlib.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Fondation declarative des definitions de fanions », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O44-SL04 — Creer tests/unit/test_feature_flag_definitions.py : douze champs requis sans defaut et cohort_key None explicite admis tandis que tout autre None refuse (dont expires_at None refuse) ; BOOLEAN bool exact avec int refuse, VARIANT token borne ; value_schema et dimensions hors whitelist refusées, doublons de dimensions refusés ; entrees permutees produisent diagnostics identiques sans index dependant de l'ordre ; flag_id dupliqué refusé même a version differente ; hostiles (callable, sous-classe non exacte, metaclass, instance etrangere) refuses sans declenchement d'eq/hash sur donnees invalides et sans crash ; conteneur d'entree non list/tuple exact refuse avant iteration ; purpose prose non altéree ; expires_at : Z et +00:00 acceptes, naif +02:00 garbage vide refusés, formats decale hors borne ASCII (espace separateur, date compacte, week-date, fraction plus de 6 chiffres) refusés — sans horloge systeme, import stdlib datetime legitime ; messages constants ne reproduisant aucune valeur invalide.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Fondation declarative des definitions de fanions », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O44-SL05 — Creer tests/integration/test_feature_flag_definitions_integration.py : interpreteur enfant frais sans bytecode sous gardes IO causales avant import, aucun I/O metier, construction et validation d'une definition temoin sans diagnostic, refus ferme d'une tentative de champ ou valeur d'expression (callable) avant tout usage, absence d'effet verifiee, marqueur final dedie, perimetre sans Django/PG/reseau, autres sources inchangees.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Fondation declarative des definitions de fanions », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O44-SL06 — Reussir py_compile des trois fichiers sous l'interpreteur DEVOPS actuel (min 3.11, runtime 3.14.8) puis tests unitaires et integration sous mandats distincts.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Preuves », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O44-SL07 — Verifier UTF-8 LF, perimetre feature_flags.py plus deux suites, relecture byte-exacte des fichiers figes, regression ciblée des suites existantes sous runtime actuel, strict valide apres preuves avant tout cochage.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Preuves », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### O44-SL08 — Prouver delta normatif MOTAMOT de la seule exigence R1 sans scenario ajoute, R2-R4 de feature-flags inchangees, baseline nouvelle prise avant preparation par le checker (preservation des 3 sources availability, 6 artefacts archives/stat, 133 hashes y compris la mise a jour developpeur AGENTS, config LLM autorisee) et non un ancien recompte suppose ; declarer explicitement ce qui reste non realise : aucun evaluateur runtime, aucune persistance ni affectation, aucune operation admin ou audit effectif, aucun cycle de vie ni decision d'expiration, aucun lien resolution/gate, R3 de capabilities non déclaré réalisé ; archivage et statistiques distincts apres controle.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Preuves », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
