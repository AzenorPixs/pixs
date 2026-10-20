# Conception — C19

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 a été adopté et archivé le 18 octobre 2026 ; ses précisions normatives sont intégrées au canon. Les arbitrages propres au présent change restent à lever avant réalisation.

## État actuel vérifié

Constat : Le dépôt ne déclare pas de release ou paquet utilisable publié ; une recette de sources ne prouve pas une identité de distribution installable.

Sources consultées et empreintes recoupées avec la matrice :

- [README.md](../../../README.md).
- [openspec/specs/artifact-publication/spec.md](../../specs/artifact-publication/spec.md).
- [openspec/specs/release-management/spec.md](../../specs/release-management/spec.md).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Associer canal expérimental local, version, provenance, inventaire, composition et artefact immuable. Consommer les vérificateurs et matériaux publics de confiance fournis en amont par N03 ; vérifier les résultats liés aux octets qualifiés sans attendre C19 pour rendre les contrôles disponibles. Déclarer support/limites et corréler la recette C17 au paquet C18. Publication seulement sur instruction explicite ultérieure.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Les identités/autorités et mécanismes de confiance sont arrêtés en amont via N03 ; C19 consolide version/support et décision finale de publication sans modifier implicitement l’identité qualifiée. Aucun secret, signature ou publication pendant la préparation.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [qualify-first-pbo-composition](../qualify-first-pbo-composition/proposal.md).
- [build-first-pbo-pfo-debian-package](../build-first-pbo-pfo-debian-package/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Installation du paquet final depuis environnement vierge ; empreinte/signature invalide ou révoquée rejetée ; canal non autorisé refusé ; provenance et inventaire vérifiables ; aucun secret embarqué ; version/support et preuve finale corrélés.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.

## Dépendances après audit transversal P0

[C17](../qualify-first-pbo-composition/proposal.md), [C18](../build-first-pbo-pfo-debian-package/proposal.md), [N03](../archive/2026-10-20-add-p0-artifact-trust-and-preinstallation-verification/proposal.md).

Les conditions d’activation et la construction des résultats sont séparées de cet ordre de préparation ; aucun cycle inverse vers la recette finale.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

### T01 — Confiance avant première installation

C19 réalise tardivement les vérifications nécessaires avant installation par C17. N03 dédié validé ; déplacer les contrats/vérificateurs précoces, conserver publication finale C19.

Contrôles à intégrer : Canal interdit et signature absente/expirée/révoquée refusés avant installation ; Révocation vérifiable publication indisponible ; Paquet qualifié immuable et révalidation si octets ou identité changent.

### T13 — Première livraison et origines de mise à niveau

Une première version n’a pas nécessairement d’origine distribuée supportée ; un numéro source ancien ne prouve pas une migration autorisée. Déclarer les origines réellement supportées dans C16/C19 ; cas sans origine explicite et sauts non prouvés refusés.

Contrôles à intégrer : Installation vierge distincte d’une mise à niveau ; Interruption de migration et contraction prématurée refusées ; Retour arrière seulement si matrice accepte schéma/données ; Aucun downgrade automatique.

### T17 — Reproductibilité, versions et dossier de livraison

Les pins observés et unités vertes ne valent pas qualification officielle du graphe ou du paquet ; signatures finales ne doivent pas modifier l’objet déjà qualifié. Contrôles officiels/compatibilité avant build puis sur l’artefact final ; aucune version actualisée ou dépendance installée pendant l’audit.

Contrôles à intégrer : Deux builds contrôlés et graphe identique ; Identité de l’artefact de recette égale à celle livrée ; Budgets/support déclarés avec preuves et limites ; Strict global exit réel conservé, warnings non masqués.

Voir [audit transversal durable](../archive/2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.
