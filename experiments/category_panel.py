"""
Items List Panel

    { sfroid : 2014 }

"""

import wx
from wx.lib.scrolledpanel import ScrolledPanel
from experiments.editable_text import (DoubleClickEditor,
                                       stop_editing_category_name,
                                       TextObj)
from experiments.event_bus import notify_category_sel_event


class CategoryListPanel(ScrolledPanel):  # pylint: disable=too-many-ancestors
    """
    Panel to hold a list of line item panels.
    It also supports drag and drop of items.
    """
    def __init__(self, parent):
        ScrolledPanel.__init__(self, parent, -1)
        self.border = 5
        self.list_items_names = []
        self.current_selection = None

        self.Bind(wx.EVT_LEFT_UP, self.cb_on_left_up)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.sizer.Add((0, self.border))
        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()

    def cb_on_left_up(self, event):
        """
        Clear focus from the editor if its currently editing
        """
        if self.current_selection is not None:
            stop_editing_category_name(self.current_selection)


    def add_item(self, item):
        """
        Inserts a new item at while keeping the list sorted
        """
        new_list = self.list_items_names + [item]
        new_list.sort()
        self.list_items_names = new_list
        pos = new_list.index(item)
        item = DoubleClickEditor(self, TextObj(item.idx, item.get_text()))
        if pos == len(new_list) - 1:
            self.sizer.Add(item, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, border=self.border)
        else:
            self.sizer.Insert(pos + 1, item, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, border=self.border)

        item.callback_on_selection(self.cb_on_selection)

        self.SetAutoLayout(1)
        self.SetupScrolling()


    def cb_on_selection(self, item):
        """
        Called when a category is clicked on
        """
        old_selection = self.current_selection
        if old_selection is not None:
            # clear old selection / close editing if required
            old_selection.clear_selected()
            old_selection.end_edit(True, "lost_focus")

        self.current_selection = item
        item.set_selected()
        notify_category_sel_event(item)


    def add_items(self, data):
        """
        Convenience method to add multiple items at the same time
        """
        for dt in data:
            self.add_item(dt)


    def update_data(self, data):
        """
        Clear all itmes and add new ones.
        """
        # clear self
        self.sizer.Clear(True)
        self.list_items_names = []

        self.add_items(data)
