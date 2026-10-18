# Tâches — vocabulaire initial des états de décision d’architecture v1

- [x] 1. Vérifier les artefacts, le canon inchangé et la validation OpenSpec ciblée avant code.
- [x] 2. Fournir le module pur ArchitectureDecisionState conforme à la convention Enum.
- [x] 3. Vérifier syntaxe, contrat unitaire, import en processus frais et régressions applicables.
- [x] 4. Vérifier UTF-8/LF, périmètre des seules écritures autorisées et validations OpenSpec finales.

Preuves : validation stricte ciblée exit 0 avant code ; source exacte ; py_compile des trois modules exit 0 ; 19 tests réussis, dont import frais avec gardes et régressions pureté/façades ; contrôle UTF-8/LF et empreintes des canons/cadrages inchangés. Global standard : exit 0. Strict global : exit 1, quatre avertissements de longueur dans bulk-operations (requirements 6, 10, 13) et identity-assurance (requirement 4), aucune erreur ; architecture-decisions et ce change valides. L’archive et le rapport restent des obligations de clôture distinctes, non anticipées par les coches.
