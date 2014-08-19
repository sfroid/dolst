"""
loads credentials from json file and returns them
"""

import simplejson
import argparse


def abs_path(path):
    from os.path import abspath, dirname, join
    return abspath(join(dirname(__file__), *path))


class GoogleTasks(object):
    def __init__(self, fname=None):
        self.http = None
        self.cred = None
        self.service = None
        if fname is None:
            self.client_details_fname = abs_path(["..", "settings", "credentials.json"])
        else:
            self.client_details_fname = fname

        self.cred_fname = abs_path(["..", "settings", "dolst3.json"])

    def get_cred_data(self):
        """
        load credentials info from json file
        """
        return simplejson.loads(open(self.client_details_fname).read())


    def get_cred_field(self, cred_data, field):
        """
        re
        """
        try:
            field_val = cred_data["installed"][field]
        except KeyError:
            raise Exception("%s field not found in credentials data" % field)

        return field_val


    def get_saved_credentials(self):
        """ return stored credentials. None if creds not found """
        from oauth2client.file import Storage
        storage = Storage(self.cred_fname)

        self.cred = storage.get()
        return (True if self.cred is not None else False)


    def autheticate_and_get_creds(self):
        """ open browser to authenticate, create credentials,
        save and return cred object """
        from oauth2client.file import Storage
        from oauth2client import tools
        from oauth2client.client import OAuth2WebServerFlow

        storage = Storage(self.cred_fname)
        cred_info = self.get_cred_data()
        flow = OAuth2WebServerFlow(client_id=self.get_cred_field(cred_info, "client_id"),
                                   client_secret=self.get_cred_field(cred_info, "client_secret"),
                                   scope="https://www.googleapis.com/auth/tasks",
                                   redirect_uri="http://localhost:27381",
                                   )

        parser = argparse.ArgumentParser(parents=[tools.argparser])
        flags = parser.parse_args()
        error = None

        try:
            cred = tools.run_flow(flow, storage, flags)
        except SystemExit:
            cred = None
            error = "Authentication request was rejected."

        self.cred = cred
        return ((True if cred is not None else False),
                ("Successfully authenticated." if error is None else error))


    def create_http_object_and_service(self):
        import httplib2
        from apiclient.discovery import build

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




