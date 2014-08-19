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
        self.api_initialized = False
        self.init_api()
        self.tasklists = None


    def init_api(self):
        result = self.tasks_api.get_saved_credentials()
        if result is True:
            self.tasks_api.create_http_object_and_service()

        self.api_initialized = result


    def is_authenticated(self):
        return self.api_initialized


    def get_user_credentials(self):
        result, msg = self.tasks_api.autheticate_and_get_creds()
        self.api_initialized = result

        if result is True:
            self.tasks_api.create_http_object_and_service()

    def get_task_lists(self):
        if self.tasklists is None:
            tlists = self.tasks_api.get_tasklists()
            self.tasklists = [TaskList(t['id'], t['title']) for t in tlists['items']]

        return self.tasklists



