# Auth local — C03

Module essentiel déclaré `pixs.auth` 0.1.0 ; capacité locale `auth.local` 1.0.0, requise sans fallback. Le manifest commun `component.toml` et les mécanismes Kernel de résolution/lifecycle s'appliquent. Une installation ne crée aucune confiance et ne vaut pas activation applicative.

## Contrats publics

`contracts.py` expose les DTO et trois Protocols versionnés 1.0.0 : AuthenticationService, SessionService et CredentialService. PostgresLocalAuthService les implémente ; aucune table Django privée ne constitue un port public. Les références numériques Core sont les URI `pixs.core.identity:<UUIDv7>` validées par les ports publics Core.

La composition serveur fournit explicitement alias/peer_alias, profile_id, horloge UTC fiable, sources de confiance et d'assurance, CoreFactSource, participant C05 PostgreSQL, source de classification et factory C04 RuntimeAuthorizationDecider. `configuration.create_local_auth_sources` fournit les deux sources PostgreSQL de production. L'absence, l'expiration ou la révocation d'une sélection approuvée ferme l'accès. L'assurance CLAIMED initiale est explicite ; aucun niveau supérieur ou MFA n'est déduit.

La factory de décideur reçoit les arguments nommés request, operation_id et authentication_source. AuthInvocationSource reconstitue la preuve native dans chaque frontière physique ; un DTO ou une ancienne décision ALLOW ne prouve aucune autorité actuelle. Bootstrap R01 utilise AuthBootstrapBackend et une sélection initiale explicitement autorisée, sans session de la base cible. C08 possède l'orchestration de provisionnement.

## Persistance et opérations

Enregistrer explicitement les apps de `apps.DJANGO_REQUIRED_APPS`. `migration_lock.run_auth_initial(alias, origin=None, target="0.1.0")` applique la migration propriétaire 0001, onze tables privées. Le verrou advisory appartient à la même connexion physique PostgreSQL ; un schéma partiel ou inconnu est refusé. Aucune migration n'est lancée à l'import ou par simple découverte.

Connexion et renouvellement n'émettent leurs justificatifs qu'après commit Auth/C05 commun. Une répétition ou réponse perdue ne restitue jamais de secret. Le renouvellement consomme un REFRESH une seule fois ; sa répétition reconnue ou concurrence antérieure ne réémet rien. Une réutilisation postérieure suspecte retire seulement la session reconnue. Les dates d'authentification, d'activité et d'expiration absolue ne sont pas prolongées par le renouvellement.

D14 autorise le seul retrait durable en cas de panne d'audit. L'opération et son événement minimal sont persistés, puis reconcile_audit revalide une autorité actuelle et vérifie les colonnes propriétaires ; une ancienne décision ou un JSON modifié ne suffit pas. Le changement/récupération échoue sans changement de mot de passe si l'audit requis manque ; le repli retire les accès seuls. Un commit non vérifiable retourne UNKNOWN et ne remet aucun jeton.

## Façades et activité

WebAuthFacade et ApiAuthFacade sont des adaptateurs explicitement montés par l'hôte C06/N04. Hôte/origine HTTPS sont obligatoires. Le web utilise un cookie `__Host-pixs-session`, Secure/HttpOnly/SameSite=Lax/Path=/, sans Domain, plafonné par l'absolu ; CSRF Django réel et origine exacte protègent les mutations. Aucun justificatif Auth n'est remis au JavaScript. L'API/CLI utilise Bearer opaque, sans repli cookie. Les réponses Auth portent no-store. Aucun serveur HTTP, route, écoute réseau ou frontend n'est activé par ces modules.

CliAuthFacade réutilise les contrats et services, garde l'accès en mémoire et conserve le REFRESH dans un trousseau Secret Service seulement qualifié dans le processus. `cli_vault.select_refresh_vault` teste un namespace aléatoire indépendant et le nettoie ; sinon MemoryRefreshVault est choisi, sans fichier clair. Le résultat affichable CliAuthStatus ne contient aucun jeton. La qualification native C03 a constaté MEMORY dans l'environnement OpenCode ; elle ne prouve pas un trousseau disponible sur un poste utilisateur. La fermeture du processus termine les références mémoire ; elle ne remplace pas une révocation serveur explicite.

`activity.UserActivityEvidence` est un fait obtenu d'un port serveur de confiance fourni par C06 ; booléen client, heartbeat et renouvellement ne valent pas activité. La date d'origine et les références acteur/session/contexte doivent correspondre. Le même fait ne prolonge jamais l'inactivité par répétition. Le producteur C06 reste distinct de la fixture de recette C03.

## Qualification et limites

Les recettes dédiées figurent dans tests/unit/test_auth_*.py et tests/integration/test_auth_*_postgres.py. Le banc PostgreSQL utilise exclusivement des schémas jetables dont l'OID et le propriétaire sont prouvés ; chaque recette possède son processus Django. Les accès privés sont chargés uniquement par ce processus et les sorties sont filtrées. Les fixtures de plan, clé opérateur, classification C10 et activité sont déclarées explicitement. Les preuves natives et versions réellement exécutées sont consignées dans la VALIDATION du change C03.

La bibliothèque ne livre pas les routes C06, la composition et l'hôte C07, l'orchestration C08, une activation C10 ou un P0 global. Aucun connecteur externe, IdP, OpenLDAP ou KDC n'est installé/activé par défaut. Le banc D11 qualifie une adaptation d'enveloppe Argon2id Django/OpenLDAP sans service durable. Les paramètres Argon2id restent ceux du profil qualifié, sans conversion en clé Kerberos ni baisse de protection.
