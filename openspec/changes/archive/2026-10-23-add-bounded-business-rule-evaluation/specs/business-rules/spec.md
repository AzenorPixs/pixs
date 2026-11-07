# business-rules — précisions O06 v1 adoptées le 22 octobre 2026

## MODIFIED Requirements

### Requirement: Règles métier séparées des contrôles de sécurité

Une règle métier MUST déclarer son propriétaire, son contrat d'entrée, son
résultat et son contexte de version. Elle MUST NOT accorder une permission,
remplacer une décision du PDP ou contourner une garde de workflow.

#### Scenario: Règle invoquée pour une action protégée

- **WHEN** une règle recommande qu'une action soit applicable
- **THEN** l'autorisation et les gardes de workflow sont évaluées séparément

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

### Requirement: Effets appliqués par le propriétaire métier

Une évaluation de règle MUST produire une décision ou une proposition
structurée. Toute mutation consécutive MUST passer par une Command autorisée du
module propriétaire ; le moteur de règles MUST NOT écrire directement des
modèles ou données d'un autre composant.

#### Scenario: Décision conduisant à une mutation

- **WHEN** une règle produit une décision de transition métier
- **THEN** le module propriétaire la valide au travers de sa Command publique

Le DSL v1 MUST NOT muter les entrées, appeler une Command ou interpréter un nom exécutable. Le raccordement à la Command MUST être fourni explicitement par la composition propriétaire et MUST conserver la réévaluation courante des droits, gardes, version, tenant/scope et gouvernance. Ses refus et erreurs MUST être propagés sans effet confirmé inventé. Le profil MUST rester facultatif, sans activation P0 implicite, provider externe ou dépendance nouvelle ; sa réalisation utilise la bibliothèque standard Python existante.

### Requirement: Tests, explications et audit

Chaque règle stable MUST disposer de cas de test versionnés. Le système MUST
conserver une explication corrélée de l'évaluation sans enregistrer de secret,
de donnée non nécessaire ou de détail privé de l'implémentation.

#### Scenario: Décision contestée

- **WHEN** un opérateur autorisé consulte une décision tracée
- **THEN** il obtient la version de règle et les motifs autorisés sans exposer le contexte sensible complet

Dans le profil v1, cases MUST être une liste non vide de cas fermés {case_id, inputs, expected} : identifiants non vides et uniques dans la version, entrées conformes et résultat attendu booléen. La syntaxe d'un cas MUST NOT valoir preuve de son exécution. Une règle stable MUST NOT être activée avant réussite de son corpus versionné.

Le résultat v1 MUST contenir exactement profile_version, rule_id, rule_version, owner, correlation_id, matched et reason_codes. La corrélation MUST être fournie explicitement par l'appelant ; matched est booléen et reason_codes porte des codes stables minimisés. À corrélation et contexte versionné identiques, résultat et refus MUST être reproductibles. Résultats et diagnostics MUST NOT recopier valeurs d'entrée, champs sensibles ou contexte complet. L'intégration MUST conserver l'explication sous les contrats d'audit, rétention et accès applicables ; sa consultation MUST être autorisée et une corrélation MUST NOT devenir un droit.
