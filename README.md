# Meistertask CLI

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

    Super commands
        tasks          list tasks according the selection criteria

    Special commands:
        comment        add a comment to a given task-id
        getid          get a task id
        start          start a work interval for a given task-id
        stop           stop a running work interval for a given task-id
