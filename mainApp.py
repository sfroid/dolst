import wx
import logging

import settings
import utils
from wx.lib.splitter import MultiSplitterWindow


class SamplePane(wx.Panel):
    """
    Just a simple test window to put into the splitter.
    """
    def __init__(self, parent, colour, label):
        wx.Panel.__init__(self, parent, style=wx.BORDER_SUNKEN)
        self.SetBackgroundColour(colour)
        wx.StaticText(self, -1, label, (5, 5))

    def SetOtherLabel(self, label):
        wx.StaticText(self, -1, label, (5, 30))


class WindowFrame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, size=(400, 500))
        self.CreateStatusBar()
        self.createMenuBar()

        self.addChildPanels()
        self.CenterOnScreen()
        self.SetMinSize

    def createMenuBar(self):
        filemenu = wx.Menu()

        filemenu.Append(wx.ID_ABOUT, "&About",
                        "Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")

        menuBar = wx.MenuBar()
        # Adding the "filemenu" to the MenuBar
        menuBar.Append(filemenu, "&File")
        # Adding the MenuBar to the Frame content.
        self.SetMenuBar(menuBar)

    def addChildPanels(self):
        splitter = MultiSplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.splitter = splitter

        p1 = SamplePane(splitter, "pink", "Panel One")
        p1.SetOtherLabel(
            "There are two sash\n"
            "drag modes. Try\n"
            "dragging with and\n"
            "without the Shift\n"
            "key held down."
            )
        splitter.AppendWindow(p1, 140)

        p2 = SamplePane(splitter, "sky blue", "Panel Two")
        p2.SetOtherLabel("This window\nhas a\nminsize.")
        p2.SetMinSize(p2.GetBestSize())
        splitter.AppendWindow(p2, 150)

        p3 = SamplePane(splitter, "yellow", "Panel Three")
        p3.SetMinSize(p3.GetBestSize())
        splitter.AppendWindow(p3, 125)


class MainApp(wx.App):
    def __init__(self):
        wx.App.__init__(self)

    def createWindow(self):
        self.frame = WindowFrame(settings.app_settings.get('title', 'Dolst'))
        return self.frame


def main():
    utils.initLogging()

    app = MainApp()
    frame = app.createWindow()
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
