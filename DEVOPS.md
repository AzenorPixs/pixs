# DEVOPS.md — pixs

Version : 0.6

Généré automatiquement par Debian Installeur Unifié (DIU).
Début du relevé (UTC) : 2026-10-19T13:28:09Z
Environnement d'exécution DIU : PHYSICAL

Les sondes système concernent le contexte d'exécution DIU.
Les outils DevOps sont interrogés avec les binaires indiqués dans leurs rubriques.
Les dépendances Python sont recherchées en priorité dans les venv du projet, puis dans le Python DevOps en repli explicite.
Dans l’inventaire Python, la flèche indique le Python sondé ; Installation indique le chemin observé dans les métadonnées.
Les dépendances Python attendues proviennent de [project].dependencies dans pyproject.toml.
Les dépendances JavaScript sont regroupées par manifeste et catégorie sous NPM et OpenCode.
Leurs déclarations, versions verrouillées npm et métadonnées locales sont distinctes ; un verrou ne prouve pas une installation.
Les contraintes JavaScript ne sont pas résolues et cet inventaire ne prouve pas le chargement de plugins OpenCode.
Un inventaire multi-environnements ne valide pas un environnement Python unique.
Cet inventaire ne constitue pas une qualification fonctionnelle ni une preuve de réussite des tests du projet.

# Système d'exploitation

  * Debian GNU/Linux 13 (trixie)


# Docker

  * 29.9.1
  * /usr/bin/docker


# Docker-Compose

  * 5.6.0
  * /usr/local/bin/docker-compose


# Git

  * 2.47.3
  * /usr/bin/git


# Go

  * 1.27.2
  * /home/devops/go/current/bin/go


# Node

  * 24.22.0
  * /home/devops/node/current/bin/node


# NPM

  * 11.19.1
  * /home/devops/node/current/bin/npm


## Dépendances JavaScript du projet

### frontend/package.json

  * Manifeste : /home/devops/datas/pixs/frontend/package.json
  * Verrous présents : /home/devops/datas/pixs/frontend/package-lock.json
  * Verrou npm retenu : /home/devops/datas/pixs/frontend/package-lock.json

#### dependencies

  * @tanstack/react-router : déclarée 1.170.41 ; verrouillée (npm) 1.170.41 ; observée 1.170.41
    * Installation : /home/devops/datas/pixs/frontend/node\_modules/@tanstack/react-router
  * react : déclarée 19.3.0 ; verrouillée (npm) 19.3.0 ; observée 19.3.0
    * Installation : /home/devops/datas/pixs/frontend/node\_modules/react
  * react-dom : déclarée 19.3.0 ; verrouillée (npm) 19.3.0 ; observée 19.3.0
    * Installation : /home/devops/datas/pixs/frontend/node\_modules/react-dom

#### devDependencies

  * vite : déclarée 8.3.1 ; verrouillée (npm) 8.3.1 ; observée 8.3.1
    * Installation : /home/devops/datas/pixs/frontend/node\_modules/vite

# OpenCode

  * 1.19.3
  * /home/devops/.opencode/bin/opencode


## Dépendances OpenCode du projet

### .opencode/package.json

  * Manifeste : /home/devops/datas/pixs/.opencode/package.json
  * Verrous présents : /home/devops/datas/pixs/.opencode/package-lock.json
  * Verrou npm retenu : /home/devops/datas/pixs/.opencode/package-lock.json

#### dependencies

  * @opencode-ai/plugin : déclarée 1.18.34 ; verrouillée (npm) 1.18.34 ; observée 1.18.34
    * Installation : /home/devops/datas/pixs/.opencode/node\_modules/@opencode-ai/plugin

# OpenSpec

  * 1.14.3
  * /home/devops/.local/npm/bin/openspec


# OpenSSL

  * 3.5.7
  * /usr/bin/openssl


# PostgreSQL Client

  * 17.11
  * /usr/bin/psql


# PostgreSQL Serveur

  * 16.15
  * 127.0.0.1:5432
  * Les variables PostgreSQL sont chargées depuis project.env
  * PG_HOST PG_PORT PG_DATABASE PG_USERNAME PG_PASSWORD


# Python

  * 3.14.8
  * /home/devops/python/current/bin/python3
  * venv: disponible


# Python - Dépendances du projet - Source de vérité `pyproject.toml`

  * Django ==6.1.2 : 6.1.2 --> /home/devops/datas/pixs/.venv/bin/python3
    * Environnement : /home/devops/datas/pixs/.venv
    * Installation : /home/devops/datas/pixs/.venv/lib/python3.14/site-packages
  * psycopg [binary]==3.3.6 : 3.3.6 --> /home/devops/datas/pixs/.venv/bin/python3
    * Environnement : /home/devops/datas/pixs/.venv
    * Installation : /home/devops/datas/pixs/.venv/lib/python3.14/site-packages
  * asgiref ==3.12.1 : 3.12.1 --> /home/devops/datas/pixs/.venv/bin/python3
    * Environnement : /home/devops/datas/pixs/.venv
    * Installation : /home/devops/datas/pixs/.venv/lib/python3.14/site-packages
  * sqlparse ==0.6.0 : 0.6.0 --> /home/devops/datas/pixs/.venv/bin/python3
    * Environnement : /home/devops/datas/pixs/.venv
    * Installation : /home/devops/datas/pixs/.venv/lib/python3.14/site-packages


# Python - Gestionnaire de paquets

  * 26.2.1
  * /home/devops/python/current/bin/pip3


# Prompts

  * Dossier des prompts : /home/devops/datas/prompts
  * Index des prompts : /home/devops/datas/prompts/INDEX.md


# Tests navigateurs extérieurs en mode headless

La détection ne vérifie pas le fonctionnement du mode headless.

## Chromium

  * 155.0.8059.79
  * /usr/bin/chromium
  * Mode headless : --headless


## Firefox

  * 153.5.0esr
  * /usr/bin/firefox
  * Mode headless : --headless
