
# Recette temps v2 — adopté documentaire T0, non exécutée

Statut : tous scénarios **NON EXÉCUTÉS**. Le contrat commun `pixs.time.evidence` version `2.0.0` est distinct du contrat privé Z12 `z12.time_intent/v2`, schéma `2.0.0`, avec 11 liaisons et 16 champs conservés. Réalisation, contrôles locaux, correction, retest et validation par unité T1, T2, T3 avant suivante ; T4 qualification intégrée et contrôle global final distinct. Les sources de tests sont incluses dans chaque unité future. Vocabulaire : `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, `MAY`.

| ID | Source future de test | Entrée | Oracle | Preuve native | Environnement |
|---|---|---|---|---|---|
| R-TIME-01 | `src/pixs/pzt_ca/native/_time_obs.pxi`, `src/pixs/pzt_ca/time_handle.pyx` | incertitude `U = 1000000000ns` acceptée et `U = 999999999ns` acceptée | `OBSERVED` | intervalle entier vérifié au point d'usage | qualification sur cibles réelles, environnement autorisé |
| R-TIME-02 | mêmes sources | incertitude `U = 1000000001ns` | `REFUSED`, sans prolongation | garde d'usage, aucun droit réarmé | mêmes conditions |
| R-TIME-03 | mêmes sources | âge réel `600000000000ns` accepté et `599999999999ns` accepté en `SYNCHRONISE` | `OBSERVED` si autres gardes vérifiées | âge réel jamais rajeuni, provenance vérifiée | mêmes conditions |
| R-TIME-04 | mêmes sources | âge `600000000001ns` en `SYNCHRONISE` | `REFUSED` | garde d'usage, sans grâce | mêmes conditions |
| R-TIME-05 | mêmes sources, `Z12TimeBudgetCtx` | acquisition `250000000ns` | `OBSERVED` | compteur et échéance globale `1s`, `2` acquisitions au plus | mêmes conditions |
| R-TIME-06 | mêmes sources | 2 acquisitions et global `1000000000ns` acceptables sous toutes autres gardes, acquisition `250000001ns`, troisième acquisition ou dépassement global refusés | `OBSERVED` si bornes exactes et autres gardes vérifiées, sinon `REFUSED` ou `IN_DOUBT`, sans réarmement | temps monotone conservé, parent prioritaire, suspension invalidant le bail | mêmes conditions |
| R-TIME-07 | mêmes sources | booléen, flottant, nul, inconnu, doublon, référence client non autoritaire | `REFUSED` de contrat | pont opérateur natif avant vues, revérification C | mêmes conditions |
| R-TIME-08 | mêmes sources, profil affine | `rho_den` nul, débordement `uint64`, plafond non normalisé, `max_elapsed_ns` nul | `REFUSED` | arithmétique vérifiée, arrondi vers le large, paires `int64` pleine plage sans époque en `int64` nanosecondes | mêmes conditions |
| R-TIME-09 | composition D17, politique protégée | profil périmé, révocation courante, source non authentifiée, âge rajeuni par lecture | `REFUSED` | provenance et continuité vérifiées, âge réel | mêmes conditions |
| R-TIME-10 | producteur local, report distant | seul report distant ou monotone étranger, `None` public, DTO, manieur forgé | diagnostic seul, sans bail, sans observation positive | corrélation et domaines qualifiés localement requis | mêmes conditions |
| R-TIME-11 | Core, Auth, Agent, PZT | intervalle couvrant changement `DENY` et `ALLOW`, `Clock.now` historique seul | refus ou relecture bornée, sans décision par point seul | gardes décisionnelles et métier conservées, `Clock.now` non preuve v2 | mêmes conditions |
| R-TIME-12 | `src/pixs/pzt_ca/native/_ceremony.pxi`, `src/pixs/pzt_ca/ceremony_handle.pyx` | 22 champs et enveloppe 4 conformes, domaines conservés | `OBSERVED` de cérémonie sans admission | clef D10 attendue distincte M1, ordre défi, mesure, signature, réception | mêmes conditions |
| R-TIME-13 | mêmes sources | nonce réutilisé, ordre inversé, type inconnu, concurrence, suspension, reboot, expiration | `REFUSED` avec invalidation avant usage | nonce à usage unique consommé avant usage, nettoyage privé | mêmes conditions |
| R-TIME-14 | profil `§18.3` | attente humaine dans budget du profil, budget cérémonie distinct de D11 | `OBSERVED` si bornes respectées, sinon `TIME_UNVERIFIABLE` | parent jamais prolongé | mêmes conditions |
| R-TIME-15 | futur `src/pixs/pzt_ca/native/_tls_time_window.pxi` | intervalle entier comparé aux dates réelles, source non qualifiée ou latence inconnue | `OBSERVED` si chaîne admissible, sinon `REFUSED` | dérive conservative, `nocerttimecheck` interdit, `U` supérieur à `1s` refusé | mêmes conditions |
| R-TIME-16 | source indépendante du domaine restaurable | instantané, restauration, retour incohérent | baux et modèle invalidés jusqu'à nouvelle preuve | ni identifiant d'amorçage ni paires d'horloges seuls, D9 distincte, D6 jamais rouvert, R01 `600s` non réarmé | mêmes conditions |
| R-TIME-17 | runtime, `pixs.agent`, PZT seul | fonction indépendante, service par horloge, catalogue et mandat de cible exacte, LXC sans horloge hôte | continuation selon contrats, sans prolongation | PBO et PA par PZT seulement | mêmes conditions |

Simulacres et montages ne qualifient rien de réel. Hors ligne âge supérieur à `600s` seulement avec modèle et provenance et continuité qualifiés, profil courant, acquisition actuelle et `U_usage` inférieur ou égal à `1s`, sinon `INVERIFIABLE` et refus des temporels. Invalidités de profil, provenance et continuité entraînent refus. D18 nonces, clef D10 et `TLS` réels inchangés.
