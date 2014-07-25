import wx
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class EditableText(wx.Panel):
    def __init__(self, parent, text, width=-1):
        wx.Panel.__init__(self, parent, size=(width, -1))

        self.text = text
        self.escapePressed = False
        self.width = width

        textpos = (0, 0)

        self.stext = wx.StaticText(self, -1, text, pos=textpos, size=(width, -1))
        self.setStaticTextSize()
        self.stext.Bind(wx.EVT_LEFT_UP, self.onLeftDown)

        self.editText = wx.TextCtrl(self, -1, size=self.stext.GetSize())
        self.editText.Bind(wx.EVT_KEY_DOWN, self.onKeyDownInEdit)
        self.editText.Bind(wx.EVT_KILL_FOCUS, self.onEditLostFocus)
        self.editText.Hide()

    def onLeftDown(self, event=None):
        self.startEdit()

    def onGainFocus(self, event=None):
        self.onLeftDown()

    def startEdit(self):
        self.escapePressed = False
        self.stext.Hide()

        size = self.stext.GetSize()
        pos = self.stext.GetPositionTuple()
        self.editText.SetSize(size)
        self.editText.SetPosition(pos)
        self.editText.SetValue(self.text)

        self.editText.Show()
        self.editText.SetFocus()

    def setStaticTextSize(self):
        size = self.stext.GetSize()
        size = (self.width, size[1] + 2)
        self.stext.SetSize(size)

    def onKeyDownInEdit(self, event):
        key = event.GetKeyCode()
        print key

        if key == wx.WXK_RETURN:
            if not (event.controlDown or
                    event.altDown or
                    event.shiftDown or
                    event.metaDown):
                self.onEndEdit(True)
                self.Parent.onMoveFocusDownOnEnter()
                return

        if key == wx.WXK_ESCAPE:
            self.escapePressed = True
            self.onEndEdit(False)
            return

        if key in (wx.WXK_UP, wx.WXK_DOWN):
            self.onEndEdit(False)
            self.Parent.onMoveFocusUpDown(1 if key == wx.WXK_UP else 0)
            return

        event.Skip()

    def onEditLostFocus(self, event):
        if self.escapePressed is True:
            self.onEndEdit(False)
            return
        self.onEndEdit(True)

    def onEndEdit(self, save):
        if save:
            self.text = self.editText.GetValue()
            self.stext.Label = self.text
            self.setStaticTextSize()

        self.editText.Hide()
        self.stext.Show()


class MyLinePanel(wx.Panel):
    def __init__(self, parent, text, width=-1):
        wx.Panel.__init__(self, parent, size=(width, -1))
        self.text = text
        border = 0

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.chkbox = wx.CheckBox(self, -1)
        self.chkbox.Bind(wx.EVT_CHECKBOX, self.onToggleCheckbox)
        sizer.Add(self.chkbox, 0)
        self.textEditor = EditableText(self, text, width - 2*border)
        sizer.Add(self.textEditor, 1, wx.EXPAND|wx.ALL, 0)
        self.SetSizer(sizer)
        self.Layout()
        sizer.Fit(self)
        print self.__class__, self.GetSize()

    def onToggleCheckbox(self, event):
        print "checkbox value: %s"%self.chkbox.GetValue()

    def onMoveFocusUpDown(self, direction):
        self.Parent.onMoveFocusUpDown(direction, self)

    def onMoveFocusDownOnEnter(self):
        self.Parent.onMoveFocusDownOnEnter(self)

    def setFocus(self):
        self.textEditor.onGainFocus("dummy")


class MyPanel(wx.Panel):
    def __init__(self, parent, width):
        wx.Panel.__init__(self, parent, -1, size=(width, -1))
        self.border = 1
        self.width = width
        self.textPanels = []

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = sizer

        for x in range(10):
            text = "Item %s"%(x+1)
            textPanel = MyLinePanel(self, text, width - 2*self.border)
            sizer.Add(textPanel, 0, wx.EXPAND|wx.ALL, self.border)
            self.textPanels.append(textPanel)

        self.SetSizer(sizer)
        self.Layout()
        sizer.Fit(self)

    def getTextPanelPos(self, tpanel):
        for i, tp in enumerate(self.textPanels):
            if tp == tpanel:
                return i

        return None

    def onMoveFocusUpDown(self, direction, textPanel):
        pos = self.getTextPanelPos(textPanel)
        if pos is None:
            logging.error("Could no find position for testPanel: %s", textPanel)

        if direction == 1:
            # UP
            if pos > 0:
                self.textPanels[pos-1].setFocus()
            else:
                self.textPanels[-1].setFocus()
        else:
            if pos < (len(self.textPanels) - 1):
                self.textPanels[pos+1].setFocus()
            else:
                self.textPanels[0].setFocus()

    def onMoveFocusDownOnEnter(self, textPanel):
        pos = self.getTextPanelPos(textPanel)
        textPanel = MyLinePanel(self, "", self.width - 2*self.border)

        if pos == len(self.textPanels) - 1:
            self.sizer.Add(textPanel, 0, wx.EXPAND|wx.ALL, self.border)
            self.textPanels.append(textPanel)
        else:
            self.sizer.Insert(pos+1, textPanel, 0, wx.EXPAND|wx.ALL, self.border)
            self.textPanels.insert(pos+1, textPanel)

        self.sizer.Layout()
        textPanel.setFocus()






class MyFrame(wx.Frame):
    def __init__(self, title, size):
        wx.Frame.__init__(self, None, -1, title=title, size=size)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        width, ignore = self.GetClientSizeTuple()
        sizer.Add(MyPanel(self, width), 0, wx.EXPAND, 1)

        print self.__class__, self.GetSize()


if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame("Todo list panel", (500, 500))
    frame.CenterOnScreen()
    frame.Show()
    app.MainLoop()

