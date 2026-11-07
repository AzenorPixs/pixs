# Tâches — Représentation minimale d’un événement d’audit

## 1. Publication du module de représentation

- [x] 1.1 Publier exactement `src/pixs/kernel/audit_event.py` comme module pur du Kernel, sans aucune autre source applicative ajoutée ou modifiée.
- [x] 1.2 Écrire une docstring de module indiquant que les valeurs sont fournies par un caller trusted ou des fixtures synthétiques, que la validation est structurelle et qu’aucune persistance, minimisation, classification de secret, masquage de données ou obligation runtime n’est prouvée.
- [x] 1.3 Ne déclarer que deux exports publics : `AuditEvent` et `validate_audit_event`.
- [x] 1.4 Définir `AuditEvent` comme `dataclass(frozen=True)` sans `__post_init__`, sans builder, sans exception publique et sans validation dans le constructeur.
- [x] 1.5 Déclarer exactement les treize champs du design, sans champ, défaut, alias, constructeur spécifique ou méthode applicative supplémentaire.
- [x] 1.6 Vérifier que la construction accepte structurellement des valeurs invalides, et que `validate_audit_event` reste le seul point fermé de validation.

## 2. Validation structurelle de l’événement

- [x] 2.1 Vérifier que `validate_audit_event(event: object)` retourne une liste fraîche de `Diagnostic`, neuve et indépendante à chaque appel.
- [x] 2.2 Exiger `type(event) is AuditEvent` avant toute lecture d’attribut et refuser une sous-classe sans accéder à ses champs.
- [x] 2.3 Vérifier qu’une entrée non exacte produit au plus un diagnostic d’élément et que les champs ne sont jamais inspectés.
- [x] 2.4 Agréger au maximum un refus par champ, sans diagnostic indexé par position dans un tuple ou par occurrence d’une valeur.
- [x] 2.5 Trier et dédupliquer les diagnostics selon `(element, constraint, message)` de façon stable, puis retourner la liste.
- [x] 2.6 Vérifier que chaque message est une contrainte statique nommant le champ et la règle, sans reproduire une valeur, un identifiant, un motif, un environnement, une cause technique ou un secret.

## 3. Chaînes opaques et valeurs optionnelles

- [x] 3.1 Valider chaque chaîne obligatoire opaque par `type(value) is str and bool(value)`, sans `strip()` ni normalisation.
- [x] 3.2 Vérifier qu’une chaîne composée uniquement d’espaces est acceptée comme référence opaque valide pour les champs concernés.
- [x] 3.3 Pour les champs obligatoires opaques, refuser `True`, `False`, `None`, `0`, une chaîne vide, un objet, une liste, un tuple et tout autre type non exact avant tout appel à `bool()`, `str()`, `len()` ou un callback de l’objet hostile.
- [x] 3.4 Autoriser `tenant_reference` et `reason_or_error` à être soit `None`, soit une chaîne exacte non vide.
- [x] 3.5 Vérifier qu’aucun vocabulaire n’est imposé pour `event_id`, `actor_reference`, `action`, `resource_type`, `resource_id`, `result`, `reason_or_error`, `tenant_reference` ou les références de corrélation.
- [x] 3.6 Vérifier l’absence de longueur maximale, quota, troncature, politique de minimisation, classification de secret ou validation d’un secret.

## 4. Horodatage UTC et calendrier réel

