
# Acknowledgement

First of all let me acknowledge one project at Github [Save-O-Clock](https://github.com/Ex-iT/save-o-clock) from which this project has been arose. As I assume `Save-O-Clock` is mostly like a sample application to write screensavers for Windows(tm) using Python/Tkinter, and that's the goal of whole this project - Tk Screensavers.

Why have I chosen Save-O-Clock? Hmmmmm, I just downloaded it, learned a bit code and compiled it as was written in its `README.md` file. And in a couple of minutes I got a real working screensaver which I could install and use in my `Windows(tm) 10` system as I've always wished.

# Fast start [2025_02_15]

If you do not wish to dive deep into all this stuff just run these several commands to have screeen savers in your Windows(tm) system.

`Note`. You should have `python` and `pip` binaries installed on your system.

```sh
git clone https://github.com/beotiger/tk-screensavers.git
cd tk-screensavers
pip install --user pipenv
pipenv install --dev
build
install
```

Then right click somewhere on empty part of your Desktop, choose `Personalize` from drop-down menu, find section `Lock screen` and link `Screen saver settings`.
Choose `tkscrsavers` from the list and click button `Apply`!

Hope this works as fine for you as it works for me!

# Tk Screensavers - prelude

It is a project to make and use screensavers for `Windows(tm)` particularly. Note `s` at the end of word `screensavers` - that is. I wanted not just write one screensaver and use it as usual, but have a bunch of customizable screensavers that could be easily written in `Python` language and used anywhere on `Windows(tm)` systems in order to form a large neverending animation cycling on your desktop while you speak on your phone or drink a cup of coffee.

And this project - [Tk Screensavers](https://github.com/beotiger/tk-screensavers) - let you do this!

# Adding your own screensaver

All screensavers (we call it modules mostly from now on) are located in subfolder `screensavers`. So all what is needed is to put a Python module in there, run `tkscrsavers.py` with option /d (for development mode) and it will find and add new module into available screensavers list and show Settings dialog (GUI). After that we can set some options if needed then save and close settings dialog after which we can recompile and use our new screensaver along with others.

But there are several points to consider - new screensaver should abide to some rules to be compatible with tkscrsavers.py modules.

One sane step is to use special module called `_skeleton.py` in `screensavers` folder, copy it under any other unique name and use it as a starting point for a new screensaver. All common steps to do it are described in this file (`_skeleton.py`).

See page [README_savers.md](README_savers.md) for how screensavers look like and what options they have.

# Tkinter Tcl/Tk

All modules in `screensavers` folder use [Python tkinter](https://docs.python.org/3/library/tkinter.html) module to draw animation mostly on its `Canvas` (aside from `saveoclock` app which uses Frame and Label widgets to animate its text). `Canvas` let us draw primitives such as lines, ovals, arcs, polygons and rectangles along with textes, images, bitmaps and other windows. More of this can be found online anywhere, one or two links are:

[tutorial](https://tkdocs.com/tutorial/canvas.html)
[plus2net.com](https://www.plus2net.com/python/tkinter-canvas.php)
[shipman/canvas](https://tkdocs.com/shipman/canvas.html)

Or you can use any `tkinter` widgets for your purposes of course.

## Why Tkinter?

Tkinter itself is a part of `Python` built-in modules and as `Python` [official documentation](https://docs.python.org/3/library/tkinter.html) states:

*The tkinter package (“Tk interface”) is the standard Python interface to the Tcl/Tk GUI toolkit. Both Tk and tkinter are available on most Unix platforms, including macOS, as well as on Windows systems.*

## PyGame?

Personnaly I do think about using for example [PyGame](https://www.pygame.org) coupled with [PyOpenGL](https://pyopengl.sourceforge.net/) to get faster animation and more grained control over the screen to create awesome beautiful brilliant screen savers. We will see if we can do this. May be can may be not. Who knows?

## Arcade Screen Saver Framework

There is also [Arcade](https://github.com/pythonarcade/arcade) based `Python` framework that allows you to write official Windows screen savers using `Python` and `Arcade` - [Arcade Screen Saver Framework](https://github.com/SirGnip/arcade_screensaver_framework) as its own `README.md` file states.

I tried it one time but could not get it working on my system with current `Python 3.12` installation and dependencies versions which became incompatible with each others. It is not so lightweighted application also with too many additional packages/dependencies which I do not like much personnaly. So be it (sigh).

# Testing

## pipenv

See [README_pipenv.md](README_pipenv.md) file for detailed instructions using `pipenv`.

Run this command:

```bash
pipenv install --dev
```

It should install required packages `pywin32`, `screeninfo` and `pyinstaller` in virtual environment under `.venv/` folder.

If something goes wrong you can try to delete `Pipfile.lock` file and try the previous command again.

Then we can use `pipenv` every time for our project.

To start main application run:

```bash
pipenv run python tkscrsavers.py /d
```

Command option `/d` tells `tkscrsavers.py` to check all modules in `screensavers` folder, add new ones to available list and refresh common app settings such as `app_name`, `app_version`, `app_url`, `app_date`, `app_authors` and `app_license`.

`app_options` won't be affetcted by this option to preserve your options intact. If you want to load default module options use `"Load default options"` button in Settings GUI.

If you did not any changes in `screensavers` folder you may start application without any command options.

It will open Settings GUI to deal with screen savers - you can add, remove, mix and reorder active modules, set timers individually for each module which tells in seconds how long this module will be working until next one, and change options for each module.

There is button `Test` to test and play with module in windowed mode.

Note. If you use only one module for screensaver the timer has no effect for as a rule screensaver should work until any key pressed or mouse moved or computer fall asleep under some circumstances.

See page [README_GUI.md](README_GUI.md) for more information about its using.

To test main application in screensaver mode run:
```bash
pipenv run python tkscrsavers.py /s
```

This should start application in full screen mode and use all active modules with its timers until you press any key on your keyboard or move your mouse on your table. Or spill some coffee on your monitor in awe ;)

We can use this whole thing as a demo scene! Please take this into consideration.

To test each module individually we can use this command:

```bash
pipenv run python screensavers/boids.py
```

to start Boids for example. Or to start Steering:

```bash
pipenv run python screensavers/steering.py
```

and so on.

# Standalone application - executable for Windows(tm)

To build a standalone executable (`exe` file which can be runned on any Windows(tm) machine without `Python` itself and without any dependencies) we use [PyInstaller](https://www.pyinstaller.org/).

If you use `pipenv` as it was recommended above, `pyinstaller` application should be in your virtual environment.

If you do not use `pipenv` then edit `build.bat` file to delete pipenv call in it: `pipenv start`

## Onefile installation

Just run `build.bat` which do all job under the hood for you using prepared `tkscrsavers.spec` file.
Note that it should add all modules - old and new ones - from folder `screensavers` which are used as screensavers for Windows(tm) system due to hidden imports used in `.spec` file.

```powershell
build.bat
```

It will create the two executables in folders ./dist: `tkscrsavers.exe` and `tkscrsavers.scr`. .exe file can be used for editing settings and .scr file used for direct testing screensaver(s). Also .scr file can be installed indirectly as a screensaver (see below). To install it permanently for screensaver role run install.bat:

```powershell
install.bat
```

It will ask you for elevated privileges and copy `tkscrsavers.scr` file into Windows(tm) system folder for screensavers, i.e. to `C:\Windows\System32` folder where all `.scr` files serve as screensavers.

Now you can use tkscrsavers as usual screensaver utility for `Windows(tm)`, i.e. choose it in Screen saver settings (System Settings -> Personalization -> Lock screen -> Screen saver settings), edit its Settings and run Preview in screensavers modal window made by Windows(tm).

But it has its disadvantage - for more grown file size which takes a while while starting the whole application.


## Onedir installation

To make lower in file size and speed up its starting you may find more appropriate to create onedir installation instead of onefile.

Run next command:

```powershell
build_onedir.bat
```

It will create the whole application in folder dist\tkscrsavers\ using prepared `tkscrsavers_onedir.spec` file. If you use your explorer to navigate there you will find two files - `tkscrsavers.exe` and `tkscrsavers.scr`. Use the first one (`.exe`) to start Settings GUI to organize screensavers and the second one (`.scr`) to test them in real world. The `.scr` file Windows(tm) system runs with `/s` option automatically to start it as screensaver.

Also you can install `tkscrsavers.scr` to use it as a system screensaver - right click on it in explorer and choose `Install` option from context menu which should appear at any `.scr` file. After this `Windows(tm)` shows its Screensavers modal window where you can change screensavers options too and set timer under `Wait` field to indicate when screensaver should start after you leave your computer intact for a while.

Onedir installation has its own disadvantages too: it cannot be installed directly into `C:\Windows\System32` folder and when you run Windows(tm) screensaver settings directly and choose and apply another screensaver the previous installation of `tkscrsavers` can disappear so that you must install it again from its folder as it is shown above.

And when you need to delete this whole project from your hard drive you need to save `./dist` folder anywhere in some place if you want to use it as a system screensaver onward.

When onefile installation should always be available for you in `C:\Windows\System32` folder.

# Using screensaver(s) on Windows(tm)

**Important note.** On some `Windows(tm)` systems the Screensavers ability would be blocked for no reason. When such a case you can not change global screensavers options for they will be disabled by the system.

To remedy this you should do several following steps:

1. Press `Win+R` to open the `Run` command dialog box.
2. Type `gpedit.msc` and press `Enter` to open the `Local Group Policy Editor` (LGPE).
3. Navigate to `User Configuration` > `Administrative Templates` > `Control Panel` > `Personalization`.
4. Double-click on the `Enable screen saver` option on the right-hand side.
5. Check the `Enabled` box on the next screen.
6. Click `Apply` and then click `OK`.
7. Close all windows.

From now on screensavers should be enabled for you. If not ask `William W. Gates` why they are not there (it's a joke) ;).

To check screensavers from system wide:

1. Open Windows(tm) `System Settings`.
2. Click on `Personalization`.
3. Click on `Lock screen`.
4. Click the `Screen saver settings` link.

Note that when you use these steps our `tkscrsavers` screensaver can disappear from global screensavers list.
Or it can disappear from there for no reason - if we did not use install.bat script to copy onefile installation in `C:\Windows\System32` folder. In such a case we should install it again. To do this just explore your `.\dist\tkscrsavers` folder, right click on `tkscrsavers.scr` file, choose `Install` option and `OK` button then. Our screensaver should be active then again.

To ensure which is the current screensaver set in your system right now you can run the following command from console or through `Win+R` key combination using [Miscrosoft(tm) Powershell](https://en.wikipedia.org/wiki/PowerShell):

```powershell
powershell.exe -command "& (Get-ItemProperty 'HKCU:Control Panel\Desktop').{SCRNSAVE.EXE}"
```

It should launch current screensaver immediately.

# Folder structure and common files

## settings.json (tkscrsavers.json), tkscrsvr.ico, MS Mincho.ttf, tkscrsavers_log.txt

All modules settings are placed in file **settings.json** in [JSON](https://www.json.org/json-en.html) format.
Its name is **tkscrsavers.json** in current user home directory when compiled/installed version of `tkscrsavers.py` used.

It has the following structure:

```json
{
"module1":
    {
    "title": "App title",
    "version": "App version",
    "url": "App url",
    "date": "App date",
    "authors": "App author(s)",
    "license": "MIT",
    "options":
    {
        "background": "black",
        "option2": ["#FFF", "#F8F", "#F2F"],
        "option3": 123,
        "option4": 3.1415,
        /* ... */
        "optionN": "Str Value"
    },
    "order": 2,     /* Order of module in active modules */
    "hidden": 0,    /* Not used currently. Wanted to hide/unhide modules from available list */
    "timer": 120    /* Timer to trigger next module in queue (in seconds) */
    },
"module2":
    {
        /* ... */
    },
/* etc. */
}
```

Also there is an `ico` file representing an icon for application GUI (`tkscrsvr.ico`) and font file `MS Mincho.ttf` which is used by `crazychars.py` and `matrix.py` modules and is available on any `Microsoft Windows(tm)` system along with all its fonts.

When application is frozen by `onedir` installation (i.e. bundled by `pyinstaller` through `onedir` variant) all these files are avalailable in folder `.\dist\tkscrsavers\_internal` for read and write.

**tkscrsavers_log.txt** keeps all log messages from `tkscrsavers.py` and `tkscrsavgui.py` and can be removed any time peacefully. It is located in current user home directory when we use compiled/installed version of `tkscrsavers.py`.

## Extra files for this project

`.vscode` - folder for inner VS Code settings if any and file `launch.json` for launching `.py` files from `VS Code editor`.

`.gitignore` - to list files and folders that are not to be processed by `Git` while comitting.

`build.bat` - Windows(tm) batch file to compile `*.py` files into one project under `.\dist\` folder. Use it when you changed something in `*.py` code and/or added new modules into `screensavers` folder. When you add modules into `screensavers` folder do not forget to run `tkscrsavers.py` with `/d` parameter to add theses new modules into available modules list.

`install.bat` - run this file to copy `tkscrsavers.scr` file from .\dist folder to `C:\Windows\System32` folder where system can ever it found as its screensaver.

`MS Mincho.ttf` - this font is for `matrix.py` module. This font should be available in your Windows(tm) system for free any way and is there only for some hidden purposes. See [MS Mincho.ttf](https://learn.microsoft.com/en-us/typography/font-list/ms-mincho) for details regarding this font.

`Pipfile` - do not know what is it yet. But have some clues)

`settings.json` - all screensavers settings used when testing and running modules from development project. It will we in `.\dist\tkscrsavers\_internal` folder after project compiling in `onedir` variation, as mentioned above. Or it is named as `tkscrsavers.json` in current user home folder when we use compiled/installed version of `Tk Scrsavers` application!

`tkscrsavers_log.txt` - log file for testing

`tkscrsavers.spec` - .spec file for `pyinstaller` to compile whole project into independent Windows(tm) executable application. See some notes above about it.

`tkscrsavers_onedir.spec` - like `tkscrsavers.spec` but it is used for `onedir` installation (see above).

`tkscrsvr.ico` - ICO file 32x32 pixels in size to use as a main icon for Settings GUI application and can be used by any module.

## Source project files

`tkscrsavers.py` - main project file to run screensavers themselves and Settings GUI.
`tkscrsavgui.py` - Settings GUI to edit modules settings and add/remove them to/from available modules list. Can be run by itself.
`tooltip.py` - helper module used by `tkscrsavgui.py` to show tooltips for some widgets.

## Folder screensavers

Folder `screensavers` serves to hold all screensavers as `Python` modules. You can add new module there to use it along with other modules. Copy `_skeleton.py` file, change its name and use it as a starting point to create your new brand stunning amazing awesome great terrific screensaver.

After changing something there do not forget to run `tkscrsavers.py` with `/d` parameter to add new modules into available modules list and refresh some options such as `app_name`, `app_version` etc. for each module.

# Using Visual Studio Code

This project was mostly build with the help of [Visual Studio Code](https://code.visualstudio.com/).

There is file `launch.json` in `.vscode` folder which helps us to run any `.py` module with `F5` button.

You should ensure that you are using appropriate `Python` interpreter when open project in VS Code first time. Press `F1` to open `Command Palette` and find `Python: Select Interpreter` command and choose the one that points to virtual environment chosen for this project. After this step this option will be stored in `VS Code` settings and you will not need to do this again.

There is setting to ask you to enter command option(s) when you run a `.py` module. Just hit `Enter` after `F5` each time to skip this step.

To test screensaver work navigate to `tkscrsavers.py` in VS Code explorer, press `F5`, type `/s` and hit `Enter`.

To use development mode after changing files in `screensavers` folder use `/d` option when launching `tkscrsavers.py`. There is no need to use `/d` option every time.

Also you can test any module in `screensavers` folder. Just navigate to it, press `F5` and `Enter` to launch.

# PAGE - Python Automatic GUI Generator

Settings GUI in `tkscrsavgui.py` base was built by [PAGE](https://page.sourceforge.net/) version 8.0 in conjunction with `Tcl` version 8.6. `PAGE` tends to become great program with several disadvantages nontheless which we can be used to eventually. After it's job we need to do some code trimming and aligning. Never mind it is a great tool any way. In my humble opinion, of course.

# Dates and versions of tools

This project was built on March-April 2024.

The version of Windows(tm) and other system global tools these days:

## Windows(tm)
```bash
ver

Microsoft Windows [Version 10.0.19045.4170]
```

## Python
```bash
python -V
Python 3.12.2
```

## Pip
```bash
pip -V
pip 24.0 from C:\Python312\Lib\site-packages\pip (python 3.12)
```

## Pipenv
```bash
pipenv --version
pipenv, version 2023.12.1
```

## Tkinter
```bash
python -m tkinter
This is Tcl/Tk 8.6.13
```

Any other tools versions should be up to date in virtual environment that you use.
Note. `pipenv` can use any `Python` version that your wish but we tend to use the latest one by now.
Also `pipenv` use `pip` under the hood - do not know why I wrote it down there. Never mind.

## Visual Studio Code version information
```
Version: 1.87.2 (user setup)
Commit: 863d2581ecda6849923a2118d93a088b0745d9d6
Date: 2024-03-08T15:20:17.278Z
Electron: 27.3.2
ElectronBuildId: 26836302
Chromium: 118.0.5993.159
Node.js: 18.17.1
V8: 11.8.172.18-electron.0
OS: Windows_NT x64 10.0.19045
```

## Visual Studio Code extensions
```bash
code --list-extensions
```

These are extentions I want to highlight above others:

```bash
alefragnani.bookmarks
alefragnani.numbered-bookmarks
alefragnani.project-manager
alefragnani.read-only-indicator
alefragnani.separators

bmewburn.vscode-intelephense-client
christian-kohler.path-intellisense
dbaeumer.vscode-eslint
esbenp.prettier-vscode

fabiospampinato.vscode-highlight

formulahendry.auto-close-tag
formulahendry.auto-complete-tag
formulahendry.auto-rename-tag

ibm.output-colorizer

jsynowiec.vscode-insertdatestring
kamikillerto.vscode-colorize

ms-python.black-formatter
ms-python.debugpy
ms-python.isort
ms-python.pylint
ms-python.python
ms-python.vscode-pylance

naumovs.color-highlight

ryu1kn.text-marker
shardulm94.trailing-spaces

visualstudioexptteam.vscodeintellicode-completions
```

# Good bye and see you later

Thank you for using this software and for your attention on the project.

Sincerely Yours,
Beotiger & co.
@2024_04_03_0956

# P.S. Big money here

Let's make a lot of money. Acknowledgments, credits, many thanks and a couple of tea/coffee/cacao cups.
