# Références normatives — O06

Copie contrôlée après reprise RSMP validée explicitement le 22 octobre 2026. Le canon demeure autorité. Les quatre exigences et cinq scénarios sont conservés et précisés par le profil v1. Les dispositions NE et l’audit du 17 octobre 2026 sont historiques : aucune preuve runtime n’est déduite de ces textes.

## Blocs canoniques complets et empreintes

### Règles métier séparées des contrôles de sécurité

Source : openspec/specs/business-rules/spec.md. SHA-256 UTF-8 du bloc exact : c043f03b3acc0e71b58aa51b1eac41f0d2beaeadae518e091ba56f8b8bfa537f.

~~~~text
### Requirement: Règles métier séparées des contrôles de sécurité

Une règle métier MUST déclarer son propriétaire, son contrat d'entrée, son
résultat et son contexte de version. Elle MUST NOT accorder une permission,
remplacer une décision du PDP ou contourner une garde de workflow.

#### Scenario: Règle invoquée pour une action protégée

- **WHEN** une règle recommande qu'une action soit applicable
- **THEN** l'autorisation et les gardes de workflow sont évaluées séparément

~~~~

### Déclarations versionnées et déterministes

Source : openspec/specs/business-rules/spec.md. SHA-256 UTF-8 du bloc exact : 3bc49d5a45d24c97bd4ecf5791a1fd35ed3956766eb69dde6177962aa2e61e01.

~~~~text
### Requirement: Déclarations versionnées et déterministes

Les règles, tables de décision et dépendances déclarées MUST être versionnées,
validées et évaluées de manière déterministe pour une même entrée et une même
version. Leur DSL MUST être déclaratif et restreint ; une règle MUST NOT
évaluer du code arbitraire au runtime. Une règle ambiguë, incomplète ou
incompatible MUST être refusée avant activation.

#### Scenario: Évaluation rejouée

- **WHEN** une même règle reçoit deux fois le même contexte versionné
- **THEN** elle produit le même résultat ou le même refus explicite

Pour le profil optionnel O06 JSON v1 adopté le 22 octobre 2026, le document MUST contenir exactement profile_version, rule_id, rule_version, owner, input_schema, expression et cases. profile_version MUST être l'entier exact 1 ; rule_id, rule_version et owner MUST être des chaînes non vides. input_schema MUST associer chaque nom non vide à un descripteur fermé {type, required}, où required est booléen et type appartient à null, boolean, integer, string, array. Les tableaux MUST contenir seulement ces valeurs récursivement, sans objet métier arbitraire ni float. Le booléen MUST rester distinct de l'entier, sans coercition.

La grammaire MUST fermer chaque expression sur {op, args}. all et any prennent une liste non vide d'expressions ; not exactement une expression. eq, ne, lt, lte, gt, gte, in prennent exactement deux opérandes ; exists prend exactement une référence de champ déclaré. Un opérande MUST être exactement {field: nom} ou {literal: valeur}. Un champ, opérateur, type ou référence non déclaré et une arité incorrecte MUST être refusés. Les entrées MUST refuser champs inconnus, champs obligatoires absents et types incompatibles. Un optional absent effectivement consommé hors exists MUST produire un refus explicite.

L'évaluation MUST être pure, sans I/O, réseau, fichier, horloge, hasard ni code arbitraire. all/any MUST parcourir les arguments dans l'ordre déclaré avec court-circuit dès que le résultat est déterminé. exists MUST vérifier seulement la présence d'un champ déclaré. eq/ne MUST refuser des types principaux différents et comparer les tableaux récursivement avec types exacts ; lt/lte/gt/gte MUST comparer uniquement deux entiers ou deux chaînes de même type. in MUST exiger un tableau à droite et comparer ses éléments par égalité stricte, sans confondre true et 1. Le résultat métier MUST être booléen. Un catalogue MUST associer explicitement owner/rule_id/rule_version à une définition immuable ; un contenu divergent pour une identité/version déjà activée MUST être refusé. Aucune table ou dépendance non déclarée n'est découverte ou activée implicitement.

#### Scenario: Expression exécutable proposée

- **WHEN** une règle contient du code ou une expression exécutable non déclarée par le DSL
- **THEN** sa validation échoue avant activation

Les documents JSON v1 de règle et d'entrée MUST être du UTF-8 strict, chacun de 65 536 octets au plus, de profondeur 8 au plus et de 256 nœuds au plus. La racine conteneur est au niveau 1 ; chaque conteneur enfant ajoute un niveau. Tout conteneur ou scalaire compte un nœud ; un nom de clé n'en compte pas. Les dépassements, clés dupliquées, Unicode invalide, floats et valeurs non JSON MUST être refusés avant l'activation ou l'évaluation concernée. La construction directe d'objets Python MUST NOT contourner ces garanties ni modifier une limite globale de l'interpréteur. Les erreurs MUST être typées, stables et sans valeur refusée recopiée.