- [x] 4.1 Implémenter la grammaire UTC stricte `YYYY-MM-DDTHH:MM:SS[.fraction 1 à 6](Z | +00:00)` dans le module, sans importer de fonction privée.
- [x] 4.2 Vérifier les positions, séparateurs et chiffres ASCII ; `re` standard est permis pour la seule grammaire UTC locale, sans dupliquer les parseurs SemVer, puis refuser les bornes horaires, minutes et secondes invalides.
- [x] 4.3 Analyser le calendrier réel avec le `datetime.fromisoformat` standard et vérifier que le résultat possède un décalage UTC.
- [x] 4.4 Convertir uniquement une `ValueError` attendue de `datetime.fromisoformat` en diagnostic fixe sans écho de l’entrée.
- [x] 4.5 Propager toute exception inattendue issue de la validation de l’horodatage, sans capture générale.
- [x] 4.6 Dans les tests applicatifs, rendre la classe `datetime` patchable et vérifier réellement que le validateur appelle `fromisoformat`, y compris pour un cas calendaire, sans dépendre d’une assertion zéro E/S physique.
- [x] 4.7 Vérifier qu’aucune horloge système, aucun fuseau local et aucun environnement ne sont consultés par le comportement validé.

## 5. Composant, version et grammaires publiques

- [x] 5.1 Valider `component_id` avec `parse_requirement` public, en exigeant `constraints == ()` et `target_id == value`.
- [x] 5.2 Refuser un `component_id` avec comparateur, cible divergente, entrée vide, type inexistant ou forme invalide.
- [x] 5.3 Valider `component_version` avec `parse_version` public, sans imposer un sous-ensemble ou une grammaire parallèle.
- [x] 5.4 Convertir uniquement les `ValueError` attendues des deux parseurs publics en diagnostics fixes.
- [x] 5.5 Propager les erreurs inattendues des parseurs ou toute erreur de programmation, sans les transformer en refus normalisé.
- [x] 5.6 Vérifier qu’aucune fonction privée de `manifest.models` ou d’un autre module n’est utilisée pour les composants et versions.

## 6. Tuples de corrélation et de causalité

- [x] 6.1 Exiger pour `correlation_ids` et `causation_ids` des objets de type exactement `tuple`, avant toute itération, comparaison ou appel d’un objet hostile.
- [x] 6.2 Vérifier que chaque élément d’un tuple non vide est une chaîne de type exact `str` et non vide.
- [x] 6.3 Autoriser les tuples vides comme représentation syntaxiquement permise, sans en déduire une présence ou une absence d’obligation runtime.
- [x] 6.4 Conserver l’ordre et le contenu des éléments valides : aucun tri, aucune déduplication, aucune normalisation, aucune transformation et aucune modification de l’événement.
- [x] 6.5 Produire au plus un diagnostic par tuple en cas d’élément invalide, sans nommer la position ni reproduire la valeur.
- [x] 6.6 Vérifier qu’aucun format `UUID`, `traceparent`, `operation_id`, acteur, tenant ou ressource n’est inventé pour les identifiants de corrélation et de causalité.

## 7. Tests unitaires sûrs

- [x] 7.1 Publier exactement `tests/unit/test_audit_event.py` comme première source de tests du module.
- [x] 7.2 Vérifier l’absence d’autres exports publics, la présence des deux exports prévus et la docstring de confiance caller/synthétique.
- [x] 7.3 Couvrir la structure immuable du modèle : treize champs exacts, absence de `__post_init__` et absence de validation par le constructeur.
- [x] 7.4 Couvrir les chaînes opaques valides et hostiles, notamment les chaînes d’espaces et le refus des booléens exacts avant tout callback.
- [x] 7.5 Couvrir les valeurs `None` admises uniquement pour les champs prévus.
- [x] 7.6 Couvrir l’horodatage UTC valide, les bornes invalides, le calendrier réel via la classe `datetime` patchable et la propagation d’une erreur inattendue.
- [x] 7.7 Couvrir les grammaires publiques de `component_id` et `component_version`, avec refus par diagnostic fixe sans écho.
- [x] 7.8 Couvrir les tuples vides, les tuples valides, les éléments invalides, la conservation d’ordre et l’absence de mutation ou déduplication.
- [x] 7.9 Couvrir le diagnostic exact d’un objet incorrect ou d’une sous-classe, sans lecture des champs hostiles.
- [x] 7.10 Couvrir la fraîcheur de la liste, le tri/déduplication stable et l’absence de valeur dans les messages.

## 8. Intégration sûre en processus frais

