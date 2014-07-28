"""
Create a experimental panel which contains
- list of checkboxes
- text labels with checkboxes
- editable text
- drag drop, etc

    { sfroid : 2014 }

"""

import wx
from utilities.log_utils import set_logging_level_to_debug
from experiments.items_list_panel import ItemsListPanel
from experiments.main_menu import create_menu_bar

class DolstTopFrame(wx.Frame):
    """
    Top level window of our application.
    """
    def __init__(self, title, size):
        wx.Frame.__init__(self, None, -1, title=title, size=size)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        width, _ = self.GetClientSizeTuple()

        self.item_list_panel = ItemsListPanel(self, width)
        sizer.Add(self.item_list_panel, 0, wx.EXPAND, 1)

        self.menubar = create_menu_bar(self)
        self.SetMenuBar(self.menubar)


def main():
    """
    Main entry point for the app.
    """
    # import wx.lib.inspection
    app = wx.App(False)
    frame = DolstTopFrame("Todo list panel", (500, 500))
    frame.CenterOnScreen()
    frame.Show(True)
    # wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()


if __name__ == "__main__":
    set_logging_level_to_debug()
    main()
