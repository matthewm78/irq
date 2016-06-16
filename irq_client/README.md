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

The client uses the host:port of 127.0.0.1:5000 to connect to, but this can be overidden
for other deployment setups.  Here is an example command for getting info about all 
the current IRQs for a non-default host/port:

* `python3 src/main/scripts/irqclient --host 192.168.1.100 --port 8080 show_irq_info`
