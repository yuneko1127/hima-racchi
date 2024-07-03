from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    task_time = request.form['task_time']
    tasks.append({'name': task_name, 'time': task_time})
    return redirect(url_for('task_list'))

@app.route('/tasks')
def task_list():
    return render_template('tasks.html', tasks=tasks)

@app.route('/delete_task/<int:index>')
def delete_task(index):
    if index < len(tasks):
        del tasks[index]
    return redirect(url_for('task_list'))

if __name__ == '__main__':
    app.run(debug=True)
