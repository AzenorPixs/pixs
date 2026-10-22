# C04 — Autorisation Django et Super Admin

## Pourquoi

À l'ouverture du change, authorize et source-filter-plan-v1 fournissaient les
profils préparatoires, sans démontrer le PEP Django ni l'exception runtime
du compte fonctionnel. Le RUN CISMP3 réalise ce seul change.

## Réalisation

C04 fournit les adapters Django de faits, policies, décision, filtrage source
et déclaration. Les faits Auth restent produits et revérifiés par C03 ; Core
recoupe ses métadonnées et conserve ses données propriétaires. Les profils
PDP purs restent réutilisés. Les comptes ordinaires gardent DENY, ALLOW puis
refus par défaut, obligations et fraîcheur. Le seul Super Admin actif
reconnu par le Binding de l'installation dispose du contrôle canonique dans
PLATFORM et dans les tenants explicitement accordés.

R01 reste disjoint de l'identité applicative cible : preuve C03, plan/hash/
cibles/effets C08, fenêtre finale de 600 s et consommation au commit.
Une inspection après réponse perdue ne devient jamais un nouvel apply.
Les contrôles finaux Auth et de fraîcheur utilisent les décisions et reçus
natifs réellement émis, sans réactiver un justificatif retiré.

## Capacités

Aucune nouvelle capacité normative. Le delta authorization du 20 octobre 2026
porte les exigences R01 et le raccord de retrait d'accès Auth déjà adoptés
au canon. Sa source est conservée ; skip_specs reste désactivé.
Le recoupement exécuté du 21 octobre confirme huit exigences déjà identiques.
Les précisions internes, signatures et limites sont dans design.md ;
les résultats effectivement exécutés sont dans VALIDATION.md.

## Dépendances et impacts

- C02 Core PostgreSQL est livré et ses six familles PG sont recontrôlées.
- C05 audit durable est livré à la référence CAB51 ; le PEP et le sink sont
  exercés réellement avec C04.
- Les API Auth C03 sont consommées par contrat explicite ; leur qualification
  commune et leurs sources de confiance/assurance sont distinguées de la
  livraison des sessions et services Auth.
- C08/C10/Idempotence/Outbox encore synthétiques dans certaines recettes
  ne sont pas présentés comme propriétaires livrés.

C04 ne crée aucun endpoint, panneau, worker, migration, dépendance nouvelle
ou opération Git. C06/C07/C09/C13 et C17/C18/C19 conservent leurs garanties
d'interface, de composition, d'effets et de distribution à qualifier.
La présence du code ne déclare pas un P0 global disponible.

## Critères et clôture

Les critères sont suivis dans tasks.md et reliés aux preuves de VALIDATION.md :
autorité backend, propriété et contexte, DENY ordinaire, accords tenant,
dérogations, obligations, filtrage SQL et limites temporelles.
Archive, publication, STATISTIQUES.md à six sections et gate individuel
restent des preuves distinctes de la réalisation ; aucun change suivant
n'est lancé dans ce RUN borné à un seul change.
