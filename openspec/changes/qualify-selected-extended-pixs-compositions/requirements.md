# Références normatives — Q01

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| testing | Trois niveaux de vérification distincts | 1 | testing-80cd79b262db |
| testing | Kit de conformité et composant d'exemple | 1 | testing-58168e595c5f |
| testing | Suites de conformité versionnées par contrat | 1 | testing-e39b8c953ee7 |
| testing | Garanties obligatoires séparées des capacités optionnelles | 1 | testing-d36328278c75 |
| testing | Reproductibilité sur la topologie de référence | 1 | testing-5c9a87774d44 |
| testing | Preuves sans secret ni donnée de production | 1 | testing-039da2f8bc2c |
| testing | Conformité de la composition frontend récursive | 1 | testing-943792eb6f1f |
| testing | Conformité des projections d'annuaire optionnelles | 1 | testing-6604920280fd |
| testing | Exécution navigateur headless des unités frontend web | 2 | testing-121a020f91da |
| reference-composition | Qualification du binaire commun et des profils de ressources P0 | 4 | reference-composition-7131b276f78e |
| reference-composition | Capacités obligatoires du P0 | 1 | reference-composition-0af0b6011293 |
| reference-composition | Capacités hors P0 explicites | 1 | reference-composition-986398c06367 |
| reference-composition | Preuve reproductible | 1 | reference-composition-ab553efe6c54 |
| reference-composition | Profil initial PBO PFO Debian local v1 | 2 | reference-composition-5f1322f3cd28 |
| reference-composition | Garanties du socle conservées dans le profil initial | 1 | reference-composition-70063af8e7b7 |
| reference-composition | Parcours installable et utilisable du profil initial | 1 | reference-composition-2614801b7609 |
| reference-composition | Capacités non sélectionnées du profil initial | 1 | reference-composition-ef9b2d25c156 |
| reference-composition | Preuve de la composition effectivement distribuée | 1 | reference-composition-7961b985d4cc |
| reference-composition | Choix C01 systemd et exception d’amorçage du profil Debian local | 2 | reference-composition-80e3d17e557d |
| reference-composition | Qualification et source de vérité après amorçage | 2 | reference-composition-b86766ab642e |
| reference-composition | Profil Auth standard sans connecteur externe installé | 2 | reference-composition-fa2727180f3d |
| reference-composition | Composition ZT initiale et Domaines | 1 | reference-composition-4f43b97aaed5 |
| pixs-domains | Identité et FQDN explicites | 1 | pixs-domains-02f0f83aed5e |
| pixs-domains | ZT obligatoire dédié ou partagé | 2 | pixs-domains-686f4e13ff70 |
| pixs-domains | Isolation dans un ZT partagé | 1 | pixs-domains-bd2991264b73 |
| pixs-domains | Services minimaux par Domaine | 1 | pixs-domains-c9ce061e2b23 |
| pixs-domains | Tenants et propriété des ressources | 2 | pixs-domains-784b3416b755 |
| pixs-domains | Individus et identités multiples | 1 | pixs-domains-8e5157150f7c |
| pixs-domains | Transferts fonctionnels contrôlés V1 | 1 | pixs-domains-ba4dfa97bf7d |
| pixs-domains | Structures organisationnelles non transférables V1 | 1 | pixs-domains-2d4b91559aa3 |
| pixs-domains | Retrait du premier Domaine | 1 | pixs-domains-f9d0dad1d882 |
| pixs-domains | Approbations internes et externes | 1 | pixs-domains-94814997f512 |
| pixs-domains | Références PG et services de Domaine en mode normal ou critique | 1 | pixs-domains-d8fce09ab784 |
| organization-charts | Trois référentiels propriétaires | 1 | organization-charts-c0cec12f0548 |
| organization-charts | Hiérarchie structurelle et affiliations | 1 | organization-charts-43a3193484d2 |
| organization-charts | Source explicite de chaque miroir | 1 | organization-charts-8369220fda62 |
| organization-charts | Structure seule par défaut | 1 | organization-charts-3f5fd5146131 |
| organization-charts | Admission et droits séparés du miroir | 1 | organization-charts-a06107e07b95 |
| brick-redundancy | Remplacement sans déplacement direct | 1 | brick-redundancy-ce67ff7e1fde |
| brick-redundancy | Mode par famille et exceptions | 1 | brick-redundancy-78e23fa4ab8f |
| brick-redundancy | Conditions de reprise propres à la brique | 1 | brick-redundancy-29e8a1e997e2 |
| brick-redundancy | Unicité de l’autorité et automatisation | 1 | brick-redundancy-b7eb34bb70c2 |
| brick-redundancy | Observation et démantèlement | 1 | brick-redundancy-8df77aef5446 |
| brick-redundancy | Compatibilité de versions par famille | 1 | brick-redundancy-73cbc72a8e34 |
| brick-redundancy | Références PostgreSQL répliquées et garanties conservées | 1 | brick-redundancy-9c403ec6ed51 |
| managed-device-policies | Cibles V1 et exécutants locaux | 1 | managed-device-policies-8a43d725b9c8 |
| managed-device-policies | Gestion ZT et jonction d’authentification distinctes | 1 | managed-device-policies-f3d868c20f8b |
| managed-device-policies | Politiques communes et spécifiques | 1 | managed-device-policies-0fc04bee903f |
| managed-device-policies | Priorités et contradictions | 1 | managed-device-policies-a7f801c0bbd9 |
| managed-device-policies | Application par PA et état vérifié | 1 | managed-device-policies-fc87e0db8071 |
| managed-device-policies | Session hors ligne bornée | 1 | managed-device-policies-53ac3cf3063d |
| managed-device-policies | Rotation des secrets machine et services | 1 | managed-device-policies-0e3d3ee17150 |
| managed-device-policies | Redémarrage par profil et conclusion après reprise | 1 | managed-device-policies-0a228d3c9bf5 |

### Référence courante testing-80cd79b262db

Source : [testing](../../specs/testing/spec.md), ligne 8. SHA-256 : `80cd79b262db211694774e16f8ed675227919c38ef9d1862fb8a9035fac0760b`.

Scénarios : Unitaires verts, intégration rouge.

~~~~text
### Requirement: Trois niveaux de vérification distincts

Le projet MUST distinguer les tests unitaires des comportements internes, les tests d'intégration des compositions et des dépendances réelles de référence, et les tests de conformité des contrats publiés ; le succès d'un niveau MUST NOT tenir lieu de preuve pour un autre.

#### Scenario: Unitaires verts, intégration rouge

- **WHEN** des tests unitaires réussissent alors qu'un test d'intégration de composition échoue
- **THEN** la release est considérée non valide et l'échec d'intégration est rapporté explicitement
~~~~

### Référence courante testing-58168e595c5f

Source : [testing](../../specs/testing/spec.md), ligne 17. SHA-256 : `58168e595c5f67539e8bd6e7df750ef0b24d712cc11f6474c341d148f64ba8da`.

Scénarios : Exemple P0 validé.

~~~~text
### Requirement: Kit de conformité et composant d'exemple

Le Developer Kit MUST fournir des validateurs et suites de conformité
versionnés pour les manifests, contrats et composants déclarés compatibles. Un
composant d'exemple P0 MUST démontrer la composition par contrats, le contexte
tenant/scope et l'autorisation ; il MUST NOT devenir une dépendance de
production.

#### Scenario: Exemple P0 validé

- **WHEN** le composant d'exemple est validé par le Developer Kit
- **THEN** les preuves indiquent les versions de contrats et les contrôles P0 exécutés
~~~~

### Référence courante testing-e39b8c953ee7

Source : [testing](../../specs/testing/spec.md), ligne 30. SHA-256 : `e39b8c953ee7d94cfe2a82b02eb3861ed9d722fd0f45ef1308e5c4b76721a989`.

Scénarios : Certification expirée.

~~~~text
### Requirement: Suites de conformité versionnées par contrat

