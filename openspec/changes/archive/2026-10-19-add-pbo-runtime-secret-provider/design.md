# Conception — C01

## Statut et périmètre autorisé

RÉALISATION QUALIFIÉE FONCTIONNELLEMENT sous le RUN parent CISMP3/ISMP, après clôture de la RSMP documentaire approuvée. Suites unitaires et transport natif avec fixtures publiques prouvés ; archivage et statistiques restent des états distincts. C00 adopté et archivé le 18 octobre 2026 ; son canon est la référence. Reprise C05/C08 interface future seulement.

## État actuel vérifié

Références et résolution pures ; `check_template` `secrets_resolved=False`. Structures existantes à réutiliser : `src/pixs/kernel/config/resolution.py`, `src/pixs/backend/settings.py`, `src/pixs/backend/checks.py`.

## Architecture B01-B09

B01 : journal local temporaire distinct des logs, hors paquet/dépôt en exploitation, contrat transitoire approuvé avant réalisation. Backend seul. Répertoire et rétention explicites exigés ; aucune valeur de secret.

B02 : installation et journal UUIDv7, `schema_version`, séquence monotone `>=1`, `AuditEvent` 13 champs existant. Références seules, identité OS vérifiée, PLATFORM explicite sans `tenant_id`/`scope_id`, autorisation technique d’amorçage propre jamais déduite de sa forme. Tailles et rétention obligatoires sans chiffre.

B03 : fichier régulier sans symlink, append-only, création exclusive `O_CREAT|O_EXCL` sans troncature ni suivi de lien, verrou sur objet stable distinct et consultatif. Acquittement seulement après append complet + `fsync` fichier et répertoire à création. Reçu lié, jamais `True` comme preuve.

B04 : même `event_id` + contenu identique → réconciliation sans doublon ; divergent → refus. Fin partielle/corruption/saturation/échec sync/résultat incertain → refus fermé, conservation preuves, sans troncature/purge/recréation/rejeu. Empreinte = cohérence seule, pas de garantie contre root/restauration.

B05 : résolution/refus/rotation/révocation auditables avant remise. Échec audit ordinaire → refus sans valeur. Root OS MUST NOT devenir Super Admin ; aucune dérogation inventée.

B06 : après PostgreSQL et sink C05 : journal SEALED, transfert ordonné idempotent par `event_id` + empreinte, acquittement lié au commit propriétaire. Sans preuve de reprise complète, aucune conformité P0 ni admission C08/C07. Conservation selon rétention/holds, aucune suppression après import.

B07 : `LoadCredentialEncrypted` par service, valeurs en mémoire seule du consommateur. UID et unité réellement vérifiés, mapping rôle/finalité/référence par politique de confiance. Opérateur OS d’amorçage distinct du Super Admin.

B08 : durées de vie, validités, délais révocation, budgets arrêt/restart obligatoires sans défaut numérique. Secret absent/expiré/révoqué ou politique non vérifiable → refus. Rotation copie chargée : arrêt attesté puis remplacement et restart.

B09 : exception INSTALLER explicitement demandée : OS+unité réels, politique versionnée à ensemble fermé, refus par défaut, PLATFORM + audit obligatoires. Ne crée ni DigitalIdentity ni session ni tenant ni permission métier ni Super Admin.

## Schémas et reçus

Record `BootstrapAuditRecordV1` exact : `schema_version`, `journal_id` UUIDv7, `sequence`, `event` (AuditEvent 13 champs avec `event_id` UUIDv7), `event_sha256`. JSON UTF-8 déterministe : tri des clés explicite, séparateurs compacts, pas de NaN, pas de normalisation ni coercition, tableaux pour tuples, aucun secret. `event_sha256` = SHA-256 du seul événement sérialisé ; pas de JCS ni signature promise. Reçu `BootstrapAuditReceiptV1` exact : `journal_id`, `event_id`, `sequence`, `event_sha256`, émis seulement après append/sync réussis, relu et comparé en récupération. États `OPEN` append seul, `SEALED` reprise seule ; état incertain/corruption bloque sans purge/troncature.

## Sources de preuve et critères

PID1/cgroup et credential privé UID ; politique de confiance ; corrélation audit ; version épinglée + gate non-ready tant que version révoquée non redémarrée. Distinguer tests adapter isolé fixtures synthétiques, transport réel hôte qualifié, qualification paquet C17/C18/C19. Aucun callback ni assertion env ne vaut preuve.

## Hors profil et limites

PA actif, réseau PZT actif, DNS par PA, image Docker et options hors sélection. Aucune réalisation C05/C08. Seuls les cinq canons correspondant aux deltas C01 sont destinés à la synchronisation autorisée de ce change. Voir revue transversale P0 du 17 octobre 2026 : T03 réadmission, T05 amorçage C01/C08, sans tâche cochée.

## Références et frontières conservées

- C00 adopté et archivé : `openspec/changes/archive/2026-10-18-define-first-installable-pbo-profile/proposal.md`.
- Audit transversal durable : `openspec/changes/archive/2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json`.
- Rapport transversal de préparation : `reports/audit-transversal-p0-2026-10-17/RAPPORT.md`.

Les deltas portent les garanties normatives, y compris l’exception au Subject applicatif avant base, sans autoriser d’action métier. L’exception de stockage local reste limitée à l’amorçage ; aucun fichier local ne devient source de vérité métier après reprise PostgreSQL. Les tests emploient exclusivement des données synthétiques, sans secret réel. Les preuves de panne de processus et d’appel fsync restent distinctes d’une qualification matérielle contre coupure de courant.

## Réalisation et frontières de confiance

