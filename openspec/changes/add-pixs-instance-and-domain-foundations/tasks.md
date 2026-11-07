# Tâches — C97

Plan ACL-PIXS-2026-10-31-E3-R1, validé le 31 octobre 2026. Toutes les tâches ci-dessous sont futures et non lancées. Les vérifications nécessaires appartiennent à chaque unité avant sa validation ; leur présence ne constitue pas une exécution.

- [ ] 1. Identité Instance et données pré-domaine : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 2. Domaines FQDN et rattachement ZT : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 3. Bases et contrôleurs séparés : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 4. Transition après ZT initialisé : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.
- [ ] 5. Continuité et conformité : préciser les contrats puis réaliser le seul périmètre et ses contrôles nominaux/refus/reprise avant validation.

## Sous-lots normalisés

Chaque tâche correspond à son sous-lot ; les identifiants sont stables, ne fixent pas seuls l’ordre de réalisation et ne peuvent pas être réutilisés. Aucun alias historique n’existe à la création. Sources : [proposal.md](proposal.md), [design.md](design.md) et [requirements.md](requirements.md).

### C97-SL01 — Identité Instance et données pré-domaine

- Exigences et version cible propres à cette unité :
  - `pixs-instance` — **Identité logique et référentiel commun**.
  - `pixs-instance` — **Modes Standalone ZT et Domaine**.
  - `pixs-instance` — **Références PG avant et après Domaine** — clause pré-domaine uniquement ; la postcondition après transfert est vérifiée en C97-SL04.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Ajout de PBO** : il référence les individus communs tout en conservant les données et responsabilités de ses modules.
  - **Transport pré-domaine** : le mode reste Standalone et les contrôles réseau et applicatifs restent nécessaires.
  - **Mode ZT** : le référentiel des individus et les données pré-domaine restent au niveau Instance.

- Tâche rattachée : 1, libellé conservé ci-dessus.
- Objectif et périmètre : Identité, référentiel commun, trois modes et données pré-domaine au niveau Instance. La clause après transfert reste attribuée à C97-SL04 ; aucun Domaine réel n'est créé ou activé par cette unité.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Sources d'identité, modes et données pré-domaine et contrats d'amorçage C08 vérifiés ; propriétaires identifiés. Aucun Domaine actif, résultat ultérieur de C96/Z30 ou service de Domaine opérationnel n'est requis pour ces fondations.
- Critères observables : Prouver identité commune, transport pré-domaine, trois modes distincts et maintien des données/identités pré-domaine dans PG Instance. Ces fondations sont vérifiables sans Domaine actif, sans dépendre des réalisations ultérieures de C96 ou Z30 ; publier les contrats qu'elles consommeront. Le scénario positif d'activation est couvert en C97-SL04, sans être revendiqué ici.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### C97-SL02 — Domaines FQDN et rattachement ZT

- Exigences et version cible propres à cette unité :
  - `pixs-domains` — **Identité et FQDN explicites**.
  - `pixs-domains` — **ZT obligatoire dédié ou partagé**.
  - `pixs-domains` — **Isolation dans un ZT partagé**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Racine déjà utilisée** : la déclaration est refusée avant activation.
  - **Deux sous-domaines** : ils peuvent être rattachés avec des périmètres distincts.
  - **Faux suffixe** : la condition hiérarchique DNS est refusée.
  - **Même ZT sans politique** : l’initiation inter-domaines est refusée.

- Tâche rattachée : 2, libellé conservé ci-dessus.
- Objectif et périmètre : Contrats FQDN, plan de rattachement dédié/partagé et isolation. La validation d'un plan ne crée aucun Domaine ; toute création effective du premier Domaine relève de C97-SL04 après vérification du ZT.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats d'Instance consommés de C97-SL01, règles canoniques FQDN et interfaces ZT concernés vérifiés. Les plans et refus sont contrôlés sans effet de création ; la vérification opérationnelle du ZT à la création reste obligatoire en C97-SL04.
- Critères observables : Vérifier unicité FQDN, hiérarchie par labels, plans de rattachement distincts et refus inter-domaines sans politique. Prouver que la préparation n'engendre aucun Domaine et qu'une demande de création du premier Domaine est refusée si le ZT n'est pas entièrement initialisé. Les effets du rattachement réel sont vérifiés en C97-SL04 avec les propriétaires ZT.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### C97-SL03 — Bases et contrôleurs séparés

- Exigences et version cible propres à cette unité :
  - `pixs-instance` — **Minima et contrôleurs distincts**.
  - `pixs-instance` — **Références PG avant et après Domaine** — contrats de séparation et préparation ; le transfert effectif est vérifié en C97-SL04.
  - `pixs-domains` — **Services minimaux par Domaine** — contrats et refus de disponibilité ; la qualification des services réels relève des propriétaires et conditionne C97-SL04.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Contrôleurs regroupés** : les propriétaires des bases, identités et autorisations restent distincts.
  - **ZT partagé et KZT manquant** : ses services de Domaine restent non opérationnels tant que ce minimum manque.

