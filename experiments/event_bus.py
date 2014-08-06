"""
Custom events used by the application

Events for category selection change or
data modification changes, etc go here.
"""

import wx
import wx.lib.newevent


CATEGORY_SEL_CHANGED, EVT_CAT_SEL_CHANGED = wx.lib.newevent.NewEvent()


class EventBus(wx.EvtHandler):
    """
    Singleton event bus class.
    This is used for throwing and catching common events
    usually by the controller

    NOTE: Do not instantiate this class directly.
          Use the get_event_bus method instead
    """
    singleton_event_bus = None


def get_event_bus():
    """
    Returns the singleton event bus
    Creates it too, if it does not exist yet.
    """
    # our singleton eventbus lives here
    if EventBus.singleton_event_bus is None:
        event_bus = EventBus()
        EventBus.singleton_event_bus = event_bus

    return EventBus.singleton_event_bus


def call_on_category_sel_event(callback):
    """
    Register a cb to be called when a
    category selection event occurs
    """
    eventbus = get_event_bus()
    eventbus.Bind(EVT_CAT_SEL_CHANGED, callback)


def notify_category_sel_event(item):
    """
    Announce that a category selection
    event has occured, to anyone that's listening
    """
    eventbus = get_event_bus()
    event = CATEGORY_SEL_CHANGED(item=item)
    wx.PostEvent(eventbus, event)


def test2():
    """
    test method 2 for the event bus
    """
    eventbus = get_event_bus()

    def cb_test3(event):
        """
        event callback function
        """
        print "Arrived in the event handler"

    # create an event
    print "creating and binding the event"
    some_new_event, evt_some_new_event = wx.lib.newevent.NewEvent()
    eventbus.Bind(evt_some_new_event, cb_test3)

    print "firing the event"
    evt = some_new_event(attr1="what's up")
    wx.PostEvent(eventbus, evt)



def test():
    """
    Mini test for get_event_bus and EventBus class
    """
    app = wx.App(False)
    frame = wx.Frame(None, -1, "hello")
    frame.CenterOnScreen()
    frame.Show(True)
    wx.CallAfter(test2)
    app.MainLoop()

    print "test completed"


if __name__ == "__main__":
    test()
