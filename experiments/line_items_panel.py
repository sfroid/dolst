"""
The Line panel which holds the editable text and other widgets.

    { sfroid : 2014 }

"""

import wx
import logging
from experiments.editable_text import EditableText

class LineItemsPanel(wx.Panel):
    """
    A wx.Panel which holds a line of elements like
    dropdown arrow, checkbox, editable text, gear icon, etc.

    This can also be dragged, but drag drop is handled by the
    parent widget (another wx panel probably).
    """
    def __init__(self, parent, parent_item, previous_item, data):
        wx.Panel.__init__(self, parent)

        self.parent_item = parent_item
        self.previous_item = previous_item
        self.next_item = None

        self.text, self.idx, self.complete, self.level = data
        self.end_edit_callbacks = []
        self.child_items = []

        (self.text_editor, self.checkbox,
         self.checkbox_panel, self.sizer) = (None, )*4

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

        if self.level > 0:
            self.sizer.Insert(0, (20 * self.level, 0))

        self.set_background_color("#ffffff")
        self.update_text_view()

        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Layout()


    def set_next_item(self, next_item):
        """
        set the next item
        """
        self.next_item = next_item


    def set_previous_item(self, previous_item):
        """
        set the previous item
        """
        self.previous_item = previous_item


    def add_child(self, child):
        """
        append a child item to this item
        """
        self.child_items.append(child)


    def get_child_count(self):
        """
        returns the number of children
        """
        return len(self.child_items)


    def cb_on_tab_pressed(self, item, shift_pressed):
        """
        Evt handler - called when tab is pressed while editing text
        """
        # add a spacer when spacer added
        changed = False

        if shift_pressed is True:
            item0 = self.sizer.GetItem(0)
            if item0.IsSpacer():
                self.sizer.Remove(0)
                changed = True
        else:
            self.sizer.Insert(0, (15, 0))
            changed = True

        if changed is True:
            self.Layout()


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
