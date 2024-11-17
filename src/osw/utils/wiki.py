from uuid import UUID

# Legacy imports:
from osw.model.static import get_full_title, get_namespace, get_title  # noqa: F401


def get_osw_id(uuid: UUID) -> str:
    """Generates a OSW-ID based on the given uuid by prefixing "OSW" and removing
    all '-' from the uuid-string. Duplicates OSW.get_osw_id() from src/sw/core/osw.py

    Parameters
    ----------
    uuid
        An UUID object, e.g., UUID("2ea5b605-c91f-4e5a-9559-3dff79fdd4a5")

    Returns
    -------
        OSW-ID string, e.g., OSW2ea5b605c91f4e5a95593dff79fdd4a5
    """
    return "OSW" + str(uuid).replace("-", "")


def get_uuid(osw_id) -> UUID:
    """Returns the uuid for a given OSW-ID. Duplicate of OSW.get_uuid() from src/sw/core/osw.py

    Parameters
    ----------
    osw_id
        OSW-ID string, e.g., OSW2ea5b605c91f4e5a95593dff79fdd4a5

    Returns
    -------
        uuid object, e.g., UUID("2ea5b605-c91f-4e5a-9559-3dff79fdd4a5")
    """
    return UUID(osw_id.replace("OSW", ""))


def namespace_from_full_title(full_title: str) -> str:
    """extracts the namespace from a full title (namespace:title)

    Parameters
    ----------
    full_title
        the full title to extract the namespace from

    Returns
    -------
        the namespace as a string
    """
    return full_title.replace(title_from_full_title(full_title), "").replace(":", "")


def title_from_full_title(full_title: str) -> str:
    """extracts the title from a full title (namespace:title)

    Parameters
    ----------
    full_title
        the full title to extract the title from

    Returns
    -------
        the title as a string
    """
    namespace = full_title.split(":")[0]
    return full_title.split(f"{namespace}:")[-1]


def is_empty(val):
    """checks if the given value is empty"""
    if val is None:
        return True
    elif isinstance(val, list) or isinstance(val, str) or isinstance(val, dict):
        return len(val) == 0
    return False
