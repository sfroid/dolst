"""
Main menu for dolst app
"""

import wx
import wx.lib.inspection


class MenuIDs(object):
    """
    Container to hold menu ids
    for the menus
    """
    id_inspection_tool = 1001
    id_exit = 1002
    id_print_tree = 1003
    id_test_tree = 1004


def cb_open_inpection_tool(event):
    """
    Opens the wx inspected widget
    """
    wx.lib.inspection.InspectionTool().Show()


def cb_exit_application(event):
    """
    Obvious
    """
    app = wx.GetApp()
    app.Exit()


def cb_dump_tree(event):
    """
    Obvious
    """
    app = wx.GetApp()
    app.view_top_frame.items_panel.print_tree()


def cb_test_tree(event):
    """
    Obvious
    """
    app = wx.GetApp()
    app.view_top_frame.items_panel.test_tree()


def create_menu_bar(frame):
    """
    Creates the main menu bar
    """
    menubar = wx.MenuBar()

    menu1 = wx.Menu()
    menu1.Append(MenuIDs.id_exit, "&Exit", "Exit application")

    menubar.Append(menu1, "&File")
    frame.Bind(wx.EVT_MENU, cb_exit_application, id=MenuIDs.id_exit)


    menu2 = wx.Menu()
    menu2.Append(MenuIDs.id_inspection_tool, "&wx Inspection tool", "Open inspection tool")
    frame.Bind(wx.EVT_MENU, cb_open_inpection_tool, id=MenuIDs.id_inspection_tool)

    menu2.Append(MenuIDs.id_print_tree, "&dump tree", "Dump tree details")
    frame.Bind(wx.EVT_MENU, cb_dump_tree, id=MenuIDs.id_print_tree)

    menu2.Append(MenuIDs.id_test_tree, "&test tree", "Test tree structure")
    frame.Bind(wx.EVT_MENU, cb_test_tree, id=MenuIDs.id_test_tree)

    menubar.Append(menu2, "De&v menu")


    return menubar
