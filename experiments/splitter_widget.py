"""
Splitter panel to hold the categories and the task list
"""

import wx
import logging


class SplitterPane(wx.SplitterWindow):
    def __init__(self, parent, ID):
        wx.SplitterWindow.__init__(self, parent, ID,
                                   style = wx.SP_LIVE_UPDATE)

        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSashChanged)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.OnSashChanging)


    def add_panels(self, panel_class1, panel_class2, min_width):
        sty = wx.BORDER_SUNKEN

        self.left_panel = panel_class1(self)
        self.left_panel.SetBackgroundColour("white")

        self.right_panel = panel_class2(self)
        self.right_panel.SetBackgroundColour("white")

        self.SetMinimumPaneSize(min_width)
        self.SplitVertically(self.left_panel, self.right_panel, min_width)

        return self.left_panel, self.right_panel


    def OnSashChanged(self, evt):
        logging.info("sash changed to %s\n" % str(evt.GetSashPosition()))


    def OnSashChanging(self, evt):
        logging.info("sash changing to %s\n" % str(evt.GetSashPosition()))
