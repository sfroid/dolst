"""
Drag and drop mixing class for Items List Panel

    { sfroid : 2014 }

"""

import wx
import logging

class DragDropMixin(object):
    """ Mixin for supporting drag and drop """
    def __init__(self):
        self.dragging = False
        self.left_down = False
        self.left_down_position = None
        self.dragged_data = {}
        self.x, self.y, self.dx, self.dy = 0, 0, 0, 0
        self.insertions_points = None
        self.old_insertion_point = None
        self.instance = None


    def set_instance(self, instance):
        """ set the instance this Drag Drop works on """
        from experiments.items_list_panel import ItemsListPanel
        self.instance = instance
        isinstance(self.instance, ItemsListPanel)


    def cb_on_left_down(self, event, item):
        """ called to note possible drag start position and item"""
        logging.debug("left down on item %s", str(item))
        self.left_down = True
        ipos = self.ScreenToClient(item.GetPositionTuple())
        mpos = self.ScreenToClient(wx.GetMousePosition())

        self.x, self.y = item.GetPositionTuple()
        self.dx, self.dy = (ipos[0] - mpos[0], ipos[1] - mpos[1])

        self.left_down_position = event.GetPositionTuple()
        event.Skip()


    def cb_on_mouse_move(self, event, item):
        """
        we might start dragging here (under the right conditions)
        and handle dragging once it starts
        """
        if (self.dragging is False) and (self.left_down is True):
            pos = event.GetPosition()
            if self.square_distance(pos, self.left_down_position) > 100:
                self.start_dragging(event, item)
        elif self.dragging is True:
            self.continue_dragging(event)
        else:
            event.Skip()


    def cb_on_left_up(self, event, item):
        """ end dragging """
        self.left_down = False
        if self.dragging is True:
            logging.debug("end dragging")
            self.finish_dragging(item)

            self.dragging = False
            self.dragged_data = {}
        else:
            event.Skip()


    def start_dragging(self, event, item):
        """ save state and setup things for actual dragging """
        logging.debug("starting to drag %s", item)
        self.dragging = True
        self.dragged_data['tree_item'] = item

        # move out the item tree from the tree
        item.remove_tree_from_parent()

        # and move out the children UI elements
        hd_items = set(item.get_all_children())

        # order them in the way they are in the view
        hd_items = [itx for itx in self.instance.line_item_panels if itx in hd_items]
        items_shown = [i.IsShown() for i in hd_items]
        self.instance.detach_items_from_ui(hd_items)
        self.dragged_data['hd_items'] = hd_items
        self.dragged_data['items_shown'] = items_shown
        item.Raise()

        self.instance.Layout()

        # create list of y positions of all remaining list_items
        self.insertions_points = self.instance.get_insertion_point_list()
        posy = item.GetPosition()[1]
        self.old_insertion_point = self.get_insertion_point(self.insertions_points, posy)

        self.continue_dragging(event)


    def continue_dragging(self, dummy_event):
        """ move things around while dragging - its a dance """
        item = self.dragged_data.get('tree_item', None)
        if item is not None:
            y = wx.GetMousePosition()[1]

            posy = (y + self.dy)
            new_insertion_point = self.get_insertion_point(self.insertions_points, posy)
            logging.debug("new insertion point : %s at %s", new_insertion_point, posy)

            if new_insertion_point != self.old_insertion_point:
                self.adjust_item_location(item, new_insertion_point, self.old_insertion_point)
                self.old_insertion_point = new_insertion_point
                self.instance.Layout()

            item.SetPosition(wx.Point(self.x, y + self.dy))
            item.Refresh()


    def insert_items_again(self, ipt):
        """ insert dragging related items back into view """
        for line_item, shown in reversed(zip(self.dragged_data['hd_items'],
                                             self.dragged_data['items_shown'])):
            self.instance.line_item_panels.insert(ipt, line_item)
            self.instance.sizer.Insert(ipt, line_item, 0,
                                       wx.EXPAND | wx.LEFT | wx.RIGHT, self.instance.border)
            if shown is True:
                line_item.Show()



    def finish_dragging(self, item):
        """ done with dragging. Put things in their correct places """
        y = wx.GetMousePosition()[1]
        posy = (y + self.dy)

        insertion_point = self.get_insertion_point(self.insertions_points, posy)
        if insertion_point == 0:
            # insert at top
            self.instance.head_item.insert_tree(item, 0)
        else:
            # insert in middle or end
            prev_item = self.instance.line_item_panels[insertion_point - 1]
            if insertion_point < len(self.instance.line_item_panels) - 1:
                next_item = self.instance.line_item_panels[insertion_point + 1]
            else:
                next_item = None

            if (prev_item.expanded is True) and (prev_item.has_child(next_item)):
                prev_item.insert_tree(item, 0)
            else:
                prev_item.get_parent_item().insert_after(item, prev_item)

        self.insert_items_again(insertion_point + 1)

        # (width bug) reinsert item to make sure it takes full width
        self.instance.sizer.Detach(item)
        self.instance.sizer.Insert(insertion_point, item, 0,
                                   wx.EXPAND | wx.LEFT | wx.RIGHT, self.border)
        self.instance.SetAutoLayout(1)
        self.instance.SetupScrolling()


    def get_insertion_point(self, ipoints, pos):  # pylint: disable=no-self-use
        """ get the sizer location of possible drop point """
        for i, dummy_item, ipt in ipoints:
            if pos < ipt:
                logging.debug("insertion point is %s", i - 1)
                return (i - 1) if i > 0 else 0
        return len(ipoints) - 1


    def adjust_item_location(self, item, nip, oip):
        """ move things around as dragging proceeds """
        if nip == oip:
            return
        self.instance.line_item_panels.remove(item)
        self.instance.sizer.Detach(item)
        self.instance.line_item_panels.insert(nip, item)
        self.instance.sizer.Insert(nip, item)


    def square_distance(self, x, y):  # pylint: disable=no-self-use
        """ squared distance of mouse from place where dragging started """
        a1, a2 = x
        b1, b2 = y
        return (a1 - b1) ** 2 + (a2 - b2) ** 2