- [x] 8.1 Publier exactement `tests/integration/test_audit_event_integration.py`, sans créer `tests/integration/test_audit_event.py`.
- [x] 8.2 Installer dans le processus frais des sondes réelles contre les accès fichiers/environnement, l’horloge système, les sockets, les subprocess et les imports de couche base, éprouver chaque route (compteur 1), puis remettre les compteurs à zéro avant les phases applicatives. Vérifier zéro après chaque phase sans masquer un accès applicatif par une remise à zéro.
- [x] 8.3 Autoriser les imports Bootstrap nécessaires au module et à ses dépendances, sans exiger une absence théorique absolue de toute activité physique d’import.
- [x] 8.4 Importer et valider des événements représentatifs dans le sous-processus, incluant les cas horodatage, composants et tuples.
- [x] 8.5 Vérifier qu’aucun accès applicatif interdit n’est observé pendant la validation après l’armement effectif des sondes.
- [x] 8.6 Limiter la sortie du subprocess à un marqueur fixe et ne jamais reproduire de valeur, diagnostic brut, environnement ou secret.
- [x] 8.7 Propager ou diagnostiquer explicitement toute erreur inattendue du subprocess, sans capture générale ni masque de l’échec initial.

## 9. Compilations natives et exécution des tests

- [x] 9.1 Compiler nativement `src/pixs/kernel/audit_event.py` avec un mandat distinct et vérifier son exit réel.
- [x] 9.2 Compiler nativement `tests/unit/test_audit_event.py` avec un mandat distinct et vérifier son exit réel.
- [x] 9.3 Compiler nativement `tests/integration/test_audit_event_integration.py` avec un mandat distinct et vérifier son exit réel.
- [x] 9.4 Exécuter les tests unitaires ciblés du module et vérifier leur exit réel ainsi que leur output complet.
- [x] 9.5 Exécuter le test d’intégration ciblé et vérifier son exit réel ainsi que son output complet.
- [x] 9.6 Exécuter la suite de 192 tests sûrs existante, sans PG réel supplémentaire, pour préserver les comportements fanions, backend et source PostgreSQL déjà acquis.
- [x] 9.7 Exécuter les tests directement concernés des dépendances : `tests/unit/test_semver_constraints.py`, `tests/unit/test_manifest_models.py` et `tests/unit/test_diagnostics_typed.py`.
- [x] 9.8 Vérifier que les ajouts de tests sont déterminés par les comportements réellement prouvés, sans ajouter un nombre ou une longueur imposé arbitrairement.

## 10. Périmètre, encodage et conformité OpenSpec

- [x] 10.1 Vérifier que le périmètre exact comprend trois nouveaux chemins de code/tests et aucun autre fichier source, test ou configuration modifié.
- [x] 10.2 Vérifier que les cinquante-deux fichiers de baseline prévus restent inchangés, y compris les quarante-neuf fichiers existants et les trois modules de tests dépendants.
- [x] 10.3 Vérifier l’encodage UTF-8 et les fins de ligne LF des trois nouveaux fichiers, sans contenu CRLF ni secret.
- [x] 10.4 Vérifier que le delta normatif est la copie byte exact de la seule norme canonique `audit` « Contenu minimal d’un événement d’audit », y compris son Scenario, sans norme nouvelle, modifiée ou supprimée.
- [x] 10.5 Vérifier l’absence de nouvelle dépendance, de package exporté, de README modifié, de Git, de wire format, de persistance, de route, d’API, de panneau admin, de PG réel supplémentaire et de politique d’audit.
- [x] 10.6 Exécuter la validation OpenSpec stricte du change avant cochage.
- [x] 10.7 Exécuter la validation OpenSpec stricte canonique concernée avant cochage.
- [x] 10.8 Vérifier qu’aucune tâche n’est cochée avant preuve observable de son exécution réussie.

