"""
Main menu for the dolst app.
"""

import wx


def on_key_press(event):
    """
    Called on a key press
    """
    keycode = event.GetKeyCode()
    print "got key %s" % keycode

def main():
    """
    app main entry point
    """
    app = wx.App()
    frame = wx.Frame(None, -1, "Hello")
    panel = wx.Panel(frame, -1)
    panel.Bind(wx.EVT_KEY_DOWN, on_key_press)
    frame.Show()
    app.MainLoop()


main()
