
Vagrant.configure(2) do |config|

  config.vm.box = "ubuntu/trusty64"
  config.vm.network "private_network", ip: "192.168.50.100"
  config.vm.hostname = "vagrant-docker-example"

  # Only if vagrant up/resume do we want to forward ports
  if ['up', 'resume', 'reload'].include? ARGV[0]
    if File.exists?(File.dirname(__FILE__) + '/dev-env-project/forward_ports.rb')
      require_relative 'dev-env-project/forward_ports'
      forward_ports(config)
    else
      print colorize_red("you have not specified any ports to forward")
    end
  end
  config.vm.provision :docker
  config.vm.provision :docker_compose, yml: "/vagrant/dev-env-project/docker-compose.yml", rebuild: true, run: "always"

  config.vm.provider :virtualbox do |vb|
    vb.customize ['modifyvm', :id, '--memory', ENV['VM_MEMORY'] || 4096]
  end
end
