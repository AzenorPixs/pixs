## ADDED Requirements

### Requirement: Admission de production du profil local avec secrets protégés

L’admission en production du profil Debian local MUST relier l’artefact installé aux preuves de protection des secrets d’amorçage et de récupération sans ancien hôte selon la politique retenue. Un profil host+tpm2 non qualifié ou une récupération non prouvée MUST empêcher cette admission. La livraison fonctionnelle C01 MUST rester distincte de ces preuves et du verdict global P0.

#### Scenario: Provider livré et récupération absente

- **WHEN** C01 est livré mais qu’aucun exercice conforme sans ancien TPM ne démontre la récupération du profil retenu
- **THEN** l’installation ne revendique pas l’admission de production au titre de cette protection

#### Scenario: Protection et secours prouvés pour un artefact

- **WHEN** la plateforme, le mode de protection, la récupération et leur correspondance à l’artefact installé sont prouvés
- **THEN** cette dimension peut être admise sans valider automatiquement les autres obligations de la composition
