# Références normatives — O24

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| ai-agents / 11 | [Fournisseurs et capacités IA déclarés](../../specs/ai-agents/spec.md#L11) | NE | AUDIT_AVANT_CREATION |
| ai-agents / 28 | [Données et récupération gouvernées](../../specs/ai-agents/spec.md#L28) | NE | AUDIT_AVANT_CREATION |
| ai-agents / 41 | [Outils explicitement autorisés et médiés](../../specs/ai-agents/spec.md#L41) | NE | AUDIT_AVANT_CREATION |
| ai-agents / 53 | [Prompts, évaluations, budgets et audit](../../specs/ai-agents/spec.md#L53) | NE | AUDIT_AVANT_CREATION |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence ai-agents--17db8b7a83

Source : `openspec/specs/ai-agents/spec.md`, ligne 11. SHA-256 du bloc : `98a4f57bf95a6b2ac57a5e3a1d6eb6d3436217142d9a5200029473fe25d5e4c5`.

~~~~text
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
~~~~

### Référence ai-agents--c68f58b142

Source : `openspec/specs/ai-agents/spec.md`, ligne 28. SHA-256 du bloc : `2d90f3ca5663149160694b6fa35e6d4b6dad4c8e166db1d68e4cdf4bc2ca4f0e`.

~~~~text
### Requirement: Données et récupération gouvernées

Toute donnée, mémoire ou récupération transmise à un modèle MUST respecter le
ScopeContext, la finalité, la classification, la résidence, la rétention et
l'autorisation applicables. Une donnée non autorisée ou non classifiée MUST NOT
être transmise à un fournisseur ou index IA externe ; toute sortie de donnée
MUST aussi respecter une politique de sortie déclarée avant transmission.

#### Scenario: Récupération hors périmètre

- **WHEN** un agent demande une source hors de son tenant ou scope autorisé
- **THEN** la source est exclue avant la construction du contexte de modèle
~~~~

### Référence ai-agents--8331cac4d5

Source : `openspec/specs/ai-agents/spec.md`, ligne 41. SHA-256 du bloc : `ed58a13da1f83c88f29402aa1c947d19c7828a21331440abe6639971d48eb35b`.

~~~~text
### Requirement: Outils explicitement autorisés et médiés

Un agent MUST invoquer uniquement des outils déclarés, versionnés et autorisés
pour son contexte. Une invocation qui modifie l'état MUST passer par la Command
publique du propriétaire ; une sortie de modèle MUST NOT être traitée comme une
autorisation ou une preuve métier.

#### Scenario: Agent proposant une mutation

- **WHEN** un agent propose une opération d'écriture
- **THEN** la Command cible réévalue identité, périmètre et autorisation avant exécution
~~~~

### Référence ai-agents--8419294222

Source : `openspec/specs/ai-agents/spec.md`, ligne 53. SHA-256 du bloc : `4643253a86aed5dc0fac19f965795359b363d4fc2dddf3fb802884b399ea01c4`.

~~~~text
### Requirement: Prompts, évaluations, budgets et audit

Les prompts, configurations, évaluations et budgets MUST être versionnés et
traçables. Les limites d'usage et de coût doivent être appliquées via les
quotas déclarés ; les traces MUST minimiser les contenus sensibles et MUST NOT
contenir de credential ou secret.

#### Scenario: Budget épuisé

- **WHEN** une demande IA dépasse le budget déclaré
- **THEN** elle est refusée ou différée avec un état et un audit explicites
~~~~

