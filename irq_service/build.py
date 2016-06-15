from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")


name = "irqapi"
default_task = "publish"


@init
def set_properties(project):
    project.depends_on("flask==0.11.1")
    project.depends_on("flask-restful==0.3.5")

    project.set_property('distutils_console_scripts', ['irqservice=irqapi.main:run'])
