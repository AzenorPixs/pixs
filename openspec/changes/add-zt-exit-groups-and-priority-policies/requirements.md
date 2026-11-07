# Références normatives — Z31

Plan ACL-PIXS-2026-10-31-E3-R1, validé ; relevé du 31 octobre 2026. Les blocs ci-dessous sont des copies de référence, jamais des deltas ADDED/MODIFIED ni une autorité indépendante du canon. Leur présence ne prouve aucune réalisation.

## Traçabilité des exigences et scénarios

| Capacité | Exigence cible | Scénarios | Référence |
|---|---|---:|---|
| zt-network-services | EZT distinct facultatif et groupes | 1 | zt-network-services-b00860d61906 |
| zt-network-services | Répartition et continuité EZT | 1 | zt-network-services-c0d7619c05f7 |
| zt-network-services | Santé par chemin et famille IP | 1 | zt-network-services-c1574cf12e7f |

## Blocs sources complets

### Référence zt-network-services-b00860d61906

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 65. SHA-256 du bloc : `b00860d61906096ec9ea962760d5179c2fe18efe94fb63f59d6ff06c71ba7017`.

Scénarios sources : EZT externe.

~~~~text
### Requirement: EZT distinct facultatif et groupes

EZT MUST être un rôle distinct optionnel et désactivé par défaut, avec référence CZT et état RAM sans PG propre. Les politiques de sortie MUST pouvoir désigner des groupes avec niveaux de priorité et membres explicitement autorisés, y compris externes par approbation sans changement d'appartenance.

#### Scenario: EZT externe

- **WHEN** un groupe référence un EZT d’un autre ZT
- **THEN** son inclusion et son usage exigent les autorisations applicables sans le rendre membre local.
~~~~

### Référence zt-network-services-c0d7619c05f7

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 74. SHA-256 du bloc : `c0d7619c05f7a300a5d837375353b23fb94b2feb3e02ace22969c3f13e1984d9`.

Scénarios sources : Groupe indisponible.

~~~~text
### Requirement: Répartition et continuité EZT

Les nouvelles connexions MUST être réparties entre les EZT admissibles du meilleur niveau disponible, avec poids configurables égaux par défaut. Chaque connexion MUST conserver son EZT tant que possible ; retour au préféré MUST être configurable avec maintien des connexions par défaut. L’absence de membre utilisable MUST conduire au blocage, sans sortie directe implicite.

#### Scenario: Groupe indisponible

- **WHEN** aucun EZT du groupe autorisé n’est utilisable
- **THEN** le trafic concerné reste bloqué sans utiliser une sortie non autorisée.
~~~~

### Référence zt-network-services-c1574cf12e7f

Source : [zt-network-services](../../specs/zt-network-services/spec.md), ligne 83. SHA-256 du bloc : `c1574cf12e7feae841d07b444e6750c07e271dde0efb6f59d151857480319c54`.

Scénarios sources : Sortie IPv6 rompue.

~~~~text
### Requirement: Santé par chemin et famille IP

Les groupes EZT MUST avoir critères de santé configurables par chemin et famille IP, avec temporisations d'exclusion et réadmission. La santé IPv4 MUST NOT suffire à qualifier le chemin IPv6 ni un simple processus vivant à qualifier la sortie.

#### Scenario: Sortie IPv6 rompue

- **WHEN** un EZT fonctionne en IPv4 mais échoue aux critères IPv6
- **THEN** son admissibilité IPv6 est traitée séparément.
~~~~
