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

        self.menubar = create_menu_bar()
        self.SetMenuBar(self.menubar)

        self._setup_development_menu()

        self.item_list_panel.SetFocus()


    def cb_on_key_down(self, event):
        """
        handler for keypressess events
        """
        key = event.GetKeyCode()
        print "Got key %s" % key

        if self._secret_key_unlocked_state is False:
            if ((key == 70) and  # key f
                    event.controlDown and
                    event.altDown):
                self._secret_key_unlocked_state = True
        else:
            self._secret_key_unlocked_state = False
            if ((key == 83) and  # key j
                    event.controlDown and
                    event.altDown):
                # install the secret menu
                from experiments.main_menu import add_development_menu
                add_development_menu(self.menubar)

        event.Skip()


    def _setup_development_menu(self):
        """
        setup a method to enable the development menu
        """
        self._secret_key_unlocked_state = False


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
