# Conception du vocabulaire de démarrage

## Référentiel et frontière

La capacité initial-administration, exigence « Modes de démarrage explicites », fixe les quatre valeurs INSTALLER, FIRST_CONFIGURATION, NORMAL et MAINTENANCE. Cette réalisation minimale ne précise aucun choix ouvert. Les cadrages confient les règles aux propriétaires applicatifs ; le module appartient donc au backend et n’ajoute pas une responsabilité métier au Kernel.

## Représentation

src/pixs/backend/startup_mode.py expose uniquement StartupMode(Enum) et __all__ = ["StartupMode"], sans mixin str, alias, normalisation, valeur par défaut ou façade supplémentaire. Le patron reprend le vocabulaire ArchitectureDecisionState déjà livré.

## Validation

Les tests unitaires vérifient le contrat public exact et les refus sans normalisation. L’intégration importe la façade backend puis le vocabulaire dans un processus frais -I -B avec environnement synthétique minimal. Des gardes éprouvées par contrôles positifs détectent les écritures, accès réseau, créations de processus, lectures d’environnement et imports de bases/Django. La façade garde ses exports et ses modules mécaniques existants.

Compiler les trois fichiers et exécuter les tests du vocabulaire ainsi que les régressions backend pertinentes. Vérifier UTF-8/LF, périmètre et conformité OpenSpec ciblée ; conserver l’exit réel des validations globales et leurs éventuels warnings préexistants.

## Limites et retour

Aucun marqueur externe, choix de mode au démarrage, état initial en base, authentification, transition, audit, service ou installation. Aucune qualification PostgreSQL ou navigateur n’est pertinente pour ce module pur. Aucun fichier existant n’est modifié. Un retrait éventuel de ces seuls fichiers nouveaux exige une autorisation distincte ; aucun mécanisme de retour automatique n’est créé.
