"""
The Line panel which holds the editable text and other widgets.
"""

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

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.checkbox = wx.CheckBox(self, -1)
        self.checkbox.Bind(wx.EVT_CHECKBOX, self.on_toggle_checkbox)
        sizer.Add(self.checkbox, 0)
        self.text_editor = EditableText(self, text, width - 2 * border)
        self.textEditor.callback_on_end_edit(self.on_end_textedit)
        sizer.Add(self.text_editor, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(sizer)
        self.Layout()
        sizer.Fit(self)


    def on_toggle_checkbox(self, event):
        """
        Event handler that's called when the checkbox is clicked.
        """
        print "checkbox value: %s" % self.checkbox.GetValue()


    def callback_on_end_textedit(self, callback, reason=None):
        """
        Record a callback which will be called when an edit finishes.
        Optionally, specify a reason (or a tuple of reasons). The callback will
        be called only if the reason for ending the edit
        (enter, esc or up/down pressed) matches the given reason.
        """
        self.end_edit_callbacks.append((callback, reason))


    def on_end_textedit(self, reason):
        """
        Called when a child editable text finishes edition
        for any reason. Reason is also returned and can be

        key_up
        key_down
        key_enter
        key_escape
        lost_focus
        """
        for callback, rs in self.end_edit_callbacks:
            if isinstance(rs, tuple):
                if reason in rs:
                    callback(reason)
            elif rs == reason:
                callback(reason)
            elif rs is None:
                callback(reason)


    def set_focus_and_edit_test(self):
        self.text_editor.start_edit("dummy")


