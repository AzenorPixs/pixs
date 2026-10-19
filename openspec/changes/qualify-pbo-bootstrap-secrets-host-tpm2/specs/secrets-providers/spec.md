## ADDED Requirements

### Requirement: Protection combinée des secrets d’amorçage PBO

Sur un hôte compatible du profil Debian local, les sources persistantes des secrets d’amorçage PBO MUST être chiffrées et authentifiées avec le mode systemd host+tpm2 explicitement sélectionné. Leur remise MUST conserver le transport LoadCredentialEncrypted, l’identité native, la politique, l’audit et le cycle de vie C01. Les sources et clés réelles MUST rester hors dépôt, paquet et image.

#### Scenario: Hôte autorisé disposant des deux facteurs

- **WHEN** le service démarre sur une plateforme qualifiée avec la clé hôte et le TPM autorisés
- **THEN** il obtient uniquement ses références autorisées sous les contrôles C01 et la preuve identifie le mode combiné utilisé sans révéler de valeur

#### Scenario: Copie du stockage sur une autre machine

- **WHEN** les fichiers chiffrés et la clé hôte sont copiés vers une machine sans le TPM d’origine
- **THEN** cette copie ne permet pas le déchiffrement sous le profil combiné et aucun fallback ne remet la valeur

### Requirement: Absence de dégradation implicite de la protection matérielle

Un TPM absent, incompatible ou non vérifiable MUST empêcher la qualification et l’admission sous le profil host+tpm2. Un mode null, host seul ou automatique sans preuve des deux facteurs MUST NOT satisfaire ce profil. Une autre protection MUST être explicitement sélectionnée et qualifiée avant admission, sans repli silencieux.

#### Scenario: Machine sans TPM utilisable

- **WHEN** le prévol ne démontre pas un TPM compatible avec la protection retenue
- **THEN** la dimension est déclarée non qualifiée et la mise en production sous ce profil est bloquée sans bascule vers host seul

#### Scenario: Fixture chiffrée en mode nul

- **WHEN** les seuls essais réussis utilisent le mode null ou prouvent uniquement le transport de credentials
- **THEN** ils restent des preuves fonctionnelles et ne permettent pas d’annoncer la confidentialité ou l’authenticité de production

### Requirement: Politique de démarrage et plateformes de protection déclarées

Le profil MUST déclarer les versions, le type de TPM, la protection de la clé hôte et la politique de mesures de démarrage et de mise à jour effectivement retenue. TPM physique, TPM transmis et vTPM MUST être qualifiés selon leurs frontières propres. Une modification de politique MUST préserver un chemin de reprise contrôlé sans désactivation implicite des vérifications.

#### Scenario: Mise à jour autorisée de la plateforme

- **WHEN** une mise à jour modifie les mesures couvertes par la politique retenue
- **THEN** sa transition est préparée et testée sous cette politique, ou le service reste non prêt avec un chemin de récupération déclaré

#### Scenario: Substitution par un vTPM non qualifié

- **WHEN** une installation substitue un vTPM à un TPM physique sans preuve propre à cette plateforme
- **THEN** elle ne conserve pas automatiquement le verdict de protection de l’hôte précédent

### Requirement: Preuve cryptographique distincte des essais fonctionnels

La qualification MUST produire des preuves versionnées du mode combiné sur la plateforme cible, avec déchiffrement autorisé et refus pour facteur manquant ou incorrect, données altérées et politique incompatible. Elle MUST déclarer les limites face au contrôle de l’hôte et à la lecture mémoire. Un test C01 isolé MUST NOT valoir cette qualification ni celle du produit complet.

#### Scenario: Facteur incorrect ou credential altéré

- **WHEN** un essai remplace la clé hôte, retire le TPM, altère le ciphertext ou viole la politique de démarrage
- **THEN** chaque cas applicable prouve le refus sans secret exposé et toute dimension non exécutée reste explicitement non qualifiée

#### Scenario: Processus consommateur compromis

- **WHEN** une revue évalue la protection d’une valeur déjà remise au processus autorisé
- **THEN** la preuve ne prétend pas que le chiffrement au repos empêche sa lecture en mémoire par un attaquant contrôlant ce processus ou l’hôte
