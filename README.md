# Login - Hackathon 2021

# Installation

## Clone the repository to your local machine

First, you will have to clone the repository:
```
git clone https://github.com/Kannely/hackathon2021.git
```

Make sure you are on the master branch, otherwise you can change your branch with the following command:
```
git checkout master
```

Also check that you have Python 3 with a version above 3.6.

## Creation of virtual environments

### Windows 

To create a virtual environment for the project, run the following command:
```
python -m venv venv
```
Once installed, you can activate it as follows:
* Command Prompt
```
venv\Scripts\activate.bat
```
* PowerShell
```
venv\Scripts\Activate.ps1
```
You should see ```(venv)``` before the path.

In the virtual environment, install Django:
```
python -m pip install Django
```

To test if the installation went well, execute:
```
python test_installation\django_1.py
```
You should see a version number, such as ```3.1.5``` .

To run the app, use:
```
cd squelette
python manage.py runserver
```

When you are done you can leave the virtual environments with the command:
```
deactivate
```

### Linux 

Before proceeding, make sure that virtual environments can be created on your system. You may need to install an additional package before being able to, such as ```python3-venv``` on Debian-based systems.

To create a virtual environment for the project, run the following command:
```
python3 -m venv venv
```
Once installed, you can activate it as follows:
```
source venv/bin/activate
```

In the virtual environment, install Django:
```
pip install django
```

To test if the installation went well, execute:
```
python test_installation\django_1.py
```
You should see a version number, such as ```3.1.5``` .

To run the app, use:
```
cd squelette
python manage.py runserver
```

When you are done you can leave the virtual environments with the command:
```
deactivate
```

## Initialisation of the database

Note : this is not necessary if the ```db.sqlite3``` already exists in the project folder.

First of all, the database needs to be initialized. To do so, run:
```
python manage.py migrate
```

To create a superuser which can access the admin panel, use:
```
python manage.py createsuperuser
```
Follow the instruction by choosing a username and a password (you can leave a blank e-mail address if you want).

# Development

## Updating the database's model

When modifying ```backend/models.py``` file, it is necessary to run a few commands to apply the modifications to the database. Run both commands:
```
python manage.py makemigrations backend
python manage.py migrate
```

Note : the process may not be straightforward if the changes in the database are non-trivial to adapt. In such cases, it is necessary to make manual adjustements.

# Deployment

## Scalingo

The branch ```master``` is deployed at the following link : https://hack-squelette.osc-fr1.scalingo.io/
