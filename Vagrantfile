# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provider "virtualbox" do |v|
    v.cpus = 2
  end
  config.vm.network "forwarded_port", guest: 5000, host: 5001
  config.vm.network "private_network", ip: "192.168.99.99"

end