Chaque contrat de fournisseur MUST disposer d'une suite de conformité versionnée, indépendante de la technologie implémentée ; le runtime MUST NOT déclarer compatible un provider dont la conformité obligatoire est absente, expirée ou échouée.

#### Scenario: Certification expirée

- **WHEN** un provider présente une preuve de conformité expirée pour sa version déclarée
- **THEN** il est exclu de la sélection tant qu'une nouvelle exécution de la suite ne réussit pas
~~~~

### Référence courante testing-d36328278c75

Source : [testing](../../specs/testing/spec.md), ligne 39. SHA-256 : `d36328278c755b37406a5e622e90fa37830a6eced09cc942616a9a727ff1ba7d`.

Scénarios : Isolement acceptable.

~~~~text
### Requirement: Garanties obligatoires séparées des capacités optionnelles

Les tests MUST distinguer les garanties obligatoires des capacités optionnelles : une capacité optionnelle absente ou indisponible peut produire un état dégradé ou désactivé si elle reste isolée ; une incompatibilité de contrat, une ambiguïté de fournisseur, un défaut d'isolation de tenant ou une violation de sécurité MUST bloquer l'activation.

#### Scenario: Isolement acceptable

- **WHEN** une capacité optionnelle tombe sans fuite d'accès ni perte de donnée
- **THEN** l'état dégradé est accepté et diagnostiqué alors que le socle reste actif
~~~~

### Référence courante testing-5c9a87774d44

Source : [testing](../../specs/testing/spec.md), ligne 48. SHA-256 : `5c9a87774d4470bf5f6841e39716eac35717003f1a96035eed8b40c2bea9127e`.

Scénarios : Divergence de topologie.

~~~~text
### Requirement: Reproductibilité sur la topologie de référence

Les tests MUST être exécutables sur la topologie de référence du projet et sur toute topologie isolée déclarée compatible ; une différence de topologie MUST NOT modifier silencieusement les règles d'autorisation, de partage, de projection ou de suppression.

#### Scenario: Divergence de topologie

- **WHEN** un test d'invariant de périmètre produit un résultat différent selon la topologie
- **THEN** l'écart est bloquant et la topologie concernée perd sa mention de compatibilité
~~~~

### Référence courante testing-039da2f8bc2c

Source : [testing](../../specs/testing/spec.md), ligne 57. SHA-256 : `039da2f8bc2c7813607be8b8461e2ae623cee2da0496085c523ff7c83b51e9f3`.

Scénarios : Secret détecté dans un rapport.

~~~~text
### Requirement: Preuves sans secret ni donnée de production

Les fixtures, exemples et rapports produits par les tests MUST être synthétiques et reproductibles, sans secret, sans token et sans donnée de production ; les rapports MUST NOT exposer de détail exploitable.

#### Scenario: Secret détecté dans un rapport

- **WHEN** un artefact de test contient une valeur sensible réelle ou apparentée
- **THEN** le rapport est invalidé, la fuite est signalée et l'exécution est bloquante pour la publication
~~~~

### Référence courante testing-943792eb6f1f

Source : [testing](../../specs/testing/spec.md), ligne 66. SHA-256 : `943792eb6f1f8e6bb073fc42d79baa3a9c4ed3b7a7c5233b9cd3c8ebc19cfd3d`.

Scénarios : Composition reproductible avec sous-module.

~~~~text
### Requirement: Conformité de la composition frontend récursive

Les suites de conformité MUST vérifier la résolution récursive des modules et sous-modules frontend, la propriété des contributions, les dépendances publiques, les contraintes SemVer, les collisions, les modes obligatoire et optionnel, ainsi que l'équivalence de composition entre développement et artefacts distribués. Une résolution frontend MUST NOT dépendre de l'ordre des imports, du filesystem ou d'un code distant runtime.

#### Scenario: Composition reproductible avec sous-module

- **WHEN** la même composition incluant un module et un sous-module frontend est construite deux fois
- **THEN** les contributions actives, l'ordre de chargement et les diagnostics produits sont identiques
~~~~

### Référence courante testing-6604920280fd

Source : [testing](../../specs/testing/spec.md), ligne 75. SHA-256 : `6604920280fdee4ad9e71d6cef9d6576c30c1fa5efa9ba06157d6f7d21745c65`.

Scénarios : Repli conforme sans élargissement de droits.

~~~~text
### Requirement: Conformité des projections d'annuaire optionnelles

Les suites de conformité MUST vérifier le mapping versionné, la projection
sortante idempotente, la reprise, les suppressions propagées, l'isolation de
tenant et de scope, la fraîcheur après mutation, le repli PostgreSQL et l'état
DEGRADED d'un provider LDAP indisponible. Elles MUST vérifier que LDAP ne peut
ni écrire dans Pixs, ni fournir une ACL, une décision d'autorisation, une
révocation ou une authentification par cette capacité.

#### Scenario: Repli conforme sans élargissement de droits

- **WHEN** LDAP devient indisponible pendant une consultation autorisée
- **THEN** la suite confirme la réponse PostgreSQL, l'état DEGRADED et l'absence de divulgation ou de droit supplémentaire
~~~~

### Référence courante testing-121a020f91da

Source : [testing](../../specs/testing/spec.md), ligne 89. SHA-256 : `121a020f91da796da68634e9f74a654ebc2160b8922ae90a777a642f3d3fe310`.

Scénarios : Les deux moteurs déclarent les cas; Moteur manquant ou cas non exécuté.

~~~~text
### Requirement: Exécution navigateur headless des unités frontend web

Les tests unitaires de la partie frontend web MUST être exécutés dans tous les
navigateurs déclarés par DEVOPS.md, en mode headless ; le succès de ces tests
uniquement sous Node MUST NOT tenir lieu de preuve de cette exigence.

#### Scenario: Les deux moteurs déclarent les cas

- **WHEN** `npm --prefix frontend test` s'exécute sur un environnement
  déclarant Chromium et Firefox headless
- **THEN** chaque cas unitaire frontend reçoit une preuve d'exécution issue de
  chaque navigateur déclaré et le résultat global n'est vert qu'avec les deux
  moteurs

#### Scenario: Moteur manquant ou cas non exécuté

- **WHEN** un navigateur déclaré est indisponible, ne répond pas dans les
  bornes, ou n'exécute pas l'intégralité des cas
- **THEN** l'exécution est en échec diagnostiqué, sans substitution par le
  seul résultat Node ou par la réussite du build
~~~~

### Référence courante reference-composition-7131b276f78e

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 10. SHA-256 : `7131b276f78ec528ebd8d3dc65dca30cc41d7a9b3f3ae193754cb02b3e8ea9e6`.

Scénarios : Garanties de qualification du parcours initial PA PZT; P0 sans exécution réseau; P0 sans réseau distant; Plan de ressources sans preuve sur cible.

~~~~text
### Requirement: Qualification du binaire commun et des profils de ressources P0

Le profil initial PBO MUST qualifier le binaire commun Kernel/Core/Auth/Agent/PZT et ses ressources selon reference-runtime et runtime. Il MUST sélectionner et qualifier PA système/PZT local pour préparer PostgreSQL, sans activation déduite de la présence des modules ni confusion avec le réseau distant. La preuve MUST respecter les garanties détaillées du scénario ci-dessous.

#### Scenario: Garanties de qualification du parcours initial PA PZT

- **WHEN** le profil initial PBO et son parcours de préparation PostgreSQL sont évalués
- **THEN** Le profil initial PBO MUST qualifier le binaire commun Kernel/Core/Auth/Agent/PZT et son plan de processus selon reference-runtime et runtime. La preuve MUST relier budgets accordés, configuration demandée, état appliqué, mesures et scénarios de panne. Les modules essentiels MUST rester composés et leur présence MUST NOT valoir activation. Le parcours initial de préparation PostgreSQL par PA MUST sélectionner explicitement les exécutants PA système et PZT local avec leurs profils propres à qualifier ; une absence de réseau distant MUST NOT être confondue avec l'absence de ce transport local obligatoire.

#### Scenario: P0 sans exécution réseau

