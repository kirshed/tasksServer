from task_view import TasksView
from tasks_vm import TasksVm
from tasks_model import TasksModel
from flask import Flask, render_template

####################THIS IS THE SERVER!!!!!!!!!!!!!!!!!!!!!!###############

app = Flask(__name__)

# def main():
view = TasksView()
model = TasksModel()
vm = TasksVm(view, model)


@app.route('/')
def index():
    return 'Hello world'


@app.route('/addtask/<task>')
def addtask(task):
    new_id = model.create_id()
    model.add_task(new_id, task)
    new_t_id = {"new_id": new_id}
    return render_template("add_t.html", tsk=new_t_id)


@app.route('/editask/<t_id>/<edit>')
def editask(t_id, edit):
    t = model.edit_task(t_id, edit)
    if t:
        task_edit = {"my_id": t_id}
        return render_template("edit_t.html", tsk=task_edit)
    return "The task doesn't exist"

@app.route('/getask/<num>')
def getask(num):
    t = model.get_task(num)
    if t:
        tsk = {'data': t.tsk, 'my_id': t.my_id, 'time': t.t}
        return render_template("get_t.html", tsk=tsk)
    return "The task doesn't exist"


@app.route('/getalltasks')
def getalltasks():
    tasks = model.get_all_tasks()
    if tasks:
        tsks = []
        for t in tasks:
            tsk = {'my_id': t['my_id'], 'data': t['task']}
            tsks.append(tsk)
        return render_template("get_all_t.html", tsks=tsks)
    return "No tasks exist"

@app.route('/deletask/<num>')
def deletask(num):
    # returns bool
    t = model.remove_task(num)
    if t:
        t_delete = {'my_id': num}
        return render_template("delete_t.html", tsk=t_delete)
    return "The task doesn't exist"


@app.route('/delall')
def delall():
    # returns bool
    model.delete_all_tasks()
    return render_template("delete_all.html")


# num = int(view.print_view())
# vm.execute(num)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    # main()
