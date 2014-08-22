"""
loads credentials from json file and returns them
"""

import httplib2
from apiclient.discovery import build

class GoogleTasks(object):
    def __init__(self):
        self.http = None
        self.cred = None
        self.service = None


    def set_credentials(self, cred):
        self.cred = cred
        http = httplib2.Http()
        self.http = self.cred.authorize(http)
        self.service = build("tasks", "v1", http=http)


    def get_tasklists(self):
        tasklists = self.service.tasklists().list().execute(http=self.http)
        return tasklists


    def get_task_items(self, list_id):
        tasks = self.service.tasks().list(tasklist=list_id).execute(http=self.http)
        return tasks