- **WHEN** le profil initial conserve le réseau désactivé
- **THEN** les modules essentiels restent présents dans le binaire PBO et aucun exécutant PA/PZT ni résultat réseau n'est inventé
- **AND** l’absence de PZT local empêche de qualifier le parcours de préparation PostgreSQL par PA

#### Scenario: P0 sans réseau distant

- **WHEN** le profil initial sélectionne la préparation PostgreSQL par PA sans réseau distant
- **THEN** les modules essentiels et les exécutants PA système/PZT local nécessaires sont explicitement sélectionnés et qualifiés sans revendiquer de résultat de réseau distant

#### Scenario: Plan de ressources sans preuve sur cible

- **WHEN** une composition P0 possède un plan mais pas de recette sur l'environnement distribué
- **THEN** elle ne revendique pas un binaire ou un dimensionnement qualifié sur cette seule déclaration
~~~~

### Référence courante reference-composition-0af0b6011293

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 35. SHA-256 : `0af0b601129367e64eba64554f480dd9d5a1b93ee2348a0ba66ad4ac964e8671`.

Scénarios : Capacité P0 absente.

~~~~text
### Requirement: Capacités obligatoires du P0

Une composition P0 MUST inclure les mécanismes de composition, `pixs.core`, `pixs.auth` essentiel avec son authentification locale autonome et PostgreSQL par défaut, le contexte tenant/scope, l'autorisation, les API et contrats publics, migrations, runtime, provisionnement, sécurité, secrets, audit, observabilité, gouvernance, cycle de vie des données, conformité et un composant d'exemple.

#### Scenario: Capacité P0 absente

- **WHEN** une composition se présente comme P0 mais omet une capacité obligatoire
- **THEN** sa validation échoue avant activation ou publication
~~~~

### Référence courante reference-composition-986398c06367

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 44. SHA-256 : `986398c063671a966f8bc20f7e0d7706fe89595ff960a233fa8fbc266c49ad03`.

Scénarios : Synchronisation non sélectionnée.

~~~~text
### Requirement: Capacités hors P0 explicites

Toute capacité hors P0 MAY être ajoutée par sélection explicite. Son absence
MUST être déclarée ou représentée par un état compatible et MUST NOT affaiblir
les garanties du P0.

#### Scenario: Synchronisation non sélectionnée

- **WHEN** une composition P0 n'inclut aucun provider de synchronisation
- **THEN** elle reste valide sans annoncer de capacité réactive
~~~~

### Référence courante reference-composition-ab553efe6c54

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 55. SHA-256 : `ab553efe6c54a415ee9b8e42bbb9e9d009d3681dce99c2210ada04af4ef236b4`.

Scénarios : Deux validations identiques.

~~~~text
### Requirement: Preuve reproductible

La validation P0 MUST produire une preuve versionnée du graphe de composants,
contrats, profils et contrôles exécutés. Cette preuve MUST NOT contenir de secret,
credential ou donnée de production.

#### Scenario: Deux validations identiques

- **WHEN** la même composition P0 est validée avec les mêmes entrées
- **THEN** elle produit le même graphe et des contrôles équivalents
~~~~

### Référence courante reference-composition-5f1322f3cd28

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 66. SHA-256 : `5f1322f3cd28af91090d23c44e81cab453f1e264e606a48d7fbaa4ea3853d90e`.

Scénarios : Garanties du profil Debian local avec préparation PA; Architecture seulement observée.

~~~~text
### Requirement: Profil initial PBO PFO Debian local v1

Le profil pbo-p0-debian-local-v1 MUST identifier PBO/PFO, Debian 13 local, Django/TanStack et PostgreSQL distinct de PBO, préparé par PA système via PZT local. Il MUST déclarer et qualifier ses versions, architectures et exécutants selon le scénario ci-dessous ; un relevé de développement ou une preuve sans ces exécutants MUST NOT qualifier ce profil révisé.

#### Scenario: Garanties du profil Debian local avec préparation PA

- **WHEN** la première livraison du profil pbo-p0-debian-local-v1 est évaluée
- **THEN** La première livraison de profil `pbo-p0-debian-local-v1` MUST identifier PBO/PFO, Debian 13 local, Django, TanStack et PostgreSQL comme service distinct du processus PBO, préparé par le PA système de cet hôte via le parcours PA/PZT déclaré. Le profil MUST sélectionner les exécutants PA système et PZT local nécessaires à ce parcours ; une qualification historique sans ces exécutants MUST NOT prouver ce profil révisé. Elle MUST déclarer ses architectures et versions qualifiées avant distribution ; le relevé de développement MUST NOT tenir lieu de qualification.

#### Scenario: Architecture seulement observée

- **WHEN** une architecture apparaît dans l’environnement de développement sans recette correspondante
- **THEN** elle n’est pas annoncée comme supportée par le profil livré
~~~~

### Référence courante reference-composition-70063af8e7b7

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 80. SHA-256 : `70063af8e7b7f3ec61cbf3a60e111e20b60fcc09b6574df183ec392d1f1dce56`.

Scénarios : Module essentiel absent.

~~~~text
### Requirement: Garanties du socle conservées dans le profil initial

Le profil initial MUST satisfaire les capacités obligatoires P0 et composer les modules de gestion `pixs.agent` (PA hors PZT) et `pixs.pzt` (PZT), ainsi que le module DNS essentiel côté PBO. La désactivation réseau MUST NOT retirer ces modules ni affaiblir identité, périmètre, autorisation, audit, gouvernance ou reprise applicables.

#### Scenario: Module essentiel absent

- **WHEN** le réseau est désactivé mais `pixs.agent`, `pixs.pzt` ou le module DNS essentiel manque à la composition PBO
- **THEN** la qualification du profil échoue avant publication
~~~~

### Référence courante reference-composition-2614801b7609

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 89. SHA-256 : `2614801b7609ab3d7e337158b1a189846ac07b7308a13f21974f0e532efc17de`.

Scénarios : Démonstration mémoire seule.

~~~~text
### Requirement: Parcours installable et utilisable du profil initial

Le profil MUST permettre installation, première configuration, authentification, administration et opérations Core via contrats publics. Les rôles web, worker et scheduler MUST utiliser le même artefact et la persistance de référence ; une composition de test seule MUST NOT prouver ces parcours.

#### Scenario: Démonstration mémoire seule

- **WHEN** les seuls contrôles réussis utilisent des fixtures mémoire sans installation ni dépendance réelle
- **THEN** le profil ne revendique pas un parcours installable et utilisable qualifié
~~~~

### Référence courante reference-composition-ef9b2d25c156

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 98. SHA-256 : `ef9b2d25c1563c4766241a4a4b0e5df4f4188397774c38481e8c1f9e7bd395ab`.

Scénarios : Option absente sans dépendance obligatoire.

~~~~text
### Requirement: Capacités non sélectionnées du profil initial

Le profil MUST déclarer les capacités non sélectionnées et leurs limites sans annoncer leurs garanties. Une dépendance obligatoire d’une capacité sélectionnée MUST NOT être exclue sous prétexte d’option ; son absence bloque la qualification concernée.

#### Scenario: Option absente sans dépendance obligatoire

- **WHEN** aucun provider de synchronisation n’est sélectionné et aucune capacité retenue ne l’exige
- **THEN** son absence est déclarée sans annoncer de synchronisation ni affaiblir le P0
~~~~

### Référence courante reference-composition-7961b985d4cc

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 107. SHA-256 : `7961b985d4cc6e4533276d182585f4d018bce58499a8d3ce46b8b3ae71f2da57`.

Scénarios : Sources et paquet divergents.

~~~~text
### Requirement: Preuve de la composition effectivement distribuée

La preuve initiale MUST relier exigences applicables, scénarios exécutés, composants, versions et artefact installé. Elle MUST distinguer code présent, déclarations, dimensions non évaluées et verdicts observés, sans secret ni compatibilité globale supposée.

#### Scenario: Sources et paquet divergents

- **WHEN** la recette porte sur des sources différentes de celles du paquet proposé
- **THEN** elle ne suffit pas à qualifier la composition distribuée
~~~~

