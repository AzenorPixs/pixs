# Conception du profil mémoire tombstone-v1

## Sources et frontière

Le requirement « Profil structurel préparatoire de tombstone v1 » de openspec/specs/data-lifecycle/spec.md est la référence, avec TECHNICAL.md §14.3 et PROJECT.md §2.15. Le patron local est data_outbound_declaration.py et ses diagnostics VALIDATE. Le delta reprend exactement le bloc canonique ; aucune nouvelle règle normative ni modification des cadrages.

## Représentation et validation

src/pixs/kernel/data_tombstone_profile.py définit TombstoneProfile par dataclass(frozen=True), dans l'ordre canonique des huit champs, sans défaut. __all__ contient TombstoneProfile et validate_data_tombstone_profile, sans modification de la façade kernel.

validate_data_tombstone_profile(candidate: object) retourne list[Diagnostic]. Le candidat doit avoir le type exact TombstoneProfile. Les références exigent type(value) is str et une chaîne non vide ; les cinq références éventuelles acceptent aussi None explicite. Aucune normalisation ni résolution. deletion_version exige type(value) is int et une valeur >=0, donc refuse bool et les sous-classes.

deleted_at exige une str exacte. Une expression régulière complète à chiffres ASCII fixe le format YYYY-MM-DDTHH:MM:SS, fraction optionnelle de 1 à 6 chiffres, puis Z ou +00:00. Une construction calendaire standard vérifie année, mois, jour et heures/minutes/secondes, sans consulter d'horloge. Aucun instant ne sera normalisé ou stocké sous un autre type.

La règle croisée est vérifiée par identité : scope_id is not None et tenant_id is None produit un diagnostic scope_context. Les diagnostics utilisent le préfixe data_tombstone_profile., l'étape VALIDATE et des contraintes/messages statiques sans valeur. Ils sont triés et dédupliqués par (element, constraint, message).

## Validations et preuves

Tests unitaires : surface et ordre exacts, champs tous explicites, immutabilité, conservation opaque, UTC Z/+00:00 et fractions, limites calendaires et bissextiles, mauvais types/sous-classes/objets hostiles, version booléenne/négative, portée, diagnostics stables triés uniques sans écho.

Intégration : import et validation dans un processus frais -I -B sous environnement réduit, gardes positives d'entrée/sortie, réseau, processus, environnement, base et horloge ; aucune activité sur ces surfaces pendant les opérations testées. Artefacts temporaires confinés à la racine et nettoyés.

Compilation des trois fichiers et tests ciblés avec /home/devops/python/current/bin/python3. Régressions des profils et vocabulaires de données, diagnostics, pureté Kernel et façades. Validation OpenSpec du change et du canon, puis globale qualifiée : codes natifs conservés, avertissements historiques de longueur distingués conformément à la demande explicite. Vérification UTF-8/LF, delta identique au canon et empreintes des fichiers de référence sans Git.

Les tâches ne sont cochées qu'après ces preuves. L'archive est une commande distincte avec --skip-specs et décision CGPT distincte ; le rapport STATISTIQUES.md à six sections est obligatoire après l'archive.

## Limites

Le profil reste interne, partiel et mémoire. Aucune suppression, purge, persistance, propagation, reconstruction, restauration, outbox, politique, fournisseur, format réseau, façade publique, configuration, dépendance ou base utilisée. Aucune valeur None ne fournit d'autorisation ou d'exemption. Les garanties générales du canon restent à réaliser par les futures intégrations.
