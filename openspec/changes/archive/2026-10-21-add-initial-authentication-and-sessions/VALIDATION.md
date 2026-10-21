# Validation C03 — authentification locale et sessions

Qualification du 21 octobre 2026. RUN cismp1-pixs-d4031c8c16a3409d ; session ses_ea598d5c9ffee1IM7aJ25LQ2Oe ; contexte CAB 433 ; référence commune relue 52. Change add-initial-authentication-and-sessions. Le checkpoint propriétaire est /home/devops/datas/pixs/output/cismp/cismp1-pixs-d4031c8c16a3409d/state.json.

La réalisation locale est qualifiée. Cette validation autorise son archivage C03 ; elle ne remplace pas les preuves distinctes d'archive, de STATISTIQUES.md, de publication et de gate terminal. Le cycle global Pixs reste incomplet. Aucun commit, push ou déploiement n'est autorisé ou réalisé par cette livraison.

## Sources et frontières

Module pixs.auth 0.1.0 ; capacité auth.local 1.0.0 requise sans fallback ; AuthenticationService, SessionService et CredentialService 1.0.0. Le manifest et les mécanismes communs Kernel s'appliquent. La migration 0001 crée onze modèles privés en 127 opérations, sans FK privée vers Core. Empreinte : 4ca163b7a54065dd49598bb1af87fa2816b0af4e1761153e0dd85a7413f63f82. La génération native prt_15c848eba001wdZmxC6jg1eEBW n'a ouvert aucune connexion SQL. L'ancien suivi d'empreinte a été réconcilié avec cette preuve sans régénération ni rejeu.

Le snapshot des 51 chemins source/recettes suivis dans le checkpoint a pour empreinte 1606bc1e649187d634634197ef0f2172ffa6bce3ca4defb755aa910f4bdb7166 (JSON trié par chemin avec path/sha256). Les neuf canons de requirements.md sont recontrôlés et inchangés à la clôture. Le détail des fichiers et décisions est conservé dans le checkpoint, sans valeurs privées PG.

## Résultats natifs réellement exécutés

| Périmètre | Résultat | Preuve native |
|---|---:|---|
| Unitaires Auth complets | 116 tests, succès | prt_15ca65245001NaEZ3LhFSuAP5U |
| PostgreSQL final, onze processus/schémas indépendants | 243 cas nommés, succès ; nettoyage et fermeture de toutes connexions | prt_15ca8876f001sJWfHI1Omb7Mf6 |
| Compilation Python modifié, checks Django, dérive modèle/migration | 49 fichiers ; aucun diagnostic ; aucune dérive ; aucune connexion DB | prt_15cab59df001RU8Re0fjWesxLO |
| Django/OpenLDAP réel via fonctions de production inchangées | 4 tests, succès ; processus temporaire arrêté/nettoyé | prt_15b5e06ce00109fYiUmKhij0hO |
| Façades HTTP avec CSRF Django réel, service explicitement simulé | 22 tests, succès ; inclus dans les 116 finaux | prt_15c99aeed001HSO3JAbTLREfI1 |
| Protocole trousseau CLI simulé | 15 tests, succès ; inclus dans les 116 finaux | prt_15c9c1985001ogbzD8SASHfy8p |
| Trousseau natif de l'environnement OpenCode | repli MEMORY réussi, nettoyage confirmé, aucun fichier clair ; Secret Service non qualifié | prt_15c9fa65b001fvYr3hae5zw2AT |

Les 243 cas finaux se répartissent en stockage/migration 22, vérificateur/invocation/métadonnées 42, backend bootstrap 24, commun R01/C04/C05 21, configuration persistée 24, admission 22, retrait/réconciliation 18, rotation 18, justificatifs 18, activité 16 et façades réelles 18. Les préconditions communes réexécutées par des fixtures ne sont pas ajoutées à ce total.

Versions exécutées : Python 3.14.8, Django 6.1.2, PostgreSQL 16.14, argon2-cffi 25.1.0, cryptography 50.0.2 ; Debian 13/OpenLDAP 2.6.10+dfsg-1 pour D11. Argon2id v19 : m=102400 Kio, t=2, p=8, résultat 32 octets, sel au moins 16 octets. La plage Python déclarée n'est pas relevée ; les autres versions de cette plage ne sont pas exécutées. Aucun lint/type checker Python supplémentaire n'est configuré pour ce périmètre. Aucun frontend n'est modifié et aucun test navigateur de produit n'est présenté comme exécuté.

## Correspondance des critères applicables

