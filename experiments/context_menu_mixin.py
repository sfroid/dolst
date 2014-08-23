"""
Context menus

"""

import wx

class ContextMenu(wx.EvtHandler):
    def __init__(self):
        self.Bind(wx.EVT_CONTEXT_MENU, self.on_context_menu)
        pass

    def on_context_menu(self, event):
        from experiments.editable_text import DoubleClickEditor
        from experiments.line_items_panel import LineItemsPanel
        from experiments.category_panel import CategoryListPanel
        from experiments.items_list_panel import ItemsListPanel

        if isinstance(self, DoubleClickEditor):
            self.show_itemlist_menu()
        if isinstance(self, LineItemsPanel):
            self.show_item_menu()
        if isinstance(self, CategoryListPanel):
            self.show_catpanel_menu()
        if isinstance(self, ItemsListPanel):
            self.show_item_panel_menu()

    def show_itemlist_menu(self):
        self.test_menu()
        pass

    def show_item_menu(self):
        self.test_menu()
        pass

    def show_catpanel_menu(self):
        self.test_menu()
        pass

    def show_item_panel_menu(self):
        self.test_menu()
        pass

    def test_menu(self):
        menu = wx.Menu()
        options = [("Choice One", self.on_choose_one),
                   ("Choice Two", self.on_choose_two)]

        for text, callback in options:
            item_id = wx.NewId()
            item = wx.MenuItem(menu, item_id, text)
            self.Bind(wx.EVT_MENU, callback, id=item_id)
            menu.AppendItem(item)

        self.PopupMenu(menu)
        menu.Destroy()

    def on_choose_one(self, event):
        print "chose one"

    def on_choose_two(self, event):
        print "chooose two"



