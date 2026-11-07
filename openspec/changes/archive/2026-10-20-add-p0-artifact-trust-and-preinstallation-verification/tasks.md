# Tâches — N03

La préparation du 17 octobre 2026 est historique. La réalisation suivante a été autorisée par 1CISMP2 dans le canon existant, sans nouvelle exigence ni synchronisation canonique. Les preuves natives et leurs limites figurent dans VALIDATION.md.

- [x] 1. Valider matériaux publics, canaux, autorités et mécanismes de signature/provenance/révocation sans choisir de secret réel. — Contrats v1, clés publiques SPKI et fenêtres ; signatures éphémères uniquement en tests.
- [x] 2. Définir les contrats et points de contrôle précoces, distincts de C19. — Trois modules Python ; check_install, check_startup, check_upgrade ; VerifiedArtifact immuable.
- [x] 3. Présenter fichiers, outils et précisions avant réalisation. — NFDOC relue, conception arbitrée et mandats CAB unitaires corrélés ; aucune nouvelle dépendance ou exigence canonique.
- [x] 4. Réaliser génération et vérification des preuves sur des octets construits sans publication implicite. — Port signataire fiable, OpenSSL réel ; archive de fixture et preuves liées aux trois empreintes.
- [x] 5. Relier les vérifications aux entrées installation/démarrage/upgrade et aux preuves de sécurité du build. — Gates testés ; reçus indépendants requis ; installation et qualification finales C17/C18/C19 hors lot.
- [x] 6. Traiter révocation hors ligne, rotation/chevauchement et indisponibilité de publication. — Bundle local signé, plancher de séquence, empreintes de clés sous alias, rotation réelle et vérification sans réseau Python.
- [x] 7. Qualifier signature/empreinte/canal/provenance/inventaire invalides sur fixtures autorisées. — 35 tests finaux réussis ; l’échec diagnostique initial est corrigé et la suite complète est relancée.
- [x] 8. Vérifier immuabilité, nouvelle identité corrélée et absence de secret dans les sorties. — Trois empreintes et identité canonique ; sources et sorties contrôlées ; clés éphémères nettoyées.
- [x] 9. Fournir les contrats et preuves liés aux octets consommés pour C18/C17 puis C19. — La fixture consomme les octets vérifiés et en confirme l’empreinte ; les consommateurs finaux gardent leurs recettes et leurs tâches propres.
- [x] 10. Borner publication, signature, synchronisation, archivage et Git à leur autorisation. — Aucun secret ou signataire réel, aucune publication externe, aucun Git ; archivage unique délégué par CISMP après preuves, rapport postarchive exigé avant clôture.

## Sous-lots normalisés

Annotation rétrospective du 30 octobre 2026. Plan ACL-2026-10-30-R1. Une tâche existante correspond à un sous-lot ; les groupes, numéros, libellés, cases et preuves ci-dessus restent les sources conservées. Les numéros SL identifient les unités et ne fixent pas leur ordre de réalisation.

Les états possibles sont À FAIRE, EN COURS, RÉALISÉ À VALIDER, VALIDÉ, BLOQUÉ, ABANDONNÉ et NON VÉRIFIABLE. La case source décrit seulement l’avancement documentaire. Sans preuve datée et rattachée au périmètre de l’unité, sa qualification actuelle reste NON VÉRIFIABLE ; les validations historiques restent attachées à leur date, leur version et leur portée. Le présent relevé ne rejoue aucun contrôle produit.

Sources du périmètre, des dépendances et des critères : [proposal.md](proposal.md), [design.md](design.md), [requirements.md](requirements.md). Les dépendances non individualisées restent à vérifier dans ces sources ; aucune dépendance n’est déduite de la numérotation.

### N03-SL01 — Valider matériaux publics, canaux, autorités et mécanismes de signature/provenance/révocation sans choisir de secret réel. — Contrats v1, clés publiques SPKI et fenêtres ; signatures éphémères uniquement en tests.

