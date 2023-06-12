import click
from datetime import datetime, timezone, timedelta

def get_stdin(ctx, param, value):
    if not value and not click.get_text_stream('stdin').isatty():
        return click.get_text_stream('stdin').read().strip()
    else:
        return value

def _getStatus(object, id):

    res_type = str(type(object))
    if  res_type == "<class 'pymeistertask.projects.Project'>":
        status = {1: "active", 4: "trashed", 5:"archived"}
    elif res_type == "<class 'pymeistertask.sections.Section'>":
        status = {1: "active", 2: "trashed"}
    elif res_type == "<class 'pymeistertask.tasks.Task'>":
        status = {1: "open", 2: "completed", 8:"trashed", 18:"completed_archived"}

    return status[id]

def _prepareTabulateWidth(headers):

    width = list()
    for h in headers:
        if h in ["description", "notes", "notes_html", "name"]:
            width.append(30)
        else:
            width.append(None)
    return width

def _prepareTabulateData(ressources, colfilter=None):

    # data = [[('' if ressource.__getattribute__(h) == None else ressource.__getattribute__(h)) for h in headers] for ressource in ressources]

    # prepare the dataset as a list of list, because tabulate cannot consume the Ressource object
    data = list()
    

    for ressource in ressources:
        filterout = False
        line = list()
 
        # filter headers for unwanted columns
        headers = [i for i in ressources[0]._setattrs if i not in ["project_id", "notes", "notes_html", "assignee_name", "sequence"]]
        if colfilter: headers = [i for i in headers if i not in colfilter]
        
        for h in headers:

            element_value = ressource.__getattribute__(h)

            # Eliminate None Objects
            if element_value == None:
                line.append('')
            # remove (avatar) URLS 
            elif h.startswith("avatar"):
                line.append("[URL]")
            # make long (>50) strings short
            elif len(str(element_value)) > 50:
                line.append(str(element_value)[0:50])
            # make timestamps short
            elif (h.endswith('_at') or h == "due") and len(element_value) > 10:
                line.append(click.style(str(element_value)[0:16], fg='green'))
            # make IDs blue
            elif h.endswith('_id') or h == 'id':
                line.append(click.style(element_value, fg='blue'))
            # make tokens red
            elif h == 'token':
                line.append(click.style(element_value, fg='red'))
            # make colors, colorful
            elif h == 'color':
                color = tuple(int(element_value[i:i+2], 16) for i in (0, 2, 4))
                line.append(click.style(element_value, fg=color))
            # replace status id's with text
            elif h == 'status':
                status_element_value = _getStatus(ressource, element_value)
                line.append(click.style(status_element_value, bold=True))
            else:
                line.append(element_value)
            
        data.append(line)  

    return headers, data

def _filter(ressources: list, query: tuple):
    """filter ressource objects according to a list of queries in the format key=value"""

    query_tuples = list()
    for q in query:
        q = q.split('=', 2)
        query_tuples.append((q[0], q[1]))
    
    for ressource in ressources:
        matched = list()
        for q in query_tuples:
            element_value = ressource.__getattribute__(q[0])
            if query:
                if str(element_value).find(q[1]) >= 0:
                    matched.append(True)
                    
        
        if len(matched) == len(query_tuples): yield ressource


def getRessource(context, ressource_name, project_id, query):
    """get a ressource according to its name and project"""
    
    ressources = context.__getattribute__(ressource_name).filter_by_project(project_id)
    if query:
        ressources = list(_filter(ressources, query))
    
    return ressources

def stop_workinterval(meisterApi, task_id):
    """starts a workinterval for the given task id"""

    interval = meisterApi.workintervals.filter_by_task(task_id, ongoing=True)[0]
    end_time = datetime.now(tz=timezone.utc).isoformat()
    data = {'finished_at': end_time}
    meisterApi.workintervals.update(interval.id, data)
    click.echo("Stopped workinterval on task \"{}\" at {}".format(task_id, str(end_time)))

def start_workinterval(meisterApi, task_id):
    """stops a workinterval for the given task id"""

    start_time = datetime.now(tz=timezone.utc).isoformat()
    data = {'started_at': start_time}
    meisterApi.workintervals.create(task_id, data)
    click.echo("Started workinterval for task \"{}\" at {}".format(task_id, str(start_time)))