# Plan de qualification runtime — N02

Date : 21 octobre 2026.

Statut : plan préparé ; plateformes, mécanismes et paramètres à sélectionner ; aucune recette runtime exécutée.

## 1. Objectif et portée

Qualifier la frontière entre credentials natifs protégés et données hors ligne pour un profil de client effectivement sélectionné. N02 est adopté et synchronisé au canon. Le présent plan organise les preuves attendues sans ajouter d’exigence fonctionnelle, choisir de bibliothèque ni déclarer de plateforme supportée.

La qualification porte sur la séparation du coffre, le refus de repli non protégé, les sauvegardes et exports, les données interdites, l’isolation et la réévaluation serveur à la reconnexion. O23 porte le client et son mécanisme de plateforme ; O17 porte les projections ; O18 porte les intentions et leur réconciliation. Les parcours de notification ou de lien profond ne sont examinés que s’ils consomment cette frontière dans le profil retenu.

L’exécution, les compléments de code nécessaires et l’installation éventuelle de dépendances nécessitent leur mandat propre. Ce plan ne lance aucun service, ne manipule aucun coffre ou credential réel et n’engage ni Git, archivage ni publication. Les tâches runtime N02 4 et 5 restent ouvertes.

## 2. Références et traçabilité

Les codes ci-dessous servent uniquement à repérer les exigences dans ce plan.

| Référence | Exigence canonique | Responsabilité de qualification |
|---|---|---|
| NC-S | [native-clients — Session et stockage local sécurisés](../../specs/native-clients/spec.md) | O23 : coffre déclaré, séparation et refus du repli. |
| NC-O | [native-clients — Offline-first et révocation cohérents](../../specs/native-clients/spec.md) | O23 avec O17/O18 : effets locaux provisoires, révocation et reconnexion. |
| NC-A | [native-clients — Contrats publics et SDK compatibles](../../specs/native-clients/spec.md) | O23 et, si retenu, O21 : versions et interfaces publiques du client. |
| OF-E | [offline-first — Éligibilité déclarée et projections non autoritatives](../../specs/offline-first/spec.md) | O17 : ressources et champs sélectionnés, sans autorité locale. |
| OF-I | [offline-first — Intentions provisoires réévaluées au serveur](../../specs/offline-first/spec.md) | O18 : identité, droits, gouvernance, concurrence et idempotence au serveur. |
| OF-C | [offline-first — Conflits, révocation et purge locale](../../specs/offline-first/spec.md) | N02 et O17/O18/O23 : coffre séparé, données restreintes interdites, invalidation et purge. |

Les scénarios canoniques « Sauvegarde d’application », « Mécanisme sécurisé indisponible », « Révocation purgeant le local », « Coffre natif séparé de la réplique » et « Donnée restreinte hors réplique refusée » restent les références de sortie. Les scénarios de reconnexion et de refus d’une intention complètent leur preuve dans le profil combiné.

Sources complémentaires : [conception N02](design.md), [tâches N02](tasks.md), [conception O17](../add-offline-eligible-local-projections/design.md), [conception O18](../add-offline-intents-and-server-reconciliation/design.md), [conception O23](../add-native-client-contract-and-session-support/design.md), [authentification](../../specs/authentication/spec.md), [contrats API](../../specs/api/spec.md), [gouvernance](../../specs/data-governance/spec.md), [tests et preuves](../../specs/testing/spec.md), [PROJECT §2.45](../../../PROJECT.md), [TECHNICAL — offline-first](../../../TECHNICAL.md) et [BUILD — conformité offline/native](../../../BUILD.md).

## 3. Prérequis et points d’entrée

