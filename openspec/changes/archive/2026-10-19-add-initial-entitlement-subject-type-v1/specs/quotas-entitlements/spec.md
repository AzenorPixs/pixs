## ADDED Requirements

### Requirement: Quatre types de sujet d'entitlement explicites

Le profil MUST exposer EntitlementSubjectType comme une Enum passive sans mixin str, avec exactement INSTALLATION, PLATFORM, TENANT et SCOPE, dans cet ordre et avec une valeur identique au nom. Le module pixs.kernel.entitlement_subject_type MUST déclarer uniquement EntitlementSubjectType dans __all__, sans modifier la façade Kernel.

#### Scenario: Consultation des quatre sujets canoniques

- **WHEN** un consommateur importe le module public et consulte ou construit les quatre membres
- **THEN** il obtient les membres Enum et leurs valeurs exactes, avec un export explicite et une façade inchangée

### Requirement: Construction fermée sans normalisation du type de sujet

Une valeur non déclarée MUST être refusée sans normalisation ni alias. Ce vocabulaire MUST NOT être confondu avec les sept portées QuotaPolicy.subject_scope.

#### Scenario: Portée étrangère ou valeur altérée refusée

- **WHEN** le consommateur fournit IDENTITY, IP, OPERATION, USER, une casse différente, une valeur vide, un espace ajouté ou un type non admis
- **THEN** la construction est refusée sans normalisation ni admission implicite

### Requirement: Passivité du type de sujet d'entitlement

Le vocabulaire MUST NOT produire de persistance, appel de provider, accès Core, base, réseau, environnement, processus ou autre effet métier à l'import ou à son utilisation. Un membre MUST NOT déduire une admissibilité, un héritage, une autorisation ou une résolution.

#### Scenario: Import et utilisation sans effet métier

- **WHEN** le module est importé dans un processus frais puis ses membres sont utilisés sous gardes actives
- **THEN** aucun effet métier ni appel protégé n'est observé, les contrôles positifs prouvent les gardes et le membre SCOPE ne donne aucun droit

### Requirement: Limite structurelle sans modification des contrôles existants

Le profil MUST conserver les contrôles applicatifs existants, notamment l'exception Super Admin et l'absence d'élargissement par scope. Il MUST NOT constituer une preuve d'implémentation des droits ou quotas persistants.

#### Scenario: Vocabulaire seul disponible

- **WHEN** seul EntitlementSubjectType est livré
- **THEN** aucune résolution, réservation, persistance, hiérarchie ou permission ne peut être déduite de cette livraison et les exigences applicatives restent inchangées
