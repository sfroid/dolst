"""
Editable text panel

    { sfroid : 2014 }

"""

import wx
from experiments.platform_tools import get_editable_text_pos, get_editor_ctrl_pos
from experiments.wx_utils import shifted_and_expanded, get_insertion_pos

class EditableText(wx.Panel):
    """
    A text field that allows inline editing when the user click on it.
    """
    def __init__(self, parent, text):
        wx.Panel.__init__(self, parent)

        self.text = text
        self.escape_pressed = False
        self.editing_text = False
        self.end_edit_callbacks = []
        self.tab_pressed_callbacks = []
        self.del_in_empty_callbacks = []
        self.last_cursor_position = None

        textpos = get_editable_text_pos()

        self.stext = wx.StaticText(self, -1, self.text)
        sizer = shifted_and_expanded(self.stext, textpos, wx.LEFT)

        self.stext.Bind(wx.EVT_LEFT_UP, self.cb_on_mouse_left_up)

        self.text_editor = wx.TextCtrl(self, -1, self.text, size=self.stext.GetSize())
        self.text_editor.Bind(wx.EVT_KEY_DOWN, self._on_key_down_in_edit)
        self.text_editor.Bind(wx.EVT_KILL_FOCUS, self.cb_on_editor_lost_focus)
        self.text_editor.Hide()

        self._default_text_props = self._get_default_text_props()

        self.SetSizer(sizer)
        self.Layout()


    def _get_default_text_props(self):
        """
        Return the default text properties as a dictionary
        """
        font = self.stext.GetFont()
        strikethrough = font.GetStrikethrough()

        text_colour = self.stext.GetForegroundColour()

        return {
            'strikethrough': strikethrough,
            'text_colour': text_colour,
        }


    def cb_on_mouse_left_up(self, event=None):
        """
        Handler for mouse click event
        """
        self.start_edit(mouse_pos=event.GetPositionTuple())


    def start_edit(self, mouse_pos=None, insertion_point=None):
        """
        This method hides the uneditable static text field and replaces
        it with an editable textctrl containing the same text
        as the hidden text field and sets focus on it.
        """
        self.escape_pressed = False

        size = self.stext.GetSize()
        size = (size[0], size[1] + 4)
        pos = self.stext.GetPositionTuple()

        xshift, yshift = get_editor_ctrl_pos()

        pos = (pos[0] + xshift, pos[1] + yshift)

        self.stext.Hide()
        self.text_editor.SetSize(size)
        self.text_editor.SetPosition(pos)
        self.text_editor.SetValue(self.text)

        self.text_editor.Show()
        self.text_editor.SetFocus()

        def set_insertion_point(editor, loc):
            """
            set the caret in the editor once it is made visible
            Without the callafter, the whole text gets selected.
            """
            if loc == -1:
                editor.SetInsertionPointEnd()
            else:
                editor.SetInsertionPoint(loc)

        if mouse_pos is not None:
            caret_location = get_insertion_pos(self, self.text, mouse_pos)
            wx.CallAfter(set_insertion_point, self.text_editor, caret_location)

        if insertion_point is not None:
            wx.CallAfter(set_insertion_point, self.text_editor, insertion_point)

        self.editing_text = True


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


    def _call_del_in_empty_callbacks(self, key):
        """
        Call the callbacks when del/backspace pressed on empty text
        """
        for callback, data in self.del_in_empty_callbacks:
            callback(data, key)


    def _on_key_down_in_edit(self, event):
        """
        Called when we are in edit mode and a key is pressed.
        Used for handling "Enter", "Esc" and the "Up" and "Down" keys.
        """
        key = event.GetKeyCode()
        #print "Keycode : %s" % key

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
                        self._call_del_in_empty_callbacks(key)

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

    def end_edit(self, save, reason):
        """
        Called to end editing
        """
        if self.editing_text is True:
            self._on_end_edit(save, reason)



    def _on_end_edit(self, save, reason):
        """
        Called when edit is done.
        The save argument determines whether the edit is to be
        saved or discarded. (e.g. discarded if esc was pressed)
        """
        if save:
            self.text = self.text_editor.GetValue()
            self.stext.Label = self.text

        self.last_cursor_position = self.text_editor.GetInsertionPoint()
        self.text_editor.Hide()
        self.stext.Show()
        self.editing_text = False

        self._call_end_edit_callbacks(reason)
        self.Layout()


    def set_text_properties(self, props):
        """
        Sets the properties of the test
        """
        if "strikethrough" in props:
            strk_through = props['strikethrough']

            font = self.stext.GetFont()
            font.SetStrikethrough(strk_through)
            self.stext.SetFont(font)

        if "text_colour" in props:
            # colour can be in #rrggbb(aa) aa optional
            text_colour = props['text_colour']
            self.stext.SetForegroundColour(text_colour)

    def reset_text_properties(self):
        """
        Reset text properties to the default values
        """
        props = self._default_text_props

        strikethrough = props['strikethrough']
        text_colour = props['text_colour']

        font = self.stext.GetFont()
        font.SetStrikethrough(strikethrough)
        self.stext.SetFont(font)

        self.stext.SetForegroundColour(text_colour)
        self.Update()
        self.Refresh()


    def close(self):
        """
        Gets ready to close this widget
        """
        self.end_edit_callbacks = []
        self._on_end_edit(False, None)
        self.DestroyChildren()
        self.Destroy()


    def pass_wheel_scrolls_to(self, callback):
        """
        Bind mouse wheel event to the callback
        """
        self.Bind(wx.EVT_MOUSEWHEEL, callback)
        self.stext.Bind(wx.EVT_MOUSEWHEEL, callback)
        self.text_editor.Bind(wx.EVT_MOUSEWHEEL, callback)


