# Conception — N03 : Confiance des artefacts avant installation

Préparation dédiée validée explicitement par le développeur le 17 octobre 2026. Réalisation non autorisée.

## Écart démontré

`artifact-publication` exige identité, signature, provenance, inventaire et révocation vérifiables avant installation/démarrage/mise à niveau (exigences 3–5). C18 transmet le paquet à C17 ; C17 l’installe pour sa recette ; C19, qui dépend de C17/C18, porte actuellement la réalisation de ces contrôles. Un ordre global acyclique de dossiers ne suffit donc pas : la recette peut précéder la disponibilité de son mécanisme de confiance.

Références : [canon](../../../openspec/specs/artifact-publication/spec.md), [C17 tâches](../../../openspec/changes/qualify-first-pbo-composition/tasks.md), [C18 tâches](../../../openspec/changes/build-first-pbo-pfo-debian-package/tasks.md), [C19 tâches](../../../openspec/changes/publish-first-qualified-pbo-release/tasks.md).

## Préparation recommandée

Créer `add-p0-artifact-trust-and-preinstallation-verification` : contrats des matériaux publics de confiance, vérificateur avant installation, politique de canal/versions/empreintes, provenance/inventaire et révocation localement vérifiable si publication indisponible. Formaliser les contrôles de sécurité de build et leur preuve sans installer d’outil ni choisir d’autorité ou d’algorithme nouveau.

C19 conserve identité finale de release, support, corrélation de recette, décision et action de publication. Les primitives/gates précoces ne doivent pas attendre sa clôture. Le traitement des dérogations de vulnérabilité doit suivre le canon ; les différences de formulation avec BUILD doivent être résolues explicitement avant application de cette politique.

## Dépendances et livraison

N03 dépend de C00 pour les décisions du profil. C18/C17 requièrent ses contrats/vérificateurs. Le générateur consomme l’artefact une fois construit ; la dépendance de conception n’exige pas de signer un fichier avant qu’il existe. C19 consomme les preuves finales et ne réécrit pas l’artefact déjà qualifié ; toute modification d’identité ou d’octets exige la revalidation applicable.

## Critères futurs

Canal non autorisé, empreinte discordante, signature absente/expirée/révoquée, provenance/inventaire non vérifiables : refus avant opération. Révocation vérifiable publication indisponible ; rotation et chevauchement testés ; correction avec nouvelle identité immuable ; aucun secret dans artefact/log/fixture. Matériaux de confiance de test synthétiques, aucune clé réelle manipulée pendant cette préparation.

## Portée de préparation et retour

Aucun code produit, secret, compte, service, dépendance, migration, données réelles, signature ou publication n’est manipulé par cette préparation. Les tâches restent futures et non cochées. Une évolution persistante ultérieure exige schéma/version, contrat de compatibilité et reprise/compensation revue ; aucun downgrade automatique ni purge implicite.

## Dépendances après audit transversal P0

[C00](../define-first-installable-pbo-profile/proposal.md).

Les conditions d’activation et la construction des résultats sont séparées de cet ordre de préparation ; aucun cycle inverse vers la recette finale.
