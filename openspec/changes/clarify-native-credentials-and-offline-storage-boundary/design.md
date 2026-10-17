# Conception — N02

## Décision validée pour préparation

Le développeur a choisi le 17 octobre 2026 : coffre natif séparé des données hors ligne. L’alternative interdisant toute persistance de credential en profil hors ligne n’est pas retenue pour ces deltas.

## Frontières

Le mécanisme sécurisé déclaré de la plateforme est propriétaire des credentials. Les projections, caches, index locaux et files d’intentions ne reçoivent aucun secret, jeton ou donnée restreinte. Leur export, sauvegarde ou synchronisation ne copie pas le contenu du coffre. Une référence opaque éventuelle n’est pas un credential ni une permission ; elle ne doit pas suffire à accéder au coffre.

Le client utilise le credential pour l’authentification conforme à C03 ; il ne l’insère pas dans une intention différée, un journal ou un payload de synchronisation. Le stockage protégé ne valide pas une opération hors ligne et ne prolonge aucune session ou permission révoquée.

Si le mécanisme sécurisé ne peut être vérifié ou utilisé, aucun repli vers fichier, stockage ordinaire ou copie dans la base locale hors ligne. Le résultat reste un refus explicite. Le choix des adapters, bibliothèques et plateformes et leur qualification restent à traiter en O23.

## Dépendances conditionnelles

Les profils combinant clients natifs et offline-first doivent utiliser les précisions approuvées de N02 dans O17/O18/O23. Un client en ligne ne reçoit pas automatiquement un mode hors ligne ; un frontend web ne reçoit pas une autorisation de persister des jetons dans son stockage local.

## Préservation du canon

Les scénarios existants de sauvegarde protégée et de purge sur révocation sont conservés. L’interdiction de stockage local des données restreintes demeure, y compris hors réplique ; le chiffrement ou un fichier extérieur ne la lève pas. Seule la frontière des credentials natifs protégés est précisée par la décision validée.

## Recette future

Fixtures synthétiques de coffre et de base locale séparées ; vérification des exports et sauvegardes ; refus lorsque le coffre est indisponible ; absence de secret dans intentions et logs ; révocation/reconnexion ; aucun effet métier confirmé sans backend. Aucun test sur credential réel pendant cette préparation.
