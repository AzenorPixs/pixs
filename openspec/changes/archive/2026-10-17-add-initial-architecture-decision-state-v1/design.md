# Conception du vocabulaire initial

## Référentiel

openspec/specs/architecture-decisions/spec.md, exigence « États traçables », fournit les quatre états. Les exigences « Décision contextualisée » et « OpenSpec reste normatif », ainsi que la relation entre décisions remplacées, restent hors de ce sous-lot. Le vocabulaire n’impose aucun choix architectural ni transition.

## Implémentation minimale

src/pixs/kernel/architecture_decision_state.py définit uniquement ArchitectureDecisionState(Enum) et __all__ = ["ArchitectureDecisionState"]. Les noms et valeurs sont PROPOSED, ACCEPTED, SUPERSEDED et REJECTED, sans alias ni normalisation. La convention Enum sans mixin str réutilise le patron existant de data_persistence.py. Aucune façade __init__ n’est modifiée.

## Validation

Les unités contrôlent noms, valeurs, ordre, absence d’alias, export et refus des valeurs non déclarées. L’intégration réutilise le protocole existant d’import en processus frais -I -B, environnement synthétique minimal et gardes avec contrôles positifs des écritures, réseau, processus, environnement et bases. Les imports mécaniques existants ne doivent pas être étendus. Syntaxe des trois fichiers, régressions des façades et pureté, UTF-8/LF et validations OpenSpec ciblées sont requis.

## Limites et retour

Aucune mutation persistante, base réelle, session, provider, interface ou installation. Aucun delta normatif n’est nécessaire : la métadonnée skip_specs: true est déjà utilisée par les dossiers de réalisation du canon courant. Ne pas confondre le vocabulaire avec une décision validée ou une traçabilité complète. Aucun fichier préexistant n’est supprimé ou remplacé.
