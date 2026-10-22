# Validation N03 — confiance des artefacts avant installation

RUN : `cismp2-pixs-ac0840c5f4524da9` ; parent historique : `cismp2-pixs-4f3dfe97e25742ef`. Session native : `ses_ea7d229efffe8mhOwKaAxc0akA`.

## Autorisation et périmètre

L’invocation `1CISMP2` couvre un seul change, sa réalisation dans le canon existant, son archivage, ses statistiques et son arrêt ciblé. Les deux phrases RSMP de BUILD.md et TECHNICAL.md et l’identité CAB de remplacement ont reçu leurs validations distinctes. Aucun Git, déploiement ou publication externe n’est engagé.

Trois modules backend et trois fichiers de tests sont livrés. Les dix tâches N03 sont prouvées dans leur rôle de producteur de contrats et vérificateurs précoces ; la qualification des consommateurs C17/C18/C19 reste séparée.

## Vérifications réellement exécutées

| Vérification | Résultat observé |
| --- | --- |
| Compilation Python des six fichiers | Exit 0 ; bytecode éphémère sous racine, supprimé |
| Compilation du module corrigé | Exit 0 |
| Première suite réelle | 35 tests, un échec de classification diagnostique du bundle absent |
| Correction minimale | Refus désormais BUNDLE_MALFORMED ; aucune autre garantie changée |
| Suite complète finale | 35 tests réussis, zéro échec, zéro erreur, zéro skip ; 4,060 s |
| OpenSpec strict avant archive | Totals: 193 passed, 0 failed (193 items) ; exit 0 |
| Archivage N03 | Une seule exécution réussie, avec --yes --skip-specs ; exit 0 |
| OpenSpec strict après archive | Totals: 192 passed, 0 failed (192 items) ; exit 0 |
| Canon après archive | 78 fichiers inchangés par comparaison SHA-256 |
| Encodage | UTF-8/LF vérifié sur les fichiers livrés |
| Clés de tests | Générées uniquement dans le processus test, sous racine ; nettoyées ; aucune clé privée statique |
| PostgreSQL, navigateur, installation système | Non applicables à ce lot de vérification d’artefacts ; non exécutés |
| Git | Non inspecté et non modifié |

L’archivage a produit un avertissement non bloquant : l’heuristique de proposition attend des titres anglais `Why/What Changes`, alors que ce dossier conserve ses titres français. Le code retour d’archive et les validations strictes sont distingués de cet avertissement.

## Matrice de traçabilité

| Exigence canonique | Preuve de la contribution N03 |
| --- | --- |
| artifact-publication 1 — canal | Canaux connus et diagnostics sûrs constaté/attendu ; signatures liées au canal |
| artifact-publication 2 — immuabilité | Protection des trois empreintes, identité canonique sans collision, nouvelle version corrélée |
| artifact-publication 3 — identité | Attentes explicites de version/source/composition ; altérations de l’artefact et des deux pièces refusées |
| artifact-publication 4 — signature | Signatures Ed25519 OpenSSL réelles ; tampering malgré empreinte recalculée, expiration et révocation refusés |
| artifact-publication 5 — autorités et rotation | Clés expérimentales distinctes, chevauchement de deux signataires, révocation sous alias/PEM reformaté, bundle local authentifié |
| security 2 — vulnérabilité critique | Dérogation limitée et reçue indépendamment ; absence de dérogation/reçu, mauvaises empreintes et échéances refusées |
| security 3 — échec fermé | Données absentes ou ambiguës, signature invérifiable et OpenSSL indisponible/timeout refusés |
| security 4 — diagnostic | Codes différenciés, erreur fournisseur assainie, absence de clé privée dans les sorties contrôlées |
| deb-package 1 — corrélation | Identité attendue et trois empreintes liées aux mêmes octets ; aucune identité de release réelle inventée |
| deb-package 4 — upgrade | Gate avec reçu de compatibilité indépendant avant consommation ; aucune recette de migration/rollback système prétendue |
| deb-package 5 — absence de code distant | Vérification locale sans téléchargement implicite ; test avec réseau Python interdit |

Les tests d’intégration construisent une archive de fixture réelle et consomment seulement les octets renvoyés dans `VerifiedArtifact`. Les empreintes du fichier de fixture écrit sont contrôlées. La mutation des objets de confiance par le fournisseur n’altère pas les snapshots déjà vérifiés.

## Fichiers et cohérence documentaire

- `src/pixs/backend/artifact_trust_materials.py` : matériaux publics et validation pure.
- `src/pixs/backend/artifact_trust_proof.py` : preuve signée et adaptateur OpenSSL de vérification.
- `src/pixs/backend/artifact_trust_gate.py` : contrôles précoces, octets immuables et historique fourni par propriétaire fiable.
- `tests/unit/test_artifact_trust_materials.py`, `tests/unit/test_artifact_trust_proof.py`, `tests/integration/test_artifact_trust_gate_integration.py` : suites exécutées.

Les références N03 des propositions/conceptions C17/C18/C19 sont seules déplacées vers cette archive ; aucune réalisation de ces autres changes n’est engagée. PROJECT.md, README.md et DEVOPS.md restent cohérents avec les limites du lot. Les changements BUILD/TECHNICAL restent limités aux phrases RSMP approuvées ; l’édition C02 indépendante de TECHNICAL a été réconciliée et préservée. Aucun fichier canonique n’est écrit.

## Limites de preuve

L’appelant local fiable fournit les matériaux, le temps UTC, le plancher monotone de révocation, l’historique et les reçus authentifiés d’audit/compatibilité. N03 n’implémente ni leur persistance ni l’autorité métier qui les produit. Un simple booléen d’auteur ne les remplace pas.

Aucun paquet Debian final, système installé, migration, restauration, racine de signature réelle ou publication externe n’a été qualifié. Le succès de fixture ne vaut ni audit durable C05 ni P0 complet. Le cycle global reste incomplet.

## Références natives

- Tests finaux : native:ses_ea7d229efffe8mhOwKaAxc0akA:msg_15860275a001ybGGN5h6eqjYEu:prt_15860305e001mEP2r5k666y1b6:bash:completed.
- Archive unique : native:ses_ea7d229efffe8mhOwKaAxc0akA:msg_1586f8590001Ee1E4sJTyp44EH:prt_1586f9001001T3KsgF4l41E8r3:bash:completed.
- Strict postarchive : native:ses_ea7d229efffe8mhOwKaAxc0akA:msg_15871178a001fFHfAnovSO3AZr:prt_158712047001MtvyErPZqgBfPp:bash:completed.
- Checkpoint non versionné : `output/cismp/cismp2-pixs-ac0840c5f4524da9/state.json`.
- Le rapport postarchive `STATISTIQUES.md` et la publication CAB restent obligatoires avant le gate terminal.
