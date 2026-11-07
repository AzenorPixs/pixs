# Matrice de conservation reconstruite

Cette matrice corrige la traçabilité dans le présent lot ; l'archive reste intacte.

H0 : `1d96ece501606330b45c6819054ba6e581b824bd` ; H1 : `b83f9de8827f94fe930972a6abf6663fca7a1c29`. H0 est le parent direct de H1.
Les repères B sont des repères d'audit, sans changement d'identifiant normatif.
Les preuves complètes, chemins, lignes et empreintes brutes sont dans [evidence.json](evidence.json).

## Réconciliation des totaux

| Origine | Exigences | Scénarios |
| --- | ---: | ---: |
| audit-ancien | 5 | 5 |
| audit-bootstrap | 1 | 1 |
| initial-administration-bootstrap | 7 | 9 |
| initial-application-bootstrap-bootstrap | 4 | 4 |
| operations-ancien | 5 | 5 |
| operations-bootstrap | 1 | 1 |
| stable-72 | 277 | 280 |
| **Total** | **300** | **305** |

Les dix exigences et dix scénarios omis sont les 5/5 anciens d'audit et les 5/5 anciens d'operations.
Les capacités sont comptées par chemins distincts : 76, sans additionner deux fois audit et operations.

## Convention de lecture

Source H0 = canon avant ; source D = delta du bootstrap archivé dans H1.
Pour chaque capacité, les lignes source/cible renvoient aux chemins indiqués ci-dessous.
Les dépendances listées sont les références de capacités explicites du bloc et celles déclarées pour le bootstrap ; absence de référence ne vaut pas indépendance.
Deux exigences portent un repliement de prose documenté, sans identité brute prétendue.
La colonne courante décrit la présence d'un repère, pas l'identité de tout son comportement ni un accord humain.

## accessibility

Canon H0/H1/courant : `openspec/specs/accessibility/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0001 | R : Niveau cible WCAG 2.2 AA | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0002 | S : Contribution non conforme — sous « Niveau cible WCAG 2.2 AA » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0003 | R : Fonctionnement clavier et technologies d'assistance | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0004 | S : Parcours clavier complet — sous « Fonctionnement clavier et technologies d'assistance » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0005 | R : Sémantique native préservée | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0006 | S : Rôle ARIA redondant — sous « Sémantique native préservée » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |
| B0007 | R : Validation outillée et manuelle combinées | H0 L35 | L35 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L35 |
| B0008 | S : Défaut non détectable automatiquement — sous « Validation outillée et manuelle combinées » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L39 |

## ai-agents

Canon H0/H1/courant : `openspec/specs/ai-agents/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0009 | R : Fournisseurs et capacités IA déclarés | H0 L11 | L11 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L11 |
| B0010 | S : Fournisseur absent — sous « Fournisseurs et capacités IA déclarés » | H0 L18 | L18 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L18 |
| B0011 | S : Fournisseur présent sans activation — sous « Fournisseurs et capacités IA déclarés » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L23 |
| B0012 | R : Données et récupération gouvernées | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L28 |
| B0013 | S : Récupération hors périmètre — sous « Données et récupération gouvernées » | H0 L36 | L36 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L36 |
| B0014 | R : Outils explicitement autorisés et médiés | H0 L41 | L41 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L41 |
| B0015 | S : Agent proposant une mutation — sous « Outils explicitement autorisés et médiés » | H0 L48 | L48 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L48 |
| B0016 | R : Prompts, évaluations, budgets et audit | H0 L53 | L53 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L53 |
| B0017 | S : Budget épuisé — sous « Prompts, évaluations, budgets et audit » | H0 L60 | L60 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L60 |

## api

Canon H0/H1/courant : `openspec/specs/api/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0018 | R : Contrats OpenAPI versionnés par majeure | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L18 |
| B0019 | S : Rupture sans nouvelle majeure bloquée — sous « Contrats OpenAPI versionnés par majeure » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L22 |
| B0020 | R : Enveloppes stables et erreurs typées | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L27 |
| B0021 | S : Rejou identique restitué — sous « Enveloppes stables et erreurs typées » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L33 |
| B0022 | R : Périmètre canonique et autorisation à la frontière | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L38 |
| B0023 | S : Tenant d'en-tête non canonique rejeté — sous « Périmètre canonique et autorisation à la frontière » | H0 L34 | L34 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L44 |

## architecture-decisions

Canon H0/H1/courant : `openspec/specs/architecture-decisions/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0024 | R : Décision contextualisée | H0 L10 | L10 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L10 |
| B0025 | S : Décision de provider documentée — sous « Décision contextualisée » | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0026 | R : OpenSpec reste normatif | H0 L22 | L22 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L22 |
| B0027 | S : Décision contradictoire — sous « OpenSpec reste normatif » | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L28 |
| B0028 | R : États traçables | H0 L33 | L33 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L33 |
| B0029 | S : Décision remplacée — sous « États traçables » | H0 L38 | L38 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L38 |

## artifact-publication

Canon H0/H1/courant : `openspec/specs/artifact-publication/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0030 | R : Canaux comme contextes de confiance distincts | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0031 | S : Artefact du mauvais canal — sous « Canaux comme contextes de confiance distincts » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0032 | R : Immuabilité et corrélation des corrections | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0033 | S : Écrasement d'un artefact publié — sous « Immuabilité et corrélation des corrections » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0034 | R : Identité vérifiable avant installation | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0035 | S : Emprunte discordante — sous « Identité vérifiable avant installation » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |
| B0036 | R : Signature, provenance et inventaire bloquants | H0 L35 | L35 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L35 |
| B0037 | S : Signature révoquée — sous « Signature, provenance et inventaire bloquants » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L39 |
| B0038 | R : Autorités distinctes et gestion des clés | H0 L44 | L44 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L44 |
| B0039 | S : Dépôt de publication indisponible — sous « Autorités distinctes et gestion des clés » | H0 L48 | L48 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L48 |

## audit

Canon H0/H1/courant : `openspec/specs/audit/spec.md`.
D : `openspec/changes/archive/2026-09-16-specify-initial-application-bootstrap/specs/audit/spec.md`, dans H1.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0048 | R : Audit fonctionnel distinct des logs techniques | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |
| B0049 | S : Perte de télémétrie technique — sous « Audit fonctionnel distinct des logs techniques » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L36 |
| B0050 | R : Contenu minimal d'un événement d'audit | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L41 |
| B0051 | S : Refus d'autorisation tracé — sous « Contenu minimal d'un événement d'audit » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L45 |
| B0052 | R : Périmètre obligatoire d'audit | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L50 |
| B0053 | S : Opération destructive sans audit — sous « Périmètre obligatoire d'audit » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L54 |
| B0054 | R : Append-only et réécriture contrôlée | H0 L35 | L35 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L59 |
| B0055 | S : Obligation d'effacement — sous « Append-only et réécriture contrôlée » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L63 |
| B0056 | R : Minimisation et non-duplication des données | H0 L44 | L44 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L68 |
| B0057 | S : Payload sensible détecté — sous « Minimisation et non-duplication des données » | H0 L48 | L48 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L72 |
| B0058 | R : Audit exhaustif du panneau d'administration | D L3 | L53 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L77 |
| B0059 | S : Navigation non auditable — sous « Audit exhaustif du panneau d'administration » | D L13 | L63 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L81 |

## audit-integrity

Canon H0/H1/courant : `openspec/specs/audit-integrity/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0040 | R : Mécanisme d'intégrité explicitement déclaré | H0 L11 | L11 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L11 |
| B0041 | S : Audit standard sans mécanisme déclaré — sous « Mécanisme d'intégrité explicitement déclaré » | H0 L20 | L20 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L20 |
| B0042 | R : Preuves vérifiables et chaînage résilient | H0 L25 | L25 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L25 |
| B0043 | S : Événement modifié — sous « Preuves vérifiables et chaînage résilient » | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |
| B0044 | R : Exports et conservation vérifiables | H0 L37 | L37 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L37 |
| B0045 | S : Export soumis à vérification — sous « Exports et conservation vérifiables » | H0 L44 | L44 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L44 |
| B0046 | R : Confidentialité, rétention et droit d'effacement préservés | H0 L49 | L49 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L49 |
| B0047 | S : Effacement d'une donnée auditée — sous « Confidentialité, rétention et droit d'effacement préservés » | H0 L56 | L56 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L56 |

## authentication

