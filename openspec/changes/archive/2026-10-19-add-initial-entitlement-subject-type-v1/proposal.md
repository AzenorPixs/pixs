# Vocabulaire initial du type de sujet d'entitlement

## Pourquoi

TECHNICAL.md §25.2 décrit les sujets INSTALLATION, PLATFORM, TENANT et SCOPE d'un entitlement. PROJECT.md §2.44 et le canon quotas-entitlements en fixent les limites. Aucune représentation Python dédiée n'existe. Ce vocabulaire doit rester distinct des sept portées de QuotaPolicy.

## Modifications proposées

Ajouter EntitlementSubjectType, une Enum passive à quatre valeurs exactes, un export explicite et des preuves unitaires et d'import en processus frais. Le profil ne résout aucun entitlement et ne donne aucun accès.

## Capacités

### Capacités nouvelles

Aucune.

### Capacités modifiées

- quotas-entitlements : profil structurel initial du type de sujet, sans modification des contrôles applicatifs existants.

## Impact

Trois nouveaux fichiers Python : src/pixs/kernel/entitlement_subject_type.py, tests/unit/test_entitlement_subject_type.py et tests/integration/test_entitlement_subject_type_integration.py. Aucune façade existante modifiée, aucune dépendance ajoutée. Aucun provider, quota, entitlement persistant, hiérarchie, permission, migration, API, frontend ou effet externe. O15 reste préparatoire et distinct.

README.md et PROJECT.md §34 sont actualisés dans le même change pour refléter les compteurs canoniques, l'inventaire et le ratio après archivage. Leurs preuves et passages historiques sont préservés ; ces compteurs ne qualifient pas le produit.
