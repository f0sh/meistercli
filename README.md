```
--      __  __        _       _                ____  _      ___ 
--     |  \/  |  ___ (_) ___ | |_  ___  _ __  / ___|| |    |_ _|
--     | |\/| | / _ \| |/ __|| __|/ _ \| '__|| |    | |     | | 
--     | |  | ||  __/| |\__ \| |_|  __/| |   | |___ | |___  | | 
--     |_|  |_| \___||_||___/ \__|\___||_|    \____||_____||___|
--                                                            
```

Quick and dirty command line interface for the MeisterTask API, which mainly fulfills my daily use cases. To query the Meistertask API a fork of [tomkins/pymeistertask](https://github.com/tomkins/pymeistertask) library is used. Built with [click](https://github.com/pallets/click) for the CLI interface and [tabulate](https://github.com/astanin/python-tabulate) for visualizing in tables.

## Commands

    Commands on global level:
        projects       get projects assigned to account

    Global Arguments:
        -p / --project ID

    Commands on project level:
        checklists     get checklists within the project
        labels         get labels within the project
        persons        get persons attached to any project
        sections       get sections in this project
        workintervals  get work intervals within the project

    Arguments:
        -q / --query   Multiple Key=Value criterias

    Super commands
        tasks          list tasks according the selection criteria

    Special commands:
        comment        add a comment to a given task-id
        getid          get a task id
        start          start a work interval for a given task-id
        stop           stop a running work interval for a given task-id

## Usage Examples

**Get tasks with a query criteria inside a section**

    $ meistercli tasks list -q name=Task -c 123456

**Start a working interval for that task**

    $ meistercli tasks getid -q name=Task -c 123456 | meistercli start

**Adding comments to tasks**

    $ meistercli tasks getid -q name=Task -c 123456 | meistercli comment "this is my comment to that"