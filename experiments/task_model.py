"""
Data model for task lists
"""

class TaskMixin(object):
    """
    Common methods for Task and TaskCategory classes
    """
    def append_task(self, task):
        """
        Append a task to the task list
        """
        self.tasks.append(task)
        task.set_parent(self)


    def remove_task(self, task):
        """
        Remove a task from the task list
        """
        self.tasks.remove(task)
        task.set_parent(None)
        return task


class Task(TaskMixin):
    """
    Blueprint of a task
    """
    def __init__(self):
        self.text = ""
        self.complete = False
        self.by_date = None
        self.bgcolor = "#000000"
        self.tasks = []
        self.parent = None


    def set_parent(self, parent):
        """
        Set the parent for this task
        """
        self.parent = parent


    def get_parent(self):
        """
        Returns the parent for this task
        """
        return self.parent


    def set_complete(self, complete):
        """
        Set completion value
        """
        self.complete = complete


    def is_complete(self):
        """
        Is the task complete
        """
        return self.complete


class TaskCategory(TaskMixin):
    """
    Blueprint of a task category
    """
    def __init__(self, name):
        self.name = name
        self.tasks = []


    def rename(self, name):
        """
        Rename this task category
        """
        self.name = name
