from task import Task
from flask import Flask


class TasksVm:
    def __init__(self, vw, mdl):
        self.view = vw
        self.model = mdl
        # functions dictionary
        self.funcMap = dict()
        self.funcMap[1] = self.add_t
        self.funcMap[2] = self.edit_t
        self.funcMap[3] = self.get_t
        self.funcMap[4] = self.get_all_t
        self.funcMap[5] = self.remove_t
        self.funcMap[6] = self.delete_all
        self.funcMap[7] = self.exit_program
        self.funcMap[8] = self.helper

    # calling specified function
    def execute(self, num):
        if num > 7 or num < 1:
            print("Not an option, please enter a number from the menu")
        else:
            # calling requested function
            self.funcMap.get(num)()
        # recalling execute
        newNum = int(self.view.print_view())
        self.execute(newNum)

    # adding task
    def add_t(self):
        print("Please enter the task you would like to add:")
        task_str = input()
        t_id = self.model.create_id()
        # creating new task
        task = Task(t_id, task_str)
        # calling add_task from model
        self.model.add_task(task.my_id, task_str)
        print("task", t_id, "added at", task.t)
        return task

    # editing existing task if exists
    def edit_t(self):
        print("Please enter the task id you would like to edit:")
        id = int(input())
        print("please enter the edited task:")
        edited = input()
        if self.model.edit_task(id, edited):
            try:
                t = self.model.get_task(id)
            except:
                print("unable to perform task. try adding an additional task first, then try again")
                return
            print("task", id, "edited at", t.last_edit)
        else:
            print("task", id, "does not exist")

    # getting specified task
    def get_t(self):
        print("Please enter the task id you would like to get:")
        id = int(input())
        try:
            task = self.model.get_task(id)
        except:
            print("unable to perform task. try adding an additional task first, then try again")
            return
        if task:
            if task.last_edit == '0':
                print("the task you requested:", task.tsk, "was created at", task.t)
            else:
                print("the task you requested:", task.tsk, "was created at", task.t, "and was last edited at",
                      task.last_edit)
        else:
            print("the task doesn't exist")

    # getting all tasks
    def get_all_t(self):
        tasks = self.model.get_all_tasks()
        if tasks:
            for t in tasks:
                print("task #", t['my_id'], "is", t['task'])
            return tasks
        print("There are no tasks to display")

    # removing specified task
    def remove_t(self):
        print("Please enter the task id you would like to remove:")
        id = int(input())
        if self.model.remove_task(id):
            print("task", id, "was deleted")
        else:
            print("task", id, "does not exist")

    # exiting program
    def exit_program(self):
        exit()

    def delete_all(self):
        self.model.delete_all_tasks()
        print("all tasks were deleted")

    def helper(self):
        self.model.helper()
