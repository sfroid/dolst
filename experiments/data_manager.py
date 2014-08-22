"""
Tasks data broker and manager

"""

import wx
from experiments.api_conn import GoogleTasks


class TaskList(object):
    def __init__(self, idx, title):
        self.idx = idx
        self.title = title
        self.items = None

    def get_title(self):
        return self.title

    def set_items(self, items):
        self.items = items

    def get_items(self):
        return self.items

    def __cmp__(self, other):
        return cmp(self.title, other.title)

    def get_text(self):
        return self.title


class TaskItem(object):
    pass


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

        return self.tasklists

    def get_task_items(self, list_id):
        task_list = self.tasklists.get(task_list, None)
        if task_list is None:
            raise ValueError("Bad task list id, or task list does not exist. ID : %s" % list_id)

        if


        return task_items


