# Conception — N02

## Décision adoptée et synchronisée

La séparation du coffre natif et des données hors ligne est préparée le 17 octobre 2026, puis adoptée et synchronisée le 21 octobre 2026 dans `offline-first` et `native-clients`. L’alternative interdisant toute persistance de credential en profil hors ligne n’est pas retenue. Les deux exigences modifiées et les trois scénarios ajoutés sont intégrés au canon ; les deltas conservés tracent cette adoption sans double application.

## Frontières

Le mécanisme sécurisé déclaré de la plateforme est propriétaire des credentials. Les projections, caches, index locaux et files d’intentions ne reçoivent aucun secret, jeton ou donnée restreinte. Leur export, sauvegarde ou synchronisation ne copie pas le contenu du coffre. Une référence opaque éventuelle n’est pas un credential ni une permission ; elle ne doit pas suffire à accéder au coffre.

Le client utilise le credential pour l’authentification conforme à C03 ; il ne l’insère pas dans une intention différée, un journal ou un payload de synchronisation. Le stockage protégé ne valide pas une opération hors ligne et ne prolonge aucune session ou permission révoquée.

Si le mécanisme sécurisé ne peut être vérifié ou utilisé, aucun repli vers fichier, stockage ordinaire ou copie dans la base locale hors ligne. Le résultat reste un refus explicite. Le choix des adapters, bibliothèques et plateformes et leur qualification restent à traiter en O23.

## Dépendances conditionnelles

Les profils combinant clients natifs et offline-first doivent appliquer la frontière canonique N02 dans les contrats documentaires O17/O18/O23, alignés le 21 octobre 2026. L’adoption est acquise ; les mécanismes de plateforme et leurs preuves restent à qualifier avant réalisation. Un client en ligne ne reçoit pas automatiquement un mode hors ligne ; un frontend web ne reçoit pas une autorisation de persister des jetons dans son stockage local.

## Préservation du canon

Les scénarios existants de sauvegarde protégée et de purge sur révocation sont conservés. L’interdiction de stockage local des données restreintes demeure, y compris hors réplique ; le chiffrement ou un fichier extérieur ne la lève pas. Seule la frontière des credentials natifs protégés est précisée par la décision validée.

## Recette future

Fixtures synthétiques de coffre et de base locale séparées ; vérification des exports et sauvegardes ; refus lorsque le coffre est indisponible ; absence de secret dans intentions et logs ; révocation/reconnexion ; aucun effet métier confirmé sans backend. Ces recettes runtime ne sont pas exécutées par l’adoption documentaire ; les tâches de qualification restent ouvertes et le dossier reste actif, sans archivage.

## Vérifications documentaires du 21 octobre 2026

OpenSpec 1.14.3, avec télémétrie désactivée, valide `validate --all --strict --no-interactive --json --report findings` avec code de sortie 0 : 190 éléments sur 190, soit 112 changes actifs et 78 capacités, sans erreur ni avertissement. Les deux blocs N02 sont identiques entre deltas et canon ; les scénarios existants sont préservés et trois scénarios sont ajoutés. Le canon compte 831 exigences et 986 scénarios ; PROJECT et README reprennent ces totaux.

Les six interdictions identifiées dans Bulk, observabilité, PA et PZT utilisent `MUST NOT`, sans modification des scénarios ni du comportement attendu. Les cadrages distinguent l’interdiction de stockage local de `RESTRICTED` du refus par défaut de `SENSITIVE_PERSONAL` ; l’exception du coffre natif ne permet pas de stocker une donnée `RESTRICTED`.

Les contrôles documentaires réussissent sur les 19 fichiers Markdown modifiés : UTF-8/LF, fin de fichier, absence d’espaces finaux et de marqueurs de conflit. Les liens locaux des 555 documents de cadrage, de spécification et de changes actifs contrôlés existent. Les empreintes des 180 autres groupes documentaires suivis restent inchangées ; aucun fichier de code n’est modifié. Les trois tâches documentaires N02 sont cochées ; les qualifications, l’archivage et la publication restent ouverts. Aucun test applicatif, build, recette de coffre, opération Git ou archivage n’est exécuté par cette adoption.
