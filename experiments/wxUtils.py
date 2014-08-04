"""
Wx related UI utility functions go here
"""

import wx

def expanded(widget, flags=None, padding=0):
    """
    Encapsulation for an items that needs to take
    the maximum available space in the horizontal direction
    """
    sizer = wx.BoxSizer(wx.VERTICAL)
    if flags is None:
        sizer.Add(widget, 0, wx.EXPAND | wx.ALL, padding)
    else:
        sizer.Add(widget, 0, wx.EXPAND | flags, padding)
    return sizer


def shifted_and_expanded(widget, shift, flags=0):
    """
    Encapsulation for an items that needs to take
    the maximum available space in the horizontal direction
    """
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add((0, shift[1]), 0, wx.EXPAND)
    sizer.Add(widget, 0, wx.EXPAND | flags, shift[0])
    return sizer

def get_top_frame():
    """
    Returns the top level frame of the app
    """
    return wx.GetApp()._view_top_frame
