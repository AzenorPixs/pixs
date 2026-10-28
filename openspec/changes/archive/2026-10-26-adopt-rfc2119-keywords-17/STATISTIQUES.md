# STATISTIQUES — lot 17 — migration RFC 2119

Rapport créé lors du découpage validé le 2026-10-26, daté 2026-10-26T20:28:25.273105+00:00. Ce lot est dérivé de 2026-09-10-adopt-rfc2119-keywords ; il ne représente pas une nouvelle fonctionnalité. Les données de l'implémentation historique restent N/A, sans reconstitution. Les mesures partagées de l'intervention figurent uniquement dans le [rapport global](../2026-09-10-adopt-rfc2119-keywords/STATISTIQUES.md) et ne doivent pas être additionnées depuis les lots.

### Agents de codage

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---|
| Codex — modèle exact non exposé | N/A | OpenAI | N/A | N/A | N/A | N/A |

### Agents orchestrateurs

| Modèle de LLM | Version | Fournisseur | Niveau de raisonnement | TTMT moyen | Tokens/seconde moyens | Temps de service (% total) |
|---|---|---|---|---:|---:|---|
| Aucun agent orchestrateur distinct | N/A | N/A | N/A | N/A | N/A | N/A |

## 1. Statistiques générales et décisions

Le développeur a explicitement autorisé le découpage et les archivages --skip-specs. Ce suivi est exécuté directement par Codex, sans RUN CAB nouveau et sans attribution des anciens compteurs OpenCode.

| Mesure du lot | Valeur | Part de la collection |
|---|---:|---:|
| Fichiers normatifs | 3 | 5,4 % des 56 fichiers |
| Exigences | 9 | 4,4 % des 205 exigences |
| Scénarios | 9 | 4,4 % des 206 scénarios |
| Lot archivé | 1 | 4,8 % des 21 lots |

Trois séries de contrôles API stricts vérifient les mêmes 21 lots (avant archivage, après archivage isolé, après publication). Pour ce lot : proposition et deltas valides aux trois étapes, soit 6/6 résultats conformes (100,0 %), 0/6 erreur (0,0 %). Il ne s'agit pas de six lots ou de six commandes distinctes. Les [preuves de validation](VALIDATION.md) distinguent ces étapes et le contrôle de resynchronisation.

Temps de service, tokens, cache, coût et compactions de l'agent direct : N/A, télémétrie attribuable non collectée. Sondes : N/A, non activées ; aucune mesure rétroactive.

## 2. Types de messages et d'outils

Messages et outils Codex par type : N/A, historique quantitatif complet non collecté. Le [registre global](../2026-09-10-adopt-rfc2119-keywords/STATISTIQUES.md) couvre les commandes de contrôle et d'archivage instrumentées, pas l'intégralité des outils de l'agent. Une commande terminée ne prouve pas la réussite d'une validation : les champs valid et les diagnostics sont examinés séparément.

## 3. Fichiers modifiés

Les fichiers normatifs sont transférés entiers, sans modification de contenu. Les métadonnées, tâches, README, preuves et ce rapport sont créés pour tracer ce lot. Le nombre total de tentatives d'édition de l'agent est N/A faute de télémétrie correspondante ; les chemins et empreintes effectivement publiés figurent au [manifest](../../../../output/rfc2119-split/20261026T200749Z/manifest.json).

| Fichier normatif publié | Conservation | Part des fichiers du lot |
|---|---|---:|
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-adopt-rfc2119-keywords-17/specs/data-governance/spec.md | Octets identiques à la sauvegarde (1/1, 100,0 %) | 33,3 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-adopt-rfc2119-keywords-17/specs/data-lifecycle/spec.md | Octets identiques à la sauvegarde (1/1, 100,0 %) | 33,3 % |
| /home/devops/datas/pixs/openspec/changes/archive/2026-10-26-adopt-rfc2119-keywords-17/specs/scope-context/spec.md | Octets identiques à la sauvegarde (1/1, 100,0 %) | 33,3 % |
| Total | 3/3 fichiers intacts | 100,0 % |

## 4. Commandes

| Opération bornée de ce lot | Nombre | Réussie | Refusée | Erreur |
|---|---:|---:|---:|---:|
| archive adopt-rfc2119-keywords-17 --yes --skip-specs --json | 1 | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |
| Total de l'archivage de ce lot | 1 | 1 (100,0 %) | 0 (0,0 %) | 0 (0,0 %) |

Le [reçu natif](../../../../output/rfc2119-split/20261026T200749Z/archive-17-native.json) conserve argv complet, répertoire de préparation, horodatages, stdout, stderr et code de retour 0 ; specsUpdated=false. Les validations groupées ne sont pas artificiellement comptées comme autant de commandes par lot.

## 5. Accès web

Aucun outil de navigation web observé pendant ce découpage. URLs de visite : aucune ; nombre observé 0. Taux sur un dénominateur de 0 : N/A. Le transport du modèle et les API locales ne sont pas mesurés ici. Aucun accès refusé n'est présenté comme une visite réussie.

## 6. Synthèse globale

| Mesure temporelle du lot | Valeur |
|---|---|
| Début de la commande d'archivage | 2026-10-26T20:17:26.312623+00:00 |
| Fin de la commande d'archivage | 2026-10-26T20:17:26.448415+00:00 |
| Durée totale de travail propre à ce lot | N/A — préparation et vérifications partagées, non ventilées |

| Mesure du quota Codex sur 7 jours | Horodatage | Quota utilisé | Réinitialisation |
|---|---|---:|---|
| Avant — propre au lot | N/A | N/A | N/A |
| Après — propre au lot | N/A | N/A | N/A |
| Différence propre au lot | — | N/A | — |

Les relevés existent globalement dans le [rapport du lot 01](../2026-09-10-adopt-rfc2119-keywords/STATISTIQUES.md) ; ils ne prouvent pas une consommation exclusive par lot. Ils ne sont donc pas redistribués dans ces lignes.

Le lot est archivé et validé dans le profil historique documentaire ; l'archivage a été effectué dans la préparation isolée puis publié. Il ne synchronise pas le canon. Le profil comparé au canon actuel conserve globalement 8 écarts de scénarios ultérieurs (13/21 lots valides) ; il ne permet pas de réappliquer ces anciens deltas. Le résultat individuel est détaillé dans [VALIDATION.md](VALIDATION.md).

Les 56 fichiers, 205 exigences et 206 scénarios de la collection sont conservés sans duplication ; les 78 empreintes du canon restent identiques. 3.1 est conforme pour cette qualification structurelle historique, sans qualification de resynchronisation ; 2.1 reste NON VÉRIFIABLE. Aucun code, Git ou comportement runtime n'est modifié ; aucune exposition de secret n'est observée dans les sorties autorisées.
