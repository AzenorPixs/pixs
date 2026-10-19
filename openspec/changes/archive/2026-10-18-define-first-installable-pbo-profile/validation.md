# Vérifications de préparation — 17 octobre 2026

## Livrables et périmètre

Vingt changes actifs C00–C19 ont été créés. Le [plan](plan-de-preparation.md) les relie et expose leurs dépendances. C00 contient neuf exigences proposées et dix scénarios répartis en trois deltas ; ils ne sont pas synchronisés dans le canon.

C01–C19 décrivent la réalisation future du canon existant. Leurs `requirements.md` conservent références, scénarios et empreintes, sans delta normatif artificiel. La métadonnée native `skip_specs: true` signifie uniquement qu’aucune évolution du comportement spécifié n’est prévue. Une nouvelle précision normative exigera son delta avant réalisation.

L’état natif « planning complete » constate la présence des documents ; il ne prouve ni la levée des barrières de conception, ni l’autorisation de coder, ni la réalisation des tâches. Les 196 tâches demeurent non cochées.

## Validation OpenSpec exécutée

| Commande | Exit natif | Résultat |
|---|---:|---|
| `openspec validate --changes --strict --json` | 0 | 20 changes valides, 0 échec |
| `openspec validate --all --strict --json` | 1 | 96 éléments passent, 2 sont signalés, sur 98 |

Les sorties natives complètes sont conservées dans [validation.json](validation.json).

Les quatre avertissements globaux sont préexistants et inchangés :

- `bulk-operations` : `requirements[6]`, `requirements[10]`, `requirements[13]`.
- `identity-assurance` : `requirements[4]`.

Message natif commun :

```text
Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior.
```

Aucune correction de ces textes canoniques n’a été effectuée et aucun succès strict global n’est revendiqué.

## Contrôles documentaires

- Vingt identifiants de changes uniques ; aucun candidat PA actif, Bulk, Docker ou option non sélectionnée créé.
- Références locales, structure, JSON, UTF-8/LF et absence de tâche cochée contrôlés.
- Dépendances résolues, graphe sans cycle ; ajout explicite de C05 à C03 et C04 après revue des obligations d’audit runtime.
- Cent quatre-vingt-treize exigences PZT référencées dans la table d’applicabilité ; ce classement ne certifie pas une recette ni l’exclusion de toutes les clauses d’un contrat conditionnel.
- Deux cent six empreintes d’entrées de la matrice inchangées, dont toutes les spécifications canoniques et les fichiers source/tests référencés.
- Ordre matériel initial de création, ordre final conseillé et ajustements de dépendances distingués dans [preparation.json](preparation.json).

## Non exécuté

Aucun test du produit, serveur, navigateur, connexion PostgreSQL, migration, installation, compilation produit, publication, commit, push, synchronisation ou archivage. Aucun code produit, configuration OpenCode, cadrage racine ou texte canonique modifié. Les modifications préexistantes du dépôt sont préservées.

Les choix ouverts du profil sont des barrières de conception visibles, notamment provider de secrets, sessions, contrats/identifiants PZT-DNS, architecture de packaging et identité de signature. La demande de préparation ne les valide pas implicitement et n’autorise aucune implémentation.
