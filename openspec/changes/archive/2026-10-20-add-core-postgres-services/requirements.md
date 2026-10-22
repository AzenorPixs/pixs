# Exigences de réalisation — C02

## Portée et lecture de la matrice

Cette matrice complète le relevé documentaire le 19 octobre 2026. Elle référence le canon sans le recopier ni le modifier ; le profil C00 adopté reste applicable. Chaque scénario nommé renvoie au bloc de son exigence source, avec toutes ses clauses. Les identifiants C02-R et C02-T sont des repères de traçabilité de ce dossier, pas de nouvelles exigences normatives.

Les tâches désignent `tasks.md` ; V01 à V12 désignent la recette future de `design.md`. Les relations dans les deux sens sont explicites : objectif et données dans le modèle logique → exigence et scénarios ci-dessous → tâches → vérifications et responsable. Les statuts P du relevé initial étaient historiques ; aucun résultat fonctionnel actuel n’est attribué aux lignes consolidées.

La matrice principale couvre toutes les exigences de core, migrations et scope-context. La matrice transverse sélectionne les clauses nécessaires aux contrats, à la sécurité et à l’intégration de C02 ; elle n’impose pas à C02 l’implémentation complète de ces capacités. Les contrôles applicatifs suivent l’exception Super Admin canonique dans son seul périmètre, sans modifier les profils structurels.

## Matrice principale

