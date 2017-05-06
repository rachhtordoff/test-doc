
Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/trusty64"
  config.vm.network "private_network", ip: "192.168.50.100"
  config.vm.hostname = "vagrant-docker-example"

  # Only if vagrant up/resume do we want to forward ports
  if ['up', 'resume', 'reload'].include? ARGV[0]
    if File.exists?(File.dirname(__FILE__) + '/uniproject/forward_ports.rb')
      require_relative 'uniproject/forward_ports'
      forward_ports(config)
    else
      print "you have not specified any ports to forward"
    end
  end
  config.vm.provision :docker
  config.vm.provision :docker_compose, yml: "/vagrant/uniproject/docker-compose.yml", rebuild: true, run: "always"

  config.vm.provider :virtualbox do |vb|
    vb.customize ['modifyvm', :id, '--memory', ENV['VM_MEMORY'] || 4096]
  end

  #setup database if we have one
  if File.exists?("uniproject/db_setup.sh")
    config.vm.provision "shell", path: "uniproject/db_setup.sh"
  end
end
