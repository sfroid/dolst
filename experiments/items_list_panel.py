"""
Items List Panel

    { sfroid : 2014 }

"""

import wx
import logging
from experiments.line_items_panel import LineItemsPanel


class ItemsListPanel(wx.Panel):
    """
    Panel to hold a list of lint item panels.
    It also supports drag and drop of items.
    """
    def __init__(self, parent, width):
        wx.Panel.__init__(self, parent, -1, size=(width, -1))
        self.border = 1
        self.width = width
        self.line_item_panels = []

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer

        for cdx1 in range(10):
            text = "Item %s" % (cdx1 + 1)
            line_item_panel = LineItemsPanel(self, text, width - 2 * self.border)
            line_item_panel.callback_on_end_textedit(self._on_end_line_item_textedit)
            sizer.Add(line_item_panel, 0, wx.EXPAND | wx.ALL, self.border)
            self.line_item_panels.append(line_item_panel)

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

        self._insert_new_item(pos)

    def _insert_new_item(self, pos):
        """
        Insert new line item at pos (or at end if pos at end)
        Also sets focus at that item.
        """

        line_item_panel = LineItemsPanel(self, "", self.width - 2 * self.border)

        if pos == len(self.line_item_panels) - 1:
            self.sizer.Add(line_item_panel, 0, wx.EXPAND | wx.ALL, self.border)
            self.line_item_panels.append(line_item_panel)
        else:
            self.sizer.Insert(pos + 1, line_item_panel, 0,
                              wx.EXPAND | wx.ALL, self.border)
            self.line_item_panels.insert(pos + 1, line_item_panel)

        self.sizer.Layout()

    def _set_focus_on_item_for_edit(self, pos):
        """
        Sets focus on a particular item and starts editing text
        """
        pos = pos % len(self.line_item_panels)
        item = self.line_item_panels[pos]
        item.set_focus_and_startedit()
