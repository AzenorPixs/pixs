## Context

Les sources normatives restent bulk-operations B05/B13, PolicyV1, MappingDescriptorV1, RowDiagnosticV1 et JSONValueV1 dans events. Les sources des contrats, ports serveur et persistance précédemment livrés sont préservées par empreinte. La capacité de production n'est pas présumée par les tests synthétiques.

## Goals / Non-Goals

Décoder et mapper un flux IMPORT de segments bytes exacts avec mémoire et diagnostics bornés. Une ligne parsée/mappée n'est ni une validation du schéma métier propriétaire, ni une mutation, ni un checkpoint engagé. Aucun accès de stockage ou itérateur fourni par payload ; seul le code serveur alimentera le parseur.

## Decisions

- API Python privée de type feed(bytes)/finish()/close(), données de mapping/politique/champs publics déclarées et capturées avant tout decode/parsing. Types exacts des clés, valeurs imbriquées et catalogues d'abord ; aucune coercition ni défaut numérique de production.
- CSV : UTF-8 strict sans BOM, virgule, guillemets doubles doublés, LF/CRLF déterministes, champs multilignes et coupures de caractères pris en charge. Le header conserve les noms exacts non vides uniques, appartient aux sources déclarées et satisfait les champs requis ; aucune normalisation, dialecte automatique ou colonne surnuméraire. Les valeurs CSV restent des chaînes, sans None implicite ni conversion métier.
- NDJSON : un objet JSON par ligne, fin LF admise, lignes vides, doublons de clés, non-finis, UTF-8/Unicode invalides et dépassements refusés. Les doublons sont détectés avant construction du dict ; parse_constant refuse les constantes non JSON et la validation JSON contrôle aussi les flottants débordés. Décoder UTF-8 explicitement avant json, sans accepter UTF-16/32 par défaut.
- Les limites proviennent de PolicyV1. Buffers et résultats de chaque appel restent bornés, aucune accumulation du fichier complet. Une limite qui empêche la consommation/vérification complète, une fermeture prématurée ou un EOF partiel interdit d'annoncer une complétude vraie. Une dernière ligne complète sans LF reste admissible.
- Les méthodes de parsing ne modifient aucun état global csv.field_size_limit ou limite entière de l'interpréteur. Si une capacité numérique physique est indisponible, produire un refus statique de capacité sans repli, coercition ou valeur reproduite.
- Mapping limité aux champs publics du propriétaire déclarés côté serveur, selon les bindings exacts déjà validés. Les références opaques ne prouvent pas autorité/existence. Les champs optionnels absents ne sont pas remplis par un défaut Bulk.
- Diagnostics de contenu conformes à RowDiagnosticV1 (code statique déclaré, champ déclaré ou None, position positive ou None), sans byte/valeur/exception utilisateur. Les erreurs de composition peuvent employer les Diagnostic Kernel statiques existants ; ne pas confondre les deux contrats. Les structures intermédiaires sont des choix Python internes, pas un schéma logique supplémentaire.
- Aucune méthode owner, gouvernance, audit ou stockage n'est exécutée par ce lot. L'autorisation, la gouvernance, l'immutabilité des versions source et les transactions restent les responsabilités des étapes du runtime qui les composent.

## Validation

Trois compilations Python ; tests de fractionnements arbitraires, UTF-8, BOM, LF/CRLF, quotes multilignes, headers, colonnes, JSON doublons/non-finis, bornes et complétude, fermeture et types hostiles ; intégration fraîche sous gardes positives fichiers/réseau/processus/environ/DB/Core concret. Les 258 tests existants de 34 modules sont regroupés en une invocation <=2000 caractères sous mandat distinct. Aucun PG réel rejoué car ORM/migrations inchangés et preuves antérieures conservées par empreinte. Strict change sans issue ; global qualifié seulement par les trois WARNING historiques exacts et aucune nouvelle issue. UTF-8/LF, sources et périmètre vérifiés, puis archive unique et rapport distinct obligatoire.

## Références techniques

- Python 3.12 csv : https://docs.python.org/3.12/library/csv.html
- Python 3.12 json : https://docs.python.org/3.12/library/json.html

Ces références guident les choix stdlib sans remplacer le canon OpenSpec validé.
