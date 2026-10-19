# Exigences de réalisation — C01

Cette table conserve le relevé canonique de préparation et ses statuts historiques P, sans affaiblir les MUST existants. La réalisation C01 relève ensuite du RUN parent CISMP3/ISMP ; les preuves et les limites sont détaillées ci-dessous.

| Capacité / ligne | Exigence | Statut | Scénarios sources |
|---|---|---|---|
| configuration / 8 | Schémas typés validés avant activation — `openspec/specs/configuration/spec.md:8` | P | Configuration invalide bloquée |
| configuration / 17 | Priorité déterministe des sources — `openspec/specs/configuration/spec.md:17` | P | Surcharge déterministe |
| configuration / 28 | Secrets par référence hors artefacts — `openspec/specs/configuration/spec.md:28` | P | Secret embarqué refusé |
| secrets-providers / 11 | Références externes sans valeur persistée — `openspec/specs/secrets-providers/spec.md:11` | P | Diagnostic de référence indisponible |
| secrets-providers / 22 | Accès runtime associé à une identité de workload — `openspec/specs/secrets-providers/spec.md:22` | P | Worker non autorisé |
| secrets-providers / 33 | Rotation, durée de vie et révocation contrôlées — `openspec/specs/secrets-providers/spec.md:33` | P | Secret tourné |
| secrets-providers / 47 | Audit minimisé et échec fermé — `openspec/specs/secrets-providers/spec.md:47` | P | Provider indisponible |

Deltas C01 : `specs/audit/spec.md`, `specs/secrets-providers/spec.md`, `specs/reference-composition/spec.md`, `specs/initial-administration/spec.md`, `specs/authorization/spec.md` — journal d’amorçage, provider systemd, sélection profil, INSTALLER borné. N’affaiblissent aucune garantie ; bornes chiffrées à déclarer, non inventées.

## Empreintes SHA-256 du canon après synchronisation

- `openspec/specs/configuration/spec.md` : `8e710a2390f044b0d5f78ddf68546e3310eddbb878eea29171ea5608dd425904`.
- `openspec/specs/secrets-providers/spec.md` : `fa537fca310131c63fae0130d0b30699964c6fa08d709afacc6c5ed153b00b3b`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales demeurent applicables aux fonctions livrées. Aucun statut ne vaut verdict produit. Preuves RSMP documentaires distinctes des preuves unitaires et du transport réel.

## Traçabilité de réalisation C01

| Périmètre | Réalisation | Preuve actuelle / limite |
|---|---|---|
| Références et réglages Django | `bootstrap_policy.py`, `provider.py`, `runtime_resolve.py` | Gabarits purs inchangés ; tests de remises fraîches, refus et LazySettings sans base. |
| Identité et transport systemd | `native.py`, provider lecture seule/ACL | Formats D-Bus, identité et transport natifs recoupés ; qualification fonctionnelle avec fixtures publiques. |
| TTL, rotation et révocation | `lifecycle.py`, gardes et reçus du journal | Tests isolés et arrêt/redémarrage réel prouvés ; nouvelle invocation et révocation recoupées avec les reçus. |
| Audit B01-B06 | `bootstrap_audit.py` | Journal réel par FD, reçus comparés, refus sur corruption/saturation/incertitude ; aucune qualification matérielle contre coupure. |
| B07-B09 et limites | Politique fermée, mode INSTALLER explicitement transmis, PLATFORM | Aucune identité applicative, session ou permission métier ; root reste opérateur système. |

La régression unitaire globale observée compte 1 945 tests réussis. Les valeurs numériques et les références synthétiques du harnais ne font pas partie d’un contrat de configuration de production. La qualification fonctionnelle hôte et la synchronisation des cinq canons sont prouvées. Validations d’archivage, archive et rapport statistique restent des barrières distinctes du RUN. Les contrats B01-B09 normatifs demeurent dans les cinq deltas existants ; cette table ne crée aucune nouvelle exigence normative.

Preuve durable : [PREUVES-C01.json](PREUVES-C01.json). La commande de vérification indépendante est `c3-cmd-236584a2-effect` (permission native once, exit 0). Elle ne remplace pas une mesure matérielle contre coupure ni une qualification cryptographique de production.
