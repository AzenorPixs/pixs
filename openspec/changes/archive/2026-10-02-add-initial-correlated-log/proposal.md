# Journal local corrélé initial

## Why
observability Signaux structurés exige émission corrélée sans secret. correlation_id UUID exact existe avec nil/max, aucune extraction traceparent ni émission locale observée. Il s agit d une absence implémentable, non d une incohérence.

## What Changes
- Adaptateur plat correlated_log pour composition initiale seule, parse traceparent 00 strict et correlation_id selon grammaire existante, événement fixe sans message libre ni timestamp.
- Émission réelle locale unique write str vers sink caller borné, StringIO réel en tests, sans handler global ni réseau ni fichier ni secret.
- Refus génériques fixes sans brut, échec write détecté sans relance, mêmes IDs sur trois composants connus.
- Aucune génération span/trace, aucune inspection tracestate, aucun nouveau contrat public ni profil ni route ni version ni norme.

## Capabilities
### New Capabilities
Aucune.
### Modified Capabilities
- observability : sous-jalon journal local initial seul, reste métriques/traces/propagation/runtime globaux non prouvés.

## Impact
Un helper plat, deux tests futurs, un append README seul. Aucune norme réécrite, aucune activation globale.
