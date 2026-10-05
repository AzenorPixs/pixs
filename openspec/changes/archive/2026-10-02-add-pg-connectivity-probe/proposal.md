# Sonde PG connectivite initiale ASYNC

## Why
initial-application-bootstrap exige PostgreSQL comme persistance de reference avec secrets runtime uniquement. Aucune sonde PG reelle dans src, aucune preuve de connexion sans ecriture metier. Absence implementable, non incoherence.

## What Changes
- Sonde ASYNC bornee SELECT 1 seul vers IP litterale unique avec host et hostaddr identiques, credentials et delais fournis par caller, autocommit vrai et lecture seule de session, fermeture garantie.
- Refus generiques fixes sans valeur connexion ni traceback, duree locale observee distinguee de toute garantie reelle.
- Aucune mutation, DDL, config persistante, generation span, handler global, nouveau contrat, profil, route, version ou norme.

## Capabilities
### New Capabilities
Aucune.
### Modified Capabilities
- initial-application-bootstrap : sous-jalon connectivite PG seule, reste composition globale, P0, migrations et disponibilite non prouves.

## Impact
Un helper ASYNC, deux tests futurs, un append README seul. Aucune norme reecrite, aucune activation globale.
