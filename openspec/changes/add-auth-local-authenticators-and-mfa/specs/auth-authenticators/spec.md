## ADDED Requirements

### Requirement: Méthodes locales disponibles dans le profil autonome

La composition locale standard MUST fournir mot de passe, passkeys/WebAuthn, TOTP et récupération à usage unique sous politique Auth. Leur disponibilité MUST NOT exiger de fournisseur externe ni imposer l'enrôlement de toutes les méthodes. Le stockage persistant par défaut MUST être PostgreSQL sous propriété Auth.

#### Scenario: Connexion locale sans annuaire

- **WHEN** aucun annuaire ou IdP externe n'est installé et une méthode locale est enrôlée selon la politique
- **THEN** la méthode permet une authentification vérifiée et C03 établit la session selon ses garanties

### Requirement: Enrôlement et retrait vérifiés des moyens

L'ajout, le remplacement et le retrait d'un moyen MUST vérifier l'acteur, l'identité canonique, le périmètre et l'assurance requise. Un moyen retiré MUST cesser d'établir de nouveaux contextes selon la borne de révocation déclarée ; les contextes dérivés MUST être invalidés selon authentication.

#### Scenario: Remplacement non autorisé

- **WHEN** un compte ordinaire tente de remplacer le facteur d'une identité hors de son périmètre
- **THEN** aucun moyen n'est modifié et un refus sans secret est produit

#### Scenario: Moyen retiré

- **WHEN** un moyen a été retiré et sa borne de révocation est atteinte
- **THEN** sa présentation ne permet plus de nouvelle authentification ni de renouvellement

### Requirement: Preuves indépendantes et assurance réellement obtenue

Auth MUST attribuer MULTI_FACTOR ou PHISHING_RESISTANT uniquement à partir des preuves vérifiées et d'un mapping explicite. Un même secret, une preuve rejouée ou deux sources équivalentes MUST NOT être comptés comme facteurs indépendants. L'exception Super Admin MUST suivre identity-assurance sans inventer de niveau.

#### Scenario: Double présentation du même facteur

- **WHEN** deux étapes reposent sur le même secret ou la même preuve
- **THEN** Auth ne les compte pas comme deux facteurs indépendants

#### Scenario: Secours sans MFA

- **WHEN** le Super Admin utilise son authentification propre au premier démarrage ou au secours
- **THEN** aucun MFA n'est imposé et seul le niveau réellement obtenu est annoncé

### Requirement: Challenges et tentatives bornés

Les vérifications MUST utiliser les protections anti-rejeu adaptées à la méthode et une politique bornée de tentatives. Les challenges WebAuthn MUST être liés à l'opération, à la confiance du site et à une validité limitée. Une nouvelle tentative MUST NOT remettre implicitement les compteurs à zéro.

#### Scenario: Challenge WebAuthn réutilisé

- **WHEN** un challenge déjà consommé ou émis pour une autre origine est présenté
- **THEN** la vérification échoue avant création d'un contexte

#### Scenario: Nouvelle tentative après limite

- **WHEN** un demandeur renouvelle sa requête après avoir atteint le plafond applicable
- **THEN** la protection reste appliquée sans remise à zéro implicite

### Requirement: Récupération à usage unique sans restauration implicite

La consommation d'un code de récupération MUST être atomique et à usage unique. Le parcours MUST invalider les sessions concernées et MUST NOT restaurer un niveau élevé sans nouvelle preuve ou intervention autorisée. Une voie locale de récupération MUST pouvoir fonctionner sans messagerie externe obligatoire.

#### Scenario: Consommation concurrente

- **WHEN** deux requêtes présentent le même code de récupération valide
- **THEN** au plus une consommation réussit et l'autre n'établit aucun contexte

#### Scenario: Récupération sans messagerie

- **WHEN** le profil autonome ne dispose pas de messagerie externe
- **THEN** la voie locale explicitement provisionnée reste utilisable selon la politique et les exceptions applicables

### Requirement: Biométrie locale et moyens matériels optionnels

Le profil WebAuthn MUST vérifier la preuve cryptographique et MUST NOT collecter le visage, l'empreinte digitale ou leur gabarit. Les adaptateurs carte à puce et certificat MUST déclarer confiance et assurance, sans droit déduit du matériel. Une reconnaissance biométrique centrale MUST rester hors de ce profil.

#### Scenario: Vérification par empreinte ou visage

- **WHEN** l'appareil vérifie localement la personne et signe le challenge WebAuthn
- **THEN** Pixs vérifie la preuve sans recevoir de donnée biométrique

#### Scenario: Carte non approuvée

- **WHEN** une carte présente un certificat hors de la confiance configurée
- **THEN** l'authentification est refusée même si la signature est valide
