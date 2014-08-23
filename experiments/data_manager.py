"""
Tasks data broker and manager

"""

import wx
from experiments.api_conn import GoogleTasks


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
        if task_list is None:
            raise ValueError("Bad task list id, or task list does not exist. ID : %s" % list_obj.idx)

        if task_list.is_populated() is False:
            task_items = self.tasks_api.get_task_items(task_list.idx)
            task_items = dict([(t['id'], TaskItem(t['id'],
                                                  t.get('parent', None),
                                                  t['title'],
                                                  t['status'] != 'needsAction',
                                                  t.get('position', None)
                                                  ))
                               for t in task_items['items']])

            task_list.set_items(task_items)

        task_items = task_list.get_items_for_view()

        return task_items
