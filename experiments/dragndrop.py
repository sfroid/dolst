"""
Drag and drop mixing class for Items List Panel

    { sfroid : 2014 }

"""

import wx
import logging
from experiments.line_items_panel import LineItemsPanel

class DragDropMixin(object):
    def __init__(self):
        self.dragging = False
        self.left_down = False
        self.left_down_position = None
        self.dragged_data = {}
        self.dx, self.dy = 0, 0

    def on_drag_start(self):
        logging.debug("starting drag")
        self.dragging = True


    def on_drag_end(self):
        logging.debug("ending drag")
        self.dragging = False

    def cb_on_left_down(self, event, item):
        logging.debug("left down on item %s", str(item))
        self.left_down = True
        ipos = self.ScreenToClient(item.GetPositionTuple())
        mpos = self.ScreenToClient(wx.GetMousePosition())

        self.x, self.y = item.GetPositionTuple()
        self.dx, self.dy = (ipos[0] - mpos[0], ipos[1] - mpos[1])

        self.left_down_position = event.GetPositionTuple()
        event.Skip()

    def cb_on_mouse_move(self, event, item):
        if (self.dragging is False) and (self.left_down is True):
            pos = event.GetPosition()
            if self.square_distance(pos, self.left_down_position) > 100:
                self.start_dragging(event, item)
        elif self.dragging is True:
            self.continue_dragging(event)
        else:
            event.Skip()

    def start_dragging(self, event, item):
        logging.debug("starting to drag %s", item)
        self.dragging = True
        self.dragged_data['tree_item'] = item

        # move out the item tree from the tree
        item.remove_tree_from_parent()

        # and move out the children UI elements
        hd_items = set(item.get_all_children())

        # order them in the way they are in the view
        hd_items = [itx for itx in self.line_item_panels if itx in hd_items]
        items_shown = [i.IsShown() for i in hd_items]
        self.detach_items_from_UI(hd_items)
        self.dragged_data['hd_items'] = hd_items
        self.dragged_data['items_shown'] = items_shown
        item.Raise()

        self.sizer.Layout()

        # create list of y positions of all remaining list_items
        self.insertions_points = self.get_insertion_point_list()
        posy = item.GetPosition()[1]
        self.old_insertion_point = self.get_insertion_point(self.insertions_points, posy)
        # create

        self.continue_dragging(event)
        #self.Layout()

    def continue_dragging(self, event):
        item = self.dragged_data.get('tree_item', None)
        if item is not None:
            x, y = wx.GetMousePosition()

            posy = (y + self.dy)
            new_insertion_point = self.get_insertion_point(self.insertions_points, posy)
            logging.debug("new insertion point : %s at %s", new_insertion_point, posy)

            if new_insertion_point != self.old_insertion_point:
                self.adjust_item_location(item, new_insertion_point, self.old_insertion_point)
                self.old_insertion_point = new_insertion_point
                self.Layout()

            item.SetPosition(wx.Point(self.x, y + self.dy))
            #item.Refresh()


    def cb_on_left_up(self, event, item):
        self.left_down = False
        if self.dragging is True:
            logging.debug("end dragging")
            self.finish_dragging(item)

            self.dragging = False
            self.dragged_data = {}
        else:
            event.Skip()

    def finish_dragging(self, item):
        x, y = wx.GetMousePosition()
        posy = (y + self.dy)

        insertion_point = self.get_insertion_point(self.insertions_points, posy)
        if insertion_point == 0:
            # insert at top
            self.head_item.insert_tree(item, 0)
            for line_item, shown in reversed(zip(self.dragged_data['hd_items'],
                                             self.dragged_data['items_shown'])):
                self.line_item_panels.insert(1, line_item)
                self.sizer.Insert(1, line_item, 0,
                                  wx.EXPAND | wx.LEFT | wx.RIGHT, self.border)
                if shown is True:
                    line_item.Show()
        else:
            # insert in middle or end
            prev_item = self.line_item_panels[insertion_point - 1]
            if insertion_point < len(self.line_item_panels) - 1:
                next_item = self.line_item_panels[insertion_point + 1]
            else:
                next_item = None


            # insert at the end
            if next_item is None:
                # insert as sibling of prev item
                prev_item.get_parent_item().insert_after(item, prev_item)
                for line_item, shown in reversed(zip(self.dragged_data['hd_items'],
                                                     self.dragged_data['items_shown'])):
                    self.line_item_panels.insert(insertion_point + 1, line_item)
                    self.sizer.Insert(insertion_point + 1, line_item, 0,
                                      wx.EXPAND | wx.LEFT | wx.RIGHT, self.border)
                    if shown is True:
                        line_item.Show()
            else:  # insert in the middle
                if prev_item.expanded is False:
                    # tree, list, sizer
                    prev_item.get_parent_item().insert_after(item, prev_item)
                    for line_item, shown in reversed(zip(self.dragged_data['hd_items'],
                                                         self.dragged_data['items_shown'])):
                        self.line_item_panels.insert(insertion_point + 1, line_item)
                        self.sizer.Insert(insertion_point + 1, line_item, 0,
                                          wx.EXPAND | wx.LEFT | wx.RIGHT, self.border)
                        if shown is True:
                            line_item.Show()

                else:
                    if prev_item.has_child(next_item): # next is child of prev (insert as child)
                        prev_item.insert_tree(item, 0)
                        for line_item, shown in reversed(zip(self.dragged_data['hd_items'],
                                                      self.dragged_data['items_shown'])):
                            self.line_item_panels.insert(insertion_point + 1, line_item)
                            self.sizer.Insert(insertion_point + 1, line_item, 0,
                                              wx.EXPAND | wx.LEFT | wx.RIGHT, self.border)
                            if shown is True:
                                line_item.Show()
                    else: # next is not child of prev (insert as child of parent)
                        prev_item.get_parent_item().insert_after(item, prev_item)
                        for line_item, shown in reversed(zip(self.dragged_data['hd_items'],
                                                             self.dragged_data['items_shown'])):
                            self.line_item_panels.insert(insertion_point + 1, line_item)
                            self.sizer.Insert(insertion_point + 1, line_item, 0,
                                              wx.EXPAND | wx.LEFT | wx.RIGHT, self.border)
                            if shown is True:
                                line_item.Show()

        self.sizer.Detach(item)
        self.sizer.Insert(insertion_point, item, 0,
                          wx.EXPAND | wx.LEFT | wx.RIGHT, self.border)
        self.SetAutoLayout(1)
        self.SetupScrolling()

    def get_insertion_point(self, ipoints, pos):
        for i, item, ipt in ipoints:
            if pos < ipt:
                logging.debug("insertion point is %s", i - 1)
                return (i-1) if i > 0 else 0
        return len(ipoints) - 1

    def adjust_item_location(self, item, nip, oip):
        if nip == oip:
            return
        self.line_item_panels.remove(item)
        self.sizer.Detach(item)
        self.line_item_panels.insert(nip, item)
        self.sizer.Insert(nip, item)


    def square_distance(self, p, q):
        a1, a2 = p
        b1, b2 = q
        return ( (a1 - b1)**2 + (a2 - b2)**2 )

