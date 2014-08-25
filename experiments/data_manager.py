"""
Tasks data broker and manager

"""

import wx
import thread
import time
import logging

from experiments.api_conn import GoogleTasks
from experiments.event_bus import (bind_on_event,
                                   EVT_ITEM_EDITED,
                                   EVT_COMP_CHANGED,
                                   EVT_ITEM_MOVED,
                                   )


class ChangeQueue(object):
    def __init__(self):
        self.keep_running = True
        self.queue = []
        thread.start_new_thread(self.processQueue, ())

    def enque(self, data_tuple):
        self.queue.append(data_tuple)

    def processQueue(self):
        while self.keep_running is True:
            try:
                while len(self.queue) > 0:
                    data_tuple = self.queue.pop(0)
                    method, args = data_tuple[0], data_tuple[1:]
                    method(*args)
            except:
                logging.exception("Error while processing queue : %s", str(data_tuple))

            time.sleep(5)

    def stop_thread(self):
        self.keep_running = False


class TasksDataManager(object):
    """
    This class keeps the local data of the google tasks.
    We usually look at one tasklist at a time. So we will have the notion of a current tasklist
    We will have the ability to sync that task list in a periodic manner automatically
    Probably once a minute

    We load the tasklists and keep them
    We then can load a particular tasklist and return all tasks in that list
    We will set that tasklist as current and can set auto sync

    """
    def __init__(self):
        self.tasks_api = GoogleTasks()
        self.tasklists = None
        self.list_to_items = {}
        self.item_to_list = {}
        self.changeQueue = ChangeQueue()

        bind_on_event(EVT_ITEM_EDITED, self.on_item_edited)
        bind_on_event(EVT_COMP_CHANGED, self.on_item_change_complete)
        bind_on_event(EVT_ITEM_MOVED, self.on_item_moved)


    def close(self):
        self.changeQueue.stop_thread()


    def set_credentials(self, cred):
        self.tasks_api.set_credentials(cred)


    def get_task_lists(self):
        if self.tasklists is None:
            tlists = self.tasks_api.get_tasklists()
            self.tasklists = dict([(t['id'], TaskList(t['id'], t['title'])) for t in tlists['items']])

        data = [TaskListView(tlist) for tlist in self.tasklists.values()]
        return data

    def get_task_items(self, list_obj):
        task_list = self.tasklists.get(list_obj.idx, None)
        tl_idx = task_list.idx

        if task_list is None:
            raise ValueError("Bad task list id, or task list does not exist. ID : %s" % tl_idx)

        if task_list.is_populated() is False:
            task_items = self.tasks_api.get_task_items(tl_idx)
            task_items = dict([(t['id'], TaskItem(t['id'],
                                                  t.get('parent', None),
                                                  t['title'],
                                                  t['status'] != 'needsAction',
                                                  t.get('position', None)
                                                  ))
                               for t in task_items['items']])

            self.list_to_items[tl_idx] = task_items
            self.item_to_list.update(dict([(t, tl_idx) for t in task_items.keys()]))

            task_list.set_items(task_items)

        task_items = task_list.get_items_for_view()

        return task_items


    def on_item_edited(self, event):
        logging.info("received item edit notification")
        idx, title = event.idx, event.title
        tl_idx = self.item_to_list.get(idx, None)
        if tl_idx is None:
            logging.error("task list index not found : %s", tl_idx)
            return

        self.tasks_api.update_item_title(tl_idx, idx, title)


    def on_item_change_complete(self, event):
        logging.info("received item checkbox notification")
        idx, complete = event.idx, event.complete
        tl_idx = self.item_to_list.get(idx, None)
        if tl_idx is None:
            logging.error("task list index not found : %s", tl_idx)
            return

        self.tasks_api.update_item_complete(tl_idx, idx, complete)

    def on_item_moved(self, event):
        logging.info("received item moved notification")
        idx, parent, previous = event.idx, event.parent, event.previous
        tl_idx = self.item_to_list.get(idx, None)
        if tl_idx is None:
            logging.error("task list index not found : %s", tl_idx)
            return

        self.tasks_api.move_item(tl_idx, idx, parent, previous)



class TaskList(object):
    def __init__(self, idx, title):
        self.idx = idx
        self.title = title
        self.item_dict = None
        self.item_hierarchy = None

    def is_populated(self):
        return (self.item_dict is not None)

    def get_title(self):
        return self.title

    def set_items(self, item_dict):
        self.item_dict = item_dict
        self.item_hierarchy = self.restructure_items(self.item_dict)
        self.sort_task_items()

    def get_items(self):
        return self.item_hierarchy

    def get_items_for_view(self):
        result = self.copy_hierarchy_for_view()
        return result

    def __cmp__(self, other):
        return cmp(self.title, other.title)

    def restructure_items(self, item_dict):
        items = item_dict.values()
        root_level_items = []
        for item in items:
            parent = item.get_parent()
            if parent is not None:
                parent = item_dict[parent]
                parent.add_child(item)
            else:
                root_level_items.append(item)

        return root_level_items

    def sort_task_items(self):
        self.item_hierarchy.sort(key=lambda x: x.get_position())
        for titem in self.item_hierarchy:
            titem.sort_children()

    def copy_hierarchy_for_view(self):
        def build_view_items(items):
            result = []
            for item in items:
                vitem = TaskView(item)
                result.append(vitem)
                vitem.add_children(build_view_items(item.get_children()))
            return result

        return build_view_items(self.item_hierarchy)


class TaskItem(object):
    def __init__(self, idx, parent, title, complete, position):
        self.idx = idx
        self.parent = parent
        self.position = position
        self.title = title
        self.complete = complete
        self.children = []

    def get_parent(self):
        return self.parent

    def add_child(self, item):
        self.children.append(item)

    def get_position(self):
        return self.position

    def get_children(self):
        return self.children[:]

    def sort_children(self):
        if len(self.children) > 1:
            self.children.sort(key=lambda x: x.get_position())
        for titem in self.children:
            titem.sort_children()


class TaskListView(object):
    def __init__(self, tlist):
        self.idx = tlist.idx
        self.title = tlist.title

    def get_text(self):
        return self.title


class TaskView(object):
    def __init__(self, task):
        self.idx = task.idx
        self.title = task.title
        self.complete = task.complete
        self.children = []

    def get_text(self):
        return self.title

    def get_details(self):
        return (self.idx, self.title, self.complete, self.children[:])

    def get_children(self):
        return self.children[:]

    def add_children(self, children):
        self.children.extend(children)

