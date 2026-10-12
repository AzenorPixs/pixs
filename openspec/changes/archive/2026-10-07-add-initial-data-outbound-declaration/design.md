# Conception — Représentation déclarative interne d'une déclaration de flux sortant

## Contexte

Source canonique : data-governance/spec.md, exigence « Profil de gouvernance
versionné par composant », scénario « Flux sortant sans consommateur refusé »
(texte : destination « sans consommateur ni garantie documentée »). Patron de
validateur : data_governance_profile.py (garde de
type exact d'abord, `_refusal` fixes, `_pack` trié/dédupliqué). Le processeur et le but ne sont pas modélisés dans cette représentation partielle ; aucun conflit avec TECHNICAL.md n’est établi.

## Forme livrée

@dataclass(frozen=True) : destination_reference: str ;
consumer_reference: str | None ; guarantee_reference: str | None. Aucun défaut,
sans __post_init__ ni méthode ; constructeur structurellement permissif ;
validateur seul point fermé retournant list[Diagnostic] (VALIDATE), messages
fixes sans écho.
__all__ = ["DataOutboundDeclaration", "validate_data_outbound_declaration"].

## Règles de validation

- type exact différent : refus unique
  data_outbound_declaration.declaration « déclaration de transfert exacte
  attendue », avant tout getattr et sans invocation d'objet hostile ;
- destination_reference : str exact non vide, opaque, sans trim ni grammaire ;
  None, sous-classes de str, bool et int refusés
  (data_outbound_declaration.destination_reference « référence opaque exacte
  non vide attendue ») ;
- consumer_reference et guarantee_reference : None exact (champ non fourni) ou
  str exact non vide ; refus sinon
  (data_outbound_declaration.<champ> « None exact ou référence opaque str
  exacte non vide attendue ») ;
- refus de scénario, uniquement si consumer_reference is None ET
  guarantee_reference is None : element
  data_outbound_declaration.outbound_flow, message fixe « transfert sans
  consommateur ni garantie documentée refusé ». Une valeur non None invalide
  (vide, sous-classe, bool, int) appelle le refus de champ, jamais le refus de
  scénario ; une des deux présentes (None de l'autre) n'est jamais refusée par
  cette unité.

## Décisions

- Absence conjointe = seul état refusé par le scénario ; lecture « sans A ni B »
  conservée telle quelle ; aucune norme de présence séparée inventée ;
- référence de destination exigée : un transfert qui « déclare une destination »
  sans destination n'est pas un flux déclarable ; décision de structure,
  consignée, sans portée normative nouvelle ;
- pas de ConfidentialityLevel, pas de lien DataGovernanceProfile, pas d'import
  pixs.core, pas de dépendance nouvelle ; Diagnostic/VALIDATE réutilisés ;
- représentation interne et partielle ; fichiers et façades archivés inchangés
  octet à octet.

## Critères observables

Validité : destination + consommateur seul → [] ; destination + garantie seule
→ [] ; destination + les deux → []. Scénario : destination + None + None →
exactement un diagnostic outbound_flow. Refus de champs : par champ fautif,
préfixe data_outbound_declaration. ; type exact d'abord ; hostiles jamais
invoqués ; diagnostics triés, dédupliqués, stables, sans écho de valeur ;
export exact à deux noms ; dataclass frozen. Import et appels sans effet
observable sur les surfaces gardées (non preuve universelle).

## Validation prévue

- openspec validate strict du change et de la spec data-governance : exit 0,
  avant code puis après ;
- globaux --specs et --all --strict --json --report findings : exit 1 natif
  admis uniquement sous qualification intégrale (couverture 76/77 items,
  identité exacte des 19 WARNING de la baseline, 0 ERROR, 127 empreintes de
  cadrages/canon inchangées) ; toute divergence suspend le mandat (reprise
  CISMP) ;
- py_compile des trois nouveaux fichiers ; tests unitaire et intégration
  (processus frais -I -B, environnement réduit, marqueur
  DATA_OUTBOUND_DECLARATION_SAFE_INTEGRATION_OK, quatre assertions hors with) ;
- régression bornée : tests/unit/test_data_governance_profile.py ;
  tests/integration/test_kernel_purity.py et
  tests/integration/test_public_api_facades.py ;
- UTF-8/LF des nouveaux fichiers, empreintes hors périmètre.

## Non-goal

Aucune activation, exécution, refus runtime, audit, autorisation de
destination, vérification de contenu de garantie, résidence, région, provider,
lien au profil, sémantique de None au-delà de « champ non fourni ».
