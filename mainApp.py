import wx


def main():
    app = MainApp()
    frame = app.createWindow()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
