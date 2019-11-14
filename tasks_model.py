import pandas as pd
import pymongo
from flask import Flask, render_template
from task import Task
from datetime import datetime

app = Flask(__name__)


class TasksModel:
    def __init__(self):
        myclient = pymongo.MongoClient('mongodb://localhost:27017/')
        mydb = myclient['tasksdatabase']
        self.mycol = mydb['tasks1']
        self.new_id = 0
        if self.mycol.find_one():
            # first = self.mycol.find_one({'_id': 1}, {})
            first = self.mycol.find_one()
            self.new_id = int(first['my_id'])
        else:
            self.new_id = 0
            init_id = {'my_id': '0', 'new_id': str(self.new_id)}
            self.mycol.insert(init_id)

    # generate a new id
    def create_id(self):
        self.new_id += 1
        id_update = {'my_id': str(self.new_id)}
        # updating newist id in db
        self.mycol.replace_one({}, id_update)
        return self.new_id

    # adding new task to dictionary
    def add_task(self, task_id, task_str):
        tsk = Task(task_id, task_str)
        new_task = {'my_id': str(tsk.my_id), 'task': tsk.tsk, 'time': tsk.t,
                    'edit': (tsk.last_edit)}
        self.mycol.insert(new_task)
        t = self.mycol.find_one({'my_id': str(tsk.my_id)})
        return

    def get_all_tasks(self):
        tasks = self.mycol.find({})
        if tasks.count() > 1:
            return tasks[1:]
        return []

    # editing existing task in dict
    def edit_task(self, my_id, edited):
        if self.mycol.find_one({'my_id': str(my_id)}):
            try:
                tsk = self.get_task(my_id)
            except:
                return
            tme = tsk.t
            edt_t = tsk.edit_time(datetime.now())
            # updating task id in db
            self.mycol.replace_one({'my_id': str(my_id)},
                                   {'my_id': str(my_id), 'task': edited, 'time': tsk.t,
                                    'edit': tsk.last_edit}, upsert=False)
            return True
        else:
            return False

    # getting task form db
    def get_task(self, my_id):
        '''a = self.mycol.find({})
        for x in a:
            print(x)'''
        if self.mycol.find_one({'my_id': str(my_id)}):
            t = self.mycol.find_one({'my_id': str(my_id)})
            tsk = Task(my_id, t['task'])
            tsk.set_time(t['time'])
            tsk.edit_time(t['edit'])
            return tsk
        else:
            return 0

    # removing task from dictionary
    def remove_task(self, my_id):
        if self.mycol.find_one({'my_id': str(my_id)}):
            self.mycol.delete_one({'my_id': str(my_id)})
            return True
        else:
            return False

    def delete_all_tasks(self):
        self.mycol.delete_many({})
        self.new_id = 0
        id_update = {'my_id': str(self.new_id)}
        # updating newist id in db
        self.mycol.replace_one({}, id_update)
        return

    def helper(self):
        t = self.mycol.find_one({})
        return
