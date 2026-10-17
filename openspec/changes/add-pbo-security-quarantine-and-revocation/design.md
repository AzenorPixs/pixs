# Conception — N01

## Statut

Préparation du change dédié validée par le développeur le 17 octobre 2026. Aucune implémentation, migration ou opération sur un composant réel n’est autorisée.

## Responsabilités

C15 garde maintenance normale, diagnostic et observabilité. N01 possède la procédure d’urgence et la coordination de ses effets ; C03/C04 restent propriétaires des sessions, justificatifs et décisions d’accès. Les composants et providers appliquent leurs propres commandes publiques, sans écriture directe dans les données privées d’un autre propriétaire. O29 publie la révocation de versions dans un catalogue ; son absence ne doit pas empêcher la procédure PBO. PA07 demeure responsable de la quarantaine locale d’un PA sélectionné.

## Contrat de conception à préciser avant réalisation

Le plan d’incident doit relier une identité d’opération, acteur, périmètre canonique, cible/type, version ou génération attendue, motif minimisé, politique courante, idempotence et résultats. Ces champs décrivent un schéma de travail à revoir ; ils ne fixent pas une nouvelle API publique par la seule rédaction de cette conception.

La décision autoritative est persistante. Les admissions web, exécutions/reprises de jobs et activations concernées doivent consulter la décision courante. Une observation de santé, un drapeau client ou un ancien snapshot ne confère pas un droit de reprise.

## Séquence proposée

1. Authentifier et autoriser le demandeur ; vérifier contexte, version/génération et plan encore courant.
2. Persister la décision et son état d’opération avec l’audit applicable et une référence de corrélation.
3. Invoquer les contrats propriétaires ; réconcilier chaque résultat sans déduire un effet de son seul envoi ou acquittement.
4. Refuser les nouvelles admissions concernées ; qualifier les délais de propagation et traiter séparément les opérations déjà engagées selon leurs contrats.
5. Après panne, reprendre depuis les faits persistants, sans réactivation implicite ni annulation inventée d’un effet confirmé.
6. La sortie d’incident est une opération distincte, explicitement autorisée, avec nouvelles validations et résultat observé.

Les délais sont déclarés et mesurés par profil. Les objectifs temporels PZT ne deviennent pas des garanties universelles PBO. Si une cible ne peut plus être un exécutant de confiance, son résultat ne doit pas suffire seul à attester son assainissement.

## Cas de refus et de panne

Refuser demande hors périmètre, acteur non autorisé, version/génération obsolète, fait de sécurité invérifiable ou absence de persistance requise. Un provider optionnel isolé peut laisser le reste disponible ; une obligation de sécurité ou un composant essentiel invalide maintient la disponibilité concernée à faux. Un arrêt ou effet non observé reste inconnu, jamais annoncé terminé.

L’exception Super Admin est portée par son identité authentifiée et ses tenants explicitement accordés. Elle ne produit pas un audit, une signature, une mesure ou une action qui n’a pas eu lieu, et ne se transfère pas à un worker.

## Points de conception à valider avant code

Schéma/version des commandes, stockage propriétaire, identités des cibles, garanties de transaction avec l’audit, protocoles de propagation et preuve de secours. Aucun nouvel état public de lifecycle, logiciel de détection ou privilège hôte n’est choisi implicitement.

## Recette future

Acteur ordinaire refusé ; tenant non accordé ; replay idempotent ; incident concurrent/obsolète ; provider obligatoire ou optionnel ; réconciliation après perte de réponse et crash ; blocage des admissions et reprises ; absence de fausse readiness ; réactivation autorisée et preuve de non-transfert du privilège.

Les primitives pures et les tests unitaires existants ne remplacent pas ces recettes runtime. Les dépendances de contrat sont C03/C04/C05/C07/C09/C15 ; l’artefact C18 puis C17 doivent porter les preuves correspondantes.
