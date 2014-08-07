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
    menubar.Append(menu2, "De&v menu")
    frame.Bind(wx.EVT_MENU, cb_open_inpection_tool, id=MenuIDs.id_inspection_tool)

    menu3 = wx.Menu()
    menu3.Append(MenuIDs.id_print_tree, "&dump tree", "Dump tree details")
    menubar.Append(menu3, "Dump Tree")
    frame.Bind(wx.EVT_MENU, cb_dump_tree, id=MenuIDs.id_print_tree)

    return menubar