Canon H0/H1/courant : `openspec/specs/authentication/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0060 | R : Fournisseurs déclarés et confiance explicite | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0061 | S : Émetteur non approuvé refusé — sous « Fournisseurs déclarés et confiance explicite » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0062 | R : Identifiant externe canonique et liaison explicite | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0063 | S : Courriel seul non rapproché — sous « Identifiant externe canonique et liaison explicite » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L23 |
| B0064 | R : Sessions bornées et révocation propagée | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L28 |
| B0065 | S : Révocation propagée — sous « Sessions bornées et révocation propagée » | H0 L34 | L34 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |

## authorization

Canon H0/H1/courant : `openspec/specs/authorization/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0072 | R : Modèle Subject Resource Action Context | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L57 |
| B0073 | S : Propriété sans politique refusée — sous « Modèle Subject Resource Action Context » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L61 |
| B0074 | R : Priorité DENY puis ALLOW puis refus | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L76 |
| B0075 | S : Conflit DENY contre ALLOW — sous « Priorité DENY puis ALLOW puis refus » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L80 |
| B0076 | R : Évaluation applicative avant exposition | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L85 |
| B0077 | S : Liste filtrée à la source — sous « Évaluation applicative avant exposition » | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L89 |

## authorization-engine

Canon H0/H1/courant : `openspec/specs/authorization-engine/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0066 | R : Politiques déclaratives versionnées | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0067 | S : Politique à code rejetée — sous « Politiques déclaratives versionnées » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0068 | R : Décisions et filtrage tracés | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0069 | S : Décision périmée non réutilisée — sous « Décisions et filtrage tracés » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |
| B0070 | R : Groupes bornés et délégation auditée | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L37 |
| B0071 | S : Moteur indisponible — sous « Groupes bornés et délégation auditée » | H0 L34 | L34 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L43 |

## backup-disaster-recovery

Canon H0/H1/courant : `openspec/specs/backup-disaster-recovery/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0078 | R : Stratégie déclarée par déploiement | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0079 | S : Procédure sans objectifs déclarés — sous « Stratégie déclarée par déploiement » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0080 | R : Périmètres de sauvegarde distincts | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0081 | S : Sauvegarde partielle — sous « Périmètres de sauvegarde distincts » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0082 | R : Restauration cohérente et réapplication des gouvernances | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0083 | S : Objet restauré après suppression validée — sous « Restauration cohérente et réapplication des gouvernances » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |
| B0084 | R : Tests de restauration isolés et preuves | H0 L35 | L35 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L35 |
| B0085 | S : Démarrage après restauration — sous « Tests de restauration isolés et preuves » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L39 |
| B0086 | R : Restauration destructive autorisée et auditée | H0 L44 | L44 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L44 |
| B0087 | S : Suppression implicite refusée — sous « Restauration destructive autorisée et auditée » | H0 L48 | L48 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L48 |

## bulk-operations

Canon H0/H1/courant : `openspec/specs/bulk-operations/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0088 | R : Contrat BulkOperation suivi par operation_id | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0089 | S : Suivi distinct des travaux — sous « Contrat BulkOperation suivi par operation_id » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0090 | R : Import via staging privé et commandes propriétaires | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0091 | S : Ligne en conflit rejetée — sous « Import via staging privé et commandes propriétaires » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0092 | R : Export filtré, gouverné et révocable | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0093 | S : Export hors périmètre refusé — sous « Export filtré, gouverné et révocable » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |

## business-rules

Canon H0/H1/courant : `openspec/specs/business-rules/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0094 | R : Règles métier séparées des contrôles de sécurité | H0 L10 | L10 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L10 |
| B0095 | S : Règle invoquée pour une action protégée — sous « Règles métier séparées des contrôles de sécurité » | H0 L16 | L16 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L16 |
| B0096 | R : Déclarations versionnées et déterministes | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0097 | S : Évaluation rejouée — sous « Déclarations versionnées et déterministes » | H0 L29 | L29 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L29 |
| B0098 | S : Expression exécutable proposée — sous « Déclarations versionnées et déterministes » | H0 L34 | L34 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L40 |
| B0099 | R : Effets appliqués par le propriétaire métier | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L47 |
| B0100 | S : Décision conduisant à une mutation — sous « Effets appliqués par le propriétaire métier » | H0 L46 | L46 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L54 |
| B0101 | R : Tests, explications et audit | H0 L51 | L51 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L61 |
| B0102 | S : Décision contestée — sous « Tests, explications et audit » | H0 L57 | L57 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L67 |

## capabilities

Canon H0/H1/courant : `openspec/specs/capabilities/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0103 | R : Descripteur de capacité résolu à la composition | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0104 | S : Résolution indépendante de l'ordre — sous « Descripteur de capacité résolu à la composition » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0105 | R : États de disponibilité distincts | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0106 | S : Capacité optionnelle indisponible isolée — sous « États de disponibilité distincts » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L23 |
| B0107 | R : Fanion ne remplace pas la résolution | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L28 |
| B0108 | S : Fanion sans fournisseur refusé — sous « Fanion ne remplace pas la résolution » | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |

## compatibility

Canon H0/H1/courant : `openspec/specs/compatibility/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0109 | R : Contraintes de version déclarées et vérifiées | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0110 | S : Contrainte insatisfaite à l'activation — sous « Contraintes de version déclarées et vérifiées » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0111 | R : Aucune compatibilité présumée | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0112 | S : Version supérieure non testée — sous « Aucune compatibilité présumée » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0113 | R : Matrice de compatibilité globale | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0114 | S : État bloqué déterministe — sous « Matrice de compatibilité globale » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |
| B0115 | R : Compatibilité déclarative distincte de la conformité comportementale | H0 L35 | L35 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L35 |
| B0116 | S : Déclaration sans conformité — sous « Compatibilité déclarative distincte de la conformité comportementale » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L39 |
| B0117 | R : Coexistence pendant les montées de version | H0 L44 | L44 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L44 |
| B0118 | S : Suppression prématurée — sous « Coexistence pendant les montées de version » | H0 L48 | L48 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L48 |

## component-model

Canon H0/H1/courant : `openspec/specs/component-model/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0119 | R : Types de composants unifiés | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0120 | S : Sous-module validé comme module — sous « Types de composants unifiés » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0121 | S : Facette frontend d'un sous-module — sous « Types de composants unifiés » | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0122 | R : Manifest déclaratif unique | H0 L22 | L22 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L22 |
| B0123 | S : Secret dans le manifest rejeté — sous « Manifest déclaratif unique » | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0124 | R : Schéma de manifest versionné et validable | H0 L31 | L31 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L31 |
| B0125 | S : Version de schéma inconnue — sous « Schéma de manifest versionné et validable » | H0 L38 | L38 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L38 |
| B0126 | R : Identifiants stables namespacés | H0 L43 | L43 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L43 |
| B0127 | S : Collision d'identifiants refusée — sous « Identifiants stables namespacés » | H0 L49 | L49 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L49 |
| B0128 | R : États de composition, installation et santé distincts | H0 L54 | L54 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L54 |
| B0129 | S : États non assimilés — sous « États de composition, installation et santé distincts » | H0 L58 | L58 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L58 |

## component-registry

Canon H0/H1/courant : `openspec/specs/component-registry/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0130 | R : Catalogue de composants et sources déclarées | H0 L11 | L11 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L11 |
| B0131 | S : Source locale sélectionnée — sous « Catalogue de composants et sources déclarées » | H0 L19 | L19 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L19 |
| B0132 | R : Installation vérifiée sans activation implicite | H0 L24 | L24 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L24 |
| B0133 | S : Composant téléchargé non sélectionné — sous « Installation vérifiée sans activation implicite » | H0 L31 | L31 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L31 |
| B0134 | R : Révocation et retrait contrôlés | H0 L36 | L36 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L36 |
| B0135 | S : Version révoquée au contrôle de composition — sous « Révocation et retrait contrôlés » | H0 L43 | L43 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L43 |
| B0136 | R : Recherche et résolution déterministes | H0 L48 | L48 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L48 |
| B0137 | S : Deux versions compatibles candidates — sous « Recherche et résolution déterministes » | H0 L54 | L54 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L54 |

## configuration

