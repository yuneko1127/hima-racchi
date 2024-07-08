from flask import Flask, render_template, request, redirect, url_for

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

@app.route('/plan', methods=['POST'])
def create_plan():
    min_time = int(request.form['min_time'])
    plan = find_diverse_plan(tasks, min_time)
    return render_template('plan.html', plan=plan)

def find_diverse_plan(tasks, min_time):
    dp = [float('inf')] * (min_time + 1)
    dp[0] = 0
    task_selection = [[] for _ in range(min_time + 1)]
    task_count = [{} for _ in range(min_time + 1)]
    
    for i in range(1, min_time + 1):
        for task in tasks:
            if task['time'] <= i:
                if dp[i - task['time']] + task['time'] < dp[i]:
                    dp[i] = dp[i - task['time']] + task['time']
                    task_selection[i] = task_selection[i - task['time']] + [task]
                    task_count[i] = task_count[i - task['time']].copy()
                    task_count[i][task['name']] = task_count[i].get(task['name'], 0) + 1
                elif dp[i - task['time']] + task['time'] == dp[i]:
                    current_diversity = len(task_count[i])
                    new_diversity = len(task_count[i - task['time']].copy().keys())
                    if new_diversity > current_diversity:
                        dp[i] = dp[i - task['time']] + task['time']
                        task_selection[i] = task_selection[i - task['time']] + [task]
                        task_count[i] = task_count[i - task['time']].copy()
                        task_count[i][task['name']] = task_count[i].get(task['name'], 0) + 1

    if dp[min_time] == float('inf'):
        return None
    
    return task_selection[min_time]

if __name__ == '__main__':
    app.run(debug=True)
