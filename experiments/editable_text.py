"""
Editable text panel

    { sfroid : 2014 }

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
        self.tab_pressed_callbacks = []
        self.del_in_empty_callbacks = []

        textpos = (0, 0)

        self.stext = wx.StaticText(self, -1, text, pos=textpos, size=(width, -1))
        self._set_static_text_size()
        self.stext.Bind(wx.EVT_LEFT_UP, self.cb_on_mouse_left_up)

        self.text_editor = wx.TextCtrl(self, -1, text, size=self.stext.GetSize())
        self.text_editor.Bind(wx.EVT_KEY_DOWN, self._on_key_down_in_edit)
        self.text_editor.Bind(wx.EVT_KILL_FOCUS, self.cb_on_editor_lost_focus)
        self.text_editor.Hide()

        self.Layout()


    def _set_static_text_size(self):
        """
        The default text size / spacing is not aesthetic, so we give a
        bit of padding around the text.
        """
        size = self.stext.GetSize()
        size = (self.width, size[1] + 2)
        self.stext.SetSize(size)


    def cb_on_mouse_left_up(self, event=None):
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

        size = self.stext.GetSize()
        pos = self.stext.GetPositionTuple()
        pos = (pos[0] - 4, pos[1])

        self.stext.Hide()
        self.text_editor.SetSize(size)
        self.text_editor.SetPosition(pos)
        self.text_editor.SetValue(self.text)

        self.text_editor.Show()
        self.text_editor.SetFocus()
        self.Layout()


    def callback_on_end_edit(self, callback):
        """
        Set a callback to be called when an edit finishes.
        The callback is called with arguments
        callback(self, reason)
        """
        if callback not in self.end_edit_callbacks:
            self.end_edit_callbacks.append(callback)


    def callback_on_tab_pressed(self, callback):
        """
        Set a callback to be called when an tab is pressed
        """
        if callback not in self.tab_pressed_callbacks:
            self.tab_pressed_callbacks.append(callback)


    def callback_on_del_in_empty(self, callback, data):
        """
        Set a callback to be called when del/backspace is pressed
        when text editor is empty
        """
        if callback not in self.del_in_empty_callbacks:
            self.del_in_empty_callbacks.append((callback, data))


    def _call_end_edit_callbacks(self, reason):
        """
        Call the end edit callbacks with the reason.
        """
        for callback in self.end_edit_callbacks:
            callback(self, reason)


    def _call_del_in_empty_callbacks(self):
        """
        Call the callbacks when del/backspace pressed on empty text
        """
        for callback, data in self.del_in_empty_callbacks:
            callback(data)


    def _on_key_down_in_edit(self, event):
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
                self._on_end_edit(True, 'key_return')
                return

        if not (event.controlDown or
                event.altDown or
                event.metaDown):
            if key == wx.WXK_TAB:
                self._call_tab_pressed_callbacks(True if event.shiftDown else False)
                return

            if not event.shiftDown:
                if key in (wx.WXK_DELETE, wx.WXK_BACK):
                    curr_text = self.text_editor.GetValue()
                    if curr_text == "":
                        self._call_del_in_empty_callbacks()

                if key == wx.WXK_ESCAPE:
                    self.escape_pressed = True
                    self._on_end_edit(False, 'key_escape')
                    return

                if key in (wx.WXK_UP, wx.WXK_DOWN):
                    self._on_end_edit(False, ('key_up' if key == wx.WXK_UP else 'key_down'))
                    return

        event.Skip()


    def _call_tab_pressed_callbacks(self, shift_pressed):
        """
        Call tab pressed callbacks
        """
        for _cb in self.tab_pressed_callbacks:
            _cb(self, shift_pressed)


    def cb_on_editor_lost_focus(self, event):
        """
        Called when the editor loses focus for any reason
        while we are in edit mode.
        """
        # ignore focus lost event because of escape key
        if self.escape_pressed is True:
            self.escape_pressed = False
            return
        self._on_end_edit(True, 'lost_focus')


    def _on_end_edit(self, save, reason):
        """
        Called when edit is done.
        The save argument determines whether the edit is to be
        saved or discarded. (e.g. discarded if esc was pressed)
        """
        if save:
            self.text = self.text_editor.GetValue()
            self.stext.Label = self.text
            self._set_static_text_size()

        self.text_editor.Hide()
        self.stext.Show()

        self._call_end_edit_callbacks(reason)


    def set_text_properties(self, props):
        """
        Sets the properties of the test
        """
        if "strikethrough" in props:
            strk_through = props['strikethrough']

            font = self.stext.GetFont()
            font.SetStrikethrough(strk_through)
            self.stext.SetFont(font)

            font = self.text_editor.GetFont()
            font.SetStrikethrough(strk_through)
            self.text_editor.SetFont(font)


    def close(self):
        """
        Gets ready to close this widget
        """
        self.end_edit_callbacks = []
        self._on_end_edit(False, None)
        self.DestroyChildren()
        self.Destroy()