Canon H0/H1/courant : `openspec/specs/configuration/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0138 | R : Schémas typés validés avant activation | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0139 | S : Configuration invalide bloquée — sous « Schémas typés validés avant activation » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0140 | R : Priorité déterministe des sources | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0141 | S : Surcharge déterministe — sous « Priorité déterministe des sources » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L23 |
| B0142 | R : Secrets par référence hors artefacts | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L28 |
| B0143 | S : Secret embarqué refusé — sous « Secrets par référence hors artefacts » | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |

## contracts

Canon H0/H1/courant : `openspec/specs/contracts/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0144 | R : Catégories de contrats non interchangeables | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0145 | S : Événement au lieu d'une commande refusé — sous « Catégories de contrats non interchangeables » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0146 | R : Versionnement SemVer indépendant | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0147 | S : Champ obligatoire ajouté — sous « Versionnement SemVer indépendant » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0148 | R : Dépréciation et retrait encadrés | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0149 | S : Suppression anticipée bloquée — sous « Dépréciation et retrait encadrés » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |

## core

Canon H0/H1/courant : `openspec/specs/core/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0150 | R : Module obligatoire au-dessus du noyau | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0151 | S : Composition sans core refusée — sous « Module obligatoire au-dessus du noyau » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0152 | R : Primitives minimales communes | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0153 | S : Primitive consommée par contrat — sous « Primitives minimales communes » | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0154 | R : Aucun fournisseur concret imposé | H0 L31 | L31 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L31 |
| B0155 | S : Substitution de fournisseur — sous « Aucun fournisseur concret imposé » | H0 L35 | L35 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L35 |

## data-governance

Canon H0/H1/courant : `openspec/specs/data-governance/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0156 | R : Profil de gouvernance versionné par composant | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L18 |
| B0157 | S : Flux sortant sans consommateur refusé — sous « Profil de gouvernance versionné par composant » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L22 |
| B0158 | R : Classification restrictive par défaut | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L27 |
| B0159 | S : Export non classifié refusé — sous « Classification restrictive par défaut » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L33 |
| B0160 | R : Demandes relatives aux données tracées | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L38 |
| B0161 | S : Effacement propagé — sous « Demandes relatives aux données tracées » | H0 L34 | L34 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L44 |

## data-lifecycle

Canon H0/H1/courant : `openspec/specs/data-lifecycle/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0162 | R : Dimensions et états distincts | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L18 |
| B0163 | S : Suppression logique tracée — sous « Dimensions et états distincts » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L22 |
| B0164 | R : Purge autorisée, auditée et idempotente | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L43 |
| B0165 | S : Purge prématurée refusée — sous « Purge autorisée, auditée et idempotente » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L47 |
| B0166 | R : Tombstones contre la résurrection | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L52 |
| B0167 | S : Restauration sans résurrection — sous « Tombstones contre la résurrection » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L56 |

## deb-package

Canon H0/H1/courant : `openspec/specs/deb-package/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0168 | R : Paquet corrélé à la release | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L22 |
| B0169 | S : Version de paquet incohérente — sous « Paquet corrélé à la release » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0170 | R : Configuration et secrets hors paquet | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L36 |
| B0171 | S : Secret trouvé dans le paquet — sous « Configuration et secrets hors paquet » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L40 |
| B0172 | R : Services alignés sur le lifecycle Pixs | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L45 |
| B0173 | S : Redémarrage par le gestionnaire de services — sous « Services alignés sur le lifecycle Pixs » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L49 |
| B0174 | R : Mise à niveau du paquet sous validation | H0 L35 | L35 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L54 |
| B0175 | S : Mise à niveau interrompue — sous « Mise à niveau du paquet sous validation » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L58 |
| B0176 | R : Aucune installation de code distant implicite | H0 L44 | L44 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L63 |
| B0177 | S : Téléchargement proposé à l'installation — sous « Aucune installation de code distant implicite » | H0 L48 | L48 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L67 |

## dependencies

Canon H0/H1/courant : `openspec/specs/dependencies/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0178 | R : Dépendances déclarées typées | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0179 | S : Optionnelle absente tolérée — sous « Dépendances déclarées typées » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0180 | R : Cycles et incompatibilités refusés | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0181 | S : Cycle détecté — sous « Cycles et incompatibilités refusés » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L23 |
| B0182 | R : Ordre de chargement déterministe | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L28 |
| B0183 | S : Double composition identique — sous « Ordre de chargement déterministe » | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |
| B0184 | R : Graphe frontend récursif et façades publiques | H0 L37 | L37 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L37 |
| B0185 | S : Import privé d'un parent refusé — sous « Graphe frontend récursif et façades publiques » | H0 L41 | L41 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L41 |

## design-system

Canon H0/H1/courant : `openspec/specs/design-system/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0186 | R : Tokens sémantiques d'intention | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0187 | S : Valeur brute refusée — sous « Tokens sémantiques d'intention » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0188 | R : Primitives à API stable | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0189 | S : Variante non déclarée — sous « Primitives à API stable » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0190 | R : Cohérence Light et Dark par les tokens | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0191 | S : Primitive inspectée dans les deux modes — sous « Cohérence Light et Dark par les tokens » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |
| B0192 | R : Adapter de rendu sans contournement | H0 L35 | L35 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L35 |
| B0193 | S : Accès direct au moteur refusé — sous « Adapter de rendu sans contournement » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L39 |

## developer-experience

Canon H0/H1/courant : `openspec/specs/developer-experience/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0194 | R : Parcours local reproductible | H0 L10 | L10 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L10 |
| B0195 | S : Premier composant local — sous « Parcours local reproductible » | H0 L16 | L16 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L16 |
| B0196 | R : Génération sans activation implicite | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0197 | S : Scaffolding d'un provider — sous « Génération sans activation implicite » | H0 L27 | L27 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L27 |
| B0198 | R : Diagnostics sans fuite | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |
| B0199 | S : Manifest incomplet — sous « Diagnostics sans fuite » | H0 L38 | L38 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L38 |

## directory-projections

Canon H0/H1/courant : `openspec/specs/directory-projections/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0200 | R : Périmètre des ressources projetées | H0 L11 | L11 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L11 |
| B0201 | S : Ressource hors périmètre déclarée — sous « Périmètre des ressources projetées » | H0 L16 | L16 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L16 |
| B0202 | R : Autorité PostgreSQL des primitives Core | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0203 | S : Mutation Core demandée — sous « Autorité PostgreSQL des primitives Core » | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0204 | R : LDAP sans autorité ni écriture métier | H0 L31 | L31 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L31 |
| B0205 | S : Écriture LDAP refusée — sous « LDAP sans autorité ni écriture métier » | H0 L36 | L36 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L36 |
| B0206 | R : Fonctions de sécurité exclues de la projection | H0 L41 | L41 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L41 |
| B0207 | S : Fonction de sécurité déléguée à LDAP — sous « Fonctions de sécurité exclues de la projection » | H0 L46 | L46 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L46 |
| B0208 | R : Provider et mapping de projection déclarés | H0 L51 | L51 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L51 |
| B0209 | S : Mapping incomplet bloqué — sous « Provider et mapping de projection déclarés » | H0 L61 | L61 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L61 |
| B0210 | R : Projection sortante après mutation confirmée | H0 L66 | L66 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L66 |
| B0211 | S : Mutation confirmée éligible à la projection — sous « Projection sortante après mutation confirmée » | H0 L72 | L72 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L72 |
| B0212 | R : Convergence reprenable et idempotente | H0 L77 | L77 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L77 |
| B0213 | S : Reprise après indisponibilité LDAP — sous « Convergence reprenable et idempotente » | H0 L82 | L82 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L82 |
| B0214 | R : Retard et retrait de projection observables | H0 L87 | L87 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L87 |
| B0215 | S : Perte de visibilité autorisée — sous « Retard et retrait de projection observables » | H0 L93 | L93 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L93 |
| B0216 | R : Consultation avec préférence LDAP et repli PostgreSQL | H0 L98 | L98 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L98 |
| B0217 | S : LDAP indisponible — sous « Consultation avec préférence LDAP et repli PostgreSQL » | H0 L108 | L108 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L108 |
| B0218 | R : Fraîcheur après mutation et cohérence de lecture | H0 L113 | L113 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L113 |
| B0219 | S : Lecture après changement de groupe — sous « Fraîcheur après mutation et cohérence de lecture » | H0 L121 | L121 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L121 |
| B0220 | R : Autorisation et confidentialité préservées à la consultation | H0 L126 | L126 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L126 |
| B0221 | S : Consultation hors tenant refusée — sous « Autorisation et confidentialité préservées à la consultation » | H0 L135 | L135 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L135 |