### Référence courante reference-composition-80e3d17e557d

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 116. SHA-256 : `80e3d17e557db39ab0b1f163e3b9be60f18df6f7f0cdd4ef4555404d6256b8c9`.

Scénarios : Hôte intermédiaire conservé non prêt; Source locale hors phase autorisée.

~~~~text
### Requirement: Choix C01 systemd et exception d’amorçage du profil Debian local

Le profil pbo-p0-debian-local-v1 MUST sélectionner le transport C01 LoadCredentialEncrypted systemd avec rotation par arrêt attesté et redémarrage contrôlé. Avant disponibilité de la base Pixs et du sink C05, il MUST déclarer explicitement l’exception limitée du journal fonctionnel local d’amorçage, ses politiques et son autorisation INSTALLER.

#### Scenario: Hôte intermédiaire conservé non prêt

- **WHEN** le provider est configuré mais qu’une preuve d’identité, d’audit, de reprise ou de qualification requise manque
- **THEN** la composition reste non prête sans affaiblir les obligations C17/C18/C19

#### Scenario: Source locale hors phase autorisée

- **WHEN** le journal local est proposé comme autorité applicative après reprise complète ou pour des opérations métier ordinaires
- **THEN** la composition refuse cet usage hors de l’exception d’amorçage
~~~~

### Référence courante reference-composition-b86766ab642e

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 130. SHA-256 : `b86766ab642ec0550cf7661ba1d162a50901d633d9bb6948cc548c4cb0225c3e`.

Scénarios : Hôte intermédiaire conservé non prêt; Source locale hors phase autorisée.

~~~~text
### Requirement: Qualification et source de vérité après amorçage

Cette exception MUST NOT devenir une source de vérité métier parallèle après reprise dans PostgreSQL. Les architectures, versions, capacités de stockage et politiques MUST être qualifiées avant distribution ; DEVOPS.md, un test isolé ou un reçu mémoire MUST NOT valoir qualification du paquet.

#### Scenario: Hôte intermédiaire conservé non prêt

- **WHEN** le provider est configuré mais qu’une preuve d’identité, d’audit, de reprise ou de qualification requise manque
- **THEN** la composition reste non prête sans affaiblir les obligations C17/C18/C19

#### Scenario: Source locale hors phase autorisée

- **WHEN** le journal local est proposé comme autorité applicative après reprise complète ou pour des opérations métier ordinaires
- **THEN** la composition refuse cet usage hors de l’exception d’amorçage
~~~~

### Référence courante reference-composition-fa2727180f3d

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 144. SHA-256 : `fa2727180f3d824fbb7e3619a5b0196d02d52df210f1022887c5b3578875e857`.

Scénarios : Profil livré sans connecteurs externes; Profil Domaine.

~~~~text
### Requirement: Profil Auth standard sans connecteur externe installé

Le profil pré-domaine MUST sélectionner Auth local PG et garder les connecteurs externes absents sauf sélection explicite. Le mode Domaine MUST composer les capacités LZT/OpenLDAP et KZT/MIT Kerberos requises par Domaine ; IdP sortant et connecteurs externes MUST rester distincts et non activés implicitement. Présence de logiciel et service opérationnel MUST rester séparés.

#### Scenario: Profil livré sans connecteurs externes

- **WHEN** un profil Standalone standard est installé
- **THEN** Auth PG fonctionne selon sa politique sans service LDAP/KDC ou émission sortante implicite.

#### Scenario: Profil Domaine

- **WHEN** une composition revendique un Domaine opérationnel
- **THEN** ses LZT/KZT et son ZT admissible doivent être vérifiés, même si aucune source externe n’est installée.
~~~~

### Référence courante reference-composition-4f43b97aaed5

Source : [reference-composition](../../specs/reference-composition/spec.md), ligne 158. SHA-256 : `4f43b97aaed55b2b87629f7cc9dfae67e927a01213a4051882f1cc89c67f335e`.

Scénarios : PBO seul disponible.

~~~~text
### Requirement: Composition ZT initiale et Domaines

La qualification MUST distinguer PBO composé, PA/PZT disponibles, ZT entièrement initialisé et Domaine opérationnel. Les minima MUST suivre pixs-instance, pixs-domains et zt-instances ; un contrat pur ou artefact présent MUST NOT prouver ces états. Le premier PZT complet MUST cibler Debian/Linux et les autres profils MUST déclarer leurs rôles qualifiés.

#### Scenario: PBO seul disponible

- **WHEN** PBO est qualifié mais aucun exécutant CZT/DZT/PKIZT n’est admissible
- **THEN** la composition ne revendique pas ZT initialisé ni création de Domaine admissible.
~~~~

### Référence courante pixs-domains-02f0f83aed5e

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 11. SHA-256 : `02f0f83aed5e7e038716c3f91cc0b8f31edb2c5ea812cd6dbe8b37b700589e39`.

Scénarios : Racine déjà utilisée.

~~~~text
### Requirement: Identité et FQDN explicites

Chaque Domaine MUST posséder une identité stable et un FQDN DNS explicitement choisi. Deux Domaines d'une même Instance MUST NOT déclarer le même FQDN exact. La position DNS MUST NOT créer d'approbation ni d'autorisation implicite.

#### Scenario: Racine déjà utilisée

- **WHEN** un Domaine demande le FQDN exact d’un autre Domaine de l’Instance
- **THEN** la déclaration est refusée avant activation.
~~~~

### Référence courante pixs-domains-686f4e13ff70

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 20. SHA-256 : `686f4e13ff70e8af073de2ac6f80d25d553a84feb6cec9fec11dc0f13c5d93cc`.

Scénarios : Deux sous-domaines; Faux suffixe.

~~~~text
### Requirement: ZT obligatoire dédié ou partagé

Chaque Domaine MUST utiliser une instance ZT. Il MAY créer son ZT ou utiliser celui de l'Instance lorsque son FQDN est égal au FQDN ZT ou en est un sous-domaine par labels DNS. Plusieurs Domaines admissibles MAY utiliser ce même ZT ; le partage MUST rester explicitement déclaré.

#### Scenario: Deux sous-domaines

- **WHEN** association.pixs.fr et recherche.pixs.fr choisissent le ZT pixs.fr
- **THEN** ils peuvent être rattachés avec des périmètres distincts.

#### Scenario: Faux suffixe

- **WHEN** association-autrepixs.fr demande le ZT pixs.fr en invoquant un suffixe de caractères
- **THEN** la condition hiérarchique DNS est refusée.
~~~~

### Référence courante pixs-domains-bd2991264b73

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 34. SHA-256 : `bd2991264b73d60314f90b7bb3d936bee405c507992fe50e7ff2e06fb1da6fc6`.

Scénarios : Même ZT sans politique.

~~~~text
### Requirement: Isolation dans un ZT partagé

Les politiques MUST pouvoir être propres à un Domaine ou partagées explicitement. Les communications inter-domaines MUST être refusées par défaut et nécessiter une politique explicite. Le partage du ZT MUST NOT fusionner les identités, ACL applicatives, annuaires ou realms.

#### Scenario: Même ZT sans politique

- **WHEN** deux acteurs de Domaines différents partagent ZT sans autorisation de communication
- **THEN** l’initiation inter-domaines est refusée.
~~~~

### Référence courante pixs-domains-c9ce061e2b23

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 43. SHA-256 : `c9ce061e2b23d3859a4cb92e01635334908d63f103ce5c9db7b2b2c1d5a053c5`.

Scénarios : ZT partagé et KZT manquant.

~~~~text
### Requirement: Services minimaux par Domaine

Chaque Domaine MUST disposer de sa PG indépendante, de ses organigrammes organisationnel/fonctionnel, d'au moins un LZT/OpenLDAP et d'un KZT/MIT Kerberos. Chaque Domaine MUST déclarer son realm, unique dans l'Instance. Les minima CZT/SZT/RZT/STZT/DZT/PKIZT MUST être évalués par ZT réel, pas dupliqués par déduction pour un ZT partagé.

