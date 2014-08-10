"""
Wx related UI utility functions go here
"""

import wx
import os
import logging

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
    return wx.GetApp().view_top_frame


def get_insertion_pos(parent, text, mouse_pos):
    """
    Find the character position for a given mouse position
    TODO: Improve this using binary search.
    """
    dummy_text = wx.TextCtrl(parent, -1, pos=(-2000, -2000))
    width, last_width, midpt = 0, 0, 0
    mouse_x = mouse_pos[0]
    idx2 = 0

    if len(text) == 0:
        return 0

    for idx2 in range(1, len(text)):
        width, dummy = dummy_text.GetTextExtent(text[:idx2])
        if width > mouse_x:
            midpt = (width + last_width) / 2.0
            if midpt > mouse_x:
                return idx2 - 1
            return idx2
        last_width = width
    def destroy_dummy(parent, child):
        logging.info("dummy destroyed")
        parent.RemoveChild(child)

    wx.CallLater(500, destroy_dummy, parent, dummy_text)
    return idx2 + 1


def get_image_path(num):
    # TODO - change paths when refactoring
    fnames = { 1: "arrow_right.png",
               2: "arrow_down.png",
               3: "arrow_down.png",}

    name = fnames.get(num, "arrow_down.png")

    return os.path.join(os.path.dirname(__file__), name)
