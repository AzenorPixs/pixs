# Exigences de réalisation — C07

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 adopté le 18 octobre 2026 et intégré au canon apporte les précisions de première livraison ; il ne supprime aucun MUST existant.

Relecture documentaire du 21 octobre 2026 : les lignes, intitulés, scénarios et empreintes ci-dessous désignent le canon courant, y compris l’adoption Auth/Core et les précisions du profil initial et de PA/PZT. Une dérive impose une nouvelle lecture avant réalisation. Le statut P conserve le constat historique de la matrice ; N/A — ajout à la traçabilité désigne une clause ajoutée à cette table, sans inventer son statut dans la matrice ni son verdict fonctionnel.

C07 consomme les contrats publics Core/Auth et d’audit ; les scénarios de leurs services restent à qualifier chez leurs propriétaires C02/C03/C05 et lors de l’intégration. Leur présence dans cette table n’étend pas C07 à la réalisation de ces services. Les exécutants PA/PZT restent hors sélection de cette reprise documentaire ; leurs obligations de séparation et celles des modules essentiels de gestion demeurent applicables à la composition.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| authentication / 40 | [Module essentiel autonome pixs.auth](../../../specs/authentication/spec.md#L40) | N/A — ajout à la traçabilité | Composition applicative sans Auth ; Fixture structurelle isolée |
| authentication / 52 | [Autonomie locale et PostgreSQL par défaut](../../../specs/authentication/spec.md#L52) | N/A — ajout à la traçabilité | Installation autonome ; PostgreSQL indisponible |
| authentication / 64 | [Propriété des données Auth et protection des justificatifs](../../../specs/authentication/spec.md#L64) | N/A — ajout à la traçabilité | Session persistée ; Liaison avec Core |
| authentication / 76 | [Sous-modules Auth composés par les mécanismes communs](../../../specs/authentication/spec.md#L76) | N/A — ajout à la traçabilité | Source installée sans confiance |
| capabilities / 8 | [Descripteur de capacité résolu à la composition](../../../specs/capabilities/spec.md#L8) | P | Résolution indépendante de l'ordre |
| capabilities / 17 | [États de disponibilité distincts](../../../specs/capabilities/spec.md#L17) | P | Capacité optionnelle indisponible isolée |
| capabilities / 28 | [Fanion ne remplace pas la résolution](../../../specs/capabilities/spec.md#L28) | P | Fanion sans fournisseur refusé |
| capabilities / 37 | [Résolution sur version déclarée](../../../specs/capabilities/spec.md#L37) | P | Identifiant seul sans dispense de conformité |
| capabilities / 51 | [Sélection du fournisseur sur la version de capacité](../../../specs/capabilities/spec.md#L51) | P | Fournisseur configuré incompatible refusé |
| compatibility / 8 | [Contraintes de version déclarées et vérifiées](../../../specs/compatibility/spec.md#L8) | P | Contrainte insatisfaite à l'activation |
| compatibility / 17 | [Aucune compatibilité présumée](../../../specs/compatibility/spec.md#L17) | P | Version supérieure non testée |
| compatibility / 26 | [Matrice de compatibilité globale](../../../specs/compatibility/spec.md#L26) | P | État bloqué déterministe |
| compatibility / 35 | [Compatibilité déclarative distincte de la conformité comportementale](../../../specs/compatibility/spec.md#L35) | P | Déclaration sans conformité |
| compatibility / 44 | [Coexistence pendant les montées de version](../../../specs/compatibility/spec.md#L44) | P | Suppression prématurée |
| compatibility / 123 | [Responsabilités de l'appelant et du noyau pour les preuves](../../../specs/compatibility/spec.md#L123) | P | Preuve authentifiée par l'appelant |
| component-model / 8 | [Types de composants unifiés](../../../specs/component-model/spec.md#L8) | P | Sous-module validé comme module ; Facette frontend d'un sous-module |
| component-model / 54 | [États de composition, installation et santé distincts](../../../specs/component-model/spec.md#L54) | P | États non assimilés |
| configuration / 8 | [Schémas typés validés avant activation](../../../specs/configuration/spec.md#L8) | P | Configuration invalide bloquée |
| configuration / 17 | [Priorité déterministe des sources](../../../specs/configuration/spec.md#L17) | P | Surcharge déterministe |
| configuration / 28 | [Secrets par référence hors artefacts](../../../specs/configuration/spec.md#L28) | P | Secret embarqué refusé |
| contracts / 17 | [Versionnement SemVer indépendant](../../../specs/contracts/spec.md#L17) | P | Champ obligatoire ajouté |
| contracts / 26 | [Dépréciation et retrait encadrés](../../../specs/contracts/spec.md#L26) | P | Suppression anticipée bloquée |
| core / 8 | [Module obligatoire au-dessus du noyau](../../../specs/core/spec.md#L8) | N/A — ajout à la traçabilité | Composition sans core refusée |
| core / 116 | [Frontière Core Auth et dépendance unidirectionnelle](../../../specs/core/spec.md#L116) | N/A — ajout à la traçabilité | Révocation canonique |
| dependencies / 37 | [Graphe frontend récursif et façades publiques](../../../specs/dependencies/spec.md#L37) | P | Import privé d'un parent refusé |
| extension-contracts / 8 | [Points d'extension publics versionnés](../../../specs/extension-contracts/spec.md#L8) | P | Contribution sans point déclaré rejetée |
| extension-contracts / 17 | [Contributions déclarées et isolées](../../../specs/extension-contracts/spec.md#L17) | P | Accès privé bloqué |
| extension-contracts / 26 | [Niveau de confiance des extensions](../../../specs/extension-contracts/spec.md#L26) | P | Extension de développement en production |
| extension-contracts / 38 | [Collisions et composition déterministe](../../../specs/extension-contracts/spec.md#L38) | P | Deux routes en collision |
| extension-contracts / 47 | [Composition interface au build](../../../specs/extension-contracts/spec.md#L47) | P | Code distant implicite refusé |
| extension-contracts / 56 | [Frontières publiques des composants frontend imbriqués](../../../specs/extension-contracts/spec.md#L56) | P | Slot enfant non déclaré |
| initial-application-bootstrap / 11 | [Composition Django initiale déclarée](../../../specs/initial-application-bootstrap/spec.md#L11) | P | Composition initiale valide |
| initial-application-bootstrap / 27 | [Configuration sensible de la composition Django initiale](../../../specs/initial-application-bootstrap/spec.md#L27) | P | Connexion fournie par configuration runtime |
| initial-application-bootstrap / 39 | [Surface HTTP initiale minimale](../../../specs/initial-application-bootstrap/spec.md#L39) | P | Route initiale non déclarée |
| initial-application-bootstrap / 54 | [Shell TanStack initial intégré](../../../specs/initial-application-bootstrap/spec.md#L54) | P | Démarrage du shell initial |
| kernel / 8 | [Noyau sans logique métier](../../../specs/kernel/spec.md#L8) | P | Démarrage minimal sans modèle métier |
| kernel / 17 | [Noyau fournit des registres génériques](../../../specs/kernel/spec.md#L17) | P | Résolution déterministe |
| kernel / 26 | [Noyau agnostique aux fournisseurs](../../../specs/kernel/spec.md#L26) | P | Module ajouté sans modification du noyau |
| kernel / 35 | [Composition ambiguë refusée explicitement](../../../specs/kernel/spec.md#L35) | P | Deux fournisseurs sans sélection |
| lifecycle / 8 | [États de cycle de vie distincts](../../../specs/lifecycle/spec.md#L8) | P | États non confondus |
| lifecycle / 17 | [Transitions autorisées et refusées](../../../specs/lifecycle/spec.md#L17) | P | Désactivation sans perte et purge explicite |
| lifecycle / 26 | [Ordre déterministe des hooks](../../../specs/lifecycle/spec.md#L26) | P | Double résolution identique |
| lifecycle / 35 | [Idempotence des opérations](../../../specs/lifecycle/spec.md#L35) | P | Rejeu sans double effet |
| lifecycle / 44 | [Diagnostic des échecs](../../../specs/lifecycle/spec.md#L44) | P | Activation invalide bloquée |
| migrations / 8 | [Contrat de migration](../../../specs/migrations/spec.md#L8) | P | Migration sans version cible |
| migrations / 17 | [Planification et ordre déterministes](../../../specs/migrations/spec.md#L17) | P | Deux migrations concurrentes |
| migrations / 26 | [Compatibilité pendant l'application](../../../specs/migrations/spec.md#L26) | P | Coexistence pendant migration |
| migrations / 35 | [Reprise idempotente](../../../specs/migrations/spec.md#L35) | P | Interruption puis reprise |
| migrations / 44 | [Contraction contrôlée](../../../specs/migrations/spec.md#L44) | P | Contraction prématurée |
| modules / 8 | [Manifest lisible obligatoire](../../../specs/modules/spec.md#L8) | P | Manifest incomplet |
| modules / 17 | [Frontière API publique et privée](../../../specs/modules/spec.md#L17) | P | Accès à une API non déclarée |
| modules / 26 | [Propriété des données et migrations associées](../../../specs/modules/spec.md#L26) | P | Changement de schéma non migré |
| modules / 35 | [Chargement contrôlé déterministe](../../../specs/modules/spec.md#L35) | P | Cycle de dépendances |
| modules / 44 | [Propriété des contributions frontend modulaires](../../../specs/modules/spec.md#L44) | P | Sous-module autonome intégré |
| providers / 8 | [Déclaration lisible des fournisseurs](../../../specs/providers/spec.md#L8) | P | Implémentation non déclarée |
| providers / 17 | [Sélection explicite sans choix implicite](../../../specs/providers/spec.md#L17) | P | Deux candidats sans configuration |
| providers / 26 | [Conformité contractuelle vérifiable](../../../specs/providers/spec.md#L26) | P | Fournisseur non conforme activé |
| providers / 35 | [Dégradation contrôlée et diagnostic](../../../specs/providers/spec.md#L35) | P | Indisponibilité d'un fournisseur |
| reference-composition / 10 | [Qualification du binaire commun et des profils de ressources P0](../../../specs/reference-composition/spec.md#L10) | N/A — ajout à la traçabilité | P0 sans exécution réseau ; Plan de ressources sans preuve sur cible |
| reference-composition / 24 | [Capacités obligatoires du P0](../../../specs/reference-composition/spec.md#L24) | P | Capacité P0 absente |
| reference-composition / 33 | [Capacités hors P0 explicites](../../../specs/reference-composition/spec.md#L33) | P | Synchronisation non sélectionnée |
| reference-composition / 44 | [Preuve reproductible](../../../specs/reference-composition/spec.md#L44) | P | Deux validations identiques |
| reference-composition / 55 | [Profil initial PBO PFO Debian local v1](../../../specs/reference-composition/spec.md#L55) | N/A — ajout à la traçabilité | Architecture seulement observée |
| reference-composition / 64 | [Garanties du socle conservées dans le profil initial](../../../specs/reference-composition/spec.md#L64) | N/A — ajout à la traçabilité | Module essentiel absent |
| reference-composition / 73 | [Parcours installable et utilisable du profil initial](../../../specs/reference-composition/spec.md#L73) | N/A — ajout à la traçabilité | Démonstration mémoire seule |
| reference-composition / 82 | [Capacités non sélectionnées du profil initial](../../../specs/reference-composition/spec.md#L82) | N/A — ajout à la traçabilité | Option absente sans dépendance obligatoire |
| reference-composition / 91 | [Preuve de la composition effectivement distribuée](../../../specs/reference-composition/spec.md#L91) | N/A — ajout à la traçabilité | Sources et paquet divergents |
| reference-composition / 100 | [Choix C01 systemd et exception d’amorçage du profil Debian local](../../../specs/reference-composition/spec.md#L100) | N/A — ajout à la traçabilité | Hôte intermédiaire conservé non prêt ; Source locale hors phase autorisée |
| reference-composition / 114 | [Qualification et source de vérité après amorçage](../../../specs/reference-composition/spec.md#L114) | N/A — ajout à la traçabilité | Hôte intermédiaire conservé non prêt ; Source locale hors phase autorisée |
| reference-composition / 128 | [Profil Auth standard sans connecteur externe installé](../../../specs/reference-composition/spec.md#L128) | N/A — ajout à la traçabilité | Profil livré sans connecteurs externes |
| reference-runtime / 12 | [Binaire PBO commun et socle modulaire](../../../specs/reference-runtime/spec.md#L12) | N/A — ajout à la traçabilité | Socle partagé par plusieurs rôles ; Contrats conservés dans un processus |
| reference-runtime / 26 | [Compilation PBO Nuitka standalone](../../../specs/reference-runtime/spec.md#L26) | N/A — ajout à la traçabilité | Distribution autonome complète ; Mode onefile substitué |
| reference-runtime / 40 | [Cython ciblé et mesuré dans PBO](../../../specs/reference-runtime/spec.md#L40) | N/A — ajout à la traçabilité | Optimisation sans preuve ; Gain ciblé qualifié |
| reference-runtime / 54 | [Qualification du binaire PBO](../../../specs/reference-runtime/spec.md#L54) | N/A — ajout à la traçabilité | Compilation sans mesure de performance |
| reference-runtime / 63 | [Pile de référence unique](../../../specs/reference-runtime/spec.md#L63) | P | Runtime décrit ; Réseau désactivé |
| reference-runtime / 77 | [Adapter explicite](../../../specs/reference-runtime/spec.md#L77) | P | Runtime alternatif non déclaré |
| reference-runtime / 88 | [Absence de sélection cachée](../../../specs/reference-runtime/spec.md#L88) | P | Paquet alternatif présent |
| reference-runtime / 98 | [Version stable actuelle de Django](../../../specs/reference-runtime/spec.md#L98) | P | Nouvelle version stable officielle |
| reference-runtime / 111 | [Adaptation complète à la stable Django ciblée](../../../specs/reference-runtime/spec.md#L111) | P | Migration encore non qualifiée |
| reference-runtime / 122 | [Relevé et qualification de la stable courante](../../../specs/reference-runtime/spec.md#L122) | P | Relevé horodaté |
| reference-runtime / 135 | [Qualification reproductible et politique sans dérogation](../../../specs/reference-runtime/spec.md#L135) | P | Build reproductible et nouvelle qualification |
| reference-runtime / 149 | [Dépendances Python les plus récentes compatibles avec Django](../../../specs/reference-runtime/spec.md#L149) | P | Version imposée par Django |
| reference-runtime / 161 | [Versions exactes, plages et bornes minimales Django](../../../specs/reference-runtime/spec.md#L161) | P | Plage et borne minimale |
| reference-runtime / 172 | [Qualification du graphe Python et incompatibilités explicites](../../../specs/reference-runtime/spec.md#L172) | P | Graphe incompatible ou contrainte absente |
| reference-runtime / 186 | [Absence d'installation forcée ou de recul Django](../../../specs/reference-runtime/spec.md#L186) | P | Version de dépendance refusée par Django |
| reference-runtime / 197 | [Compatibilité avec le Python actuel du projet](../../../specs/reference-runtime/spec.md#L197) | P | Version compatible ; Incompatibilité avec Python actuel ; Solution validée par le développeur |
| reference-runtime / 221 | [Couche exécutable PA séparée](../../../specs/reference-runtime/spec.md#L221) | P | Exécutants distincts du backend |
| reference-runtime / 234 | [Modules de gestion pixs.agent et pixs.pzt dans PBO](../../../specs/reference-runtime/spec.md#L234) | N/A — ajout à la traçabilité | Composition des deux modules de gestion ; Réseau désactivé |
| runtime / 23 | [Modes d'exploitation PBO Standalone et ZT](../../../specs/runtime/spec.md#L23) | N/A — ajout à la traçabilité | Exploitation Standalone sans réseau activé ; Exploitation ZT ; Transport PZT en mode Standalone |
| runtime / 42 | [Profil de ressources par environnement d'exécution](../../../specs/runtime/spec.md#L42) | N/A — ajout à la traçabilité | Quota inférieur aux ressources physiques ; Exécutant distant |
| runtime / 56 | [Dimensionnement explicite et borné des processus](../../../specs/runtime/spec.md#L56) | N/A — ajout à la traçabilité | Multiplication des connexions ; Rôle inconnu ou budget invalide |
| runtime / 70 | [Proposition de dimensionnement sous configuration](../../../specs/runtime/spec.md#L70) | N/A — ajout à la traçabilité | Détection sans politique d'adaptation ; Adaptation sous politique |
| runtime / 84 | [Ressources détectées demandées et appliquées distinctes](../../../specs/runtime/spec.md#L84) | N/A — ajout à la traçabilité | Application partielle d'un profil |
| runtime / 93 | [Reconfiguration contrôlée des ressources](../../../specs/runtime/spec.md#L93) | N/A — ajout à la traçabilité | Réduction de workers occupés ; Plusieurs schedulers |
| runtime / 107 | [Budgets compatibles avec les garanties du profil](../../../specs/runtime/spec.md#L107) | N/A — ajout à la traçabilité | Ressources insuffisantes pour une garantie |
| runtime / 116 | [Supervision et qualification des profils de ressources](../../../specs/runtime/spec.md#L116) | N/A — ajout à la traçabilité | Profil sans recette de ressources ; Redémarrage supervisé |
| runtime / 130 | [Profils distincts d'un même artefact](../../../specs/runtime/spec.md#L130) | P | Profil activé par configuration |
| runtime / 139 | [Profils de déploiement déclarés](../../../specs/runtime/spec.md#L139) | P | Capacité absente dans un profil local |
| runtime / 151 | [Exposition minimale par défaut](../../../specs/runtime/spec.md#L151) | P | Endpoint de management publiquement joignable |
| runtime / 160 | [Processus stateless et coordination persistante](../../../specs/runtime/spec.md#L160) | P | Redémarrage d'un worker ; État technique PA requis en conteneur |
| runtime / 174 | [Lease du scheduler avec clôture de péremption](../../../specs/runtime/spec.md#L174) | P | Ancien détenteur toujours actif |
| runtime / 183 | [Arrêt, drain et reprise contrôlés](../../../specs/runtime/spec.md#L183) | P | Arrêt pendant traitement |
| runtime / 192 | [États techniques PA et PZT distincts du runtime PBO](../../../specs/runtime/spec.md#L192) | P | Recréation du conteneur PA PZT |
| runtime / 205 | [Topologies locales et distantes PA PZT](../../../specs/runtime/spec.md#L205) | N/A — ajout à la traçabilité | Hôte local avec tous les composants ; Hôte distant sans backend local ; Hôte distant avec backend local |
| services / 8 | [Enregistrement contractuel des services](../../../specs/services/spec.md#L8) | P | Service privé non exposé |
| services / 17 | [Résolution déterministe du fournisseur](../../../specs/services/spec.md#L17) | P | Ambiguïté refusée |
| services / 28 | [Traçabilité et sécurité des appels](../../../specs/services/spec.md#L28) | P | Contexte non vérifiable |

## Empreintes SHA-256 du canon

- `openspec/specs/authentication/spec.md` : `8c3a41d0f1c5531b9c15954c547b9970261a864812633a2db23944fe2b17ad4a`.
- `openspec/specs/capabilities/spec.md` : `e9c0328da863d9fda5c128e339ab59e23fa3ca8b1a0cc3379ce1e014334975aa`.
- `openspec/specs/compatibility/spec.md` : `aee6de57607e95e8442b59155cf893f4ef7454db6a0ba60fbfbd9abe360eb544`.
- `openspec/specs/component-model/spec.md` : `6972572f92f9f020b89f5cf8e81ead65005fa858695a838089dd27fd4200b3ae`.
- `openspec/specs/configuration/spec.md` : `8e710a2390f044b0d5f78ddf68546e3310eddbb878eea29171ea5608dd425904`.
- `openspec/specs/contracts/spec.md` : `ad08fabc8ff78db8678ec873c9c50235b57fdf2554111d48adf57f274e4a3897`.
- `openspec/specs/core/spec.md` : `1332388a595ac64fcc6ca8ce3fe8e70c9b371a9f038e820ec8ab48364ea92666`.
- `openspec/specs/dependencies/spec.md` : `ca3f3276a1e741fb987fa690356b89e4c3e8b3e52717451264179b8e7e16cca7`.
- `openspec/specs/extension-contracts/spec.md` : `f7d5d14c29aeb97aad6780413d5560686264a3cc3f97b29eca907182166f90eb`.
- `openspec/specs/initial-application-bootstrap/spec.md` : `688063fbafcd34535d87b7f4920d8e4952ff2ed3267bd5b442400a3d9f0fe3a4`.
- `openspec/specs/kernel/spec.md` : `af511f0aa57aeb5b5a919404fb15255ab1492fc8ff4ac7b2e6e90b09cbf45127`.
- `openspec/specs/lifecycle/spec.md` : `e4f8fb1bc340000c2fafed0a6d2862b9ad033d668e89691bfdeb3bf6dc8215d3`.
- `openspec/specs/migrations/spec.md` : `9b3ced385afbeaa7414a1d58752078482e57efa242064e21e7fb4b6fde451efe`.
- `openspec/specs/modules/spec.md` : `7ea4899dff68afd31f22a501e587da4dcad9c911d1689583672678cf108ff37b`.
- `openspec/specs/providers/spec.md` : `5aceaa82194cfc9802dcf6ef1bd9e4fc35b18b5156d1b29685e41d23689a7fd7`.
- `openspec/specs/reference-composition/spec.md` : `53f1d388d6999fcf7af05317a9774d2c4e708a90157fe1666b4210e0d1314a4c`.
- `openspec/specs/reference-runtime/spec.md` : `6bbb170eb652b0b07a7b7dd61775b1cd52284fa7b53b05374c8f3267b089fed7`.
- `openspec/specs/runtime/spec.md` : `130f1c090012bf9180ccee1b4a71926de47183bcf6b69539608a3a8e5e5a73ac`.
- `openspec/specs/services/spec.md` : `e754ac950e612d335017122e23e55d75d3fb214f927fabcb2d48da8722013c37`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.

## Limites des preuves du 21 octobre 2026

Le complément canonique du binaire commun et des profils de ressources est tracé ci-dessus par ses clauses et scénarios actuels. Les recettes C07 présentes ne qualifient ni le binaire Nuitka standalone, ni les budgets CPU/mémoire/concurrence, ni les modes Standalone/ZT du produit. Le transport, le plan et les adapters génériques demeurent des preuves bornées ; Agent/PZT et les attestations des recettes unitaires sont explicitement synthétiques.

La recette native C01 a ensuite réussi après autorisation distincte de sudo sur cet hôte. Le contrôleur UID 0 a créé et arrêté la seule unité temporaire `pixs-c07-c4-entry-0593a443.service` (RuntimeMaxSec 45 s), avec consommateur UID 1000 et fixtures publiques. Les 17 contrôles sont vrais : entrée C01 réelle, journal C01 initialisé et audit confirmé, vrai Django/ASGI, frontières HTTP, contexte actif puis arrêt lifespan et attestation native de quiescence. Le mode `null` qualifie le fonctionnement uniquement ; aucune connexion PostgreSQL ni qualification P0 n’est déduite de cette recette. Les reçus sont attestés par CGPT dans [VALIDATION.md](VALIDATION.md), séparément des preuves natives OpenCode. Les premiers essais en mode utilisateur et sans journal initialisé restent des échecs conservés. Voir la matrice d’application locale dans [VALIDATION.md](VALIDATION.md) : une clause référencée n’est jamais assimilée à un scénario produit exécuté.
