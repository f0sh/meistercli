import click
import helpers
from tabulate import tabulate
from commands import cli



@cli.group()
def projects():
    """get projects"""


@projects.command('list')
@click.option('-s', '--status', default="active", type=click.Choice(['active', 'archived', 'all']), help='only get projects with the given status')
@click.option('-q', '--query', type=str, help='only get tasks with given string in name')
@click.pass_context
def projects_list(ctx, status, query):
    """get projects assigned to account"""

    meisterApi = ctx.obj
    ressources = meisterApi.projects.all(status=status)

    headers, data = helpers._prepareTabulateData(ressources, query)
    click.echo("Found {} items:".format(len(data)))
    click.echo(tabulate(data, headers=headers, tablefmt="simple_grid"))


@cli.group()
def tasks():
    """get tasks"""


@tasks.command('list')
@click.option('-id', '--task-id', type=int, help='get a specific task')
@click.option('-s', '--status', default="open", type=click.Choice(['open', 'completed', 'trashed', 'completed_archived']), help='only get tasks with the given status')
@click.option('-c', '--section', type=int, help='only get tasks in the given section')
@click.option('-q', '--query', type=str, default=[], multiple=True, help='only get tasks with given string in name')
@click.option('-t', '--token', type=str, help='a task token from the web interface')
@click.pass_context
def list_tasks(ctx, task_id, status, section, query: list, token):
    """lists a single task by id or all tasks by project or section"""

    project_id = ctx.parent.parent.params['project']
    meisterApi = ctx.obj

    if(token and token.startswith("http")):
        token = token.split("/")[-1]

    if token:
        query = list(query)
        query.append('token={}'.format(token))

    if(task_id):
        ressources = list(meisterApi.tasks.get(task_id))

    elif(section):
        ressources = meisterApi.tasks.filter_by_section(section, status=status, items=500)

    else:
        ressources = meisterApi.tasks.filter_by_project(project_id, status=status, items=500)
        
    #ressources = list(filter(lambda x: x.name.find(filter_name), ressources))
    
    if query:
        ressources = list(helpers._filter(ressources, query))

    headers, data = helpers._prepareTabulateData(ressources)
    width = helpers._prepareTabulateWidth(headers)
    
    click.echo(tabulate(data, headers=headers, tablefmt="simple_grid", maxcolwidths=width))
    click.echo("Found {} items:".format(len(data)))


@tasks.command('getid')
@click.option('-id', '--task-id', type=int, help='get a specific task')
@click.option('-s', '--status', default="open", type=click.Choice(['open', 'completed', 'trashed', 'completed_archived']), help='only get tasks with the given status')
@click.option('-c', '--section', type=int, help='only get tasks in the given section')
@click.option('-q', '--query', type=str, multiple=True, help='only get tasks with given string in name')
@click.option('-t', '--token', type=str, help='a task token from the web interface')
@click.pass_context
def getid_of_task(ctx, task_id, status, section, query, token):
    """returns an id for task"""
    
    project_id = ctx.parent.parent.params['project']
    meisterApi = ctx.obj

    if(token and token.startswith("http")):
        token = token.split("/")[-1]

    if token:
        query = list(query)
        query.append('token={}'.format(token))

    if(task_id):
        ressources = list(meisterApi.tasks.get(task_id))

    elif(section):
        ressources = meisterApi.tasks.filter_by_section(section, status=status)

    else:
        ressources = meisterApi.tasks.filter_by_project(project_id, status=status)

    if query:
        ressources = list(helpers._filter(ressources, query))

    try:
        id = [r.id for r in ressources][0]
        click.echo(id)
    
    except IndexError as e:
        pass

@tasks.command('add')
@click.argument('title', callback=helpers.get_stdin, required=True)
@click.option('-c', '--section', type=str, required=True, help='the section-id')
@click.option('-n', '--notes', type=str, required=False, help='desciption for the task')
@click.option('-d', '--due', type=str, required=False, help='due date')
@click.option('-l', '--label', type=int, required=False, multiple=True, help='label id')
@click.pass_context
def add_task(ctx, title, section, notes, due, label):
    """create a new task"""

    if not title: task_title = click.prompt("Task Title", type=str)
    if not title: task_note = click.prompt("Task Description", type=str)

    data = {}
    if title: data['name'] = title
    if notes: data['notes'] = notes
    if due: data['due'] = due
    if label: data['label'] = label
    click.echo("About to create new task: {}".format(data))
    ctx.obj.tasks.create(section_id=section, data=data)
    

@cli.group()
def persons():
    """get persons attached to any project"""


@cli.group()
def sections():
    """get sections in this project"""


@cli.group()
# @click.option('-t', '--task', type=int, help='only get checklists for the given task id')
def checklists():
    """get checklists within the project"""


@cli.group()
@click.option('-t', '--task', type=int, help='only get checklists for the given task id')
@click.option('-0', '--raw', is_flag=True, default=False, help='return all values')
def labels(project, task, raw):
    """get labels within the project"""


@cli.group()
@click.option('-p', '--project', default=2374836, help='only get checklists in the given project')
@click.option('-t', '--task', type=int, help='only get checklists for the given task id')
def workintervals(project, task):
    """get work intervals within the project"""



@click.command('list')
@click.option('-q', '--query', multiple=True, type=str, help='only get tasks with given string in name')
@click.pass_context
def list_elements(ctx, query):
    """lists all elements by project"""
    
    project_id = ctx.parent.parent.params['project']
    meisterApi = ctx.obj

    ressources = helpers.getRessource(meisterApi, ctx.parent.info_name, project_id, query)
    headers, data = helpers._prepareTabulateData(ressources)
    width = helpers._prepareTabulateWidth(headers)

    click.echo("Found {} items:".format(len(data)))
    click.echo(tabulate(data, headers=headers, tablefmt="simple_grid", maxcolwidths=width))


@click.command('getid')
@click.option('-q', '--query', type=str, multiple=True, help='only get tasks with given string in name')
@click.pass_context
def getid_of_elements(ctx, query):
    """lists all elements by project"""
    
    project_id = ctx.parent.parent.params['project']
    meisterApi = ctx.obj
    ressources = helpers.getRessource(meisterApi, ctx.parent.info_name, project_id, query)

    try:
        id = [r.id for r in ressources][0]
        click.echo(id)
    
    except IndexError as e:
        pass

    