## distributed-cache

Canon H0/H1/courant : `openspec/specs/distributed-cache/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0222 | R : Cache uniquement dérivé et reconstruisible | H0 L10 | L10 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L10 |
| B0223 | S : Perte complète du cache — sous « Cache uniquement dérivé et reconstruisible » | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0224 | R : Partitionnement et autorisation conservés | H0 L22 | L22 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L22 |
| B0225 | S : Changement de tenant — sous « Partitionnement et autorisation conservés » | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L28 |
| B0226 | R : Invalidation déterministe et traçable | H0 L33 | L33 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L33 |
| B0227 | S : Permission révoquée — sous « Invalidation déterministe et traçable » | H0 L40 | L40 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L40 |
| B0228 | R : Dégradation et protection contre l'avalanche | H0 L45 | L45 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L45 |
| B0229 | S : Expiration concurrente — sous « Dégradation et protection contre l'avalanche » | H0 L51 | L51 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L51 |

## docker-image

Canon H0/H1/courant : `openspec/specs/docker-image/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0230 | R : Composition reproductible corrélée à la release | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L22 |
| B0231 | S : Deux constructions d'une même release — sous « Composition reproductible corrélée à la release » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0232 | R : Image sans état ni secret | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L36 |
| B0233 | S : Valeur sensible dans l'image — sous « Image sans état ni secret » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L40 |
| B0234 | R : Configuration validée à l'exécution | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L45 |
| B0235 | S : Démarrage avec configuration invalide — sous « Configuration validée à l'exécution » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L49 |
| B0236 | R : Sondes alignées sur les états de santé | H0 L35 | L35 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L54 |
| B0237 | S : Dépendance optionnelle indisponible — sous « Sondes alignées sur les états de santé » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L58 |
| B0238 | R : Arrêt propre et orchestration sans autorité | H0 L44 | L44 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L63 |
| B0239 | S : Arrêt demandé pendant un traitement — sous « Arrêt propre et orchestration sans autorité » | H0 L48 | L48 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L67 |

## document-repositories

Canon H0/H1/courant : `openspec/specs/document-repositories/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0240 | R : Contrat référentiel et modes déclarés | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0241 | S : Mode ambigu refusé — sous « Contrat référentiel et modes déclarés » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0242 | R : Autorisation et audit préservés | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0243 | S : Contournement refusé — sous « Autorisation et audit préservés » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L23 |
| B0244 | R : Mappings, conflits et reprises | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L28 |
| B0245 | S : Divergence traitée explicitement — sous « Mappings, conflits et reprises » | H0 L34 | L34 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L34 |

## events

Canon H0/H1/courant : `openspec/specs/events/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0246 | R : Événements immuables versionnés | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0247 | S : Contrat d'intégration séparé — sous « Événements immuables versionnés » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0248 | R : Publication après validation transactionnelle | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0249 | S : Transaction échouée sans événement — sous « Publication après validation transactionnelle » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0250 | R : Consommateurs idempotents et ordonnés | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0251 | S : Rejou sans double effet — sous « Consommateurs idempotents et ordonnés » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |

## extension-contracts

Canon H0/H1/courant : `openspec/specs/extension-contracts/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0252 | R : Points d'extension publics versionnés | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0253 | S : Contribution sans point déclaré rejetée — sous « Points d'extension publics versionnés » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0254 | R : Contributions déclarées et isolées | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0255 | S : Accès privé bloqué — sous « Contributions déclarées et isolées » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0256 | R : Niveau de confiance des extensions | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0257 | S : Extension de développement en production — sous « Niveau de confiance des extensions » | H0 L33 | L33 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L33 |
| B0258 | R : Collisions et composition déterministe | H0 L38 | L38 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L38 |
| B0259 | S : Deux routes en collision — sous « Collisions et composition déterministe » | H0 L42 | L42 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L42 |
| B0260 | R : Composition interface au build | H0 L47 | L47 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L47 |
| B0261 | S : Code distant implicite refusé — sous « Composition interface au build » | H0 L51 | L51 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L51 |
| B0262 | R : Frontières publiques des composants frontend imbriqués | H0 L56 | L56 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L56 |
| B0263 | S : Slot enfant non déclaré — sous « Frontières publiques des composants frontend imbriqués » | H0 L60 | L60 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L60 |

## external-synchronization

Canon H0/H1/courant : `openspec/specs/external-synchronization/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0264 | R : Contrat de synchronisation et autorité déclarés | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0265 | S : Import direct refusé — sous « Contrat de synchronisation et autorité déclarés » | H0 L18 | L18 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L18 |
| B0266 | R : Reprise persistante et rejou idempotent | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L23 |
| B0267 | S : Reprise après interruption — sous « Reprise persistante et rejou idempotent » | H0 L27 | L27 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L27 |
| B0268 | R : Périmètre, traçabilité et échec fermé | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |
| B0269 | S : Périmètre non vérifiable refusé — sous « Périmètre, traçabilité et échec fermé » | H0 L36 | L36 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L36 |

## feature-flags

Canon H0/H1/courant : `openspec/specs/feature-flags/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0270 | R : Définition versionnée et bornée | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L18 |
| B0271 | S : Règle à expression rejetée — sous « Définition versionnée et bornée » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L22 |
| B0272 | R : Ciblage et cohorte déterministes | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L27 |
| B0273 | S : Même contexte même décision — sous « Ciblage et cohorte déterministes » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L31 |
| B0274 | R : Échec fermé pour le sensible | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L72 |
| B0275 | S : Fanion d'autorisation indisponible — sous « Échec fermé pour le sensible » | H0 L34 | L34 | IDENTIQUE | Aucune référence explicite dans le bloc | RATTACHEMENT MODIFIÉ L85 ; `6ac22961c242` ; voir VERIFICATIONS.md |
| B0276 | R : Affectations hors artefacts | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L113 |
| B0277 | S : Affectation embarquée rejetée — sous « Affectations hors artefacts » | H0 L45 | L45 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L119 |

## frontend

Canon H0/H1/courant : `openspec/specs/frontend/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0278 | R : Contributions déclarées et routage sans collision | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0279 | S : Route ambiguë bloquée — sous « Contributions déclarées et routage sans collision » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0280 | R : Session fournie par le shell et autorisation applicative | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0281 | S : Garde frontale non substitutive — sous « Session fournie par le shell et autorisation applicative » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0282 | R : Mutations provisoires et invalidation tenant-aware | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0283 | S : Invalidation après commande — sous « Mutations provisoires et invalidation tenant-aware » | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |
| B0284 | R : Sous-modularité frontend par le modèle de composants commun | H0 L37 | L37 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L37 |
| B0285 | S : Sous-module optionnel isolé — sous « Sous-modularité frontend par le modèle de composants commun » | H0 L41 | L41 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L41 |

## identity-assurance

