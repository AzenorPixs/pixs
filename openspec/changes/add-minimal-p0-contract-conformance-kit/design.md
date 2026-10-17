# Conception — N06 : Kit minimal de conformité des contrats P0

Découpage dédié validé explicitement par le développeur le 17 octobre 2026, sans implémentation.

## Écart démontré

`testing` #2/#3 exige un Developer Kit et des suites versionnées par contrat, ainsi que l’exclusion d’un provider dont la conformité obligatoire manque/expire/échoue. `developer-experience` exige le parcours local de l’exemple P0. Le kit actuel valide des manifests ; [validators.py](../../../src/pixs/developer_kit/validators.py) documente explicitement qu’il n’est ni kit complet ni preuve de conformité production. [example/demo.py](../../../src/pixs/example/demo.py) est une démonstration pure.

C17 prévoit la matrice, l’exécution et les preuves sur paquet, sans détailler la production d’un kit minimal réutilisable et de ses suites. O22 porte le kit/CLI complet et dépend des SDK O21 et de C17 ; le rendre entièrement obligatoire étendrait le P0. Il faut donc préciser qui fournit cette partie obligatoire avant la recette.

## Préparation recommandée

Créer `add-minimal-p0-contract-conformance-kit` pour les seules capacités/providers du profil : sélection des suites par contrat/version, résultat et portée explicites, provenance des preuves fournie par l’exécuteur de confiance, diagnostic sûr, parcours d’exemple tenant/scope/autorisation. Réutiliser les validateurs et exemples existants. Ne pas transformer le code d’exemple en dépendance de production.

C17 conserve la qualification du paquet final et l’agrégation des preuves ; O21/O22 conservent SDK et CLI complète. Les contrats C06/C07/C09/C10/C11/C14/N01 fournissent les points à qualifier ; aucune dépendance inverse du code d’hôte vers la recette finale. Une condition d’activation exige les preuves applicables, sans créer un cycle de préparation.

## Critères futurs

Suite absente, mauvaise version, expirée ou échouée : sélection/activation refusée selon canon. Résultat unitaire non présenté comme intégration ; exemple reproduit sans secret ni donnée de production, mutation persistante seulement dans fixture autorisée et via contrat propriétaire. Deux exécutions identiques donnent même graphe et verdicts équivalents, sans confondre champs de manifest et preuve signée par un exécuteur.

## Validité des preuves et absence de cycle

Le porteur ConformityAttestation existant reste structurel et inchangé. L’exécuteur de confiance vérifie provenance et validité avant de fournir les attestations ; le Kernel ne devient ni exécuteur de suite ni autorité cryptographique. Le format externe, la durée de validité et le mécanisme d’authentification sont des décisions à revoir avant code.

C07 peut fournir son hôte intermédiaire avant ce kit, avec readiness P0 refusée tant que les preuves obligatoires manquent. N06 qualifie les contrats disponibles et C17 la composition installée finale. Il n’existe donc pas de dépendance ferme C07 → C17 ni C07 → N06 ; les conditions d’activation restent explicites.

## Portée de préparation et retour

Aucun code produit, secret, compte, service, dépendance, migration, données réelles, signature ou publication n’est manipulé par cette préparation. Les tâches restent futures et non cochées. Une évolution persistante ultérieure exige schéma/version, contrat de compatibilité et reprise/compensation revue ; aucun downgrade automatique ni purge implicite.

## Dépendances après audit transversal P0

[C06](../add-protected-core-http-commands-and-queries/proposal.md), [C07](../activate-reference-runtime-composition/proposal.md), [C09](../add-reference-worker-scheduler-and-event-delivery/proposal.md), [C10](../enforce-core-data-governance-and-lifecycle/proposal.md), [C11](../compose-modular-frontend-with-core-api/proposal.md), [C14](../add-essential-pbo-pzt-and-dns-modules/proposal.md), [N01](../add-pbo-security-quarantine-and-revocation/proposal.md).

Les conditions d’activation et la construction des résultats sont séparées de cet ordre de préparation ; aucun cycle inverse vers la recette finale.
