# Conception — C00

## Contexte et autorisation

Le développeur a validé l’inventaire puis demandé C00 et la préparation progressive des changes nécessaires au profil, sans implémentation. L’inventaire de référence est `reports/p0-coverage-2026-10-16/inventaire-global.json` ; les sources normatives restent les capacités sous `openspec/specs/`.

Les cadrages sont consultés dans l’ordre AGENTS, PROJECT, TECHNICAL, BUILD, DEVOPS. Le registre normatif PA/PZT conserve ses choix validés et ses modalités ouvertes. Les modifications préexistantes du dépôt sont préservées. Une session directe de préparation ne déclenche ni OpenCode ni CAB.

## Profil retenu pour préparer les dossiers

| Dimension | Périmètre |
|---|---|
| Identité documentaire du profil | `pbo-p0-debian-local-v1`, sans nouvelle variable d’environnement |
| Distribution initiale | Paquet Debian PBO/PFO indépendant ; Debian 13 local, architecture exacte à qualifier avant construction |
| Autorités | Django pour règles/transactions ; PostgreSQL externe comme source de vérité ; TanStack/React pour PFO |
| Runtime | web, worker et scheduler du même artefact ; coordination persistante ; pas de haute disponibilité annoncée |
| Installation | INSTALLER, FIRST_CONFIGURATION, NORMAL, MAINTENANCE ; marqueur externe et état initial en base distincts |
| Identité et périmètre | Compte Super Admin unique authentifiable, premier tenant explicite, comptes ordinaires et scopes sous contrats Core |
| Administration | Panneau initial `/admin/`, routes publiques explicites et API versionnée ; contrôles identiques aux façades CLI/asynchrones |
| PZT et DNS côté PBO | Modules essentiels présents, données propriétaires, configuration souhaitée et états inspectables ; pas de fausse disponibilité d’un exécutant absent |
| Exécution PZT/DNS par PA | Non sélectionnée ; aucun PA ne reçoit d’instruction ou de mesure à collecter dans ce profil |
| Capacités supplémentaires | Non sélectionnées par défaut ; toute dépendance obligatoire des fonctions retenues reste requise |
| Recette | Unités, intégration réelle PostgreSQL, conformité versionnée, Chromium/Firefox headless et vérifications manuelles d’accessibilité |
| Livraison | Canal expérimental local explicitement identifié ; identité signée, provenance, inventaire et révocation vérifiables avant installation |

La première installation d’un tenant ne modifie pas l’architecture multi-tenant : les tests négatifs vérifient aussi l’isolement entre tenants synthétiques. Le composant d’exemple démontre les contrats dans la recette, sans devenir une dépendance de production.

## Décisions et alternatives

1. **Paquet PBO/PFO d’abord.** La séparation Debian est normative. L’image Docker impose trois binaires PA et étendrait le chemin critique ; elle n’est pas retenue pour cette première livraison.
2. **Gestion PZT/DNS obligatoire, exécution non sélectionnée.** La présence du module PZT ne lance pas le réseau. A06c distingue le module DNS de son service distinct piloté par PA. Les interfaces de gestion conservent leurs contrats et annoncent l’absence d’exécution. Retirer les modules ou simuler leurs mesures contredirait le canon.
3. **Conditions évaluées par rôle.** Les 174 contrats détaillés restent attachés à leurs traitements. Le profil sans PA ne déclenche ni PKI réseau, attestation, relais, auxiliaire temporel ni purge de télémétrie d’un collecteur absent. Les valeurs validées ne sont pas réécrites et restent opposables dès sélection du rôle.
4. **Préparation distincte de réalisation.** C01–C19 portent les compléments d’implémentation des comportements déjà spécifiés. Ils référencent le canon sans inventer de delta identique pour satisfaire un outil. Leur métadonnée `skip_specs: true` exprime l’absence d’évolution normative prévue, pas une dispense d’exigence ni de recette. Une précision modifiant le comportement normatif devra fournir un delta avant toute réalisation.

## Décisions de conception encore nécessaires

Ces points sont des barrières à la réalisation, pas des valeurs implicitement approuvées par la validation de l’inventaire. Les dossiers peuvent être préparés sans les trancher ; ils ne sont pas tous prêts à implémenter.

| Sujet | Dossier responsable | Barrière |
|---|---|---|
| SecretProvider concret, identité de workload, rotation/révocation | C01 | Arbitrage de sécurité et conformité avant implémentation du provider ; aucun provider externe ni dépendance nouvelle imposés ici |
| Modèle persistant Core, contrats propriétaires et transactions | C02 | Revue des schémas et contraintes avant modèles/migrations |
| Authentification initiale, sessions/jetons, cookies/Bearer et bornes | C03 | Choix de confiance et durées explicites ; aucun rapprochement par courriel ni stockage navigateur implicite |
| Reconnaissance Super Admin, accords tenant, obligations PEP et audits dérogés | C04/C05 | Revue transversale ; aucune exception conférée par un profil structurel |
| Identifiants canoniques modules PZT/DNS et contrats de gestion | C14 | Décision d’architecture traçable avant manifests ; aucune valeur inventée pour un choix laissé ouvert |
| Noms/versions de paquets, architectures et origines compatibles | C18 | Fixation avant construction ; aucune architecture déclarée qualifiée du seul DEVOPS |
| Objectifs de service, RPO/RTO, budgets et support | C15/C16/C17/C19 | Déclarer puis qualifier les valeurs du profil ; pas de seuil universel arbitraire |
| Autorités et mécanisme de signature | C19 | Décision de confiance avant signature/publication ; aucun secret dans les documents |

