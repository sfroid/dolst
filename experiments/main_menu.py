"""
Main menu for dolst app
"""

import wx


def create_menu_bar():
    """
    Creates the main menu bar
    """
    menubar = wx.MenuBar()

    menu1 = wx.Menu()
    menu1.Append(-1, "&Mercury", "Mercury in status bar")
    menu1.Append(-1, "&Venus", "Venus in status bar")
    menu1.Append(-1, "&Close", "Close this frame")

    menubar.Append(menu1, "&Planets")

    return menubar


def add_development_menu(menubar):
    """
    adds the development menu to the main menu
    """
    menu1 = wx.Menu()
    menu1.Append(-1, "&Mercury", "Mercury in status bar")
    menu1.Append(-1, "&Venus", "Venus in status bar")
    menu1.Append(-1, "&Close", "Close this frame")

    menubar.Append(menu1, "Dev menu")
