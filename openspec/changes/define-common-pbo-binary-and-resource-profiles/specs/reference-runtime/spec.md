## ADDED Requirements

### Requirement: Admission indépendante de la sélection officielle Nuitka PBO

La sélection Nuitka PBO MUST provenir d'une observation directe HTTPS vérifiée et datée en UTC, suivie d'une revue explicitement autorisée du dossier figé. L'admission MUST lier le manifeste exact et la campagne dans un registre protégé distinct du candidat, non modifiable par le constructeur ou son appelant. Un booléen, un relevé auto-déclaré ou son empreinte seule MUST NOT établir cette autorité. Le constructeur MUST vérifier l'admission hors ligne.

#### Scenario: Observation et revue du manifeste exact

- **WHEN** une nouvelle campagne dispose d'une observation officielle exploitable, d'une sélection de la dernière stable non retirée, d'entrées figées vérifiées et d'une revue explicitement autorisée
- **THEN** une admission liée à l'identité de campagne et au manifeste exact est conservée dans le registre protégé, sans que cette décision seule autorise installation, compilation ou qualification

#### Scenario: Preuve auto-déclarée ou registre substitué

- **WHEN** le demandeur fournit un booléen de validation, une admission dans son candidat, une identité de responsable non autorisée ou un registre de remplacement
- **THEN** ces éléments ne valent pas admission et le contrôle refuse avant outils avec PBO_CAMPAIGN_EVIDENCE_INVALID, sans repli implicite ni compilation

#### Scenario: Observation officielle impossible ou non concluante

- **WHEN** HTTPS ou la date n'est pas vérifiable, la source est indisponible ou différente, ou que les données ne permettent pas d'établir la dernière stable non retirée
- **THEN** aucune sélection n'est admise, aucune preuve rétroactive n'est inventée et aucune ancienne version n'est choisie implicitement

### Requirement: Conservation et rattachement des preuves de sélection PBO

Le dossier figé MUST conserver entrées, manifeste, autorisation et admission sans réécriture. Le registre MUST préserver retraits et état courant ; une admission absente, retirée ou invérifiable MUST bloquer la construction. Le rapport MUST lier `selection_admission_ref`, `selection_admission_sha256` et `selection_manifest_sha256` aux preuves vérifiées, sans cycle d'empreintes. La reproduction MUST conserver dates et entrées sans nouvelle sélection.

#### Scenario: Altération ou échange après admission

- **WHEN** un fichier ou le manifeste est altéré, ou qu'une admission est présentée pour une autre campagne ou d'autres octets
- **THEN** les empreintes ou l'identité divergent, la construction est refusée avec PBO_CAMPAIGN_EVIDENCE_INVALID et les preuves d'origine restent conservées

#### Scenario: Retrait ou état courant non vérifiable

- **WHEN** l'admission est absente, retirée, inaccessible ou que son état courant est ambigu, y compris après restauration
- **THEN** la construction reste bloquée avec PBO_CAMPAIGN_EVIDENCE_INVALID, sans réactivation depuis une ancienne copie favorable

#### Scenario: Reproduction avec admission et rapport liés

- **WHEN** les entrées et l'admission de la campagne d'origine restent vérifiées et utilisables pour une reproduction
- **THEN** dates et versions d'origine sont conservées, le rapport lie les références et empreintes vérifiées d'admission et de manifeste, et le constructeur ne consulte pas PyPI pour sélectionner une autre version
