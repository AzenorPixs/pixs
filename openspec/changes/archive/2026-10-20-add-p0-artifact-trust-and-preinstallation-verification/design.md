# Conception — N03 : Confiance des artefacts avant installation

Préparation dédiée validée explicitement le 17 octobre 2026 ; les sections de préparation ci-dessous sont historiques. La réalisation autorisée ensuite par 1CISMP2 et ses preuves sont décrites en fin de document.

## Écart démontré

`artifact-publication` exige identité, signature, provenance, inventaire et révocation vérifiables avant installation/démarrage/mise à niveau (exigences 3–5). C18 transmet le paquet à C17 ; C17 l’installe pour sa recette ; C19, qui dépend de C17/C18, porte actuellement la réalisation de ces contrôles. Un ordre global acyclique de dossiers ne suffit donc pas : la recette peut précéder la disponibilité de son mécanisme de confiance.

Références : [canon](../../../../openspec/specs/artifact-publication/spec.md), [C17 tâches](../../../../openspec/changes/qualify-first-pbo-composition/tasks.md), [C18 tâches](../../../../openspec/changes/build-first-pbo-pfo-debian-package/tasks.md), [C19 tâches](../../../../openspec/changes/publish-first-qualified-pbo-release/tasks.md).

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

[C00](../archive/2026-10-18-define-first-installable-pbo-profile/proposal.md).

Les conditions d’activation et la construction des résultats sont séparées de cet ordre de préparation ; aucun cycle inverse vers la recette finale.


## Réalisation N03 du 20 octobre 2026

L’invocation `1CISMP2` autorise la réalisation de ce seul change dans le canon validé. La préparation du 17 octobre et son `preparation.json` restent des faits historiques ; leurs indicateurs ne constituent pas le statut courant. Le RUN de remplacement CAB est explicitement autorisé et conserve le lien avec son parent dans le checkpoint.

Les deux phrases de BUILD et TECHNICAL relatives aux vulnérabilités critiques ont été alignées sur `security` après validation RSMP distincte. Aucun canon n’a été modifié. Aucun composant, service ou fournisseur n’est activé automatiquement.

### Implémentation et dépendances

Trois modules sous `src/pixs/backend/` fournissent les matériaux publics, l’assemblage/vérification de preuves et les contrôles précoces : `artifact_trust_materials.py`, `artifact_trust_proof.py`, `artifact_trust_gate.py`. Trois modules de tests exercent les cas réels. Python reste compatible avec le minimum 3.12 du projet ; aucune dépendance n’est ajoutée. L’adaptateur utilise uniquement `/usr/bin/openssl`, sans shell, avec un délai de 10 secondes et des fichiers temporaires de données publiques dans le parent explicitement fourni.

