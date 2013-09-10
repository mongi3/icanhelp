Simple setup/test instructions:
===============================

To setup a test environment in a virtual machine, do the following:

1) install vagrant (ubuntu sudo apt-get install vagrant) or download off web
 1b) install virtualbox?? (this may be installed as part of vagrant and unncessary...)
2) in base directory where untar'd release (contains Vagrantfile) issue command:
   vagrant up  (this will provision and start VM)
3) goto webbrowser and enter address: "localhost:8080/icanhelp"
4) Code changes and updates can be made in the extracted icanhelp directory.
   These source files are shared with the VM and should update.
5) when done testing, feel free to tear down VM with command:
   vagrant destroy
