# Proposal

## Why

Le parcours local de validation d'un `component.toml` n'a pas de point d'entrée public unifié : les appels directs au parser noyau exposent des diagnostics bruts pouvant contenir une entrée non fiable (valeur, nom de clé, chemin privé, version reproduite). Le change fournit une façade locale à résultat immuable avec diagnostics sanitisés (champ/règle, jamais de valeur), sans activation ni Kit complet.

## What Changes

- Ajoute `src/pixs/developer_kit/` : façade `validate_manifest_text` (pure, sans FS) et `validate_manifest_file` (fichier exact seulement sur demande explicite de l'appelant), type retour immuable `ValidationReport`, sanitisation vers vocabulaires fermés champ/règle avec repli `manifest : entrée invalide`, ports publiés `kernel.manifest` + `kernel.diagnostics` uniquement.
- Ajoute `src/pixs/developer_kit/README.md` : documentation du parcours local (écrire → valider → lire diagnostics champ/règle, sans secret/réseau/production).
- Ajoute tests unitaires (enveloppe, sanitisation, adversariaux sans affichage de valeurs) et test d'intégration validant `src/pixs/example/component.toml` via le kit.
- Aucune activation, aucun provisionnement, aucune publication, aucune dépendance nouvelle, aucun secret, aucun réseau.

## Capabilities

### New Capabilities

Aucune.

### Modified Capabilities

- `developer-experience` — `Parcours local reproductible` : le parcours utilise la façade et ses validateurs publiés, sans secret ni donnée de production.
- `developer-experience` — `Diagnostics sans fuite` : les diagnostics associent champ et règle attendue sans révéler secret, credential, donnée de production ou détail privé ; les entrées non fiables sont repliées sans écho.
## Impact

Code : nouveau paquet `src/pixs/developer_kit/` + README + 2 fichiers de tests. Docs : parcours local documenté. Tests : unitaires + intégration mémoire. Aucune modification du noyau, des specs canoniques, des cadrages ou des dépendances. Dépendance réutilisée : component-model et ses exigences de schéma existantes ; aucune modification ni delta pour cette capability. Pas de Kit complet ni de preuve de conformité production ; P0 global, runtime et audit durable restent non prouvés.
