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
        cat_panel, items_panel = splitter.add_panels(CategoryListPanel, ItemsListPanel, 125, 50)

        self.category_panel = cat_panel
        self.items_panel = items_panel

        self.menubar = create_menu_bar(self)
        self.SetMenuBar(self.menubar)

    def update_category_view(self, data):
        """
        Updates/Redraws the category view with the given data
        """
        self.category_panel.update_data(data)


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