#### Scenario: ZT partagé et KZT manquant

- **WHEN** un nouveau Domaine partage un ZT opérationnel mais ne possède aucun KZT
- **THEN** ses services de Domaine restent non opérationnels tant que ce minimum manque.
~~~~

### Référence courante pixs-domains-784b3416b755

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 52. SHA-256 : `784b3416b7559266c7a1b38d15a475ebd8b05a90e2f00eb976a8bf198703e0f4`.

Scénarios : Domaine sans tenant; Tenant rattaché deux fois.

~~~~text
### Requirement: Tenants et propriété des ressources

Un Domaine MUST accepter zéro, un ou plusieurs tenants ; chaque tenant MUST appartenir à un seul Domaine après transition. Les scopes enfants MUST rester rattachés à leur tenant sans cycles. Les propriétés Instance, Domaine et Tenant MUST être distinctes et n'accorder aucun droit implicite.

#### Scenario: Domaine sans tenant

- **WHEN** un Domaine opérationnel ne contient aucun tenant
- **THEN** ses services et son rattachement ZT restent valides.

#### Scenario: Tenant rattaché deux fois

- **WHEN** une mutation rattache simultanément un tenant à deux Domaines
- **THEN** elle est refusée sans ambiguïté de propriétaire.
~~~~

### Référence courante pixs-domains-8e5157150f7c

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 66. SHA-256 : `8e5157150f7c0a1801085b1c19bdd9c69fe4c345dcba246bb25ed2aba4727793`.

Scénarios : Affiliation sans admission.

~~~~text
### Requirement: Individus et identités multiples

Un individu Core MUST pouvoir être affilié à plusieurs Domaines et tenants et posséder plusieurs identités par Domaine. Chaque participation MUST conserver ses admissions, profils et habilitations. Une affiliation Core MUST NOT valoir admission ZT, sauf politique automatique explicite.

#### Scenario: Affiliation sans admission

- **WHEN** un individu est affilié à Recherche sans politique d’admission automatique
- **THEN** son appartenance ZT n’est pas créée par cette seule affiliation.
~~~~

### Référence courante pixs-domains-ba4dfa97bf7d

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 75. SHA-256 : `ba4dfa97bf7dfe8389d5a8f4597671aa9630b9e24d13f8a2ea071bc82dc36b12`.

Scénarios : Tenant transféré.

~~~~text
### Requirement: Transferts fonctionnels contrôlés V1

La V1 MUST prévoir les transferts autorisés d'identités numériques, données métier et tenants entre Domaines de la même Instance, avec vérification des dépendances, continuité des références et réévaluation des droits cibles. Le transfert MUST NOT copier implicitement des autorisations ni être présenté comme déplacement d'une brique exécutable.

#### Scenario: Tenant transféré

- **WHEN** un transfert de tenant est engagé entre deux Domaines
- **THEN** son identité est conservée, son propriétaire est unique et les habilitations de destination sont réévaluées.
~~~~

### Référence courante pixs-domains-2d4b91559aa3

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 84. SHA-256 : `2d4b91559aa387da2cb8be333d66674748a755850567e45bba8b742811112985`.

Scénarios : Transfert de département.

~~~~text
### Requirement: Structures organisationnelles non transférables V1

La V1 MUST NOT proposer le transfert fonctionnel de structures organisationnelles entre Domaines. Miroitage autorisé et réorganisation interne MUST rester distincts d'un tel transfert.

#### Scenario: Transfert de département

- **WHEN** une demande V1 vise à transférer un département entre Domaines
- **THEN** elle est refusée comme hors périmètre sans modifier les structures source ou cible.
~~~~

### Référence courante pixs-domains-f9d0dad1d882

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 93. SHA-256 : `f9d0dad1d882e815cf4d5b665b2037e6591dcb271ed3dd1e9f7605fcd4759334`.

Scénarios : Dernier Domaine.

~~~~text
### Requirement: Retrait du premier Domaine

Le premier Domaine MAY être retiré par procédure explicite si au moins un autre Domaine est opérationnel et si données, identités, authentification globale et dépendances sont traitées. Le retrait MUST NOT rétablir Standalone, laisser l'administration sans identité admissible ou retirer un ZT partagé encore requis.

#### Scenario: Dernier Domaine

- **WHEN** le retrait vise le seul Domaine opérationnel
- **THEN** il est refusé sans retour implicite en Standalone.
~~~~

### Référence courante pixs-domains-94814997f512

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 102. SHA-256 : `94814997f512912fbd83b186f7db3bf2f0771d0e37c0e5ecfc7fe81a41c5562f`.

Scénarios : Individu externe reconnu.

~~~~text
### Requirement: Approbations internes et externes

Les Domaines MUST pouvoir établir des approbations dans une même Instance ou entre Instances selon zt-instances. Un individu externe MUST conserver son identité d'origine ; la cible MUST conserver une référence et décider séparément de ses admissions et droits. Les composantes DNS et Kerberos MUST être explicites.

#### Scenario: Individu externe reconnu

- **WHEN** une approbation permet de reconnaître l’identité externe
- **THEN** la reconnaissance ne crée pas d’identité locale indépendante ou de droits automatiques.
~~~~

### Référence courante pixs-domains-d8fce09ab784

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 111. SHA-256 : `d8fce09ab78488325720197abff25a3f229a41ca7f6e38dac7da16c02df7b924`.

Scénarios : Reconstruction de Domaine.

~~~~text
### Requirement: Références PG et services de Domaine en mode normal ou critique

LZT et KZT MUST être obligatoires par Domaine. PG MUST rester souveraine pour les données de référence Pixs ; LDAP MUST porter l'état opérationnel Kerberos durable en mode normal. Une reconstruction complète depuis PG MUST suivre le mode critique autorisé, avec restauration protégée ou recréation/reprovisionnement selon profil et sauvegardes disponibles. La réplication LDAP MUST NOT remplacer la référence Core PG.

#### Scenario: Reconstruction de Domaine

- **WHEN** tous les annuaires du Domaine sont perdus
- **THEN** le Domaine applique sa procédure critique, distingue données de référence et clés récupérées/recréées, puis vérifie la remise en service.
~~~~

### Référence courante organization-charts-c0cec12f0548

Source : [organization-charts](../../specs/organization-charts/spec.md), ligne 11. SHA-256 : `c0cec12f054833f37f9ef4e5d2ae8e89737e329ea5b1f9ce56459b44fffdf241`.

Scénarios : ZT partagé.

~~~~text
### Requirement: Trois référentiels propriétaires

Core MUST gérer l'organigramme organisationnel et le fonctionnel, par Domaine après transition. CZT MUST gérer l'organigramme structurel de son ZT. PBO MUST présenter trois volets distincts ; un ZT partagé MUST conserver les périmètres des Domaines sans dupliquer une racine ZT par Domaine.

#### Scenario: ZT partagé

- **WHEN** deux Domaines utilisent le même CZT
- **THEN** leurs volets Core restent propres et les périmètres structurels sont présentés dans le ZT commun.
~~~~

### Référence courante organization-charts-43a3193484d2

Source : [organization-charts](../../specs/organization-charts/spec.md), ligne 20. SHA-256 : `43a3193484d2bee52ef6f44cfe182b5c6b34e2cfb44d4f63bcd89d3ed21ebcd1`.

Scénarios : Deux parents structurels.

~~~~text
### Requirement: Hiérarchie structurelle et affiliations

L'organigramme ZT MUST posséder une racine unique, au plus un parent structurel par structure, aucun cycle et des affiliations multiples possibles. Chaque acteur technique MUST avoir une structure responsable de référence ; chaque individu MUST avoir un rattachement principal par ZT. Ces relations MUST rester distinctes des permissions et de la hiérarchie PKI.

#### Scenario: Deux parents structurels

- **WHEN** une structure ZT reçoit deux parents structurels
- **THEN** la mutation est refusée sans empêcher les affiliations transversales autorisées.
~~~~

