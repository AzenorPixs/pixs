# Design — formalize-pa-pzt-and-distribution

## Source et autorité

PROJECT §43–§44, TECHNICAL §42–§45 et BUILD §46–§47 sont les sources du cadrage
validé. Leur trace est conservée dans TRACABILITE.md. OpenSpec devient la source
normative des exigences déclarées ; la prose historique du cadrage n’est pas
une nouvelle décision ou une preuve d’implémentation.

## Formalisation conservatrice

pixs-agent porte les quatre binaires, la séparation des sept modes, les droits,
les opérations locales et R01–R68. pzt porte les garanties réseau, le module
essentiel PBO et les 174 contrats détaillés. Les clauses opératoires sont
intégrées en texte dans chaque exigence, plutôt que remplacées par une référence
au cadrage. Les options rejetées, notes historiques et paramètres non décidés
sont distingués par les règles de lecture normative ; les obligations des
profils/traitements ne sont pas généralisées à chaque PA ordinaire.
Les exemples de recette sont des scénarios à exécuter ultérieurement.

## Décisions ultérieures préservées

Quatre binaires Debian et trois Docker, sans utilisateur dans Docker.
Nuitka compile démon système, événements système et utilisateur ; Cython compile
PZT. Le module PZT est essentiel côté PBO même désactivé. Le réseau activé est
exécuté par le binaire PA/PZT. Les contrôles applicatifs conservent l’exception
Super Admin transversale sans preuve inventée ou credentials transférés.

## Frontières des capacités existantes

deb-package et docker-image gardent leurs garanties de sécurité ; seules leurs
compositions/corrélations sont précisées. runtime/stateless est explicitement
PBO ; les états locaux techniques PA ne deviennent pas de l’autorité métier.
reference-runtime conserve la pile PBO/PFO, les politiques Django et toutes
les autres exigences. artifact-publication demeure inchangée, signatures requises
y compris pour une livraison locale expérimentale.

## Validation et retour

Valider d’abord les deltas, puis déclarer les canons et vérifier leur identité
exacte avec les deltas attendus. Comparer empreintes du code, environnement,
configuration et spécifications non ciblées ; vérifier contrats, choix B,
dates, R01–R68, UTF-8/LF et liens locaux. Aucun test d’exécution n’est pertinent
pour ce change purement documentaire. La synchronisation manuelle prouvée
permet l’archivage avec --skip-specs, sans réappliquer les mêmes deltas.
Les fichiers antérieurs sont préservés hors modifications ciblées ; aucune
migration de données, installation ou opération externe n’est prévue.

## Résultats et limites de validation

Les six capacités ciblées et le change passent la validation stricte sans
avertissement. La validation globale standard réussit 79/79. Le mode strict
global est affecté par trois WARNING de longueur préexistants dans bulk-operations,
dont le fichier est inchangé ; ils sont hors périmètre et ne sont pas corrigés
ou masqués. Les avertissements introduits dans les exigences ciblées ont été
résolus par séparation des comportements, sans supprimer les scénarios existants.
