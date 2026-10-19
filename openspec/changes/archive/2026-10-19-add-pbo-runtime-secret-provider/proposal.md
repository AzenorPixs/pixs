# C01 — Configuration et secrets effectifs

## Why

Les références de secrets et la résolution de configuration sont pures ; check_template conserve secrets_resolved=False. Le provider systemd, le journal d’amorçage et les entrées runtime C01 sont réalisés sous le RUN parent CISMP3/ISMP. La qualification fonctionnelle du transport sur l’hôte est prouvée ; aucune disponibilité P0 n’est revendiquée.

## What Changes

Sélectionner `LoadCredentialEncrypted` systemd par service comme transport retenu ; fournir réglages runtime validés, identité workload réellement vérifiée, accès, rotation/révocation et audit d’amorçage limité. Journal fonctionnel local temporaire, contrat d’exception transitoire approuvé par le développeur, puis réalisé sous mandats du RUN parent. Les preuves unitaires et la qualification hôte restent distinctes. Les formats internes B01-B09 sont explicitement décrits par les deltas, sans fournisseur implicite supplémentaire.

## Capacités

### Capacités nouvelles

Deltas normatifs C01 validés : journal d’amorçage B01-B09, provider systemd, sélection profil et autorisation technique INSTALLER bornée. Réalisation détaillée dans design.md et tasks.md ; aucune activation générale du profil.

### Capacités modifiées

Les cinq canons correspondant aux deltas C01 sont synchronisés en conservant les exigences non concernées. `requirements.md` relie exigences sources et deltas proposés ; `skip_specs` retiré car deltas présents. Si la conception exige un comportement nouveau, un delta dédié MUST être présenté et approuvé avant réalisation.

## Dépendances

- C00 adopté et archivé : `openspec/changes/archive/2026-10-18-define-first-installable-pbo-profile/proposal.md`.
- Reprise C05/C08 comme interface future, sans implémenter C05/C08 ni revendiquer P0 prêt.

## Impact

Périmètre C01 : Kernel déclaratif inchangé ; résolution dans adapter backend ; UID et rattachement unité réellement vérifiés ; contexte PLATFORM sans identifiants avec autorisation technique INSTALLER bornée, distincte du Subject applicatif et du Super Admin. Rotation par arrêt attesté puis remplacement et redémarrage contrôlé ; reload ou suppression source seule MUST NOT valoir révocation. Audit avant toute remise de secret ; durées/limites/versions obligatoires vérifiables sinon non-ready. `SettingsTemplate` et `check_template` restent purs et non prêts.

La RSMP documentaire a été clôturée dans les dix fichiers approuvés. La réalisation actuelle relève de l’autorisation du RUN parent CISMP3/ISMP et de ses mandats CAB unitaires ; la RSMP seule n’autorisait aucun code. L’intervention hôte bornée a reçu une validation distincte et a été exécutée manuellement en root, puis vérifiée indépendamment. Aucune migration, dépendance supplémentaire, opération Git ou disponibilité P0 n’est comprise.

## Critères de sortie

Secret absent/expiré/révoqué ou politique non vérifiable → démarrage refusé ; workload non autorisé → refus audité ; rotation testée par restart ; aucune valeur en configuration distribuée, artefacts, diagnostics ou audit.

## Barrière de conception

Le contrat B01-B09, le transport systemd et la rotation par redémarrage contrôlé ont été validés avant réalisation. Les limites numériques sont des paramètres explicites obligatoires, sans défaut de production. La qualification fonctionnelle hôte est prouvée : douze événements, reçus relus, rotation avec nouvelle invocation, révocation et deux unités absentes. Les validations d’archivage, l’archive et STATISTIQUES.md restent des barrières distinctes de clôture du RUN.

Preuve durable : [PREUVES-C01.json](PREUVES-C01.json). La commande de vérification indépendante est `c3-cmd-236584a2-effect` (permission native once, exit 0). Elle ne remplace pas une mesure matérielle contre coupure ni une qualification cryptographique de production.
