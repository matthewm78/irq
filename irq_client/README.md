# Overview
A Python-based client for interacting with the IRQ REST web service.

This client is a command-line tool that uses argparse for creating sets of commands
and processing CLI arguments.

# Usage
The command can be run from the root of the project with:

```
export PYTHONPATH=$(pwd)/src/main/python:$PYTHONPATH
python3 src/main/scripts/irqclient
```

You can receive general help with:

* ` python3 src/main/scripts/irqclient -h`

This will also show a list of available commands.  You can then show help for the
specific command with (for the `show_interrupts` command):

* ` python3 src/main/scripts/irqclient show_interrupts -h`

The command requires the host and port of the IRQ service to be specified.  Here
is an example command for getting info about all the current IRQs:

* `python3 src/main/scripts/irqclient --host 127.0.0.1 --port 5000 show_irq_info`
