# Login - Hackathon 2021


## Install



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
Result should be ```3.1.5``` .

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
