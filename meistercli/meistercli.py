from meistercli.commands import *
from meistercli.commands_model import *


def main():
    sections.add_command(list_elements)
    persons.add_command(list_elements)
    checklists.add_command(list_elements)
    labels.add_command(list_elements)
    workintervals.add_command(list_elements)

    sections.add_command(getid_of_elements)
    persons.add_command(getid_of_elements)
    checklists.add_command(getid_of_elements)
    labels.add_command(getid_of_elements)
    workintervals.add_command(getid_of_elements)

    cli()

if __name__ == '__main__':
    main()