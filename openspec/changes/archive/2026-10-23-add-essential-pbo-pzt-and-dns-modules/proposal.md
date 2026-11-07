# C14 — Modules essentiels PZT et DNS

## Pourquoi

Le constat initial relevait l’absence des modules essentiels PZT/DNS exigés par le canon. C14 fournit désormais leurs responsabilités de gestion, leurs données, contrats et surfaces ; les preuves et garanties effectivement qualifiées figurent dans VALIDATION.md.

## Modifications proposées

Livrer le module essentiel pixs.pzt et le module DNS essentiel, propriété de leurs données, contrats publics, administration et état réseau désactivé. Le périmètre exact dépend de l’examen clause par clause C00 ; une simple page “désactivé” ne suffit pas. Toute clause impérative exigeant PA/DNS actif ajoute D01 au chemin critique.

## Capacités

### Capacités nouvelles

Aucune évolution normative nouvelle n’est prévue : ce dossier prépare la réalisation des comportements déjà exigés par le canon et les précisions du profil C00 adoptées le 18 octobre 2026 et intégrées au canon.

### Capacités modifiées

Aucun texte canonique modifié par ce dossier. `requirements.md` relie les exigences et scénarios sources ; `skip_specs: true` évite un delta artificiel. Si la conception exige un comportement nouveau ou une modification normative, un delta devra être présenté et approuvé avant réalisation.

## Dépendances

- `define-first-installable-pbo-profile`.
- `add-core-postgres-services`.
- `integrate-runtime-authorization-and-super-admin`.
- `add-durable-minimized-audit`.
- `add-protected-core-http-commands-and-queries`.
- `compose-modular-frontend-with-core-api`.

## Impact

Périmètre réalisé : deux responsabilités de gestion PBO propriétaires pixs.pzt et pixs.dns composées par les mécanismes communs ; manifests, contrats, migrations et liaisons publiques explicites. Conserver configuration souhaitée, versions et états d’absence d’exécutant ; appliquer les choix validés pertinents à la configuration. N’engager aucun PA, service DNS ou réseau non sélectionné, ni canal de substitution.

La réalisation et les tests ont été explicitement demandés dans le cycle 1CISMP4, après la reprise documentaire bornée validée. Cette invocation autorise la clôture de ce seul change avec archivage, statistiques et publication CAB ; Git, déploiement et activation BIND 9 restent hors périmètre. Aucun canon ni dépendance n’est modifié.

## Critères de sortie de réalisation

Modules composés même réseau désactivé ; absence essentielle bloquante ; configuration/visualisation/supervision honnêtes ; aucune mesure ni application réseau inventée ; aucun canal PBO–PA de substitution ; chaque clause conservée, motivée ou renvoyée vers évolution normative approuvée.

## Barrière de conception

Identifiants canoniques et contrats de gestion, sous-modules et schémas ; recouper chaque clause applicable de la table C00. Toute obligation active non conditionnelle rejoint le chemin critique ; aucune exemption supposée.