- Tâche rattachée : 3, libellé conservé ci-dessus.
- Objectif et périmètre : Schémas, propriétaires, contrats de contrôleurs séparés, ressources préparables et contrôles de disponibilité. Leur préparation ne crée ni active un Domaine et ne vaut pas qualification des services LDAP/Kerberos.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Contrats d'Instance de C97-SL01, modèles de propriété, stockage et interfaces de contrôleurs vérifiés. Les services de Domaine actifs ne sont pas requis pour préparer ces contrats et leurs refus ; leurs résultats réels sont requis au point d'activation en C97-SL04.
- Critères observables : Prouver séparation des propriétaires/bases/habilitations même si les contrôleurs sont regroupés, et le refus de déclarer les services de Domaine opérationnels si un minimum tel que KZT manque. Les contrats et refus peuvent être vérifiés avant la transition ; ils ne prouvent pas la disponibilité des services réels. Le transfert PG et les services cibles sont vérifiés en C97-SL04 avant activation.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### C97-SL04 — Transition après ZT initialisé

- Exigences et version cible propres à cette unité :
  - `pixs-instance` — **ZT entièrement initialisé avant Domaine**.
  - `pixs-instance` — **Maintenance des écritures pour la transition**.
  - `pixs-instance` — **Références PG avant et après Domaine** — transfert et postconditions effectifs.
  - `pixs-domains` — **Services minimaux par Domaine** — preuves opérationnelles des services requis.
  - `pixs-instance` — **Absence de retour Domaine Standalone V1**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **ZT incomplet** : la transition reste bloquée avec les capacités manquantes identifiées.
  - **Préconditions vérifiées** : après preuve du ZT entièrement initialisé, la procédure autorisée peut créer le premier Domaine ; son activation attend les preuves de transfert et de disponibilité requises.
  - **Activation du premier Domaine** : l’identité de Domaine devient utilisable selon son profil et l’ancienne identité d’Instance ne reste pas une autre voie de connexion.
  - **Interruption de transfert** : la procédure réconcilie les états propriétaires avant toute répétition ou reprise des écritures.
  - **Ancienne sauvegarde** : les contrôles empêchent de rétablir le mode et les identités Standalone devenus caducs.

- Tâche rattachée : 4, libellé conservé ci-dessus.
- Objectif et périmètre : Procédure de création puis activation du premier Domaine, après vérification du ZT ; maintenance des écritures, transfert contrôlé, authentification cible et postconditions effectives.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Résultats consommés de SL01 à SL03 et contrats de transition C96 vérifiés ; autorisation et plan de maintenance courants. Vérifier le ZT entièrement initialisé avant création ; obtenir ensuite les preuves de transfert C96 et de services O38/O39 et autres propriétaires requis avant activation. Aucun dossier de change n'est présumé livré en bloc.
- Critères observables : Avant toute création du premier Domaine, vérifier les rôles ZT essentiels, identités, stockage et politiques ; un état administratif ou un processus vivant ne suffit pas. Puis, sous procédure autorisée et maintenance des écritures, créer le Domaine et coordonner les travaux de ses propriétaires. Avant activation et reprise des écritures, vérifier transfert des identités/données/relations, PG séparées, services minimaux réels dont LZT/KZT et authentification cible selon le profil. Prouver l'invalidation des anciennes identités d'Instance, la réconciliation après interruption et l'absence de retour Standalone. Ces preuves appartiennent à cette unité, sans attendre C97-SL05.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.

### C97-SL05 — Continuité et conformité

- Exigences et version cible propres à cette unité :
  - `pixs-instance` — **Administration globale par identités habilitées**.
  - `pixs-instance` — **Absence de retour Domaine Standalone V1**.
  - `pixs-instance` — **Habilitations Instance et domaines**.
- Résultats observables à vérifier dans cette unité (scénarios source, non exécutés) :
  - **Domaine d’authentification non habilité** : la demande est refusée malgré la validité de son authentification.
  - **Ancienne sauvegarde** : les contrôles empêchent de rétablir le mode et les identités Standalone devenus caducs.
  - **PBO mutualisé** : son action reste limitée aux périmètres explicitement autorisés.

- Tâche rattachée : 5, libellé conservé ci-dessus.
- Objectif et périmètre : Continuité, habilitations et conformité de bout en bout ; consolidation des preuves déjà exigées par unité, sans reporter les contrôles de C97-SL01 à SL04.
- Composants visés : les propriétaires et contrats cités dans design.md ; les fichiers d'implémentation seront identifiés avant code, sans squelette produit ici.
- Prérequis : Preuves des unités SL01 à SL04 et des propriétaires externes recoupées pour les versions et périmètres consommés ; habilitations et environnement de continuité disponibles. Une lacune bloquante interdit la validation.
- Critères observables : Recouper les preuves locales de C97-SL01 à SL04, exercer continuité, refus d'administration sans habilitation et reprise sans retour Standalone. Une preuve obligatoire absente d'une unité antérieure bloque cette consolidation ; elle ne transforme pas rétroactivement sa préparation en réalisation.
- Contrôles futurs : types/versions/périmètres, nominal et refus, autorisation/fraîcheur, concurrence et interruption/reprise nécessaires à l'unité ; résultats propriétaires et postconditions réelles avant toute coche.
- État : À FAIRE. Preuves de réalisation : aucune. Le présent document n'est ni une validation fonctionnelle ni une recette.