class DoubleClickEditor(EditableText):
    """
    Line editor for categories
    """
    def __init__(self, parent, text):
        EditableText.__init__(self, parent, text)

        self.selected = False
        self.selected_callbacks = []
        self.stext.Bind(wx.EVT_LEFT_DCLICK, self.cb_on_mouse_dblclick)
        self.SetBackgroundColour("#ffffff")


    def cb_on_mouse_dblclick(self, event):
        """
        Called on a mouse left double click
        """
        self.start_edit(mouse_pos=event.GetPositionTuple())


    def cb_on_mouse_left_up(self, event=None):
        """
        Override parent class method.
        Set current as selected.
        """
        if self.selected is False:
            self._call_selected_callbacks()


    def callback_on_selection(self, callback):
        """
        Set a callback to be called when an edit finishes.
        The callback is called with arguments
        callback(self, reason)
        """
        if callback not in self.selected_callbacks:
            self.selected_callbacks.append(callback)

    def _call_selected_callbacks(self):
        """
        Call the end edit callbacks with the reason.
        """
        for callback in self.selected_callbacks:
            callback(self)


    def set_selected(self):
        """
        Set selected style
        """
        self.selected = True
        self._set_background_color("focused")


    def clear_selected(self):
        """
        Clear selection style
        """
        self.selected = False
        self._set_background_color("blur")


    def _set_background_color(self, state):
        """
        Set background and foreground color for selected category
        """
        if state == "focused":
            self.SetBackgroundColour("#ddddff")
            self.SetForegroundColour("#000000")
            font = self.stext.GetFont()
            font.SetWeight(wx.FONTWEIGHT_BOLD)
        else:
            self.SetBackgroundColour("#ffffff")
            self.SetForegroundColour("#333333")
            font = self.stext.GetFont()
            font.SetWeight(wx.FONTWEIGHT_NORMAL)
        self.stext.SetFont(font)
        self.Layout()


def stop_editing_category_name(item):
    """
    Finish editing on edited window
    """
    if item.editing_text is True:
        item.end_edit(True, "lost_focus")
        print "finished editing"
