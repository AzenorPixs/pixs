# Exigences de réalisation — C17

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 proposé ajoute les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| artifact-publication / 8 | [Canaux comme contextes de confiance distincts](../../specs/artifact-publication/spec.md#L8) | ND | Artefact du mauvais canal |
| artifact-publication / 17 | [Immuabilité et corrélation des corrections](../../specs/artifact-publication/spec.md#L17) | ND | Écrasement d'un artefact publié |
| artifact-publication / 26 | [Identité vérifiable avant installation](../../specs/artifact-publication/spec.md#L26) | ND | Emprunte discordante |
| artifact-publication / 35 | [Signature, provenance et inventaire bloquants](../../specs/artifact-publication/spec.md#L35) | ND | Signature révoquée |
| artifact-publication / 44 | [Autorités distinctes et gestion des clés](../../specs/artifact-publication/spec.md#L44) | ND | Dépôt de publication indisponible |
| audit / 93 | [Profil structurel préparatoire d'occultation de champ d'audit v1](../../specs/audit/spec.md#L93) | L | Structure valide sans effet |
| audit / 102 | [Types et modes du profil d'occultation v1](../../specs/audit/spec.md#L102) | L | Types d'occultation exacts |
| audit / 111 | [Référence de remplacement du profil d'occultation v1](../../specs/audit/spec.md#L111) | L | Référence de remplacement selon le mode |
| audit / 120 | [Validation pure du profil d'occultation v1](../../specs/audit/spec.md#L120) | L | Structure invalide refusée sans écho |
| audit / 129 | [Limites des garanties du profil d'occultation v1](../../specs/audit/spec.md#L129) | L | Profil distinct d'une occultation effective |
| audit / 138 | [Portée préparatoire de la projection décision et audit v1](../../specs/audit/spec.md#L138) | L | Projection distincte d’un audit réalisé ; Obligations et exceptions conservées |
| audit / 153 | [Limites de la projection décision et audit v1](../../specs/audit/spec.md#L153) | L | Aucune ouverture runtime |
| audit / 162 | [Portée limitée de l'acquittement observé du port audit v1](../../specs/audit/spec.md#L162) | L | Retour du port distinct d'une preuve persistante |
| audit / 172 | [Exclusions de l'invocation préparatoire du port audit v1](../../specs/audit/spec.md#L172) | L | Contrats étrangers conservés |
| audit / 182 | [Contrats d'audit et projection pure conservés v1](../../specs/audit/spec.md#L182) | L | Projection seule sans invocation |
| authorization-engine / 161 | [Profil préparatoire fermé source-filter-plan-v1](../../specs/authorization-engine/spec.md#L161) | L | Profil de filtrage sans rupture du PDP |
| authorization-engine / 170 | [Entrées homogènes de source-filter-plan-v1](../../specs/authorization-engine/spec.md#L170) | L | Hétérogénéité refusée |
| authorization-engine / 179 | [Limite explicite et lot vide de source-filter-plan-v1](../../specs/authorization-engine/spec.md#L179) | L | Limite dépassée ; Lot vide admis |
| authorization-engine / 193 | [Évaluation par ressource de source-filter-plan-v1](../../specs/authorization-engine/spec.md#L193) | L | Lot mixte ALLOW et DENY |
| authorization-engine / 202 | [Résultat déclaratif de source-filter-plan-v1](../../specs/authorization-engine/spec.md#L202) | L | Lot avec DENY seul ; Tri et déduplication ; Expiration minimum |
| authorization-engine / 221 | [Échec fermé du lot de source-filter-plan-v1](../../specs/authorization-engine/spec.md#L221) | L | Booléen comme entier refusé ; Erreur backend fermée |
| authorization-engine / 235 | [Fraîcheur et invalidation de source-filter-plan-v1](../../specs/authorization-engine/spec.md#L235) | L | Plan distinct d'une autorisation courante |
| authorization-engine / 244 | [Frontières préparatoires de source-filter-plan-v1](../../specs/authorization-engine/spec.md#L244) | L | Doubles mémoire sans preuve de P0 |
| authorization-engine / 253 | [Structure préparatoire AuditDecisionProjectionV1](../../specs/authorization-engine/spec.md#L253) | L | Deux objets originaux conservés |
| authorization-engine / 263 | [Types exacts des événements de la projection audit v1](../../specs/authorization-engine/spec.md#L263) | L | Objets étrangers refusés avant accès |
| authorization-engine / 273 | [Sous-ensemble PDP complet de la projection audit v1](../../specs/authorization-engine/spec.md#L273) | L | Décision incomplète refusée |
| authorization-engine / 283 | [Effet et motif cohérents de la projection audit v1](../../specs/authorization-engine/spec.md#L283) | L | Deux correspondances fermées ; Motif incohérent refusé |
| authorization-engine / 298 | [Version de politique et instant explicites de la projection audit v1](../../specs/authorization-engine/spec.md#L298) | L | Version ou instant incomplet refusé ; Version politique indépendante |
| authorization-engine / 313 | [Validation de l’événement générique fourni pour la projection audit v1](../../specs/authorization-engine/spec.md#L313) | L | Instant divergent refusé ; Notations UTC équivalentes |
| authorization-engine / 328 | [Correspondances métier de la projection audit v1](../../specs/authorization-engine/spec.md#L328) | L | Cible ou résultat divergent refusé |
| authorization-engine / 338 | [Correspondance tenant de la projection audit v1](../../specs/authorization-engine/spec.md#L338) | L | Tenant exact requis ; Plateforme sans tenant |
| authorization-engine / 353 | [Corrélation et causalité de la projection audit v1](../../specs/authorization-engine/spec.md#L353) | L | Référence requise absente ; Ordre et références conservés |
| authorization-engine / 368 | [Métadonnées indépendantes de la projection audit v1](../../specs/authorization-engine/spec.md#L368) | L | Métadonnées sans inférence |
| authorization-engine / 378 | [Diagnostics et pureté de la projection audit v1](../../specs/authorization-engine/spec.md#L378) | L | Refus sans écho ni effet ; Erreur inattendue non masquée |
| authorization-engine / 392 | [Validation préalable de la projection audit avant invocation v1](../../specs/authorization-engine/spec.md#L392) | L | Projection invalide refusée avant le port |
| authorization-engine / 402 | [Erreurs du validateur de projection audit propagées v1](../../specs/authorization-engine/spec.md#L402) | L | Erreur inattendue du validateur propagée |
| authorization-engine / 412 | [Invocation unique du port pour une projection audit valide v1](../../specs/authorization-engine/spec.md#L412) | L | Projection valide transmise une fois |
| authorization-engine / 422 | [Acquittement booléen exact du port audit v1](../../specs/authorization-engine/spec.md#L422) | L | Retour True exact reconnu ; Autre retour refusé sans coercition |
| authorization-engine / 437 | [Exceptions du port audit sans relance v1](../../specs/authorization-engine/spec.md#L437) | L | Exception du port sans relance ; Interruption système propagée |
| authorization-engine / 452 | [Frontières de l'invocation du port audit v1](../../specs/authorization-engine/spec.md#L452) | L | Deux invocations explicites distinctes |
| capabilities / 8 | [Descripteur de capacité résolu à la composition](../../specs/capabilities/spec.md#L8) | P | Résolution indépendante de l'ordre |
| capabilities / 17 | [États de disponibilité distincts](../../specs/capabilities/spec.md#L17) | P | Capacité optionnelle indisponible isolée |
| capabilities / 28 | [Fanion ne remplace pas la résolution](../../specs/capabilities/spec.md#L28) | P | Fanion sans fournisseur refusé |
| capabilities / 37 | [Résolution sur version déclarée](../../specs/capabilities/spec.md#L37) | P | Identifiant seul sans dispense de conformité |
| capabilities / 51 | [Sélection du fournisseur sur la version de capacité](../../specs/capabilities/spec.md#L51) | P | Fournisseur configuré incompatible refusé |
| compatibility / 8 | [Contraintes de version déclarées et vérifiées](../../specs/compatibility/spec.md#L8) | P | Contrainte insatisfaite à l'activation |
| compatibility / 17 | [Aucune compatibilité présumée](../../specs/compatibility/spec.md#L17) | P | Version supérieure non testée |
| compatibility / 26 | [Matrice de compatibilité globale](../../specs/compatibility/spec.md#L26) | P | État bloqué déterministe |
| compatibility / 35 | [Compatibilité déclarative distincte de la conformité comportementale](../../specs/compatibility/spec.md#L35) | P | Déclaration sans conformité |
| compatibility / 44 | [Coexistence pendant les montées de version](../../specs/compatibility/spec.md#L44) | P | Suppression prématurée |
| compatibility / 53 | [Contraintes de contrats sur versions exactes déclarées](../../specs/compatibility/spec.md#L53) | L | Contrat implémenté en version incompatible |
| compatibility / 66 | [Preuve de conformité externe](../../specs/compatibility/spec.md#L66) | L | Attestation externe sans contenu de rapport |
| compatibility / 81 | [Liaison exacte des attestations de conformité](../../specs/compatibility/spec.md#L81) | L | Métadonnées de build dans la liaison de preuve |
| compatibility / 98 | [Couverture des attestations avant activation](../../specs/compatibility/spec.md#L98) | L | Activation sans preuve refusée ; Preuve d'un autre fournisseur ou d'une autre version refusée ; Preuves concordantes autorisant l'activation |
| compatibility / 123 | [Responsabilités de l'appelant et du noyau pour les preuves](../../specs/compatibility/spec.md#L123) | P | Preuve authentifiée par l'appelant |
| compatibility / 137 | [Matrice P0 limitée aux dimensions connues](../../specs/compatibility/spec.md#L137) | L | Dimension inconnue non évaluée |
| component-model / 8 | [Types de composants unifiés](../../specs/component-model/spec.md#L8) | P | Sous-module validé comme module ; Facette frontend d'un sous-module |
| component-model / 22 | [Manifest déclaratif unique](../../specs/component-model/spec.md#L22) | L | Secret dans le manifest rejeté |
| component-model / 31 | [Schéma de manifest versionné et validable](../../specs/component-model/spec.md#L31) | L | Version de schéma inconnue |
| component-model / 43 | [Identifiants stables namespacés](../../specs/component-model/spec.md#L43) | L | Collision d'identifiants refusée |
| component-model / 54 | [États de composition, installation et santé distincts](../../specs/component-model/spec.md#L54) | P | États non assimilés |
| component-model / 63 | [Manifest schéma 1 — capacités et contrats versionnés](../../specs/component-model/spec.md#L63) | L | Descripteur de capacité du schéma 1 |
| component-model / 78 | [Manifest schéma 1 — propriétaire et contrats exacts](../../specs/component-model/spec.md#L78) | L | Propriétaire dérivé du composant |
| component-model / 89 | [Manifest schéma 1 — listes de dépendances](../../specs/component-model/spec.md#L89) | L | Dépendances selon la grammaire commune |
| component-model / 103 | [Manifest schéma 1 — refus des anciennes déclarations](../../specs/component-model/spec.md#L103) | L | Capacité fournie sans version refusée |
| contracts / 8 | [Catégories de contrats non interchangeables](../../specs/contracts/spec.md#L8) | L | Événement au lieu d'une commande refusé |
| contracts / 17 | [Versionnement SemVer indépendant](../../specs/contracts/spec.md#L17) | P | Champ obligatoire ajouté |
| contracts / 26 | [Dépréciation et retrait encadrés](../../specs/contracts/spec.md#L26) | P | Suppression anticipée bloquée |
| core / 40 | [Profil minimal des utilisateurs et identités numériques v1](../../specs/core/spec.md#L40) | L | Identité minimale valide ; Identifiant ou vocabulaire invalide |
| core / 59 | [Liaison utilisateur identité explicite et unique](../../specs/core/spec.md#L59) | L | Entités indépendantes et liaison explicite ; Cardinalité violée ou référence absente |
| core / 79 | [Représentation minimale des comptes de service](../../specs/core/spec.md#L79) | L | Compte de service sans utilisateur |
| core / 91 | [Frontière des validateurs du profil identité](../../specs/core/spec.md#L91) | L | Validation structurelle sans effet applicatif |
| data-lifecycle / 33 | [Vocabulaire commun des stratégies de suppression](../../specs/data-lifecycle/spec.md#L33) | L | Vocabulaire déclaratif distinct de la persistance |
| data-lifecycle / 61 | [Profil structurel préparatoire de tombstone v1](../../specs/data-lifecycle/spec.md#L61) | L | Structure valide sans effet |
| data-lifecycle / 70 | [Référence, version et instant du profil tombstone-v1](../../specs/data-lifecycle/spec.md#L70) | L | Version et instant du tombstone structurel |
| data-lifecycle / 79 | [Références optionnelles du profil tombstone-v1](../../specs/data-lifecycle/spec.md#L79) | L | Références opaques sans exemption |
| data-lifecycle / 88 | [Validation pure du profil tombstone-v1](../../specs/data-lifecycle/spec.md#L88) | L | Structure invalide refusée sans écho |
| data-lifecycle / 97 | [Limites des garanties du profil tombstone-v1](../../specs/data-lifecycle/spec.md#L97) | L | Tombstone structurel distinct d'une preuve d'effacement |
| deb-package / 8 | [Paquet corrélé à la release](../../specs/deb-package/spec.md#L8) | ND | Version de paquet incohérente ; Deux paquets indépendants |
| deb-package / 22 | [Configuration et secrets hors paquet](../../specs/deb-package/spec.md#L22) | ND | Secret trouvé dans le paquet |
| deb-package / 31 | [Services alignés sur le lifecycle Pixs](../../specs/deb-package/spec.md#L31) | ND | Redémarrage par le gestionnaire de services |
| deb-package / 40 | [Mise à niveau du paquet sous validation](../../specs/deb-package/spec.md#L40) | ND | Mise à niveau interrompue |
| deb-package / 49 | [Aucune installation de code distant implicite](../../specs/deb-package/spec.md#L49) | ND | Téléchargement proposé à l'installation |
| deb-package / 58 | [Distribution Debian indépendante PA et PBO PFO](../../specs/deb-package/spec.md#L58) | ND | Distribution Debian indépendante PA et PBO PFO |
| deb-package / 67 | [Quatre binaires dans le paquet PA](../../specs/deb-package/spec.md#L67) | ND | Quatre binaires dans le paquet PA |
| dependencies / 8 | [Dépendances déclarées typées](../../specs/dependencies/spec.md#L8) | L | Optionnelle absente tolérée |
| dependencies / 17 | [Cycles et incompatibilités refusés](../../specs/dependencies/spec.md#L17) | L | Cycle détecté |
| dependencies / 28 | [Ordre de chargement déterministe](../../specs/dependencies/spec.md#L28) | L | Double composition identique |
| dependencies / 37 | [Graphe frontend récursif et façades publiques](../../specs/dependencies/spec.md#L37) | P | Import privé d'un parent refusé |
| dependencies / 46 | [Grammaire des contraintes de version](../../specs/dependencies/spec.md#L46) | L | Conjonction de comparateurs explicites |
| dependencies / 60 | [Sémantique et refus des contraintes de version](../../specs/dependencies/spec.md#L60) | L | Contrainte malformée refusée |
| dependencies / 73 | [Évaluation sur versions propres](../../specs/dependencies/spec.md#L73) | L | Contrainte de capacité insatisfaite |
| dependencies / 87 | [Incompatibilités obligatoires et optionnelles](../../specs/dependencies/spec.md#L87) | L | Optionnelle incompatible isolée |
| developer-experience / 10 | [Parcours local reproductible](../../specs/developer-experience/spec.md#L10) | P | Premier composant local |
| developer-experience / 21 | [Génération sans activation implicite](../../specs/developer-experience/spec.md#L21) | P | Scaffolding d'un provider |
| developer-experience / 32 | [Diagnostics sans fuite](../../specs/developer-experience/spec.md#L32) | P | Manifest incomplet |
| extension-contracts / 8 | [Points d'extension publics versionnés](../../specs/extension-contracts/spec.md#L8) | P | Contribution sans point déclaré rejetée |
| extension-contracts / 17 | [Contributions déclarées et isolées](../../specs/extension-contracts/spec.md#L17) | P | Accès privé bloqué |
| extension-contracts / 26 | [Niveau de confiance des extensions](../../specs/extension-contracts/spec.md#L26) | P | Extension de développement en production |
| extension-contracts / 38 | [Collisions et composition déterministe](../../specs/extension-contracts/spec.md#L38) | P | Deux routes en collision |
| extension-contracts / 47 | [Composition interface au build](../../specs/extension-contracts/spec.md#L47) | P | Code distant implicite refusé |
| extension-contracts / 56 | [Frontières publiques des composants frontend imbriqués](../../specs/extension-contracts/spec.md#L56) | P | Slot enfant non déclaré |
| frontend / 46 | [Vocabulaire structurel préparatoire FrontendContributionType v1](../../specs/frontend/spec.md#L46) | L | Nom admis dans le profil v1 ; Nom hors profil v1 refusé |
| frontend / 60 | [Syntaxe lexicale préparatoire FrontendEntryPath v1](../../specs/frontend/spec.md#L60) | L | Chemin relatif reconnu lexicalement ; Forme hors profil refusée |
| frontend / 74 | [Limites du contrôle lexical FrontendEntryPath v1](../../specs/frontend/spec.md#L74) | L | Résultat lexical sans effet ni preuve physique |
| frontend / 83 | [Syntaxe lexicale préparatoire FrontendContributionId v1](../../specs/frontend/spec.md#L83) | L | Identifiant namespacé reconnu lexicalement ; Forme hors profil refusée |
| frontend / 97 | [Limites du contrôle lexical FrontendContributionId v1](../../specs/frontend/spec.md#L97) | L | Résultat lexical sans effet ni preuve de propriété |
| frontend / 106 | [Champs de la déclaration préparatoire FrontendContributionDeclaration v1](../../specs/frontend/spec.md#L106) | L | Déclaration structurelle bien formée ; Champ obligatoire absent ou invalide |
| frontend / 120 | [Dépendances et catégorie de périmètre de la déclaration frontend v1](../../specs/frontend/spec.md#L120) | L | Dépendances déclaratives selon la grammaire commune ; Grammaire ou catégorie inconnue refusée |
| frontend / 134 | [Préservation et immutabilité de la déclaration frontend v1](../../specs/frontend/spec.md#L134) | L | Valeurs conservées sans mutation |
| frontend / 143 | [Limites du profil préparatoire de déclaration frontend v1](../../specs/frontend/spec.md#L143) | L | Namespace réservé reconnu lexicalement seulement ; Contrôle sans effets sous gardes |
| frontend / 157 | [Conteneur préparatoire FrontendManifestFacet v1](../../specs/frontend/spec.md#L157) | L | Facette v1 structurée reconnue ; Forme ou version hors profil refusée |
| frontend / 171 | [Rattachement de la facette frontend au composant commun](../../specs/frontend/spec.md#L171) | L | Manifest historique sans facette ; Type de composant hors périmètre |
| frontend / 185 | [Déclarations de contribution sérialisées sans transformation](../../specs/frontend/spec.md#L185) | L | Déclarations ordonnées préservées ; Déclaration hors profil refusée |
| frontend / 199 | [Limites de la facette préparatoire frontend v1](../../specs/frontend/spec.md#L199) | L | Reconnaissance sans effet runtime |
| identity-assurance / 48 | [Vocabulaire structurel préparatoire IdentityAssurance v1](../../specs/identity-assurance/spec.md#L48) | L | Valeurs fermées sans effet ; Valeur étrangère refusée ; Absence sans défaut implicite |
| initial-application-bootstrap / 11 | [Composition Django initiale déclarée](../../specs/initial-application-bootstrap/spec.md#L11) | P | Composition initiale valide |
| initial-application-bootstrap / 27 | [Configuration sensible de la composition Django initiale](../../specs/initial-application-bootstrap/spec.md#L27) | P | Connexion fournie par configuration runtime |
| initial-application-bootstrap / 39 | [Surface HTTP initiale minimale](../../specs/initial-application-bootstrap/spec.md#L39) | P | Route initiale non déclarée |
| initial-application-bootstrap / 54 | [Shell TanStack initial intégré](../../specs/initial-application-bootstrap/spec.md#L54) | P | Démarrage du shell initial |
| initial-application-bootstrap / 68 | [Profil de test intégré isolé](../../specs/initial-application-bootstrap/spec.md#L68) | P | Vérification locale conjointe |
| kernel / 8 | [Noyau sans logique métier](../../specs/kernel/spec.md#L8) | P | Démarrage minimal sans modèle métier |
| kernel / 17 | [Noyau fournit des registres génériques](../../specs/kernel/spec.md#L17) | P | Résolution déterministe |
| kernel / 26 | [Noyau agnostique aux fournisseurs](../../specs/kernel/spec.md#L26) | P | Module ajouté sans modification du noyau |
| kernel / 35 | [Composition ambiguë refusée explicitement](../../specs/kernel/spec.md#L35) | P | Deux fournisseurs sans sélection |
| performance / 8 | [Mesurer avant d'optimiser](../../specs/performance/spec.md#L8) | NE | Optimisation non mesurée |
| performance / 17 | [Budgets déclarés et vérifiés](../../specs/performance/spec.md#L17) | NE | Régression détectée |
| performance / 26 | [Objectifs propres au profil](../../specs/performance/spec.md#L26) | NE | Budget hors profil |
| performance / 38 | [Aucune performance au prix des invariants](../../specs/performance/spec.md#L38) | NE | Cache court-circuitant l'autorisation |
| performance / 47 | [Caches et projections dérivés non autoritaires](../../specs/performance/spec.md#L47) | NE | Cache périmé indisponible |
| providers / 8 | [Déclaration lisible des fournisseurs](../../specs/providers/spec.md#L8) | P | Implémentation non déclarée |
| providers / 17 | [Sélection explicite sans choix implicite](../../specs/providers/spec.md#L17) | P | Deux candidats sans configuration |
| providers / 26 | [Conformité contractuelle vérifiable](../../specs/providers/spec.md#L26) | P | Fournisseur non conforme activé |
| providers / 35 | [Dégradation contrôlée et diagnostic](../../specs/providers/spec.md#L35) | P | Indisponibilité d'un fournisseur |
| reference-composition / 10 | [Capacités obligatoires du P0](../../specs/reference-composition/spec.md#L10) | P | Capacité P0 absente |
| reference-composition / 22 | [Capacités hors P0 explicites](../../specs/reference-composition/spec.md#L22) | P | Synchronisation non sélectionnée |
| reference-composition / 33 | [Preuve reproductible](../../specs/reference-composition/spec.md#L33) | P | Deux validations identiques |
| reference-runtime / 10 | [Pile de référence unique](../../specs/reference-runtime/spec.md#L10) | P | Runtime décrit ; Réseau désactivé |
| reference-runtime / 24 | [Adapter explicite](../../specs/reference-runtime/spec.md#L24) | P | Runtime alternatif non déclaré |
| reference-runtime / 35 | [Absence de sélection cachée](../../specs/reference-runtime/spec.md#L35) | P | Paquet alternatif présent |
| reference-runtime / 45 | [Version stable actuelle de Django](../../specs/reference-runtime/spec.md#L45) | P | Nouvelle version stable officielle |
| reference-runtime / 58 | [Adaptation complète à la stable Django ciblée](../../specs/reference-runtime/spec.md#L58) | P | Migration encore non qualifiée |
| reference-runtime / 69 | [Relevé et qualification de la stable courante](../../specs/reference-runtime/spec.md#L69) | P | Relevé horodaté |
| reference-runtime / 82 | [Qualification reproductible et politique sans dérogation](../../specs/reference-runtime/spec.md#L82) | P | Build reproductible et nouvelle qualification |
| reference-runtime / 96 | [Dépendances Python les plus récentes compatibles avec Django](../../specs/reference-runtime/spec.md#L96) | P | Version imposée par Django |
| reference-runtime / 108 | [Versions exactes, plages et bornes minimales Django](../../specs/reference-runtime/spec.md#L108) | P | Plage et borne minimale |
| reference-runtime / 119 | [Qualification du graphe Python et incompatibilités explicites](../../specs/reference-runtime/spec.md#L119) | P | Graphe incompatible ou contrainte absente |
| reference-runtime / 133 | [Absence d'installation forcée ou de recul Django](../../specs/reference-runtime/spec.md#L133) | P | Version de dépendance refusée par Django |
| reference-runtime / 144 | [Compatibilité avec le Python actuel du projet](../../specs/reference-runtime/spec.md#L144) | P | Version compatible ; Incompatibilité avec Python actuel ; Solution validée par le développeur |
| reference-runtime / 168 | [Couche exécutable PA séparée](../../specs/reference-runtime/spec.md#L168) | P | Couche exécutable PA séparée |
| release-management / 8 | [Définition et support d'une release](../../specs/release-management/spec.md#L8) | ND | Release sans déclaration de support |
| release-management / 17 | [Chemin de migration vérifiable](../../specs/release-management/spec.md#L17) | ND | Saut non prouvé |
| release-management / 26 | [Mise à niveau orchestrée par prévalidations](../../specs/release-management/spec.md#L26) | ND | Étape de prévalidation échouée |
| release-management / 35 | [Coexistence transitoire N et N+1](../../specs/release-management/spec.md#L35) | ND | Contraction pendant la fenêtre |
| release-management / 44 | [Retour arrière soumis à la matrice](../../specs/release-management/spec.md#L44) | ND | Retour arrière non garanti |
| release-management / 55 | [Activation, retrait et instance non valide](../../specs/release-management/spec.md#L55) | ND | Instance échouant aux contrôles |
| resilience / 8 | [Isolation des défaillances optionnelles](../../specs/resilience/spec.md#L8) | NE | Fournisseur optionnel en panne isolé |
| resilience / 17 | [Dégradation sans affaiblissement sécurité](../../specs/resilience/spec.md#L17) | NE | Dégradé sans permissivité |
| resilience / 26 | [Révocation et diagnostic des compromissions](../../specs/resilience/spec.md#L26) | NE | Composant compromis bloqué |
| secrets-providers / 11 | [Références externes sans valeur persistée](../../specs/secrets-providers/spec.md#L11) | P | Diagnostic de référence indisponible |
| secrets-providers / 22 | [Accès runtime associé à une identité de workload](../../specs/secrets-providers/spec.md#L22) | P | Worker non autorisé |
| secrets-providers / 33 | [Rotation, durée de vie et révocation contrôlées](../../specs/secrets-providers/spec.md#L33) | P | Secret tourné |
| secrets-providers / 47 | [Audit minimisé et échec fermé](../../specs/secrets-providers/spec.md#L47) | P | Provider indisponible |
| service-objectives / 10 | [Objectifs versionnés](../../specs/service-objectives/spec.md#L10) | NE | Objectif de reprise déclaré |
| service-objectives / 21 | [Absence de seuil universel implicite](../../specs/service-objectives/spec.md#L21) | NE | Mesure locale isolée |
| service-objectives / 32 | [Validation reproductible](../../specs/service-objectives/spec.md#L32) | NE | Objectif non satisfait |
| services / 8 | [Enregistrement contractuel des services](../../specs/services/spec.md#L8) | P | Service privé non exposé |
| services / 17 | [Résolution déterministe du fournisseur](../../specs/services/spec.md#L17) | P | Ambiguïté refusée |
| services / 28 | [Traçabilité et sécurité des appels](../../specs/services/spec.md#L28) | P | Contexte non vérifiable |
| testing / 8 | [Trois niveaux de vérification distincts](../../specs/testing/spec.md#L8) | P | Unitaires verts, intégration rouge |
| testing / 17 | [Kit de conformité et composant d'exemple](../../specs/testing/spec.md#L17) | P | Exemple P0 validé |
| testing / 30 | [Suites de conformité versionnées par contrat](../../specs/testing/spec.md#L30) | P | Certification expirée |
| testing / 39 | [Garanties obligatoires séparées des capacités optionnelles](../../specs/testing/spec.md#L39) | P | Isolement acceptable |
| testing / 48 | [Reproductibilité sur la topologie de référence](../../specs/testing/spec.md#L48) | P | Divergence de topologie |
| testing / 57 | [Preuves sans secret ni donnée de production](../../specs/testing/spec.md#L57) | P | Secret détecté dans un rapport |
| testing / 66 | [Conformité de la composition frontend récursive](../../specs/testing/spec.md#L66) | P | Composition reproductible avec sous-module |
| testing / 75 | [Conformité des projections d'annuaire optionnelles](../../specs/testing/spec.md#L75) | P | Repli conforme sans élargissement de droits |
| testing / 89 | [Exécution navigateur headless des unités frontend web](../../specs/testing/spec.md#L89) | P | Les deux moteurs déclarent les cas ; Moteur manquant ou cas non exécuté |

## Empreintes SHA-256 du canon

- `openspec/specs/artifact-publication/spec.md` : `7888cada73c3beff836fe2bd6dd6a62b166af317e7036680fb6a1f9e248a5b1f`.
- `openspec/specs/audit/spec.md` : `43d8dd9947fbac84c5decbf829825db577276853f5224e5bacc021c22bf4f513`.
- `openspec/specs/authorization-engine/spec.md` : `bd9de765f72d4700da314f81dbce9d3d0ee532f3bcc5be319f005ffbfd18b20b`.
- `openspec/specs/capabilities/spec.md` : `e9c0328da863d9fda5c128e339ab59e23fa3ca8b1a0cc3379ce1e014334975aa`.
- `openspec/specs/compatibility/spec.md` : `aee6de57607e95e8442b59155cf893f4ef7454db6a0ba60fbfbd9abe360eb544`.
- `openspec/specs/component-model/spec.md` : `6972572f92f9f020b89f5cf8e81ead65005fa858695a838089dd27fd4200b3ae`.
- `openspec/specs/contracts/spec.md` : `ad08fabc8ff78db8678ec873c9c50235b57fdf2554111d48adf57f274e4a3897`.
- `openspec/specs/core/spec.md` : `d0eb213fa2fbb3ccca042133d910166b35f4a3e8e60178ad02b12420034bada3`.
- `openspec/specs/data-lifecycle/spec.md` : `a3498cc4d3622d569fc9e3f8251a5c5324a9b3d1c612fe014618146297083426`.
- `openspec/specs/deb-package/spec.md` : `46730b2c3505085325539b6ae2386806e5b59bb19aa46adf5f4571335d016e64`.
- `openspec/specs/dependencies/spec.md` : `ca3f3276a1e741fb987fa690356b89e4c3e8b3e52717451264179b8e7e16cca7`.
- `openspec/specs/developer-experience/spec.md` : `9008a4c9affc2e6dc13c7247fd375c349a8d85fa2733878756dd27373ad8e4b1`.
- `openspec/specs/extension-contracts/spec.md` : `f7d5d14c29aeb97aad6780413d5560686264a3cc3f97b29eca907182166f90eb`.
- `openspec/specs/frontend/spec.md` : `e646e3faf793db109a93f803423cfa4606deeb67b91d4b3301fa219e82cf9414`.
- `openspec/specs/identity-assurance/spec.md` : `61ad48e4c2899ed6a270d36e09609d7c62fbae58c97179ba42acbc41ae0654e6`.
- `openspec/specs/initial-application-bootstrap/spec.md` : `688063fbafcd34535d87b7f4920d8e4952ff2ed3267bd5b442400a3d9f0fe3a4`.
- `openspec/specs/kernel/spec.md` : `af511f0aa57aeb5b5a919404fb15255ab1492fc8ff4ac7b2e6e90b09cbf45127`.
- `openspec/specs/performance/spec.md` : `da1e316cc46da6f8990b47d826cba522d72e81888df9f4ea08bae49451399916`.
- `openspec/specs/providers/spec.md` : `5aceaa82194cfc9802dcf6ef1bd9e4fc35b18b5156d1b29685e41d23689a7fd7`.
- `openspec/specs/reference-composition/spec.md` : `7c4d7b603f35f02f6d2ba0eb10dd202793ec288fee0c65a5ff15d244446233ff`.
- `openspec/specs/reference-runtime/spec.md` : `4bbbc0451013b7139f3898b4a5aebd592ab1c50b6aa6cce4e1246957e4052351`.
- `openspec/specs/release-management/spec.md` : `0fd7fc3720214df3741c8eed94e0db460b2fd67101cee3310c08b952672f6e3f`.
- `openspec/specs/resilience/spec.md` : `b32b0eff946a12be7ee217c5bc2ffe19b763fe015b0dcb4b46c9e8254f43d1f3`.
- `openspec/specs/secrets-providers/spec.md` : `8e134d9117ca775984f14c91fb75e042fdf7612b8f6f81a336be93b8673b1dff`.
- `openspec/specs/service-objectives/spec.md` : `80c0a0888df5e5da8ec65f23d39171224421ae8ac5bf99ebf17e198a3d505e42`.
- `openspec/specs/services/spec.md` : `e754ac950e612d335017122e23e55d75d3fb214f927fabcb2d48da8722013c37`.
- `openspec/specs/testing/spec.md` : `5e0c976821f8623c976d43125c7d5738fbf100b9fae1a112d45894e9fdc7a148`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
