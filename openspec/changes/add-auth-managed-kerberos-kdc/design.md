# Conception — KDC Kerberos propre géré par pixs.auth

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

KZT/MIT avec backend LDAP, realm et verrouillage, provisionnement progressif et reprise critique selon profil/sauvegardes.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [auth-managed-kerberos](../../specs/auth-managed-kerberos/spec.md).
- [authentication](../../specs/authentication/spec.md).
- [pixs-domains](../../specs/pixs-domains/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Statut

PROPOSITION_DOCUMENTAIRE. Change ouvert sans implémentation ni production de code. Les spécifications sont proposées, sans synchronisation ni archivage. La recette ci-dessous reste à exécuter lors d'un mandat de réalisation distinct.

## Frontières et architecture

Le composant proposé `pixs.auth.kerberos.kdc` gère un KDC propre comme service séparé de Django. Le produit/version n'est pas sélectionné ici. Il peut être activé sans OpenLDAP ; si une composition choisit un backend LDAP, sa dépendance à l'annuaire propre devient explicite et vérifiée. Aucun connecteur de realm externe n'est requis.

PostgreSQL porte les identités canoniques et politiques/mappings Auth. Le KDC conserve uniquement son stockage cryptographique et protocolaire déclaré. Realms, principals et SPN ne remplacent pas les UUID Core ; les affiliations tenant restent résolues côté Pixs. Aucun trust inter-realm n'est créé par découverte DNS ou correspondance de noms.

L'enrôlement des clés Kerberos est distinct du stockage de mots de passe local : aucune clé n'est dérivée d'un hash de mot de passe Pixs supposé portable. Clés maîtresses et keytabs suivent le mécanisme protégé sélectionné et des comptes techniques minimaux. Leur récupération n'exige pas un secret disponible uniquement après authentification par le KDC lui-même.

Les tickets déjà délivrés peuvent conserver une validité protocolaire après un retrait. La conception distingue arrêt de nouvelle émission/renouvellement, contrôle courant côté Pixs et effet chez un service tiers. Chaque client sensible doit pouvoir respecter la borne de révocation déclarée ou rester non admissible ; aucune invalidation instantanée universelle n'est promise.

Référence : [MIT Kerberos — database types](https://web.mit.edu/kerberos/krb5-latest/doc/admin/dbtypes.html), comme preuve que backend technique et référentiel Pixs sont deux choix distincts, sans sélection de MIT Kerberos.

## Dépendances

- [define-essential-autonomous-auth-module](../define-essential-autonomous-auth-module/proposal.md).
- [add-initial-authentication-and-sessions](../archive/2026-10-21-add-initial-authentication-and-sessions/proposal.md).
- [add-core-postgres-services](../archive/2026-10-20-add-core-postgres-services/proposal.md).
- [add-durable-minimized-audit](../archive/2026-10-21-add-durable-minimized-audit/proposal.md).

Les contrats de secrets, autorisation, audit, gouvernance, périmètre et reprise restent applicables. L'exception Super Admin de authorization/initial-administration s'applique dans son seul périmètre aux contrôles runtime ; elle ne crée ni preuve cryptographique ni conformité de protocole absente.

## Arbitrages avant réalisation

Produit/version, backend, topologie et HA éventuelle, realms et SPN, profils cryptographiques/préauthentification, temps fiable, durées et renouvellements, protection/rotation des keytabs et clés maîtresses, réplication, reprise et clients qualifiés.

Les choix de produits non arrêtés et dépendances supplémentaires exigent la revue applicable avant code. Aucun paramètre numérique arbitraire n'est réputé adopté.

## Migration et retour

Réutiliser les UUID et contrats existants. Définir migrations, reprise idempotente, état incomplet, plan d'arrêt/retrait et impacts sur sessions/clients avant réalisation. Aucun renommage, suppression, réinitialisation de base ou mouvement de fichier dans cette préparation. Le retour ne doit pas réadmettre un justificatif révoqué ou restaurer implicitement une confiance.

## Recette future

- Qualifier KDC seul puis avec OpenLDAP si ce backend est sélectionné, sans source externe installée.
- Tester temps invalide, realm non approuvé, keytab expirée, retrait, ticket encore valide et restauration.

Relier les scénarios du delta à l'artefact et aux versions effectivement qualifiés. Les mocks et contrôles documentaires ne prouvent pas la disponibilité de la capacité.

## Statut des deltas antérieurs après contrôle E3

Les anciens fichiers sous specs/ ont été déplacés, avec empreintes conservées, vers [l’historique interne](historique-deltas-avant-e3/README.md). Le [contrôle de couverture](COUVERTURE_DELTAS_E3.md) relie chaque ancienne exigence au contrat courant et aux tâches ouvertes. Le dossier reste actif ; skip_specs évite seulement la réapplication des anciennes prescriptions. Il ne termine ni la réalisation, ni les tests, ni les 49 tâches encore ouvertes dans les sept dossiers concernés.
