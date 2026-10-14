# formalize-pa-pzt-and-distribution

## Pourquoi

Les cadrages PA/PZT sont intégrés et les décisions sont validées ; les capacités
OpenSpec correspondantes manquent. Le développeur limite explicitement cette
session à leur rédaction et déclaration, sans implémentation.

## Ce qui change

- Déclarer pixs-agent : quatre binaires, sept modes, droits, contrats, recette
  R01–R68 et compilation Nuitka pour trois binaires / Cython pour PZT.
- Déclarer pzt : module essentiel PBO, exécution PA, réseau WireGuard et
  contrats détaillés des 174 décisions déjà validées, dont 74 compléments PA.
- Aligner deb-package, docker-image, runtime et reference-runtime sur les
  périmètres PA/PBO/PFO, la distribution quatre/trois binaires et les états PA.
- Mettre à jour les cadrages, README et CHANGELOG pour distinguer spécifié,
  implémenté, qualifié et publié.

## Impact et limites

Spécifications et documentation uniquement. Aucun code/test logiciel, dépendance
installée, binaire, paquet, image, signature, clé, réseau, base ou publication.
Aucune opération Git. Versions/outils exacts, paramètres ouverts et preuves de
recette restent à établir. La première qualification future est Debian/Linux
et Docker locaux puis les autres cibles ; la première livraison envisagée reste
locale, expérimentale et signée selon artifact-publication.

## Critères d’acceptation

Deux capacités canoniques déclarées ; quatre capacités existantes alignées ;
174 références et contrats applicables tracés ; 68 recettes conservées ;
validation OpenSpec et contrôles documentaires réussis ; code et environnement
préservés. L’archivage ne porte que ce change documentaire après preuves.
