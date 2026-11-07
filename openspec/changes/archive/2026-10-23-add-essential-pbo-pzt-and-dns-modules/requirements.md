# Exigences de réalisation — C14

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 adopté le 18 octobre 2026 et intégré au canon apporte les précisions de première livraison ; il ne supprime aucun MUST existant.

Références réconciliées le 22 octobre 2026 avec le canon courant par titre, scénarios, ligne et empreinte. Les liens de ligne et empreintes désignent ce relevé ; une dérive impose une nouvelle lecture avant réalisation. La matrice C00 archivée conserve ses références historiques et n’est pas modifiée. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
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
| reference-runtime / 234 | [Modules de gestion pixs.agent et pixs.pzt dans PBO](../../../specs/reference-runtime/spec.md#L234) | ND | Composition des deux modules de gestion ; Réseau désactivé |
| pzt / 77 | [Module essentiel pixs.pzt et exécutable PZT indépendant](../../../specs/pzt/spec.md#L77) | ND | Réseau désactivé et gestion conservée |
| pzt / 149 | [DNS essentiel partagé administré par PBO](../../../specs/pzt/spec.md#L149) | ND | DNS essentiel partagé administré par PBO |
| pzt / 212 | [Audit applicable et faits réellement établis](../../../specs/pzt/spec.md#L212) | ND | Audit applicable et faits réellement établis |
| pzt / 221 | [Portée des contrats techniques et valeurs ouvertes](../../../specs/pzt/spec.md#L221) | ND | Portée des contrats techniques et valeurs ouvertes |
| pzt / 230 | [Qualification et état de spécification distincts](../../../specs/pzt/spec.md#L230) | ND | Qualification et état de spécification distincts |
| pzt / 296 | [Lecture normative des contrats de décision intégrés](../../../specs/pzt/spec.md#L296) | ND | Paramètre ancien précisé par une décision ultérieure |
| pzt / 432 | [Contrat A06c — DNS Pixs géré par un module essentiel PBO, option B validée](../../../specs/pzt/spec.md#L432) | ND | Conformité du traitement A06c |

## Empreintes SHA-256 du canon

- `openspec/specs/pzt/spec.md` : `21daa3cc9299b13d29a7f85e7a23e5c5726a06c16f73df7a35c0197c6ff1fec3`.
- `openspec/specs/reference-runtime/spec.md` : `6bbb170eb652b0b07a7b7dd61775b1cd52284fa7b53b05374c8f3267b089fed7`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.


## Recoupement du canon courant le 23 octobre 2026

Les 21 titres, lignes et ensembles de scénarios du relevé C00 restent
résolus. L'empreinte PZT est actualisée après lecture des clauses applicables
et de la clause d'amorçage PKI/PZT autonome de première installation ajoutée
au canon. Cette exception relève de Z12 et du parcours C08 ; elle ne rend
pas disponibles des ports, une autorité technique ou un transport initial.

Les surfaces C14 livrent la gestion ordinaire sous PostgreSQL et C03/C04/C05.
Elles n'émettent aucune confiance initiale, ne transportent pas de clé privée
ou de credential PostgreSQL et n'ouvrent aucun canal d'amorçage. L'adoption
PostgreSQL, le retrait irréversible de l'autorité initiale et l'admission
ordinaire demeurent des étapes propriétaires distinctes à prouver dans leur
parcours ; aucune qualification de ces étapes n'est déduite de C14.

## Recoupement complémentaire avant clôture — 23 octobre 2026

Le canon PZT a reçu deux exigences Z12 : profil X.509 des terminaux de
première installation et résolution locale du matériel TLS par le propriétaire
courant. Le préfixe antérieur est reconstitué octet pour octet et retrouve
l'empreinte 652aeb4b9ab911bbafb7b3f9f3c7ad582b5bed8af5a806ce9925579caaf7aba5 ;
les 21 titres, lignes et ensembles de scénarios ci-dessus sont inchangés.
Leurs règles de séparation de confiance, de refus fermé et d'absence de clé
privée ou d'autorité déduite d'une référence sont conservées. C14 n'émet ni
ne résout de matériel TLS et ne qualifie pas ces deux parcours Z12. Aucun
port d'amorçage ou transport de substitution n'est ajouté. Seule l'empreinte
courante et ce recoupement documentaire sont actualisés ; aucun canon,
code, cadrage ou choix d'activation n'est modifié.
