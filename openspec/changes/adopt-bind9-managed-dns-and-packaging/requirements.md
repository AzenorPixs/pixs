# Références et décision BIND 9

## Source de la décision

Le développeur a retenu BIND 9 fourni par Debian, installé et configuré par PA,
avec présence dans Docker Pixs. Il a confirmé « Choix BIND 9 et packaging ;
activation ultérieure », puis demandé un dossier OpenSpec distinct. Aucun
numéro de version, topologie, port ou droit d'infrastructure n'est ajouté
par interprétation.

Le 24 octobre 2026, le développeur a validé la spécification présentée et
autorisé l'ouverture de ce change sans implémentation ni production de code.
Cet accord confirme les trois exigences et neuf scénarios du dossier ;
il ne lance aucune réalisation ni activation. La synchronisation a ensuite été
explicitement autorisée le même jour avec les renvois Z05/Debian/Docker,
toujours sans implémentation ni production de code.

## Références normatives existantes

| Source | Obligations conservées | SHA-256 du relevé |
|---|---|---|
| [openspec/specs/pzt/spec.md](../../specs/pzt/spec.md) | A06c–A06k : gestion essentielle, exécution PA distincte, DoT, cache/TTL, vues, suffixe et absence de repli | 6a666454ee45da31cdd1c61e1bf4d9d1383311b3cea19c01b028f340bc1e1349 |
| [openspec/specs/deb-package/spec.md](../../specs/deb-package/spec.md) | Paquets, versions, données/secrets hors paquet, lifecycle et distribution PA/PBO séparée | 0451c3c94bf4c99e30578780dc2f4ac2c3b6367b9d4d3da493a12dc9f56874a3 |
| [openspec/specs/docker-image/spec.md](../../specs/docker-image/spec.md) | Image sans état/secret, activation et supervision selon le profil, processus PA/PZT présents | 4267e07ceeaea6a456d8a04a0af35cbf78c2df68c799221cc1d1cc0c47aa4c9b |

Les empreintes du tableau désignent le canon après synchronisation BIND 9
du 24 octobre 2026 ; elles ne qualifient pas le logiciel. Toute nouvelle
dérive impose relecture des clauses affectées.
Les deltas ajoutent trois exigences et neuf scénarios : un choix logiciel
et deux règles de distribution. Ils ne réécrivent pas les contrats détaillés
A06c–A06k ni leur exception Super Admin applicative.

### Recoupement à l'ouverture du 24 octobre 2026

Les trois canons et les quinze liens internes ont été contrôlés à nouveau.
Les empreintes deb-package et docker-image sont inchangées. Le canon PZT
ajoute le profil X.509 des terminaux initiaux Z12 et la résolution locale
du matériel TLS sous propriétaire courant. Son préfixe antérieur est
reconstitué octet pour octet et retrouve l'empreinte
652aeb4b9ab911bbafb7b3f9f3c7ad582b5bed8af5a806ce9925579caaf7aba5.
Les clauses DNS A06c–A06k sont donc conservées ; aucune émission de certificat,
résolution de matériel TLS ou autorité initiale n'est ajoutée par BIND 9.
Ce recoupement décrit le relevé d'ouverture, antérieur à l'ajout des trois
exigences BIND 9 ; le tableau ci-dessus est actualisé après synchronisation.

## Répartition des preuves

| Objet | Propriétaire / dossier | Ce que ce dossier ne prouve pas |
|---|---|---|
| Gestion souhaitée et contrats | [C14](../archive/2026-10-23-add-essential-pbo-pzt-and-dns-modules/proposal.md) | BIND installé ou service actif |
| Exécution DNS et adapters PA | [Z05](../add-pzt-managed-dns-service-and-pa-adapters/proposal.md) | Transport, DoT, vues ou états appliqués qualifiés |
| Instruction autorisée | [PA01](../add-pa-authorized-instruction-execution/proposal.md) | Mandat/exécutant disponibles par leur seule documentation |
| Gestion Agent | [PA10](../separate-pa-pzt-and-pbo-management-modules/proposal.md) | Garantie d'un exécutant ou canal PZT réel |
| Image | [Docker Pixs](../build-and-qualify-pixs-docker-image/proposal.md) | Artefact construit, état/secret absent de toutes les couches |

Aucune absence de dépendance, non-sélection ou fixture n'est marquée PASS.
Le canon est synchronisé pour les trois exigences BIND 9 validées. Les cadrages
communs et les archives existantes sont conservés ; aucune archive nouvelle
ni réalisation n'est produite par cette adoption documentaire.


## Correspondance exacte entre les deltas validés et le canon synchronisé

| Capacité | Exigence canonique | Scénarios intégrés |
|---|---|---|
| pzt | [Fournisseur BIND 9 du DNS géré sur Debian et Docker Pixs](../../specs/pzt/spec.md#L13402) | 3 |
| deb-package | [Installation BIND 9 par le PA du rôle serveur DNS Debian](../../specs/deb-package/spec.md#L113) | 3 |
| docker-image | [Logiciel BIND 9 fourni dans Docker Pixs sans activation implicite](../../specs/docker-image/spec.md#L131) | 3 |


Les trois blocs sont copiés intégralement depuis les deltas validés, sans
modifier les clauses canoniques préexistantes. Les deltas sont conservés
comme provenance de la décision ; aucune seconde application ni archive
n'est engagée. Les renvois de conception et d'exigences de Z05, C18, PA09
et X01 sont raccordés à ces exigences, sans cocher leurs tâches produit.
