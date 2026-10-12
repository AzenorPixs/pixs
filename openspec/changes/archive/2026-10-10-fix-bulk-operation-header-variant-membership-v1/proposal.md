# Correction — appartenance canonique des variantes Header

## Motivation

Le canon validé exige un membre BulkOperationVariant limité à IMPORT et EXPORT.
La garde actuelle contrôle seulement le type exact ; un objet de ce type créé
hors des membres peut être accepté. La lecture source établit cette lacune ;
la reproduction bornée sera conservée séparément comme preuve.

## Périmètre

Corriger uniquement la garde bulk_type de BulkOperationHeader par identité des
membres canoniques. Ajouter un objet forgé dans le test de refus existant.
Les diagnostics et les acceptations IMPORT/EXPORT restent identiques.

## Limites

Aucun changement du canon, profil, champ, façade, dépendance ou comportement
runtime. Aucun import/export effectif, transition, persistance, autorisation,
rattachement Job/tenant/scope ni modification de Status. Aucun Git.