Note de séquence : après tous les cochages, exécuter la validation stricte post-cochage ; obtenir ensuite une autorisation d’archivage unitaire distincte, exécuter l’archive, puis produire et vérifier séparément `STATISTIQUES.md` avec ses six sections, UTF-8/LF, totaux croisés et mesures `N/A` motivées. L’archivage et le rapport statistique ne constituent pas des tâches pré-cochage du souscycle.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

Preuves et constats conservés dans le présent fichier : « 2. Validation structurelle de l’événement ».

### C56-SL01 — Publier exactement `src/pixs/kernel/audit_event.py` comme module pur du Kernel, sans aucune autre source applicative ajoutée ou modifiée.

- Ancien repère et tâche rattachée : tâche 1.1 ; section « 1. Publication du module de représentation », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL02 — Écrire une docstring de module indiquant que les valeurs sont fournies par un caller trusted ou des fixtures synthétiques, que la validation est structurelle et qu’aucune persistance, minimisation, classification de secret, masquage de données ou obligation runtime n’est prouvée.

- Ancien repère et tâche rattachée : tâche 1.2 ; section « 1. Publication du module de représentation », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL03 — Ne déclarer que deux exports publics : `AuditEvent` et `validate_audit_event`.

- Ancien repère et tâche rattachée : tâche 1.3 ; section « 1. Publication du module de représentation », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL04 — Définir `AuditEvent` comme `dataclass(frozen=True)` sans `__post_init__`, sans builder, sans exception publique et sans validation dans le constructeur.

- Ancien repère et tâche rattachée : tâche 1.4 ; section « 1. Publication du module de représentation », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL05 — Déclarer exactement les treize champs du design, sans champ, défaut, alias, constructeur spécifique ou méthode applicative supplémentaire.

- Ancien repère et tâche rattachée : tâche 1.5 ; section « 1. Publication du module de représentation », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL06 — Vérifier que la construction accepte structurellement des valeurs invalides, et que `validate_audit_event` reste le seul point fermé de validation.

- Ancien repère et tâche rattachée : tâche 1.6 ; section « 1. Publication du module de représentation », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL07 — Vérifier que `validate_audit_event(event: object)` retourne une liste fraîche de `Diagnostic`, neuve et indépendante à chaque appel.

- Ancien repère et tâche rattachée : tâche 2.1 ; section « 2. Validation structurelle de l’événement », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL08 — Exiger `type(event) is AuditEvent` avant toute lecture d’attribut et refuser une sous-classe sans accéder à ses champs.

- Ancien repère et tâche rattachée : tâche 2.2 ; section « 2. Validation structurelle de l’événement », ligne 15 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL09 — Vérifier qu’une entrée non exacte produit au plus un diagnostic d’élément et que les champs ne sont jamais inspectés.

- Ancien repère et tâche rattachée : tâche 2.3 ; section « 2. Validation structurelle de l’événement », ligne 16 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL10 — Agréger au maximum un refus par champ, sans diagnostic indexé par position dans un tuple ou par occurrence d’une valeur.

- Ancien repère et tâche rattachée : tâche 2.4 ; section « 2. Validation structurelle de l’événement », ligne 17 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL11 — Trier et dédupliquer les diagnostics selon `(element, constraint, message)` de façon stable, puis retourner la liste.

- Ancien repère et tâche rattachée : tâche 2.5 ; section « 2. Validation structurelle de l’événement », ligne 18 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL12 — Vérifier que chaque message est une contrainte statique nommant le champ et la règle, sans reproduire une valeur, un identifiant, un motif, un environnement, une cause technique ou un secret.

- Ancien repère et tâche rattachée : tâche 2.6 ; section « 2. Validation structurelle de l’événement », ligne 19 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL13 — Valider chaque chaîne obligatoire opaque par `type(value) is str and bool(value)`, sans `strip()` ni normalisation.

- Ancien repère et tâche rattachée : tâche 3.1 ; section « 3. Chaînes opaques et valeurs optionnelles », ligne 23 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL14 — Vérifier qu’une chaîne composée uniquement d’espaces est acceptée comme référence opaque valide pour les champs concernés.

