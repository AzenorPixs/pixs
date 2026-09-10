## 1. Contrat et état de provisionnement

- [ ] 1.1 Définir le contrat versionné de plan et d'opération de provisionnement, puis vérifier les états non provisionné, en cours, prêt et échoué.
- [ ] 1.2 Implémenter la persistance, le verrouillage et la clé d'idempotence de l'opération, puis vérifier qu'un rejeu concurrent ne duplique aucune étape.
- [ ] 1.3 Relier l'état prêt à la frontière de mise en service, puis vérifier qu'une installation non provisionnée refuse le trafic métier.

## 2. Configuration et identité de bootstrap

- [ ] 2.1 Définir et valider le schéma de configuration de bootstrap, puis vérifier qu'une référence obligatoire absente ou invalide bloque la mise en service.
- [ ] 2.2 Intégrer la résolution de secrets par références externes redacted, puis vérifier qu'aucun secret ne figure dans les artefacts, audits ou diagnostics.
- [ ] 2.3 Créer le rattachement explicite de l'opérateur initial et ses permissions minimales, puis vérifier l'absence de compte et privilège administrateur implicites.

## 3. Provisionnement des tenants

- [ ] 3.1 Implémenter la Command plateforme de création idempotente d'un tenant, puis vérifier sa frontière transactionnelle et la propriété canonique du tenant racine.
- [ ] 3.2 Créer les rattachements administratifs initiaux autorisés et le ScopeContext associé, puis vérifier le refus d'un tenant ou d'un accès hors périmètre.
- [ ] 3.3 Produire les événements et audits de provisionnement, puis vérifier qu'ils portent acteur, corrélation, résultat et aucune donnée sensible.

## 4. Reprise et conformité

- [ ] 4.1 Implémenter la reprise autorisée depuis chaque étape persistée, puis vérifier une interruption avant mise en service sans identité, tenant ni autorisation dupliqués.
- [ ] 4.2 Ajouter les diagnostics opérateur et les contrôles de santé du provisionnement, puis vérifier le redaction et les états d'échec fermés.
- [ ] 4.3 Ajouter les tests unitaires, intégration et conformité de la capacité, puis vérifier le bootstrap, le rejeu, le refus et la reprise sur données synthétiques.
