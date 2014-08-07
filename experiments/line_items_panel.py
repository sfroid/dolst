"""
The Line panel which holds the editable text and other widgets.

    { sfroid : 2014 }

"""

import wx
import logging
from experiments.editable_text import EditableText
from experiments.linked_tree import DoublyLinkedLinearTree

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

        self.text, self.idx, self.complete = data
        self.end_edit_callbacks = []

        (self.text_editor, self.checkbox,
         self.checkbox_panel, self.sizer,
         self.spacer) = (None, )*5

        self.do_layout()


    def do_layout(self):
        """
        set the layout and background color
        """
        self.sizer = sizer = wx.BoxSizer(wx.HORIZONTAL)

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

        self.text_editor = EditableText(self, self.text)
        self.text_editor.callback_on_end_edit(self.cb_on_end_textedit)
        self.text_editor.callback_on_tab_pressed(self.cb_on_tab_pressed)
        sizer.Add(self.text_editor, 1, wx.EXPAND)

        self.spacer = self.sizer.Insert(0, (20 * self.level, 0))

        self.set_background_color("#ffffff")
        self.update_text_view()

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
                pos = parent_parent.get_child_pos(parent)

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

        self.update_text_view()

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
        level = self.adjust_level()
        self.sizer.Remove(0)
        self.sizer.Insert(0, (20 * level, 0))

        for child in self.get_children():
            child.adjust_indent_level()
        self.Layout()


    def __str__(self):
        return self.text


    def __repr__(self):
        return self.text