- Ancien repère et tâche rattachée : tâche 3.2 ; section « 3. Chaînes opaques et valeurs optionnelles », ligne 24 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL15 — Pour les champs obligatoires opaques, refuser `True`, `False`, `None`, `0`, une chaîne vide, un objet, une liste, un tuple et tout autre type non exact avant tout appel à `bool()`, `str()`, `len()` ou un callback de l’objet hostile.

- Ancien repère et tâche rattachée : tâche 3.3 ; section « 3. Chaînes opaques et valeurs optionnelles », ligne 25 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL16 — Autoriser `tenant_reference` et `reason_or_error` à être soit `None`, soit une chaîne exacte non vide.

- Ancien repère et tâche rattachée : tâche 3.4 ; section « 3. Chaînes opaques et valeurs optionnelles », ligne 26 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL17 — Vérifier qu’aucun vocabulaire n’est imposé pour `event_id`, `actor_reference`, `action`, `resource_type`, `resource_id`, `result`, `reason_or_error`, `tenant_reference` ou les références de corrélation.

- Ancien repère et tâche rattachée : tâche 3.5 ; section « 3. Chaînes opaques et valeurs optionnelles », ligne 27 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL18 — Vérifier l’absence de longueur maximale, quota, troncature, politique de minimisation, classification de secret ou validation d’un secret.

- Ancien repère et tâche rattachée : tâche 3.6 ; section « 3. Chaînes opaques et valeurs optionnelles », ligne 28 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL19 — Implémenter la grammaire UTC stricte `YYYY-MM-DDTHH:MM:SS[.fraction 1 à 6](Z | +00:00)` dans le module, sans importer de fonction privée.

- Ancien repère et tâche rattachée : tâche 4.1 ; section « 4. Horodatage UTC et calendrier réel », ligne 32 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL20 — Vérifier les positions, séparateurs et chiffres ASCII ; `re` standard est permis pour la seule grammaire UTC locale, sans dupliquer les parseurs SemVer, puis refuser les bornes horaires, minutes et secondes invalides.

- Ancien repère et tâche rattachée : tâche 4.2 ; section « 4. Horodatage UTC et calendrier réel », ligne 33 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL21 — Analyser le calendrier réel avec le `datetime.fromisoformat` standard et vérifier que le résultat possède un décalage UTC.

- Ancien repère et tâche rattachée : tâche 4.3 ; section « 4. Horodatage UTC et calendrier réel », ligne 34 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL22 — Convertir uniquement une `ValueError` attendue de `datetime.fromisoformat` en diagnostic fixe sans écho de l’entrée.

- Ancien repère et tâche rattachée : tâche 4.4 ; section « 4. Horodatage UTC et calendrier réel », ligne 35 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL23 — Propager toute exception inattendue issue de la validation de l’horodatage, sans capture générale.

- Ancien repère et tâche rattachée : tâche 4.5 ; section « 4. Horodatage UTC et calendrier réel », ligne 36 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL24 — Dans les tests applicatifs, rendre la classe `datetime` patchable et vérifier réellement que le validateur appelle `fromisoformat`, y compris pour un cas calendaire, sans dépendre d’une assertion zéro E/S physique.

- Ancien repère et tâche rattachée : tâche 4.6 ; section « 4. Horodatage UTC et calendrier réel », ligne 37 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL25 — Vérifier qu’aucune horloge système, aucun fuseau local et aucun environnement ne sont consultés par le comportement validé.

- Ancien repère et tâche rattachée : tâche 4.7 ; section « 4. Horodatage UTC et calendrier réel », ligne 38 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL26 — Valider `component_id` avec `parse_requirement` public, en exigeant `constraints == ()` et `target_id == value`.

- Ancien repère et tâche rattachée : tâche 5.1 ; section « 5. Composant, version et grammaires publiques », ligne 42 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL27 — Refuser un `component_id` avec comparateur, cible divergente, entrée vide, type inexistant ou forme invalide.

