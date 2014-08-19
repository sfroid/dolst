"""
Main controller class

Manages the view, data source, their
initialization and communication between them.
"""
import wx
import logging
from experiments.event_bus import call_on_category_sel_event
from experiments.top_frame import DolstTopFrame

PERMISSION_MSG = """
Dolst needs to be associated with a google account to sync with google tasks.\n
Click OK to open a web browser to google and give permission to Dolst to manage tasks.
Click Cancel to exit Dolst.
"""


class Controller(object):
    """
    Main controller class for Dolst
    """
    def __init__(self):
        self.view = None
        self.model = None
        self._init_view()
        self._init_data_model()

        call_on_category_sel_event(self._on_category_selection)


    def _init_view(self):  # pylint: disable=no-self-use
        """
        Initialize the view
        """
        frame = DolstTopFrame("To-do list panel", (500, 500))
        frame.CenterOnScreen()
        frame.Show(True)
        self.view = frame


    def _init_data_model(self):  # pylint: disable=no-self-use
        """
        Initialize the data model
        """
        logging.info("Intializing data model")
        from experiments.data_manager import TasksDataManager

        self.model = TasksDataManager()
        wx.CallAfter(self.load_authorization)

    def load_authorization(self):
        if self.model.is_authenticated() is False:
            wx.CallAfter(self._get_authorization)
        else:
            self.done_initialize()

    def _get_authorization(self):
        dlg = wx.MessageDialog(self.view,
                               PERMISSION_MSG,
                               "Google tasks permission...",
                               wx.OK | wx.CANCEL | wx.OK_DEFAULT,
                               )
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            import thread
            thread.start_new_thread(self._open_browser_and_sign_on)

            dlg = wx.MessageDialog(self.view,
                                   "A browser window has been opened",
                                   "Browser opened...",
                                   wx.OK | wx.CANCEL | wx.OK_DEFAULT,
                                   )
            result = dlg.ShowModal()
            dlg.Destroy()
        else:
            self.exit_app()

    def _open_browser_and_sign_on(self):
        self.model.get_user_credentials()
        if self.model.is_authenticated() is True:
            self.done_initialize()
        else:
            self.authentication_failed()




    def done_initialize(self):
        wx.CallAfter(self._update_category_view, self._get_category_data())

    def authentication_failed(self):
        dlg = wx.MessageDialog(self.view,
                               "We failed to get permissions from google.",
                               "Authentication Failed...",
                               wx.OK | wx.CANCEL | wx.OK_DEFAULT,
                               )
        dlg.ShowModal()
        dlg.Destroy()
        self.exit_app()



    def _get_category_data(self):  # pylint: disable=no-self-use
        """
        Get list of categories from the data model
        """
        return self.model.get_task_lists()


    def _update_category_view(self, data):
        """
        Update the category panel with the list of categories
        """
        self.view.update_category_view(data)


    def _on_category_selection(self, event):
        """
        Called when selected category is changed.
        """
        logging.info("received category selection event")
        category_obj = event.item.obj
        self._update_items_view(self._get_items_data(category_obj))


    def _get_items_data(self, category_obj):
        """
        Get list of category items from the data model
        """
        return self.model.get_task_items(category_obj)


    def _update_items_view(self, data):
        """
        Update view item panel with list of items
        """
        self.view.clear_and_add_items(data)


    def _update_category_data(self):
        """
        Update category data in response to user edits
        """
        pass


    def _update_items_data(self):
        """
        Update items data in response to user edits
        """
        pass


    def _dummy_get_item(self, text, depth=2):
        """
        Recursive method which returns a tree of items
        """
        from random import randint
        idx = randint(10000, 20000)
        completed = (0 < randint(1, 10) < 6)
        if depth > 0:
            children = tuple([self._dummy_get_item("%s:%s" % (text, d), depth - 1)
                              for d in range(2)])
        else:
            children = []
        return (text, idx, completed, children)

    def exit_app(self):
        try:
            self.model.save_data(self.view.get_data())
        except:
            pass
        wx.Exit()


def main():
    """
    Main entry point for the controller
    """
    logging.getLogger().setLevel(logging.INFO)
    app = wx.App(False)
    controller = Controller()
    app.view_top_frame = controller.view
    app.MainLoop()


if __name__ == "__main__":
    main()