| Critères | Réalisation et preuve |
|---|---|
| D01/D02/D12, propriétaire Auth et contrats publics | Métadonnées/AuthInvocationSource/CoreFactSource réels ; absence de FK privée Core ; trois Protocols ; façades réelles vérifiées parmi les 243 cas. Cookie Secure/HttpOnly/SameSite=Lax/Path=/ sans Domain, origine/hôte HTTPS, CSRF réel ; API sans fallback cookie ; réponses no-store et absence de jeton web/CLI affichable. |
| D03–D06/D09, politique et temps | Unitaire policy18, vérificateur42, admission22 : politiques plateforme/tenant/scope, refus contradictoires, échéances courantes ; limites 5/2 sur le compte, concurrence du dernier emplacement et remplacement explicite sans clôture silencieuse. |
| D07/D08/D10, rotation et répétitions | Rotation18 : consommation unique, concurrence, réponse perdue, répétition reconnue, arrivée suspecte postérieure ; retrait de la seule session, aucun second secret ; authentification, inactivité et absolu inchangés par rotation. |
| Activité serveur | Activité16 : date d'origine, acteur/session/contexte, fait serveur dédupliqué, booléen/heartbeat/futur/session expirée refusés et rollback si audit échoue ; aucune activité déduite du renouvellement. |
| D13/D14, audit et commit | Admission22, retrait18, rotation18, justificatifs18 et façades18 : participant C05 réel et décideur C04 réel ; rollback avant nouvel accès si audit requis échoue ; retrait seul durable avec pending minimal ; réconciliation reconstruite et autorité fraîche ; commits réels suivis d'erreur => UNKNOWN sans jeton ni changement fictif annoncé. |
| Mot de passe et récupération | Justificatifs18 : moins de 300 secondes exigés ; modification committée et révocation globale, aucune reconnexion automatique ; repli audit avec hash inchangé, retrait global seul et UNCHANGED ; aucune restauration MFA/assurance implicite. |
| D11 | Unitaires password11 et quatre tests OpenLDAP réels : enveloppes Django/LDAP, version/paramètres/sel/résultat préservés, mauvais mot de passe et formats incompatibles refusés sans affaiblissement ; aucune conversion Kerberos/AD ou activation d'annuaire. |
| D15/D16, R01 et confiance | R01 pur22, backend24, commun21, configuration24 : Ed25519, clé préautorisée, mapping, plan exact, fenêtre dix minutes et consommation avec le commit ; autre frontière physique, plan substitué, confiance absente/expirée/révoquée ou snapshot falsifié refusés. |
| D17 | CLI réelle parmi les façades18, protocole trousseau15 et test natif MEMORY : accès mémoire, renouvellement qualifié ou mémoire seule, aucun fichier clair ni session permanente ; issue inconnue/réauthentification retire les références locales. |

Les suites initiales de vérificateur/bootstrap utilisent des doubles Core/confiance explicitement déclarés. Les suites communes, de configuration et de services utilisent ensuite les vraies sources PostgreSQL Auth, CoreFactSource, RuntimeTrustedFactsProvider/RuntimeAuthorizationDecider et PostgresAuditParticipant. Les fixtures de plan, clé opérateur et classification C10 sont déclarées et ne prouvent pas leur activation hôte. Le producteur d'activité C06 est une fixture serveur explicite dans la recette ; aucun producteur réel C06 n'est revendiqué.

Les parcours IdP/OIDC/SAML/WebAuthn/TOTP, enrôlement renforcé, annuaire/KDC et multi-source ne sont pas sélectionnés par ce change local. Les garanties du panneau, du provisionnement global, de l'opérateur INSTALLER hôte, de l'activation C07, de la classification C10 et du P0 global ne sont pas déduites des tests C03. Les exigences canoniques et les responsabilités C06/C07/C08/C10 restent conservées ; ces limites ne créent aucun fallback local ou privilège implicite.

## Incidents corrigés et reprise

Les échecs intermédiaires restent dans le checkpoint. La première recette commune des façades utilisait token_hash au lieu du champ privé digest : test corrigé, schéma nettoyé, puis 18 cas réussis et régression finale réussie. Le premier pilote de régression partageait les settings Django : stockage22 réussi puis refus avant namespace de la deuxième recette ; pilote corrigé pour un processus par recette, sans modification produit. Les anciennes divergences de transcription et demandes non admises ont été réconciliées ; aucun effet consommé n'a été rejoué.

La remédiation CAB/Syncthing est indépendante : voir /home/devops/datas/cab/reports/diagnostic-cab-2026-10-20.md. L'état mutable CAB est exclu de Syncthing, les compteurs/snapshots diagnostics sont corrigés et les tests CAB dédiés sont prouvés dans ce rapport. Le RUN C03 garde son identité parentale et sa nouvelle session autorisée ; aucun autre RUN ni service partagé n'est arrêté.

## Archivage et livraison

Les tâches de réalisation sont cochées après leurs preuves. La seule obligation postérieure à l'archivage, tâche 3.4, reste ouverte jusqu'au rapport STATISTIQUES.md réel et contrôlé, puis est cochée par mandat distinct dans l'archive. Le delta C03 a déjà été adopté/synchronisé dans les canons inchangés ; l'archivage n'applique pas une seconde fois ces deltas. La publication protège les ressources utiles sous resource-scoped-v1, sans exclusion globale et sans interruption des autres RUN. La livraison demande ensuite le gate individuel, le désarmement et la libération ciblée ; l'archive seule ne suffit pas.

## Contrôles documentaires de clôture

Le contrôle OpenSpec strict a réussi pour C03 et pour les 78 canons (78 réussites, zéro échec), natif prt_15cb54ca6001H5zdDjfC9Q4M1z. Les renvois Markdown sont adaptés à la position finale d’archive et vérifiés sous cette position. Les paragraphes Auth de TECHNICAL.md sont réconciliés sans autre modification de cadrage. Le transport documentaire v1 a refusé proposal.md avant écriture ; la cible est restée inchangée, puis le mandat neuf v2 a réussi (prt_15cb4fb5c001nbLS0OxfLH4gS9). Aucun effet consommé n’a été rejoué.
