# N01 — Procédure d’urgence de sécurité PBO

## Pourquoi

L’audit des 94 exigences initialement non évaluées constate que le PDP sait refuser un fait de révocation, mais qu’aucune procédure PBO persistante de traitement d’une compromission n’est démontrée. C15 décrit principalement maintenance, santé et observabilité ; PA07 et O29 ne remplacent pas cette responsabilité PBO.

Le développeur a validé le 17 octobre 2026 la préparation d’un change dédié après examen de la proposition N01. Cette validation autorise les documents, sans implémentation.

## Modifications proposées

- Préparer la procédure d’urgence distincte du cycle normal demandée par `resilience`.
- Désigner explicitement l’autorité de blocage/révocation, le périmètre, la version/génération et le résultat persistant.
- Relier les propriétaires de sessions/justificatifs, composants/providers et points d’accès aux admissions web, travaux et activations.
- Distinguer demande, décision, effet observé, état incertain et réactivation autorisée, sans rollback fictif.

## Capacités

### Capacités nouvelles

Aucune : réalisation de `resilience`, `security`, `authorization`, `operations`, `runtime` et `testing` dans leurs clauses applicables.

### Capacités modifiées

Aucune évolution normative imposée par cette préparation. `skip_specs: true` évite un delta identique ; les futures commandes, schémas ou garanties observables qui nécessitent une précision devront être proposés avant réalisation.

## Dépendances et consommateurs

C03, C04, C05, C07, C09 et C15 fournissent identité, autorisation, audit, runtime, travaux et gestion. C18 doit inclure le résultat dans l’artefact ; C17 le qualifie avant C19.

## Impact et limites

Préparation documentaire uniquement. Aucune détection automatique d’intrusion, lecture de secret, modification de droits système, action de quarantaine réelle ou réinitialisation. Les contrôles applicatifs suivent l’exception Super Admin du canon dans son seul périmètre, sans preuve fabriquée ni délégation de credentials.
