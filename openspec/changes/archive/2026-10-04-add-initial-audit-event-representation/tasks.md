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
