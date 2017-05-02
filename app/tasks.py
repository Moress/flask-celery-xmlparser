from time import sleep
from celery import states
from extensions import celery, db
from models import ParseTaskInfo
from lxml import etree


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

    if promise_task.state != states.FAILURE and promise_task.info is not None:
        result['COUNT'] = promise_task.info.get('count')
        result['WEIGHT'] = promise_task.info.get('weight')

    return result


@celery.task(bind=True, max_retries=0)
def parse(self, path):
    with celery.app.app_context():
        meta = {'weight': 0, 'count': 0}
        try:
            for (cur_count, cur_weight) in xml_parse(path):
                sleep(0.2)
                meta['count'] = cur_count
                meta['weight'] = cur_weight
                self.update_state(state='WORKING', meta=meta)

            ParseTaskInfo.query.filter_by(task_id=self.request.id).update(
                 {'weight': meta['weight'], 'state': states.SUCCESS, 'count': meta['count']})
            db.session.commit()
            return meta
        except:
            ParseTaskInfo.query.filter_by(task_id=self.request.id).update(
                {'weight': meta['weight'], 'state': states.FAILURE, 'count': meta['count']})
            db.session.commit()
            self.update_state(state=states.FAILURE, meta=meta)
            return meta


def xml_parse(path):
    tree = etree.parse(path)
    root = tree.getroot()

    item_map = {}

    count = 0
    weight = 0
    for element in root.iter("item"):
        item_id = element.findtext("id")
        parent_id = element.findtext("parentId")

        if item_id is not None:
            if item_map.get(item_id) is None:
                item_map[item_id] = {'child_count': 0, 'state': 'exist', 'type': 'child'}
            else:
                if item_map[item_id]['type'] == 'child' or item_map[item_id]['state'] == "exist":
                    raise ValueError("Duplicate id in file structure", item_id)

                item_map[item_id]['state'] = 'exist'

        if parent_id is not None:
            if item_map.get(parent_id) is None:
                item_map[parent_id] = {'child_count': 1, 'state': 'not_exist', 'type': 'parent'}
            else:
                item_map[parent_id]['child_count'] += 1
                item_map[parent_id]['type'] = 'parent'

        count += 1
        yield (count, weight)

    orphan_parents = [item_id for item_id, item in item_map.items()
                      if item['state'] == 'not_exist' and item['type'] == 'parent']

    if len(orphan_parents) > 0:
        raise ValueError("Exist orphan parents", ",".join(orphan_parents))

    weight = sum(item['child_count'] for item in item_map.values() if item['type'] == 'parent')
    yield (count, weight)
