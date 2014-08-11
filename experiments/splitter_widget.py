"""
Splitter panel to hold the categories and the task list
"""

import wx
import logging


class SplitterPane(wx.SplitterWindow):
    """
    Splitter panel - shows the category on the left and
    todo items on the right
    """
    def __init__(self, parent, ID):
        wx.SplitterWindow.__init__(self, parent, ID,
                                   style=wx.SP_LIVE_UPDATE)

        self.left_panel = None
        self.right_panel = None

        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.on_sash_changed)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.on_sash_changing)


    def add_panels(self, panel_class1, panel_class2, width, min_width):
        """
        Add the left and right panels
        """
        self.left_panel = panel_class1(self)
        self.left_panel.SetBackgroundColour("white")

        self.right_panel = panel_class2(self)
        self.right_panel.SetBackgroundColour("white")

        self.SetMinimumPaneSize(min_width)
        self.SplitVertically(self.left_panel, self.right_panel, width)

        return self.left_panel, self.right_panel


    def on_sash_changed(self, evt):
        """
        Called after sash position has changed
        """
        logging.info("sash changed to %s in %s\n", str(evt.GetSashPosition()), self)


    def on_sash_changing(self, evt):
        """
        Called while sash position is being dragged
        """
        logging.info("sash changing to %s in %s\n", str(evt.GetSashPosition()), self)
