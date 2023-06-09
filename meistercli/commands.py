from datetime import datetime, timezone, timedelta
import sys
import io
import os
from tabulate import tabulate
from pymeistertask.api import MeisterTaskAPI
import click
import helpers
from pathlib import Path
import json


def _getTask(field, value):

    tasks = meisterApi.tasks.filter_by_project(personal_project, status='open')

    for t in tasks:
        if(getattr(t, field)) == value:
            return t

@click.group()
@click.option('--apikey', help="Set the API key")
@click.option('-p', '--project', default=2374836, help="Set the project id")
@click.pass_context
def cli(ctx, apikey=None, project=None):
    
    cfgfiles = [ "~/.meistercli.conf", "..\meistercli.conf" ]

    config = None
    ctxobj = {}
    
    for cfgfile in cfgfiles:
        if not Path(cfgfile).is_file():
            # skip / ignore files that don't exist
            continue
    
        # try to open the file
        try:
            with open(cfgfile) as config_file:
                config = json.load(config_file)
                apikey = config['apikey']
        except Exception as e:
            if (e is IOError): continue
            print ("Error in config file " + cfgfile + ": " + str(e))
            exit()

    if (apikey is not None): 
        # save APIKEY for later use
        ctx.obj = MeisterTaskAPI(bearer_token=apikey)
    try:
        ctx.obj
    except:
        print ("No apikey defined. Either specify --apikey or put it into ~/.meistercli.conf.")
        exit()


@cli.command(short_help='get a task id')
@click.argument('query')
def getid(self, query):
    """return the task-id for a given meistertask web token
    \f
    which can be a task url or a task token."""
    
    if(query.startswith("http")):
        query = query.split("/")[-1]
    
    task = _getTask("token", query)
    click.echo("ID for task \"{}\" is: {}".format(task.name, task.id))

@cli.command()
@click.argument('comment', callback=helpers.get_stdin, required=False)
@click.option('-id', '--task-id', callback=helpers.get_stdin, required=False)
@click.pass_context
def comment(ctx, comment, task_id):
    """add a comment to a given task-id"""

    data = {'text':comment}
    if(comment and task_id):
        ctx.obj.comments.create(task_id, data)
    else:
        click.echo("Error: Either task id or comment is missing.")

@cli.command()
@click.argument('task-id', callback=helpers.get_stdin, required=False)
@click.pass_context
def start(ctx, task_id):
    """start a work interval for a given task-id"""
    # if not task_id:
    #     task_id = raw_input()
    helpers.start_workinterval(ctx.obj, task_id)


@cli.command()
@click.argument('task-id', callback=helpers.get_stdin, required=False)
@click.pass_context
def stop(ctx, task_id):
    """stop a running work interval for a given task-id"""
    if not task_id:
        task_id = raw_input()
    helpers.stop_workinterval(ctx.obj, task_id)


