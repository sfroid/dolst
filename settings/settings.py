'''
Application and view settings

- sfroid (c)
'''

VIEW_SETTINGS = {
    'categories_visible': True,
    'categories_width': 100,
    'lists_visible': True,
    'lists_width': 100,
}

APP_SETTINGS = {
    'title': "Dolst"
}

TEST_SETTINGS = {
    'file_check_delay': 10,
}


def get_setting(self_module, group, attr=None, default=None):
    """
    Reload the settings module and return the latest setting
    referred by group and attr.

    If attr is not present, return default.
    """
    reload(self_module)
    try:
        if attr is None:
            return getattr(self_module, group, default)
        return getattr(self_module, group).get(attr, default)
    except BaseException:
        return default
