# Tasks

## 1. Préparation

- [x] 1.1 Confirmer l’absence de change actif, les 27 baselines, les 136 tests et les normes R2/R4 ; publier les cinq artefacts dont le delta reproduit R2/R4 mot pour mot, puis réussir les stricts du change et canonique avant tout code.

## 2. Codec

- [x] 2.1 Ajouter l’exception à message fixe et `encode_feature_flag_source_snapshot` : type exact, validation réelle intégrale du lot avant extraction, copies récursives neuves, pas d’asdict, pas de copie générique, pas d’écho d’erreur.
- [x] 2.2 Ajouter `decode_feature_flag_source_snapshot` : clés et types exacts avant hachage ou hook, reconstruction des dataclasses canoniques, appel réel du validateur de lot complet, aucune normalisation ni alias.

## 3. Tests

- [x] 3.1 Créer la suite unitaire causale : aller-retours, scalaires opaques, `False`, Unicode, conteneurs frais, hostiles sans hook, clés et formes invalides, liaisons invalides, absence d’écho et conservation de la valeur structurellement valide mais évaluée `INVALID`.
- [x] 3.2 Créer la suite d’intégration en processus frais avec gardes éprouvées : composition réelle, validateurs réellement appelés et comptes nuls pour filesystem, réseau, sous-processus, horloge, PostgreSQL et secrets.

## 4. Preuves

- [x] 4.1 Réussir les trois compilations, la nouvelle suite unitaire, la nouvelle intégration et les 136 régressions dans l’environnement Python explicite.
- [x] 4.2 Vérifier les 27 baselines inchangées, les anciens modules et tests non modifiés, UTF-8/LF, limites sans persistance, PostgreSQL, audit, cache, dépendance, export ou README, puis le delta canonique exact.
- [x] 4.3 Réussir les stricts après preuves et faire contrôler les critères, les résultats et la cohérence du change par CGPT avant son autorisation distincte d’archivage.

Après cochage sous mandat distinct et strict réussi, l’archivage exige sa propre autorisation CGPT et son mandat CAB. Le rapport STATISTIQUES.md est produit après archivage sous un mandat séparé ; sa preuve reste obligatoire avant de déclarer le sous-job terminé.
