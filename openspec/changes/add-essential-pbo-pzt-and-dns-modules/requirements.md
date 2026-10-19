# Exigences de réalisation — C14

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 adopté le 18 octobre 2026 et intégré au canon apporte les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
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
| reference-runtime / 177 | [Module PZT essentiel dans PBO](../../specs/reference-runtime/spec.md#L177) | ND | Module PZT essentiel dans PBO |
| pzt / 21 | [Module essentiel PBO et binaire PZT dédié](../../specs/pzt/spec.md#L21) | ND | Module essentiel PBO et binaire PZT dédié |
| pzt / 84 | [DNS essentiel partagé administré par PBO](../../specs/pzt/spec.md#L84) | ND | DNS essentiel partagé administré par PBO |
| pzt / 147 | [Audit applicable et faits réellement établis](../../specs/pzt/spec.md#L147) | ND | Audit applicable et faits réellement établis |
| pzt / 156 | [Portée des contrats techniques et valeurs ouvertes](../../specs/pzt/spec.md#L156) | ND | Portée des contrats techniques et valeurs ouvertes |
| pzt / 165 | [Qualification et état de spécification distincts](../../specs/pzt/spec.md#L165) | ND | Qualification et état de spécification distincts |
| pzt / 174 | [Lecture normative des contrats de décision intégrés](../../specs/pzt/spec.md#L174) | ND | Paramètre ancien précisé par une décision ultérieure |
| pzt / 310 | [Contrat A06c — DNS Pixs géré par un module essentiel PBO, option B validée](../../specs/pzt/spec.md#L310) | ND | Conformité du traitement A06c |

## Empreintes SHA-256 du canon

- `openspec/specs/pzt/spec.md` : `81d2b355b118a6e4007f065a6fad91ada3915261fbbd51b0a5fc28e2a230290f`.
- `openspec/specs/reference-runtime/spec.md` : `4bbbc0451013b7139f3898b4a5aebd592ab1c50b6aa6cce4e1246957e4052351`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
