"""
Platform specific hacks
"""

from platform import system


PLATFORM = system()

PLATFORM_MAPPING = {
    "Windows": "win",
    "Darwin": "mac",
    "Linux": "linux",
}

PLATFORM = PLATFORM_MAPPING.get(PLATFORM, "win")


def get_editable_text_pos():
    """
    Returns the position of the static text
    in the editable text widget
    """
    if PLATFORM == "mac":
        return (4, 0)
    return (4, 3)


def get_editor_ctrl_pos():
    """
    Returns the position of the text editor
    windows in the editable text widget
    """
    if PLATFORM == "mac":
        return (-2, -3)
    return (-4, -3)
