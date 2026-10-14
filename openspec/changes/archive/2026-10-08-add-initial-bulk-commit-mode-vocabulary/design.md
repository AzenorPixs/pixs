# Conception — Modes d’import en masse

## Contrat représenté

`BulkCommitMode` est une Enum de la bibliothèque standard. Ses seuls membres, dans l’ordre de l’exigence canonique, sont VALIDATE_ONLY, ATOMIC, ATOMIC_PER_CHUNK et BEST_EFFORT, avec nom égal à la valeur. Le module interne expose seulement ce symbole dans `__all__`, sans réexport à la racine du noyau.

Cette représentation ne choisit aucun mode et ne réalise aucune transaction. La distinction entre validation seule, atomicité globale, atomicité par lot et traitement au mieux demeure à implémenter dans le contrat d’import complet. Les conflits restent rejetés par défaut conformément au canon ; cette unité ne crée pas de politique de conflit.

## Choix minimal

Réutiliser Enum comme les vocabulaires existants ; aucun validateur, diagnostic, factory, valeur par défaut, provider ou dépendance n’est ajouté. Le noyau conserve ses façades publiques.

## Vérifications

Le canon bulk-operations est contrôlé avant création. Le change est validé strictement avant et après code. Compiler le module avec l’interpréteur déclaré, inspecter son import isolé et sa surface, puis exécuter les suites existantes sur la pureté, les façades et les vocabulaires voisins. Contrôler UTF-8/LF, les seuls fichiers autorisés et les empreintes initiales.

L’archive n’ajoute aucune exigence au canon : le delta MODIFIED reprend exactement l’exigence et son scénario. L’archivage et STATISTIQUES.md demandent chacun un mandat distinct après les preuves.
