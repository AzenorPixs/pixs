# add-initial-bulk-operation-status-v1

## Pourquoi

La RSMP validée définit le profil structurel préparatoire BulkOperationStatus v1.
Le Kernel ne possède pas encore cette représentation interne ni sa validation pure.

## Ce qui change

- Ajouter src/pixs/kernel/bulk_operation_status.py : représentation immuable
  à deux champs explicites et validateur produisant des diagnostics statiques.
- Ajouter des tests unitaires et une intégration en processus frais sous gardes d'effets.
- Réutiliser BulkOperationState, Diagnostic et VALIDATE existants.

## Impact

Capacité concernée : bulk-operations. Le delta MODIFIED reprend à l'identique
les trois exigences BulkOperationStatus v1 déjà présentes dans le canon.
Aucun nouveau choix normatif, dépendance, export de façade, état/transitions,
rattachement Job, autorisation, persistance, import ou export effectif.
L'archivage utilisera --skip-specs après preuve de cette identité canonique.
Les avertissements de longueur sont qualifiés séparément selon le prompt.
