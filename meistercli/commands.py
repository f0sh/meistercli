"""CLI Commands"""
# pylint: disable=unused-argument, protected-access
import json
import sys
from pathlib import Path
from pymeistertask.api import MeisterTaskAPI
import click
from meistercli import helpers



@click.group()
@click.option('--apikey', help="Set the API key")
@click.option('-p', '--project', default=2374836, help="Set the project id")
@click.pass_context
def cli(ctx, apikey=None, project=None):
    # pylint: disable=broad-exception-caught

    cfgfiles = [ Path.joinpath(Path.home(), ".meistercli.conf"), "meistercli.conf" ]

    config = None

    for cfgfile in cfgfiles:
        if not Path(cfgfile).is_file():
            # skip / ignore files that don't exist
            continue

        # try to open the file
        try:
            with open(cfgfile, encoding='UTF-8') as config_file:
                config = json.load(config_file)
                apikey = config['apikey']
        except OSError as e:
            if e is OSError:
                continue
            print ("Error in config file " + cfgfile + ": " + str(e))
            sys.exit()

    if apikey is not None: 
        # save APIKEY for later use
        ctx.obj = MeisterTaskAPI(bearer_token=apikey)
    try:
        ctx.obj
    except Exception:        
        print ("No apikey defined. Either specify --apikey or put it into ~/.meistercli.conf.")
        exit()


# @cli.command(short_help='get a task id')
# @click.argument('query')
# @click.pass_context
# @DeprecationWarning
# def getid(ctx, query):
#     """return the task-id for a given meistertask web token
#     \f
#     which can be a task url or a task token."""
#     project_id = ctx.parent.parent.params['project']

#     if query.startswith("http"):
#         query = query.split("/")[-1]
    
#     tasks = ctx.obj.tasks.filter_by_project(project_id, status='open')

#     for task in tasks:
#         if(getattr(task, field)) == value:
#             click.echo("ID for task \"{}\" is: {}".format(task.name, task.id))
#             return
    
@cli.command()
@click.argument('comment', callback=helpers.get_stdin, required=False)
@click.option('-id', '--task-id', callback=helpers.get_stdin, required=False)
@click.pass_context
def comment(ctx, comment, task_id):
    """add a comment to a given task-id"""
    # pylint: disable=redefined-outer-name

    data = {'text':comment}
    if comment and task_id:
        ctx.obj.comments.create(task_id, data)
    else:
        click.echo("Error: Either task id or comment is missing.")

@cli.command()
@click.argument('task-id', callback=helpers.get_stdin, required=False)
@click.pass_context
def start(ctx, task_id):
    """start a work interval for a given task-id"""

    helpers.start_workinterval(ctx.obj, task_id)


@cli.command()
@click.argument('task-id', callback=helpers.get_stdin, required=False)
@click.pass_context
def stop(ctx, task_id):
    """stop a running work interval for a given task-id"""

    helpers.stop_workinterval(ctx.obj, task_id)
    