| Prérequis | État ou preuve nécessaire avant la recette concernée |
|---|---|
| Référentiel N02 | Adoption acquise ; relever les versions et empreintes des exigences utilisées par le dossier de recette. |
| Profil sélectionné | Identifier le client, son mode connecté ou natif/hors ligne, les ressources, champs, opérations et capacités retenus. Une préparation documentaire ne sélectionne pas O17/O18/O23 dans P0. |
| Plateforme et coffre | Fixer OS, version, architecture, type de session, mécanisme sécurisé, adapter, bibliothèques et règles d’accès. Décrire les garanties réelles et les limites du mécanisme. |
| Stockages locaux | Identifier coffre, projections, caches, index, files, fichiers temporaires, sauvegardes et exports ; déclarer propriétaires, isolation et chemins de persistance du banc. |
| Gouvernance et cycle de vie | Déclarer classifications admissibles, rétention, purge, événements d’invalidation et comportement hors ligne. `RESTRICTED` reste interdit localement, y compris hors réplique ou dans un stockage chiffré ; `SENSITIVE_PERSONAL` reste refusé par défaut. |
| Sessions et délais | Réutiliser les contrats Auth applicables ; fixer les durées, expirations, limites de fraîcheur et éventuels baux déjà prévus par le profil. Aucun délai de purge ou de révocation n’est inventé par ce plan. |
| Dépendances intégrées | Disposer des interfaces publiques Auth, autorisation, API, gouvernance et propriétaires de données nécessaires. Leurs preuves locales ne qualifient pas à elles seules leur assemblage avec le client. |
| Banc isolé | Prévoir comptes et données synthétiques, au moins deux utilisateurs et deux tenants/scopes avec une matrice explicite d’accès autorisés et refusés, coupure réseau, redémarrage, coffre verrouillé ou inaccessible, et sauvegarde/restauration contrôlée. |
| Méthode d’observation | Définir avant exécution les états attendus, points de contrôle, bornes contractuelles et moyens de détecter une fuite ou un effet confirmé. Une propriété non observable reste non démontrée. |
| Autorisation d’exécution | Délimiter les environnements, accès et perturbations autorisés. Tout outil ou dépendance supplémentaire suit la validation applicable avant installation. |

Les inspections de stockage utilisent des marqueurs publics inertes. Les justificatifs éventuels du banc restent confinés à l’exécuteur et à leur transport protégé ; leurs valeurs ne figurent ni dans les rapports ni dans le contexte des agents. Aucune donnée ou credential de production n’est requis.

## 4. Matrice des plateformes à sélectionner

Toutes les lignes ci-dessous sont des candidates de recette, sans sélection ni qualification acquise. Les versions et architectures exactes sont à fixer avant exécution.

| Famille | Place proposée dans la campagne | Preuves spécifiques attendues |
|---|---|---|
| Desktop Linux, candidat Debian 13 | Premier banc possible, en cohérence avec l’environnement de développement décrit par DEVOPS. L’existence d’une session graphique et d’un coffre reste à vérifier. | Adapter réellement utilisé, identité de session, contrôle d’accès au coffre, verrouillage, persistance et sauvegarde. |
| Desktop Windows | Campagne conditionnelle à la sélection d’un client Windows en O23. | Garanties du mécanisme déclaré, isolation des utilisateurs, profils de session et comportement après redémarrage. |
| Desktop macOS | Campagne conditionnelle à la sélection d’un client macOS en O23. | Garanties du mécanisme déclaré, contrôle d’accès du client, verrouillage et règles de sauvegarde/reprise. |
| Android | Campagne conditionnelle à une cible mobile sélectionnée. | Mécanisme déclaré, cycle de vie de l’application, verrouillage, sauvegarde/restauration et persistance hors ligne. |
| iOS | Campagne conditionnelle à une cible mobile sélectionnée. | Mécanisme déclaré, cycle de vie de l’application, verrouillage, sauvegarde/restauration et persistance hors ligne. |
| Frontend web, si présent dans le profil | Contrôle de non-régression de la frontière navigateur ; l’exception du coffre natif ne lui est pas transférée. | Absence de jeton persistant accessible au JavaScript par défaut ; contrôles dans Chromium et Firefox déclarés par DEVOPS, en headless lorsque applicable. |

