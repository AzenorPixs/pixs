"""Validateur lexical pur FrontendEntryPath v1 : syntaxe seule, sans effet.

Ne réalise aucun accès fichiers, résolution, enregistrement, composition,
chargement, activation, champ de manifest, routage, permission, normalisation,
décodage ni persistance. N’établit ni existence, ni confinement physique,
ni confiance du code.
"""


def validate_frontend_entry_path_v1(value: object) -> str:
    """Valide lexicalement une entrée FrontendEntryPath v1 et la retourne inchangée."""
    if not isinstance(value, str):
        raise TypeError("FrontendEntryPath v1 invalide")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("FrontendEntryPath v1 invalide") from exc
    if value == "":
        raise ValueError("FrontendEntryPath v1 invalide")
    if value.startswith("/"):
        raise ValueError("FrontendEntryPath v1 invalide")
    for segment in value.split("/"):
        if segment == "":
            raise ValueError("FrontendEntryPath v1 invalide")
        if segment == "." or segment == "..":
            raise ValueError("FrontendEntryPath v1 invalide")
        if "\\" in segment or ":" in segment or "?" in segment or "#" in segment or "%" in segment:
            raise ValueError("FrontendEntryPath v1 invalide")
        for char in segment:
            code = ord(char)
            if code < 0x20 or code == 0x7F:
                raise ValueError("FrontendEntryPath v1 invalide")
    return value


__all__ = ["validate_frontend_entry_path_v1"]