- Ancien repère et tâche rattachée : tâche 5.2 ; section « 5. Composant, version et grammaires publiques », ligne 43 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL28 — Valider `component_version` avec `parse_version` public, sans imposer un sous-ensemble ou une grammaire parallèle.

- Ancien repère et tâche rattachée : tâche 5.3 ; section « 5. Composant, version et grammaires publiques », ligne 44 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL29 — Convertir uniquement les `ValueError` attendues des deux parseurs publics en diagnostics fixes.

- Ancien repère et tâche rattachée : tâche 5.4 ; section « 5. Composant, version et grammaires publiques », ligne 45 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL30 — Propager les erreurs inattendues des parseurs ou toute erreur de programmation, sans les transformer en refus normalisé.

- Ancien repère et tâche rattachée : tâche 5.5 ; section « 5. Composant, version et grammaires publiques », ligne 46 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL31 — Vérifier qu’aucune fonction privée de `manifest.models` ou d’un autre module n’est utilisée pour les composants et versions.

- Ancien repère et tâche rattachée : tâche 5.6 ; section « 5. Composant, version et grammaires publiques », ligne 47 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL32 — Exiger pour `correlation_ids` et `causation_ids` des objets de type exactement `tuple`, avant toute itération, comparaison ou appel d’un objet hostile.

- Ancien repère et tâche rattachée : tâche 6.1 ; section « 6. Tuples de corrélation et de causalité », ligne 51 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL33 — Vérifier que chaque élément d’un tuple non vide est une chaîne de type exact `str` et non vide.

- Ancien repère et tâche rattachée : tâche 6.2 ; section « 6. Tuples de corrélation et de causalité », ligne 52 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL34 — Autoriser les tuples vides comme représentation syntaxiquement permise, sans en déduire une présence ou une absence d’obligation runtime.

- Ancien repère et tâche rattachée : tâche 6.3 ; section « 6. Tuples de corrélation et de causalité », ligne 53 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL35 — Conserver l’ordre et le contenu des éléments valides : aucun tri, aucune déduplication, aucune normalisation, aucune transformation et aucune modification de l’événement.

- Ancien repère et tâche rattachée : tâche 6.4 ; section « 6. Tuples de corrélation et de causalité », ligne 54 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL36 — Produire au plus un diagnostic par tuple en cas d’élément invalide, sans nommer la position ni reproduire la valeur.

- Ancien repère et tâche rattachée : tâche 6.5 ; section « 6. Tuples de corrélation et de causalité », ligne 55 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL37 — Vérifier qu’aucun format `UUID`, `traceparent`, `operation_id`, acteur, tenant ou ressource n’est inventé pour les identifiants de corrélation et de causalité.

- Ancien repère et tâche rattachée : tâche 6.6 ; section « 6. Tuples de corrélation et de causalité », ligne 56 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL38 — Publier exactement `tests/unit/test_audit_event.py` comme première source de tests du module.

- Ancien repère et tâche rattachée : tâche 7.1 ; section « 7. Tests unitaires sûrs », ligne 60 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL39 — Vérifier l’absence d’autres exports publics, la présence des deux exports prévus et la docstring de confiance caller/synthétique.

- Ancien repère et tâche rattachée : tâche 7.2 ; section « 7. Tests unitaires sûrs », ligne 61 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL40 — Couvrir la structure immuable du modèle : treize champs exacts, absence de `__post_init__` et absence de validation par le constructeur.

- Ancien repère et tâche rattachée : tâche 7.3 ; section « 7. Tests unitaires sûrs », ligne 62 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL41 — Couvrir les chaînes opaques valides et hostiles, notamment les chaînes d’espaces et le refus des booléens exacts avant tout callback.

- Ancien repère et tâche rattachée : tâche 7.4 ; section « 7. Tests unitaires sûrs », ligne 63 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL42 — Couvrir les valeurs `None` admises uniquement pour les champs prévus.

