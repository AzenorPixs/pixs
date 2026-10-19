## ADDED Requirements

### Requirement: Gestion PZT et DNS du profil initial sans exécution réseau

Dans le profil initial PBO/PFO sans réseau sélectionné, PBO MUST conserver les modules de gestion `pixs.agent` (PA hors PZT) et `pixs.pzt` (PZT), le module DNS essentiel et leurs fonctions de gestion sous contrats publics. Les états MUST distinguer configuration souhaitée, absence d’exécutant et état appliqué. Le système MUST NOT fabriquer une mesure réseau.

#### Scenario: Service DNS non sélectionné

- **WHEN** le module de gestion DNS est composé sans exécution sélectionnée du service DNS
- **THEN** sa présence est vérifiable mais aucun serveur DNS disponible ni configuration réseau appliquée n’est annoncé

### Requirement: Exécution PA non sélectionnée et absence de canal substitué

Le profil initial sans exécution PA ou PZT sélectionnée MUST NOT engager d’échange PBO–PA ni activer implicitement PZT ou un service DNS. Toute sélection ultérieure MUST respecter les contrats PA/PZT applicables ; la proximité locale MUST NOT permettre un canal de substitution hors PZT.

#### Scenario: Tentative de contrôle local sans PZT admissible

- **WHEN** une opération nécessite un exécutant PA mais aucun transport PZT admissible n’est sélectionné
- **THEN** l’opération est refusée sans repli par fichier, socket ou canal loopback hors PZT

### Requirement: Applicabilité des contrats PZT dans le profil initial

La qualification du profil MUST évaluer les clauses PZT selon leurs rôles et conditions, y compris la gestion PBO. Les exigences d’exécution non sélectionnées MUST rester conservées ; une obligation applicable non satisfaite MUST bloquer la qualification. La correspondance canonique PA/PZT conserve références, valeurs, garanties et portée des identités et preuves.

#### Scenario: Clause obligatoire dans un contrat conditionnel

- **WHEN** un contrat principalement exécutant contient une obligation applicable à la gestion PBO du profil
- **THEN** cette obligation reste vérifiée et n’est pas exclue par le classement général du contrat
