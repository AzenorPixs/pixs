## Context

Les spécifications actives sont en français et utilisent des mots-clés
normatifs français historiques, ce qui laisse des avertissements systématiques au validateur OpenSpec.
Le projet souhaite désormais adopter la RFC 2119 sans renoncer au français.

## Goals / Non-Goals

**Goals:**

- Employer les mots-clés RFC 2119 exacts dans toutes les exigences actives.
- Préserver mot pour mot les comportements, scénarios et limites existants, hors
  remplacement des mots-clés normatifs.
- Donner aux futurs changements une règle de rédaction vérifiable.

**Non-Goals:**

- Ne pas modifier les exigences fonctionnelles, les scénarios, le code ou les
  contrats publics.
- Ne pas réécrire les changements OpenSpec archivés, qui constituent un
  historique fidèle de la convention alors en vigueur.

## Decisions

1. **Prose française et mots-clés anglais RFC 2119.** Les mots-clés exacts
   `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT` et `MAY` sont reconnus par les
   outils et par les lecteurs internationaux ; la phrase qui les porte reste en
   français. Les interdictions utilisent nécessairement les paires exactes
   `MUST NOT` ou `SHOULD NOT`, jamais une négation française placée avant un
   mot-clé anglais. Traduire ou hybrider les mots-clés est rejeté car le
   validateur ne les reconnaît pas comme RFC 2119.

2. **Migration uniquement des marqueurs normatifs en majuscules.** Les
   formulations françaises ou en minuscules des documents de cadrage restent
   explicatives, tandis que les exigences comportementales sont centralisées
   dans OpenSpec. Une réécriture globale de toute la prose est rejetée car elle
   augmenterait le risque de dérive sans améliorer la vérifiabilité.

3. **Deltas complets pour chaque capacité active.** Chaque delta reprend ses
   blocs d'exigences complets avec les seuls mots-clés modifiés, pour garantir
   qu'un futur archivage ne réintroduise pas l'ancienne convention.

## Risks / Trade-offs

- [Mélange temporaire avec les archives] → les archives sont explicitement
  historiques ; les référentiels actifs, changements ouverts et règles futures
  appliquent la nouvelle convention.
- [Remplacement mécanique incomplet] → contrôles de comptage, validation du
  change et validation de toutes les spécifications actives.

## Migration Plan

1. Générer les deltas complets depuis les spécifications actives.
2. Remplacer les mots-clés normatifs dans le référentiel actif et les changements
   non archivés.
3. Valider les changements puis le référentiel de spécifications.

Le retour arrière consiste à rétablir les fichiers de ce changement et les
spécifications actives depuis le contrôle de version ; aucune donnée ou
compatibilité runtime n'est concernée.
