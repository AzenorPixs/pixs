# Exigences de réalisation — C07

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 adopté le 18 octobre 2026 et intégré au canon apporte les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
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
| compatibility / 123 | [Responsabilités de l'appelant et du noyau pour les preuves](../../specs/compatibility/spec.md#L123) | P | Preuve authentifiée par l'appelant |
| component-model / 8 | [Types de composants unifiés](../../specs/component-model/spec.md#L8) | P | Sous-module validé comme module ; Facette frontend d'un sous-module |
| component-model / 54 | [États de composition, installation et santé distincts](../../specs/component-model/spec.md#L54) | P | États non assimilés |
| configuration / 8 | [Schémas typés validés avant activation](../../specs/configuration/spec.md#L8) | P | Configuration invalide bloquée |
| configuration / 17 | [Priorité déterministe des sources](../../specs/configuration/spec.md#L17) | P | Surcharge déterministe |
| configuration / 28 | [Secrets par référence hors artefacts](../../specs/configuration/spec.md#L28) | P | Secret embarqué refusé |
| contracts / 17 | [Versionnement SemVer indépendant](../../specs/contracts/spec.md#L17) | P | Champ obligatoire ajouté |
| contracts / 26 | [Dépréciation et retrait encadrés](../../specs/contracts/spec.md#L26) | P | Suppression anticipée bloquée |
| dependencies / 37 | [Graphe frontend récursif et façades publiques](../../specs/dependencies/spec.md#L37) | P | Import privé d'un parent refusé |
| extension-contracts / 8 | [Points d'extension publics versionnés](../../specs/extension-contracts/spec.md#L8) | P | Contribution sans point déclaré rejetée |
| extension-contracts / 17 | [Contributions déclarées et isolées](../../specs/extension-contracts/spec.md#L17) | P | Accès privé bloqué |
| extension-contracts / 26 | [Niveau de confiance des extensions](../../specs/extension-contracts/spec.md#L26) | P | Extension de développement en production |
| extension-contracts / 38 | [Collisions et composition déterministe](../../specs/extension-contracts/spec.md#L38) | P | Deux routes en collision |
| extension-contracts / 47 | [Composition interface au build](../../specs/extension-contracts/spec.md#L47) | P | Code distant implicite refusé |
| extension-contracts / 56 | [Frontières publiques des composants frontend imbriqués](../../specs/extension-contracts/spec.md#L56) | P | Slot enfant non déclaré |
| initial-application-bootstrap / 11 | [Composition Django initiale déclarée](../../specs/initial-application-bootstrap/spec.md#L11) | P | Composition initiale valide |
| initial-application-bootstrap / 27 | [Configuration sensible de la composition Django initiale](../../specs/initial-application-bootstrap/spec.md#L27) | P | Connexion fournie par configuration runtime |
| initial-application-bootstrap / 39 | [Surface HTTP initiale minimale](../../specs/initial-application-bootstrap/spec.md#L39) | P | Route initiale non déclarée |
| initial-application-bootstrap / 54 | [Shell TanStack initial intégré](../../specs/initial-application-bootstrap/spec.md#L54) | P | Démarrage du shell initial |
| kernel / 8 | [Noyau sans logique métier](../../specs/kernel/spec.md#L8) | P | Démarrage minimal sans modèle métier |
| kernel / 17 | [Noyau fournit des registres génériques](../../specs/kernel/spec.md#L17) | P | Résolution déterministe |
| kernel / 26 | [Noyau agnostique aux fournisseurs](../../specs/kernel/spec.md#L26) | P | Module ajouté sans modification du noyau |
| kernel / 35 | [Composition ambiguë refusée explicitement](../../specs/kernel/spec.md#L35) | P | Deux fournisseurs sans sélection |
| lifecycle / 8 | [États de cycle de vie distincts](../../specs/lifecycle/spec.md#L8) | P | États non confondus |
| lifecycle / 17 | [Transitions autorisées et refusées](../../specs/lifecycle/spec.md#L17) | P | Désactivation sans perte et purge explicite |
| lifecycle / 26 | [Ordre déterministe des hooks](../../specs/lifecycle/spec.md#L26) | P | Double résolution identique |
| lifecycle / 35 | [Idempotence des opérations](../../specs/lifecycle/spec.md#L35) | P | Rejeu sans double effet |
| lifecycle / 44 | [Diagnostic des échecs](../../specs/lifecycle/spec.md#L44) | P | Activation invalide bloquée |
| migrations / 8 | [Contrat de migration](../../specs/migrations/spec.md#L8) | P | Migration sans version cible |
| migrations / 17 | [Planification et ordre déterministes](../../specs/migrations/spec.md#L17) | P | Deux migrations concurrentes |
| migrations / 26 | [Compatibilité pendant l'application](../../specs/migrations/spec.md#L26) | P | Coexistence pendant migration |
| migrations / 35 | [Reprise idempotente](../../specs/migrations/spec.md#L35) | P | Interruption puis reprise |
| migrations / 44 | [Contraction contrôlée](../../specs/migrations/spec.md#L44) | P | Contraction prématurée |
| modules / 8 | [Manifest lisible obligatoire](../../specs/modules/spec.md#L8) | P | Manifest incomplet |
| modules / 17 | [Frontière API publique et privée](../../specs/modules/spec.md#L17) | P | Accès à une API non déclarée |
| modules / 26 | [Propriété des données et migrations associées](../../specs/modules/spec.md#L26) | P | Changement de schéma non migré |
| modules / 35 | [Chargement contrôlé déterministe](../../specs/modules/spec.md#L35) | P | Cycle de dépendances |
| modules / 44 | [Propriété des contributions frontend modulaires](../../specs/modules/spec.md#L44) | P | Sous-module autonome intégré |
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
| runtime / 8 | [Profils distincts d'un même artefact](../../specs/runtime/spec.md#L8) | P | Profil activé par configuration |
| runtime / 17 | [Profils de déploiement déclarés](../../specs/runtime/spec.md#L17) | P | Capacité absente dans un profil local |
| runtime / 29 | [Exposition minimale par défaut](../../specs/runtime/spec.md#L29) | P | Endpoint de management publiquement joignable |
| runtime / 38 | [Processus stateless et coordination persistante](../../specs/runtime/spec.md#L38) | P | Redémarrage d'un worker ; État technique PA requis en conteneur |
| runtime / 52 | [Lease du scheduler avec clôture de péremption](../../specs/runtime/spec.md#L52) | P | Ancien détenteur toujours actif |
| runtime / 61 | [Arrêt, drain et reprise contrôlés](../../specs/runtime/spec.md#L61) | P | Arrêt pendant traitement |
| runtime / 70 | [États techniques PA distincts du runtime PBO](../../specs/runtime/spec.md#L70) | P | États techniques PA distincts du runtime PBO |
| services / 8 | [Enregistrement contractuel des services](../../specs/services/spec.md#L8) | P | Service privé non exposé |
| services / 17 | [Résolution déterministe du fournisseur](../../specs/services/spec.md#L17) | P | Ambiguïté refusée |
| services / 28 | [Traçabilité et sécurité des appels](../../specs/services/spec.md#L28) | P | Contexte non vérifiable |

## Empreintes SHA-256 du canon

- `openspec/specs/capabilities/spec.md` : `e9c0328da863d9fda5c128e339ab59e23fa3ca8b1a0cc3379ce1e014334975aa`.
- `openspec/specs/compatibility/spec.md` : `aee6de57607e95e8442b59155cf893f4ef7454db6a0ba60fbfbd9abe360eb544`.
- `openspec/specs/component-model/spec.md` : `6972572f92f9f020b89f5cf8e81ead65005fa858695a838089dd27fd4200b3ae`.
- `openspec/specs/configuration/spec.md` : `8e710a2390f044b0d5f78ddf68546e3310eddbb878eea29171ea5608dd425904`.
- `openspec/specs/contracts/spec.md` : `ad08fabc8ff78db8678ec873c9c50235b57fdf2554111d48adf57f274e4a3897`.
- `openspec/specs/dependencies/spec.md` : `ca3f3276a1e741fb987fa690356b89e4c3e8b3e52717451264179b8e7e16cca7`.
- `openspec/specs/extension-contracts/spec.md` : `f7d5d14c29aeb97aad6780413d5560686264a3cc3f97b29eca907182166f90eb`.
- `openspec/specs/initial-application-bootstrap/spec.md` : `688063fbafcd34535d87b7f4920d8e4952ff2ed3267bd5b442400a3d9f0fe3a4`.
- `openspec/specs/kernel/spec.md` : `af511f0aa57aeb5b5a919404fb15255ab1492fc8ff4ac7b2e6e90b09cbf45127`.
- `openspec/specs/lifecycle/spec.md` : `e4f8fb1bc340000c2fafed0a6d2862b9ad033d668e89691bfdeb3bf6dc8215d3`.
- `openspec/specs/migrations/spec.md` : `9b3ced385afbeaa7414a1d58752078482e57efa242064e21e7fb4b6fde451efe`.
- `openspec/specs/modules/spec.md` : `7ea4899dff68afd31f22a501e587da4dcad9c911d1689583672678cf108ff37b`.
- `openspec/specs/providers/spec.md` : `5aceaa82194cfc9802dcf6ef1bd9e4fc35b18b5156d1b29685e41d23689a7fd7`.
- `openspec/specs/reference-composition/spec.md` : `7c4d7b603f35f02f6d2ba0eb10dd202793ec288fee0c65a5ff15d244446233ff`.
- `openspec/specs/reference-runtime/spec.md` : `4bbbc0451013b7139f3898b4a5aebd592ab1c50b6aa6cce4e1246957e4052351`.
- `openspec/specs/runtime/spec.md` : `0eb07f4494b590fdd845cfe90143a34dc331717b5b38b293dee4b45c100cee11`.
- `openspec/specs/services/spec.md` : `e754ac950e612d335017122e23e55d75d3fb214f927fabcb2d48da8722013c37`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
