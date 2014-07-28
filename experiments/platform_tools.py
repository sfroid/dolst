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