### Référence courante organization-charts-8369220fda62

Source : [organization-charts](../../specs/organization-charts/spec.md), ligne 29. SHA-256 : `8369220fda6234df9ed1556288de294305748cfda265cac54698c3df3fa38184`.

Scénarios : Écriture sur miroir.

~~~~text
### Requirement: Source explicite de chaque miroir

Un périmètre de miroitage MUST choisir une source explicite parmi les trois organigrammes, ses données et transformations autorisées. Ses mutations MUST passer par la source et respecter les contraintes cibles. Une modification de la copie MUST NOT devenir silencieusement une deuxième autorité.

#### Scenario: Écriture sur miroir

- **WHEN** un opérateur tente de modifier directement la copie reflétée
- **THEN** l’interface applique le contrat de la source ou refuse l’écriture concurrente.
~~~~

### Référence courante organization-charts-3f5fd5146131

Source : [organization-charts](../../specs/organization-charts/spec.md), ligne 38. SHA-256 : `3f5fd5146131f61a9cf1d8e9811329be5f7f571d315ad76e8af0231f736a8105`.

Scénarios : Miroir standard.

~~~~text
### Requirement: Structure seule par défaut

Le miroir MUST porter sur la structure seule par défaut. La synchronisation des rattachements et affiliations MAY être activée explicitement par périmètre ; les individus MUST rester référencés depuis Core sans duplication d'identité ou de moyen d'authentification.

#### Scenario: Miroir standard

- **WHEN** un miroir est créé sans sélection des affiliations
- **THEN** les seules structures et relations hiérarchiques autorisées sont reprises.
~~~~

### Référence courante organization-charts-a06107e07b95

Source : [organization-charts](../../specs/organization-charts/spec.md), ligne 47. SHA-256 : `a06107e07b9597bbf983057cb15e8480fd7a774f5e4c3628bc1d29e71ecce71b`.

Scénarios : Affiliation vers un ZT.

~~~~text
### Requirement: Admission et droits séparés du miroir

Un miroir MUST NOT créer implicitement admission ZT, compte, permission ou copie d'ACL. Une affiliation vers ZT MUST exiger l'admission applicable et les politiques ZT MUST être réévaluées après modification autorisée.

#### Scenario: Affiliation vers un ZT

- **WHEN** le miroir reçoit l’affiliation d’un individu non admis
- **THEN** aucune participation effective ni autorisation ZT n’est déduite.
~~~~

### Référence courante brick-redundancy-ce67ff7e1fde

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 11. SHA-256 : `ce67ff7e1fde4ca9f4b7ad0badf7054c4e1fe46c1db73b174b19e30bd470ee1a`.

Scénarios : Second PZT.

~~~~text
### Requirement: Remplacement sans déplacement direct

Une brique MUST être remplacée par initialisation d'une seconde brique identifiée, synchronisation, vérification puis activation/reprise avant démantèlement selon ses critères. La procédure MUST NOT déplacer implicitement le processus ou copier l'identité d'un nouveau membre.

#### Scenario: Second PZT

- **WHEN** un PZT supplémentaire est initialisé pour remplacer un rôle
- **THEN** il reçoit son identité et son admission propres avant de reprendre le rôle autorisé.
~~~~

### Référence courante brick-redundancy-78e23fa4ab8f

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 20. SHA-256 : `78e23fa4ab8fa0bb63d03ef7d2eed6192c067b88caebb136646f31b66c88d7e2`.

Scénarios : Exception au mode.

~~~~text
### Requirement: Mode par famille et exceptions

Chaque famille MUST définir son mode d'autorité et de synchronisation par défaut. Une brique MAY y déroger par configuration explicite ; une exception incompatible avec le mode de famille MUST être justifiée et tracée. La dérogation MUST NOT supprimer une garantie spécifique obligatoire du rôle.

#### Scenario: Exception au mode

- **WHEN** un administrateur propose une exception de mode
- **THEN** sa justification, sa portée et ses contrôles sont enregistrés avant admission.
~~~~

### Référence courante brick-redundancy-29e8a1e997e2

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 29. SHA-256 : `29e8a1e997e28be127916e1f936f38f70b6562b68b46d5dab57cff4629b3a465`.

Scénarios : Copies requises absentes.

~~~~text
### Requirement: Conditions de reprise propres à la brique

Chaque brique MUST déclarer ses exigences de synchronisation et l'éventuel état partiel admissible avec limites explicites. La procédure MUST vérifier les critères courants avant activation. La règle générale MUST NOT abaisser le minimum PG synchrone ni permettre la perte d'une écriture confirmée dans un profil qui la protège.

#### Scenario: Copies requises absentes

- **WHEN** une reprise CZT ne satisfait pas son minimum synchrone configuré
- **THEN** la règle générale d’état partiel ne permet pas de la confirmer.
~~~~

### Référence courante brick-redundancy-b7eb34bb70c2

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 38. SHA-256 : `b7eb34bb70c29f74664bbd69e8874a6819b8e6ecf8a60cc8c2626164191d7f65`.

Scénarios : Ancien maître isolé.

~~~~text
### Requirement: Unicité de l’autorité et automatisation

Un rôle à maître unique MUST empêcher l'ancien et le nouveau maître d'exercer simultanément. La reprise MAY être automatique sous politique et mandat préalablement autorisés ; sinon un administrateur MUST confirmer. Une injoignabilité seule MUST NOT prouver l'exclusion.

#### Scenario: Ancien maître isolé

- **WHEN** l’ancien maître est injoignable mais son exclusion n’est pas démontrée
- **THEN** la prise d’autorité reste bloquée selon le contrat du rôle.
~~~~

### Référence courante brick-redundancy-8df77aef5446

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 47. SHA-256 : `8df77aef54469a86d9737a29a58a9b52c8f4fc211a4ac422a8bb6a1a5f8b9175`.

Scénarios : Nouvel actif non vérifié.

~~~~text
### Requirement: Observation et démantèlement

Chaque brique MUST définir la vérification du nouvel actif, l'éventuelle période d'observation, le statut de l'ancienne et ses critères de démantèlement. L'ancienne MAY rester secours passif, copie de retrait ou autre état déclaré ; elle MUST NOT reprendre des droits expirés ou révoqués.

#### Scenario: Nouvel actif non vérifié

- **WHEN** le service de remplacement n’a pas satisfait les contrôles
- **THEN** le démantèlement n’est pas autorisé sur sa seule activation administrative.
~~~~

### Référence courante brick-redundancy-73cbc72a8e34

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 56. SHA-256 : `73cbc72a8e34d14d7ef69dc78d17ffb7d5f3c0e0fcfd1898d8a241e4867f752c`.

Scénarios : Versions hors plage.

~~~~text
### Requirement: Compatibilité de versions par famille

Chaque famille MUST déclarer si des versions identiques sont requises ou si une plage de compatibilité est admise. Une paire non qualifiée MUST être refusée pour synchronisation/reprise ; la présence des binaires MUST NOT prouver la compatibilité.

#### Scenario: Versions hors plage

- **WHEN** une réplique est installée dans une version non admise
- **THEN** la synchronisation protégée ou la reprise concernée reste bloquée avec diagnostic.
~~~~

### Référence courante brick-redundancy-9c403ec6ed51

Source : [brick-redundancy](../../specs/brick-redundancy/spec.md), ligne 65. SHA-256 : `9c403ec6ed51a5c3ebdc3db0b60ff70c1382311adacdd6a3fc42fdc997c6fd23`.

Scénarios : Copies distinctes.

~~~~text
### Requirement: Références PostgreSQL répliquées et garanties conservées

Les bases PG Instance, Domaine, CZT, DZT et PKIZT MUST pouvoir disposer de répliques synchrones avec un primaire d'écriture unique. Leur minimum de confirmations MUST être configurable sans réduction automatique en panne ; promotion MUST exclure l'ancien primaire et préserver les écritures confirmées. Une réplication MUST rester celle d'une même base logique sans fusion de Domaines.

#### Scenario: Copies distinctes