~~~~

### Effets appliqués par le propriétaire métier

Source : openspec/specs/business-rules/spec.md. SHA-256 UTF-8 du bloc exact : 3efeb2c13a061e35fdaf6caffc33dd78d6bd4e9ea594022ccd4757186a9b54d8.

~~~~text
### Requirement: Effets appliqués par le propriétaire métier

Une évaluation de règle MUST produire une décision ou une proposition
structurée. Toute mutation consécutive MUST passer par une Command autorisée du
module propriétaire ; le moteur de règles MUST NOT écrire directement des
modèles ou données d'un autre composant.

#### Scenario: Décision conduisant à une mutation

- **WHEN** une règle produit une décision de transition métier
- **THEN** le module propriétaire la valide au travers de sa Command publique

Le DSL v1 MUST NOT muter les entrées, appeler une Command ou interpréter un nom exécutable. Le raccordement à la Command MUST être fourni explicitement par la composition propriétaire et MUST conserver la réévaluation courante des droits, gardes, version, tenant/scope et gouvernance. Ses refus et erreurs MUST être propagés sans effet confirmé inventé. Le profil MUST rester facultatif, sans activation P0 implicite, provider externe ou dépendance nouvelle ; sa réalisation utilise la bibliothèque standard Python existante.

~~~~

### Tests, explications et audit

Source : openspec/specs/business-rules/spec.md. SHA-256 UTF-8 du bloc exact : a2b91111f1902b9b478890f9a4cb7ee440621f988438f443f610ca0a73c1cc7e.

~~~~text
### Requirement: Tests, explications et audit

Chaque règle stable MUST disposer de cas de test versionnés. Le système MUST
conserver une explication corrélée de l'évaluation sans enregistrer de secret,
de donnée non nécessaire ou de détail privé de l'implémentation.

#### Scenario: Décision contestée

- **WHEN** un opérateur autorisé consulte une décision tracée
- **THEN** il obtient la version de règle et les motifs autorisés sans exposer le contexte sensible complet

Dans le profil v1, cases MUST être une liste non vide de cas fermés {case_id, inputs, expected} : identifiants non vides et uniques dans la version, entrées conformes et résultat attendu booléen. La syntaxe d'un cas MUST NOT valoir preuve de son exécution. Une règle stable MUST NOT être activée avant réussite de son corpus versionné.

Le résultat v1 MUST contenir exactement profile_version, rule_id, rule_version, owner, correlation_id, matched et reason_codes. La corrélation MUST être fournie explicitement par l'appelant ; matched est booléen et reason_codes porte des codes stables minimisés. À corrélation et contexte versionné identiques, résultat et refus MUST être reproductibles. Résultats et diagnostics MUST NOT recopier valeurs d'entrée, champs sensibles ou contexte complet. L'intégration MUST conserver l'explication sous les contrats d'audit, rétention et accès applicables ; sa consultation MUST être autorisée et une corrélation MUST NOT devenir un droit.
~~~~

## Preuves attendues

Chaque tâche de tasks.md conserve ses critères, commandes, résultats et scénarios. Le delta MODIFIED et le canon doivent porter les mêmes quatre blocs. La validation documentaire ne coche aucune tâche runtime et l’archivage ne réapplique pas un delta déjà synchronisé.

## Annexe O06 — Matrice de preuves des tâches 1 à 4 et du scénario exécutable

Sans modification des blocs normatifs ci-dessus. Bornes et scopes actuels conservés :
profil JSON v1 `65536 octets / 8 niveaux / 256 nœuds`, opérateurs
`all,any,not,eq,ne,lt,lte,gt,gte,in,exists`, résultats 7 champs
`profile_version,rule_id,rule_version,owner,correlation_id,matched,reason_codes`.
Composant provider `pixs.business-rules@1.0.0`, Core/Kernel `0.1.0`,
Django `6.1.2`, PostgreSQL `16.14` (server_version_num `160014`) prouvés. C09/C10 synthétiques déclarés par la
fixture C06, P0 absent, aucune UI.

- Unitaires : 95 natifs `call_01a16596b5eb72b3b5c1282e2c09d872`
  (profil 51 + moteur 34 + manifest 10), dépendances pures inchangées.
