import requests
import logging
import json
from dao_helper import get_all_objects, get_object,make_request,GRAPH_URL

RESOURCE_PATH = "/planner/tasks"

def get_plans(group_generator_func):
    for group in group_generator_func:
        for plan in get_plans_for_group(group['id']):
            plan['details'] = get_plan_details(plan['id'])
            yield (plan)


def get_tasks(plan_generator_func):
    for plan in plan_generator_func:
        for task in get_tasks_for_plan(plan['id']):
            task['details'] = get_task_details(task['id'])
            yield task


def get_tasks_for_plan(plan_id):
    yield from get_all_objects(f'/planner/plans/{plan_id}/tasks')


def get_plans_for_group(group_id):
    try:
        yield from get_all_objects(f'/groups/{group_id}/planner/plans')
    except requests.exceptions.HTTPError:
        # already logged in make_request function, no action needed
        pass


def get_plan_details(plan_id):
    return get_object(f'/planner/plans/{plan_id}/details')


def get_task_details(task_id):
    return get_object(f'/planner/tasks/{task_id}/details')

def create_tasks(task_data_generator):
    """
    Function to create a task
    :param task_data: json object with group details, must contain plan identifier
    :param task_data: {title:string, percentComplete:int, dueDate:dateTimeTimeZone, assigneePriority: string, bucketId:string}
    :return: void
    """
    for task_data in task_data_generator:
        plan_id = task_data.get("planId") if 'planId' in task_data else None
        logging.info("planId = " +planId)
        logging.error("gen: task_data= "+ task_data +"task_data type = " +str(type(task_data)))
        try:
            for data in task_data:
                plan_id = data.get("planId")
                logging.info("planId = " +planId)
                logging.error("gen: task_data= "+ task_data +"task_data type = " +str(type(task_data)))
        except:
            logging.error("extra loop failed: data = " + data)
        if not plan_id:
            try:
                logging.error("planId not found, task data= " + json.dumps(task_data)+" task_data type = " +str(type(task_data)))
            except:
                logging.error("except planId not found, task data= " + str(task_data)+" task_data type = " +str(type(task_data)))
            raise Exception("Couldn't find id for plan")

        logging.info(f'trying to create task {task_data.get("title")}')
        make_request(f'{GRAPH_URL}{RESOURCE_PATH}', 'POST', task_data)




def update_tasks(task_data):
    """
    :param task_id:
    :param task_update_data: {@odata.etag:string, title:string, percentComplete:int, dueDate:dateTimeTimeZone, assigneePriority: string, bucketId:string}
    :return:
    """

    task_id = task_data['task_id'] if 'task_id' in task_data else None


    if not task_id:
        raise Exception("Couldn't find id for plan")
        #task_data = {"title":"updated title2","percentComplete":50,"@odata.etag":'W/"JzEtVGFzayAgQEBAQEBAQEBAQEBAQEBARCc="', "bucketId":"21xu56a4ykSdmaVjflkl75cAOedV"}

    make_request(f'{GRAPH_URL}{RESOURCE_PATH}{task_id}', 'PATCH',task_data)
    ###FIXME check return value from make_request
