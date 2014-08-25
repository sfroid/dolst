"""
Drag and drop mixing class for Items List Panel

    { sfroid : 2014 }

"""

import wx
import logging

from experiments.event_bus import notify_event, ITEM_MOVED_EVENT


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
        self.half_height = None


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

        logging.debug("clicked item pos : %s", item.GetPosition()[1])
        self.old_insertion_point = -1
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
        returnval = self.dragging
        if self.dragging is True:
            logging.debug("end dragging")
            self.continue_dragging(event)
            self.finish_dragging(item)

            self.dragging = False
            self.dragged_data = {}
        else:
            event.Skip()

        return returnval


    def start_dragging(self, event, item):
        """ save state and setup things for actual dragging """
        logging.debug("starting to drag %s", item)
        self.dragging = True
        self.dragged_data['tree_item'] = item
        self.dragged_data['item_parent'] = item.get_parent_item()
        self.dragged_data['item_previous'] = item.get_previous_sibling()

        item.remove_tree_from_parent()
        hd_items = set(item.get_all_children())

        # order them in the way they are in the view
        hd_items = [itx for itx in self.instance.line_item_panels if itx in hd_items]
        items_shown = [i.IsShown() for i in hd_items]

        self.instance.detach_items_from_ui(hd_items)
        self.dragged_data['hd_items'] = hd_items
        self.dragged_data['items_shown'] = items_shown
        self.dragged_data['item_text'] = item.text_editor.stext.GetLabel()
        self.set_dragging_text(item, len(hd_items))
        item.Raise()
        item.cb_mouse_left_item("dummyevent")

        self.instance.Layout()

        # create list of y positions of all remaining list_items
        self.insertions_points = self.instance.get_insertion_point_list()
        self.half_height = (self.insertions_points[1] - self.insertions_points[0])/2.0
        self.continue_dragging(event)


    def set_dragging_text(self, item, numItems):
        """ set the label of the dragged text """
        label = item.text_editor.stext.GetLabel()
        if numItems > 0:
            label = "%s... (+%s item%s)" % (label[:10], numItems, "s" if numItems > 1 else "")
            item.text_editor.stext.SetLabel(label)


    def reset_dragging_text(self, item):
        """ set the dragged item's text label to the original value """
        item.text_editor.stext.SetLabel(self.dragged_data['item_text'])


    def continue_dragging(self, dummy_event):
        """ move things around while dragging - its a dance """
        item = self.dragged_data.get('tree_item', None)
        if item is not None:
            y = wx.GetMousePosition()[1]

            posy = (y + self.dy) + self.half_height
            new_insertion_point = self.get_insertion_point(self.insertions_points, posy)

            if new_insertion_point != self.old_insertion_point:
                logging.debug("new insertion point : %s at %s", new_insertion_point, posy)
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
        posy = (y + self.dy) + self.half_height

        insertion_point = self.get_insertion_point(self.insertions_points, posy)
        ins_loc = self.get_sizer_insertion_index(insertion_point)
        if insertion_point == 0:
            # insert at top
            self.instance.head_item.insert_tree(item, 0)
        else:
            # insert in middle or end
            prev_visible_item = self.get_kth_visible_item(insertion_point - 1)

            if ins_loc < len(self.instance.line_item_panels) - 1:
                next_item = self.instance.line_item_panels[ins_loc + 1]
            else:
                next_item = None

            if (prev_visible_item.expanded is True) and (prev_visible_item.has_child(next_item)):
                prev_visible_item.insert_tree(item, 0)
            else:
                prev_visible_item.get_parent_item().insert_after(item, prev_visible_item)

        self.insert_items_again(ins_loc + 1)
        self.reset_dragging_text(item)

        # (statictext width bug) reinsert item to make sure it takes full width
        self.instance.sizer.Detach(item)
        self.instance.sizer.Insert(ins_loc, item, 0,
                                   wx.EXPAND | wx.LEFT | wx.RIGHT, self.border)
        self.instance.SetAutoLayout(1)
        self.instance.SetupScrolling()

        self.notify_on_move(item)


    def notify_on_move(self, item):
        new_parent = item.get_parent_item()
        new_previous = item.get_previous_sibling()
        old_parent = self.dragged_data['item_parent']
        old_previous = self.dragged_data['item_previous']

        if (new_parent != old_parent) or (new_previous != old_previous):
            idx = item.text_editor.obj.idx
            parent, previous = None, None
            if hasattr(new_parent, 'text_editor'):
                parent = new_parent.text_editor.obj.idx
            if hasattr(new_previous, 'text_editor'):
                previous = new_previous.text_editor.obj.idx

            notify_event(ITEM_MOVED_EVENT,
                         idx=idx,
                         parent=parent,
                         previous=previous)


    def get_insertion_point(self, ipoints, pos):  # pylint: disable=no-self-use
        """ get the view location of current drop point """
        for j, ipt in enumerate(ipoints):
            if pos < ipt:
                return (j-1) if j > 0 else 0
        return j


    def get_kth_visible_item(self, idxk):
        """ return the kth visible item (0 based) """
        shown_count = 0
        for item in self.instance.sizer.Children:
            if item.IsShown():
                if shown_count == idxk:
                    return item.GetWindow()
                shown_count += 1


    def get_sizer_insertion_index(self, idxk):
        """ return the index for the kth visible item """
        shown_count = 0
        for i, item in enumerate(self.instance.sizer.Children):
            if item.IsShown():
                if shown_count == idxk:
                    return i
                shown_count += 1
        return len(self.instance.sizer.Children)


    def adjust_item_location(self, item, nip, oip):
        """ move things around as dragging proceeds """
        if nip == oip:
            return
        self.instance.line_item_panels.remove(item)
        self.instance.sizer.Detach(item)
        loc = self.get_sizer_insertion_index(nip)
        self.set_dragged_item_indent_level(item, loc)
        self.instance.line_item_panels.insert(loc, item)
        self.instance.sizer.Insert(loc, item)


    def set_dragged_item_indent_level(self, item, loc):
        """ set indent level of item as its dragged around """
        level = 0
        for i in range(loc - 1, -1, -1):
            prev = self.instance.line_item_panels[i]
            if prev.IsShown() is True:
                level = prev.level
                if prev.expanded and len(prev.children) > 0:
                    level = level + 1

                break

        item.set_indent_level(level)


    def square_distance(self, x, y):  # pylint: disable=no-self-use
        """ squared distance of mouse from place where dragging started """
        a1, a2 = x
        b1, b2 = y
        return (a1 - b1) ** 2 + (a2 - b2) ** 2
