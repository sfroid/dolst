"""
Main controller class

Manages the view, data source, their
initialization and communication between them.
"""
import wx
from experiments.event_bus import call_on_category_sel_event
from experiments.top_frame import DolstTopFrame

class Controller(object):
    def __init__(self):
        self.view = self._init_view()
        self.model = self._init_data_model()

        wx.CallAfter(self._update_category_view, self._get_category_data())
        call_on_category_sel_event(self._on_category_selection)

    def _init_view(self):
        frame = DolstTopFrame("Todo list panel", (500, 500))
        frame.CenterOnScreen()
        frame.Show(True)
        return frame

    def _init_data_model(self):
        print "Intializing data model"
        pass

    def _get_category_data(self):
        return ["Category %s" % x for x in range(1, 8)]

    def _update_category_view(self, data):
        self.view.update_category_view(data)


    def _on_category_selection(self, event):
        print "received category selection event"
        cat_name = event.item.text
        self._update_items_view(self._get_items_data(cat_name))

    def _get_items_data(self, category_name):
        from random import randint
        return [self._dummy_get_item("%s: Item %s" % ( category_name, x )) for x in range(randint(0, 5), randint(6, 10))]

    def _update_items_view(self, data):
        # TODO : make this a call into self.view
        # rather than into view.items_panel
        self.view.items_panel.clear_and_add_items(data)
        pass

    def _update_category_data(self):
        pass

    def _update_items_data(self):
        pass

    def _dummy_get_item(self, text, depth=3):
        from random import randint
        idx = randint(10000, 20000)
        completed = (0 < randint(1, 10) < 6)
        if depth > 0:
            children = tuple([self._dummy_get_item("%s : Child %s" % (text, d), depth-1) for d in range(randint(0, 2))])
        else:
            children = []
        return (text, idx, completed, children)



def main():
    """
    Main entry point for the controller
    """
    app = wx.App(False)
    controller = Controller()
    app._view_top_frame = controller.view
    app.MainLoop()


if __name__ == "__main__":
    main()
