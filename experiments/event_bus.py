"""
Custom events used by the application

Events for category selection change or
data modification changes, etc go here.
"""

import wx
from wx.lib.newevent import NewEvent
import logging


CATEGORY_SEL_CHANGED, EVT_CAT_SEL_CHANGED = NewEvent()
ITEM_EDITED_EVENT, EVT_ITEM_EDITED = NewEvent()
ITEM_MOVED_EVENT, EVT_ITEM_MOVED = NewEvent()
ITEM_ADDED_EVENT, EVT_ITEM_ADDED = NewEvent()
ITEM_DELETED_EVENT, EVT_ITEM_DELETED = NewEvent()

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


def bind_on_event(event, callback):
    """
    Register a cb to be called when an
    event occurs
    """
    eventbus = get_event_bus()
    eventbus.Bind(event, callback)


def notify_event(event, item):
    """
    Announce that an event has occured,
    to anyone that's listening to that event
    """
    eventbus = get_event_bus()
    evt = event(item=item)
    wx.PostEvent(eventbus, evt)


def unbind_event(event, callback):
    """ unbind from an event """
    eventbus = get_event_bus()
    eventbus.Unbind(event, handler=callback)


def test2():
    """
    test method 2 for the event bus
    """
    eventbus = get_event_bus()

    def cb_test3(event):
        """
        event callback function
        """
        logging.debug("Arrived in the event handler")

    # create an event
    logging.debug("creating and binding the event")
    some_new_event, evt_some_new_event = NewEvent()
    eventbus.Bind(evt_some_new_event, cb_test3)

    logging.debug("firing the event")
    evt = some_new_event(attr1="what's up")
    wx.PostEvent(eventbus, evt)



def test():
    """
    Mini test for get_event_bus and EventBus class
    """
    logging.getLogger().setLevel(logging.INFO)
    app = wx.App(False)
    frame = wx.Frame(None, -1, "hello")
    frame.CenterOnScreen()
    frame.Show(True)
    wx.CallAfter(test2)
    app.MainLoop()

    logging.debug("test completed")


if __name__ == "__main__":
    test()
