import os
import time

from factory import create_manager_app, create_app
from flask import render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from tasks import *

app = create_app()
manager = create_manager_app(app)


@app.route('/')
def index():
    tasks = ParseTaskInfo.query.order_by(ParseTaskInfo.date_add.desc()).slice(0, 10)
    return render_template('index.html', tasks=map(update_async_state, tasks))


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file_upload']
        if file:
            time_prefix = time.strftime("%Y-%m-%d_%H-%M-%S")
            user_filename = secure_filename(file.filename)
            filename = time_prefix + "_" + user_filename
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            start_parse_task(path, user_filename)

    return redirect(url_for('index'))


@app.route('/task_status/<task_id>')
def task_status(task_id):
    return jsonify(get_parse_state(task_id))


if __name__ == '__main__':
    manager.run()

