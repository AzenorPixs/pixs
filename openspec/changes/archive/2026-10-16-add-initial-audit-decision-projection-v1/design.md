## Context

Le RSMP livré a ajouté onze exigences dans authorization-engine et deux dans audit, sans modifier d'ancien texte. Le Kernel possède AuditEvent à treize champs et son validateur public ; le PDP possède un événement distinct à dix champs, dont certaines données peuvent être None. La projection exige leur sous-ensemble complet sans modifier ces contrats.

## Goals / Non-Goals

Le lot implémente exactement les treize exigences canoniques et leurs vingt scénarios. Il reste purement mémoire et limité à un nouveau module Core/authz, avec deux fichiers de tests. Il ne produit, persiste, acquitte ni exporte aucun audit et ne prouve ni exhaustivité, privilège ni conformité P0. Aucun Kernel ne dépend du PDP.

## Decisions

1. AuditDecisionProjectionV1 est une dataclass frozen à slots, avec exactement decision_event et audit_event explicites. Les objets sont conservés par identité, sans copie, normalisation ou valeur par défaut. Le validateur accepte object et retourne des Diagnostic VALIDATE.
2. Les types exacts sont vérifiés avant les attributs étrangers. Les cinq identifiants PDP sont des str exactes non vides. ScopeContext est exact et contrôlé par validate_structure sur le même objet ; ScopeStructureError attendu devient un diagnostic statique. Les exceptions inattendues se propagent.
3. Effect et reason_code restent ALLOW/ALLOWED ou DENY/DENIED. policy_version est un tuple exact non None conservé dans la décision originale, dont le contenu n'est pas réinterprété ni traversé. evaluated_at est un datetime exact avec tzinfo is timezone.utc.
4. validate_audit_event est réutilisé sur l'événement générique original, sans duplication des grammaires date/SemVer. occurred_at fourni est comparé au même instant UTC, sans génération ni lecture d'horloge.
5. Les correspondances acteur, ressource, action, résultat, motif et tenant sont exactes. Les tuples originaux contiennent la corrélation et la causalité requises tout en préservant ordre, doublons et autres références. Les métadonnées sont explicites et indépendantes ; aucun complément n'est fabriqué.
6. Les diagnostics sont frais, statiques, triés et dédupliqués sans valeur brute, str ou repr d'objet étranger. Une projection valide retourne une liste vide. Aucun IO, callback, horloge ou mutation d'objet.
7. Le module conserve les conventions existantes et expose localement son profil et son validateur, sans modifier les façades existantes. La bibliothèque standard suffit, sans nouvelle dépendance.

## Risks / Trade-offs

- Une projection valide pourrait être prise à tort pour un audit réalisé : les docstrings et tests rappellent les limites normatives.
- Les événements PDP incomplets sont refusés explicitement, sans placeholder ni modification de leurs producteurs.
- Version de politique et version de composant restent distinctes ; aucune inférence ni sérialisation du tuple politique.
- Types hostiles et sous-classes sont refusés avant callbacks ; les tests vérifient aussi les exceptions inattendues.
- Les quatre avertissements globaux de longueur historiques sont qualifiés avec leur exit natif ; aucune correction hors périmètre.

## Migration Plan

Aucune migration ni modification de production existante. Création des trois nouveaux fichiers, syntaxe sur chacun, tests dédiés et régressions audit/authz, stricts ciblés, contrôle de cohérence. Les tâches sont cochées seulement après preuve. Sous exclusion cohorte READY : validations globales, archivage unique --skip-specs seulement après preuve des deltas verbatim, puis rapport STATISTIQUES.md à six sections sous mandat distinct.

## Open Questions

Aucune décision normative nouvelle ; les ambiguïtés du RSMP sont déjà résolues. Toute découverte hors de ces exigences suspend son seul périmètre avant extension.
