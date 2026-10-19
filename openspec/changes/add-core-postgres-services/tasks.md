# Tâches — C02

Ces tâches décrivent la réalisation future. Le complément documentaire du 19 octobre 2026 relie les exigences, le modèle logique, les interfaces et les vérifications V01 à V12 de `design.md`. Les options A de D01 à D04 sont adoptées ; cette validation documentaire ne lance aucune implémentation ni production de code et les dix tâches restent non cochées. La revue préalable sera reconfirmée sur les sources courantes au début d’un mandat distinct, sans assimiler la préparation ou son strict à une preuve produit ni redemander les mêmes décisions.

## 1. Revue de conception

- [ ] 1.1 Reconfirmer les exigences/scénarios et empreintes de requirements.md, l’adoption C00 et les régressions à préserver ; vérifier l’allocation de chaque ligne aux tâches, à V01–V12 et aux lots propriétaires.
- [ ] 1.2 Décliner les options A adoptées de D01–D04 : schéma propriétaire, contrats/versionnement, concurrence et interfaces transactionnelles, accords tenant et politiques de données ; présenter les fichiers de réalisation, critères et tout delta nécessaire dans un mandat distinct. Documenter les conditions d’activation distinctes des dépendances de réalisation, sans rouvrir les orientations acquises ; toute déviation structurante reste à faire valider.

R01 complète cette revue par le contrat d’autorité C08/C02 : preuve d’opérateur pré-session, mapping conforme au canon, plan fermé, confirmations, audit et reprise. Les références de réalisation restent dans 1.2/2.3/2.4 ; aucune tâche n’est ajoutée ou cochée par le complément.

## 2. Réalisation future

- [ ] 2.1 Réaliser les modèles/contrats arrêtés en D01/D02 : utilisateurs/identités distincts, liaisons, groupes et deux sortes d’appartenances, tenants/scopes, rôles/permissions/ACL et stockage des accords ; conserver les façades pures et la propriété des scopes métier. Relier les contraintes et déclarations de services à V01–V06/V11.
- [ ] 2.2 Implémenter persistance et migrations Core selon le contrat propriétaire : clés/références, concurrence, dimensions de cycle de vie et protections de suppression ; déclarer origine/cible, avancement et compensation/retour compatibles, sans downgrade automatique. Fournir V01–V03/V08–V11.
- [ ] 2.3 Implémenter les lectures et mutations propriétaires sous identité/contexte/corrélation de confiance ; fournir les raccordements C04/C05 et résultats transactionnels C06/C09 selon D03, ainsi que les gardes du contrat R01 C08/C02 sans exiger une session préalable du compte cible. Refuser preuve/plan/port manquant, autorité C01 métier, rejeu divergent ou issue inconnue ; ne pas écrire les tables privées voisines. Distinguer conformité locale V04/V05/V06/V07 et garanties runtime des consommateurs, sans dépendance inverse de livraison.
- [ ] 2.4 Exécuter la part C02 de V01–V11 : régression des structures, PostgreSQL réel, collisions concurrentes, topologie/isolation, stockage des accords, transaction et refus des raccordements incomplets, migration interrompue/exclusion et compatibilité/contraction. Relier V05/V07 aux cas R01 B01–B10 de C08. Attribuer à C03/C04/C05/C06/C08/C09/C10/C16 les recettes intégrées dépendant de leurs réalisations ; conserver leurs conditions d’activation en attente, distinctes des non-applicabilités motivées.

## 3. Preuves et clôture futures

- [ ] 3.1 Exécuter syntaxe, contrôles configurés et suites applicables au périmètre réellement modifié, y compris les façades structurelles préservées ; conserver commandes, résultats natifs et preuves V01/V06/V12.
- [ ] 3.2 Relier chaque scénario de requirements.md aux preuves V01–V12, contrôler isolation/refus/concurrence/absence de secret et les conditions d’activation ; distinguer succès, échec, non exécuté et non applicable motivé. Ne pas clore une garantie intégrée obligatoire sur un double mémoire.
- [ ] 3.3 Examiner diff et périmètre, préserver changements préexistants et documenter impacts/limites sans annoncer un P0 complet avant C17/C19.
- [ ] 3.4 N’engager Git, synchronisation, archivage, déploiement ou publication que dans un périmètre ensuite autorisé ; produire STATISTIQUES.md si un archivage est demandé et réussi.
