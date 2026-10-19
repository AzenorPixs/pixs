# Exigences de réalisation — C13

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 adopté le 18 octobre 2026 et intégré au canon apporte les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| accessibility / 8 | [Niveau cible WCAG 2.2 AA](../../specs/accessibility/spec.md#L8) | P | Contribution non conforme |
| accessibility / 17 | [Fonctionnement clavier et technologies d'assistance](../../specs/accessibility/spec.md#L17) | P | Parcours clavier complet |
| accessibility / 26 | [Sémantique native préservée](../../specs/accessibility/spec.md#L26) | P | Rôle ARIA redondant |
| accessibility / 35 | [Validation outillée et manuelle combinées](../../specs/accessibility/spec.md#L35) | P | Défaut non détectable automatiquement |
| audit / 8 | [Audit dérogeable du Super Admin](../../specs/audit/spec.md#L8) | P | Opération Super Admin sans audit persistant ; Audit ordinaire toujours obligatoire |
| audit / 23 | [Portée de l'exception dans les exigences d'audit](../../specs/audit/spec.md#L23) | P | Profil d'occultation inchangé |
| audit / 32 | [Audit fonctionnel distinct des logs techniques](../../specs/audit/spec.md#L32) | P | Perte de télémétrie technique |
| audit / 41 | [Contenu minimal d'un événement d'audit](../../specs/audit/spec.md#L41) | P | Refus d'autorisation tracé |
| audit / 50 | [Périmètre obligatoire d'audit](../../specs/audit/spec.md#L50) | P | Opération destructive sans audit |
| audit / 59 | [Append-only et réécriture contrôlée](../../specs/audit/spec.md#L59) | P | Obligation d'effacement |
| audit / 68 | [Minimisation et non-duplication des données](../../specs/audit/spec.md#L68) | P | Payload sensible détecté |
| audit / 77 | [Audit exhaustif du panneau d'administration](../../specs/audit/spec.md#L77) | P | Navigation non auditable |
| authorization / 8 | [Portée du contrôle total du Super Admin](../../specs/authorization/spec.md#L8) | P | Tenant non accordé au Super Admin ; Tenant accordé malgré un refus ACL |
| authorization / 23 | [Exception Super Admin dans toutes les interfaces](../../specs/authorization/spec.md#L23) | P | Même exception selon la façade |
| authorization / 33 | [Contrôles applicatifs dérogeables par le Super Admin](../../specs/authorization/spec.md#L33) | P | Contrôle applicatif dérogé |
| authorization / 43 | [Priorité transversale de l'exception Super Admin](../../specs/authorization/spec.md#L43) | P | Compte ordinaire sans exception ; Contrat structurel sans privilège |
| authorization / 57 | [Modèle Subject Resource Action Context](../../specs/authorization/spec.md#L57) | P | Propriété sans politique refusée |
| authorization / 66 | [Priorité DENY puis ALLOW puis refus](../../specs/authorization/spec.md#L66) | P | Conflit DENY contre ALLOW |
| authorization / 77 | [Évaluation applicative avant exposition](../../specs/authorization/spec.md#L77) | P | Liste filtrée à la source |
| authorization-engine / 8 | [Exception Super Admin distincte des profils préparatoires](../../specs/authorization-engine/spec.md#L8) | P | Profils préparatoires sans privilège ajouté |
| authorization-engine / 17 | [Politiques déclaratives versionnées](../../specs/authorization-engine/spec.md#L17) | P | Politique à code rejetée |
| authorization-engine / 26 | [Décisions et filtrage tracés](../../specs/authorization-engine/spec.md#L26) | P | Décision périmée non réutilisée |
| authorization-engine / 37 | [Groupes bornés et délégation auditée](../../specs/authorization-engine/spec.md#L37) | P | Moteur indisponible |
| authorization-engine / 48 | [Profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L48) | P | Sélecteur générique refusé |
| authorization-engine / 57 | [Conditions typées du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L57) | P | Booléen distinct d'un entier |
| authorization-engine / 68 | [Assurances et faits du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L68) | P | Fait inconnu refusé fermé ; Assurances non substituables |
| authorization-engine / 82 | [Limites et obligations du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L82) | P | Obligation inconnue rejetée |
| authorization-engine / 91 | [Obligations honorées par le PEP du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L91) | P | ALLOW minimal avec obligation honorée |
| authorization-engine / 100 | [Snapshot et priorité du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L100) | P | DENY prévaut sur ALLOW mêmes cibles |
| authorization-engine / 109 | [Calcul d'expiration du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L109) | P | Auth expirée malgré TTL |
| authorization-engine / 120 | [Transitions temporelles et réévaluation du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L120) | P | ALLOW expire à activation future DENY |
| authorization-engine / 129 | [Confiance backend et diagnostics du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L129) | P | Booléen client insuffisant |
| authorization-engine / 140 | [Plateforme et intertenant du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L140) | P | Intertenant minimal refusé ; Plateforme ALLOW explicite ; Plateforme sans explicite refusée |
| design-system / 8 | [Tokens sémantiques d'intention](../../specs/design-system/spec.md#L8) | P | Valeur brute refusée |
| design-system / 17 | [Primitives à API stable](../../specs/design-system/spec.md#L17) | P | Variante non déclarée |
| design-system / 26 | [Cohérence Light et Dark par les tokens](../../specs/design-system/spec.md#L26) | P | Primitive inspectée dans les deux modes |
| design-system / 35 | [Adapter de rendu sans contournement](../../specs/design-system/spec.md#L35) | P | Accès direct au moteur refusé |
| frontend / 8 | [Contributions déclarées et routage sans collision](../../specs/frontend/spec.md#L8) | P | Route ambiguë bloquée |
| frontend / 17 | [Session fournie par le shell et autorisation applicative](../../specs/frontend/spec.md#L17) | P | Garde frontale non substitutive |
| frontend / 26 | [Mutations provisoires et invalidation tenant-aware](../../specs/frontend/spec.md#L26) | P | Invalidation après commande |
| frontend / 37 | [Sous-modularité frontend par le modèle de composants commun](../../specs/frontend/spec.md#L37) | P | Sous-module optionnel isolé |
| initial-administration / 11 | [Compte Super Admin unique de paramétrage et de secours](../../specs/initial-administration/spec.md#L11) | ND | Compte fonctionnel non nominatif ; Second compte et transfert refusés |
| initial-administration / 25 | [Exception liée au compte actif](../../specs/initial-administration/spec.md#L25) | ND | Privilège permanent du compte actif |
| initial-administration / 34 | [Absence de MFA obligatoire au démarrage et au secours](../../specs/initial-administration/spec.md#L34) | ND | Premier démarrage sans MFA ; Réactivation de secours sans MFA |
| initial-administration / 49 | [Modes de démarrage explicites](../../specs/initial-administration/spec.md#L49) | ND | Marqueur externe indisponible |
| initial-administration / 63 | [Première configuration et transitions de mode](../../specs/initial-administration/spec.md#L63) | ND | État initial en base distinct du marqueur |
| initial-administration / 75 | [Provisionnement interactif de la base](../../specs/initial-administration/spec.md#L75) | ND | Base migrable |
| initial-administration / 90 | [Reprise et références de secrets après provisionnement](../../specs/initial-administration/spec.md#L90) | ND | Référence de secret après provisionnement |
| initial-administration / 105 | [Création conditionnelle du Super Admin](../../specs/initial-administration/spec.md#L105) | ND | Mots de passe différents ; Compte fonctionnel créé explicitement |
| initial-administration / 126 | [Réutilisation du Super Admin d'une base conservée](../../specs/initial-administration/spec.md#L126) | ND | Base conforme conservée |
| initial-administration / 136 | [Marqueur externe et première configuration](../../specs/initial-administration/spec.md#L136) | ND | Configuration initiale inachevée |
| initial-administration / 152 | [Panneau d'administration contrôlé](../../specs/initial-administration/spec.md#L152) | ND | Administrateur ordinaire soumis aux ACL |
| initial-administration / 165 | [Changement contrôlé de la route d'administration](../../specs/initial-administration/spec.md#L165) | ND | Ancienne route d'administration |
| initial-administration / 177 | [Expérience et état du panneau](../../specs/initial-administration/spec.md#L177) | ND | Santé réservée au root |
| initial-administration / 192 | [Désactivation externe du Super Admin](../../specs/initial-administration/spec.md#L192) | ND | Connexion root désactivée ; Secours malgré le marqueur de désactivation ; Transaction engagée lors de la désactivation |
| installation-provisioning / 9 | [Provisionnement du compte fonctionnel de secours](../../specs/installation-provisioning/spec.md#L9) | ND | Provisionnement sans compte nominatif ni MFA |
| installation-provisioning / 18 | [Provisionnement explicite et états inspectables](../../specs/installation-provisioning/spec.md#L18) | ND | Installation non provisionnée |
| installation-provisioning / 30 | [Configuration et secrets vérifiés avant mise en service](../../specs/installation-provisioning/spec.md#L30) | ND | Référence de secret indisponible |
| installation-provisioning / 42 | [Opérateur initial explicite et sans privilège implicite](../../specs/installation-provisioning/spec.md#L42) | ND | Identité opérateur absente |
| installation-provisioning / 55 | [Création tenant-scoped contrôlée](../../specs/installation-provisioning/spec.md#L55) | ND | Rejou du provisionnement du premier tenant |
| installation-provisioning / 68 | [Reprise contrôlée et auditée](../../specs/installation-provisioning/spec.md#L68) | ND | Interruption avant mise en service |
| internationalization / 8 | [Catalogues par composant et langue canonique](../../specs/internationalization/spec.md#L8) | P | Clé manquante bloquée |
| internationalization / 17 | [Résolution déterministe et formats localisés](../../specs/internationalization/spec.md#L17) | P | Valeur métier préservée ; Préférence navigateur avant défaut d'installation |
| security / 8 | [Exception applicative réservée au Super Admin](../../specs/security/spec.md#L8) | P | Revendication root sans authentification propre |
| security / 17 | [Profil de sécurité déclaré par composant](../../specs/security/spec.md#L17) | P | Vulnérabilité critique bloquante |
| security / 26 | [Échec fermé sans mode permissif](../../specs/security/spec.md#L26) | P | Contexte non vérifiable refusé |
| security / 37 | [Diagnostics sans exposition sensible](../../specs/security/spec.md#L37) | P | Secret hors journaux |
| themes / 8 | [Modes clair et sombre obligatoires](../../specs/themes/spec.md#L8) | P | Bascule sans rechargement |
| themes / 17 | [Tokens sémantiques sans valeurs codées](../../specs/themes/spec.md#L17) | P | Valeur codée rejetée |

## Empreintes SHA-256 du canon

- `openspec/specs/accessibility/spec.md` : `a3f9275d101b121d225c2975931a567b5ffed9d512ea22185bb28094e5821baf`.
- `openspec/specs/audit/spec.md` : `43d8dd9947fbac84c5decbf829825db577276853f5224e5bacc021c22bf4f513`.
- `openspec/specs/authorization-engine/spec.md` : `bd9de765f72d4700da314f81dbce9d3d0ee532f3bcc5be319f005ffbfd18b20b`.
- `openspec/specs/authorization/spec.md` : `87c9799579008033f39e47a579b8bf536f0d9c8973d678750a540a02ea63166f`.
- `openspec/specs/design-system/spec.md` : `c5ff33414eda8c66695366e189038db1f311f428e2e5e19b774907421131778e`.
- `openspec/specs/frontend/spec.md` : `e646e3faf793db109a93f803423cfa4606deeb67b91d4b3301fa219e82cf9414`.
- `openspec/specs/initial-administration/spec.md` : `200ce5a01e6d741d9021b2c78dd7f31efd7eeed566309168c0f3fbf468b5c4e5`.
- `openspec/specs/installation-provisioning/spec.md` : `2d33df47ef9ad0c073c4e0d7677c98e3cd96cb8e3b6866894c6d3cb7d305e7b4`.
- `openspec/specs/internationalization/spec.md` : `72a1a1756ae168e16d51055edeaa44786894caf20cc420c96ce9bb3da8907232`.
- `openspec/specs/security/spec.md` : `c033c6fa6a6fc43d6e7e3295cd7dc7f554bbcbe0c12cb9baf0431acd6f7a685f`.
- `openspec/specs/themes/spec.md` : `bd2008d3546647c84d913397230724ca1c48d3aac6ad3b4c509550ddbca6fb64`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
