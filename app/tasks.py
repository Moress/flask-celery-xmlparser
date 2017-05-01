from time import sleep
from extensions import celery, db
from models import ParseTaskInfo


def start_parse_task(path, user_filename):
    task_promise = parse.delay(path)
    info = ParseTaskInfo(task_id=task_promise.id, state=task_promise.state, filename=user_filename)
    db.session.add(info)
    db.session.commit()


def get_parse_state(task_id):
    promise_task = parse.AsyncResult(task_id)
    result = {
        'STATE': promise_task.state,
        'COUNT': 0,
        'WEIGHT': 0,
    }

    if promise_task.state is not 'FAILURE' and promise_task.info is not None:
        result['COUNT'] = promise_task.info.get('count')
        result['WEIGHT'] = promise_task.info.get('weight')

    return result


def update_async_state(task):
    if task.state is not 'FAILURE' and task.state is not 'SUCCEED':
        async_state = get_parse_state(task.task_id)
        task.state = async_state["STATE"]
        task.weight = async_state["WEIGHT"]
        task.count = async_state["COUNT"]
    return task


@celery.task(bind=True)
def parse(self, path):
    with celery.app.app_context():
        meta = {'weight': 0, 'count': 0}

        for i in range(100):
            sleep(0.2)
            meta['weight'] += 1
            meta['count'] += 1
            self.update_state(state='WORKING', meta=meta)

        ParseTaskInfo.query.filter_by(task_id=self.request.id).update(
            {'weight': meta['weight'], 'state': 'SUCCESS', 'count': meta['count']})
        db.session.commit()

        return meta

