# Tâches — C01

Réalisation et qualification fonctionnelle prouvées sous le RUN parent CISMP3/ISMP. La RSMP documentaire initiale n’autorisait que sa rédaction ; les réalisations suivantes relèvent du mandat parent. Les états d’archive, de statistiques et de publication sont suivis séparément par le gate terminal du RUN et ne sont pas déduits des coches.

## 1. Revue de conception

- [x] 1.1 Revoir exigences et deltas B01-B09, adoption C00 archivé ; sources et périmètre recoupés avant réalisation.
- [x] 1.2 Valider le contrat systemd-restart, l’audit d’amorçage, PLATFORM + INSTALLER borné, schémas et reçus. Choix et contrat validés explicitement par le développeur.

## 2. Réalisation

- [x] 2.1 Déclarer le provider approuvé, le manifeste PROVIDER 0.1.0, les entrées runtime et les garanties.
- [x] 2.2 Relier les références aux réglages Django sans valeur distribuée. LazySettings.configure réel vérifié dans les consommateurs v1/v2 ; aucun accès base ou django.setup.
- [x] 2.3 Implémenter résolution autorisée, refus fermé, rotation/révocation et audit minimisé. Reçus persistants relus avant succès, sans callback booléen de substitution.
- [x] 2.4 Tester absence de provider, workload non autorisé, révocation, restart et absence de fuite. Cas isolés et harnais réel validés avec fixtures publiques ; mode null limité au transport fonctionnel.

## 3. Preuves et autorisations de clôture

- [x] 3.1 Exécuter syntaxe, contrôles ciblés et suites applicables. Régression globale 1 945 tests réussis ; correctifs/récupération 26 tests ; cinq deltas C01 strictement validés, dont le contenu normatif est conservé pendant synchronisation.
- [x] 3.2 Vérifier isolation, échecs attendus, absence de secret réel et conformité des scénarios. Qualification indépendante c3-cmd-236584a2-effect : 12 événements, reçus, invocations, versions et absence des deux unités recoupés.
- [x] 3.3 Examiner contenus et empreintes du périmètre. Cinq invariants Kernel/gabarits/contrôles préservés ; aucun état Git inspecté ; aucune disponibilité P0 annoncée.
- [x] 3.4 Vérifier les autorisations des opérations de clôture. Archivage, synchronisation des seuls cinq canons et STATISTIQUES.md sont autorisés par le RUN parent et confirmés par la demande finale du développeur ; chaque effet conserve un mandat CAB distinct. Aucune autorisation Git ou déploiement général n’en découle.

## Barrières terminales indépendantes

Les validations globales d’archivage, l’archive effective, sa publication, le rapport STATISTIQUES.md à six sections et le gate puis désarmement/libération restent obligatoires. Leurs preuves sont consignées dans le checkpoint et le rapport final après leur exécution ; les tâches ci-dessus ne prétendent pas les avoir produites par avance.

Voir [PREUVES-C01.json](PREUVES-C01.json) pour les reçus, identifiants et limites de qualification.
