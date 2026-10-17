# Conception — C03

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 formalise le profil ; ses précisions normatives restent proposées tant qu’elles ne sont pas approuvées/adoptées.

## État actuel vérifié

Constat : Le code expose des identités structurelles et mappings d’assurance ; il ne démontre pas une authentification de session réellement utilisable.

Sources consultées et empreintes recoupées avec la matrice :

- [src/pixs/core/identity/models.py](../../../src/pixs/core/identity/models.py).
- [src/pixs/core/authz/assurance_mapping.py](../../../src/pixs/core/authz/assurance_mapping.py).
- [src/pixs/backend/api/README.md](../../../src/pixs/backend/api/README.md).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Authentifier une DigitalIdentity par un provider explicitement approuvé, établir un contexte canonique et des sessions/jetons persistants bornés. Ne jamais rapprocher par courriel. L’authentification propre du Super Admin reste distincte de l’exemption de MFA ; le navigateur ne persiste pas de justificatif par défaut.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Provider initial, choix sessions/cookies/Bearer par façade, rotation/révocation et durées. Ces arbitrages modifient sécurité et contrats : revue avant réalisation, sans valeurs arbitraires.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [add-pbo-runtime-secret-provider](../add-pbo-runtime-secret-provider/proposal.md).
- [add-core-postgres-services](../add-core-postgres-services/proposal.md).

- [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md) : dépendance renforcée après revue des obligations d’audit.

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Connexion/déconnexion et révocation réelles ; jeton ou session expiré refusé ; aucune fusion par courriel ; aucun MFA fictif ni exigence MFA interdite au premier démarrage/secours.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.