La preuve identifie le matériel ou la virtualisation, les mécanismes disponibles et leurs limites. Une VM, un émulateur ou un double de coffre ne qualifie que son propre périmètre ; son résultat ne vaut pas automatiquement pour un appareil physique ou une autre version du système. Docker, LXC et les binaires PA/PZT ne sont pas assimilés aux clients natifs O23.

Le verdict est attaché au couple client/plateforme, au mécanisme, à l’adapter, aux versions et à la configuration testés. Le développement sous Debian ne démontre pas le support des autres lignes.

## 5. Scénarios et critères d’acceptation

Chaque ligne produit des observations avant/après et une référence de preuve sans valeur sensible. Tous les scénarios du profil combiné sont exécutés avec un coffre réel de la plateforme et les dépendances intégrées ; les doubles servent aux contrôles préparatoires et à l’injection de pannes.

| ID | Scénario et méthode | Critère d’acceptation | Références |
|---|---|---|---|
| Q01 | Utiliser un credential de banc via l’interface publique du client et le mécanisme sécurisé sélectionné, puis redémarrer selon le profil déclaré. | Le credential est utilisable seulement dans son contexte autorisé ; sa persistance suit le coffre, sans fichier, base ou copie durable non protégés. Aucune autorité métier ne découle de sa présence. | NC-S, NC-A |
| Q02 | Faire fonctionner projections, caches, index et files avec des marqueurs synthétiques distincts ; examiner les contenus persistés et exportés. | Aucun secret, jeton ou credential n’est copié dans ces contenus. Le stockage et les droits du coffre restent séparés. L’usage du credential dans le transport d’authentification déclaré ne le transforme pas en donnée répliquée. | NC-S, OF-C |
| Q03 | Préparer une intention hors ligne et provoquer des erreurs ou refus ; examiner intention, diagnostic, journal et rapport du banc. | Aucun credential, secret ou preuve brute n’est incorporé dans l’intention ou les traces. Les erreurs sont explicites et corrélables sans contenu sensible. | OF-I, OF-C, NC-S |
| Q04 | Rendre le mécanisme de coffre absent, verrouillé, inaccessible ou non vérifiable, selon les cas du profil. | L’opération nécessitant le credential est refusée ; aucun repli vers fichier, stockage ordinaire ou base hors ligne. Un état d’échec n’est pas présenté comme une authentification réussie. | NC-S |
| Q05 | Exécuter séparément Q05a (extraction technique du banc), Q05b (export métier conditionnel ou refus attendu) et Q05c (sauvegarde ordinaire et restauration), selon les modalités ci-dessous. | Chaque sous-cas reçoit sa preuve et son résultat. Aucun contenu extrait, exporté ou sauvegardé ne copie le coffre ou ses credentials ; un export métier non sélectionné ou non autorisé reste refusé ou indisponible selon son contrat. | NC-S, OF-C, OF-E |
| Q06 | Tenter de stocker une ressource synthétique classée `RESTRICTED` dans réplique, cache, index, file, fichier externe, stockage chiffré et coffre. | La persistance locale de cette donnée est refusée dans chaque cas. L’exception du coffre porte sur les credentials natifs, pas sur les données restreintes. Les autres classifications conservent leurs politiques déclarées. | OF-C |
| Q07 | Demander une ressource ou une opération non éligible hors ligne ; vérifier aussi les champs autorisés d’une projection éligible. | La ressource ou opération non éligible reste indisponible, sans réplication implicite. Une projection autorisée reste versionnée, bornée et non autoritative. | OF-E |
| Q08 | Changer utilisateur, tenant ou scope, puis tenter de relire la projection, reprendre une intention ou utiliser le credential du contexte précédent. | Les contrôles du profil empêchent toute réutilisation hors périmètre ; invalidation ou purge suivent le cycle déclaré. Un compte ordinaire ne bénéficie pas de l’exception Super Admin. | NC-S, NC-O, OF-C |
| Q09 | Créer une intention hors ligne, reconnecter le client, puis soumettre et rejouer la même intention. | Le client montre un état provisoire avant la réponse autoritative. Le backend réévalue identité, périmètre, droits et gouvernance ; une confirmation correspond à un résultat propriétaire prouvé, sans double effet au rejeu. | OF-I, NC-O |
| Q10 | Révoquer ou laisser expirer l’accès pendant une déconnexion ; reconnecter et soumettre une ancienne intention. | Le coffre ne prolonge pas le droit ; le serveur refuse l’accès non valide avant effet métier. Les données et intentions sont invalidées ou purgées selon les événements et bornes du profil. Aucun effacement distant instantané n’est revendiqué sans moyen de l’observer. | NC-O, OF-I, OF-C |
| Q11 | Modifier au serveur la version, le périmètre ou les droits d’une ressource avant reconnexion ; inclure les contrôles de quota applicables au profil. | La décision courante prévaut ; le conflit ou refus est explicite. Aucune fusion silencieuse, ancienne permission ou réservation locale n’est présentée comme acquise. | OF-I, OF-C |
| Q12 | Interrompre puis redémarrer le client ; restaurer un ancien état local sur le banc selon le plan autorisé. | La séparation du coffre est conservée ; états provisoires, expirations et tombstones applicables sont réévalués. Une issue inconnue est réconciliée avant rejeu, sans résurrection de droit ni double effet confirmé. | NC-O, OF-I, OF-C |
| Q13 | Si une façade web appartient au profil, effectuer connexion, déconnexion, changement de périmètre et usage hors ligne déclaré dans les navigateurs retenus. | Aucune persistance de jeton accessible au JavaScript par défaut ; aucun accès au coffre natif par substitution de profil. Les scénarios web ne valent pas recette d’un mécanisme natif. | NC-S, NC-O ; contrats API applicables |

