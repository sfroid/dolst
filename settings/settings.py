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
    curr_module = sys.modules[__name__]
    reload(curr_module)
    try:
        if attr is None:
            return getattr(curr_module, group, default)
        return getattr(curr_module, group).get(attr, default)
    except BaseException:
        return default
