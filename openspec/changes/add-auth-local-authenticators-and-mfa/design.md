# Conception — Méthodes locales modernes et MFA extensible

## Statut

PROPOSITION_DOCUMENTAIRE. Change ouvert sans implémentation ni production de code. Les spécifications sont proposées, sans synchronisation ni archivage. La recette ci-dessous reste à exécuter lors d'un mandat de réalisation distinct.

## Frontières et architecture

Les sous-modules proposés sont `pixs.auth.local.password`, `.webauthn`, `.totp` et `.recovery`. Ils sont livrés dans le profil local ; leur présence ne force pas l'enrôlement de toutes les méthodes. C03 conserve les sessions. Les contrats d'assurance existants restent partagés ; l'évaluation runtime vérifie les preuves réelles.

PostgreSQL porte les liens, empreintes non réutilisables, politiques et états de consommation. Les graines TOTP et clés privées suivent la protection de secrets déclarée ; elles ne sont pas sérialisées en clair en base métier. Un hash de mot de passe ne peut pas être converti en graine TOTP ou clé Kerberos.

Empreinte digitale et visage activent de préférence une clé localement via WebAuthn. Pixs reçoit la preuve cryptographique sans gabarit biométrique. Une reconnaissance biométrique centrale serait un périmètre spécialisé ultérieur ; elle n'est pas sélectionnée ici. Cartes à puce et certificats exigent leurs profils/adaptateurs qualifiés.

Le MFA combine des facteurs indépendants prouvés : deux présentations du même secret ou une seconde source dérivée ne suffisent pas. Le parcours Super Admin conserve intégralement son exception canonique, y compris absence de MFA imposé au premier démarrage et au secours.

Références : [WebAuthn](https://www.w3.org/TR/webauthn-2/) et [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html).

## Dépendances

- [define-essential-autonomous-auth-module](../define-essential-autonomous-auth-module/proposal.md).
- [add-initial-authentication-and-sessions](../add-initial-authentication-and-sessions/proposal.md).
- [add-core-postgres-services](../add-core-postgres-services/proposal.md).
- [add-durable-minimized-audit](../add-durable-minimized-audit/proposal.md).

Les contrats de secrets, autorisation, audit, gouvernance, périmètre et reprise restent applicables. L'exception Super Admin de authorization/initial-administration s'applique dans son seul périmètre aux contrôles runtime ; elle ne crée ni preuve cryptographique ni conformité de protocole absente.

## Arbitrages avant réalisation

Bibliothèques et versions, profils de hash et migration d'empreintes, politiques de mots de passe, paramètres TOTP/fenêtres anti-rejeu, challenges WebAuthn/RP/origines, authenticators synchronisés ou liés à l'appareil, codes de récupération, budgets de tentatives et facteurs requis par action.

Les choix de produits non arrêtés et dépendances supplémentaires exigent la revue applicable avant code. Aucun paramètre numérique arbitraire n'est réputé adopté.

## Migration et retour

Réutiliser les UUID et contrats existants. Définir migrations, reprise idempotente, état incomplet, plan d'arrêt/retrait et impacts sur sessions/clients avant réalisation. Aucun renommage, suppression, réinitialisation de base ou mouvement de fichier dans cette préparation. Le retour ne doit pas réadmettre un justificatif révoqué ou restaurer implicitement une confiance.

## Recette future

- Recetter chaque méthode sur la composition PostgreSQL réelle ; tester expirations, rejeux et limites de tentatives.
- Tester changement de facteur, élévation, récupération concurrente et absence de MFA artificiel ou exigé au secours.

Relier les scénarios du delta à l'artefact et aux versions effectivement qualifiés. Les mocks et contrôles documentaires ne prouvent pas la disponibilité de la capacité.
