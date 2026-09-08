# Statistiques de session de codage — define-pixs-specifications

### Suivi des agents — OC
| Champ | Valeur observée |
| --- | --- |
| Rôle | agent de codage OpenCode |
| Écritures | 16 deltas créés (lots B 3, F 5, G 8) ; tasks.md modifié 2× ; design.md modifié 1× ; STATISTIQUES.md créé sous la présente approbation |
| Corrections mineures | 4 coquilles corrigées dans les fichiers créés (accessibility, runtime, deb-package, docker-image) |
| Validations lancées | 6× `openspec validate define-pixs-specifications` (valides), 1× `openspec validate --all` (56/0), 1× `openspec archive --yes` ; 1 tentative abandonnée `--change` (option inconnue) |
| Appels MCP | 12 : 2 timeouts, 4 rejets -32602 pré-réparation du pont, 5 approuvés (reprise s001, NFDOC-A, mcp-8, mcp-9, mcp-2), 1 refus pour forme (mcp-3) |
| Mesures | 200 exigences / 200 scénarios (`grep -c`), 1 scénario par exigence ; deltas archivés 110 608 octets, specs principales 111 911 octets (`wc -c`) |

### Suivi des agents — CGPT
| Champ | Valeur observée |
| --- | --- |
| Rôle | contrôleur de validation, porteur du skill coding-session-statistics |
| Canaux | texte de session (lots B, F, G, ordres de service) puis pont MCP `oc-cgpt-approval-bridge` |
| Décisions MCP | 5 approuvées : reprise NDOC, NFDOC-A, NQCMOC `mcp-8` (option 1), NFDOC-C `mcp-9`, NFDOC-D `mcp-2` ; 1 refusée pour forme : NFDOC-E `mcp-3` |
| Arbitrages normatifs | convention française `DOIT`/`NE DOIT PAS` assumée, warnings RFC 2119 tracés (décision 5) |
| Actions correctives | réparation du pont MCP côté CGPT après les timeouts/rejets |

## Périmètre et sources

- Session OC↔CGPT du 2026-09-08 ; change spec-driven `define-pixs-specifications`, archivé sous `2026-09-08-define-pixs-specifications`.
- Sources normatives lues : AGENTS.md, PROJECT.md §34/§34.1/§35/§36, TECHNICAL.md (§6-§10, §25, §27, §29, §35-§38), BUILD.md (structure), openspec/config.yaml, 40 deltas préexistants.
- Structure conforme au skill `coding-session-statistics` appliqué par CGPT : tableaux H3 de suivi des agents en tête, six sections H2.

## Production OpenSpec

- Capacités spécifiées : 56/56 (liste PROJECT.md §34, ordre §35, lots A-G).
- Exigences : 200 ; scénarios : 200 (exactement 1 par exigence, vérifié par `grep -c`).
- Répartition par lot (exigences) : A 30, B 28, C 24, D 24, E 22, F 32, G 40.
- Deltas créés par OC : 16 (lots B 3, F 5, G 8) ; 40 préexistants repris sans modification.
- Volume : deltas archivés 110 608 octets ; specs principales synchronisées 111 911 octets (`wc -c`).
- Artefacts de clôture : tasks.md (cases 1.1-2.6 puis 3.1-3.3), design.md (décision 5), archive (commande unique).

## Flux MCP OC↔CGPT

- 12 appels `request_validation` : 2 timeouts (-32001) et 4 rejets (-32602) avant réparation du pont par CGPT ; 5 approuvés ; 1 refus pour forme (NFDOC-E `mcp-3`).
- Approbations : reprise NDOC (s001) ; NFDOC-A tasks.md ; NQCMOC `mcp-8` (option 1 convention française) ; NFDOC-C `mcp-9` (design.md) ; NFDOC-D `mcp-2` (tasks.md 3.1-3.3 + archive).
- Lots B, F, G validés par réponses CGPT explicites en texte de session (avant passage systématique au pont).

## Validations exécutées

- `openspec validate define-pixs-specifications` : 6 exécutions réussies (post-B, post-F, post-G ×2, post-tasks, post-design) — « Change is valid » à chaque fois.
- `openspec validate --all` final : 56 passed, 0 failed.
- Avertissements attendus : 200 WARNING RFC 2119 (convention française, décision 5) ; 1 warning non bloquant d'archive (>10 deltas, conforme décision 1).
- `openspec archive --yes` : +200 exigences / ~0 / -0 / →0 ; 56 specs créées ; change déplacé en archive.

## Écarts, correctifs et incidents

- 4 coquilles françaises corrigées dans les fichiers créés ; texte uniquement, périmètre inchangé.
- Incident canal : `mcp.cgpt-validation.timeout=30000` inadapté à la latence CGPT initiale ; pont indisponible puis réparé côté CGPT ; diagnostic OC (TCP + initialize JSON-RPC) ; conteneur OC basculé en réseau hôte par le développeur ; consolidation `127.0.0.1:8787` en attente (config non modifiée par OC).
- Périmètre d'écriture d'OC : strictement `openspec/changes/**` puis `openspec/specs/**` (via archive) ; aucun autre fichier touché ; aucun commit.

## Non disponibles (N/A)

- Relevé initial de quota : N/A (non fourni en début de session).
- Sondes modèle : N/A (non activées pendant la session).