- Recette PG : 13/13 `call_01a165a15e9f7614859786657c49ed84`,
  `code NONE`, `real_pg/cleanup/conns_closed true`. Aucun retest sans invalidation.
- Scénario exécutable : six refus explicites avant activation, zéro activation, appel natif `call_01a165a718d374fca52ddef37d5815bf`.
- La décision d’éligibilité de la tâche 5 inclut séparément les contrôles OpenSpec stricts, UTF-8/LF, fidélité des blocs et périmètre. Cette annexe ne prouve ni activation P0 ni achèvement global.

| Exigence canon | Scénario canon | Preuves réelles |
| --- | --- | --- |
| 1. Règles métier séparées des contrôles de sécurité | Règle invoquée pour une action protégée | PG `favorable_sans_permission_refuse` (`DECISION_REFUSEE`, zéro mutation, proposition non commise), `droits_revoques_apres_proposition` (DENY ajouté après `PROPOSED`, erreur propriétaire exacte propagée, `PROPOSED` resté commis) |
| 2. Déclarations versionnées et déterministes | Évaluation rejouée | Unit profil 51 + moteur 34 : parse/validate bornés, `bool≠int`, entiers longs, Unicode, rejeu résultat/refus stable sans mutation |
| 2. Déclarations versionnées et déterministes | Expression exécutable proposée | Profil fermé : refus des opérateurs eval, exec, python et import, d’un champ code et d’un opérande code ; six refus typés avant activation, appel natif `call_01a165a718d374fca52ddef37d5815bf`. Compléments : unitaires du profil inconnus/types/structures et revue de pureté du moteur. |
| 3. Effets appliqués par le propriétaire métier | Décision conduisant à une mutation | PG `command_reelle_et_proposition_durable` (`create-user` réelle, `CoreMutationResult`, `CoreUser` peer, `PROPOSED` durable 7 champs, rétention>0, sans inputs/token), `resultat_false_sans_command` (`matched false` sans dispatch mais `PROPOSED`), `version_proprietaire_courante` (`CONFLIT_CAS` réel), erreur identique propagée, `transaction_externe_refusee` |
| 4. Tests, explications et audit | Décision contestée | Corpus catalogue unitaire + PG `lecture_audit_autorisee` (`filter_audit` réel, 7 champs, minimisé), `correlation_sans_droit` (`DECISION_REFUSEE`), `lecture_contexte_etranger_refusee`, `pseudonymisation_et_retention`, `audit_indisponible_sans_mutation` (`AUDIT_CAPACITY`), `explication_effacee_refusee` (`explanation_redacted`), `isolation_tenant_et_scope` |

### Artefacts relus et empreintes SHA-256

Les révisions des entrées communes de la recette PostgreSQL sont inchangées ; l’avance de la ressource logique de schéma correspond à notre test terminé et nettoyé. La modification de core_binding après les unitaires n’affecte pas leurs imports purs. Ces constats bornent les preuves au profil testé.

| Artefact | SHA-256 |
| --- | --- |
| src/pixs/business_rules/json_contract.py | 788419466c68e9e92381868e42bff5b210b45ba62bab5039ca0a2dd3b3c484c3 |
| src/pixs/business_rules/profile.py | d9ab89052eb33bd17536133e1a729ea56711259b4c88fbf275d7dd8b97807e57 |
| src/pixs/business_rules/evaluator.py | 5b3d4f0dbbe4af441d726d523c631e7dc7ee7a80acdb8cb70d527bd369ca1a1c |
| src/pixs/business_rules/__init__.py | 9828bc22cb6a038735a8fa589c75ea77b18644216234b37a5ee31cd80868446e |
| tests/unit/test_business_rules_profile.py | eca12d76962cbfc7011d2654d0162947360df4e0d81161a7b3a97477a2eedd88 |
| tests/unit/test_business_rules_evaluator.py | eca1bcbc5de1fb6924fdc36bb1613cf242eb78ce58873c8537ef1d1cd85f7281 |
| src/pixs/business_rules/core_binding.py | 908986b04587b47f924fffb78324ae329e427f42a06e36c1a54309d5f42e099a |
| src/pixs/business_rules/manifest.py | d324dc9a072aea0b64b8ec3a9bededd6650ce7849171b78145cfbbc414f52abe |
| tests/unit/test_business_rules_manifest.py | ba12fcb1deb22bf5a32fc88c8e982e3e70425de3fa7fdb13634e1c261ccb31b3 |
| tests/integration/test_business_rules_pg.py | 51c7f4ec55032f5bca0c7b94fd9111a26a9f302290abffee81db4f9060a8d722 |
