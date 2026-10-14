## MODIFIED Requirements

### Requirement: Profil structurel préparatoire d'occultation de champ d'audit v1

Le profil d'occultation v1 MUST être une représentation interne, immuable et purement mémoire comportant exactement field_reference, mode et replacement_reference. Tous les champs MUST être fournis explicitement, sans valeur par défaut ni champ de payload avant/après.

field_reference MUST être une str exacte non vide, opaque et sans normalisation. mode MUST être une valeur exacte de l'Enum fermé RedactionMode contenant uniquement REDACTED et PSEUDONYMIZED_REFERENCE ; bool et toute sous-classe MUST être refusés. En mode REDACTED, replacement_reference MUST être None explicite ; en mode PSEUDONYMIZED_REFERENCE, replacement_reference MUST être une str exacte non vide, opaque et sans normalisation. Ces valeurs MUST provenir d'un appelant de confiance ou de fixtures synthétiques ; None MUST NOT être interprété comme une autorisation, une exemption de rétention ou une décision d'applicabilité.

La validation MUST porter uniquement sur la structure exacte et produire des diagnostics statiques VALIDATE, triés et dédupliqués, sans reproduire les valeurs. Elle MUST NOT inspecter un payload avant/après, consulter une classification, résoudre une référence, lire une horloge, effectuer une entrée/sortie, ni déduire une occultation, une pseudonymisation ou une minimisation effectives.

Ce profil préparatoire MUST NOT valoir occultation effective, preuve d'audit persistant, politique de rétention, intégrité, autorisation ni événement d'audit. Les exigences générales d'audit, de minimisation, d'append-only, de purge et de protection des données personnelles restent intégralement applicables aux futures intégrations. Aucun wire format, provider, façade publique, politique, configuration ou nouvelle dépendance n'est introduit par ce profil.

#### Scenario: Structure valide sans effet

- **WHEN** un appelant de confiance fournit les trois champs avec leurs types et contraintes déclarés, en REDACTED avec replacement_reference None ou en PSEUDONYMIZED_REFERENCE avec une référence opaque non vide
- **THEN** la validation ne produit aucun diagnostic ni effet et la représentation conserve exactement ces valeurs

#### Scenario: Structure invalide refusée sans écho

- **WHEN** une valeur a un type ou une forme interdite, notamment un mode hors de l'Enum fermé, une valeur booléenne, une référence vide dans un mode pseudonymisé, une référence non None en mode REDACTED ou un mode de sous-classe
- **THEN** la validation produit des diagnostics statiques triés et dédupliqués sans reproduire les valeurs ni fournir de garantie runtime
