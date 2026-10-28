# Revalidation — lot administration, maintenance et audit

## Validation globale stricte du 26 octobre 2026

À la demande explicite du développeur, la commande suivante est exécutée dans
`/home/devops/datas/pixs`, sans correction de spécification ni nouvel archivage :

```text
/home/devops/.local/npm/bin/openspec validate --all --strict --json --no-interactive
```

Exécution du 2026-10-26T19:43:21.110328+00:00 au 2026-10-26T19:43:21.865184+00:00, retour **0**.
Durée instrumentée du contrôle et de ses relevés : 0.757762 s.

| Périmètre global | Examinés | Valides | En échec | Part des 186 |
|---|---:|---:|---:|---:|
| Changes actifs | 108 | 108 | 0 | 58,1 % |
| Spécifications canoniques | 78 | 78 | 0 | 41,9 % |
| Total | **186** | **186** | **0** | **100 %** |

Le strict global **réussit : 0 erreur, 0 avertissement, 88 informations**.
Parmi ces informations, 87 signalent un `skip_specs` déjà déclaré dans la
configuration du change concerné. La dernière appartient à
`define-common-pbo-binary-and-resource-profiles`, pour
`reference-composition/spec.md` : la simulation d'un ancien ajout indique
que l'exigence « Qualification du binaire commun et des profils de ressources
P0 » existe déjà. Cette information n'invalide pas le strict ; aucune
configuration, proposition ou exigence n'est corrigée par cette intervention.

La commande globale porte sur les changes **actifs** et le canon. Elle ne
réexécute pas le contrôle des archives, dont les propositions complètes et
les deltas ont été validés lors du découpage précédent. Les deux niveaux de
preuve restent distincts. Aucune qualification runtime n'est déduite du
succès structurel global. Le bilan des douze tâches historiques reste
**10 CONFORME / 0 ÉCART / 1 NON VÉRIFIABLE / 1 NON APPLICABLE partielle** :
la preuve de présentation initiale et le remplacement historique de la
restriction Super Admin ne sont pas modifiés par cette commande.

Les **78 empreintes SHA-256 canoniques sont identiques avant et après**.
Aucun change n'est créé, corrigé, synchronisé ou réarchivé. Les écritures se limitent à ces rapports, aux deux statistiques et aux
preuves non versionnées.
Résultat JSON complet : [validation globale](../../../../output/openspec-global-strict/20261026T194321Z/validation.json).
Commande, horodatages, quota et empreintes : [journal](../../../../output/openspec-global-strict/20261026T194321Z/state.json).

## Relevés précédents conservés

Archive : `2026-10-26-specify-initial-administration-and-maintenance`.
Création et archivage documentaire explicitement autorisés par la demande de
découpage du 26 octobre 2026. Ce lot extrait les deltas historiques de
[la première archive](../2026-09-16-specify-initial-application-bootstrap/proposal.md), sans mise à jour du canon.

## Périmètre et conservation

| Delta transféré | Exigences | Scénarios |
|---|---:|---:|
| initial-administration | 7 | 13 |
| operations | 1 | 1 |
| audit | 1 | 1 |
| Total propre au lot | **9** | **15** |

Les trois fichiers sont identiques octet pour octet aux sources d'avant
découpage. Le lot bootstrap conserve les 4 autres exigences et 6 scénarios :
union disjointe de 13 exigences et 21 scénarios. Aucune règle normative n'est
supprimée, fusionnée ou dupliquée ; les scénarios corrigés précédemment sont préservés.

## Validation stricte complète

La CLI stricte valide ce lot actif avant archivage (retour 0, `valid=true`,
0 erreur, 0 avertissement, 3 INFO d'ajouts déjà présents dans le canon).
Après archivage, l'API native `new Validator(true)` valide séparément la
proposition complète et les deltas : **deux rapports `valid=true`, sans diagnostic**.
Le reçu natif d'archivage du 2026-10-26T19:30:29.043492+00:00
porte `specsUpdated=false`. Le lot est archivé et absent des changes actifs.

## Traçabilité et limites

Les cinq tâches documentaires propres à ce découpage sont réalisées sur preuves.
Le bilan des douze tâches historiques communes est détaillé dans
[le rapport de référence](../../../../output/rcamp/rcamp2-pixs-d2dfdf5ddd024b9b/REVALIDATION.md) : **10 CONFORME, 0 ÉCART,
1 NON VÉRIFIABLE, 1 NON APPLICABLE partielle**. Ces tâches communes ne sont
pas additionnées entre les deux archives. L'absence de reçu de présentation
initiale et la portée remplacée du bypass limité au panneau restent distinctes.
Aucune qualification d'installation, d'audit runtime ou de comportement
Super Admin n'est déduite de ces contrôles documentaires. Le canon et Git
ne sont pas modifiés par cette intervention.

Commandes complètes, entrées du validateur, retours, empreintes et reçus :
[preuves du découpage](../../../../output/revalidation-split/20261026T192534Z/state.json).
Statistiques : [STATISTIQUES.md](STATISTIQUES.md).