Les arbitrages PA/PZT qui affectent réellement sécurité, périmètre, compatibilité, exploitation ou ressources suivent la méthode de TECHNICAL §45.4 : conséquences et recommandation, regroupement par lots de trois ; absence de réponse non assimilée à validation. Aucun arbitrage absent ne bloque la rédaction des propositions, mais il bloque la réalisation concernée.

## Applicabilité PZT/DNS

Voir `applicabilite-pzt-dns.md` pour la correspondance exhaustive des exigences actuelles. Les statuts décrivent l’applicabilité au profil, jamais un test réussi. Une clause de gestion obligatoire dans un contrat principalement exécutant reste applicable à cette gestion ; le classement par titre ne peut pas la supprimer.

Si une revue détaillée révèle une obligation d’exécution PA non conditionnelle indispensable au profil, sa dépendance rejoint le chemin critique avant qualification. Le plan doit alors être amendé explicitement ; le profil ne sera pas publié avec une exemption supposée.

## Ordre de préparation et de réalisation future

Préparer C00 puis C01–C19 selon les dépendances de l’inventaire. Les tâches restent non cochées. C07 fournit un hôte intermédiaire avec refus de readiness si un élément essentiel manque ; C14 termine l’intégration des modules essentiels ; C18 construit l’artefact avant C17, et C19 vérifie son identité de distribution avant publication explicitement autorisée.

## Risques et mesures

- Confondre création de dossiers et autorisation de codage : périmètre documentaire rappelé dans chaque proposition et conception.
- Confondre réseau désactivé et module absent : scénario négatif explicite de composition.
- Déduire une conformité d’un titre, d’une archive ou d’un acquittement : preuves réelles demandées par C17 et contrôles de portée maintenus.
- Choix techniques non décidés : barrières de conception nommées dans leurs dossiers ; aucune valeur arbitraire ni dépendance installée.

## Migration et retour

C00 ne migre aucune donnée ni configuration. Les deltas ne sont pas synchronisés dans le canon pendant cette préparation. Leur adoption et toute réalisation ultérieure doivent être demandées séparément ; aucun archivage anticipé.

## Approfondissement issu de l’audit du 17 octobre 2026

Conception proposée sans implémentation. Ces contrats de travail ne modifient pas le canon ; tout changement normatif requiert son delta approuvé.

Constituer un registre de décisions du profil : identifiant stable, état canonique, contexte, alternatives, conséquences, exigences affectées, auteur de validation et réévaluation pertinente. Une fiche remplacée pointe vers sa remplaçante ; les instantanés des preuves restent datés.

Le manifeste documentaire du profil relie release, plateformes, capacités et surfaces sélectionnées, contrats obligatoires, budgets/objectifs déclarés et exclusions motivées. Chaque garantie publiée doit renvoyer à une preuve de C17 ou O31 pour cette même version et charge ; le silence sur un objectif n’invente pas de seuil.

N01 rejoint le chemin du premier P0 pour la réponse d’urgence. N02 prépare la clarification des profils natifs hors ligne, sans sélectionner ces options pour P0. Les providers concrets, seuils, support et autorités de confiance restent des décisions à soumettre avant leur réalisation ; une décision contraire au canon exige un delta approuvé.

### Exigences auditées et preuves de sortie futures

| Référence canonique | Statut statique après audit | Critère à démontrer |
|---|---|---|
| [architecture-decisions #1](../../../openspec/specs/architecture-decisions/spec.md#L10) | P | Fiche par décision arrêtée : identifiant, contexte, alternatives, conséquences, sources et revue si pertinente. |
| [architecture-decisions #2](../../../openspec/specs/architecture-decisions/spec.md#L22) | P | Décision contradictoire bloquée ou liée à un delta approuvé avant adoption. |
| [architecture-decisions #3](../../../openspec/specs/architecture-decisions/spec.md#L33) | P | PROPOSED/ACCEPTED/SUPERSEDED/REJECTED et lien vers le successeur ; historique conservé. |
| [performance #1](../../../openspec/specs/performance/spec.md#L8) | P | Référence initiale, protocole et signal observé conservés avant justification d’une optimisation. |
| [performance #2](../../../openspec/specs/performance/spec.md#L17) | ND | Budgets par surface/profil, seuils déclarés avant mesure, dépassement reproductible signalé. |
| [performance #3](../../../openspec/specs/performance/spec.md#L26) | P | Release/profil, matériel, surface, charge, méthode et validité associés ; hors profil informatif. |
| [performance #4](../../../openspec/specs/performance/spec.md#L38) | P | Aucune suppression d’isolation, d’échec fermé ou d’audit dans le chemin optimisé. |
| [performance #5](../../../openspec/specs/performance/spec.md#L47) | ND | Perte/péremption et repli source observés sans résultat erroné ou obsolète déclaré courant. |
| [service-objectives #1](../../../openspec/specs/service-objectives/spec.md#L10) | P | Objectif lié à version/périmètre/seuil/méthode/période, valeur non inventée par test local. |
| [service-objectives #2](../../../openspec/specs/service-objectives/spec.md#L21) | P | Rapport hors profil informatif ; aucune extrapolation d’un résultat ou d’une borne PZT à tout Pixs. |
| [service-objectives #3](../../../openspec/specs/service-objectives/spec.md#L32) | ND | Campagne synthétique avec versions/charge/méthode, mesure/seuil/écart ; insatisfaction explicitement remontée. |

Voir [audit individuel et limites des preuves](../define-first-installable-pbo-profile/audit-ne-94.json) et [rapport d’audit](../../../reports/audit-ne-94-2026-10-17/RAPPORT.md). Les tâches de réalisation restent non cochées.