### Q05 — Extraction technique, export métier et sauvegarde

| Sous-cas | Méthode et applicabilité | Critère d’acceptation |
|---|---|---|
| Q05a | Extraire, dans le banc autorisé, les seules données synthétiques de la réplique nécessaires à l’inspection. Cette opération technique du banc ne constitue pas une fonction d’export métier du client et n’en impose aucune. | L’extraction permet de vérifier l’absence de coffre et de credentials dans les données hors ligne, sans lire ou copier le contenu du coffre ni confirmer un droit ou un effet métier. Sa réussite ne prouve pas la disponibilité d’un export applicatif. |
| Q05b | Si un export métier hors ligne est explicitement déclaré, sélectionné et autorisé pour le profil, l’exercer selon son contrat. Sinon, vérifier son refus ou son indisponibilité explicite à la frontière existante du client. Les exports métier restent désactivés hors ligne par défaut. | Le cas sélectionné et autorisé respecte périmètre, gouvernance et absence de credentials dans le résultat. Dans les autres cas, le refus ou l’indisponibilité prévu par le contrat est le résultat réussi attendu ; aucune fonction d’export n’est ajoutée pour satisfaire la recette. |
| Q05c | Déclarer le mécanisme et le périmètre de sauvegarde ordinaire du client, puis effectuer cette sauvegarde et sa restauration sur le banc autorisé, indépendamment de la sélection d’un export métier. | La sauvegarde hors ligne ne copie pas le coffre ou ses credentials. La restauration ne fabrique ni nouvelle session ni droit. Un mécanisme distinct de reprise du coffre reste déclaré et qualifié dans son propre périmètre. |

Les preuves et statuts Q05a, Q05b et Q05c sont consignés séparément. L’absence d’export métier sélectionné ne rend pas Q05 non applicable : Q05b vérifie le refus ou l’indisponibilité attendu, tandis que l’extraction technique et la sauvegarde restent à vérifier. Un refus attendu réussi ne vaut pas qualification d’un export autorisé. Une sauvegarde ou une inspection indisponible ne reçoit pas de résultat réussi par substitution du refus d’export.