- Ancien repère et tâche rattachée : tâche 1 ; section « Tâches — N03 », ligne 5 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### N03-SL02 — Définir les contrats et points de contrôle précoces, distincts de C19. — Trois modules Python ; check_install, check_startup, check_upgrade ; VerifiedArtifact immuable.

- Ancien repère et tâche rattachée : tâche 2 ; section « Tâches — N03 », ligne 6 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### N03-SL03 — Présenter fichiers, outils et précisions avant réalisation. — NFDOC relue, conception arbitrée et mandats CAB unitaires corrélés ; aucune nouvelle dépendance ou exigence canonique.

- Ancien repère et tâche rattachée : tâche 3 ; section « Tâches — N03 », ligne 7 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### N03-SL04 — Réaliser génération et vérification des preuves sur des octets construits sans publication implicite. — Port signataire fiable, OpenSSL réel ; archive de fixture et preuves liées aux trois empreintes.

- Ancien repère et tâche rattachée : tâche 4 ; section « Tâches — N03 », ligne 8 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### N03-SL05 — Relier les vérifications aux entrées installation/démarrage/upgrade et aux preuves de sécurité du build. — Gates testés ; reçus indépendants requis ; installation et qualification finales C17/C18/C19 hors lot.

- Ancien repère et tâche rattachée : tâche 5 ; section « Tâches — N03 », ligne 9 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### N03-SL06 — Traiter révocation hors ligne, rotation/chevauchement et indisponibilité de publication. — Bundle local signé, plancher de séquence, empreintes de clés sous alias, rotation réelle et vérification sans réseau Python.

- Ancien repère et tâche rattachée : tâche 6 ; section « Tâches — N03 », ligne 10 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### N03-SL07 — Qualifier signature/empreinte/canal/provenance/inventaire invalides sur fixtures autorisées. — 35 tests finaux réussis ; l’échec diagnostique initial est corrigé et la suite complète est relancée.

- Ancien repère et tâche rattachée : tâche 7 ; section « Tâches — N03 », ligne 11 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### N03-SL08 — Vérifier immuabilité, nouvelle identité corrélée et absence de secret dans les sorties. — Trois empreintes et identité canonique ; sources et sorties contrôlées ; clés éphémères nettoyées.

- Ancien repère et tâche rattachée : tâche 8 ; section « Tâches — N03 », ligne 12 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### N03-SL09 — Fournir les contrats et preuves liés aux octets consommés pour C18/C17 puis C19. — La fixture consomme les octets vérifiés et en confirme l’empreinte ; les consommateurs finaux gardent leurs recettes et leurs tâches propres.

- Ancien repère et tâche rattachée : tâche 9 ; section « Tâches — N03 », ligne 13 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.

### N03-SL10 — Borner publication, signature, synchronisation, archivage et Git à leur autorisation. — Aucun secret ou signataire réel, aucune publication externe, aucun Git ; archivage unique délégué par CISMP après preuves, rapport postarchive exigé avant clôture.

- Ancien repère et tâche rattachée : tâche 10 ; section « Tâches — N03 », ligne 14 du texte conservé.
- Objectif et périmètre : libellé de la tâche ci-dessus, borné au change décrit dans [proposal.md](proposal.md) et à ses contrats de conception.
- Case source observée le 30 octobre 2026 : cochée.
- Dépendances et prérequis : rattachement individuel NON VÉRIFIABLE dans les tableaux de tâches ; consulter les sources du change ci-dessus avant engagement.
- Critères et contrôles : exécution de la tâche telle que libellée, avec ses précisions et exigences de conception conservées ; aucune recette supplémentaire n’est créée par cette annotation.
- Preuves disponibles à recouper : [VALIDATION.md](VALIDATION.md) ; [design.md](design.md) et commentaires de preuve attachés à la tâche dans le texte conservé.
- État de qualification actuelle : NON VÉRIFIABLE sur ce seul relevé ; case et états historiques conservés, sans nouvelle validation ni livraison.
