## Context

Pixs dispose de contrats distincts pour la configuration, les identités, les
scopes, l'autorisation, l'audit et le lifecycle, mais aucun ne coordonne leur
initialisation. Voir `proposal.md` pour la motivation et la spécification de
capacité pour les garanties observables.

## Goals / Non-Goals

**Goals:**

- Introduire une opération de management persistante qui coordonne le
  bootstrap sans contourner les contrats existants.
- Séparer l'état du provisionnement de l'état de lifecycle des composants et
  de la disponibilité du trafic métier.
- Réutiliser les identités numériques, l'autorisation, l'audit et les secrets
  externes déjà prévus par Pixs.

**Non-Goals:**

- Ne pas choisir de provider d'identité, de secrets ou de déploiement.
- Ne pas créer de mot de passe, jeton, identifiant administrateur ou tenant
  par défaut.
- Ne pas fournir une interface graphique, une API publique ou un provisionneur
  d'infrastructure.
- Ne pas définir le cycle de vie métier complet d'un tenant après sa création.

## Decisions

1. **Un plan de provisionnement persistant pilote les étapes.** Il contient
   une identité d'opération, sa version, l'acteur, la corrélation, les étapes
   validées et leur résultat. Une exécution rejouée reprend ce plan plutôt que
   de recalculer l'état depuis des ressources partielles. Une suite de scripts
   sans état est écartée car elle ne démontre ni idempotence ni reprise.

2. **La mise en service est une frontière distincte.** L'installation reste
   hors trafic métier tant que la configuration obligatoire, l'identité
   opérateur et les contrôles nécessaires ne sont pas confirmés. Cet état ne
   remplace ni `ready` des composants ni `MAINTENANCE` : il les précède. Un
   démarrage permissif est écarté car il créerait une période sans autorité
   vérifiable.

3. **L'opérateur initial est une identité préexistante ou explicitement
   établie.** Le provisionnement reçoit une référence d'identité vérifiée par
   un mécanisme d'authentification déjà déclaré, puis lui attribue seulement
   les permissions de bootstrap documentées. Un secret ou compte local généré
   est écarté afin d'éviter tout accès privilégié implicite.

4. **Le tenant est créé par une Command plateforme dédiée.** La Command
   produit le tenant racine, son ScopeContext et les rattachements initiaux
   dans une même frontière transactionnelle ; l'audit et les événements suivent
   la validation. La création par fichier de configuration ou par provider est
   écartée, car elle ne garantit ni autorisation ni propriété canonique.

5. **Les échecs conservent l'état et ne compensent pas destructivement.** Une
   étape interrompue est diagnostiquée puis reprise par une opération autorisée
   avec la même clé d'idempotence. La suppression automatique d'une identité
   ou d'un tenant partiellement créé est écartée ; elle serait une opération
   destructive distincte.

## Risks / Trade-offs

- [Provisionnement bloqué par un secret externe indisponible] → état hors
  service explicite, diagnostic redacted et reprise autorisée.
- [Opérateur initial trop privilégié] → permissions de bootstrap minimales,
  audit et retrait explicite après transfert des responsabilités.
- [Rejou concurrent] → verrouillage persistant et clé d'idempotence portés par
  l'opération de provisionnement.
- [Création tenant partielle] → transaction de la Command, état persistant et
  réparation ou reprise explicitement autorisée.

## Migration Plan

La capacité est préparatoire et ne migre aucune installation existante. Lors
de son implémentation, une installation historique devra être inspectée puis
adoptée par un plan explicite et audité ; elle ne sera jamais considérée comme
provisionnée à partir d'un simple état de configuration.
