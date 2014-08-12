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
from experiments.splitter_widget import SplitterPane
from experiments.main_menu import create_menu_bar


def expanded(widget, padding=0):
    """
    Helper method to wrap a window in
    a vertical sizer so it takes maximum space
    available in the horizontal direction
    """
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(widget, 0, wx.EXPAND | wx.ALL, padding)
    return sizer


class DolstTopFrame(wx.Frame):
    """
    Top level window of our application.
    """
    def __init__(self, title, size):
        wx.Frame.__init__(self, None, -1, title=title, size=size)

        splitter = SplitterPane(self, -1)

        sty = wx.BORDER_SUNKEN

        p1 = wx.Panel(splitter, style=sty)
        p1.SetBackgroundColour("white")
        t1 = wx.StaticText(p1, -1, "Panel One")
        p1.SetSizer(expanded(t1))

        p2 = wx.Panel(splitter, style=sty)
        p2.SetBackgroundColour("sky blue")
        t2 = wx.StaticText(p2, -1, "Panel Two")
        p2.SetSizer(expanded(t2))

        splitter.SetMinimumPaneSize(20)
        splitter.SplitVertically(p1, p2, 150)

        self.menubar = create_menu_bar(self)
        self.SetMenuBar(self.menubar)


def main():
    """
    Main entry point for the app.
    """
    app = wx.App(False)
    frame = DolstTopFrame("To-do list panel", (500, 500))
    frame.CenterOnScreen()
    frame.Show(True)
    app.MainLoop()


if __name__ == "__main__":
    set_logging_level_to_debug()
    main()
