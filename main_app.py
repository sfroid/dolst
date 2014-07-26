"""
This is the file which you run when you want to run the Dolst application.
That's right... if you didn't guess it, this is the main dolst app.

Stop reading and run it.

Author: sfroid
"""

import wx


def main():
    """
    The main entry point of our application.

    Currently this does nothing, but it will. Wait for it.
    """
    app = wx.App()
    frame = wx.Frame(None, -1, "Hello there")
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
