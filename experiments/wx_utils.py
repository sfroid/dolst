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
    def destroy(parent, child):
        """ destory the child items """
        logging.info("dummy destroyed")
        parent.RemoveChild(child)

    wx.CallLater(500, destroy, parent, dummy_text)
    return idx2 + 1


def get_image_path(num):
    """ return image path """
    # TODO - change paths when refactoring
    fnames = {1: "minus_dark_grey14.png",
              2: "minus_black14.png",
              3: "minus_light_grey14.png",
              4: "plus_dark_grey14.png",
              5: "plus_black14.png",
              6: "plus_light_grey14.png", }

    name = fnames.get(num, "minus_dark_grey.png")

    return os.path.join(os.path.dirname(__file__), name)