Q02, Q04, Q05 et Q06 couvrent directement les nouveaux scénarios et la sauvegarde protégée de N02. Q08 et Q10 couvrent la purge sur révocation ; Q09 à Q12 prouvent les limites d’autorité locale et la réconciliation dans le profil combiné.

Une révocation distante sur un appareil déconnecté ne prouve pas une purge immédiate. La recette mesure séparément l’invalidation connue du client, l’expiration locale applicable, la purge observée et le refus serveur à la reconnexion. Elle ne promet pas l’effacement d’un support inaccessible, l’absence de secret en mémoire pendant sa consommation ni une protection contre un hôte compromis au-delà des garanties déclarées du mécanisme.

## 6. Déroulement et décisions de passage

1. **Fixer le profil.** Sélectionner plateformes, versions, mécanismes, ressources et paramètres. Définir la matrice d’applicabilité Q01–Q13, les méthodes d’observation et les bornes issues des contrats. Relever les dépendances non encore disponibles.
2. **Contrôler la frontière isolée.** Vérifier séparation, contenus persistés, sauvegardes et refus avec fixtures et injection de pannes. Ce passage prépare les recettes ; il ne qualifie pas un coffre réel à partir d’un double.
3. **Qualifier chaque mécanisme réel.** Exécuter les scénarios applicables sur la plateforme sélectionnée avec l’adapter réellement utilisé et les politiques retenues.
4. **Qualifier l’assemblage.** Exécuter les parcours combinés O17/O18/O23 contre les propriétaires backend et la persistance réelle du profil, avec perte réseau, changement de contexte et reprise.
5. **Vérifier l’artefact installé.** Rejouer les contrôles applicables sur le client et la configuration effectivement distribuables. Relier leurs empreintes aux preuves et aux versions du backend.
6. **Prononcer un verdict borné.** Déclarer les plateformes et scénarios qualifiés, les échecs et les limites. Aucun résultat n’est étendu à une autre plateforme, à P0 ou à l’ensemble d’O17/O18/O23 par cette seule recette N02.

Un profil seulement connecté peut produire une preuve partielle de NC-S. Il ne permet pas de déclarer la frontière natif/hors ligne intégralement qualifiée en écartant les scénarios O17/O18. La recette combinée exige au moins un profil natif/hors ligne effectivement sélectionné et ses dépendances opérationnelles.

## 7. Preuves et verdict de qualification

Chaque résultat consigne : ID du scénario, référence canonique, profil, plateforme et architecture, versions du client/backend/adapter/mécanisme, empreinte de l’artefact, configuration pertinente sans secret, instant et fuseau, conditions injectées, résultat attendu, observation, référence de preuve et limite constatée. Les diagnostics utilisent des identifiants synthétiques et des constats minimisés ; ils ne recopient aucun justificatif.

Les statuts de recette sont : exécuté/réussi, exécuté/échoué, non exécuté, indisponible ou non applicable justifié. Ils ne créent aucun état runtime du produit. Une plateforme non sélectionnée ou une dépendance absente ne reçoit pas de résultat réussi.

La qualification d’un profil est acceptée lorsque tous ses scénarios applicables ont été exécutés et réussis, avec preuves reproductibles et dépendances réelles identifiées. Un scénario obligatoire échoué, indisponible ou non exécuté empêche ce verdict. Une exclusion précise son motif, son effet sur la revendication et le périmètre restant non qualifié.

Les conditions de sortie sont : séparation prouvée ; absence de fuite vers les données hors ligne ; refus de repli non protégé ; refus de stockage local des données restreintes ; extraction technique et sauvegarde conformes ; export métier sélectionné et autorisé conforme, sinon refus ou indisponibilité attendu vérifié ; isolation et révocation vérifiées ; absence de confirmation métier locale et de double effet au rejeu ; traçabilité complète vers l’artefact testé.

La préparation et la validation documentaire de ce plan ne cochent aucune tâche runtime. N02 reste actif jusqu’à production et examen des preuves des tâches 4 et 5 ; aucune opération Git, archivage ou publication n’est déclenchée.
