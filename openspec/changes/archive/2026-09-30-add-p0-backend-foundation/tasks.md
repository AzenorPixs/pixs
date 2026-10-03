## 1. Preparation OpenSpec

- [x] 1.1 Relire proposal et design, verifier les deltas canoniques reference-runtime/runtime sans nouvelle norme.
- [x] 1.2 Creer les seuls deltas requis et valider le change en mode strict ; verifier UTF-8/LF et coherence des cadrages.

## 2. Fondation backend

- [x] 2.1 Declarer les seules dependances directes Django==5.2.17 et psycopg==3.3.5 dans pyproject.toml, en preservant Python >=3.11.
- [x] 2.2 Preparer le paquet backend commun et la configuration explicite PIXS_PROFILE pour web/worker/scheduler, sans defaut de role, secret ou base alternative.
- [x] 2.3 Preparer les controles hors base et limites inspectables, sans declarer de services ou persistance operationnels.
- [x] 2.4 Documenter le parcours synthetique et les exclusions ; toute installation isolee reste un mandat distinct.

## 3. Preuves et cloture

- [x] 3.1 Executer les tests dedies unitaires/integration avec configurations synthetiques et garde contre toute connexion PostgreSQL.
- [x] 3.2 Executer les regressions applicables, controles de syntaxe, UTF-8/LF et validation OpenSpec stricte, puis verifier le perimetre.
- [x] 3.3 Verifier les preuves, les criteres, la coherence et la validation CGPT du dossier de cloture avant archivage.

L'archivage est exige apres toutes les taches ci-dessus prouvees et cochees, sous mandat CAB distinct apres controle CGPT ; il ne fait pas partie de la case 3.3.
La production de STATISTIQUES.md est un mandat distinct apres archivage effectif, avec sonde finale et quotas reels ou N/A motives. Aucune case ci-dessus n'est une preuve acquise. Si la session s'arrete a 16h30 Paris, conserver l'etat du premier jalon non prouve sans archivage ni declaration de reussite.
