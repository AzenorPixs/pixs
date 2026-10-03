## 1. Preparation

- [x] 1.1 Prouver perimetre, absence de change actif et perimetre CGPT.
- [x] 1.2 Preparer les cinq artefacts et reussir la validation OpenSpec stricte avant code.

## 2. Descripteurs canoniques

- [x] 2.1 Creer src/pixs/kernel/capabilities.py seul, CapabilityDescriptor sept champs, build/bind purs, validation reprise, diagnostics sans echo, sans IO ni second resolution.
- [x] 2.2 Modifier composition.py additivement : champ capability_descriptors defaut (), renseignement par build/bind sur resolved_targets existants, algorithmes fournisseurs/conformite et semantique activated inchanges.
- [x] 2.3 Creer tests/unit/test_capability_descriptors.py : descripteurs exacts, liaison descriptive fourni/non consomme/resolu, tri canonique, refus sans echo, determinisme.
- [x] 2.4 Creer tests/integration/test_capability_descriptors_integration.py : subprocess frais, gardes IO causales avant import, liaison observable via compose sur manifests synthetiques, sans Django/PG/reseau.

## 3. Preuves

- [x] 3.1 Reussir tests unitaires puis integration sur l'executable DEVOPS actuel sous mandats distincts, sans assertion de temps ni fake hard deadline.
- [x] 3.2 Verifier AST 3.11 UTF-8 LF, perimetre module+composition+2 suites, relecture byteexact, diagnostics sans valeur brute, regression ciblee suites composition/conformite existantes sous runtime actuel, strict apres preuves, avant tout cochage.
- [x] 3.3 Prouver criteres precedents et delta normatif MOTAMOT sans nouveau scenario ; aucun etat de disponibilite, fanion, activation runtime ni pretendue couverture des trois autres exigences ; archivage et statistiques distincts apres controle.

Archivage et statistiques distincts apres preuves, conserves dans le RUN parent.