- **WHEN** deux PG de Domaines différents sont déclarées
- **THEN** elles ne deviennent pas répliques d’une même base par partage de serveur ou de ZT.
~~~~

### Référence courante managed-device-policies-8a43d725b9c8

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 11. SHA-256 : `8a43d725b9c8f9f725eb22c048e5e91d1ee208d3af98a44e61ea75cfae643633`.

Scénarios : Poste administré.

~~~~text
### Requirement: Cibles V1 et exécutants locaux

Les profils V1 MUST couvrir postes Linux/Windows et serveurs Linux membres, avec Debian stable et Windows 10/11 admissibles à qualifier. Les postes administrés et serveurs Linux soumis aux politiques MUST disposer de PA/PZT locaux. Les rôles serveur de domaine MUST NOT être imposés sur chaque poste.

#### Scenario: Poste administré

- **WHEN** un poste reçoit une politique Pixs
- **THEN** les exécutants locaux sont vérifiés sans le transformer en LZT ou KZT.
~~~~

### Référence courante managed-device-policies-f3d868c20f8b

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 20. SHA-256 : `f3d868c20f8b51c27e721a1df72180c8508e9cfdf1ff06948b8294b817119a29`.

Scénarios : Hôte tiers géré.

~~~~text
### Requirement: Gestion ZT et jonction d’authentification distinctes

Un hôte MAY être intégré à ZT et administré sans jonction de domaine pour l'authentification de ses utilisateurs. Cette jonction MUST rester facultative mais exiger l'intégration ZT préalable lorsqu'elle est demandée. Le passage du PA en mode Domaine MUST NOT joindre automatiquement l'hôte au domaine d'authentification.

#### Scenario: Hôte tiers géré

- **WHEN** un hôte rejoint ZT sans jonction d’authentification
- **THEN** PA peut gérer ses capacités autorisées tandis que les utilisateurs conservent l’authentification configurée sur l’hôte.
~~~~

### Référence courante managed-device-policies-0fc04bee903f

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 29. SHA-256 : `0fc04bee903fa7c526db55656c40db141fc78bd93e1a2f658507d54be92da507`.

Scénarios : Règle propre à Windows.

~~~~text
### Requirement: Politiques communes et spécifiques

Les politiques MUST permettre des intentions communes Windows/Linux et des règles propres aux plateformes, avec politiques de poste et d'utilisateur et ciblage explicite. Les capacités non qualifiées MUST être déclarées non applicables ou indisponibles, sans simulation de succès.

#### Scenario: Règle propre à Windows

- **WHEN** une politique commune comporte une règle GPO Windows
- **THEN** l’application Linux ne prétend pas avoir appliqué cette règle native.
~~~~

### Référence courante managed-device-policies-a7f801c0bbd9

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 38. SHA-256 : `a7f801c0bbd9d9343d1e85e137ebc5eb30e56d499daabeba1006d7fe6d26ebbe`.

Scénarios : Deux valeurs au même niveau.

~~~~text
### Requirement: Priorités et contradictions

Les politiques de configuration MUST avoir des priorités explicites ; les contradictions à priorité égale MUST être signalées sans règle implicite du dernier reçu. La résolution MUST respecter les contrats de propriété et autorisations de chaque périmètre.

#### Scenario: Deux valeurs au même niveau

- **WHEN** deux politiques de même priorité imposent des valeurs incompatibles
- **THEN** l’écart est signalé et aucune valeur n’est choisie par ordre d’arrivée.
~~~~

### Référence courante managed-device-policies-fc87e0db8071

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 47. SHA-256 : `fc87e0db80717cda5b2c979b05d5045ee0bf334a5dd2cf6559bb9d13857e9c0e`.

Scénarios : Configuration reçue sans effet.

~~~~text
### Requirement: Application par PA et état vérifié

PA MUST appliquer les opérations livrées et autorisées dans le contexte système ou utilisateur approprié via pixs.agent. Réception, application, dérive et résultat confirmé MUST rester distincts. Les corrections automatiques MUST posséder leur propre politique et mandat.

#### Scenario: Configuration reçue sans effet

- **WHEN** PA reçoit une politique mais échoue à la mettre en place
- **THEN** PBO affiche l’échec sans état appliqué fictif.
~~~~

### Référence courante managed-device-policies-53ac3cf3063d

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 56. SHA-256 : `53ac3cf3063d580b57f56441ca276f52645441d643d76c41f8e4077b7e5882e7`.

Scénarios : Pas de profil hors ligne.

~~~~text
### Requirement: Session hors ligne bornée

L'ouverture de session hors ligne MAY être permise par profil explicite et borné. Elle MUST conserver les exigences de validité, protection locale et retraits connus ; une panne MUST NOT activer ce profil ni repousser ses échéances.

#### Scenario: Pas de profil hors ligne

- **WHEN** le contrôleur est indisponible sans profil hors ligne autorisé
- **THEN** aucune nouvelle permission de connexion locale n’est déduite de la panne.
~~~~

### Référence courante managed-device-policies-0e3d3ee17150

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 65. SHA-256 : `0e3d3ee171504e6660c5650982a199dc41378de37affda7cbe83cb40f3506336`.

Scénarios : Rotation native autorisée.

~~~~text
### Requirement: Rotation des secrets machine et services

La rotation des secrets machine MUST être sélectionnable par profil entre pilotage Pixs/PBO/PA et rotation native qualifiée. Les services techniques MUST pouvoir utiliser un moyen propre ou une représentation habilitée selon profil. Ces secrets MUST rester distincts du mot de passe des individus changé depuis PBO.

#### Scenario: Rotation native autorisée

- **WHEN** un poste utilise la rotation machine native qualifiée
- **THEN** elle suit son profil et sa cohérence contrôleurs sans autoriser un changement natif du mot de passe individuel.
~~~~

### Référence courante managed-device-policies-0a228d3c9bf5

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 74. SHA-256 : `0a228d3c9bf5969235d9a1b17bf8161742513eb0cd8bfd88e93f3901641b2177`.

Scénarios : Jonction exigeant redémarrage.

~~~~text
### Requirement: Redémarrage par profil et conclusion après reprise

Le profil MUST choisir redémarrage manuel ou automatique sous fenêtre autorisée, avec manuel par défaut. PBO MUST distinguer redémarrage requis et opération terminée ; les vérifications après redémarrage MUST précéder la conclusion de jonction ou de politique.

#### Scenario: Jonction exigeant redémarrage

