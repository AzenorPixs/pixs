# Exigences de réalisation — C03

La matrice ci-dessous référence le canon sans l’altérer. Le [delta authentication](specs/authentication/spec.md) des décisions du 20 octobre 2026 est adopté et intégré au canon. Les textes canoniques et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 adopté le 18 octobre 2026 ne supprime aucun MUST existant.

Les statuts P/ND et lignes des tableaux ci-dessous décrivent l’instant de préparation documentaire. Ils ne constituent pas des verdicts actuels. La qualification C03 du 21 octobre 2026 est détaillée dans VALIDATION.md et la section finale de design.md ; les scénarios C06/C07/C08/C10 et des profils non sélectionnés y restent explicitement distincts. Les empreintes canoniques sont recontrôlées avant clôture.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| authentication / 8 | [Fournisseurs déclarés et confiance explicite](../../../specs/authentication/spec.md#L8) | P | Émetteur non approuvé refusé |
| authentication / 17 | [Identifiant externe canonique et liaison explicite](../../../specs/authentication/spec.md#L17) | P | Courriel seul non rapproché |
| authentication / 28 | [Sessions bornées et révocation propagée](../../../specs/authentication/spec.md#L28) | P | Révocation propagée ; Retrait sans audit confirmé |
| identity-assurance / 8 | [Assurance et exception Super Admin](../../../specs/identity-assurance/spec.md#L8) | P | Secours avec assurance réellement obtenue |
| identity-assurance / 17 | [Contexte vérifié et dimensions distinctes](../../../specs/identity-assurance/spec.md#L17) | P | Claim absent sans surclassement |
| identity-assurance / 28 | [Seuil sensible et élévation explicite](../../../specs/identity-assurance/spec.md#L28) | P | Élévation exigée |
| identity-assurance / 37 | [Fraîcheur, révocation et récupération sans élévation implicite](../../../specs/identity-assurance/spec.md#L37) | P | Récupération sans restauration d'assurance |
| identity-assurance / 48 | [Vocabulaire structurel préparatoire IdentityAssurance v1](../../../specs/identity-assurance/spec.md#L48) | ND | Valeurs fermées sans effet ; Valeur étrangère refusée ; Absence sans défaut implicite |
| identity-assurance / 67 | [Absence d'effets du vocabulaire IdentityAssurance v1](../../../specs/identity-assurance/spec.md#L67) | ND | Valeur représentée sans assurance calculée |
| initial-administration / 11 | [Compte Super Admin unique de paramétrage et de secours](../../../specs/initial-administration/spec.md#L11) | ND | Compte fonctionnel non nominatif ; Second compte et transfert refusés |
| initial-administration / 25 | [Exception liée au compte actif](../../../specs/initial-administration/spec.md#L25) | ND | Privilège permanent du compte actif |
| initial-administration / 34 | [Absence de MFA obligatoire au démarrage et au secours](../../../specs/initial-administration/spec.md#L34) | ND | Premier démarrage sans MFA ; Réactivation de secours sans MFA |
| initial-administration / 49 | [Modes de démarrage explicites](../../../specs/initial-administration/spec.md#L49) | ND | Marqueur externe indisponible |
| initial-administration / 63 | [Première configuration et transitions de mode](../../../specs/initial-administration/spec.md#L63) | ND | État initial en base distinct du marqueur |
| initial-administration / 75 | [Provisionnement interactif de la base](../../../specs/initial-administration/spec.md#L75) | ND | Base migrable |
| initial-administration / 90 | [Reprise et références de secrets après provisionnement](../../../specs/initial-administration/spec.md#L90) | ND | Référence de secret après provisionnement |
| initial-administration / 105 | [Création conditionnelle du Super Admin](../../../specs/initial-administration/spec.md#L105) | ND | Mots de passe différents ; Compte fonctionnel créé explicitement |
| initial-administration / 126 | [Réutilisation du Super Admin d'une base conservée](../../../specs/initial-administration/spec.md#L126) | ND | Base conforme conservée |
| initial-administration / 136 | [Marqueur externe et première configuration](../../../specs/initial-administration/spec.md#L136) | ND | Configuration initiale inachevée |
| initial-administration / 152 | [Panneau d'administration contrôlé](../../../specs/initial-administration/spec.md#L152) | ND | Administrateur ordinaire soumis aux ACL |
| initial-administration / 165 | [Changement contrôlé de la route d'administration](../../../specs/initial-administration/spec.md#L165) | ND | Ancienne route d'administration |
| initial-administration / 177 | [Expérience et état du panneau](../../../specs/initial-administration/spec.md#L177) | ND | Santé réservée au root |
| initial-administration / 192 | [Désactivation externe du Super Admin](../../../specs/initial-administration/spec.md#L192) | ND | Connexion root désactivée ; Secours malgré le marqueur de désactivation ; Transaction engagée lors de la désactivation |
| initial-administration / 218 | [Opérateur technique INSTALLER avant base et sessions](../../../specs/initial-administration/spec.md#L218) | ND | Opérateur non vérifiable ; Root OS sans privilège applicatif implicite |
| initial-administration / 232 | [Limites et refus de la phase technique INSTALLER](../../../specs/initial-administration/spec.md#L232) | ND | Opérateur non vérifiable ; Root OS sans privilège applicatif implicite |
| installation-provisioning / 9 | [Provisionnement du compte fonctionnel de secours](../../../specs/installation-provisioning/spec.md#L9) | ND | Provisionnement sans compte nominatif ni MFA |
| installation-provisioning / 18 | [Provisionnement explicite et états inspectables](../../../specs/installation-provisioning/spec.md#L18) | ND | Installation non provisionnée |
| installation-provisioning / 30 | [Configuration et secrets vérifiés avant mise en service](../../../specs/installation-provisioning/spec.md#L30) | ND | Référence de secret indisponible |
| installation-provisioning / 42 | [Opérateur initial explicite et sans privilège implicite](../../../specs/installation-provisioning/spec.md#L42) | ND | Identité opérateur absente |
| installation-provisioning / 55 | [Création tenant-scoped contrôlée](../../../specs/installation-provisioning/spec.md#L55) | ND | Rejou du provisionnement du premier tenant |
| installation-provisioning / 68 | [Reprise contrôlée et auditée](../../../specs/installation-provisioning/spec.md#L68) | ND | Interruption avant mise en service |

Les quatre rattachements ajoutés lors de la relecture du 20 octobre 2026 portent sur des exigences déjà canoniques ; ils n'ajoutent aucune exigence ni aucun scénario. Leur statut ND concerne le raccordement à C03, sans réévaluer les preuves propres aux profils structurels ou à C01. Le vocabulaire IdentityAssurance v1 ne prouve aucune authentification ; l'opérateur technique INSTALLER reste indépendant des sessions Pixs et ne reçoit aucune exception Super Admin de son identité OS. Aucun test produit n'est exécuté par cette relecture.

Les trois deltas d'architecture Auth adoptés le 20 octobre 2026 ajoutent les dix rattachements ci-dessous : six clauses authentication, deux core et deux reference-composition, dont la clause P0 existante modifiée. ND désigne leur réalisation C03 non démontrée ; aucune preuve fonctionnelle n'est déduite de l'adoption.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| authentication / 40 | [Module essentiel autonome pixs.auth](../../../specs/authentication/spec.md#L40) | ND | Composition applicative sans Auth ; Fixture structurelle isolée |
| authentication / 52 | [Autonomie locale et PostgreSQL par défaut](../../../specs/authentication/spec.md#L52) | ND | Installation autonome ; PostgreSQL indisponible |
| authentication / 64 | [Propriété des données Auth et protection des justificatifs](../../../specs/authentication/spec.md#L64) | ND | Session persistée ; Liaison avec Core |
| authentication / 76 | [Sous-modules Auth composés par les mécanismes communs](../../../specs/authentication/spec.md#L76) | ND | Source installée sans confiance |
| authentication / 84 | [Politiques Auth déclaratives et contextualisées](../../../specs/authentication/spec.md#L84) | ND | Politique contradictoire |
| authentication / 92 | [Absence de repli implicite entre méthodes et sources](../../../specs/authentication/spec.md#L92) | ND | IdP externe indisponible ; Secours propre du Super Admin |
| core / 116 | [Frontière Core Auth et dépendance unidirectionnelle](../../../specs/core/spec.md#L116) | ND | Révocation canonique |
| core / 124 | [Moyens multiples sans multiplication implicite des identités](../../../specs/core/spec.md#L124) | ND | Passkey et principal pour une identité |
| reference-composition / 10 | [Capacités obligatoires du P0](../../../specs/reference-composition/spec.md#L10) | ND | Capacité P0 absente |
| reference-composition / 114 | [Profil Auth standard sans connecteur externe installé](../../../specs/reference-composition/spec.md#L114) | ND | Profil livré sans connecteurs externes |

## Empreintes SHA-256 du canon

- `openspec/specs/authentication/spec.md` : `8c3a41d0f1c5531b9c15954c547b9970261a864812633a2db23944fe2b17ad4a`.
- `openspec/specs/identity-assurance/spec.md` : `0c1693efb3e8c22afd53c96783fd39735654ad315f0872c86ae76db6cadb1fd5`.
- `openspec/specs/initial-administration/spec.md` : `a875dfd4e48cc2920ea38242b02c46aab386a7a77b645165d009d9fa47f4cc4a`.
- `openspec/specs/installation-provisioning/spec.md` : `2d33df47ef9ad0c073c4e0d7677c98e3cd96cb8e3b6866894c6d3cb7d305e7b4`.

- `openspec/specs/core/spec.md` : `1332388a595ac64fcc6ca8ce3fe8e70c9b371a9f038e820ec8ab48364ea92666`.
- `openspec/specs/reference-composition/spec.md` : `55de6c615f02df5148be2e3a7808929cfc2651ca451cd423bc3ab6cad38f9668`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.

## Raccordement à l'architecture Auth adoptée le 20 octobre 2026

Le [change d'architecture Auth](../../define-essential-autonomous-auth-module/proposal.md) porte les trois deltas désormais intégrés au canon pour pixs.auth essentiel indépendant, local autonome sur PostgreSQL par défaut. Les [méthodes locales/MFA](../../add-auth-local-authenticators-and-mfa/proposal.md) et l'[enrôlement](../../add-auth-identity-enrollment/proposal.md) restent proposés dans leurs dossiers propres. Les scénarios adoptés sont raccordés à la matrice ; leurs preuves C03/C08/C17 restent à produire, sans recette exécutée par cette adoption.

Les [arbitrages D01–D17](design.md#arbitrages-de-réalisation-à-valider) sont arrêtés et documentés ; les deltas concernés sont adoptés et les qualifications détaillées restent préalables à toute réalisation autorisée. Les références et les empreintes correspondent au canon après adoption des dix-sept décisions ; elles restent à recontrôler avant réalisation. Aucun scénario C03/C08/C17 n’est déclaré exécuté.

## Raccordement des décisions du 20 octobre 2026

| Décisions | Exigences propriétaires adoptées | Critères futurs |
|---|---|---|
| D01/D02/D12 | [C03 authentication](specs/authentication/spec.md), [N04 api](../../define-p0-web-serving-and-security-boundary/specs/api/spec.md), [C06](../../add-protected-core-http-commands-and-queries/design.md) | Façades explicitement distinctes ; cookie inaccessible au JavaScript et CSRF ; Bearer opaque ; interfaces spécialisées sans accès privé Core. |
| D03–D06/D09 | [C03 authentication](specs/authentication/spec.md) | Inactivité 60/15 minutes ; absolu 12/2 heures ; fraîcheur moins de 5 minutes ; accès 15 minutes ; limites 5/2 et choix explicite sans fermeture silencieuse. |
| D07/D08/D10 | [C03 authentication](specs/authentication/spec.md) | Une seule rotation concurrente ; aucune seconde émission sur répétition ; réponse perdue sans secret restituable ; révocation de session ciblée ou globale selon cause. |
| D11 | [C03 authentication](specs/authentication/spec.md) | Argon2id Django/argon2-cffi ; paramètres qualifiés ; réutilisation OpenLDAP vérifiée par adaptation d’enveloppe, sans baisse de protection ni service activé. |
| D13/D14 | [C05 audit](../2026-10-21-add-durable-minimized-audit/specs/audit/spec.md) et [C04 authorization](../2026-10-21-integrate-runtime-authorization-and-super-admin/specs/authorization/spec.md) | Commit commun requis pour connexion/renouvellement ; retrait seul malgré panne d’audit ; persistance du retrait et réconciliation ; Auth indisponible ou issue inconnue sans succès annoncé. |
| D15/D16 | [C04 authorization](../2026-10-21-integrate-runtime-authorization-and-super-admin/specs/authorization/spec.md) et [C08 R01](../../add-installation-and-first-configuration/design.md) | Clé préautorisée, signature Ed25519, mapping explicite sans session cible ; 10 minutes et consommation unique au commit ; plan/cible divergents refusés, reprise inspectée. |
| D17 | [C03 authentication](specs/authentication/spec.md) | Trousseau qualifié disponible, sinon mémoire du processus ; aucun fichier clair ni session permanente créée. |

Les durées et plafonds restent configurables par politique. Les exceptions canoniques du seul Super Admin et les contrôles d’assurance réellement obtenue restent préservés. Les 41 rattachements canoniques précédents ne sont ni des deltas ni une preuve produit ; la table des décisions relie les critères adoptés et la matrice complémentaire ci-dessous les référence au canon.


## Exigences canoniques issues des dix-sept décisions

Adoption documentaire du 20 octobre 2026 : 31 exigences ajoutées, 8 modifiées et 43 scénarios supplémentaires nets dans authentication, authorization, audit et api. Les sources des deltas restent conservées ; aucun archivage ni scénario produit exécuté. ND représente la réalisation non démontrée, sans requalification des preuves antérieures.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| authentication / 104 | [Interfaces spécialisées du profil Auth local](../../../specs/authentication/spec.md#L104) | ND | Session liée à Core |
| authentication / 112 | [Justificatifs opaques et stockage serveur par empreinte](../../../specs/authentication/spec.md#L112) | ND | Justificatif brut absent |
| authentication / 120 | [État Auth courant requis](../../../specs/authentication/spec.md#L120) | ND | État inaccessible |
| authentication / 128 | [Durées des sessions locales ordinaires](../../../specs/authentication/spec.md#L128) | ND | Inactivité ordinaire ; Plafond administratif |
| authentication / 140 | [Durée des accès et fraîcheur sensible](../../../specs/authentication/spec.md#L140) | ND | Validité restante courte ; Fraîcheur insuffisante |
| authentication / 152 | [Politique configurable et exceptions canoniques](../../../specs/authentication/spec.md#L152) | ND | Politique résolue |
| authentication / 160 | [Renouvellement rotatif à usage unique](../../../specs/authentication/spec.md#L160) | ND | Rotation réussie |
| authentication / 168 | [Activité utilisateur et renouvellement](../../../specs/authentication/spec.md#L168) | ND | Renouvellements seuls |
| authentication / 176 | [Concurrence et réponse perdue de rotation](../../../specs/authentication/spec.md#L176) | ND | Deux appels concurrents ; Réponse perdue |
| authentication / 188 | [Réutilisation suspecte et révocation de session](../../../specs/authentication/spec.md#L188) | ND | Réutilisation suspecte |
| authentication / 196 | [Plafond et remplacement explicite des sessions](../../../specs/authentication/spec.md#L196) | ND | Limite atteinte ; Admissions concurrentes |
| authentication / 208 | [Onglets et renouvellements sans nouvelle session](../../../specs/authentication/spec.md#L208) | ND | Même cookie |
| authentication / 216 | [Changement de mot de passe sans reconnexion automatique](../../../specs/authentication/spec.md#L216) | ND | Mot de passe changé |
| authentication / 224 | [Récupération et compromission du mot de passe](../../../specs/authentication/spec.md#L224) | ND | Récupération sans MFA ; Changement non confirmé |
| authentication / 236 | [Argon2id via les outils Django](../../../specs/authentication/spec.md#L236) | ND | Paramètres qualifiés |
| authentication / 244 | [Réutilisation Argon2id dans un profil OpenLDAP qualifié](../../../specs/authentication/spec.md#L244) | ND | Vérification croisée ; Profil incompatible |
| authentication / 256 | [Limites de la compatibilité des empreintes](../../../specs/authentication/spec.md#L256) | ND | Compatibilité documentaire seule |
| authentication / 264 | [Conservation du renouvellement de la CLI interactive](../../../specs/authentication/spec.md#L264) | ND | Trousseau indisponible |
| authorization / 112 | [Opérateur pré-session R01 lié à une confiance explicite](../../../specs/authorization/spec.md#L112) | ND | Première installation sans session |
| authorization / 120 | [Signature Ed25519 de la preuve d’amorçage](../../../specs/authorization/spec.md#L120) | ND | Plan substitué |
| authorization / 128 | [Aucune autorité implicite de bootstrap](../../../specs/authorization/spec.md#L128) | ND | Clé autoautorisée |
| authorization / 136 | [Autorisation finale R01 de dix minutes et usage unique](../../../specs/authorization/spec.md#L136) | ND | Consommation au commit |
| authorization / 144 | [Revalidation et reprise de l’amorçage](../../../specs/authorization/spec.md#L144) | ND | Expiration ou nouveau plan ; Commit puis réponse perdue |
| authorization / 43 | [Priorité transversale de l'exception Super Admin](../../../specs/authorization/spec.md#L43) | ND | Compte ordinaire sans exception ; Contrat structurel sans privilège |
| authorization / 57 | [Modèle Subject Resource Action Context](../../../specs/authorization/spec.md#L57) | ND | Propriété sans politique refusée ; Sujet technique avant identité applicative ; Opérateur R01 sans session cible |
| authorization / 76 | [Priorité DENY puis ALLOW puis refus](../../../specs/authorization/spec.md#L76) | ND | Conflit DENY contre ALLOW |
| audit / 356 | [Transaction commune des sessions et de leur audit requis](../../../specs/audit/spec.md#L356) | ND | Création et audit liés |
| audit / 364 | [Audit requis avant tout nouvel accès ordinaire](../../../specs/audit/spec.md#L364) | ND | Audit échoué à la création ; Réponse perdue après renouvellement |
| audit / 376 | [Retrait d’accès Auth prioritaire lors d’une panne d’audit](../../../specs/audit/spec.md#L376) | ND | Déconnexion malgré panne audit |
| audit / 384 | [Contrôles et exclusions du retrait prioritaire](../../../specs/audit/spec.md#L384) | ND | Nouvel accès refusé ; Auteur non vérifiable |
| audit / 396 | [Retrait durable et réconciliation de son audit manquant](../../../specs/audit/spec.md#L396) | ND | Audit manquant signalé |
| audit / 404 | [Frontière transactionnelle et preuve du retrait](../../../specs/audit/spec.md#L404) | ND | Auth ou commit non vérifiable ; Opération composée |
| audit / 8 | [Audit dérogeable du Super Admin](../../../specs/audit/spec.md#L8) | ND | Opération Super Admin sans audit persistant ; Audit ordinaire toujours obligatoire |
| audit / 23 | [Portée de l'exception dans les exigences d'audit](../../../specs/audit/spec.md#L23) | ND | Profil d'occultation inchangé |
| audit / 50 | [Périmètre obligatoire d'audit](../../../specs/audit/spec.md#L50) | ND | Opération destructive sans audit |
| audit / 77 | [Audit exhaustif du panneau d'administration](../../../specs/audit/spec.md#L77) | ND | Navigation non auditable |
| api / 49 | [Façade web à cookie et API Bearer explicitement distinctes](../../../specs/api/spec.md#L49) | ND | Cookie seul sur route Bearer |
| api / 57 | [Contrats de transport et stockage navigateur](../../../specs/api/spec.md#L57) | ND | Façade web authentifiée |

### Empreintes complémentaires du canon adopté

- `openspec/specs/authorization/spec.md` : `c09e4dac79ecbe6bdb16550d8a4d1566307127818cdeaf9dfbe9224f50858310`.
- `openspec/specs/audit/spec.md` : `19c58dc8b16e537967c46e69fca4132867e98ada591980b67872ee8c382a5eb1`.
- `openspec/specs/api/spec.md` : `7e3c27a0211e357f3bb2b51e58ae8d73c4846db660c6395a3cdda3b0adcd69fe`.


## Qualification de réalisation du 21 octobre 2026

Les preuves natives de VALIDATION.md couvrent le profil local sélectionné, ses refus, les trois façades, R01, les limites de sessions, les renouvellements, les retraits D14 et leur réconciliation. Les 116 tests unitaires et 243 cas PostgreSQL finaux ne requalifient pas automatiquement les lignes ND de provisionnement, de panneau d’administration, de MFA, de sources externes ou de P0 appartenant à d’autres changes. Le banc D11 exécute quatre cas OpenLDAP réels sans annuaire durable ; le trousseau natif non qualifié conduit au mode mémoire prévu par D17. Les conditions et producteurs explicitement simulés sont indiqués dans la validation.
