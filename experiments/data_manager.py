"""
Tasks data broker and manager

"""

import wx
from experiments.api_conn import GoogleTasks


class TaskList(object):
    def __init__(self, idx, title):
        self.idx = idx
        self.title = title

    def get_title(self):
        return self.title

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


    def get_task_lists(self):
        if self.tasklists is None:
            tlists = self.tasks_api.get_tasklists()
            self.tasklists = [TaskList(t['id'], t['title']) for t in tlists['items']]

        return self.tasklists

    def set_credentials(self, cred):
        self.tasks_api.set_credentials(cred)
