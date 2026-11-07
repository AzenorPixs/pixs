# Exigences de réalisation — C09

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 adopté le 18 octobre 2026 et intégré au canon apporte les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| events / 8 | [Événements immuables versionnés](../../../specs/events/spec.md#L8) | P | Contrat d'intégration séparé |
| events / 17 | [Publication après validation transactionnelle](../../../specs/events/spec.md#L17) | P | Transaction échouée sans événement |
| events / 26 | [Consommateurs idempotents et ordonnés](../../../specs/events/spec.md#L26) | P | Rejou sans double effet |
| events / 35 | [Profil préparatoire de déclaration d'enregistrement d'événement v1](../../../specs/events/spec.md#L35) | P | Déclaration passive de contrat de domaine ; Contrat d'intégration distinct |
| events / 49 | [Validation fermée de la déclaration d'enregistrement v1](../../../specs/events/spec.md#L49) | P | Référence ou type étranger refusé ; Contrat porté invalide |
| events / 63 | [Frontière préparatoire de la déclaration d'enregistrement v1](../../../specs/events/spec.md#L63) | P | Validité structurelle sans admission runtime |
| events / 72 | [Runtime Bulk v1 B11 — Outbox et publication](../../../specs/events/spec.md#L72) | P | Rollback sans publication ; Livraison répétée |
| interactions / 8 | [Application de l'exception Super Admin](../../../specs/interactions/spec.md#L8) | P | Command propriétaire avec dérogation métier |
| interactions / 18 | [Commandes validées et autorisées](../../../specs/interactions/spec.md#L18) | P | Mutation sans autorisation refusée |
| interactions / 27 | [Requêtes sans mutation implicite](../../../specs/interactions/spec.md#L27) | P | Lecture filtrée à la source |
| interactions / 36 | [Idempotence et traçabilité des commandes](../../../specs/interactions/spec.md#L36) | P | Rejou divergent |
| interactions / 45 | [Runtime Bulk v1 B10 — Idempotence durable](../../../specs/interactions/spec.md#L45) | P | Rejeu identique ; Rejeu divergent |
| jobs / 8 | [Exécution asynchrone demandée par le Super Admin](../../../specs/jobs/spec.md#L8) | P | Worker sans compte de service Super Admin ; Nouvelle exécution après désactivation |
| jobs / 22 | [Contrôles applicatifs des Jobs et exception](../../../specs/jobs/spec.md#L22) | P | Dérogation portée par la demande initiale |
| jobs / 31 | [Persistance et états explicites](../../../specs/jobs/spec.md#L31) | P | Reprise après interruption |
| jobs / 40 | [Autorisation réévaluée à l'exécution](../../../specs/jobs/spec.md#L40) | P | Contexte expiré refusé |
| jobs / 49 | [Idempotence et corrélation des travaux](../../../specs/jobs/spec.md#L49) | P | Double déclenchement dédupliqué |
| jobs / 90 | [Runtime Bulk v1 B08 — Jobs et liaison persistante](../../../specs/jobs/spec.md#L90) | P | Phase persistante ; Liaison multiple |
| jobs / 104 | [Runtime Bulk v1 B09 — Baux, reprise et configuration](../../../specs/jobs/spec.md#L104) | P | Reprise sous bail ; Bail périmé |
| runtime / 130 | [Profils distincts d'un même artefact](../../../specs/runtime/spec.md#L130) | P | Profil activé par configuration |
| runtime / 139 | [Profils de déploiement déclarés](../../../specs/runtime/spec.md#L139) | P | Capacité absente dans un profil local |
| runtime / 151 | [Exposition minimale par défaut](../../../specs/runtime/spec.md#L151) | P | Endpoint de management publiquement joignable |
| runtime / 160 | [Processus stateless et coordination persistante](../../../specs/runtime/spec.md#L160) | P | Redémarrage d'un worker ; État technique PA requis en conteneur |
| runtime / 174 | [Lease du scheduler avec clôture de péremption](../../../specs/runtime/spec.md#L174) | P | Ancien détenteur toujours actif |
| runtime / 183 | [Arrêt, drain et reprise contrôlés](../../../specs/runtime/spec.md#L183) | P | Arrêt pendant traitement |
| runtime / 192 | [États techniques PA et PZT distincts du runtime PBO](../../../specs/runtime/spec.md#L192) | P | Recréation du conteneur PA PZT |

## Empreintes SHA-256 du canon

- `openspec/specs/events/spec.md` : `31af2e0a1ae55bc575b9f0edb906e73d0b707e8c68458d680155251ea587bf14`.
- `openspec/specs/interactions/spec.md` : `9a2e9186b51c70c17781e2395da3e42f83dd2cc90da36bab624d90397d4ab9a0`.
- `openspec/specs/jobs/spec.md` : `82b83d6b62e3d8c2246ed8a7daf986ac6d16e66745cfab69ccd2afddf956891d`.
- `openspec/specs/runtime/spec.md` : `130f1c090012bf9180ccee1b4a71926de47183bcf6b69539608a3a8e5e5a73ac`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.


## Recoupement RSMP C09 du 22 octobre 2026

Le développeur a validé cette reprise limitée à requirements.md et design.md, ainsi que les choix de conception ci-dessous, dans le RUN CISMP2. Ce recoupement actualise les références et leurs conditions ; il ne modifie aucun canon et ne constitue pas une preuve de réalisation. Les quatre capacités comptent actuellement 7 exigences events, 5 interactions, 10 jobs et 16 runtime. Les numéros de ligne et empreintes ci-dessus désignent cette relecture ; les textes complets priment sur ces repères.

Les ajouts canoniques suivants sont également examinés dans C09 :

| Capacité / ligne | Exigence et scénarios courants | Application et contrôle C09 |
|---|---|---|
| jobs / 58 | Structure de JobDeduplicationReferenceV1 ; Références conservées exactement | Préserver le profil immuable et ses références exactes ; ne pas le présenter comme une déduplication persistante. |
| jobs / 67 | Validation fermée de JobDeduplicationReferenceV1 ; Type étranger refusé sans effet ; Référence vide refusée | Réutiliser la validation structurelle si ce profil est consommé, sans coercition ni écho. La déduplication runtime conserve ses propres preuves transactionnelles. |
| jobs / 81 | Limites de JobDeduplicationReferenceV1 ; Validation sans effet de déduplication | Aucune modification de ce contrat préparatoire ; tests de non-régression et séparation explicite du runtime. |
| runtime / 23 | Modes d'exploitation PBO Standalone et ZT ; Exploitation Standalone sans réseau activé ; Exploitation ZT ; Transport PZT en mode Standalone | C09 fournit les rôles du même PBO sous sélection explicite. Aucun échange PA/PZT ni qualification ZT n'est créé par le worker ; une capacité requise absente reste non prête. |
| runtime / 42 | Profil de ressources par environnement d'exécution ; Quota inférieur aux ressources physiques ; Exécutant distant | Le plan C09 reçoit le budget effectif de l'environnement, sans déduire le budget d'un exécutant distant de celui de PBO. Refuser un budget absent ou non vérifiable. |
| runtime / 56 | Dimensionnement explicite et borné des processus ; Multiplication des connexions ; Rôle inconnu ou budget invalide | Déclarer rôles, processus, concurrence, files et plafonds nécessaires ; contrôler les cumuls et refuser rôle ou plan invalide avant admission. |
| runtime / 70 | Proposition de dimensionnement sous configuration ; Détection sans politique d'adaptation ; Adaptation sous politique | Aucune adaptation automatique implicite. C09 applique seulement le plan explicite autorisé et borné ; aucune qualification de dimensionnement universel. |
| runtime / 84 | Ressources détectées demandées et appliquées distinctes ; Application partielle d'un profil | Distinguer configuration demandée, budget effectif et observation appliquée. Un plan accepté ou calculé n'est pas une preuve d'application. |
| runtime / 93 | Reconfiguration contrôlée des ressources ; Réduction de workers occupés ; Plusieurs schedulers | Fermer les nouvelles admissions et drainer/restituer sous contrat ; conserver baux, fencing et déduplication en présence de plusieurs schedulers. |
| runtime / 107 | Budgets compatibles avec les garanties du profil ; Ressources insuffisantes pour une garantie | Refus fermé ou état sûr déclaré si une garantie obligatoire ne peut être tenue ; aucun privilège ou délai étendu sous charge. |
| runtime / 116 | Supervision et qualification des profils de ressources ; Profil sans recette de ressources ; Redémarrage supervisé | Les rôles restent sous lifecycle déclaré et revalident leurs préconditions après redémarrage. Les mesures du profil cible et de l'artefact restent à qualifier ; compilation et tests locaux ne prouvent pas une performance de distribution. |
| runtime / 205 | Topologies locales et distantes PA PZT ; Hôte local avec tous les composants ; Hôte distant sans backend local ; Hôte distant avec backend local | Préserver les frontières PBO/PA/PZT ; aucun transport, exécutant ou droit distant implicitement ajouté par C09. Les intégrations non sélectionnées ne sont pas annoncées disponibles. |

### Prérequis réalisés et limites de réutilisation

C04, C05, C06 et C07 sont archivés. Leur présence seule ne suffit pas : leurs tâches, rapports et contrats publics sont recoupés avant intégration. C06 est réalisé : ses tasks.md, design.md, requirements.md et STATISTIQUES.md décrivent les façades et l'idempotence effectivement éprouvées ; son proposal.md historique et certains champs intermédiaires de checkpoint ne constituent pas son état final. C06 conserve des doubles C09/C10 dans ses recettes : ils ne prouvent aucun worker ou scheduler général.

Les preuves historiques C06 indiquent 166 tests unitaires, 192 cas PostgreSQL sur neuf recettes et 33 compilations. Elles ne sont pas des tests exécutés par ce RUN C09. C05 impose la participation à la transaction propriétaire et la minimisation d'audit ; C04 impose le contrôle courant ; C07 conserve sa readiness intermédiaire et n'apporte pas un binaire PBO qualifié.

Les clauses B08/B09/B10/B11 propres au runtime Bulk restent conditionnelles à sa sélection. C09 ne les active pas globalement, ne modifie pas leurs profils préparatoires et ne généralise pas leur bail au scheduler. Les garanties génériques de jobs, d'événements et de runtime sont éprouvées par leurs propres propriétaires, sans import de tables privées Bulk.
