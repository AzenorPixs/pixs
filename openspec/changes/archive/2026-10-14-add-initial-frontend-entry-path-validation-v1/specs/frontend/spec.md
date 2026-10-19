## MODIFIED Requirements

### Requirement: Syntaxe lexicale préparatoire FrontendEntryPath v1

Le profil préparatoire FrontendEntryPath v1 MUST accepter uniquement une chaîne non vide encodable en UTF-8, relative POSIX, faite de segments non vides séparés par `/`. Il MUST refuser les segments `.` et `..`, les caractères `\`, `:`, `?`, `#`, `%`, ainsi que U+0000 à U+001F et U+007F. Il MUST NOT normaliser, retirer des espaces ni décoder l'entrée.

#### Scenario: Chemin relatif reconnu lexicalement

- **WHEN** l'entrée est `frontend/routes/contacts`
- **THEN** elle est reconnue dans le seul profil lexical v1

#### Scenario: Forme hors profil refusée

- **WHEN** l'entrée est vide, non encodable en UTF-8, absolue, contient un segment vide, `.` ou `..`, ou un caractère interdit
- **THEN** elle est refusée sans correction ni décodage implicite

### Requirement: Limites du contrôle lexical FrontendEntryPath v1

Le contrôle FrontendEntryPath v1 MUST rester purement lexical et MUST NOT accéder au système de fichiers, résoudre un lien symbolique, enregistrer, composer, charger ou activer une contribution. Il MUST NOT définir de champ de manifest ni établir l'existence, le confinement physique ou la confiance du code.

#### Scenario: Résultat lexical sans effet ni preuve physique

- **WHEN** le contrôle v1 évalue une entrée
- **THEN** son résultat porte uniquement sur sa syntaxe, sans accès au système de fichiers ni preuve d'existence, de confinement ou de confiance