Ed25519, SHA-256 et JSON déterministe constituent le profil local v1 de ce lot, pas une nouvelle exigence générale. Les clés publiques SPKI Ed25519 sont décodées strictement selon [RFC 8410](https://www.rfc-editor.org/rfc/rfc8410.html). La commande de vérification emploie `pkeyutl -verify -pubin -rawin` sur un fichier de taille connue : [documentation OpenSSL](https://docs.openssl.org/3.5/man1/openssl-pkeyutl/).

### Contrats v1

La preuve signée lie `proof_version=1`, le canal, la version, la source, la composition, les trois empreintes SHA-256 de l’artefact/provenance/inventaire, le signataire, la version précédente, les opérations admises, les constats critiques, les dérogations et l’empreinte de preuve de compatibilité. `signature_hex` et `proof_sha256` forment l’enveloppe ; les champs signés excluent ces deux valeurs. L’empreinte de l’enveloppe lie les octets canoniques à la signature.

Le bundle local signé comprend `bundle_version=1`, son identifiant, l’émetteur rattaché à l’ancre, les bornes temporelles, la séquence, les identifiants et empreintes de clés révoquées et la signature. L’empreinte d’une clé est SHA-256 de ses 32 octets publics : renommage et reformatage PEM ne permettent pas de contourner une révocation. Une séquence inférieure au plancher local est refusée ; conserver ce plancher incombe au propriétaire fiable, sans persistance inventée par N03.

Les autorités déclarent leur clé publique, leurs canaux et leur fenêtre. Stable et security peuvent partager une autorité ; toute clé expérimentale reste distincte du groupe stable/security, y compris sous alias. Plusieurs clés du même canal peuvent coexister dans un chevauchement valide. Les fenêtres de l’ancre, du signataire et du bundle utilisent `début <= now < fin`, avec un temps UTC fourni par le contexte de confiance.

Le JSON refuse les clés dupliquées, les nombres non finis, les types ambigus, les versions et empreintes malformées et les structures excessives. Les plafonds du profil sont : clé publique PEM 4 Kio, JSON d’entrée 64 Kio, corps canonique signé 16 Kio, artefact 64 Mio, provenance/inventaire 1 Mio chacun, 32 autorités, 256 révocations de chaque catégorie, 256 entrées d’historique, trois opérations, seize constats critiques et huit dérogations. Les limites s’appliquent conjointement ; leur qualification sur le paquet final relève de C17/C18.

### Frontière de confiance

La politique locale choisit les attentes de canal/version/source/composition, les autorités, l’ancre, le temps, le plancher de révocation et l’historique. Ces entrées ne sont jamais déduites de la seule preuve présentée par son auteur. Les contrôles figent les matériaux et la preuve avant d’appeler le fournisseur d’octets.

Une dérogation critique exige une correspondance exacte entre les champs signés et un reçu d’audit indépendant : constat, dérogation, motif, échéance, empreinte d’artefact et empreinte du reçu. Une mise à niveau exige de même un reçu indépendant de compatibilité lié aux versions précédente/cible et aux empreintes. L’authentification et la provenance de ces reçus sont garanties par le port local fiable consommateur ; N03 ne fabrique ni audit durable C05 ni qualification C17. Un booléen ou une déclaration libre de l’auteur ne remplace aucun reçu.

L’historique est fourni par le propriétaire fiable. L’identité est un tableau JSON canonique `[channel, source, composition, version]`, sans collision de séparateurs. Une identité publiée protège les trois empreintes. Une nouvelle version dans une lignée existante exige une version précédente connue ; le vérificateur n’invente aucun stockage d’historique.

### Points de contrôle et octets consommés

`check_install`, `check_startup` et `check_upgrade` revalident les signatures et les matériaux locaux à chaque appel. Ils retournent un `VerifiedArtifact` immuable contenant les octets mêmes qui ont été vérifiés, ainsi que leurs empreintes. Le consommateur utilise ces octets ; réouvrir un chemin modifiable ne constitue pas le protocole livré.

`assemble_proof` prend un port de signature explicitement choisi par l’appelant fiable. Aucun signataire de production, aucune clé privée et aucun coffre n’est implémenté ici. Les clés éphémères ne sont générées que dans le processus des tests autorisés, sous la racine du projet, avec nettoyage vérifié.

Les erreurs utilisent des codes sûrs et différenciés. Un désaccord de canal fournit les seules valeurs énumérées connues ; les valeurs libres, chemins et sorties OpenSSL ne sont pas recopiés dans les diagnostics.

### Livraison aux consommateurs et limites

C18 peut produire les preuves d’octets construits ; C17 peut consommer les mêmes octets et les reçus de ses recettes ; C19 conserve l’identité finale de release et la décision de publication. Les fixtures construisent une archive réelle en mémoire, consomment les octets vérifiés et comparent l’empreinte du fichier écrit. Cette preuve porte sur la fixture.

Aucun paquet Debian final, aucune installation système, migration, restauration ou publication externe n’a été exécuté. Ces recettes restent dans C17/C18/C19. Aucun succès N03 ne vaut disponibilité P0. Les résultats exécutés et la matrice de traçabilité figurent dans `VALIDATION.md` ; le rapport postarchive `STATISTIQUES.md` reste obligatoire avant la clôture du parent.
