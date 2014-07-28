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
    return menubar
