## 1. Preparation

- [x] 1.1 Prouver perimetre, absence de change actif et baseline nouvelle 168 incluant les sources core masquees heritees.
- [x] 1.2 Preparer les cinq artefacts et reussir la validation OpenSpec stricte avant code.

## 2. Mapping declaratif d'assurance fournisseur

- [x] 2.1 Creer src/pixs/core/authz/assurance_mapping.py seul : ProviderAssuranceMapping (provider_id opaque non vide, trois plafonds globaux par dimension sur les enums existantes importees, accepted_rules tuples AssuranceRule dimension method niveau de cette dimension, valid_from valid_until), ProofObservation (statut dans le vocabulaire ferme ABSENT AMBIGUOUS EXPIRED UNVERIFIED VERIFIED, attested_at expires_at finis UTC stricts, aucune valeur None, tuple vide pour absence, constats normalises non secrets d'un hote deja authentifie), evaluate_assurance a reference_time fourni par l appelant sans horloge, fenetres demi ouvertes, contribution seulement au niveau declare de chaque regle referencee par dimension et methode et fournisseur, jamais de plafond implicite ni hausse d autre dimension, divergence ou absence au minimum de la dimension, AssuranceMappingError constant sans echo declenche par identites de type exactes str non vides UTC reels unicite dimension method et ordre de declaration des enums avant tout acces étranger, sans invocation de decision._rank, seule reutilisation du helper UTC policy._is_utc_aware valide CGPT, sans grammaire nouvelle ; identite de membre enum avant hachage/ordinal, jamais appartenance du type a un tuple de classes.
- [x] 2.2 Creer tests/unit/test_provider_assurance_mapping.py : plafond par dimension respecte, niveau regle superieur au plafond refuse, unicite des regles, regle d une dimension sans effet sur les autres, observation VERIFIED valideUnique donne le niveau declare, absence tuple vide donne le minimum, divergence de niveaux donne le minimum, statuts ABSENT AMBIGUOUS EXPIRED UNVERIFIED et heures hors fenetres ne contribuent jamais, reference_time explicite sans horloge systeme, permutations et determinisme, conteneurs scalaires et hostiles refuses sans invocation eq hash iter repr ; observation_id duplique refuse ; erreurs structurelles constantes (meme code element step message sous permutation) sans echo et sans retour de diagnostics ; niveaux divergents bien formes restent au minimum par dimension.
- [x] 2.3 Creer tests/integration/test_provider_assurance_mapping_integration.py : interpreteur enfant frais sans bytecode sous gardes IO causales avant import du module, aucun I/O metier, evaluation temoin deterministe sous niveau declare, refus ferme d un mapping au plafond viole avant tout effet, absence de Django PostgreSQL reseau, marqueur final dedie, aucune autre source touchee.

## 3. Preuves

- [x] 3.1 Reussir py_compile reel des trois fichiers sous DEVOPS Python 3.14.8 et verifier syntaxe minimale 3.11 par AST du checker, sans execution 3.11 revendiquee puis suites nouvelles sous mandats distincts.
- [x] 3.2 Reussir les regressions PDP directement concernees (policy decision time) et tests identite/perimetre lies aux imports reutilises sans PostgreSQL ni Django, les 200 tests du change precedent deja prouves ne sont pas rejoues sans interaction nouvelle, verifier baseline 168 preservee, stricts valide avant cochage puis apres, seul le delta R1 MOTAMOT present sans nouveau requirement ni scenario.
- [x] 3.3 Prouver les limites declarees : portion R1 du mapping seulement, pas authentification reelle, pas de verification crypto, pas de permission ni de niveau implicitement prouve depuis un statut autodeclore, R2 R3 partiellement couverts par le PDP existant mais integrations reelles non realisees ; archivage et statistiques distincts apres controle.

Archivage et statistiques distincts apres preuves, conserves dans le RUN parent.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 3. Preuves ».

### C54-SL01 — Prouver perimetre, absence de change actif et baseline nouvelle 168 incluant les sources core masquees heritees.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Preparation », ligne 3 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C54-SL02 — Preparer les cinq artefacts et reussir la validation OpenSpec stricte avant code.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Preparation », ligne 4 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C54-SL03 — Creer src/pixs/core/authz/assurance_mapping.py seul : ProviderAssuranceMapping (provider_id opaque non vide, trois plafonds globaux par dimension sur les enums existantes importees, accepted_rules tuples AssuranceRule dimension method niveau de cette dimension, valid_from valid_until), ProofObservation (statut dans le vocabulaire ferme ABSENT AMBIGUOUS EXPIRED UNVERIFIED VERIFIED, attested_at expires_at finis UTC stricts, aucune valeur None, tuple vide pour absence, constats normalises non secrets d'un hote deja authentifie), evaluate_assurance a reference_time fourni par l appelant sans horloge, fenetres demi ouvertes, contribution seulement au niveau declare de chaque regle referencee par dimension et methode et fournisseur, jamais de plafond implicite ni hausse d autre dimension, divergence ou absence au minimum de la dimension, AssuranceMappingError constant sans echo declenche par identites de type exactes str non vides UTC reels unicite dimension method et ordre de declaration des enums avant tout acces étranger, sans invocation de decision._rank, seule reutilisation du helper UTC policy._is_utc_aware valide CGPT, sans grammaire nouvelle ; identite de membre enum avant hachage/ordinal, jamais appartenance du type a un tuple de classes.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Mapping declaratif d'assurance fournisseur », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C54-SL04 — Creer tests/unit/test_provider_assurance_mapping.py : plafond par dimension respecte, niveau regle superieur au plafond refuse, unicite des regles, regle d une dimension sans effet sur les autres, observation VERIFIED valideUnique donne le niveau declare, absence tuple vide donne le minimum, divergence de niveaux donne le minimum, statuts ABSENT AMBIGUOUS EXPIRED UNVERIFIED et heures hors fenetres ne contribuent jamais, reference_time explicite sans horloge systeme, permutations et determinisme, conteneurs scalaires et hostiles refuses sans invocation eq hash iter repr ; observation_id duplique refuse ; erreurs structurelles constantes (meme code element step message sous permutation) sans echo et sans retour de diagnostics ; niveaux divergents bien formes restent au minimum par dimension.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Mapping declaratif d'assurance fournisseur », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C54-SL05 — Creer tests/integration/test_provider_assurance_mapping_integration.py : interpreteur enfant frais sans bytecode sous gardes IO causales avant import du module, aucun I/O metier, evaluation temoin deterministe sous niveau declare, refus ferme d un mapping au plafond viole avant tout effet, absence de Django PostgreSQL reseau, marqueur final dedie, aucune autre source touchee.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Mapping declaratif d'assurance fournisseur », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C54-SL06 — Reussir py_compile reel des trois fichiers sous DEVOPS Python 3.14.8 et verifier syntaxe minimale 3.11 par AST du checker, sans execution 3.11 revendiquee puis suites nouvelles sous mandats distincts.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Preuves », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C54-SL07 — Reussir les regressions PDP directement concernees (policy decision time) et tests identite/perimetre lies aux imports reutilises sans PostgreSQL ni Django, les 200 tests du change precedent deja prouves ne sont pas rejoues sans interaction nouvelle, verifier baseline 168 preservee, stricts valide avant cochage puis apres, seul le delta R1 MOTAMOT present sans nouveau requirement ni scenario.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Preuves », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C54-SL08 — Prouver les limites declarees : portion R1 du mapping seulement, pas authentification reelle, pas de verification crypto, pas de permission ni de niveau implicitement prouve depuis un statut autodeclore, R2 R3 partiellement couverts par le PDP existant mais integrations reelles non realisees ; archivage et statistiques distincts apres controle.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Preuves », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