Le manifeste `systemd_secret_provider/component.toml` déclare un PROVIDER 0.1.0, schéma 1, dépendant de `pixs.kernel` 0.1.0. Les nouvelles entrées restent dans le backend : `bootstrap_audit.py`, `bootstrap_policy.py`, `runtime_resolve.py` et le paquet `systemd_secret_provider`. Aucun contrat supplémentaire ni activation implicite C07 n’est ajouté. Le Kernel, `SettingsTemplate`, `check_template` et les contrôles existants restent inchangés.

`PolicySource(path, owner_uid, policy_id, max_policy_bytes)` est fourni par la composition de confiance, jamais par une requête non fiable. Le TOML protégé est relu à chaque résolution et consommation, sans cache. Tous les champs de `C01Policy` sont obligatoires : identité UID/unité/manager, contrôleur distinct, rôle/finalité/PLATFORM, références/noms/versions/sources chiffrées et validités, limites de taille/TTL/révocation/budgets, journal/rétention/holds/actions/versions révoquées. Aucun chiffre du harnais n’est un défaut de production. L’opérateur système, même UID 0, n’obtient aucune autorité métier.

Chaque credential transporte une enveloppe JSON exacte `schema_version=1`, `credential_version`, `value`, sans clé supplémentaire, doublon, valeur vide ou NUL. La version doit correspondre au binding. Le SDK prouve son UID et son unité par libsystemd, recoupe le snapshot chargé et les deux mappings `LoadCredentialEncrypted`, puis vérifie le répertoire réellement monté en lecture seule et ses droits/ACL pour le seul UID sélectionné. `CREDENTIALS_DIRECTORY` doit correspondre au chemin épinglé après cette preuve ; sa présence ne vaut jamais autorisation. Aucun fallback vers une source en clair n’existe.

`resolve_runtime_settings(template=..., source=..., mode=StartupMode.INSTALLER, purpose=...)` réutilise la validation pure du gabarit. `as_dict()` revalide le bundle et remet un dictionnaire neuf au consommateur de confiance pour `LazySettings.configure`, avec les deux valeurs en mémoire. Les conteneurs sont non sérialisables et leur représentation est masquée. `ready` reste faux ; aucun accès à PostgreSQL, `django.setup()`, Subject ou session Pixs n’est créé. La mémoire du consommateur autorisé reste une frontière explicite de confiance.

## Rotation et révocation réalisées

`controller_guard` couvre la transaction entière ; `unit_lease` conserve la définition de l’unité transitoire sans prouver à lui seul son arrêt. Sous `lifecycle_guard`, le contrôleur audite le début, publie atomiquement une politique sans `resolve`, arrête puis atteste l’ancienne invocation et son cgroup, remplace les deux sources chiffrées et publie la nouvelle politique. Il libère cette garde avant le démarrage pour permettre au SDK consommateur de résoudre. Le budget de redémarrage couvre le démarrage, les snapshots, la nouvelle invocation et les reçus durables des deux résolutions SDK, puis une dernière vérification de politique et de gate précède l’audit de succès.

La gate exige `Type=exec`, une durée maximale finie bornée par TTL et délai de révocation, une durée aléatoire nulle, un budget d’arrêt borné avec `TimeoutStopFailureMode=kill`, `KillMode=control-group`, `SendSIGKILL=yes`, `Restart=no`, sans ExecStop/ExecStopPost ni fallback credential. Les valeurs doivent laisser assez de validité aux credentials. La révocation bloque les résolutions, atteste l’arrêt et publie les versions révoquées avant son acquittement ; elle ne redémarre pas le consommateur.

Un échec après début conserve les preuves et tente de bloquer la politique effectivement courante, sans restaurer une version ancienne. Une impossibilité de prouver ce blocage ou l’audit produit un refus distinct nécessitant réconciliation explicite ; aucun rollback ni rejeu automatique. Les remplacements conservent propriétaire/groupe/mode, emploient un temporaire exclusif puis fsync/rename/fsync répertoire. Les fichiers incertains ne sont pas purgés.

## Preuves fonctionnelles et limites

Les suites isolées couvrent l’audit, la politique, l’accès natif, le provider, le runtime et le lifecycle. La régression globale a exécuté 1 945 tests avec succès. Les appels D-Bus en lecture seule ont confirmé les formats natifs et l’absence des deux unités du harnais. Le harnais `tests/integration/test_c01_systemd_harness.py` est syntaxiquement valide, expose son plan sans effet et refuse l’exécution non privilégiée avant toute mutation. Son exécution manuelle root approuvée et sa vérification indépendante sous CAB ont prouvé deux versions consommées, douze événements d’audit, une nouvelle invocation après rotation, la révocation et l’absence des deux unités après nettoyage. Ses valeurs publiques connues et le mode systemd-creds `--with-key=null` qualifient uniquement le transport fonctionnel ; ils ne prouvent ni confidentialité ni authenticité du chiffrement en production.

La lecture D-Bus de `ControlGroup` emploie l’interface Service, conformément au bus systemd 257 réellement observé. Le mode `--recover-case` est limité à un ancien cas vérifié : les deux identités sont contrôlées avant toute écriture, chaque unité présente doit être transitoire, correspondre au nonce du cas, à son fichier transitoire et à son UID, puis être inactive/failed avec MainPID entier nul. Les preuves sont conservées avant arrêt/réinitialisation ciblés et après déchargement ; aucune politique ou donnée ancienne n’est régénérée. Les diagnostics worker ne contiennent que l’étape et le type d’exception, qui reste propagée.

Preuve durable : [PREUVES-C01.json](PREUVES-C01.json). La commande de vérification indépendante est `c3-cmd-236584a2-effect` (permission native once, exit 0). Elle ne remplace pas une mesure matérielle contre coupure ni une qualification cryptographique de production.
