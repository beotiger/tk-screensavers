# PIPENV usage workflow

## Prelude

There is [pipenv](https://pypi.org/project/pipenv/) - handy utiliy to utilize process of creating/deactivating virtual environments and installing packages/dependencies for `Python`. And we will use namely `pipenv` for our project why not.

## Make sure you have python and pip

To use `pipenv` we must be sured that we have `Python` and `pip` at our disposal.

Use following commands and see exptected results. Version numbers may be different by time and system but should work anyway.

```sh
python --version
Python 3.12.2

pip --version
pip 24.0 from C:\Python312\Lib\site-packages\pip (python 3.12)
```

Then install pipenv if you do not have done it yet.

## Install pipenv

```sh
pip install --user pipenv
```

Also we should point `VS Code editor` to use appropriate interpretator (`F1` - `Python: Select Interpreter`) to run our `Python` scripts with `pipenv` so that it have access to concrete path and can use intellisense to find all needed dependencies.

After successful installing `pipenv` run this command:

```sh
d:\git\2024\tk-screensavers>pipenv install --dev
Creating a virtualenv for this project...
Pipfile: D:\git\2024\tk-screensavers\Pipfile
Using C:/Python312/python.exe (3.12.2) to create virtualenv...
[  ==] Creating virtual environment...created virtual environment CPython3.12.2.final.0-64 in 454ms
  creator CPython3Windows(dest=D:\git\2024\tk-screensavers\.venv, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, via=copy, app_data_dir=C:\Users\beoti\AppData\Local\pypa\virtualenv)
    added seed packages: pip==24.0
  activators BashActivator,BatchActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator

Successfully created virtual environment!
Virtualenv location: D:\git\2024\tk-screensavers\.venv
Pipfile.lock not found, creating...
Locking [packages] dependencies...
Building requirements...
Resolving dependencies...
Success!
Locking [dev-packages] dependencies...
Updated Pipfile.lock (29bb59db7223d10ee465538a242a01b446f3b18d1e586e8379ac33dd308af192)!
Installing dependencies from Pipfile.lock (8af192)...
Installing dependencies from Pipfile.lock (8af192)...
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

The previous command tells `pipenv` to install all depenencies needed for our project.

And from now on you can use it in your daily work flow under the project.

Or you can use VS Code the same - just select appropriate `Python interpreter` through command pallette (`F1` - `Python: Select Interpreter`)


## Daily usage

To start main application run:

```sh
pipenv run python tkscrsavers.py /d
```

Command option /d tells tkscrsavers.py to check all modules in `screensavers` folder, add new ones to available list and refresh common app settings such as `app_name`, `app_version`, `app_url`, `app_date` and `app_authors`.

`app_options` won't be affetcted by this option to preserve your options intact. If you want to load default module options use "Load default options" button in Settings GUI.

If you did not any changes in `screensavers` folder you may start application without any command options.

It will open Settings GUI to deal with screen savers - you can add, remove, mix and reorder active modules, set timers individually for each module which tells in seconds how long this module will be working until next one, and change options for each module.

There is button `Test` to test and play with module in windowed mode.

Note. If you use only one module for screensaver the timer has no effect for as a rule screensaver should work until any key pressed or mouse moved or computer fall asleep under some circumstances.

To test main application in screensaver mode run:

```sh
pipenv run python tkscrsavers.py /s
```

This should start application in full screen mode and use all active modules with its timers until you press any key on your keyboard or move your mouse on your table. Or spill some coffee on your monitor in awe ;)

We can use this whole thing as a demo scene! Please take this into consideration.

To test each module individually we can use this command:

```sh
pipenv run python screensavers/boids.py
```

to start Boids for example. Or to start Steering:

```bash
pipenv run python screensavers/steering.py
```

and so on. That's it.

Also we can use `VS Code editor` to run any `.py` script from it. See section `VS Code` in [README.md](README.md) file.

## Date

@2024_04_04_1233 by Beotiger from Tzaritzyn
