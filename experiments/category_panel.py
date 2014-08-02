"""
Items List Panel

    { sfroid : 2014 }

"""

import wx
import logging

class CategoryListPanel(wx.Panel):
    """
    Panel to hold a list of line item panels.
    It also supports drag and drop of items.
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.border = 5

        self.list_items_names = []

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer
        self.sizer.Add((0, self.border))
        self.SetSizer(sizer)
        self.Layout()
        sizer.Fit(self)

    def add_item(self, item):
        """
        Inserts a new item at while keeping the list sorted
        """
        new_list = self.list_items_names + [item]
        new_list.sort()
        self.list_items_names = new_list
        pos = new_list.index(item)
        item = EditableText(self, item)
        if pos == len(new_list) - 1:
            self.sizer.Add(item, flag=wx.LEFT | wx.RIGHT, border=self.border)
        else:
            self.sizer.Insert(pos + 1, item, flag=wx.LEFT | wx.RIGHT, border=self.border)

        self.Layout()
        self.Refresh()
