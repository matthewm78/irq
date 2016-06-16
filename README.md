# Overview
This repository contains code for solving the IRQ balancing problem and the IRQ
client-server problem.

The folders `irqbalance`, `irq_client`, and `irq_server` contain the code for
the IRQ balancing script, the IRQ client and the IRQ REST server respectively.


# Project Requirements
Each of the projects was designed and tested using Python 3.4.3.  The `requirements.txt` file in the root of this repository contains the Python modules needed to build and run
all of the code in the three sub-projects of this repository.  To get setup, you can
just use `pip3` with the `requirements.txt` file provided.

## PyBuilder
Each project is a PyBuilder project [PyBuilder](http://pybuilder.github.io/), which
is a build tool similar to Maven.  The `setup.py` and `build.py` in the root of each project
are files used by PyBuilder for building.

To run a build that will run unit tests and generate a distribution, you can run:

* `pyb -vvvv`

from the root of the project.  The `build.py` file has been setup so that it will
create a distribution with a `setup.py` file properly configured with things such
as project name, version, dependencies and console scripts.


# Assumptions / Caveats
This section outlines any assumptions made, known limitations and caveats related
to the designed projects.

* I started the project doing test-driven development but had to abandon that for time
reasons; the irqbalance project was the 1st one written so you can see examples there of some of the types of tests I was writing; as things progressed, my unit test style and
patterns changed some but I didn't have time to go back and synchronize things; in a
real project, the patterns, naming conventions, etc. employed would be much more
unified and coherent; I also would normally have a larger set of high-level integration
tests, particularly in the client project where a mock web service would be wired
into the client during testing to it was actually making test requests over the wire.
* I had never used Flask before this project so I'm sure there are more elegant
ways to organize a Flask project and code and configuration.
* error handling was not included in any of the code due to time constraints; in
a real project though, there would be a multitude of error handling code included
to do things like validating input, returning proper HTTP status codes, not emitting
stack traces for exceptions, building custom exception classes and handlers, etc.

## irq_service
The IRQ service makes uses of a background thread that essentially is creating
a time-series database for storing historical interrupt counts.  The solution is
a simple CSV-based solution but is not something that would be practical for
real-world use.  Some issues that would need to be addressed with the way the
database is implemented as well as how it is accessed/used would be:

* the DB file grows indefinitely so disk space would become an issue
* managing concurrent read-write access so DB integrity is maintained
* a way to handle different sampling intervals and inclusion of some
downsampling capability
* access to the DB to lookup relevant items are essentially "full-table scans"; these
are not efficient ways to lookup data

