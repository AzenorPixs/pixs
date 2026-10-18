# Tâches — vocabulaire initial des états de publication d’événement v1

- [x] 1. Vérifier le canon B11 et OutboxPublicationV1, l’absence du vocabulaire, les limites du change et sa validation OpenSpec ciblée avant code.
- [x] 2. Fournir `src/pixs/backend/event_publication_state.py`, Enum pur aux cinq valeurs canoniques.
- [x] 3. Fournir les tests unitaires de contrat/refus et l’intégration avec import frais sous gardes d’effets vérifiées.
- [x] 4. Compiler séparément les trois fichiers ; exécuter les tests et régressions ciblés ; vérifier UTF-8/LF, conformité, périmètre et empreintes ; rapporter les validations OpenSpec ciblée stricte, globale standard et globale stricte avec leurs codes réels.

Les coches attendent les preuves natives examinées par CGPT. L’archivage puis `STATISTIQUES.md` font l’objet de mandats distincts après les validations ; aucune mesure absente n’est inventée.

## Preuves examinées par CGPT

- Inventaire lecture seule : rapport `msg_14c4afa71001IxQtFYD56arAsY`. Validation ciblée avant code : `req-7e368d4be6c34c9e`, exit 0.
- Module et deux tests : contenus exacts relus ; écritures natives unitaires corrélées.
- Trois compilations séparées : `req-0fa8b603f75b4ee3`, `req-b80cc77c3d98427b`, `req-380ff0d6046e4a86`, chacune exit 0.
- Tests : `req-efe7768ccaea4992`, 54 réussis en 0,982 s, exit 0 ; contrat, import frais sous gardes vérifiées et régressions backend/outbox. Aucun PostgreSQL réel requis.
- Validation ciblée après code : `req-1ee41ba5022448c6`, exit 0. Globale standard : `req-be06a35d088744ae`, 187 valides, 0 échec, exit 0.
- Globale stricte : `req-4bc3d2aa5309403f`, 185 valides et 2 capacités signalées, exit 1 : quatre WARNING de longueur dans bulk-operations requirements[6]/[10]/[13] et identity-assurance requirements[4], zéro ERROR. Ces canons sont inchangés ; ce résultat n’est pas présenté comme un succès strict global.
- Les 16 fichiers existants suivis par empreinte sont inchangés ; sources nouvelles UTF-8/LF, sans changement de façade ou de canon. Matrice cadrages/README revue dans le périmètre du vocabulaire ; aucune mise à jour nécessaire. Git non inspecté, provenance historique non vérifiée.
