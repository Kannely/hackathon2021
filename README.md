# Login - Hackathon 2021

## Clone the repository to your local machine

First, you will have to clone the repository:
```
git clone https://github.com/Kannely/hackathon2021.git
```

Make sure you are on the master branch, otherwise you can change your branch with the following command:
```
git checkout master
```

## Creation of virtual environments

### Windows 

Creation of virtual environments is done by executing the command venv:
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


Creation of virtual environments is done by executing the command venv:
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
