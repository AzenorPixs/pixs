# N03 — Confiance des artefacts avant installation

## Pourquoi

`artifact-publication` exige identité, signature, provenance, inventaire et révocation vérifiables avant installation/démarrage/mise à niveau (exigences 3–5). C18 transmet le paquet à C17 ; C17 l’installe pour sa recette ; C19, qui dépend de C17/C18, porte actuellement la réalisation de ces contrôles. Un ordre global acyclique de dossiers ne suffit donc pas : la recette peut précéder la disponibilité de son mécanisme de confiance.

## Préparation validée

Le développeur a validé ce dossier dédié le 17 octobre 2026 dans l’audit transversal P0. [Conception, responsabilités et critères](design.md). La préparation initiale ne valait pas autorisation de code ; la réalisation a ensuite été autorisée par le RUN 1CISMP2, dans les seules exigences canoniques existantes.

## Capacités et deltas

Aucun delta normatif nouveau prévu ; réalisation du canon existant, références dans requirements.md et skip_specs explicite.

Les deltas proposés restent dans le change ; aucune synchronisation ni archive pendant cette préparation. Les paramètres encore ouverts ne sont pas réputés approuvés.

## Dépendances et intégration

Voir les responsabilités et conditions de [design.md](design.md) et le [plan global courant](../archive/2026-10-18-define-first-installable-pbo-profile/plan-global-preparation.md). Les producteurs précoces de contrats, les conditions d’activation et la recette finale restent distincts.

## Impact

Préparation documentaire du chemin P0 ; pas d’activation d’option extérieure au profil, d’outil installé, de serveur sélectionné implicitement, de clé réelle, de migration ou de publication. La réalisation N03 est livrée : trois modules Python de matériaux/preuves/contrôles et trois suites de tests. Les 35 tests finaux et les compilations sont prouvés dans VALIDATION.md. Aucun paquet final ou publication externe n’est qualifié par ce lot.

## Dépendances après audit transversal P0

[C00](../archive/2026-10-18-define-first-installable-pbo-profile/proposal.md).

Les conditions d’activation et la construction des résultats sont séparées de cet ordre de préparation ; aucun cycle inverse vers la recette finale.

## Résultat du RUN 1CISMP2

Les points de contrôle installation/démarrage/mise à niveau renvoient les octets vérifiés eux-mêmes. La révocation locale est authentifiée, la rotation et les autorités sont contrôlées, l’identité publiée protège les trois empreintes. Les reçus d’audit et de compatibilité proviennent d’un consommateur local fiable, selon les limites de design.md. Les corrections RSMP approuvées portent uniquement sur deux phrases de BUILD.md et TECHNICAL.md. Le canon reste inchangé et skip_specs est conservé.
