# Login - Hackaton 2021

## Creation of virtual environments

### Windows 

Creation of virtual environments is done by executing the command venv:
```
python -m venv venv
```
Once installed, you can activate it as follow :
#### cmd
```
venv\Scripts\activate.bat
```
#### PowerShell
```
venv\Scripts\Activate.ps1
```
You should see (venv) before the path.
Then install Django:
```
python -m pip install Django
```

pour quitter :
deactivate 
dans les deux cas


python
import django
print(django.get_version())

result should be 3.1.5

exit()

python test_installation\django_1.py