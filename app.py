from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

tasks = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    task_time = int(request.form['task_time'])
    tasks.append({'name': task_name, 'time': task_time})
    return redirect(url_for('task_list'))

@app.route('/tasks')
def task_list():
    return render_template('tasks.html', tasks=tasks)

@app.route('/delete_task/<int:index>', methods=['GET'])
def delete_task(index):
    if index < len(tasks):
        del tasks[index]
    return redirect(url_for('task_list'))

@app.route('/plan', methods=['POST'])
def create_plan():
    sukima_time = int(request.form['sukima_time'])
    plan = []
    min_time = tasks[0]["time"]
    for task in tasks:
        if task["time"] < min_time:
            min_time = task["time"]
    tasks_kyukei = [{'name': '休憩', 'time': 1}]
    tasks_kyukei.extend(tasks)
    
    while sukima_time > 0:
        filtered_tasks = []
        for task_kyukei in tasks_kyukei:
            if task_kyukei["time"] <= sukima_time:
                filtered_tasks.append(task_kyukei)
        
        if filtered_tasks:
            random_task = random.choice(filtered_tasks)
<<<<<<< HEAD
            plan.append(random_task)
            sukima_time -= random_task['time']
=======
            if random_task["name"] == "休憩":
                plan.append(random_task)
                sukima_time -= random_task["time"]
            elif sukima_time - random_task["time"] < min_time:
                do_task = {"name": random_task["name"], "time": sukima_time}
                plan.append(do_task)
                sukima_time -= do_time
            else:
                do_time = random_task["time"] + random.randint(0, sukima_time - random_task["time"])
                do_task = {'name': random_task["name"], 'time': do_time}
                plan.append(do_task)
                sukima_time -= do_time
>>>>>>> practice
        else:
            break
    
    return render_template('plan.html', plan=plan)


if __name__ == '__main__':
    app.run(debug=True)