- Ancien repère et tâche rattachée : tâche 7.5 ; section « 7. Tests unitaires sûrs », ligne 64 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL43 — Couvrir l’horodatage UTC valide, les bornes invalides, le calendrier réel via la classe `datetime` patchable et la propagation d’une erreur inattendue.

- Ancien repère et tâche rattachée : tâche 7.6 ; section « 7. Tests unitaires sûrs », ligne 65 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL44 — Couvrir les grammaires publiques de `component_id` et `component_version`, avec refus par diagnostic fixe sans écho.

- Ancien repère et tâche rattachée : tâche 7.7 ; section « 7. Tests unitaires sûrs », ligne 66 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL45 — Couvrir les tuples vides, les tuples valides, les éléments invalides, la conservation d’ordre et l’absence de mutation ou déduplication.

- Ancien repère et tâche rattachée : tâche 7.8 ; section « 7. Tests unitaires sûrs », ligne 67 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL46 — Couvrir le diagnostic exact d’un objet incorrect ou d’une sous-classe, sans lecture des champs hostiles.

- Ancien repère et tâche rattachée : tâche 7.9 ; section « 7. Tests unitaires sûrs », ligne 68 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL47 — Couvrir la fraîcheur de la liste, le tri/déduplication stable et l’absence de valeur dans les messages.

- Ancien repère et tâche rattachée : tâche 7.10 ; section « 7. Tests unitaires sûrs », ligne 69 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL48 — Publier exactement `tests/integration/test_audit_event_integration.py`, sans créer `tests/integration/test_audit_event.py`.

- Ancien repère et tâche rattachée : tâche 8.1 ; section « 8. Intégration sûre en processus frais », ligne 73 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL49 — Installer dans le processus frais des sondes réelles contre les accès fichiers/environnement, l’horloge système, les sockets, les subprocess et les imports de couche base, éprouver chaque route (compteur 1), puis remettre les compteurs à zéro avant les phases applicatives. Vérifier zéro après chaque phase sans masquer un accès applicatif par une remise à zéro.

- Ancien repère et tâche rattachée : tâche 8.2 ; section « 8. Intégration sûre en processus frais », ligne 74 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL50 — Autoriser les imports Bootstrap nécessaires au module et à ses dépendances, sans exiger une absence théorique absolue de toute activité physique d’import.

- Ancien repère et tâche rattachée : tâche 8.3 ; section « 8. Intégration sûre en processus frais », ligne 75 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL51 — Importer et valider des événements représentatifs dans le sous-processus, incluant les cas horodatage, composants et tuples.

- Ancien repère et tâche rattachée : tâche 8.4 ; section « 8. Intégration sûre en processus frais », ligne 76 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL52 — Vérifier qu’aucun accès applicatif interdit n’est observé pendant la validation après l’armement effectif des sondes.

- Ancien repère et tâche rattachée : tâche 8.5 ; section « 8. Intégration sûre en processus frais », ligne 77 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL53 — Limiter la sortie du subprocess à un marqueur fixe et ne jamais reproduire de valeur, diagnostic brut, environnement ou secret.

- Ancien repère et tâche rattachée : tâche 8.6 ; section « 8. Intégration sûre en processus frais », ligne 78 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL54 — Propager ou diagnostiquer explicitement toute erreur inattendue du subprocess, sans capture générale ni masque de l’échec initial.

- Ancien repère et tâche rattachée : tâche 8.7 ; section « 8. Intégration sûre en processus frais », ligne 79 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL55 — Compiler nativement `src/pixs/kernel/audit_event.py` avec un mandat distinct et vérifier son exit réel.

- Ancien repère et tâche rattachée : tâche 9.1 ; section « 9. Compilations natives et exécution des tests », ligne 83 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL56 — Compiler nativement `tests/unit/test_audit_event.py` avec un mandat distinct et vérifier son exit réel.

- Ancien repère et tâche rattachée : tâche 9.2 ; section « 9. Compilations natives et exécution des tests », ligne 84 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL57 — Compiler nativement `tests/integration/test_audit_event_integration.py` avec un mandat distinct et vérifier son exit réel.

