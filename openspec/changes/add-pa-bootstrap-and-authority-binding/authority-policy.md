# Politique d'autorités proposée — admission et transfert

Statut proposé. Référence : [pixs-agent](../../specs/pixs-agent/spec.md). Complète [contracts.md](./contracts.md).

Décideur : PBO et Django avec autorité compétente. PA vérifie et exécute, sans arbitrage métier. Clé ressource et périmètre définies par profil propriétaire, pas déduites d'un chemin ni d'un ordre d'arrivée.

Admission vérifie propriétaire attendu, délégation, cible, action, version, validité et révocation courantes avec exclusion. Aucune compétence d'émetteur hors pouvoirs détenus. Incompatibles bloquées sans choix implicite. L'absence de double effet reste un objectif de test : contexte, propriétaire et idempotence persistés rapprochés à la reprise, avec preuve de fencing courante au point d'effet, ancien propriétaire réellement empêché avant réouverture, ni pause ni expiration valant révocation physique prouvée.

## Table de transfert

| Étape | Action |
|---|---|
| demande | sous autorité compétente avec preuves courantes |
| drainage | arrêt des nouvelles opérations chez l'ancien |
| réconciliation | effets vérifiés, issue inconnue conservée fermée |
| exclusion | fencing persistant de l'ancien |
| engagement | nouveau propriétaire avec preuves courantes |
| réouverture | seulement après engagement vérifié |

Échec, expiration ou issue inconnue conservent fermeture et protections, jamais droit révoqué restauré. Contrat de durabilité, propriétaire, profil, taille, temps et migration manquant bloque l'implémentation concernée, sans budget nouveau.

## Matrice de cas à prévoir, tous non exécutés

| Cas | Méthode | Résultat attendu |
|---|---|---|
| ancrage absent | démarrage sans ancrage | échanges bloqués, état explicite |
| ancrage substitué | comparaison aux racines installées | refus, état conservé |
| candidat forgé | validation origine | refus sans effet |
| approbation autre cible ou octets modifiés | comparaison liens exacts | refus |
| référence de secret non résoluble | résolution par provider existant | blocage sans exposition |
| expiration ou révocation périmée | recontrôle courant | refus |
| exposition vers autre relation | contrôle isolement | refus |
| restauration obsolète | comparaison version et preuves | blocage, pas de retour automatique |
| panne et timeout | réconciliation persistée | reprise sans double effet |
| réessai identité stable | vérification identité et autorisation | pas de duplication |
| deux autorités incompatibles | détection sans choix implicite | conflit déclaré, blocage |

Champs sémantiques non présentés comme schéma fermé exécutable final. Wire, profils et crypto à revoir avant code.


## Politique d'autorité v1 — borne du codec — addendum 2026-10-26

Cet addendum conserve la séquence d'autorité existante et précise la borne du codec, sans inventer une autre politique ni un nouvel état d'exécution.

Le codec pur valide la forme et restitue les octets canoniques. Il ne résout aucune référence, ne vérifie aucun secret, n'accorde aucune confiance et ne détecte pas sémantiquement un secret. Une chaîne opaque bien formée ne vaut ni autorisation ni preuve.

L'intégration exige des prérequis non livrés : vérificateur d'origine et d'autorisation avec racines, politique et révocation courantes, état persistant avec durabilité, barrière anti-rejeu et réconciliation, stratégie de corruption et de restauration, adapteurs de secrets, de transport et de stockage qualifiés par leurs propriétaires. Ces propriétaires, vérificateurs, stockages et garanties de durabilité restent des barrières d'intégration et ne sont pas remplacés par un succès de forme.

## Addendum RSMP séquence et inconnu — principes A ADOPTÉS, interface et qualification restantes
Choix A ADOPTÉ le 2026-10-26 ; B non retenu. Principes ADOPTÉS ; interface, code et qualification restant à réaliser. Séquence conservée demande drainage réconciliation exclusion engagement réouverture. États exactement non-provisionné en-cours prêt échoué. Inconnu diagnostic sous en-cours fermé avec verrous préservés, sans rejeu aveugle. Échec expiration issue inconnue conservent fermeture, jamais droit restauré. Ancrage absent ou substitué, candidat forgé, approbation autre cible, secret non résoluble sans exposition, expiration révocation périmée, exposition autre relation, restauration obsolète, deux autorités incompatibles : refusés ou bloqués. Prêt local borné ne prouve ni transport ni base ni admission. Preuve externe absente ferme seul acte concerné.
