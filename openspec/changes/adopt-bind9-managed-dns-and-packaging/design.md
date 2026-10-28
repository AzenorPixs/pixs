# Conception — sélection BIND 9

## État et autorisation

SPÉCIFICATION_VALIDÉE — CHANGE_OUVERT. Le développeur a validé le 24 octobre 2026 la spécification présentée et autorisé l'ouverture du change, sans implémentation ni production de code. Le choix BIND 9/Debian/Docker et son pilotage par PA sont conservés ; installation, configuration et activation restent ultérieures.

Les trois exigences validées et leurs neuf scénarios sont synchronisés au canon le 24 octobre 2026, sur autorisation explicite de synchronisation et de mise à jour des renvois, sans implémentation ni production de code. Les cadrages partagés restent inchangés ; les références des lots propriétaires sont mises à jour. Aucune tâche de réalisation DNS n'est cochée et aucune qualification fonctionnelle n'est déduite de cette adoption.

## Frontières de responsabilité

| Propriétaire | Responsabilité |
|---|---|
| PBO / pixs.dns | Gestion des configurations souhaitées, zones, noms, vues et politiques par contrats publics ; conservation des révisions, droits et obligations applicables |
| PA désigné | Installation du paquet, préparation et application de configuration, inspection et lifecycle autorisés ; preuves réelles et rapprochement des issues incertaines |
| BIND 9 | Processus serveur DNS distinct de Django ; fonctionnement selon la configuration effectivement appliquée |
| PZT | Transport et identité selon les contrats sélectionnés ; aucun canal PBO–PA de substitution |
| Distribution | Version des paquets, dépendances et artefacts Debian/Docker identifiables, reproductibles et qualifiés |

Les vues BIND ne sont pas des identités Pixs. Leur correspondance avec les sujets, périmètres et droits doit être construite et qualifiée dans Z05 ; aucun tenant, libellé, IP ou certificat isolé ne confère un droit applicatif.

## Debian

Sur une cible Debian où le rôle serveur DNS est sélectionné et admis, le PA désigné installe BIND 9 depuis les paquets de la distribution prise en charge, puis applique les seuls changements autorisés.

Le paquet bind9 fournit le serveur ; la version exacte, les dépendances et outils doivent être relevés et qualifiés avec la cible. Aucune version issue d'une recherche web ni d'une fixture n'est une version de production adoptée. Un nouveau paquet ou une mise à niveau reste soumis au plan, aux contrôles, à la reprise et à l'autorisation applicables.

Le paquet PBO ne transforme pas le serveur DNS en code Django et ne donne pas à un PA client le rôle serveur. Le nom exact des services, comptes, fichiers et mécanismes de contrôle doit être vérifié sur la version retenue.

## Docker Pixs

BIND 9 est fourni dans l'image Pixs, au même titre qu'un logiciel disponible pour un rôle explicitement sélectionné. Sa présence ne prouve ni service lancé, ni zone appliquée, ni port accessible.

L'image ne contient aucun état d'instance DNS, journal mutable, clé privée ou secret. La recette inspectera également les effets des scripts d'installation du paquet et les couches de l'image. La configuration d'instance, les données persistantes et les références de secrets suivent les propriétaires et plans de stockage déjà requis par le profil.

Le PA reste responsable de l'application et de la supervision du service distinct dans le conteneur. Aucun systemd hôte, montage, privilège, utilisateur ou port supplémentaire n'est supposé ou modifié par ce document.

## Contrats et état observable

Le raccord consomme les contrats publics C14 et PA/PZT. Il ne réécrit pas les données privées de pixs.dns depuis le PA. Les configurations générées, leur révision et leur lien au plan doivent être traçables ; les états souhaité, appliqué, observé et disponible restent distincts.

Les validations de configuration et de zones précèdent une application autorisée. Les outils named-checkconf et named-checkzone peuvent contribuer aux contrôles de la version retenue ; une syntaxe correcte ne prouve ni autorisation, ni absence de fuite, ni application, ni disponibilité.

Une réponse perdue, un crash, une application partielle ou une reprise ne produit pas une nouvelle exécution aveugle. Le résultat est inspecté et rapproché sous identité, droits, mandat et version courants. L'arrêt ou le retrait ne réactive pas une ancienne zone, clé, permission ou configuration.

Les exceptions applicatives Super Admin restent celles du canon ; elles ne fabriquent aucun audit, contrôle, mesure, preuve d'application ou capacité technique absent.

## Garanties héritées

