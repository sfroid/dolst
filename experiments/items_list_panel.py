"""
Items List Panel

    { sfroid : 2014 }

"""

import wx
import logging
from experiments.line_items_panel import LineItemsPanel


class ItemsListPanel(wx.Panel):
    """
    Panel to hold a list of line item panels.
    It also supports drag and drop of items.
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.border = 1
        self.padding = 5
        self.line_item_panels = []

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.sizer.Add((0, self.padding))

        self.SetSizer(sizer)
        self.Layout()
        sizer.Fit(self)


    def _on_end_line_item_textedit(self, item, reason):
        """
        Callback when editing finishes on an item.
        """
        if reason in ("key_up", "key_down"):
            self._on_move_focus_updown(item, (1 if reason == "key_up" else 0))

        if reason == "key_return":
            self._on_move_focus_down_on_enter(item)


    def _on_move_focus_updown(self, line_item_panel, direction):
        """
        Move focus to next items (either up or down)
        """
        try:
            pos = self.line_item_panels.index(line_item_panel)
        except ValueError:
            logging.error("Could no find position for line panel: %s",
                          line_item_panel)
            return

        if direction == 1:
            # UP
            if pos > 0:
                self._set_focus_on_item_for_edit(pos - 1)
            else:
                self._set_focus_on_item_for_edit(len(self.line_item_panels) - 1)
        else:
            if pos < (len(self.line_item_panels) - 1):
                self._set_focus_on_item_for_edit(pos + 1)
            else:
                self._set_focus_on_item_for_edit(0)


    def _on_move_focus_down_on_enter(self, line_item_panel):
        """
        when enter pressed while editing, add new item
        """
        try:
            pos = self.line_item_panels.index(line_item_panel)
        except ValueError:
            logging.error("Could no find position for line panel: %s",
                          line_item_panel)
            return

        print "inserting new item in pos : %s" % pos
        self._insert_new_item(pos, line_item_panel.parent_item, line_item_panel)
        self._set_focus_on_item_for_edit(pos + 1)


    def create_line(self, parent_item, previous_item, data):
        """
        Create a line_item, bind callbacks, and return item
        """
        line_item = LineItemsPanel(self, parent_item, previous_item, data)
        line_item.callback_on_end_textedit(self._on_end_line_item_textedit)
        line_item.callback_on_del_in_empty(self._on_del_empty_line)
        return line_item


    def _on_del_empty_line(self, item):
        """
        Remove the item when del/backspace is pressed in an empty line
        """
        # remove item from sizer and destroy it
        pos = self.line_item_panels.index(item)
        self.line_item_panels.pop(pos)
        self.sizer.Remove(pos)
        self.Layout()

        wx.CallAfter(self.RemoveChild, item)
        wx.CallAfter(item.close)

        self._set_focus_on_item_for_edit(pos - 1)


    def _insert_new_item(self, pos, parent_item, previous_item):
        """
        Insert new line item at pos (or at end if pos at end)
        Also sets focus at that item.
        """

        line_item_panel = self.create_line(parent_item, previous_item,
                                           ("", 23423, False, parent_item.level))

        if pos == len(self.line_item_panels) - 1:
            self.sizer.Add(line_item_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, self.border)
            self.line_item_panels.append(line_item_panel)
        else:
            self.sizer.Insert(pos + 1, line_item_panel, 0,
                              wx.EXPAND | wx.LEFT | wx.RIGHT, self.border)
            self.line_item_panels.insert(pos + 1, line_item_panel)

        self.Layout()


    def _set_focus_on_item_for_edit(self, pos):
        """
        Sets focus on a particular item and starts editing text
        """
        if len(self.line_item_panels) > 0:
            pos = pos % len(self.line_item_panels)
            item = self.line_item_panels[pos]
            item.set_focus_and_startedit()


    def clear_and_add_items(self, data):
        """
        clears all the items and adds
        items from data
        """
        self.clear_all()

        parent = None
        previous = None
        level = 0
        self.add_items(data, parent, previous, level)
        self.Layout()


    def add_items(self, data, parent, previous, level):
        """
        Recursive method to add a bunch of items in data provided as
        a tuple of tuples.
        """
        for dt in data:
            text, idx, comp, children = dt
            previous = item = self.create_and_add_item(parent, previous, (text, idx, comp, level))
            if len(children) > 0:
                previous = self.add_items(children, item, previous, level + 1)
        return previous


    def create_and_add_item(self, parent, previous, data):
        """
        Handles a single item
        """
        line_item = self.create_line(parent, previous, data)
        self.sizer.Add(line_item, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, self.border)
        self.line_item_panels.append(line_item)
        if parent is not None:
            parent.add_child(line_item)
        return line_item


    def clear_all(self):
        """
        Removes all the items form the panel
        """
        self.line_item_panels = []
        self.sizer.Clear(True)
