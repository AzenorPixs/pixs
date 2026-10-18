# Conception — EventEnvelopeKind v1

## Référentiel et frontière

Le schéma canonique EventEnvelopeV1, sous B11 de events, fixe kind à DOMAIN ou INTEGRATION. Le backend reste propriétaire de cette enveloppe runtime ; un vocabulaire passif ne transfère aucune responsabilité au Kernel.

## Représentation

src/pixs/backend/event_envelope_kind.py expose uniquement EventEnvelopeKind(Enum) et __all__ = ["EventEnvelopeKind"]. Les noms et valeurs sont identiques dans l’ordre DOMAIN, INTEGRATION. Aucun mixin str, alias, défaut, normalisation, helper ou façade n’est ajouté.

Les validateurs, records, migrations, DomainEventContract et IntegrationEventContract existants restent inchangés. Un membre Enum n’est pas une chaîne exacte : son passage direct aux gardes existantes reste refusé ; sa valeur textuelle peut être fournie explicitement sans branchement nouveau.

## Validation

Les tests unitaires vérifient le contrat public et les recherches exactes. Les tests d’intégration éprouvent les deux valeurs contre le garde complet EventEnvelopeV1 existant et le refus des objets Enum. Un processus frais -I -B vérifie l’import sans dépendance Django/base, écriture, réseau, processus ou lecture d’environnement ; les gardes sont éprouvées par contrôles positifs.

Compiler les trois fichiers, exécuter les tests ciblés et les régressions des enveloppes et contrats existants. Contrôler UTF-8/LF, contenu et périmètre ; exécuter les validations OpenSpec ciblées et globales en conservant leurs codes réels et les éventuels avertissements préexistants.

## Limites

Aucune migration, base de données, API, interface graphique ou opération externe. PostgreSQL et navigateur ne sont pas pertinents pour ce vocabulaire pur. Aucun effet d’envoi ou de déduplication, aucune garantie exactly-once. Le retrait éventuel des seuls nouveaux fichiers exige une autorisation distincte.
