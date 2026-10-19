# Exigences de réalisation — C11

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 adopté le 18 octobre 2026 et intégré au canon apporte les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| accessibility / 8 | [Niveau cible WCAG 2.2 AA](../../specs/accessibility/spec.md#L8) | P | Contribution non conforme |
| accessibility / 17 | [Fonctionnement clavier et technologies d'assistance](../../specs/accessibility/spec.md#L17) | P | Parcours clavier complet |
| accessibility / 26 | [Sémantique native préservée](../../specs/accessibility/spec.md#L26) | P | Rôle ARIA redondant |
| accessibility / 35 | [Validation outillée et manuelle combinées](../../specs/accessibility/spec.md#L35) | P | Défaut non détectable automatiquement |
| api / 8 | [Application de l'exception Super Admin](../../specs/api/spec.md#L8) | P | API tenant-scoped du Super Admin |
| api / 18 | [Contrats OpenAPI versionnés par majeure](../../specs/api/spec.md#L18) | P | Rupture sans nouvelle majeure bloquée |
| api / 27 | [Enveloppes stables et erreurs typées](../../specs/api/spec.md#L27) | P | Rejou identique restitué |
| api / 38 | [Périmètre canonique et autorisation à la frontière](../../specs/api/spec.md#L38) | P | Tenant d'en-tête non canonique rejeté |
| design-system / 8 | [Tokens sémantiques d'intention](../../specs/design-system/spec.md#L8) | P | Valeur brute refusée |
| design-system / 17 | [Primitives à API stable](../../specs/design-system/spec.md#L17) | P | Variante non déclarée |
| design-system / 26 | [Cohérence Light et Dark par les tokens](../../specs/design-system/spec.md#L26) | P | Primitive inspectée dans les deux modes |
| design-system / 35 | [Adapter de rendu sans contournement](../../specs/design-system/spec.md#L35) | P | Accès direct au moteur refusé |
| extension-contracts / 8 | [Points d'extension publics versionnés](../../specs/extension-contracts/spec.md#L8) | P | Contribution sans point déclaré rejetée |
| extension-contracts / 17 | [Contributions déclarées et isolées](../../specs/extension-contracts/spec.md#L17) | P | Accès privé bloqué |
| extension-contracts / 26 | [Niveau de confiance des extensions](../../specs/extension-contracts/spec.md#L26) | P | Extension de développement en production |
| extension-contracts / 38 | [Collisions et composition déterministe](../../specs/extension-contracts/spec.md#L38) | P | Deux routes en collision |
| extension-contracts / 47 | [Composition interface au build](../../specs/extension-contracts/spec.md#L47) | P | Code distant implicite refusé |
| extension-contracts / 56 | [Frontières publiques des composants frontend imbriqués](../../specs/extension-contracts/spec.md#L56) | P | Slot enfant non déclaré |
| frontend / 8 | [Contributions déclarées et routage sans collision](../../specs/frontend/spec.md#L8) | P | Route ambiguë bloquée |
| frontend / 17 | [Session fournie par le shell et autorisation applicative](../../specs/frontend/spec.md#L17) | P | Garde frontale non substitutive |
| frontend / 26 | [Mutations provisoires et invalidation tenant-aware](../../specs/frontend/spec.md#L26) | P | Invalidation après commande |
| frontend / 37 | [Sous-modularité frontend par le modèle de composants commun](../../specs/frontend/spec.md#L37) | P | Sous-module optionnel isolé |
| internationalization / 8 | [Catalogues par composant et langue canonique](../../specs/internationalization/spec.md#L8) | P | Clé manquante bloquée |
| internationalization / 17 | [Résolution déterministe et formats localisés](../../specs/internationalization/spec.md#L17) | P | Valeur métier préservée ; Préférence navigateur avant défaut d'installation |
| lifecycle / 8 | [États de cycle de vie distincts](../../specs/lifecycle/spec.md#L8) | P | États non confondus |
| lifecycle / 17 | [Transitions autorisées et refusées](../../specs/lifecycle/spec.md#L17) | P | Désactivation sans perte et purge explicite |
| lifecycle / 26 | [Ordre déterministe des hooks](../../specs/lifecycle/spec.md#L26) | P | Double résolution identique |
| lifecycle / 35 | [Idempotence des opérations](../../specs/lifecycle/spec.md#L35) | P | Rejeu sans double effet |
| lifecycle / 44 | [Diagnostic des échecs](../../specs/lifecycle/spec.md#L44) | P | Activation invalide bloquée |
| modules / 8 | [Manifest lisible obligatoire](../../specs/modules/spec.md#L8) | P | Manifest incomplet |
| modules / 17 | [Frontière API publique et privée](../../specs/modules/spec.md#L17) | P | Accès à une API non déclarée |
| modules / 26 | [Propriété des données et migrations associées](../../specs/modules/spec.md#L26) | P | Changement de schéma non migré |
| modules / 35 | [Chargement contrôlé déterministe](../../specs/modules/spec.md#L35) | P | Cycle de dépendances |
| modules / 44 | [Propriété des contributions frontend modulaires](../../specs/modules/spec.md#L44) | P | Sous-module autonome intégré |
| providers / 8 | [Déclaration lisible des fournisseurs](../../specs/providers/spec.md#L8) | P | Implémentation non déclarée |
| providers / 17 | [Sélection explicite sans choix implicite](../../specs/providers/spec.md#L17) | P | Deux candidats sans configuration |
| providers / 26 | [Conformité contractuelle vérifiable](../../specs/providers/spec.md#L26) | P | Fournisseur non conforme activé |
| providers / 35 | [Dégradation contrôlée et diagnostic](../../specs/providers/spec.md#L35) | P | Indisponibilité d'un fournisseur |
| services / 8 | [Enregistrement contractuel des services](../../specs/services/spec.md#L8) | P | Service privé non exposé |
| services / 17 | [Résolution déterministe du fournisseur](../../specs/services/spec.md#L17) | P | Ambiguïté refusée |
| services / 28 | [Traçabilité et sécurité des appels](../../specs/services/spec.md#L28) | P | Contexte non vérifiable |
| themes / 8 | [Modes clair et sombre obligatoires](../../specs/themes/spec.md#L8) | P | Bascule sans rechargement |
| themes / 17 | [Tokens sémantiques sans valeurs codées](../../specs/themes/spec.md#L17) | P | Valeur codée rejetée |

## Empreintes SHA-256 du canon

- `openspec/specs/accessibility/spec.md` : `a3f9275d101b121d225c2975931a567b5ffed9d512ea22185bb28094e5821baf`.
- `openspec/specs/api/spec.md` : `58abd35620d8a6e9c65b0f525e8afda12a2291b9a531bba9248643be3afd3152`.
- `openspec/specs/design-system/spec.md` : `c5ff33414eda8c66695366e189038db1f311f428e2e5e19b774907421131778e`.
- `openspec/specs/extension-contracts/spec.md` : `f7d5d14c29aeb97aad6780413d5560686264a3cc3f97b29eca907182166f90eb`.
- `openspec/specs/frontend/spec.md` : `e646e3faf793db109a93f803423cfa4606deeb67b91d4b3301fa219e82cf9414`.
- `openspec/specs/internationalization/spec.md` : `72a1a1756ae168e16d51055edeaa44786894caf20cc420c96ce9bb3da8907232`.
- `openspec/specs/lifecycle/spec.md` : `e4f8fb1bc340000c2fafed0a6d2862b9ad033d668e89691bfdeb3bf6dc8215d3`.
- `openspec/specs/modules/spec.md` : `7ea4899dff68afd31f22a501e587da4dcad9c911d1689583672678cf108ff37b`.
- `openspec/specs/providers/spec.md` : `5aceaa82194cfc9802dcf6ef1bd9e4fc35b18b5156d1b29685e41d23689a7fd7`.
- `openspec/specs/services/spec.md` : `e754ac950e612d335017122e23e55d75d3fb214f927fabcb2d48da8722013c37`.
- `openspec/specs/themes/spec.md` : `bd2008d3546647c84d913397230724ca1c48d3aac6ad3b4c509550ddbca6fb64`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
