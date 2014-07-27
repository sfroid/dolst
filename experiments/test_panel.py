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


class DolstTopFrame(wx.Frame):
    """
    Top level window of our application.
    """
    def __init__(self, title, size):
        wx.Frame.__init__(self, None, -1, title=title, size=size)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        width, _ = self.GetClientSizeTuple()
        sizer.Add(ItemsListPanel(self, width), 0, wx.EXPAND, 1)


def main():
    """
    Main entry point for the app.
    """
    app = wx.App()
    frame = DolstTopFrame("Todo list panel", (500, 500))
    frame.CenterOnScreen()
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    set_logging_level_to_debug()
    main()