Canon H0/H1/courant : `openspec/specs/identity-assurance/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0286 | R : Contexte vérifié et dimensions distinctes | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0287 | S : Claim absent sans surclassement — sous « Contexte vérifié et dimensions distinctes » | H0 L14 | L14 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L23 |
| B0288 | R : Seuil sensible et élévation explicite | H0 L19 | L19 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L28 |
| B0289 | S : Élévation exigée — sous « Seuil sensible et élévation explicite » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |
| B0290 | R : Fraîcheur, révocation et récupération sans élévation implicite | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L37 |
| B0291 | S : Récupération sans restauration d'assurance — sous « Fraîcheur, révocation et récupération sans élévation implicite » | H0 L34 | L34 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L43 |

## initial-administration

Canon H0/H1/courant : `openspec/specs/initial-administration/spec.md`.
D : `openspec/changes/archive/2026-09-16-specify-initial-application-bootstrap/specs/initial-administration/spec.md`, dans H1.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0292 | R : Modes de démarrage explicites | D L3 | L11 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L49 |
| B0293 | S : Marqueur externe indisponible — sous « Modes de démarrage explicites » | D L13 | L21 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L56 |
| B0294 | R : Provisionnement interactif de la base | D L20 | L28 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L75 |
| B0295 | S : Base migrable — sous « Provisionnement interactif de la base » | D L34 | L42 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L84 |
| B0296 | S : Référence de secret après provisionnement — sous « Provisionnement interactif de la base » | D L40 | L48 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | RATTACHEMENT MODIFIÉ L108 ; `6ac22961c242` ; voir VERIFICATIONS.md |
| B0297 | R : Création conditionnelle du Super Admin | D L46 | L54 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L114 |
| B0298 | S : Mots de passe différents — sous « Création conditionnelle du Super Admin » | D L56 | L64 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L123 |
| B0299 | S : Opérateur initial vérifié — sous « Création conditionnelle du Super Admin » | D L62 | L70 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REMPLACEMENT CONSTATÉ L129 ; `6ac22961c242` ; voir VERIFICATIONS.md |
| B0300 | R : Marqueur externe et première configuration | D L68 | L76 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L145 |
| B0301 | S : Configuration initiale inachevée — sous « Marqueur externe et première configuration » | D L77 | L85 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L154 |
| B0302 | R : Panneau d'administration contrôlé | D L84 | L92 | REPLIEMENT DE PROSE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L161 |
| B0303 | S : Ancienne route d'administration — sous « Panneau d'administration contrôlé » | D L94 | L102 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | RATTACHEMENT MODIFIÉ L181 ; `6ac22961c242` ; voir VERIFICATIONS.md |
| B0304 | R : Expérience et état du panneau | D L99 | L107 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L186 |
| B0305 | S : Santé réservée au root — sous « Expérience et état du panneau » | D L108 | L116 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L195 |
| B0306 | R : Désactivation externe du Super Admin | D L114 | L122 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L201 |
| B0307 | S : Connexion root désactivée — sous « Désactivation externe du Super Admin » | D L122 | L130 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L210 |

## initial-application-bootstrap

Canon H0/H1/courant : `openspec/specs/initial-application-bootstrap/spec.md`.
D : `openspec/changes/archive/2026-09-16-specify-initial-application-bootstrap/specs/initial-application-bootstrap/spec.md`, dans H1.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0308 | R : Composition Django initiale déclarée | D L3 | L11 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L11 |
| B0309 | S : Composition initiale valide — sous « Composition Django initiale déclarée » | D L16 | L24 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L21 |
| B0310 | R : Surface HTTP initiale minimale | D L22 | L30 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L39 |
| B0311 | S : Route initiale non déclarée — sous « Surface HTTP initiale minimale » | D L31 | L39 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L48 |
| B0312 | R : Shell TanStack initial intégré | D L37 | L45 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L54 |
| B0313 | S : Démarrage du shell initial — sous « Shell TanStack initial intégré » | D L45 | L53 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L62 |
| B0314 | R : Profil de test intégré isolé | D L51 | L59 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L68 |
| B0315 | S : Vérification locale conjointe — sous « Profil de test intégré isolé » | D L60 | L68 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L77 |

## installation-provisioning

Canon H0/H1/courant : `openspec/specs/installation-provisioning/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0316 | R : Provisionnement explicite et états inspectables | H0 L9 | L9 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L18 |
| B0317 | S : Installation non provisionnée — sous « Provisionnement explicite et états inspectables » | H0 L16 | L16 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L25 |
| B0318 | R : Configuration et secrets vérifiés avant mise en service | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |
| B0319 | S : Référence de secret indisponible — sous « Configuration et secrets vérifiés avant mise en service » | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L37 |
| B0320 | R : Opérateur initial explicite et sans privilège implicite | H0 L33 | L33 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L42 |
| B0321 | S : Identité opérateur absente — sous « Opérateur initial explicite et sans privilège implicite » | H0 L40 | L40 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L50 |
| B0322 | R : Création tenant-scoped contrôlée | H0 L45 | L45 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L55 |
| B0323 | S : Rejou du provisionnement du premier tenant — sous « Création tenant-scoped contrôlée » | H0 L53 | L53 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L63 |
| B0324 | R : Reprise contrôlée et auditée | H0 L58 | L58 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L68 |
| B0325 | S : Interruption avant mise en service — sous « Reprise contrôlée et auditée » | H0 L65 | L65 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L75 |

## interactions

Canon H0/H1/courant : `openspec/specs/interactions/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0326 | R : Commandes validées et autorisées | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L18 |
| B0327 | S : Mutation sans autorisation refusée — sous « Commandes validées et autorisées » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L22 |
| B0328 | R : Requêtes sans mutation implicite | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L27 |
| B0329 | S : Lecture filtrée à la source — sous « Requêtes sans mutation implicite » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L31 |
| B0330 | R : Idempotence et traçabilité des commandes | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L36 |
| B0331 | S : Rejou divergent — sous « Idempotence et traçabilité des commandes » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L40 |

## internationalization

Canon H0/H1/courant : `openspec/specs/internationalization/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0332 | R : Catalogues par composant et langue canonique | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0333 | S : Clé manquante bloquée — sous « Catalogues par composant et langue canonique » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0334 | R : Résolution déterministe et formats localisés | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0335 | S : Valeur métier préservée — sous « Résolution déterministe et formats localisés » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L23 |

## jobs

Canon H0/H1/courant : `openspec/specs/jobs/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0336 | R : Persistance et états explicites | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L31 |
| B0337 | S : Reprise après interruption — sous « Persistance et états explicites » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L35 |
| B0338 | R : Autorisation réévaluée à l'exécution | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L40 |
| B0339 | S : Contexte expiré refusé — sous « Autorisation réévaluée à l'exécution » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L44 |
| B0340 | R : Idempotence et corrélation des travaux | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L49 |
| B0341 | S : Double déclenchement dédupliqué — sous « Idempotence et corrélation des travaux » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L53 |

## kernel

Canon H0/H1/courant : `openspec/specs/kernel/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0342 | R : Noyau sans logique métier | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0343 | S : Démarrage minimal sans modèle métier — sous « Noyau sans logique métier » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0344 | R : Noyau fournit des registres génériques | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0345 | S : Résolution déterministe — sous « Noyau fournit des registres génériques » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0346 | R : Noyau agnostique aux fournisseurs | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0347 | S : Module ajouté sans modification du noyau — sous « Noyau agnostique aux fournisseurs » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |
| B0348 | R : Composition ambiguë refusée explicitement | H0 L35 | L35 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L35 |
| B0349 | S : Deux fournisseurs sans sélection — sous « Composition ambiguë refusée explicitement » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L39 |

## lifecycle

Canon H0/H1/courant : `openspec/specs/lifecycle/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0350 | R : États de cycle de vie distincts | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0351 | S : États non confondus — sous « États de cycle de vie distincts » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0352 | R : Transitions autorisées et refusées | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0353 | S : Désactivation sans perte et purge explicite — sous « Transitions autorisées et refusées » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0354 | R : Ordre déterministe des hooks | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0355 | S : Double résolution identique — sous « Ordre déterministe des hooks » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |
| B0356 | R : Idempotence des opérations | H0 L35 | L35 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L35 |
| B0357 | S : Rejeu sans double effet — sous « Idempotence des opérations » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L39 |
| B0358 | R : Diagnostic des échecs | H0 L44 | L44 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L44 |
| B0359 | S : Activation invalide bloquée — sous « Diagnostic des échecs » | H0 L48 | L48 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L48 |

## migrations

Canon H0/H1/courant : `openspec/specs/migrations/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0360 | R : Contrat de migration | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0361 | S : Migration sans version cible — sous « Contrat de migration » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0362 | R : Planification et ordre déterministes | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0363 | S : Deux migrations concurrentes — sous « Planification et ordre déterministes » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0364 | R : Compatibilité pendant l'application | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0365 | S : Coexistence pendant migration — sous « Compatibilité pendant l'application » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |
| B0366 | R : Reprise idempotente | H0 L35 | L35 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L35 |
| B0367 | S : Interruption puis reprise — sous « Reprise idempotente » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L39 |
| B0368 | R : Contraction contrôlée | H0 L44 | L44 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L44 |
| B0369 | S : Contraction prématurée — sous « Contraction contrôlée » | H0 L48 | L48 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L48 |

## modules

