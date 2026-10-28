## ADDED Requirements

### Requirement: Fournisseur BIND 9 du DNS géré sur Debian et Docker Pixs

Sur Debian et dans Docker Pixs, le fournisseur DNS retenu MUST être BIND 9 fourni par Debian. PBO/pixs.dns MUST conserver la gestion par contrats publics ; le PA désigné MUST porter installation, configuration et lifecycle du serveur distinct. Ce choix MUST NOT sélectionner ni activer implicitement le DNS dans C14. A06c–A06k et les contrôles applicables restent opposables.

#### Scenario: Gestion PBO et exécution PA séparées

- **WHEN** un rôle serveur DNS BIND 9 est sélectionné et admis sur une cible Debian ou Docker Pixs
- **THEN** PBO administre le souhaité par les contrats publics du module DNS et le PA désigné applique les seules opérations autorisées au serveur distinct
- **AND** aucune écriture de table privée inter-modules ni exécution directe par Django ne remplace ces propriétaires

#### Scenario: Présence logicielle sans activation

- **WHEN** BIND 9 est présent mais le rôle serveur DNS n'est pas sélectionné ou admis
- **THEN** présence logicielle, configuration souhaitée, état appliqué et disponibilité MUST rester distincts ; aucun résultat de résolution absent n'est déduit du logiciel
- **AND** les fonctions de gestion de pixs.dns restent distinctes de cette disponibilité ; un PA client MUST NOT devenir serveur par la seule présence du logiciel

#### Scenario: Exécutant ou transport obligatoire indisponible

- **WHEN** une application DNS requiert un PA désigné ou un transport PZT admissible indisponible
- **THEN** l'opération reste bloquée ou d'issue explicitement inconnue selon les faits établis
- **AND** aucun canal de substitution, succès ou mesure absents n'est fabriqué
