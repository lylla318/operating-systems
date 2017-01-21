CS4410
======
This is your CS4410 project repository. You will use this repository to develop your code and submit assignments.

## Git
Git is an essential part of this class and we will be using it heavily for all the assignments. If you are not already familiar with Git, we highly suggest trying some [tutorials](https://try.github.io). You will need to install Git on your machine by using either the [Github Desktop](https://desktop.github.com/) app or one of the binaries from [here](https://git-scm.com/downloads).

## Virtual Machine
In order to develop locally, you should use the provided virtual machine to guarantee the environment is identical to our grading environment. To do this, you will need to install [Vagrant](https://www.vagrantup.com/). Once you have installed Vagrant, run `vagrant up` from within your repo directory using Command Prompt if you're on Windows or Terminal if you're on OS X. You can then connect to your VM by running `vagrant ssh` from the same directory. Your repo is automatically shared with the VM so any changes to your files are automatically synced. Once in the VM, you can navigate to the `/home/vagrant/10-P` directory and run your code.

To get started, run the following:

    # To start the VM and connect to it, run the following.
    # You can run `vagrant ssh` multiple times to open multiple terminals
    $ vagrant up
    $ vagrant ssh

    # At this point, you are inside the VM and can compile and test your code which
    # is available in your home directory.
    <vm>$ cd ~/10-P
    <vm>$ <run your code>
    <vm>$ exit

    # To turn off the VM when you're done, run the following
    $ vagrant halt


## Academic Integrity
Students are prohibited from sharing code with anyone that is not in their group or on the course staff. This includes making public forks of your repository or otherwise hosting it in a public location. Students are prohibited from rewriting Git history or otherwise attempting to change tags created by the course staff. We maintain copies of all the repositories and can easily detect when history has been modified (this includes force pushes) and any student found to be in violation of the [academic integrity policy](http://www.theuniversityfaculty.cornell.edu/AcadInteg/) will be reported to the university.
# operating-systems
