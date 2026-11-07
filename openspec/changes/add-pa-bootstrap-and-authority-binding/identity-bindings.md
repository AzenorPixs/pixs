# Liaisons d'identité proposées — relation PBO et PA

Statut proposé. PA02 désigne le lot documentaire, pas un composant propriétaire. Rôle natif PA propriétaire de l'identité et de l'état technique distingué de pixs.agent PBO qui gère les relations via PZT, contrats précis à fermer avant code. Référence : [pixs-agent](../../specs/pixs-agent/spec.md), contrat public Core. Complète [contracts.md](./contracts.md).

## Table des références

| Référence | Stabilité | Source | Propriétaire |
|---|---|---|---|
| PA technique | stable | profil propriétaire | rôle natif local PA, responsabilité et contrat exact à fermer |
| autorité logique PBO | stable | profil propriétaire | autorité compétente |
| membre PBO opérationnel | remplaçable sans élargir droits | rattachement explicite | autorité compétente |
| relation PBO et PA | stable et explicite | liaison PA, autorité, périmètre | relation gérée par pixs.agent PBO via PZT avec vérification locale PA, responsabilité et contrat exact à fermer |
| périmètre | déclaré et versionné, évolution explicitement autorisée et contrôlée sans recalcul implicite d'identité | profil | propriétaire ressource |
| version, génération, credential, opération | attributs variables et contrôles | contexte courant | vérificateur courant |

Adhésion ou remplacement de membre n'élargit aucun droit. Mappings vers DigitalIdentity par contrats publics Core, authentification, assurance et session par Auth, permissions par contrats publics Core, sans import privé. Identité distincte de permission, autorisation et assurance. Résultat provenant d'une autre relation refusé, aucune exposition de références d'autres autorités. Isolement préservé, pas d'identité nouvelle sur retry ou rotation.


## Reliure d'identité v1 — addendum 2026-10-26

Cet addendum précise la reliure sans modifier l'historique. Les détails de forme sont définis dans contracts.md du même change.

L'identifiant PA est stable et de type UUID exact en Python, avec une forme UUIDv7 canonique dans le document. Les autres références du document sont opaques et ne sont jamais interprétées comme des UUID.

La relation est opaque et distincte de l'identité. L'autorité citée est logique et ne prouve pas à elle seule l'origine ni l'autorisation. Le membre fourni par mapping reste hors document et n'est pas introduit par le codec.

Le scope est plat : PLATFORM exige tenant_id null et scope_id null, TENANT exige tenant_id opaque non vide et scope_id opaque non vide ou null. Le périmètre de ressource et sa version sont distincts du scope. La révision de configuration est opaque et distincte de l'époque et de la génération d'autorité.

La génération d'autorité, l'UID, le PID, l'identifiant de session logind, l'identifiant d'invocation et l'opération restent distincts et ne sont pas introduits par le codec.

Références : contracts.md du même change, contrats publics de Core pour l’identité et le scope, PROJECT section 44.4 pour le modèle des identités.

## Addendum RSMP identité et frontière — principes A ADOPTÉS, interface et qualification restantes
Choix A ADOPTÉ le 2026-10-26 ; B non retenu. Principes ADOPTÉS, acquis D1A D2A D3A conservés ; interface, code et qualification restant à réaliser. pa_id stable, autres refs opaques jamais interprétées. Relation opaque distincte identité. Autorité citée logique ne prouve ni origine ni autorisation. Membre mapping hors document. Périmètre et version distincts scope. Révision opaque distincte époque et génération. Droits et révocation déterminés par vérificateurs courants non livrés, jamais par stockage. Adapters Core Auth PG non qualifiés, disponibilité générale non confondue avec qualification. Aucune valeur qualified ou trusted fabriquée.
