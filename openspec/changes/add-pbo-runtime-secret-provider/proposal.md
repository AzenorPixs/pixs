# C01 — Configuration et secrets effectifs

## Pourquoi

Les références de secrets et la résolution de configuration sont pures ; check_template conserve secrets_resolved=False. Aucun provider de secrets opérationnel n’est démontré.

## Modifications proposées

Sélectionner un SecretProvider concret externe au Kernel ; fournir les réglages runtime validés, identité de workload, accès, rotation/révocation et diagnostics minimisés. Aucun nouveau fournisseur ou format implicite.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions de profil proposées dans C00.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `define-first-installable-pbo-profile`.

## Impact

Périmètre de réalisation futur : Garder le Kernel déclaratif et résoudre les références dans un adapter backend sélectionné. Associer résolution, finalité, propriétaire et identité de workload. Le démarrage ne devient prêt que si références et politiques obligatoires sont vérifiables ; prévoir rotation, révocation, rafraîchissement et audit sans valeur sensible.

La demande actuelle autorise uniquement les documents de ce dossier. Aucun code, test produit, migration, dépendance, configuration runtime, Git, déploiement ou publication n’est modifié/exécuté. Les tâches ci-jointes ne sont pas lancées.

## Critères de sortie de réalisation future

Secret requis absent/révoqué → démarrage refusé ; workload non autorisé → refus ; rotation testée ; aucune valeur dans configuration distribuée, artefacts ou diagnostics.

## Barrière de conception

Provider concret et transport d’identité workload ; mécanisme de stockage des références et politique de rotation/révocation. Décision de sécurité requise avant réalisation, avec dernières versions compatibles qualifiées si une dépendance devient nécessaire.
