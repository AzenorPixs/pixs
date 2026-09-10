# ai-agents Specification

## Purpose

Les capacités d'intelligence artificielle et d'agents composent des fournisseurs
de modèles et d'outils sous contrats, avec gouvernance, budget et audit, sans
imposer un modèle ou un fournisseur concret.

## Requirements

### Requirement: Fournisseurs et capacités IA déclarés

Un fournisseur IA MUST déclarer ses capacités de modèle, modalités, régions,
limites, contrats et niveau de confiance. Une capacité IA MUST rester DISABLED
par défaut et ne peut être activée qu'après sélection explicite du fournisseur ;
un modèle concret MUST NOT devenir obligatoire pour le Kernel.

#### Scenario: Fournisseur absent

- **WHEN** une capacité IA optionnelle ne possède aucun fournisseur compatible
- **THEN** le composant concerné reste DISABLED ou DEGRADED de façon diagnostiquable

#### Scenario: Fournisseur présent sans activation

- **WHEN** un fournisseur IA compatible est installé mais non sélectionné explicitement
- **THEN** la capacité IA reste DISABLED

### Requirement: Données et récupération gouvernées

Toute donnée, mémoire ou récupération transmise à un modèle MUST respecter le
ScopeContext, la finalité, la classification, la résidence, la rétention et
l'autorisation applicables. Une donnée non autorisée ou non classifiée MUST NOT
être transmise à un fournisseur ou index IA externe ; toute sortie de donnée
MUST aussi respecter une politique de sortie déclarée avant transmission.

#### Scenario: Récupération hors périmètre

- **WHEN** un agent demande une source hors de son tenant ou scope autorisé
- **THEN** la source est exclue avant la construction du contexte de modèle

### Requirement: Outils explicitement autorisés et médiés

Un agent MUST invoquer uniquement des outils déclarés, versionnés et autorisés
pour son contexte. Une invocation qui modifie l'état MUST passer par la Command
publique du propriétaire ; une sortie de modèle MUST NOT être traitée comme une
autorisation ou une preuve métier.

#### Scenario: Agent proposant une mutation

- **WHEN** un agent propose une opération d'écriture
- **THEN** la Command cible réévalue identité, périmètre et autorisation avant exécution

### Requirement: Prompts, évaluations, budgets et audit

Les prompts, configurations, évaluations et budgets MUST être versionnés et
traçables. Les limites d'usage et de coût doivent être appliquées via les
quotas déclarés ; les traces MUST minimiser les contenus sensibles et MUST NOT
contenir de credential ou secret.

#### Scenario: Budget épuisé

- **WHEN** une demande IA dépasse le budget déclaré
- **THEN** elle est refusée ou différée avec un état et un audit explicites
