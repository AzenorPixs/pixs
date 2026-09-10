## 1. Contrats Core et configuration

- [ ] 1.1 Définir le contrat de consultation Core et le schéma de manifest d'un `DirectoryProjectionProvider`, puis vérifier le rejet d'un provider sans mapping, périmètre ou limite de fraîcheur.
- [ ] 1.2 Implémenter la sélection déterministe de la source de lecture, puis vérifier que les consommateurs utilisent exclusivement la façade `pixs.core` et non LDAP directement.

## 2. Projection sortante LDAP

- [ ] 2.1 Implémenter le mapping versionné des identités numériques, groupes et appartenances, puis vérifier la conservation des identifiants Pixs et la restriction aux attributs autorisés.
- [ ] 2.2 Produire la projection depuis l'outbox avec checkpoints, retries, tombstones et rejeu idempotent, puis vérifier la reprise après une interruption sans doublon ni résurrection.
- [ ] 2.3 Détecter les divergences LDAP sans import de mutation, puis vérifier qu'une écriture LDAP ne modifie aucune primitive Core.

## 3. Lecture cohérente et dégradée

- [ ] 3.1 Préférer LDAP uniquement lorsqu'il est disponible et dans sa limite de fraîcheur, puis vérifier qu'une lecture post-mutation utilise PostgreSQL jusqu'à convergence.
- [ ] 3.2 Ajouter le repli PostgreSQL, les états `HEALTHY` et `DEGRADED`, les métriques et le diagnostic corrélé, puis vérifier la consultation lors d'une indisponibilité LDAP.
- [ ] 3.3 Appliquer autorisation, tenant et `ScopeContext` avant toute lecture, puis vérifier qu'aucune réponse LDAP ou PostgreSQL ne divulgue une identité ou un groupe hors périmètre.

## 4. Conformité et distribution

- [ ] 4.1 Écrire la suite de conformité du provider LDAP avec des fixtures synthétiques, puis vérifier mapping, fraîcheur, repli, suppression et isolation tenant/scope.
- [ ] 4.2 Ajouter les tests de frontières, puis vérifier que LDAP ne fournit ni ACL, ni permission, ni décision d'autorisation, ni révocation, ni authentification.
- [ ] 4.3 Intégrer les validations de manifest et de conformité au build, puis vérifier l'absence de credential, DN de production ou donnée personnelle réelle dans les artefacts et rapports.
