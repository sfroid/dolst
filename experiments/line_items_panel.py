"""
The Line panel which holds the editable text and other widgets.

    { sfroid : 2014 }

"""

import wx
import logging
from experiments.editable_text import EditableText, TextObj
from experiments.linked_tree import DoublyLinkedLinearTree
from experiments.wx_utils import get_image_path


class DropDownIcon(wx.Panel):
    """ + - icon for line items """
    image1 = None # minus dark grey
    image2 = None # minus black
    image3 = None # minus light
    image4 = None # plus dark
    image5 = None # plus black
    image6 = None # plus light
    image7 = None # minus lighter

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.expand_callback = None
        self.expanded = True
        self.current_image = None
        self.click_bound = False

        self.load_images()

        self.minus_dark = wx.StaticBitmap(self, -1, self.image1, pos=(0, 0))
        self.minus_black = wx.StaticBitmap(self, -1, self.image2, pos=(0, 0))
        self.minus_light = wx.StaticBitmap(self, -1, self.image3, pos=(0, 0))
        self.plus_dark = wx.StaticBitmap(self, -1, self.image4, pos=(0, 0))
        self.plus_black = wx.StaticBitmap(self, -1, self.image5, pos=(0, 0))
        self.plus_light = wx.StaticBitmap(self, -1, self.image6, pos=(0, 0))
        self.minus_lighter = wx.StaticBitmap(self, -1, self.image7, pos=(0, 0))

        for attr in ["minus_dark", "minus_black", "minus_light",
                     "plus_dark", "plus_black", "plus_light"]:
            image = getattr(self, attr)
            image.Bind(wx.EVT_LEFT_UP, self.cb_on_left_up)

        self.Bind(wx.EVT_LEFT_UP, self.cb_on_left_up)
        self.click_bound = True

        self.show_icon("minus_lighter", disable_click=True)


    def show_icon(self, attr, disable_click=False):
        """ hide all the show only one icon """
        image = getattr(self, attr, None)
        if (image is not None) and (image != self.current_image):
            self.current_image = image
            self.hide_all()
            image.Show()

            if disable_click is True:
                if self.click_bound is True:
                    self.Unbind(wx.EVT_LEFT_UP, handler=self.cb_on_left_up)
                    self.click_bound = False
            else:
                if self.click_bound is False:
                    self.Bind(wx.EVT_LEFT_UP, self.cb_on_left_up)
                    self.click_bound = True

            self.Refresh()


    def hide_all(self):
        """ hide all the icons """
        for attr in ["minus_dark", "minus_black", "minus_light", "minus_lighter",
                     "plus_dark", "plus_black", "plus_light"]:
            image = getattr(self, attr)
            image.Hide()


    def load_images(self):  # pylint: disable=no-self-use
        """ load the images """
        if DropDownIcon.image1 is None:
            for i in range(1, 8):
                attr = "image%s" % (i)
                image = wx.Image(get_image_path(i), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
                setattr(DropDownIcon, attr, image)


    def cb_on_left_up(self, event):
        """ on click, toggle betwen + / - """
        if self.expanded is True:
            self.expanded = False
            self.show_icon("plus_black")
        else:
            self.expanded = True
            self.show_icon("minus_light")

        if self.expand_callback is not None:
            self.expand_callback(self.expanded)

        self.Refresh()


    def set_callback_on_click(self, callback):
        """ line item can subscribe to toggle event """
        self.expand_callback = callback


class LineItemsPanel(wx.Panel, DoublyLinkedLinearTree):
    """
    A wx.Panel which holds a line of elements like
    dropdown arrow, checkbox, editable text, gear icon, etc.

    This can also be dragged, but drag drop is handled by the
    parent widget (another wx panel probably).
    """
    def __init__(self, parent, data):
        wx.Panel.__init__(self, parent)
        DoublyLinkedLinearTree.__init__(self)
        DoublyLinkedLinearTree.set_instance(self, self)
        self.expanded = True
        self.selected = False
        self.dd_icon = None

        self.text, self.idx, self.complete = data
        self.end_edit_callbacks = []
        self.callback_on_arrow_click = None

        (self.text_editor, self.checkbox,
         self.checkbox_panel, self.sizer,
         self.spacer) = (None, ) * 5

        self.do_layout()
        self.setup_highlighting()


    def do_layout(self):
        """
        set the layout and background color
        """
        self.sizer = sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.dd_icon = DropDownIcon(self)
        self.dd_icon.set_callback_on_click(self.cb_on_arrow_clicked)
        self.sizer.Add(self.dd_icon, 0, wx.CENTER, 5)

        if hasattr(LineItemsPanel, "checkbox_size"):
            size = LineItemsPanel.checkbox_size
        else:
            # hack to get rid of the empty checkbox label holder outline
            test_checkbox = wx.CheckBox(self, -1, pos=(-100, -100))
            size = test_checkbox.GetSize()
            LineItemsPanel.checkbox_size = size
            # Without the callafter, we get a crash on mac
            # Not unexpectedly, as we are not in the mainloop yet
            wx.CallAfter(self.RemoveChild, test_checkbox)

        new_size = (size[0] - 4, size[1])
        self.checkbox_panel = wx.Panel(self, -1, size=new_size)
        self.checkbox = wx.CheckBox(self.checkbox_panel, -1)
        self.checkbox.Bind(wx.EVT_CHECKBOX, self.cb_on_toggle_checkbox)
        self.checkbox.SetValue(self.complete)
        sizer.Add(self.checkbox_panel, 0)

        self.text_editor = EditableText(self, TextObj(self.idx, self.text))
        self.text_editor.callback_on_end_edit(self.cb_on_end_textedit)
        self.text_editor.callback_on_tab_pressed(self.cb_on_tab_pressed)
        sizer.Add(self.text_editor, 1, wx.EXPAND)

        self.spacer = self.sizer.Insert(0, (20 * self.level, 0))

        self.set_background_color("#ffffff")
        self.update_text_view()

        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)

        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()


    def cb_on_tab_pressed(self, item, shift_pressed):
        """
        Evt handler - called when tab is pressed while editing text
        """
        if shift_pressed is True:
            parent = self.get_parent_item()
            parent_parent = parent.get_parent_item()
            if parent_parent is not None:
                # make siblings after item, children of item
                siblings_after = parent.get_siblings_after_item(self)
                for sib in siblings_after:
                    parent.remove_child_tree(sib)
                    self.append_child_tree(sib)

                parent.remove_child_tree(self)
                parent_parent.insert_after(self, parent)
        else:
            sibling = self.get_prev_item_at_same_level()
            # do something only if same level sibling found
            # else, item is first child of parent, so do nothing
            if sibling is not None:
                self.remove_tree_from_parent()
                sibling.append_child_tree(self)

        self.adjust_indent_level()


    def cb_on_toggle_checkbox(self, event):
        """
        Event handler that's called when the checkbox is clicked.
        """
        # if checkbox is checked, show text in strikethrough
        logging.info("checkbox value: %s", self.checkbox.GetValue())

        value = self.checkbox.GetValue()
        self.set_child_checkboxes(value)
        if value is False:
            parent = self.get_parent_item()
            if hasattr(parent, "set_checked"):
                parent.set_checked(value)


    def set_child_checkboxes(self, value):
        """ if parent checkbox changes value, do same for children """
        self.checkbox.SetValue(value)
        for child in self.children:
            child.set_child_checkboxes(value)
        self.update_text_view()


    def set_cb_on_arrow_clicked(self, callback):
        """ method to subscribe to expand / contract """
        self.callback_on_arrow_click = callback


    def cb_on_arrow_clicked(self, expanded):
        """ callback on expand / contract """
        self.expanded = expanded
        if self.expanded is True:
            self.do_expansion()
        else:
            self.do_contraction()

        if self.callback_on_arrow_click is not None:
            self.callback_on_arrow_click(self, expanded)


    def do_expansion(self):
        """ expand this item """
        self.Show()
        if self.expanded:
            for child in self.children:
                child.do_expansion()


    def do_contraction(self):
        """ contract this item """
        for child in self.children:
            child.Hide()
            child.do_contraction()


    def update_text_view(self):
        """
        update the text properties based on the
        checkbox value
        """
        if self.checkbox.GetValue():
            props = {
                "strikethrough": True,
                "text_colour": "#aaaaaa",
            }

            self.text_editor.set_text_properties(props)
        else:
            self.text_editor.reset_text_properties()

        self.Layout()


    def callback_on_end_textedit(self, callback, reason=None):
        """
        Record a callback which will be called when an edit finishes.
        Optionally, specify a reason (or a tuple of reasons). The callback will
        be called only if the reason for ending the edit
        (enter, esc or up/down pressed) matches the given reason.
        """
        self.end_edit_callbacks.append((callback, reason))


    def callback_on_del_in_empty(self, callback):
        """
        Record a callback which will be called the del/backspace
        key is pressed in an empty text editor field.
        """
        self.text_editor.callback_on_del_in_empty(callback, self)


    def cb_on_end_textedit(self, editor, reason):
        """
        Called when a child editable text finishes edition
        for any reason. Reason is also returned and can be

        key_up
        key_down
        key_enter
        key_escape
        lost_focus
        """
        self.text = editor.text
        for callback, acc_rs in self.end_edit_callbacks:
            if isinstance(acc_rs, tuple):
                if reason in acc_rs:
                    callback(self, reason)
            elif acc_rs == reason:
                callback(self, reason)
            elif acc_rs is None:
                callback(self, reason)


    def set_focus_and_startedit(self, insertion_point):
        """
        Sets focus on the editable text and stats editing.
        """
        self.text_editor.start_edit(insertion_point=insertion_point)


    def close(self):
        """
        Destroy line panel
        """
        self.text_editor.close()
        self.DestroyChildren()
        self.Destroy()


    def set_background_color(self, color):
        """
        Set the background color for this panel
        """
        self.checkbox_panel.SetBackgroundColour(color)
        self.text_editor.SetBackgroundColour(color)
        self.SetBackgroundColour(color)


    def pass_wheel_scrolls_to(self, callback):
        """
        Bind mouse wheel event to the callback
        """
        self.Bind(wx.EVT_MOUSEWHEEL, callback)
        self.checkbox.Bind(wx.EVT_MOUSEWHEEL, callback)
        self.checkbox_panel.Bind(wx.EVT_MOUSEWHEEL, callback)
        self.text_editor.pass_wheel_scrolls_to(callback)


    def adjust_indent_level(self):
        """ set indent level based on parent's level """
        level = self.adjust_level()
        self.sizer.Remove(0)
        self.sizer.Insert(0, (20 * level, 0))

        for child in self.get_children():
            child.adjust_indent_level()
        self.Layout()


    def set_indent_level(self, level):
        """ set the indent level to argument """
        self.sizer.Remove(0)
        self.sizer.Insert(0, (20 * level, 0))


    def setup_dragging(self, drag_handler):
        """ set callbacks for dragging """
        def on_left_down(event):
            """ left down callback """
            drag_handler.cb_on_left_down(event, self)
        def on_mouse_move(event):
            """ mouse move callback """
            drag_handler.cb_on_mouse_move(event, self)
        def on_left_up(event):
            """ left up callback """
            dragging = drag_handler.cb_on_left_up(event, self)
            if dragging is False:
                self.on_left_up(event)

        # unbind existing method and bind new one.
        self.Unbind(wx.EVT_LEFT_UP, handler=self.on_left_up)

        self.Bind(wx.EVT_LEFT_DOWN, on_left_down)
        self.Bind(wx.EVT_MOTION, on_mouse_move)
        self.Bind(wx.EVT_LEFT_UP, on_left_up)

        cb_methods = (on_left_down, on_mouse_move, on_left_up)
        self.text_editor.setup_dragging(cb_methods)


    def insert_tree(self, item, pos):
        """ when inserting a child, if its unchecked, uncheck parent """
        super(LineItemsPanel, self).insert_tree(item, pos, update_icon=False)
        if not item.is_checked():
            self.set_checked(False)

        self.update_dd_icon()


    def append_child_tree(self, item, update_icon=True):
        """ when inserting a child, if its unchecked, uncheck parent """
        super(LineItemsPanel, self).append_child_tree(item, update_icon)
        if not item.is_checked():
            self.set_checked(False)

        if update_icon is True:
            self.update_dd_icon()


    def remove_child_tree(self, child):
        """ when removing child, if no children present, change dropdown icon """
        super(LineItemsPanel, self).remove_child_tree(child)
        self.update_dd_icon()


    def update_dd_icon(self):
        """ update the expand/contract icon """
        if self.get_child_count() > 0:
            if self.expanded is True:
                self.dd_icon.show_icon("minus_light")
            else:
                self.dd_icon.show_icon("plus_black")
        else:
            self.dd_icon.show_icon("minus_lighter", disable_click=True)


    def is_checked(self):
        """ return checkbox status """
        return self.checkbox.GetValue()

    def set_checked(self, val, propagate=True):
        """ set checkbox status """
        self.checkbox.SetValue(val)
        if propagate is True:
            if (self.parent_item is not None) and hasattr(self.parent_item, 'set_checked'):
                self.parent_item.set_checked(False)


    def on_left_up(self, event):
        """  start editing """
        if self.text_editor.editing_text is False:
            xpos = event.GetPosition()[0]
            expos = self.text_editor.GetPosition()[0]
            if xpos >= expos:
                if xpos <= expos + self.text_editor.GetSize()[0]:
                    self.text_editor.start_edit()


    def setup_highlighting(self):
        """ events for supporting highlighting on hover """
        self.Bind(wx.EVT_ENTER_WINDOW, self.cb_mouse_on_item)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.cb_mouse_left_item)


    def cb_mouse_on_item(self, event):
        """ highlight on hover """
        # TODO : replace magic numbers by settings
        self.SetBackgroundColour("#ffddaa")
        self.checkbox_panel.SetBackgroundColour("#ffddaa")
        self.text_editor.SetBackgroundColour("#ffddaa")
        self.dd_icon.SetBackgroundColour("#ffddaa")
        self.Refresh()

    def cb_mouse_left_item(self, event):
        """ remove highlight """
        # TODO : replace magic numbers by settings
        self.SetBackgroundColour("#ffffff")
        self.checkbox_panel.SetBackgroundColour("#ffffff")
        self.text_editor.SetBackgroundColour("#ffffff")
        self.dd_icon.SetBackgroundColour("#ffffff")
        self.Refresh()


    def __str__(self):
        """ string representation """
        return self.text


    def __repr__(self):
        """ string representation """
        return self.text
