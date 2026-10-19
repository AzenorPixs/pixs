# Tâches futures — protection et récupération des secrets d’amorçage

Toutes les tâches restent non cochées. La présente demande autorise uniquement la préparation documentaire ; les essais hôte et la production de code ne sont pas lancés.

## 1. Conception de réalisation

- [ ] 1.1 Relire C01 et les deltas ; fixer plateformes, versions, TPM, politique de démarrage/mise à jour, chemins et permissions sans reprendre les paramètres de fixtures.
- [ ] 1.2 Définir l’autorité de reprovisionnement, la protection indépendante du secours, RPO/RTO et impacts par secret ; faire autoriser le périmètre de réalisation et les futurs essais matériels.

## 2. Réalisation sous mandat distinct

- [ ] 2.1 Intégrer le provisionnement et la vérification du mode combiné host+tpm2 en conservant les gardes et le cycle de vie C01.
- [ ] 2.2 Intégrer le refus de profils matériels/modes non qualifiés et la transition contrôlée de politique lors des mises à jour.
- [ ] 2.3 Réaliser la procédure de remplacement d’hôte sans ancien TPM, avec réémission ou récupération protégée, nouvelles liaisons et réadmission conforme C16/N05.

## 3. Qualification future

- [ ] 3.1 Exécuter les essais cryptographiques réels positifs et négatifs sur les plateformes autorisées, sans utiliser le mode null comme preuve de production.
- [ ] 3.2 Tester la récupération avec ancien hôte indisponible, interruption, révocation postérieure au snapshot et changement de politique ; mesurer RPO/RTO et les effets de rotation par secret.
- [ ] 3.3 Exécuter syntaxe, régressions, validations OpenSpec et contrôles de non-exposition applicables ; distinguer preuves fonctionnelles, cryptographiques et produit.

## 4. Intégration et clôture futures

- [ ] 4.1 Relier les preuves versionnées au runtime C08, à la reprise C16/N05 et à l’artefact C18/C17/C19 sans annoncer de production avant satisfaction des conditions.
- [ ] 4.2 Examiner le périmètre et les limites ; ne synchroniser, archiver ou publier que sous autorisation ultérieure, avec statistiques si archivage réussi.
