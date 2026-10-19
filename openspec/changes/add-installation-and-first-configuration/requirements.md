# Exigences de réalisation — C08

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 adopté le 18 octobre 2026 et intégré au canon apporte les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
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
| initial-application-bootstrap / 11 | [Composition Django initiale déclarée](../../specs/initial-application-bootstrap/spec.md#L11) | P | Composition initiale valide |
| initial-application-bootstrap / 27 | [Configuration sensible de la composition Django initiale](../../specs/initial-application-bootstrap/spec.md#L27) | P | Connexion fournie par configuration runtime |
| initial-application-bootstrap / 39 | [Surface HTTP initiale minimale](../../specs/initial-application-bootstrap/spec.md#L39) | P | Route initiale non déclarée |
| initial-application-bootstrap / 54 | [Shell TanStack initial intégré](../../specs/initial-application-bootstrap/spec.md#L54) | P | Démarrage du shell initial |
| installation-provisioning / 9 | [Provisionnement du compte fonctionnel de secours](../../specs/installation-provisioning/spec.md#L9) | ND | Provisionnement sans compte nominatif ni MFA |
| installation-provisioning / 18 | [Provisionnement explicite et états inspectables](../../specs/installation-provisioning/spec.md#L18) | ND | Installation non provisionnée |
| installation-provisioning / 30 | [Configuration et secrets vérifiés avant mise en service](../../specs/installation-provisioning/spec.md#L30) | ND | Référence de secret indisponible |
| installation-provisioning / 42 | [Opérateur initial explicite et sans privilège implicite](../../specs/installation-provisioning/spec.md#L42) | ND | Identité opérateur absente |
| installation-provisioning / 55 | [Création tenant-scoped contrôlée](../../specs/installation-provisioning/spec.md#L55) | ND | Rejou du provisionnement du premier tenant |
| installation-provisioning / 68 | [Reprise contrôlée et auditée](../../specs/installation-provisioning/spec.md#L68) | ND | Interruption avant mise en service |
| reference-composition / 10 | [Capacités obligatoires du P0](../../specs/reference-composition/spec.md#L10) | P | Capacité P0 absente |
| reference-composition / 22 | [Capacités hors P0 explicites](../../specs/reference-composition/spec.md#L22) | P | Synchronisation non sélectionnée |
| reference-composition / 33 | [Preuve reproductible](../../specs/reference-composition/spec.md#L33) | P | Deux validations identiques |

## Empreintes SHA-256 du canon

- `openspec/specs/initial-administration/spec.md` : `200ce5a01e6d741d9021b2c78dd7f31efd7eeed566309168c0f3fbf468b5c4e5`.
- `openspec/specs/initial-application-bootstrap/spec.md` : `688063fbafcd34535d87b7f4920d8e4952ff2ed3267bd5b442400a3d9f0fe3a4`.
- `openspec/specs/installation-provisioning/spec.md` : `2d33df47ef9ad0c073c4e0d7677c98e3cd96cb8e3b6866894c6d3cb7d305e7b4`.
- `openspec/specs/reference-composition/spec.md` : `7c4d7b603f35f02f6d2ba0eb10dd202793ec288fee0c65a5ff15d244446233ff`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
