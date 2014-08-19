"""
Main menu for the dolst app.
"""

import wx
import logging

frame = None

def on_key_press(event):
    """
    Called on a key press
    """
    keycode = event.GetKeyCode()

    dlg = wx.MessageDialog(frame,
                           'Dolst needs to be associated with a google' +
                           ' account to sync with google tasks.\n\n' +
                           'Click OK to open a web browser to google and' +
                           ' give permission to Dolst to manage tasks.\n' +
                           'Click Cancel to exit Dolst.',
                           'Google tasks permission...',
                           wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT,
                           )
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        print "yay... open browser"
    else:
        print "ok... goodbye"
    print result, wx.OK, wx.CANCEL, wx.ID_OK, wx.ID_CANCEL
    print type(result)
    dlg.Destroy()

    logging.info("got key %s", keycode)


def main():
    """
    app main entry point
    """
    global frame
    app = wx.App()
    frame = wx.Frame(None, -1, "Hello")
    panel = wx.Panel(frame, -1)
    panel.Bind(wx.EVT_KEY_DOWN, on_key_press)
    frame.Show()

    app.MainLoop()
    return


logging.getLogger().setLevel(logging.INFO)
main()