Canon H0/H1/courant : `openspec/specs/modules/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0370 | R : Manifest lisible obligatoire | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0371 | S : Manifest incomplet — sous « Manifest lisible obligatoire » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0372 | R : Frontière API publique et privée | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0373 | S : Accès à une API non déclarée — sous « Frontière API publique et privée » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0374 | R : Propriété des données et migrations associées | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0375 | S : Changement de schéma non migré — sous « Propriété des données et migrations associées » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |
| B0376 | R : Chargement contrôlé déterministe | H0 L35 | L35 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L35 |
| B0377 | S : Cycle de dépendances — sous « Chargement contrôlé déterministe » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L39 |
| B0378 | R : Propriété des contributions frontend modulaires | H0 L44 | L44 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L44 |
| B0379 | S : Sous-module autonome intégré — sous « Propriété des contributions frontend modulaires » | H0 L48 | L48 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L48 |

## native-clients

Canon H0/H1/courant : `openspec/specs/native-clients/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0380 | R : Contrats publics et SDK compatibles | H0 L10 | L10 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L10 |
| B0381 | S : API incompatible — sous « Contrats publics et SDK compatibles » | H0 L16 | L16 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L16 |
| B0382 | R : Session et stockage local sécurisés | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0383 | S : Sauvegarde d'application — sous « Session et stockage local sécurisés » | H0 L27 | L27 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L25 |
| B0384 | R : Notifications et liens profonds autorisés | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L35 |
| B0385 | S : Lien profond reçu — sous « Notifications et liens profonds autorisés » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L42 |
| B0386 | R : Offline-first et révocation cohérents | H0 L44 | L44 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L47 |
| B0387 | S : Command locale après révocation — sous « Offline-first et révocation cohérents » | H0 L51 | L51 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L54 |

## notifications

Canon H0/H1/courant : `openspec/specs/notifications/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0388 | R : Contrats et préférences déclarés | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0389 | S : Canal non déclaré refusé — sous « Contrats et préférences déclarés » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0390 | R : Asynchronisme avec réessais bornés | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L22 |
| B0391 | S : Échec persistant tracé — sous « Asynchronisme avec réessais bornés » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L28 |
| B0392 | R : Confidentialité et audit | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L33 |
| B0393 | S : Donnée protégée minimisée — sous « Confidentialité et audit » | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L37 |

## object-storage

Canon H0/H1/courant : `openspec/specs/object-storage/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0394 | R : Contrat fournisseur objet et métadonnées Pixs | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0395 | S : Suppression propagée au fournisseur — sous « Contrat fournisseur objet et métadonnées Pixs » | H0 L14 | L14 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L14 |
| B0396 | R : Isolation tenant et périmètre | H0 L19 | L19 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L19 |
| B0397 | S : Accès inter-tenant refusé — sous « Isolation tenant et périmètre » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L23 |
| B0398 | R : Conformité des adaptateurs | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L28 |
| B0399 | S : Adaptateur non conforme bloqué — sous « Conformité des adaptateurs » | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |

## observability

Canon H0/H1/courant : `openspec/specs/observability/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0400 | R : Signaux structurés et corrélés | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0401 | S : Corrélation bout en bout — sous « Signaux structurés et corrélés » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0402 | R : Santé distinguée et sondes bornées | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0403 | S : Dépendance optionnelle dégradée — sous « Santé distinguée et sondes bornées » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0404 | R : Objectifs de service déclarés | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0405 | S : Objectif sans méthode de mesure — sous « Objectifs de service déclarés » | H0 L33 | L33 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L33 |
| B0406 | R : Rétention et minimisation séparées | H0 L38 | L38 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L38 |
| B0407 | S : Accès inter-tenant tracé — sous « Rétention et minimisation séparées » | H0 L44 | L44 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L44 |

## offline-first

Canon H0/H1/courant : `openspec/specs/offline-first/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0408 | R : Éligibilité déclarée et projections non autoritatives | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0409 | S : Ressource non éligible indisponible — sous « Éligibilité déclarée et projections non autoritatives » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0410 | R : Intentions provisoires réévaluées au serveur | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0411 | S : Commande hors ligne rejetée au serveur — sous « Intentions provisoires réévaluées au serveur » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L23 |
| B0412 | R : Conflits, révocation et purge locale | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L28 |
| B0413 | S : Révocation purgeant le local — sous « Conflits, révocation et purge locale » | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |

## operations

Canon H0/H1/courant : `openspec/specs/operations/spec.md`.
D : `openspec/changes/archive/2026-09-16-specify-initial-application-bootstrap/specs/operations/spec.md`, dans H1.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0414 | R : Interface de management distincte et non publique | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0415 | S : Façades convergeant sur le même contrat — sous « Interface de management distincte et non publique » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0416 | R : Opérations persistantes avec plan et idempotence | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0417 | S : Rejeu d'une opération annulée — sous « Opérations persistantes avec plan et idempotence » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |
| B0418 | R : Sorties sans secret et codes stables | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L35 |
| B0419 | S : Commande non autorisée — sous « Sorties sans secret et codes stables » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L39 |
| B0420 | R : État de maintenance avec drainage borné | H0 L35 | L35 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L44 |
| B0421 | S : Requête reçue pendant le drainage — sous « État de maintenance avec drainage borné » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L48 |
| B0422 | R : Health, diagnostic et audit opérateur | H0 L44 | L44 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L53 |
| B0423 | S : Réparation via le diagnostic — sous « Health, diagnostic et audit opérateur » | H0 L48 | L48 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L57 |
| B0424 | R : Maintenance hiérarchisée | D L3 | L53 | REPLIEMENT DE PROSE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L62 |
| B0425 | S : Maintenance d'une route — sous « Maintenance hiérarchisée » | D L11 | L62 | IDENTIQUE | authorization, identity-assurance, installation-provisioning, reference-composition, secrets-providers | REPÈRE CONSERVÉ L71 |

## performance

Canon H0/H1/courant : `openspec/specs/performance/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0426 | R : Mesurer avant d'optimiser | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0427 | S : Optimisation non mesurée — sous « Mesurer avant d'optimiser » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0428 | R : Budgets déclarés et vérifiés | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0429 | S : Régression détectée — sous « Budgets déclarés et vérifiés » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0430 | R : Objectifs propres au profil | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0431 | S : Budget hors profil — sous « Objectifs propres au profil » | H0 L33 | L33 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L33 |
| B0432 | R : Aucune performance au prix des invariants | H0 L38 | L38 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L38 |
| B0433 | S : Cache court-circuitant l'autorisation — sous « Aucune performance au prix des invariants » | H0 L42 | L42 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L42 |
| B0434 | R : Caches et projections dérivés non autoritaires | H0 L47 | L47 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L47 |
| B0435 | S : Cache périmé indisponible — sous « Caches et projections dérivés non autoritaires » | H0 L51 | L51 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L51 |

## progressive-deployment

Canon H0/H1/courant : `openspec/specs/progressive-deployment/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0436 | R : Révisions et stratégies explicitement déclarées | H0 L11 | L11 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L11 |
| B0437 | S : Stratégie non déclarée — sous « Révisions et stratégies explicitement déclarées » | H0 L18 | L18 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L18 |
| B0438 | R : Prévalidations et health gates obligatoires | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L23 |
| B0439 | S : Readiness en échec — sous « Prévalidations et health gates obligatoires » | H0 L29 | L29 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L29 |
| B0440 | R : Routage progressif sans élargissement de données | H0 L34 | L34 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L34 |
| B0441 | S : Client utilisant une majeure antérieure — sous « Routage progressif sans élargissement de données » | H0 L40 | L40 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L40 |
| B0442 | R : Retour arrière orchestré et audité | H0 L45 | L45 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L45 |
| B0443 | S : Migration irréversible appliquée — sous « Retour arrière orchestré et audité » | H0 L52 | L52 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L52 |

## providers

Canon H0/H1/courant : `openspec/specs/providers/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0444 | R : Déclaration lisible des fournisseurs | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0445 | S : Implémentation non déclarée — sous « Déclaration lisible des fournisseurs » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0446 | R : Sélection explicite sans choix implicite | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0447 | S : Deux candidats sans configuration — sous « Sélection explicite sans choix implicite » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0448 | R : Conformité contractuelle vérifiable | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0449 | S : Fournisseur non conforme activé — sous « Conformité contractuelle vérifiable » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |
| B0450 | R : Dégradation contrôlée et diagnostic | H0 L35 | L35 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L35 |
| B0451 | S : Indisponibilité d'un fournisseur — sous « Dégradation contrôlée et diagnostic » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L39 |

## quotas-entitlements

Canon H0/H1/courant : `openspec/specs/quotas-entitlements/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0452 | R : Droits rattachés sans élargissement | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0453 | S : Élargissement par scope refusé — sous « Droits rattachés sans élargissement » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0454 | R : Quotas cumulatifs et réservations atomiques | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0455 | S : Rejou sans double consommation — sous « Quotas cumulatifs et réservations atomiques » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |
| B0456 | R : Application applicative et échec fermé | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L37 |
| B0457 | S : Contrôle indisponible — sous « Application applicative et échec fermé » | H0 L34 | L34 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L43 |