A06c–A06k restent applicables : service distinct, PA ordinaires clients, vues et droits séparés, DoT, TTL/cache, sélection/secours, suffixe explicite, nommage, retraits, alias et contrôle de l'identité de destination. Aucun DNS public ne devient un secours des noms privés et aucune dépendance circulaire au DNS privé n'est introduite à l'amorçage.

Le choix BIND 9 ne choisit pas à lui seul topologie, redondance, placement des serveurs, version, ports, profils TLS, comptes, chemins, backend de secrets ou ressources. Les choix déjà acquis ne sont pas rouverts ; les paramètres réellement ouverts sont soumis avant leur réalisation.

## Répartition avec les dossiers existants

- [C14](../archive/2026-10-23-add-essential-pbo-pzt-and-dns-modules/proposal.md) : gestion PZT/DNS sans service DNS actif sélectionné.
- [Z05](../add-pzt-managed-dns-service-and-pa-adapters/proposal.md) : réalisation et qualification du service DNS et des adapters.
- [PA01](../add-pa-authorized-instruction-execution/proposal.md) : exécution autorisée des instructions.
- [PA10](../separate-pa-pzt-and-pbo-management-modules/proposal.md) : gestion PBO Agent séparée des exécutants.
- [Docker Pixs](../build-and-qualify-pixs-docker-image/proposal.md) : artefact et qualification de l'image.
- [Distribution PA](../build-and-publish-independent-pa-debian-package/proposal.md) : paquet PA/PZT indépendant.
- [Distribution PBO/PFO](../build-first-pbo-pfo-debian-package/proposal.md) : gestion DNS dans le paquet applicatif, sans activation ou installation universelle de BIND 9.

Une référence de dossier ne constitue aucune preuve de livraison de sa dépendance.

## Qualification future

La future recette distingue contrôle du paquet et de l'image, syntaxe et chargement des zones, processus réellement exécuté, droit d'administration, consultation autorisée, isolement des vues, retraits/révocations, absence de fuite et panne/reprise. Debian et Docker sont qualifiés séparément, avec versions, politiques et artefacts exacts.

Les mesures CPU/RAM et délais concernent uniquement le profil exécuté ; aucun gain ni budget nominal n'est inventé. Les fixtures ou l'absence du serveur ne qualifient pas BIND 9 actif.

## Références éditeur

- [Paquet Debian bind9](https://packages.debian.org/trixie/bind9).
- [Manuel ISC BIND 9](https://bind9.readthedocs.io/en/stable/).
- [Outils de contrôle ISC](https://bind9.readthedocs.io/en/stable/manpages.html).

Ces références documentent le logiciel ; seule la version effectivement retenue et éprouvée pourra porter une preuve de qualification.


## Matrice des qualifications futures et paramètres ouverts

| Objet | Propriétaire et cible | Preuves futures | Paramètres restant à arrêter ou qualifier |
|---|---|---|---|
| Installation Debian | PA désigné, rôle serveur admis ; Z05/PA09 | Paquet et dépendances identifiés, installation idempotente, droits et état réel après interruption | Version exacte, comptes, chemins, services, outils et ressources de la cible |
| Contenu PBO/PFO | C18 | Module de gestion présent, exécutants séparés ; présence PBO sans rôle serveur ne déclenche pas BIND 9 | Dépendances et identité de l'artefact selon le profil Debian |
| Configuration et application | Z05, contrats publics PBO/PA/PZT | Configuration et zones vérifiées avant application ; révision et plan corrélés ; souhaité/appliqué/observé distincts | Schémas des adapters, fichiers et mécanismes d'application qualifiés |
| Sécurité DNS | Z05, Debian et Docker séparément | DoT, vues et droits distincts, cache/TTL, suffixe et alias, retraits/révocations, absence de fuite et de repli public privé | Topologie, placement, serveurs, endpoints, certificats et politique courante |
| Image et données | X01, profil Docker déclaré | Version et image corrélées, toutes couches inspectées, configuration/état/secrets hors image | Dépendances verrouillées et plans de persistance, comptes et budgets réellement autorisés |
| Activation et exploitation | PA désigné et supervision du profil | Sélection explicite, effet et disponibilité réels ; arrêt, concurrence, crash, réponse perdue et reprise sans double effet | Séquencement, sondes et délais mesurés ; aucune valeur par défaut ajoutée |

Les prescriptions déjà adoptées A06c–A06k sont conservées. Les choix ouverts
de cette matrice ne sont pas résolus par un numéro de version, un port, un
montage, un privilège ou un budget inventé. Le propriétaire et l'environnement
réels doivent fournir la preuve ; aucun résultat de syntaxe, fixture ou
présence logicielle n'est une recette fonctionnelle de BIND 9.
