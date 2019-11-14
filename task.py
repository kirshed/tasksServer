from datetime import datetime


class Task:
    def __init__(self, new_id, task_str):
        self.t = datetime.now().strftime("%H:%M:%S")
        self.last_edit = '0'
        self.my_id = new_id
        self.tsk = task_str

    def edit_time(self, tme):
        if type(tme) == str:
            self.last_edit = tme
        else:
            self.last_edit = tme.strftime("%H:%M:%S")

    def set_time(self, tme):
        if type(tme) == str:
            self.t = tme
        else:
            self.t = tme.strftime("%H:%M:%S")