- Ancien repère et tâche rattachée : tâche 9.3 ; section « 9. Compilations natives et exécution des tests », ligne 85 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL58 — Exécuter les tests unitaires ciblés du module et vérifier leur exit réel ainsi que leur output complet.

- Ancien repère et tâche rattachée : tâche 9.4 ; section « 9. Compilations natives et exécution des tests », ligne 86 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL59 — Exécuter le test d’intégration ciblé et vérifier son exit réel ainsi que son output complet.

- Ancien repère et tâche rattachée : tâche 9.5 ; section « 9. Compilations natives et exécution des tests », ligne 87 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL60 — Exécuter la suite de 192 tests sûrs existante, sans PG réel supplémentaire, pour préserver les comportements fanions, backend et source PostgreSQL déjà acquis.

- Ancien repère et tâche rattachée : tâche 9.6 ; section « 9. Compilations natives et exécution des tests », ligne 88 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL61 — Exécuter les tests directement concernés des dépendances : `tests/unit/test_semver_constraints.py`, `tests/unit/test_manifest_models.py` et `tests/unit/test_diagnostics_typed.py`.

- Ancien repère et tâche rattachée : tâche 9.7 ; section « 9. Compilations natives et exécution des tests », ligne 89 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL62 — Vérifier que les ajouts de tests sont déterminés par les comportements réellement prouvés, sans ajouter un nombre ou une longueur imposé arbitrairement.

- Ancien repère et tâche rattachée : tâche 9.8 ; section « 9. Compilations natives et exécution des tests », ligne 90 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL63 — Vérifier que le périmètre exact comprend trois nouveaux chemins de code/tests et aucun autre fichier source, test ou configuration modifié.

- Ancien repère et tâche rattachée : tâche 10.1 ; section « 10. Périmètre, encodage et conformité OpenSpec », ligne 94 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL64 — Vérifier que les cinquante-deux fichiers de baseline prévus restent inchangés, y compris les quarante-neuf fichiers existants et les trois modules de tests dépendants.

- Ancien repère et tâche rattachée : tâche 10.2 ; section « 10. Périmètre, encodage et conformité OpenSpec », ligne 95 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL65 — Vérifier l’encodage UTF-8 et les fins de ligne LF des trois nouveaux fichiers, sans contenu CRLF ni secret.

- Ancien repère et tâche rattachée : tâche 10.3 ; section « 10. Périmètre, encodage et conformité OpenSpec », ligne 96 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL66 — Vérifier que le delta normatif est la copie byte exact de la seule norme canonique `audit` « Contenu minimal d’un événement d’audit », y compris son Scenario, sans norme nouvelle, modifiée ou supprimée.

- Ancien repère et tâche rattachée : tâche 10.4 ; section « 10. Périmètre, encodage et conformité OpenSpec », ligne 97 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL67 — Vérifier l’absence de nouvelle dépendance, de package exporté, de README modifié, de Git, de wire format, de persistance, de route, d’API, de panneau admin, de PG réel supplémentaire et de politique d’audit.

- Ancien repère et tâche rattachée : tâche 10.5 ; section « 10. Périmètre, encodage et conformité OpenSpec », ligne 98 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL68 — Exécuter la validation OpenSpec stricte du change avant cochage.

- Ancien repère et tâche rattachée : tâche 10.6 ; section « 10. Périmètre, encodage et conformité OpenSpec », ligne 99 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL69 — Exécuter la validation OpenSpec stricte canonique concernée avant cochage.

- Ancien repère et tâche rattachée : tâche 10.7 ; section « 10. Périmètre, encodage et conformité OpenSpec », ligne 100 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### C56-SL70 — Vérifier qu’aucune tâche n’est cochée avant preuve observable de son exécution réussie.

- Ancien repère et tâche rattachée : tâche 10.8 ; section « 10. Périmètre, encodage et conformité OpenSpec », ligne 101 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : sections de preuves et constats du présent fichier citées ci-dessus.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
