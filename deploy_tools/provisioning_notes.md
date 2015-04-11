Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3
<<<<<<< HEAD
* Git
=======
* Git 
>>>>>>> 05a051d000409e1027d61ea4554ae60cb5b6817f
* pip
* virtualenv

eg, on AWS EC2:

<<<<<<< HEAD
    wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz
    tar zxvf Python-3.4.2.tgz
    cd Python-3.4.2
    sudo yum install gcc
    ./configure --prefix=/opt/python3
    make
    sudo yum install openssl-devel
    sudo make install
    sudo ln -s /opt/python3/bin/python3 /usr/bin/python3
=======
	wget https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz
	tar zxvf Python-3.4.2.tgz
	cd Python-3.4.2
	sudo yum install gcc
	./configure --prefix=/opt/python3
	make
	sudo yum install openssl-devel
	sudo make install
	sudo ln -s /opt/python3/bin/python3 /usr/bin/python3
>>>>>>> 05a051d000409e1027d61ea4554ae60cb5b6817f

## Upstart job

* see gunicorn-upstart.template.conf
*replace SITENAME with, eg, staging.my-domain.com

## Folder structure:
Assume we have a user account at /home/username

/home/username
└── sites
    └── SITENAME
         ├── database
         ├── source
         ├── static
         └── virtualenv
