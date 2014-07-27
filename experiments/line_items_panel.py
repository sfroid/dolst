"""
The Line panel which holds the editable text and other widgets.

    { sfroid : 2014 }

"""

import wx
from experiments.editable_text import EditableText


class LineItemsPanel(wx.Panel):
    """
    A wx.Panel which holds a line of elements like
    dropdown arrow, checkbox, editable text, gear icon, etc.

    This can also be dragged, but drag drop is handled by the
    parent widget (another wx panel probably).
    """
    def __init__(self, parent, text, width=-1):
        wx.Panel.__init__(self, parent, size=(width, -1))
        self.text = text
        self.end_edit_callbacks = []

        border = 0

        self.sizer = sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.checkbox = wx.CheckBox(self, -1)
        self.checkbox.Bind(wx.EVT_CHECKBOX, self.cb_on_toggle_checkbox)
        sizer.Add(self.checkbox, 0)

        checkbox_width = self.checkbox.GetSize()[0]

        self.text_editor = EditableText(self, text, width - 2 * border - checkbox_width)
        self.text_editor.callback_on_end_edit(self.cb_on_end_textedit)
        self.text_editor.callback_on_tab_pressed(self.cb_on_tab_pressed)
        sizer.Add(self.text_editor, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(sizer)
        self.Layout()
        sizer.Fit(self)


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
        print "checkbox value: %s" % self.checkbox.GetValue()

        props = {"strikethrough": False}
        if self.checkbox.GetValue():
            props = {"strikethrough": True}
        self.text_editor.set_text_properties(props)


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


    def set_focus_and_startedit(self):
        """
        Sets focus on the editable text and stats editing.
        """
        self.text_editor.start_edit()


    def close(self):
        """
        Destroy line panel
        """
        self.text_editor.close()
        self.DestroyChildren()
        self.Destroy()