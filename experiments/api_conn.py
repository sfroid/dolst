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

    def update_item(self, tl_idx, idx, attrs):
        result = self.service.tasks().update(tasklist=tl_idx, task=idx, body=attrs).execute()
        return result


    def update_item_title(self, tl_idx, idx, title):
        attrs = {'title': title,
                 'id': idx}
        return self.update_item(tl_idx, idx, attrs)

    def update_item_complete(self, tl_idx, idx, complete):
        if complete is True:
            complete = "completed"
        else:
            complete = "needsAction"
        attrs = {'status': complete,
                 'id': idx}
        return self.update_item(tl_idx, idx, attrs)

    def move_item(self, tl_idx, idx, parent, previous):
        attrs = {
            'tasklist': tl_idx,
            'task': idx
        }
        if parent is not None:
            attrs['parent'] = parent
        if previous is not None:
            attrs['previous'] = previous

        return self.service.tasks().move(**attrs).execute()
