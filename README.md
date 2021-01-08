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

When you are done, you can leave the virtual environment with the command:
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
python test_installation/django_1.py
```
You should see a version number, such as ```3.1.5``` .

To run the app, use:
```
cd squelette
python manage.py runserver
```

When you are done, you can leave the virtual environment with the command:
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

# Utilisation

## Once the server is launched :

#### To access the front-end's index, append ```/front``` at the end of the hostname - for instance, if deployed locally, the hostname is ```localhost```.
#### Similarly, to access the back-end's index, append ```/back``` at the end of the hostname.

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

### Instructions

Before proceeding, make sure that you have access to a Scalingo account and that you have successfully generated the database locally, as Scalingo cannot generate the database on its own. Also make sure that you have a public SSH key : first check if you already have one (https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/checking-for-existing-ssh-keys ), and if you don't generate one (https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key ).

First of all, at the root of the project (which contains this ```README.md``` file), copy the ```squelette``` folder to a folder outside of the project.

On the web dashboard of Scalingo, create a new app with a name (note down the hostname, as it will be used later), and give your public SSH key. For the database, choose ```PostGreSQL``` - we will not use it, but we have to select it regardless. **Don't use the commands provided by Scalingo yet.**

Then, in your app, go to the ```Environment Variables``` tab and do the following :
 - Add this line : ```DISABLE_COLLECTSTATIC=1```
 - Add this line, **by appending to it the hostname given to you by Scalingo earlier** : ```ALLOWED_HOSTS=```
 - Remove the line which starts with ```DATABASE_URL```
Don't forget to click the ```Update``` button to save the changes.

Finally, in the terminal, with Git installed, inside the copied folder (normally, there should be a ``manage.py``` file in your current working directory), run the following commands :
```
git init
git add .
git commit -m "Init Django application"
```

Finally, run the 2 commands shown on your ```Code``` page.

### Example

The branch ```main``` is deployed on Scalingo at the following link : http://hack-scalingo.klethuillier.fr/

(To access the front-end : http://hack-scalingo.klethuillier.fr/front )
