"""
Items List Panel

    { sfroid : 2014 }

"""

import wx
from wx.lib.scrolledpanel import ScrolledPanel
import logging
from experiments.line_items_panel import LineItemsPanel, DoublyLinkedLinearTree


class ItemsListPanel(ScrolledPanel):  # pylint: disable=too-many-ancestors
    """
    Panel to hold a list of line item panels.
    It also supports drag and drop of items.
    """
    def __init__(self, parent):
        ScrolledPanel.__init__(self, parent, -1)
        self.border = 1
        self.padding = 5
        self.line_item_panels = []
        self.head_item = DoublyLinkedLinearTree()

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.sizer.Add((0, self.padding))

        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()


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

        insertion_point = line_item_panel.text_editor.last_cursor_position

        if direction == 1:
            # Up
            if pos > 0:
                self._set_focus_on_item_for_edit(pos - 1, insertion_point)
            else:
                self._set_focus_on_item_for_edit(len(self.line_item_panels) - 1, insertion_point)
        else:
            # Down
            if pos < (len(self.line_item_panels) - 1):
                self._set_focus_on_item_for_edit(pos + 1, insertion_point)
            else:
                self._set_focus_on_item_for_edit(0, insertion_point)


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
        if line_item_panel.get_child_count() > 0:
            self._insert_new_item(pos, line_item_panel, line_item_panel)
        else:
            self._insert_new_item(pos, line_item_panel.get_parent(), line_item_panel)
        self._set_focus_on_item_for_edit(pos + 1)


    def create_line(self, parent_item, sibling, data):
        """
        Create a line_item, bind callbacks, and return item
        """
        line_item = LineItemsPanel(self, data)

        if parent_item == sibling:
            sibling = None

        if sibling is None:
            parent_item.insert_tree(line_item, 0)
        else:
            parent_item.insert_after(line_item, sibling)

        line_item.callback_on_end_textedit(self._on_end_line_item_textedit)
        line_item.callback_on_del_in_empty(self._on_del_empty_line)
        line_item.pass_wheel_scrolls_to(self.cb_on_mouse_wheel_scroll)
        return line_item

    def cb_on_mouse_wheel_scroll(self, event):
        """
        called when mouse wheel is used on line items
        event.GetWheelRotation() returns Down : 120, Up: -120
        #TODO: replace 3, -3 with settings values
        """
        if event.GetWheelRotation() > 0:
            self.ScrollLines(-3)
        else:
            self.ScrollLines(3)


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

        self._set_focus_on_item_for_edit(pos - 1, -1)


    def _insert_new_item(self, pos, parent_item, previous_item):
        """
        Insert new line item at pos (or at end if pos at end)
        Also sets focus at that item.
        """

        level = 0
        if parent_item is not None:
            level = parent_item.level + 1

        line_item_panel = self.create_line(parent_item, previous_item,
                                           ("", 23423, False, level))

        if pos == len(self.line_item_panels) - 1:
            self.sizer.Add(line_item_panel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, self.border)
            self.line_item_panels.append(line_item_panel)
        else:
            self.sizer.Insert(pos + 1, line_item_panel, 0,
                              wx.EXPAND | wx.LEFT | wx.RIGHT, self.border)
            self.line_item_panels.insert(pos + 1, line_item_panel)

        self.SetAutoLayout(1)
        self.SetupScrolling()


    def _set_focus_on_item_for_edit(self, pos, insertion_point=None):
        """
        Sets focus on a particular item and starts editing text
        """
        if len(self.line_item_panels) > 0:
            pos = pos % len(self.line_item_panels)
            item = self.line_item_panels[pos]
            item.set_focus_and_startedit(insertion_point)


    def clear_and_add_items(self, data):
        """
        clears all the items and adds
        items from data
        """
        self.clear_all()

        parent = self.head_item
        sibling = self.head_item
        level = 0
        self.add_items(data, parent, sibling, level)

        self.SetAutoLayout(1)
        self.SetupScrolling()


    def add_items(self, data, parent, sibling, level):
        """
        Recursive method to add a bunch of items in data provided as
        a tuple of tuples.
        """
        for dt in data:
            text, idx, comp, children = dt
            sibling = item = self.create_and_add_item(parent, sibling, (text, idx, comp, level))
            if len(children) > 0:
                self.add_items(children, item, sibling, level + 1)


    def create_and_add_item(self, parent, sibling, data):
        """
        Handles a single item
        """
        line_item = self.create_line(parent, sibling, data)
        self.sizer.Add(line_item, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, self.border)
        self.line_item_panels.append(line_item)
        #if parent is not None:
            #parent.add_child(line_item)
        return line_item


    def clear_all(self):
        """
        Removes all the items form the panel
        """
        self.line_item_panels = []
        self.sizer.Clear(True)
