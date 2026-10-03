# Conception sonde PG ASYNC bornee

## Context
settings.py gabarit sans env ni reseau, checks.py sans connexion, grep zero SELECT 1 dans src, specs bootstrap et runtime relues. Complement technique retenu : wait sur annulation appelle _try_cancel 5s puis drain sans borne, donc pas de wait_for direct autour execute comme preuve de delai.

## Goals / Non-Goals
But : prouver connectivite PG read-only bornee avec fermeture sur tous chemins. Non-buts : disponibilite globale, P0, migrations, tenant, profils, metriques, hard deadline noyau, arret serveur, seuils universels.

## Decisions
- ASYNC uniquement dans ce jalon, pas de V1 sync dont attente reseau locale resterait non bornee.
- IP litterale unique avec host et hostaddr identiques, sans DNS ni multihost. hostaddr valide stdlib sans resolution.
- connect_timeout int exact >= 2 choisi par caller, borne connect distincte par adresse unique, minimum libpq effectif documente.
- query_timeout positif fini choisi par caller comme borne locale asyncio.wait sans cancel premature ; si depassee, fermer la connexion AVANT task.cancel puis recueillir issue generique, sans retry ni cancel_safe.
- statement_timeout int positif en ms representable libpq et PG choisi par caller, best-effort serveur sans promesse de borne locale ni arret serveur.
- SELECT 1 seul, autocommit vrai, option session lecture seule, aucune DDL ni config persistante. password dbname user caller explicites non vides en str exact sans NUL et bornes. Rejeter dbname avec URI de connexion ou signe egal pour eviter toute expansion. Aucun helper ni option n invente un chemin de secrets.
- Fermeture explicite sans pool et sans async with connexion. Curseur explicitement detenu puis ferme. Succes exact tuple avec un seul int non bool egal a 1, aucun retry.
- Duree locale observee par caller, evenementiel cooperatif, jamais hard deadline noyau ni garantie reelle.
- Types exacts avant len et hash, refus fixe sans brut ni traceback libpq, aucun secret journalise, aucun etat global.

## Files
src/pixs/backend/pg_connectivity.py, tests/unit/test_pg_connectivity.py avec doubles sans PG reel, tests/integration/test_pg_connectivity_integration.py avec PG reel sous mandat dedie et vars processus seul, append seul src/pixs/backend/README.md.

## Validation
Strict avant et apres, subprocess isoles env minimal timeout30, AST 3.11 UTF-8 LF, perimetre strict, suites unit sans PG puis integration PG dediee avec valeurs operationnelles conn 2s requete 2s statement 1500ms et timeout global processus 12s comme valeurs de test uniquement.