- **WHEN** la configuration est appliquée mais le poste n’a pas redémarré
- **THEN** l’opération reste à terminer jusqu’aux contrôles après reprise.
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| testing / 8 | [Trois niveaux de vérification distincts](../../specs/testing/spec.md#L8) | P | COMPLETER_OU_INTEGRER |
| testing / 17 | [Kit de conformité et composant d'exemple](../../specs/testing/spec.md#L17) | P | COMPLETER_OU_INTEGRER |
| testing / 30 | [Suites de conformité versionnées par contrat](../../specs/testing/spec.md#L30) | P | COMPLETER_OU_INTEGRER |
| testing / 39 | [Garanties obligatoires séparées des capacités optionnelles](../../specs/testing/spec.md#L39) | P | COMPLETER_OU_INTEGRER |
| testing / 48 | [Reproductibilité sur la topologie de référence](../../specs/testing/spec.md#L48) | P | COMPLETER_OU_INTEGRER |
| testing / 57 | [Preuves sans secret ni donnée de production](../../specs/testing/spec.md#L57) | P | COMPLETER_OU_INTEGRER |
| testing / 66 | [Conformité de la composition frontend récursive](../../specs/testing/spec.md#L66) | P | COMPLETER_OU_INTEGRER |
| testing / 75 | [Conformité des projections d'annuaire optionnelles](../../specs/testing/spec.md#L75) | P | COMPLETER_OU_INTEGRER |
| testing / 89 | [Exécution navigateur headless des unités frontend web](../../specs/testing/spec.md#L89) | P | COMPLETER_OU_INTEGRER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence testing--3bc15eb3da

Source : `openspec/specs/testing/spec.md`, ligne 8. SHA-256 du bloc : `8bd293063511d9ff7c4e776d91f7b343192d9b7ad3654f1060f2ba0866743e16`.

~~~~text
### Requirement: Trois niveaux de vérification distincts

Le projet MUST distinguer les tests unitaires des comportements internes, les tests d'intégration des compositions et des dépendances réelles de référence, et les tests de conformité des contrats publiés ; le succès d'un niveau MUST NOT tenir lieu de preuve pour un autre.

#### Scenario: Unitaires verts, intégration rouge

- **WHEN** des tests unitaires réussissent alors qu'un test d'intégration de composition échoue
- **THEN** la release est considérée non valide et l'échec d'intégration est rapporté explicitement
~~~~

### Référence testing--b553810d1f

Source : `openspec/specs/testing/spec.md`, ligne 17. SHA-256 du bloc : `ff6ff6ed413bc587bd7f4420c4d84bc5d78f3ed21ebc0419cb4a65928eb5e7af`.

~~~~text
### Requirement: Kit de conformité et composant d'exemple

Le Developer Kit MUST fournir des validateurs et suites de conformité
versionnés pour les manifests, contrats et composants déclarés compatibles. Un
composant d'exemple P0 MUST démontrer la composition par contrats, le contexte
tenant/scope et l'autorisation ; il MUST NOT devenir une dépendance de
production.

#### Scenario: Exemple P0 validé

- **WHEN** le composant d'exemple est validé par le Developer Kit
- **THEN** les preuves indiquent les versions de contrats et les contrôles P0 exécutés
~~~~

### Référence testing--8240234124

Source : `openspec/specs/testing/spec.md`, ligne 30. SHA-256 du bloc : `1a25f001ea6e86cc778df2ec2938ccb06868648d5b1702000d191653c4c631c9`.

~~~~text
### Requirement: Suites de conformité versionnées par contrat

Chaque contrat de fournisseur MUST disposer d'une suite de conformité versionnée, indépendante de la technologie implémentée ; le runtime MUST NOT déclarer compatible un provider dont la conformité obligatoire est absente, expirée ou échouée.

#### Scenario: Certification expirée

- **WHEN** un provider présente une preuve de conformité expirée pour sa version déclarée
- **THEN** il est exclu de la sélection tant qu'une nouvelle exécution de la suite ne réussit pas
~~~~

### Référence testing--ec900517c4

Source : `openspec/specs/testing/spec.md`, ligne 39. SHA-256 du bloc : `0310541d7ae00ce5d4425cb1235794b54133d8de93060c47e76a5acc04cdfa38`.

~~~~text
### Requirement: Garanties obligatoires séparées des capacités optionnelles

Les tests MUST distinguer les garanties obligatoires des capacités optionnelles : une capacité optionnelle absente ou indisponible peut produire un état dégradé ou désactivé si elle reste isolée ; une incompatibilité de contrat, une ambiguïté de fournisseur, un défaut d'isolation de tenant ou une violation de sécurité MUST bloquer l'activation.

#### Scenario: Isolement acceptable

- **WHEN** une capacité optionnelle tombe sans fuite d'accès ni perte de donnée
- **THEN** l'état dégradé est accepté et diagnostiqué alors que le socle reste actif
~~~~

### Référence testing--ea8ece8809

Source : `openspec/specs/testing/spec.md`, ligne 48. SHA-256 du bloc : `3b2d50452802a83d20b35dec44cd60cd7109aa0c54aaca3bcb541088cadba393`.

~~~~text
### Requirement: Reproductibilité sur la topologie de référence

Les tests MUST être exécutables sur la topologie de référence du projet et sur toute topologie isolée déclarée compatible ; une différence de topologie MUST NOT modifier silencieusement les règles d'autorisation, de partage, de projection ou de suppression.

#### Scenario: Divergence de topologie

- **WHEN** un test d'invariant de périmètre produit un résultat différent selon la topologie
- **THEN** l'écart est bloquant et la topologie concernée perd sa mention de compatibilité
~~~~

### Référence testing--f0b3bab690

Source : `openspec/specs/testing/spec.md`, ligne 57. SHA-256 du bloc : `d9ae4d21e57d739e7b642389b1085eccff510000f3a51fdb8f674d17f68d439c`.

~~~~text
### Requirement: Preuves sans secret ni donnée de production

Les fixtures, exemples et rapports produits par les tests MUST être synthétiques et reproductibles, sans secret, sans token et sans donnée de production ; les rapports MUST NOT exposer de détail exploitable.

#### Scenario: Secret détecté dans un rapport

- **WHEN** un artefact de test contient une valeur sensible réelle ou apparentée
- **THEN** le rapport est invalidé, la fuite est signalée et l'exécution est bloquante pour la publication
~~~~

### Référence testing--2632c92c48

Source : `openspec/specs/testing/spec.md`, ligne 66. SHA-256 du bloc : `99bd959f22eec7645e810ce689df821fbd8fd6c00a706a82d3ec898d4fa2f54e`.

~~~~text
### Requirement: Conformité de la composition frontend récursive

Les suites de conformité MUST vérifier la résolution récursive des modules et sous-modules frontend, la propriété des contributions, les dépendances publiques, les contraintes SemVer, les collisions, les modes obligatoire et optionnel, ainsi que l'équivalence de composition entre développement et artefacts distribués. Une résolution frontend MUST NOT dépendre de l'ordre des imports, du filesystem ou d'un code distant runtime.

#### Scenario: Composition reproductible avec sous-module

- **WHEN** la même composition incluant un module et un sous-module frontend est construite deux fois
- **THEN** les contributions actives, l'ordre de chargement et les diagnostics produits sont identiques
~~~~

### Référence testing--19ab684105

Source : `openspec/specs/testing/spec.md`, ligne 75. SHA-256 du bloc : `4d1c7c58c3080d486f81efcd997cab6ade6c991c51d056d9ea8daa81ef6f6fa5`.

~~~~text
### Requirement: Conformité des projections d'annuaire optionnelles

Les suites de conformité MUST vérifier le mapping versionné, la projection
sortante idempotente, la reprise, les suppressions propagées, l'isolation de
tenant et de scope, la fraîcheur après mutation, le repli PostgreSQL et l'état
DEGRADED d'un provider LDAP indisponible. Elles MUST vérifier que LDAP ne peut
ni écrire dans Pixs, ni fournir une ACL, une décision d'autorisation, une
révocation ou une authentification par cette capacité.

#### Scenario: Repli conforme sans élargissement de droits

- **WHEN** LDAP devient indisponible pendant une consultation autorisée
- **THEN** la suite confirme la réponse PostgreSQL, l'état DEGRADED et l'absence de divulgation ou de droit supplémentaire
~~~~

### Référence testing--22ba62c0b8

Source : `openspec/specs/testing/spec.md`, ligne 89. SHA-256 du bloc : `121a020f91da796da68634e9f74a654ebc2160b8922ae90a777a642f3d3fe310`.

~~~~text
### Requirement: Exécution navigateur headless des unités frontend web

Les tests unitaires de la partie frontend web MUST être exécutés dans tous les
navigateurs déclarés par DEVOPS.md, en mode headless ; le succès de ces tests
uniquement sous Node MUST NOT tenir lieu de preuve de cette exigence.

#### Scenario: Les deux moteurs déclarent les cas

- **WHEN** `npm --prefix frontend test` s'exécute sur un environnement
  déclarant Chromium et Firefox headless
- **THEN** chaque cas unitaire frontend reçoit une preuve d'exécution issue de
  chaque navigateur déclaré et le résultat global n'est vert qu'avec les deux
  moteurs

#### Scenario: Moteur manquant ou cas non exécuté

- **WHEN** un navigateur déclaré est indisponible, ne répond pas dans les
  bornes, ou n'exécute pas l'intégralité des cas
- **THEN** l'exécution est en échec diagnostiqué, sans substitution par le
  seul résultat Node ou par la réussite du build
~~~~