## realtime-collaboration

Canon H0/H1/courant : `openspec/specs/realtime-collaboration/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0458 | R : Sessions collaboratives tenant-scoped et autorisées | H0 L11 | L11 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L11 |
| B0459 | S : Participant hors périmètre — sous « Sessions collaboratives tenant-scoped et autorisées » | H0 L18 | L18 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L18 |
| B0460 | R : Convergence versionnée sans mutation implicite | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L23 |
| B0461 | S : Opération concurrente convergente — sous « Convergence versionnée sans mutation implicite » | H0 L31 | L31 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L31 |
| B0462 | R : Reconnexion, révocation et offline-first cohérents | H0 L36 | L36 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L36 |
| B0463 | S : Droits retirés hors ligne — sous « Reconnexion, révocation et offline-first cohérents » | H0 L42 | L42 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L42 |
| B0464 | R : Présence minimisée et auditée | H0 L47 | L47 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L47 |
| B0465 | S : Expiration de présence — sous « Présence minimisée et auditée » | H0 L53 | L53 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L53 |

## reference-composition

Canon H0/H1/courant : `openspec/specs/reference-composition/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0466 | R : Capacités obligatoires du P0 | H0 L10 | L10 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L35 |
| B0467 | S : Capacité P0 absente — sous « Capacités obligatoires du P0 » | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L39 |
| B0468 | R : Capacités hors P0 explicites | H0 L22 | L22 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L44 |
| B0469 | S : Synchronisation non sélectionnée — sous « Capacités hors P0 explicites » | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L50 |
| B0470 | R : Preuve reproductible | H0 L33 | L33 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L55 |
| B0471 | S : Deux validations identiques — sous « Preuve reproductible » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L61 |

## reference-runtime

Canon H0/H1/courant : `openspec/specs/reference-runtime/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0472 | R : Pile de référence unique | H0 L10 | L10 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L63 |
| B0473 | S : Runtime décrit — sous « Pile de référence unique » | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L67 |
| B0474 | R : Adapter explicite | H0 L22 | L22 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L77 |
| B0475 | S : Runtime alternatif non déclaré — sous « Adapter explicite » | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L83 |
| B0476 | R : Absence de sélection cachée | H0 L33 | L33 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L88 |
| B0477 | S : Paquet alternatif présent — sous « Absence de sélection cachée » | H0 L38 | L38 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L93 |

## regional-residency

Canon H0/H1/courant : `openspec/specs/regional-residency/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0478 | R : Politique de placement versionnée par tenant | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L18 |
| B0479 | S : Élargissement par enfant refusé — sous « Politique de placement versionnée par tenant » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L22 |
| B0480 | R : Routage après identité et périmètre | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L27 |
| B0481 | S : Dérivé hors région interdit — sous « Routage après identité et périmètre » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L31 |
| B0482 | R : Bascule contrôlée sans cerveau partagé | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L36 |
| B0483 | S : Bascule sans barrière refusée — sous « Bascule contrôlée sans cerveau partagé » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L40 |

## release-management

Canon H0/H1/courant : `openspec/specs/release-management/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0484 | R : Définition et support d'une release | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0485 | S : Release sans déclaration de support — sous « Définition et support d'une release » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0486 | R : Chemin de migration vérifiable | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0487 | S : Saut non prouvé — sous « Chemin de migration vérifiable » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0488 | R : Mise à niveau orchestrée par prévalidations | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0489 | S : Étape de prévalidation échouée — sous « Mise à niveau orchestrée par prévalidations » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |
| B0490 | R : Coexistence transitoire N et N+1 | H0 L35 | L35 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L35 |
| B0491 | S : Contraction pendant la fenêtre — sous « Coexistence transitoire N et N+1 » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L39 |
| B0492 | R : Retour arrière soumis à la matrice | H0 L44 | L44 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L44 |
| B0493 | S : Retour arrière non garanti — sous « Retour arrière soumis à la matrice » | H0 L50 | L50 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L50 |
| B0494 | R : Activation, retrait et instance non valide | H0 L55 | L55 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L55 |
| B0495 | S : Instance échouant aux contrôles — sous « Activation, retrait et instance non valide » | H0 L59 | L59 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L59 |

## reporting-analytics

Canon H0/H1/courant : `openspec/specs/reporting-analytics/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0496 | R : Projections analytiques dérivées et propriétaires | H0 L10 | L10 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L10 |
| B0497 | S : Projection reconstruite — sous « Projections analytiques dérivées et propriétaires » | H0 L16 | L16 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L16 |
| B0498 | R : Couche sémantique versionnée | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0499 | S : Définition de métrique modifiée — sous « Couche sémantique versionnée » | H0 L27 | L27 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L27 |
| B0500 | R : Filtrage, gouvernance et résidence à la source | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |
| B0501 | S : Agrégat inter-tenant non autorisé — sous « Filtrage, gouvernance et résidence à la source » | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L39 |
| B0502 | R : Exports et rapports asynchrones contrôlés | H0 L44 | L44 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L44 |
| B0503 | S : Autorisation révoquée pendant un export — sous « Exports et rapports asynchrones contrôlés » | H0 L50 | L50 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L50 |

## resilience

Canon H0/H1/courant : `openspec/specs/resilience/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0504 | R : Isolation des défaillances optionnelles | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0505 | S : Fournisseur optionnel en panne isolé — sous « Isolation des défaillances optionnelles » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0506 | R : Dégradation sans affaiblissement sécurité | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0507 | S : Dégradé sans permissivité — sous « Dégradation sans affaiblissement sécurité » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0508 | R : Révocation et diagnostic des compromissions | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0509 | S : Composant compromis bloqué — sous « Révocation et diagnostic des compromissions » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |

## runtime

Canon H0/H1/courant : `openspec/specs/runtime/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0510 | R : Profils distincts d'un même artefact | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L130 |
| B0511 | S : Profil activé par configuration — sous « Profils distincts d'un même artefact » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L134 |
| B0512 | R : Profils de déploiement déclarés | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L139 |
| B0513 | S : Capacité absente dans un profil local — sous « Profils de déploiement déclarés » | H0 L24 | L24 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L146 |
| B0514 | R : Exposition minimale par défaut | H0 L29 | L29 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L151 |
| B0515 | S : Endpoint de management publiquement joignable — sous « Exposition minimale par défaut » | H0 L33 | L33 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L155 |
| B0516 | R : Processus stateless et coordination persistante | H0 L38 | L38 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L160 |
| B0517 | S : Redémarrage d'un worker — sous « Processus stateless et coordination persistante » | H0 L42 | L42 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L164 |
| B0518 | R : Lease du scheduler avec clôture de péremption | H0 L47 | L47 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L174 |
| B0519 | S : Ancien détenteur toujours actif — sous « Lease du scheduler avec clôture de péremption » | H0 L51 | L51 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L178 |
| B0520 | R : Arrêt, drain et reprise contrôlés | H0 L56 | L56 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L183 |
| B0521 | S : Arrêt pendant traitement — sous « Arrêt, drain et reprise contrôlés » | H0 L60 | L60 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L187 |

## scim-provisioning

Canon H0/H1/courant : `openspec/specs/scim-provisioning/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0522 | R : Provider SCIM déclaré et sélectionné explicitement | H0 L11 | L11 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L11 |
| B0523 | S : Deux providers SCIM compatibles — sous « Provider SCIM déclaré et sélectionné explicitement » | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0524 | R : Ingestion authentifiée par Commands propriétaires | H0 L22 | L22 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L22 |
| B0525 | S : Groupe externe reçu — sous « Ingestion authentifiée par Commands propriétaires » | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L28 |
| B0526 | R : Idempotence, mapping et désactivation contrôlés | H0 L33 | L33 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L33 |
| B0527 | S : Notification SCIM rejouée — sous « Idempotence, mapping et désactivation contrôlés » | H0 L40 | L40 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L40 |
| B0528 | R : Périmètre et confidentialité préservés | H0 L45 | L45 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L45 |
| B0529 | S : Attribut sensible non déclaré — sous « Périmètre et confidentialité préservés » | H0 L51 | L51 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L51 |

## scope-context

Canon H0/H1/courant : `openspec/specs/scope-context/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0530 | R : Tenant racine et parenté unique | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L18 |
| B0531 | S : Cycle de scopes refusé — sous « Tenant racine et parenté unique » | H0 L14 | L14 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L24 |
| B0532 | R : Propriété canonique unique | H0 L19 | L19 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L29 |
| B0533 | S : Scope sans tenant cohérent refusé — sous « Propriété canonique unique » | H0 L25 | L25 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L35 |
| B0534 | R : Contexte immuable propagé avant autorisation | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L40 |
| B0535 | S : Élargissement implicite refusé — sous « Contexte immuable propagé avant autorisation » | H0 L36 | L36 | IDENTIQUE | Aucune référence explicite dans le bloc | RATTACHEMENT MODIFIÉ L63 ; `6ac22961c242` ; voir VERIFICATIONS.md |

