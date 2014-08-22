"""
Authentication

    { sfroid : 2014 }

"""

import wx
import simplejson
import argparse
import time
import logging
import thread
import traceback

from multiprocessing import Process, Queue

from oauth2client.file import Storage
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow


"""
have auth file?
    yes - proceed

ask user permission to use google tasks
    no - return None, No permission

Yes:
    Open web browser and authenticate in separate thread

    Show message that we are awaiting authenticate with cancel button
        cancel - return None, Cancelled waiting

    Loop waiting for authentication and then close window if successful



"""


PERMISSION_MSG = """\
Dolst needs to be associated with a Google account to sync with Google Tasks.

Click OK to open a web browser and grant permission to Dolst to manage Google Tasks.

Click Cancel to exit Dolst.
"""

WAIT_MSG = """\
A browser window has been opened for authentication with google and\
permission to access google tasks.

This window will automatically close after permission is given or denied.

Click Cancel to abort.
"""

AUTH_FAIL_MSG = """\
We failed to get appropriate permissions from google.

Click OK to try agian or Cancel to exit application.
"""


def abs_path(path):
    from os.path import abspath, dirname, join
    return abspath(join(dirname(__file__), *path))


class Authentication(object):
    """
    Authentication with google account
    """
    def __init__(self, view, app_info_fname, cred_fname):
        self.view = view
        self.app_info_fname = abs_path(app_info_fname)
        self.cred_fname = abs_path(cred_fname)
        self.cred = None
        self.callback = None
        self.web_auth_inprocess = None
        self.wait_aborted = False
        self.web_auth_process = None
        self.error = None


    def reinit_attrs(self):
        """ re-initialize attributes when retrying auth """
        self.cred = None
        self.web_auth_inprocess = None
        self.wait_aborted = False
        self.web_auth_process = None
        self.error = None


    def get_credentials(self, callback, skip_consent=False):
        """ main entry method for authenticating """
        self.callback = callback

        self.cred = self.get_saved_credentials()
        if self.cred is not None:
            self.return_credentials(self.cred, "saved creds")
            return

        if skip_consent is False:
            self.get_webauth_consent()
        else:
            wx.CallAfter(self.init_web_auth)


    def get_app_info_field(self, app_info, field):
        """
        return the field from the app info data
        """
        try:
            field_val = app_info["installed"][field]
        except KeyError:
            raise Exception("%s field not found in credentials data" % field)

        return field_val


    def get_app_info(self):
        """ return the app details from the json file """
        return simplejson.loads(open(self.app_info_fname).read())


    def get_saved_credentials(self):
        """ if we have credentials saved, return them """
        storage = Storage(self.cred_fname)
        cred = storage.get()
        return cred


    def return_credentials(self, retval, msg=None):
        """ send the credentials back to the callback method """
        wx.CallAfter(self.callback, retval, msg)


    def get_webauth_consent(self):
        """ ask user if they want to open browser and authenticate """
        dlg = wx.MessageDialog(self.view,
                               PERMISSION_MSG,
                               "Google tasks permission...",
                               wx.OK | wx.CANCEL | wx.OK_DEFAULT,
                               )
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            wx.CallAfter(self.init_web_auth)
        else:
            self.return_credentials(None, "reject auth")


    def init_web_auth(self):
        """ prepare to open browser. this is a bit tricky """
        self.queue = Queue()
        # start separate process for browser
        self.web_auth_process = Process(target=self.auth_and_get_creds, args=(self.queue,))
        self.web_auth_process.start()
        self.web_auth_inprocess = True

        # start threads to wait for browser auth or user impatience
        thread.start_new_thread(self.wait_for_web_auth_process, ())
        thread.start_new_thread(self.wait_for_auth_or_dlg, ())
        wx.CallAfter(self.show_wait_message)


    def auth_and_get_creds(self, queue):
        """ separate process to get browser authentication """
        try:
            app_info = self.get_app_info()
            flow = OAuth2WebServerFlow(client_id=self.get_app_info_field(app_info, "client_id"),
                                       client_secret=self.get_app_info_field(app_info, "client_secret"),
                                       scope="https://www.googleapis.com/auth/tasks",
                                       redirect_uri="http://localhost:27381",
                                       )

            storage = Storage(self.cred_fname)
            parser = argparse.ArgumentParser(parents=[tools.argparser])
            flags = parser.parse_args()
            error = None

            try:
                cred = tools.run_flow(flow, storage, flags)
            except SystemExit:
                cred = None
                error = "Authentication request was rejected."

            cred = cred
            error = error
        except:
            cred = None
            error = traceback.format_exc()

        queue.put((cred, error))


    def wait_for_web_auth_process(self):
        """ thread which waits (blocking) for the web auth process """
        self.web_auth_process.join()
        result = self.queue.get()
        if len(result) == 2:
            self.cred, self.error = result
        else:
            self.cred, self.error = None, result

        self.web_auth_inprocess = False


    def show_wait_message(self):
        """ show a wait window to user """
        self.wait_dlg = wx.MessageDialog(self.view,
                               WAIT_MSG,
                               "Google tasks permission...",
                               wx.CANCEL,
                               )
        try:
            result = self.wait_dlg.ShowModal()
            self.wait_dlg.Destroy()
        except:
            # this will happen only if we close the dialog programmatically
            result = wx.ID_OK

        if result == wx.ID_CANCEL:
            self.wait_aborted = True
        else:
            logging.info("Web browser auth step completed")


    def wait_for_auth_or_dlg(self):
        """ thread for polled wait for wait for first of dialog or web auth process """
        while 1:
            if self.wait_aborted is True:
                self.return_credentials(None, "wait Aborted")
                self.web_auth_process.terminate()
                break;
            elif self.web_auth_inprocess is False:
                wx.CallAfter(self.return_credentials, self.cred, self.error)
                wx.CallAfter(self.close_wait_message)
                break;

            time.sleep(0.1)


    def close_wait_message(self):
        """ close the modal wait dialog """
        logging.info("\n\n\nClosing modal dialog")
        logging.info("dialog modal? : %s", self.wait_dlg.IsModal())
        if self.wait_dlg.IsModal() is False:
            self.wait_dlg.Close()
            self.wait_dlg.Destroy()
        else:
            self.wait_dlg.EndModal(wx.ID_OK)


    def do_reauth(self):
        """ if the user made a mistake, let them try auth again """
        dlg = wx.MessageDialog(self.view,
                               AUTH_FAIL_MSG,
                               "Authentication Failed...",
                               wx.OK | wx.CANCEL | wx.OK_DEFAULT,
                               )
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            return True
        return False


