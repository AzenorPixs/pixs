# Exigences de réalisation — C12

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 proposé ajoute les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| accessibility / 8 | [Niveau cible WCAG 2.2 AA](../../specs/accessibility/spec.md#L8) | P | Contribution non conforme |
| accessibility / 17 | [Fonctionnement clavier et technologies d'assistance](../../specs/accessibility/spec.md#L17) | P | Parcours clavier complet |
| accessibility / 26 | [Sémantique native préservée](../../specs/accessibility/spec.md#L26) | P | Rôle ARIA redondant |
| accessibility / 35 | [Validation outillée et manuelle combinées](../../specs/accessibility/spec.md#L35) | P | Défaut non détectable automatiquement |
| design-system / 8 | [Tokens sémantiques d'intention](../../specs/design-system/spec.md#L8) | P | Valeur brute refusée |
| design-system / 17 | [Primitives à API stable](../../specs/design-system/spec.md#L17) | P | Variante non déclarée |
| design-system / 26 | [Cohérence Light et Dark par les tokens](../../specs/design-system/spec.md#L26) | P | Primitive inspectée dans les deux modes |
| design-system / 35 | [Adapter de rendu sans contournement](../../specs/design-system/spec.md#L35) | P | Accès direct au moteur refusé |
| developer-experience / 10 | [Parcours local reproductible](../../specs/developer-experience/spec.md#L10) | P | Premier composant local |
| developer-experience / 21 | [Génération sans activation implicite](../../specs/developer-experience/spec.md#L21) | P | Scaffolding d'un provider |
| developer-experience / 32 | [Diagnostics sans fuite](../../specs/developer-experience/spec.md#L32) | P | Manifest incomplet |
| frontend / 8 | [Contributions déclarées et routage sans collision](../../specs/frontend/spec.md#L8) | P | Route ambiguë bloquée |
| frontend / 17 | [Session fournie par le shell et autorisation applicative](../../specs/frontend/spec.md#L17) | P | Garde frontale non substitutive |
| frontend / 26 | [Mutations provisoires et invalidation tenant-aware](../../specs/frontend/spec.md#L26) | P | Invalidation après commande |
| frontend / 37 | [Sous-modularité frontend par le modèle de composants commun](../../specs/frontend/spec.md#L37) | P | Sous-module optionnel isolé |
| internationalization / 8 | [Catalogues par composant et langue canonique](../../specs/internationalization/spec.md#L8) | P | Clé manquante bloquée |
| internationalization / 17 | [Résolution déterministe et formats localisés](../../specs/internationalization/spec.md#L17) | P | Valeur métier préservée ; Préférence navigateur avant défaut d'installation |
| testing / 8 | [Trois niveaux de vérification distincts](../../specs/testing/spec.md#L8) | P | Unitaires verts, intégration rouge |
| testing / 17 | [Kit de conformité et composant d'exemple](../../specs/testing/spec.md#L17) | P | Exemple P0 validé |
| testing / 30 | [Suites de conformité versionnées par contrat](../../specs/testing/spec.md#L30) | P | Certification expirée |
| testing / 39 | [Garanties obligatoires séparées des capacités optionnelles](../../specs/testing/spec.md#L39) | P | Isolement acceptable |
| testing / 48 | [Reproductibilité sur la topologie de référence](../../specs/testing/spec.md#L48) | P | Divergence de topologie |
| testing / 57 | [Preuves sans secret ni donnée de production](../../specs/testing/spec.md#L57) | P | Secret détecté dans un rapport |
| testing / 66 | [Conformité de la composition frontend récursive](../../specs/testing/spec.md#L66) | P | Composition reproductible avec sous-module |
| testing / 75 | [Conformité des projections d'annuaire optionnelles](../../specs/testing/spec.md#L75) | P | Repli conforme sans élargissement de droits |
| testing / 89 | [Exécution navigateur headless des unités frontend web](../../specs/testing/spec.md#L89) | P | Les deux moteurs déclarent les cas ; Moteur manquant ou cas non exécuté |
| themes / 8 | [Modes clair et sombre obligatoires](../../specs/themes/spec.md#L8) | P | Bascule sans rechargement |
| themes / 17 | [Tokens sémantiques sans valeurs codées](../../specs/themes/spec.md#L17) | P | Valeur codée rejetée |

## Empreintes SHA-256 du canon

- `openspec/specs/accessibility/spec.md` : `a3f9275d101b121d225c2975931a567b5ffed9d512ea22185bb28094e5821baf`.
- `openspec/specs/design-system/spec.md` : `c5ff33414eda8c66695366e189038db1f311f428e2e5e19b774907421131778e`.
- `openspec/specs/developer-experience/spec.md` : `9008a4c9affc2e6dc13c7247fd375c349a8d85fa2733878756dd27373ad8e4b1`.
- `openspec/specs/frontend/spec.md` : `e646e3faf793db109a93f803423cfa4606deeb67b91d4b3301fa219e82cf9414`.
- `openspec/specs/internationalization/spec.md` : `72a1a1756ae168e16d51055edeaa44786894caf20cc420c96ce9bb3da8907232`.
- `openspec/specs/testing/spec.md` : `5e0c976821f8623c976d43125c7d5738fbf100b9fae1a112d45894e9fdc7a148`.
- `openspec/specs/themes/spec.md` : `bd2008d3546647c84d913397230724ca1c48d3aac6ad3b4c509550ddbca6fb64`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
