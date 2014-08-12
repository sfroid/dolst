'''
Application and view settings

- sfroid (c)
'''

import sys

VIEW_SETTINGS = {
    'categories_visible': True,
    'categories_width': 100,
    'lists_visible': True,
    'lists_width': 100,
    'wheel_scroll_lines': 3,
    'background_color': "#ffffff",
}

APP_SETTINGS = {
    'title': "Dolst"
}

TEST_SETTINGS = {
    'file_check_delay': 10,
}


def get_setting(group, attr=None, default=None):
    """
    Reload the settings module and return the latest setting
    referred by group and attr.

    If attr is not present, return default.
    """
    if attr is None:
        return getattr(curr_module, group, default)
    return getattr(curr_module, group).get(attr, default)


def get_view_settings(attr, default=None):
    """ return the view setting """
    return VIEW_SETTINGS.get(attr, default)


def reload_settings():
    """ reload the settings """
    curr_module = sys.modules[__name__]
    reload(curr_module)
