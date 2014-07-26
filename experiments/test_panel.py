"""
Create a experimental panel which contains
- list of checkboxes
- text labels with checkboxes
- editable text
- drag drop, etc

- sfroid (c)
"""

import wx
import logging
from utilities.log_utils import init_logging
from experiments.editable_text import EditableText
from line_items_panel import LineItemsPanel

class MyPanel(wx.Panel):
    def __init__(self, parent, width):
        wx.Panel.__init__(self, parent, -1, size=(width, -1))
        self.border = 1
        self.width = width
        self.item_line_panels = []

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer

        for x in range(10):
            text = "Item %s" % (x + 1)
            item_line_panel = LineItemsPanel(self, text, width - 2 * self.border)
            sizer.Add(item_line_panel, 0, wx.EXPAND | wx.ALL, self.border)
            self.item_line_panels.append(item_line_panel)

        self.SetSizer(sizer)
        self.Layout()
        sizer.Fit(self)


    def getTextPanelPos(self, tpanel):
        for i, tp in enumerate(self.item_line_panels):
            if tp == tpanel:
                return i

        return None


    def on_move_focus_updown(self, direction, item_line_panel):
        pos = self.getTextPanelPos(item_line_panel)
        if pos is None:
            logging.error("Could no find position for line panel: %s",
                          item_line_panel)

        if direction == 1:
            # UP
            if pos > 0:
                self.item_line_panels[pos - 1].set_focus_and_edit_test()
            else:
                self.item_line_panels[-1].set_focus_and_edit_test()
        else:
            if pos < (len(self.item_line_panels) - 1):
                self.item_line_panels[pos + 1].set_focus_and_edit_test()
            else:
                self.item_line_panels[0].set_focus_and_edit_test()


    def on_move_focus_down_on_enter(self, item_line_panel):
        pos = self.getTextPanelPos(item_line_panel)
        item_line_panel = MyLinePanel(self, "", self.width - 2 * self.border)

        if pos == len(self.item_line_panels) - 1:
            self.sizer.Add(item_line_panel, 0, wx.EXPAND | wx.ALL, self.border)
            self.item_line_panels.append(item_line_panel)
        else:
            self.sizer.Insert(pos + 1, item_line_panel, 0,
                              wx.EXPAND | wx.ALL, self.border)
            self.item_line_panels.insert(pos + 1, item_line_panel)

        self.sizer.Layout()
        item_line_panel.set_focus_and_edit_test()


class MyFrame(wx.Frame):
    def __init__(self, title, size):
        wx.Frame.__init__(self, None, -1, title=title, size=size)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        width, ignore = self.GetClientSizeTuple()
        sizer.Add(MyPanel(self, width), 0, wx.EXPAND, 1)


if __name__ == "__main__":
    init_logging()

    app = wx.App()
    frame = MyFrame("Todo list panel", (500, 500))
    frame.CenterOnScreen()
    frame.Show()
    app.MainLoop()
