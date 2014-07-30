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
from experiments.category_panel import CategoryListPanel
from experiments.items_list_panel import ItemsListPanel
from experiments.main_menu import create_menu_bar

class DolstTopFrame(wx.Frame):
    """
    Top level window of our application.
    """
    def __init__(self, title, size):
        wx.Frame.__init__(self, None, -1, title=title, size=size)

        splitter = SplitterPane(self, -1)
        splitter.add_panels(CategoryListPanel, ItemsListPanel, 125)

        self.menubar = create_menu_bar(self)
        self.SetMenuBar(self.menubar)


def main():
    """
    Main entry point for the app.
    """
    app = wx.App(False)
    frame = DolstTopFrame("Todo list panel", (500, 500))
    frame.CenterOnScreen()
    frame.Show(True)
    app.MainLoop()


if __name__ == "__main__":
    set_logging_level_to_debug()
    main()
