"""Validateur lexical pur FrontendContributionId v1 : syntaxe seule, sans effet.

Ne réalise aucun accès fichiers, résolution, enregistrement, composition,
chargement, activation, champ de manifest, routage, permission, normalisation,
décodage, changement de casse ni persistance. N'établit ni propriété, ni
provenance, ni confiance, ni droit sur `pixs.*`, ni unicité.
"""


def validate_frontend_contribution_id_v1(value: object) -> str:
    """Valide lexicalement un identifiant et retourne sa valeur textuelle."""
    if not issubclass(type(value), str):
        raise TypeError("FrontendContributionId v1 invalide")
    segments = str.split(value, ".")
    if len(segments) < 2:
        raise ValueError("FrontendContributionId v1 invalide")
    for segment in segments:
        if len(segment) == 0:
            raise ValueError("FrontendContributionId v1 invalide")
        for index in range(len(segment)):
            code = ord(str.__getitem__(segment, index))
            if not (
                48 <= code <= 57
                or 65 <= code <= 90
                or 97 <= code <= 122
                or code == 45
                or code == 95
            ):
                raise ValueError("FrontendContributionId v1 invalide")
    return value


__all__ = ["validate_frontend_contribution_id_v1"]