| Repère | Source canonique et exigence | Scénarios sources | Tâches | Vérifications | Responsabilité / applicabilité |
|---|---|---|---|---|---|
| C02-R01 | [core / 8 — Module obligatoire au-dessus du noyau](../../../specs/core/spec.md#L8) | Composition sans core refusée | 1.1, 2.1, 3.2 | V06 | C02 ; composition commune |
| C02-R02 | [core / 17 — Primitives minimales communes](../../../specs/core/spec.md#L17) | Primitive consommée par contrat | 2.1, 2.3, 3.2 | V04, V06 | C02 ; lecture PostgreSQL de référence |
| C02-R03 | [core / 31 — Aucun fournisseur concret imposé](../../../specs/core/spec.md#L31) | Substitution de fournisseur | 1.1, 2.1, 3.2 | V06 | C02 ; aucun provider optionnel imposé |
| C02-R04 | [core / 40 — Profil minimal des utilisateurs et identités numériques v1](../../../specs/core/spec.md#L40) | Identité minimale valide ; Identifiant ou vocabulaire invalide | 2.1, 2.2, 2.4, 3.1 | V01 | C02 ; structures et persistance distinctes |
| C02-R05 | [core / 59 — Liaison utilisateur identité explicite et unique](../../../specs/core/spec.md#L59) | Entités indépendantes et liaison explicite ; Cardinalité violée ou référence absente | 2.1, 2.2, 2.4 | V01, V02 | C02 |
| C02-R06 | [core / 79 — Représentation minimale des comptes de service](../../../specs/core/spec.md#L79) | Compte de service sans utilisateur | 2.1, 2.2, 2.4 | V01, V02 | C02 ; aucun droit par le type SERVICE |
| C02-R07 | [core / 91 — Frontière des validateurs du profil identité](../../../specs/core/spec.md#L91) | Validation structurelle sans effet applicatif | 1.1, 2.1, 3.1 | V01 | C02 ; régression des validateurs purs |
| C02-R08 | [core / 102 — Autorités et limites du profil identité structurel](../../../specs/core/spec.md#L102) | Identité structurelle sans assurance implicite | 2.2, 2.3, 3.2 | V01, V07 | C02 ; intégration C04/C05 |
| C02-R09 | [migrations / 8 — Contrat de migration](../../../specs/migrations/spec.md#L8) | Migration sans version cible | 1.2, 2.2, 2.4 | V08 | C02 ; plan consommé par C08/C16 |
| C02-R10 | [migrations / 17 — Planification et ordre déterministes](../../../specs/migrations/spec.md#L17) | Deux migrations concurrentes | 2.2, 2.4 | V09 | C02 ; exclusion des exécuteurs |
| C02-R11 | [migrations / 26 — Compatibilité pendant l'application](../../../specs/migrations/spec.md#L26) | Coexistence pendant migration | 2.2, 2.4 | V10 | C02/C16 ; origines supportées déclarées |
| C02-R12 | [migrations / 35 — Reprise idempotente](../../../specs/migrations/spec.md#L35) | Interruption puis reprise | 2.2, 2.4 | V09 | C02 ; avancement persistant |
| C02-R13 | [migrations / 44 — Contraction contrôlée](../../../specs/migrations/spec.md#L44) | Contraction prématurée | 2.2, 2.4 | V10 | C02/C16 ; contraction si proposée |
| C02-R14 | [scope-context / 8 — Périmètre explicite du Super Admin](../../../specs/scope-context/spec.md#L8) | Accord tenant sans changement de propriété | 1.2, 2.1, 2.4 | V05 | C02 stockage ; C04 décision d’accord |
| C02-R15 | [scope-context / 18 — Tenant racine et parenté unique](../../../specs/scope-context/spec.md#L18) | Cycle de scopes refusé | 2.1, 2.2, 2.4 | V03 | C02 ; graphe générique |
| C02-R16 | [scope-context / 29 — Propriété canonique unique](../../../specs/scope-context/spec.md#L29) | Scope sans tenant cohérent refusé | 2.1, 2.2, 2.4 | V03 | C02 ; ressources métier de leurs propriétaires |
| C02-R17 | [scope-context / 40 — Contexte immuable propagé avant autorisation](../../../specs/scope-context/spec.md#L40) | Contexte TENANT sans tenant refusé ; Contexte PLATFORM avec identifiants refusé ; Scope orphelin refusé | 2.1, 2.3, 2.4 | V03, V04 | C02 ; structure et intégration distinctes |
| C02-R18 | [scope-context / 59 — Propagation et frontière d'autorisation du ScopeContext](../../../specs/scope-context/spec.md#L59) | Élargissement implicite refusé ; Contexte PLATFORM sans identifiants accepté sans octroyer permission ; Accès plateforme sans permission refusé et audité | 2.3, 2.4, 3.2 | V04 | C02/C04 ; exposition C06 |

## Matrice transverse et interfaces

| Repère | Source canonique et exigence | Scénarios sources | Tâches | Vérifications | Responsabilité / applicabilité |
|---|---|---|---|---|---|
| C02-T01 | [services / 8 — Enregistrement contractuel des services](../../../specs/services/spec.md#L8) | Service privé non exposé | 2.1, 2.3 | V06 | C02 |
| C02-T02 | [services / 17 — Résolution déterministe du fournisseur](../../../specs/services/spec.md#L17) | Ambiguïté refusée | 2.1, 2.3 | V06 | C02 ; résolution commune |
| C02-T03 | [services / 28 — Traçabilité et sécurité des appels](../../../specs/services/spec.md#L28) | Contexte non vérifiable | 2.3, 2.4 | V04, V07 | C02/C04/C05 |
| C02-T04 | [contracts / 8 — Catégories de contrats non interchangeables](../../../specs/contracts/spec.md#L8) | Événement au lieu d'une commande refusé | 2.1, 2.3 | V06, V07 | C02 ; C06/C09 selon catégorie |
| C02-T05 | [contracts / 17 — Versionnement SemVer indépendant](../../../specs/contracts/spec.md#L17) | Champ obligatoire ajouté | 1.2, 2.1 | V06 | C02 ; version indépendante |
| C02-T06 | [contracts / 26 — Dépréciation et retrait encadrés](../../../specs/contracts/spec.md#L26) | Suppression anticipée bloquée | 1.1, 2.1, 3.2 | V01, V06 | C02 ; retrait seulement si proposé |
| C02-T07 | [component-model / 22 — Manifest déclaratif unique](../../../specs/component-model/spec.md#L22) | Secret dans le manifest rejeté | 2.1, 2.3 | V06, V12 | C02 ; manifest Core |
| C02-T08 | [component-model / 63 — Manifest schéma 1 — capacités et contrats versionnés](../../../specs/component-model/spec.md#L63) | Descripteur de capacité du schéma 1 | 2.1, 2.3 | V06 | C02 |
| C02-T09 | [component-model / 78 — Manifest schéma 1 — propriétaire et contrats exacts](../../../specs/component-model/spec.md#L78) | Propriétaire dérivé du composant | 2.1, 2.3 | V06 | C02 |
| C02-T10 | [authorization / 8 — Portée du contrôle total du Super Admin](../../../specs/authorization/spec.md#L8) | Tenant non accordé au Super Admin ; Tenant accordé malgré un refus ACL | 1.2, 2.1, 2.4 | V05 | C02 stockage ; C04 contrôle |
| C02-T11 | [authorization / 43 — Priorité transversale de l'exception Super Admin](../../../specs/authorization/spec.md#L43) | Compte ordinaire sans exception ; Contrat structurel sans privilège | 2.3, 2.4, 3.2 | V04, V05, V07, V11 | C04 ; profils C02 préservés |
| C02-T12 | [authorization / 57 — Modèle Subject Resource Action Context](../../../specs/authorization/spec.md#L57) | Propriété sans politique refusée ; Sujet technique avant identité applicative | 2.3, 2.4 | V04 | C02/C04 ; aucune autorité déduite |
| C02-T13 | [authorization / 72 — Priorité DENY puis ALLOW puis refus](../../../specs/authorization/spec.md#L72) | Conflit DENY contre ALLOW | 2.3, 2.4 | V04, V05 | C04 ; contexte fourni par C02 |
| C02-T14 | [authorization / 83 — Évaluation applicative avant exposition](../../../specs/authorization/spec.md#L83) | Liste filtrée à la source | 2.3, 2.4 | V04 | C02 lecture ; C04 filtre ; C06 façade |
| C02-T15 | [authorization / 92 — Autorisation technique C01 bornée sans extension métier](../../../specs/authorization/spec.md#L92) | Action métier hors bootstrap | 1.2, 2.3 | V04, V05 | C01 distinct ; aucune mutation métier C02 |
| C02-T16 | [authorization / 101 — Limites de l’autorité technique d’amorçage](../../../specs/authorization/spec.md#L101) | Action métier hors bootstrap | 1.2, 2.3 | V04, V05 | C01 distinct ; aucun droit par UID 0 |
| C02-T17 | [authorization-engine / 8 — Exception Super Admin distincte des profils préparatoires](../../../specs/authorization-engine/spec.md#L8) | Profils préparatoires sans privilège ajouté | 1.1, 2.1, 3.1 | V01, V05 | C04 ; profils préparatoires inchangés |
| C02-T18 | [authorization-engine / 17 — Politiques déclaratives versionnées](../../../specs/authorization-engine/spec.md#L17) | Politique à code rejetée | 1.2, 2.1 | V06 | C02 stockage ; C04 schéma/validation |
| C02-T19 | [authorization-engine / 26 — Décisions et filtrage tracés](../../../specs/authorization-engine/spec.md#L26) | Décision périmée non réutilisée | 2.1, 2.3, 2.4 | V04, V07 | C02 faits courants ; C04 invalidation |
| C02-T20 | [authorization-engine / 37 — Groupes bornés et délégation auditée](../../../specs/authorization-engine/spec.md#L37) | Moteur indisponible | 1.2, 2.1, 2.4 | V02, V04 | C04 ; imbrication/délégation si sélectionnées |
| C02-T21 | [authorization-engine / 91 — Obligations honorées par le PEP du profil PDP minimal fermé v1](../../../specs/authorization-engine/spec.md#L91) | ALLOW minimal avec obligation honorée | 2.3, 2.4 | V07 | C04/C05 ; acquittement mémoire insuffisant |
| C02-T22 | [authorization-engine / 235 — Fraîcheur et invalidation de source-filter-plan-v1](../../../specs/authorization-engine/spec.md#L235) | Plan distinct d'une autorisation courante | 2.1, 2.3, 2.4 | V04, V07 | C04 ; versions/faits C02 |
| C02-T23 | [interactions / 18 — Commandes validées et autorisées](../../../specs/interactions/spec.md#L18) | Mutation sans autorisation refusée | 2.3, 2.4 | V04, V07 | C02/C04 ; commande propriétaire |
| C02-T24 | [interactions / 27 — Requêtes sans mutation implicite](../../../specs/interactions/spec.md#L27) | Lecture filtrée à la source | 2.3, 2.4 | V04 | C02/C04 ; pagination C06 |
| C02-T25 | [interactions / 36 — Idempotence et traçabilité des commandes](../../../specs/interactions/spec.md#L36) | Rejou divergent | 2.3, 2.4 | V07 | C02 transaction ; C06 idempotence |
| C02-T26 | [events / 17 — Publication après validation transactionnelle](../../../specs/events/spec.md#L17) | Transaction échouée sans événement | 2.3, 2.4 | V07 | C02 effet ; C09 publication |
| C02-T27 | [audit / 8 — Audit dérogeable du Super Admin](../../../specs/audit/spec.md#L8) | Opération Super Admin sans audit persistant ; Audit ordinaire toujours obligatoire | 2.3, 2.4 | V05, V07 | C04 dérogation ; C05 preuve |
| C02-T28 | [audit / 41 — Contenu minimal d'un événement d'audit](../../../specs/audit/spec.md#L41) | Refus d'autorisation tracé | 2.3, 2.4 | V07, V12 | C02 métadonnées ; C05 stockage |
| C02-T29 | [audit / 50 — Périmètre obligatoire d'audit](../../../specs/audit/spec.md#L50) | Opération destructive sans audit | 2.3, 2.4 | V07 | C05 ; aucun audit fabriqué |
| C02-T30 | [audit / 68 — Minimisation et non-duplication des données](../../../specs/audit/spec.md#L68) | Payload sensible détecté | 2.3, 3.2 | V12 | C02/C05 ; minimisation |
| C02-T31 | [data-governance / 18 — Profil de gouvernance versionné par composant](../../../specs/data-governance/spec.md#L18) | Flux sortant sans consommateur refusé | 1.2, 2.1, 3.2 | V11 | C02 données ; C10 profil versionné |
| C02-T32 | [data-governance / 27 — Classification restrictive par défaut](../../../specs/data-governance/spec.md#L27) | Export non classifié refusé | 2.1, 2.3, 3.2 | V11, V12 | C02 non-exposition ; C10 politique |
| C02-T33 | [data-lifecycle / 18 — Dimensions et états distincts](../../../specs/data-lifecycle/spec.md#L18) | Suppression logique tracée ; Vocabulaire commun de rétention fermé | 1.2, 2.1, 2.2 | V01, V11 | C02 schéma ; C10 transitions |
| C02-T34 | [data-lifecycle / 43 — Purge autorisée, auditée et idempotente](../../../specs/data-lifecycle/spec.md#L43) | Purge prématurée refusée | 2.2, 2.4 | V11 | C02 protection ; C10/C09 purge |
| C02-T35 | [data-lifecycle / 52 — Tombstones contre la résurrection](../../../specs/data-lifecycle/spec.md#L52) | Restauration sans résurrection | 2.2, 2.4 | V11 | C02 références ; C10/C16 restauration |
| C02-T36 | [security / 26 — Échec fermé sans mode permissif](../../../specs/security/spec.md#L26) | Contexte non vérifiable refusé | 2.3, 2.4 | V04, V07 | C02/C04/C05 ; dérogation canonique seule |
| C02-T37 | [security / 37 — Diagnostics sans exposition sensible](../../../specs/security/spec.md#L37) | Secret hors journaux | 2.3, 3.1, 3.2 | V12 | C02 ; diagnostics C06 sans fuite |
| C02-T38 | [initial-administration / 11 — Compte Super Admin unique de paramétrage et de secours](../../../specs/initial-administration/spec.md#L11) | Compte fonctionnel non nominatif ; Second compte et transfert refusés | 1.2, 2.1, 2.4 | V05 | C02 stockage ; C03/C04/C08 règles du compte |
| C02-T39 | [reference-composition / 10 — Capacités obligatoires du P0](../../../specs/reference-composition/spec.md#L10) | Capacité P0 absente | 1.1, 3.2, 3.3 | V12 | C07/C17 ; C02 seul ne prouve pas P0 |
| C02-T40 | [reference-composition / 62 — Parcours installable et utilisable du profil initial](../../../specs/reference-composition/spec.md#L62) | Démonstration mémoire seule | 2.3, 3.2, 3.3 | V07, V12 | Intégration C03–C10 ; recette C17 |
| C02-T41 | [reference-composition / 80 — Preuve de la composition effectivement distribuée](../../../specs/reference-composition/spec.md#L80) | Sources et paquet divergents | 3.2, 3.3, 3.4 | V12 | C17 sur paquet C18 ; apport de preuves C02 |
| C02-T42 | [reference-composition / 89 — Choix C01 systemd et exception d’amorçage du profil Debian local](../../../specs/reference-composition/spec.md#L89) | Hôte intermédiaire conservé non prêt ; Source locale hors phase autorisée | 1.2, 2.3, 3.2 | V07, V12 | C01 journal borné ; reprise C05/C08 |
| C02-T43 | [reference-composition / 103 — Qualification et source de vérité après amorçage](../../../specs/reference-composition/spec.md#L103) | Hôte intermédiaire conservé non prêt ; Source locale hors phase autorisée | 1.2, 2.3, 3.2 | V07, V12 | C05/C08 ; aucune autorité métier locale parallèle |
| C02-T44 | [directory-projections / 21 — Autorité PostgreSQL des primitives Core](../../../specs/directory-projections/spec.md#L21) | Mutation Core demandée | 2.2, 2.3 | V04, V07 | C02 source ; O08 projection seulement si sélectionnée |
| C02-T45 | [directory-projections / 98 — Consultation avec préférence LDAP et repli PostgreSQL](../../../specs/directory-projections/spec.md#L98) | LDAP indisponible | 2.3, 3.2 | V04, V06 | C02 fournit lecture PG ; O09 si LDAP sélectionné |
| C02-T46 | [directory-projections / 126 — Autorisation et confidentialité préservées à la consultation](../../../specs/directory-projections/spec.md#L126) | Consultation hors tenant refusée | 2.3, 3.2 | V04, V12 | C02/C04 ; O09 pour branche LDAP sélectionnée |

| C02-T47 | [initial-administration / 105 — Création conditionnelle du Super Admin](../../../specs/initial-administration/spec.md#L105) | Mots de passe différents ; Compte fonctionnel créé explicitement | 1.2, 2.1, 2.3, 2.4 | V05, V07 | C08 R01 B01/B03/B04 ; C02 gardes/écritures |
| C02-T48 | [initial-administration / 126 — Réutilisation du Super Admin d'une base conservée](../../../specs/initial-administration/spec.md#L126) | Base conforme conservée | 1.2, 2.1, 2.4 | V05, V07 | C08 R01 B05/B06/B07 ; aucune seconde création |
| C02-T49 | [initial-administration / 218 — Opérateur technique INSTALLER avant base et sessions](../../../specs/initial-administration/spec.md#L218) | Opérateur non vérifiable ; Root OS sans privilège applicatif implicite | 1.2, 2.3, 2.4 | V04, V05, V07 | C01 distinct ; C08 B02/B08/B09 sans transfert de droit |
| C02-T50 | [initial-administration / 232 — Limites et refus de la phase technique INSTALLER](../../../specs/initial-administration/spec.md#L232) | Opérateur non vérifiable ; Root OS sans privilège applicatif implicite | 1.2, 2.3, 2.4 | V05, V07 | C01 interdit de créer l’identité/compte ; C08 R01 séparé |
| C02-T51 | [installation-provisioning / 9 — Provisionnement du compte fonctionnel de secours](../../../specs/installation-provisioning/spec.md#L9) | Provisionnement sans compte nominatif ni MFA | 1.2, 2.1, 2.4 | V05 | C08 B03/B05 ; C02 stockage, C03/C04 identité et exception |
| C02-T52 | [installation-provisioning / 42 — Opérateur initial explicite et sans privilège implicite](../../../specs/installation-provisioning/spec.md#L42) | Identité opérateur absente | 1.2, 2.3, 2.4 | V04, V05 | C08 B01/B02 ; preuve opérateur distincte du compte cible |
| C02-T53 | [installation-provisioning / 55 — Création tenant-scoped contrôlée](../../../specs/installation-provisioning/spec.md#L55) | Rejou du provisionnement du premier tenant | 2.1, 2.2, 2.3, 2.4 | V03, V05, V07 | C08 B03/B06/B09 ; premier tenant explicitement autorisé |
| C02-T54 | [installation-provisioning / 68 — Reprise contrôlée et auditée](../../../specs/installation-provisioning/spec.md#L68) | Interruption avant mise en service | 2.2, 2.3, 2.4 | V05, V07 | C08 B06/B07/B10 ; reprise après effet/commit/marqueur |

## Applicabilité et preuves attendues

- Les quatre exigences Core ajoutées au relevé initial couvrent six scénarios : identifiants/vocabulaires, liaisons explicites, compte SERVICE sans User et frontière pure. Elles complètent la traçabilité sans modifier les règles existantes.
- Les groupes utilisateur–groupe et les appartenances identité–tenant sont explicités dans le modèle logique, V02 et les tâches 2.1/2.2/2.4. Leur réalisation applique core, scope-context, les contrôles d’autorisation et les contrats existants ; elle ne généralise pas les représentations pures en permissions runtime.
- Les migrations traitent installation vierge, origine/cible, concurrence, reprise, coexistence et contraction selon V08/V09/V10. Une absence d’origine distribuée supportée ou de contraction proposée justifie seulement les scénarios conditionnels concernés, avec motif et source.
- Les exigences de stockage et de protection sont propres à C02 ; les garanties PEP/audit/idempotence/livraison/gouvernance exigent des preuves intégrées avec C04/C05/C06/C09/C10. Une preuve locale n’autorise pas l’activation d’un service sans les preuves obligatoires.
- La référence à directory-projections conserve l’autorité PostgreSQL et le contrat de lecture. LDAP, son provider et ses garanties de convergence ne sont pas sélectionnés par C02 ; O08/O09 restent propriétaires de ces branches futures.
- Le stockage du compte fonctionnel et de ses accords est distinct de sa création, de son authentification et de l’évaluation de l’exception. C08, C03 et C04 conservent ces opérations ; une fixture ou un rôle administrateur ne fabrique aucun privilège.
- Les politiques et invariants de données sont préparés avec C10 dès le schéma. Une donnée non classifiée reste non exposée. Une purge/restauration non livrée n’est pas déclarée conforme du seul fait d’une colonne ou d’un tombstone structurel.
- Les tâches 3.1 à 3.4 consolident les commandes, résultats, portées et décisions de chaque ligne ; une preuve partagée possède une seule identité et peut être référencée par plusieurs lignes, sans multiplication de tests ni de statistiques.

- R01 relie la création/réutilisation du compte et les limites C01 au contrat d’autorité C08/C02. Les cas B01–B10 de C08 enrichissent V05/V07 ; ils n’introduisent ni session préalable obligatoire du compte futur, ni identité déduite d’UID 0, ni nouveau provider ou scénario canonique.

## Empreintes SHA-256 du canon

Les empreintes ci-dessous décrivent les sources relues pour ce complément. Toute dérive exige de relire les seuls blocs affectés avant réalisation ; ces empreintes ne sont ni des résultats de test ni des preuves d’adoption supplémentaire.

- `openspec/specs/core/spec.md` : `d0eb213fa2fbb3ccca042133d910166b35f4a3e8e60178ad02b12420034bada3`.
- `openspec/specs/migrations/spec.md` : `9b3ced385afbeaa7414a1d58752078482e57efa242064e21e7fb4b6fde451efe`.
- `openspec/specs/scope-context/spec.md` : `4a8df881b08f5b4e3c302b9966bff199276350cab9a236a9f8ff2330d28d1270`.
- `openspec/specs/services/spec.md` : `e754ac950e612d335017122e23e55d75d3fb214f927fabcb2d48da8722013c37`.
- `openspec/specs/contracts/spec.md` : `ad08fabc8ff78db8678ec873c9c50235b57fdf2554111d48adf57f274e4a3897`.
- `openspec/specs/component-model/spec.md` : `6972572f92f9f020b89f5cf8e81ead65005fa858695a838089dd27fd4200b3ae`.
- `openspec/specs/authorization/spec.md` : `427c3bc5776a640d2c944c7ccc21baebd85f0c92f258e3313d87b52fcdd779a1`.
- `openspec/specs/authorization-engine/spec.md` : `bd9de765f72d4700da314f81dbce9d3d0ee532f3bcc5be319f005ffbfd18b20b`.
- `openspec/specs/interactions/spec.md` : `9a2e9186b51c70c17781e2395da3e42f83dd2cc90da36bab624d90397d4ab9a0`.
- `openspec/specs/events/spec.md` : `31af2e0a1ae55bc575b9f0edb906e73d0b707e8c68458d680155251ea587bf14`.
- `openspec/specs/audit/spec.md` : `074ea1a323e8cd6b4f4ad83fa796b75277268efbc0f791dbb6edfde1681cd47f`.
- `openspec/specs/data-governance/spec.md` : `85c5176f49270a9eb45a51329fc200f8d1cb293bfa6bc93e62eb7fe88999ddfe`.
- `openspec/specs/data-lifecycle/spec.md` : `a3498cc4d3622d569fc9e3f8251a5c5324a9b3d1c612fe014618146297083426`.
- `openspec/specs/security/spec.md` : `c033c6fa6a6fc43d6e7e3295cd7dc7f554bbcbe0c12cb9baf0431acd6f7a685f`.
- `openspec/specs/initial-administration/spec.md` : `a875dfd4e48cc2920ea38242b02c46aab386a7a77b645165d009d9fa47f4cc4a`.
- `openspec/specs/reference-composition/spec.md` : `5c833175c3ed05b6951b4193aba6eaaa0fa3990b0e61c2ef51f41e7cc7fa92d7`.
- `openspec/specs/directory-projections/spec.md` : `d0612178893ed10acb13d3297aaf2f488ca96b7e16210beda23056fe3df0aaaa`.

- `openspec/specs/installation-provisioning/spec.md` : `2d33df47ef9ad0c073c4e0d7677c98e3cd96cb8e3b6866894c6d3cb7d305e7b4`.

## Comptage et état des preuves

La matrice principale contient 18 exigences et 24 références de scénarios ; la matrice transverse contient 54 exigences et 65 références de scénarios, soit 72 exigences et 89 références au total. Le complément R01 ajoute huit rattachements à des exigences existantes et onze références de scénarios ; il ne modifie pas le canon ni le nombre de vérifications V01–V12. Les scénarios sont comptés dans leur exigence propriétaire, sans attribuer ces nombres à des tests exécutés.

Le paragraphe de préparation du 19 octobre décrivait dix tâches non cochées et aucune recette exécutée. La réalisation locale du 20 octobre est désormais documentée dans [VALIDATION.md](VALIDATION.md), sans ajout d’exigence, de scénario canonique ou de delta. D01–D04 et R01 restent inchangés. Les preuves locales, les conditions d’activation des propriétaires et les non-applicabilités conditionnelles sont distinguées ; les statistiques et le gate restent des obligations de clôture après archivage.
