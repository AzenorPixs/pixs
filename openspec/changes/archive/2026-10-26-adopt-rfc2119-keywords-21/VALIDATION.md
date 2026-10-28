# Validation observée — lot 21

Ce lot documentaire contient 2 fichiers normatifs intacts, 10 exigences et 10 scénarios. Le contenu normatif n'est pas corrigé, réécrit ou resynchronisé.

## Validations strictes de revalidation historique

| Étape | Proposition stricte | Deltas stricts | Exigences / scénarios |
|---|---|---|---|
| prepared | valide, 0 diagnostic | valides, 0 diagnostic | 10 / 10 |
| archived-stage | valide, 0 diagnostic | valides, 0 diagnostic | 10 / 10 |
| published | valide, 0 diagnostic | valides, 0 diagnostic | 10 / 10 |

La série [CLI historique stricte](../../../../output/rfc2119-split/20261026T200749Z/prepared-historical-strict-cli.json) valide 21 lots sur 21. Les contrôles API sans droit fs.write sont conservés [avant archivage](../../../../output/rfc2119-split/20261026T200749Z/prepared-strict-api.json), [après archivage isolé](../../../../output/rfc2119-split/20261026T200749Z/archived-stage-strict-api.json) et [après publication réelle](../../../../output/rfc2119-split/20261026T200749Z/published-strict-api.json). La dernière série est datée 2026-10-26T20:19:22.208Z.

## Archivage natif

Commande : /home/devops/node/current/bin/node /home/devops/.local/npm/bin/openspec archive adopt-rfc2119-keywords-21 --yes --skip-specs --json

Le [reçu natif](../../../../output/rfc2119-split/20261026T200749Z/archive-21-native.json) retourne exit 0 et specsUpdated=false. L'archivage a eu lieu dans la préparation isolée, puis les artefacts ont été publiés dans 2026-10-26-adopt-rfc2119-keywords-21. Nom renvoyé par l'archiveur : 2026-10-26-adopt-rfc2119-keywords-21. Le lot 01 conserve le chemin historique validé ; les vingt autres utilisent la date d'application.

## Limite de resynchronisation

La [validation comparée au canon actuel](../../../../output/rfc2119-split/20261026T200749Z/prepared-strict-cli.json) retourne pour ce lot valid=true, avec 0 diagnostic(s). Au total, ce profil a 13 lots valides et 8 lots refusés pour des scénarios ajoutés ou changés depuis septembre. Les échecs sont conservés et aucune resynchronisation de ces deltas historiques au canon n'est autorisée par ce découpage.

## Intégrité et portée

Le [manifest](../../../../output/rfc2119-split/20261026T200749Z/manifest.json) affecte exactement une fois les 56 fichiers, 205 exigences et 206 scénarios à la collection des 21 lots. Les 78 fichiers du canon réel conservent leurs empreintes et passent le strict séparément.

3.1 est qualifiée pour le découpage structurel historique en 21 lots et l'archivage --skip-specs ; cela ne qualifie pas une réapplication au canon actuel. 2.1 reste NON VÉRIFIABLE : aucune préimage immédiate complète des 205 exigences avant migration n'est reconstituée.
