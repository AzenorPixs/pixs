# Vérifications de préparation globale — 17 octobre 2026

## Résultat documentaire

Les 80 dossiers supplémentaires sont préparés ; les 100 candidats de l’inventaire sont désormais des changes actifs. Aucun code produit ni texte canonique modifié, aucune réalisation lancée. Les 996 tâches restent non cochées.

Chaque nouveau dossier contient `.openspec.yaml`, `proposal.md`, `design.md`, `tasks.md` et `requirements.md`. Ce dernier conserve intégralement les blocs canoniques référencés, sans delta artificiel ni perte de conditions et de bornes. Les 458 références de blocs des nouveaux dossiers peuvent se recouper : ce nombre ne mesure pas un travail produit. La correspondance globale couvre les 717 exigences et 812 scénarios de la matrice.

## Commandes natives exécutées

| Commande | Exit natif | Résultat |
|---|---:|---|
| `openspec validate --changes --strict --json` | 0 | 100 changes valides, 0 échec |
| `openspec validate --all --strict --json` | 1 | 176 éléments passent, 2 sont signalés, sur 178 |

Les sorties complètes sont dans [validation-globale.json](validation-globale.json). Les quatre avertissements globaux préexistants sont conservés : `bulk-operations` requirements[6], [10], [13] ; `identity-assurance` requirements[4].

Message natif commun :

```text
Requirement text is very long (>500 characters). Move examples and edge cases into scenarios, or split it into separate requirements that each state one behavior.
```

Aucun succès strict global n’est revendiqué. La validation des documents ne démontre pas une conformité runtime. Les métadonnées skip_specs de 99 changes indiquent qu’ils réalisent le canon existant ; elles ne dispensent d’aucun scénario et n’autorisent aucun comportement nouveau sans delta préalable.

## Contrôles complémentaires

- 100 identifiants uniques et 100 dossiers actifs correspondant exactement au catalogue ; 20 précédents et 80 nouveaux.
- Dépendances résolues, graphe sans cycle, ajustements C05/C03/C04 du premier P0 préservés ; conditions d’activation distinctes des dépendances de préparation.
- Blocs complets des nouveaux requirements.md recoupés avec ligne, titre, SHA-256 et scénarios du canon ; copies historiques clairement séparées des effets présents.
- Correspondance des 717 exigences conservée, sans transformer les 94 lignes NE en manque d’implémentation confirmé.
- Tous les liens documentaires locaux hors copies textuelles, JSON et fichiers texte contrôlés ; UTF-8/LF et absence de tâche cochée.
- Empreintes des 148 sources produit et des 206 entrées de référence du début de cette préparation recoupées. Depuis la matrice historique, seul DEVOPS avait été régénéré ; ce contexte relu est consigné, sans qualification implicite.
- Les 108 fichiers de la préparation P0 initiale ont été suivis par empreinte ; seule la page de coordination plan-de-preparation.md est actualisée pour ne plus annoncer les 80 candidats comme non créés. Les décisions, deltas et preuves P0 restent inchangés.

Le détail vérifié est conservé dans [preparation-globale.json](preparation-globale.json).

## Validations humaines et limites

Aucun arbitrage supplémentaire n’était nécessaire pour préparer les propositions conditionnelles demandées. Les décisions encore ouvertes sont recensées dans [arbitrages-preparation-globale.md](arbitrages-preparation-globale.md) et dans chaque conception. Elles ne sont pas implicitement approuvées ; seuls les choix qui affectent réellement les garanties sont soumis avant réalisation. Les paramètres déjà décidés restent opposables et les mesures restent à qualifier.

Aucun test produit, navigateur, connexion PostgreSQL, serveur, compilation produit, installation de dépendance, migration, activation, publication, Git, synchronisation, archivage, appel fournisseur ou lecture de secret pendant cette préparation. La création des dossiers ne sélectionne pas automatiquement leurs capacités dans le premier P0 et ne les rend pas tous prêts à coder.
