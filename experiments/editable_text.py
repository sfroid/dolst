"""
Editable text panel
"""

import wx


class EditableText(wx.Panel):
    """
    A text field that allows inline editing when the user click on it.
    """
    def __init__(self, parent, text, width=-1):
        wx.Panel.__init__(self, parent, size=(width, -1))

        self.text = text
        self.escape_pressed = False
        self.width = width
        self.end_edit_callbacks = []

        textpos = (0, 0)

        self.stext = wx.StaticText(self, -1, text,
                                   pos=textpos, size=(width, -1))
        self.set_static_text_size()
        self.stext.Bind(wx.EVT_LEFT_UP, self.on_mouse_left_up)

        self.edit_text = wx.TextCtrl(self, -1, size=self.stext.GetSize())
        self.edit_text.Bind(wx.EVT_KEY_DOWN, self.on_key_down_in_edit)
        self.edit_text.Bind(wx.EVT_KILL_FOCUS, self.on_editor_lost_focus)
        self.edit_text.Hide()


    def on_mouse_left_up(self, event=None):
        """
        Handler for mouse click event
        """
        self.start_edit()


    def start_edit(self):
        """
        This method hides the uneditable static text field and replaces
        it with an editable textctrl containing the same text
        as the hidden text field and sets focus on it.
        """
        self.escape_pressed = False
        self.stext.Hide()

        size = self.stext.GetSize()
        pos = self.stext.GetPositionTuple()
        self.edit_text.SetSize(size)
        self.edit_text.SetPosition(pos)
        self.edit_text.SetValue(self.text)

        self.edit_text.Show()
        self.edit_text.SetFocus()

    def callback_on_end_edit(self, callback):
        self.end_edit_callbacks.append(callback)


    def set_static_text_size(self):
        """
        The default text size / spacing is not aesthetic, so we give a
        bit of padding around the text.
        """
        size = self.stext.GetSize()
        size = (self.width, size[1] + 2)
        self.stext.SetSize(size)


    def on_key_down_in_edit(self, event):
        """
        Called when we are in edit mode and a key is pressed.
        Used for handling "Enter", "Esc" and the "Up" and "Down" keys.
        """
        key = event.GetKeyCode()
        print key

        if key == wx.WXK_RETURN:
            if not (event.controlDown or
                    event.altDown or
                    event.shiftDown or
                    event.metaDown):
                self.on_end_edit(True, 'key_return')
                return

        if key == wx.WXK_ESCAPE:
            self.escape_pressed = True
            self.on_end_edit(False, 'key_escape')
            return

        if key in (wx.WXK_UP, wx.WXK_DOWN):
            self.on_end_edit(False, ('key_up' if key == wx.WXK_UP else 'key_down'))
            return

        event.Skip()


    def on_editor_lost_focus(self, event):
        """
        Called when the editor loses focus for any reason
        while we are in edit mode.
        """
        # ignore focus lost event because of escape key
        if self.escape_pressed is True:
            self.escape_pressed = False
            return
        self.on_end_edit(True, 'lost_focus')


    def on_end_edit(self, save, reason):
        """
        Called when edit is done.
        The save argument determines whether the edit is to be
        saved or discarded. (e.g. discarded if esc was pressed)
        """
        if save:
            self.text = self.edit_text.GetValue()
            self.stext.Label = self.text
            self.set_static_text_size()

        self.edit_text.Hide()
        self.stext.Show()

        for callback in self.end_edit_callbacks:
            callback(reason)


