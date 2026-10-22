# Conception — N04 : Entrée web et frontière de service du P0

Préparation dédiée et rédaction des deltas proposées validées explicitement par le développeur le 17 octobre 2026. Le 20 octobre 2026, seules les deux clauses api liées aux décisions C03 sur le transport et le stockage navigateur sont adoptées au canon. Les clauses antérieures d’origines, limites/cache et référence d’entrée restent proposées ; aucune réalisation n’est autorisée.

## Écart démontré

C03 porte sessions/authentification ; C06 les Commands/API ; C07 la composition ; C11 le shell ; C18 les unités de services. Aucun de ces plans ne détaille l’assemblage HTTP distribué : serveur applicatif non destiné au développement, exposition du bundle PFO et liens profonds, chemin API/admin/santé, frontière privée des rôles/management et confiance des en-têtes d’un éventuel intermédiaire.

Le gabarit [settings.py](../../../src/pixs/backend/settings.py) est explicitement préparatoire ; [runtime_profiles.py](../../../src/pixs/backend/runtime_profiles.py) ne lance aucun rôle. Le [profil de test existant](../../../src/pixs/backend/README.md) n’est pas un service de production. BUILD §13 impose de définir le mécanisme de service avant le paquet ; TECHNICAL §25 décrit CORS/CSRF/cookies, limites et formats que les quatre exigences API canoniques ne détaillent pas entièrement.

## Préparation recommandée

Créer `define-p0-web-serving-and-security-boundary`. Déclarer le contrat d’entrée HTTP du profil local : surfaces publiques/protégées, hôtes/origines, mode de session/Bearer choisi par C03, service du bundle construit, navigation directe, refus des routes inconnues et séparation des rôles.

Décrire CORS refusé par défaut, CSRF lorsque cookies, absence de persistance navigateur des jetons par défaut, cache de réponses sensibles, limites requête/durée et diagnostic minimisé. Déclarer la confiance envers un intermédiaire et la terminaison de transport si ce profil en utilise ; ne pas autoriser une exposition réseau supplémentaire par la seule rédaction. Aucun serveur, reverse proxy, bibliothèque ou version n’est choisi ici.

## Responsabilités et deltas proposés

C03 reste propriétaire des identités/sessions ; C06 des opérations et schémas métier ; C07 du lifecycle ; C11 des contributions ; N04 du branchement et des frontières de service. C18 intègre l’assemblage dans le paquet et C17 le vérifie à travers le chemin réellement livré.

Prévoir un delta ciblé dans `reference-runtime` pour le profil d’entrée et dans `api` pour les garanties HTTP choisies du cadrage technique. Présenter les valeurs de configuration et choix de session/serveur avant leur implémentation ; aucun réglage nouveau inventé comme approuvé.

## Dépendances et critères futurs

Contrats C03/C06/C07/C11/C15 avant intégration N04 ; N04 avant C18/C17. Tests de navigation directe, erreur API stable sans page HTML de fallback, routes admin modifiées, origine/hôte/en-tête d’intermédiaire non fiable refusés, cookies/CSRF si retenus, travailleurs/management non exposés. Démarrage/arrêt et cache du bundle testés sur artefact installé, sans substituer Vite ou le serveur de test au service distribué.

## Transport de session sélectionné le 20 octobre 2026

D01 de la [conception C03](../archive/2026-10-21-add-initial-authentication-and-sessions/design.md) sélectionne une façade web explicitement déclarée, avec session serveur et cookie protégé inaccessible au JavaScript ; les mutations exigent CSRF selon les règles applicables. L’API standard conserve Authorization: Bearer et ses jetons opaques ; une route n’accepte pas implicitement un cookie comme substitut d’un Bearer. Les deux clauses de [transport et stockage navigateur du delta api](specs/api/spec.md) sont adoptées au canon le 20 octobre 2026 ; elles séparent les surfaces, sans serveur choisi ni exposition réseau supplémentaire.

Les noms/chemins, attributs complets du cookie, origines, transport sécurisé et règles d’ambiguïté doivent être spécifiés et qualifiés avant code. Le stockage de jetons persistants par JavaScript dans le navigateur reste exclu par défaut. La présence du cookie ne prouve ni session courante ni autorisation ; C03 vérifie l’état et C04 le périmètre. Le backend de sessions doit respecter le stockage serveur par empreinte retenu, sans reprise aveugle d’un backend conservant l’identifiant brut.

Le comportement de déconnexion/révocation suit D14 et le delta C05 adopté ; les autres activités protégées, dont lectures/navigation du panneau, conservent leurs obligations d’audit. Les exceptions Super Admin canoniques et les protections des frontières de confiance restent distinguées.

## Paramètres ouverts et frontière de sécurité

Le profil est local ; la préparation ne l’expose pas à Internet. Le mode de session est choisi par D01 : cookie côté web déclaré et Bearer pour l’API standard. Les noms/ports/hôtes, chemins définitifs, délais, tailles, attributs du cookie, transport et fournisseur de serveur restent à déclarer et qualifier avant code. Les références de secrets restent externes. Les règles d’accès s’appliquent sous réserve de l’exception Super Admin du canon ; cette exception n’authentifie pas un en-tête de proxy et ne transforme pas un fait absent en preuve.

## Portée de préparation et retour

Aucun code produit, secret, compte, service, dépendance, migration, données réelles, signature ou publication n’est manipulé par cette préparation. Les tâches restent futures et non cochées. Une évolution persistante ultérieure exige schéma/version, contrat de compatibilité et reprise/compensation revue ; aucun downgrade automatique ni purge implicite.

## Dépendances après audit transversal P0

[C03](../archive/2026-10-21-add-initial-authentication-and-sessions/proposal.md), [C06](../add-protected-core-http-commands-and-queries/proposal.md), [C07](../activate-reference-runtime-composition/proposal.md), [C11](../compose-modular-frontend-with-core-api/proposal.md), [C15](../add-runtime-observability-and-operations/proposal.md).

Les conditions d’activation et la construction des résultats sont séparées de cet ordre de préparation ; aucun cycle inverse vers la recette finale.