## sdk-ecosystem

Canon H0/H1/courant : `openspec/specs/sdk-ecosystem/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0536 | R : Génération déterministe depuis les contrats | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0537 | S : Divergence contrat-kit bloquée — sous « Génération déterministe depuis les contrats » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0538 | R : Propagation du contexte et erreurs typées | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0539 | S : Périmètre non élargi par le client — sous « Propagation du contexte et erreurs typées » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0540 | R : Outillage validé sans secret | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0541 | S : Exemple sans secret — sous « Outillage validé sans secret » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |

## search

Canon H0/H1/courant : `openspec/specs/search/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0542 | R : Projections dérivées reconstruisibles | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0543 | S : Permission révoquée propagée — sous « Projections dérivées reconstruisibles » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0544 | R : Filtrage autorisé à la source | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0545 | S : Résultat hors périmètre exclu — sous « Filtrage autorisé à la source » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0546 | R : Cohérence et dégradation déclarées | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0547 | S : Moteur dégradé diagnostiqué — sous « Cohérence et dégradation déclarées » | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |

## secrets-providers

Canon H0/H1/courant : `openspec/specs/secrets-providers/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0548 | R : Références externes sans valeur persistée | H0 L11 | L11 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L11 |
| B0549 | S : Diagnostic de référence indisponible — sous « Références externes sans valeur persistée » | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0550 | R : Accès runtime associé à une identité de workload | H0 L22 | L22 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L22 |
| B0551 | S : Worker non autorisé — sous « Accès runtime associé à une identité de workload » | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L28 |
| B0552 | R : Rotation, durée de vie et révocation contrôlées | H0 L33 | L33 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L33 |
| B0553 | S : Secret tourné — sous « Rotation, durée de vie et révocation contrôlées » | H0 L42 | L42 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L42 |
| B0554 | R : Audit minimisé et échec fermé | H0 L47 | L47 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L47 |
| B0555 | S : Provider indisponible — sous « Audit minimisé et échec fermé » | H0 L53 | L53 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L53 |

## security

Canon H0/H1/courant : `openspec/specs/security/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0556 | R : Profil de sécurité déclaré par composant | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0557 | S : Vulnérabilité critique bloquante — sous « Profil de sécurité déclaré par composant » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0558 | R : Échec fermé sans mode permissif | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0559 | S : Contexte non vérifiable refusé — sous « Échec fermé sans mode permissif » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |
| B0560 | R : Diagnostics sans exposition sensible | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L37 |
| B0561 | S : Secret hors journaux — sous « Diagnostics sans exposition sensible » | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L41 |

## service-objectives

Canon H0/H1/courant : `openspec/specs/service-objectives/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0562 | R : Objectifs versionnés | H0 L10 | L10 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L10 |
| B0563 | S : Objectif de reprise déclaré — sous « Objectifs versionnés » | H0 L16 | L16 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L16 |
| B0564 | R : Absence de seuil universel implicite | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0565 | S : Mesure locale isolée — sous « Absence de seuil universel implicite » | H0 L27 | L27 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L27 |
| B0566 | R : Validation reproductible | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |
| B0567 | S : Objectif non satisfait — sous « Validation reproductible » | H0 L38 | L38 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L38 |

## services

Canon H0/H1/courant : `openspec/specs/services/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0568 | R : Enregistrement contractuel des services | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0569 | S : Service privé non exposé — sous « Enregistrement contractuel des services » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0570 | R : Résolution déterministe du fournisseur | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0571 | S : Ambiguïté refusée — sous « Résolution déterministe du fournisseur » | H0 L23 | L23 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L23 |
| B0572 | R : Traçabilité et sécurité des appels | H0 L28 | L28 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L28 |
| B0573 | S : Contexte non vérifiable — sous « Traçabilité et sécurité des appels » | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |

## synchronization

Canon H0/H1/courant : `openspec/specs/synchronization/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0574 | R : Mécanisme réactif optionnel sous autorité applicative | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0575 | S : Mutation non validée non propagée — sous « Mécanisme réactif optionnel sous autorité applicative » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0576 | R : Périmètre et autorisation propagés aux projections | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0577 | S : Donnée révoquée invalidée — sous « Périmètre et autorisation propagés aux projections » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0578 | R : Cohérence déclarée et échec contrôlé | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0579 | S : Fournisseur perdu diagnostiqué — sous « Cohérence déclarée et échec contrôlé » | H0 L32 | L32 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L32 |

## testing

Canon H0/H1/courant : `openspec/specs/testing/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0580 | R : Trois niveaux de vérification distincts | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0581 | S : Unitaires verts, intégration rouge — sous « Trois niveaux de vérification distincts » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0582 | R : Kit de conformité et composant d'exemple | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0583 | S : Exemple P0 validé — sous « Kit de conformité et composant d'exemple » | H0 L25 | L25 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L25 |
| B0584 | R : Suites de conformité versionnées par contrat | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |
| B0585 | S : Certification expirée — sous « Suites de conformité versionnées par contrat » | H0 L34 | L34 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L34 |
| B0586 | R : Garanties obligatoires séparées des capacités optionnelles | H0 L39 | L39 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L39 |
| B0587 | S : Isolement acceptable — sous « Garanties obligatoires séparées des capacités optionnelles » | H0 L43 | L43 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L43 |
| B0588 | R : Reproductibilité sur la topologie de référence | H0 L48 | L48 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L48 |
| B0589 | S : Divergence de topologie — sous « Reproductibilité sur la topologie de référence » | H0 L52 | L52 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L52 |
| B0590 | R : Preuves sans secret ni donnée de production | H0 L57 | L57 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L57 |
| B0591 | S : Secret détecté dans un rapport — sous « Preuves sans secret ni donnée de production » | H0 L61 | L61 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L61 |
| B0592 | R : Conformité de la composition frontend récursive | H0 L66 | L66 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L66 |
| B0593 | S : Composition reproductible avec sous-module — sous « Conformité de la composition frontend récursive » | H0 L70 | L70 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L70 |
| B0594 | R : Conformité des projections d'annuaire optionnelles | H0 L75 | L75 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L75 |
| B0595 | S : Repli conforme sans élargissement de droits — sous « Conformité des projections d'annuaire optionnelles » | H0 L84 | L84 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L84 |

## themes

Canon H0/H1/courant : `openspec/specs/themes/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0596 | R : Modes clair et sombre obligatoires | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0597 | S : Bascule sans rechargement — sous « Modes clair et sombre obligatoires » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0598 | R : Tokens sémantiques sans valeurs codées | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0599 | S : Valeur codée rejetée — sous « Tokens sémantiques sans valeurs codées » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |

## workflows

Canon H0/H1/courant : `openspec/specs/workflows/spec.md`.

| Repère | Type et intitulé | Source | H1 | Conservation | Dépendances explicites | Canon courant |
| --- | --- | --- | --- | --- | --- | --- |
| B0600 | R : Définitions et instances versionnées | H0 L8 | L8 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L8 |
| B0601 | S : Instance incompatible non migrée — sous « Définitions et instances versionnées » | H0 L12 | L12 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L12 |
| B0602 | R : Transitions gardées et autorisées | H0 L17 | L17 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L17 |
| B0603 | S : Transition non autorisée refusée — sous « Transitions gardées et autorisées » | H0 L21 | L21 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L21 |
| B0604 | R : Reprise persistante sans perte | H0 L26 | L26 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L26 |
| B0605 | S : Redémarrage avec reprise — sous « Reprise persistante sans perte » | H0 L30 | L30 | IDENTIQUE | Aucune référence explicite dans le bloc | REPÈRE CONSERVÉ L30 |

