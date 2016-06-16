# Overview
This project is for the IRQ service problem.  It creates a REST API using Flask.

# Usage
This project contains setup files so that you can easily install and run the service
inside a Vagrant.  There is a `Vagrantfile` at the root of the project that will create
an `ubuntu/trusty64` instance and request to set it up with two CPU cores. The reason
for two cores is to showcase some of the IRQ service's features related to interrupt
counts and CPU affinity.

Additionally, there is an ansible playbook in the project root that can be run against
the Vagrant instance to build and install the IRQ service from source in the instance.
It also installs an Upstart script to run the service and then starts the service running
on port `5000`.  The playbook was designed and tested with Ansible 2.1.

A helper script is also included called `create-inventory` that will generate an
inventory file at `.vagrant/inventory` that can be used by ansible to run `playbook.yml`
against the instance.  It's not necessary but may be helpful.  The script was written
on Ubuntu so some of the sed commands it uses may need to be modified for a Mac.

Here are the commands to get things running:

```
vagrant up
./create-inventory
ansible-playbook -i .vagrant/inventory playbook.yml
```
