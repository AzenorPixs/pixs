## 1. Profil préparatoire

- [x] 1.1 Ajouter BulkOperationFormat gelé à deux champs obligatoires sans défaut, référence opaque conservée et format canonique.
- [x] 1.2 Ajouter la validation pure des types exacts et membres canoniques, avec diagnostics statiques VALIDATE triés/dédupliqués sans écho.
- [x] 1.3 Couvrir les cas conformes, étrangers, dérivés, hostiles, forgés et absents, l'immutabilité et le déterminisme par tests unitaires.
- [x] 1.4 Prouver import et validation dans un processus frais sous gardes à contrôles positifs, sans import concret pixs.core.

## 2. Validations avant archivage

- [x] 2.1 Compiler séparément les trois fichiers Python et exécuter les tests ciblés et régressions applicables.
- [x] 2.2 Valider strictement le change, contrôler l'identité du delta avec les quatre exigences canoniques et la cohérence des cadrages.
- [x] 2.3 Vérifier UTF-8/LF, absence de secret, périmètre et empreintes préservées, y compris PA/PZT; cocher seulement sur preuves.
