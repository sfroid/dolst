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


    def get_tasks(self, tasklist):
        tasks = self.service.tasks.list(tasklist=tasklist).execute(http=self.http)
        return tasks


if __name__ == "__main__":
    fname = abs_path(["..", "settings", "dolst2.cred"])
    tasks = GoogleTasks(fname)
    result = tasks.get_saved_credentials()
    if result is None:
        result, msg = tasks.autheticate_and_get_creds()

    if result is True:
        tasks.create_http_object_and_service()
        print tasks.get_tasklists()
    else:
        print msg

