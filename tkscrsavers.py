import sys
import pathlib
import os
import argparse
import json
import importlib
from tkinter import *
from collections import namedtuple
# for preview window routines
import win32gui
# from win32 import win32gui
from screeninfo import get_monitors

import logging
logger = logging.getLogger(__name__)
logname = 'tkscrsavers_log.txt'
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    logname = os.path.join(os.path.expanduser('~'), logname)
else:
    logname = os.path.join(pathlib.Path(__file__).parent.resolve(), logname)
logging.basicConfig(
    filename=logname,
    level=logging.INFO,
    format='[%(asctime)s] (%(module)s:%(levelname)s) %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

# GUI for settings dialog
import tkscrsavgui

# Default settings
app_name = 'Tk-Screensavers'
app_version = '1.2.3'
app_url = 'https://github.com/beotiger'
app_date = '2024-04-01'
app_authors = 'Beotiger & co.'
app_license = 'MIT'

class TkScrSaver:
    def __init__(self, config=False, preview=False, config_handle=0, preview_handle=0, devmode=False):
        """Start screensaver in any mode: preview, config, devmode or mere screensaver.
            When @config is True we open GUI Settings window to edit all modules settings and set up active modules.
            When @preview is True we should prepare window to be shown in Windows(tm) own preview window.
            When @devmode is True we should reread all modules from folder ./screensavers,
                add new modules if they are and renew all modules app_* settings
                (except app_options) in self.scrsavers_settings dict.
                This mode should be used only when we are adding new modules or
                edit app_* settings in existing modules in folder ./screensavers.
                After finishing devmode we should recompile tkscrsavers project (see README.md for details)
            Note that in config mode we can test any module by our own means not depending on Windows(tm) preview ability.
        """
        # Dictionary with global settings for all screensavers
        self.scrsavers_settings = {}
        # And list of all active modules
        self.active_modules = []
        # Order of next screensaver
        self.active_order = 0

        # From: https://pyinstaller.org/en/stable/runtime-information.html
        # Use user home directory for log and settings file if we are in bundled state
        # Settings file name
        self.settings_file = os.path.join(pathlib.Path(__file__).parent.resolve(), 'settings.json')
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            self.settings_exe = os.path.join(os.path.expanduser('~'), 'tkscrsavers.json')
            # If there is no settings file in home directory yet copy it from original settings file
            if not os.path.isfile(self.settings_exe):
                with open(self.settings_file, 'rb') as src, open(self.settings_exe, 'wb') as dst: dst.write(src.read())
            # And use it as main settings file
            self.settings_file = self.settings_exe
        self.prepareSettings(self.settings_file, devmode)
        # Signal when global window closed
        self.alive = True
        self.root = Tk()
        self.root.title(f'{app_name} {app_version} by {app_authors}')
        self.root.geometry('0x0+-100+-100') # Make sure the initial window doesn't show
        self.root.overrideredirect(True) # No window chrome and hide from task bar
        self.root.update_idletasks()
        if config:
            self.Config_Dialog(config_handle)
        elif preview:
            self.handlePreview(preview_handle)
        else:
            self.handleScreenSaver()

    def handlePreview(self, preview_handle):
        hwnd = self.root.winfo_id()
        left, top, right, bottom = win32gui.GetWindowRect(preview_handle)
        Monitor = namedtuple('Monitor', ['width', 'height', 'x', 'y'])
        self.Create_Screen(Monitor((right-left), (bottom-top), left, top), hwnd, preview_handle)

    def handleScreenSaver(self):
        self.root.configure(background='black', cursor='none')
        self.root.bind_all('<Key>', self.close)
        self.root.bind_all('<Motion>', self.close)
        for monitor in get_monitors():
            self.Create_Screen(monitor)

    def close(self, evt=None):
        self.alive = False
        self.root.destroy()

    def Config_Dialog(self, config_handle):
        width = 592
        height = 450
        self.win = Toplevel(self.root)
        self.win.title(f'{app_name} {app_version} - Settings')
        self.win.iconbitmap(os.path.join(pathlib.Path(__file__).parent.resolve(), 'tkscrsvr.ico'))
        # @2024_03_05_1217 center window
        wx = (self.root.winfo_screenwidth() - width) // 2
        wy = (self.root.winfo_screenheight() - height) // 2
        ge = f'{width}x{height}+{wx}+{wy}'
        self.win.geometry(ge)
        # self.win.resizable(True, True)
        self.win.update_idletasks()
        self.win.protocol('WM_DELETE_WINDOW', lambda: self.close())
        tkscrsavgui.Toplevel1(self.win, self.scrsavers_settings, self.settings_file)

    def Create_Screen(self, monitor, root_handle=0, preview_handle=0):
        # def __init__(self, root, monitor, root_handle=0, preview_handle=0):
        self.monitor = monitor
        self.win = Toplevel(self.root)
        self.win.update_idletasks()
        self.win.attributes('-topmost', True)
        self.win.overrideredirect(True)
        pos = f'{self.monitor.width}x{self.monitor.height}+{self.monitor.x}+{self.monitor.y}'
        if preview_handle > 0:
            win32gui.SetParent(root_handle, preview_handle)
        self.win.geometry(pos)
        # Start screensaver from first module in order
        l = len(self.active_modules)
        # If we have at least 1 active module to run
        if l:
            name = self.active_modules[self.active_order]['name']
            opts = self.active_modules[self.active_order]['options']
            timer = 0 if l == 1 else self.active_modules[self.active_order]['timer']
            logger.debug(f'Starting screensaver {name}, order: {self.active_order}, timer: {timer}')
            # Run next module in order when window destroyed
            if timer:
                # self.win.unbind_all('<Destroy>')
                self.win.bind('<Destroy>', self.nextModule)
            # mmm = __import__(name)
            mmm = importlib.import_module('.' + name, 'screensavers')
            mmm.TkScreenSaver(self, opts, timer)
        else:
            # No module is active - just quit peacefully
            self.close()

    def nextModule(self, evt):
        """Run next module in order"""
        logger.debug(f'Running nextModule: self.alive={self.alive}, active_order={self.active_order}')
        logger.debug('Widget: %s, type(widget)=%s', evt.widget, type(evt.widget))
        if self.alive and evt.widget is self.win:
            self.active_order += 1
            if self.active_order >= len(self.active_modules): self.active_order = 0
            self.Create_Screen(self.monitor)

    def getModulesList(self):
        """Find all screensavers modules names and return its names as a list"""
        # scrsvr_modules = ['boids', 'saveoclock', 'starwars', 'rain', 'matrix', 'steering']
        scrsvr_modules = []
        dir = os.path.join(pathlib.Path(__file__).parent.resolve(), 'screensavers')
        for module in os.listdir(dir):
            if module != '__init__.py' and module != '_skeleton.py' and module[-3:] == '.py':
                scrsvr_modules.append(module[:-3])
        return sorted(scrsvr_modules)

    def getJsonSettings(self, settings_file):
        """Get global settings from user file to self.scrsavers_settings variable"""
        logger.info(f'Looking for settings file {settings_file}...')
        if os.path.isfile(settings_file):
            try:
                with open(settings_file) as fd:
                    self.scrsavers_settings = json.load(fd)
                logger.info('Settings read successfully!')
                return True
            except:
                logger.warning('Failed reading settings')
        else:
            logger.warning('Settings file is not found. Enabling devmode...')
        return False

    def prepareSettings(self, settings_file, devmode):
        """Global settings for all previously loaded modules.
            If there is no settings_file available force @devmode
            to create these settings dynamically"""
        if not self.getJsonSettings(settings_file): devmode = True
        # When in devmode reread main app_* settings from available modules
        # and add new modules if they are
        if devmode:
            logger.info('Using development mode!')
            scrs_list = self.getModulesList()
            for name in scrs_list:
                module = importlib.import_module('.' + name, 'screensavers')
                main_sets = {
                    'title': module.app_name,
                    'version': module.app_version,
                    'url': module.app_url,
                    'date': module.app_date,
                    'license': module.app_license,
                    'authors': module.app_authors
                }
                # Determine if we loaded this modules first time
                if name not in self.scrsavers_settings:
                    # Default module options
                    main_sets['options'] = module.app_options
                    main_sets['order'] = 0
                    # This option is not used yet
                    main_sets['hidden'] = 0
                    # Timer when we change scrsaver in multi-mode, in seconds
                    main_sets['timer'] = 30
                    # Store new module name with all its options in global settings
                    self.scrsavers_settings[name] = main_sets
                else:
                    # Refresh main module settings every run
                    for key, val in main_sets.items():
                        self.scrsavers_settings[name][key] = val
        # @2024_03_28_1846 Form list of active moules in given order
        self.active_modules.clear()
        for name in self.scrsavers_settings:
            if self.scrsavers_settings[name]['order']:
                self.active_modules.append({
                    'name': name,
                    'order': self.scrsavers_settings[name]['order'],
                    'timer': self.scrsavers_settings[name]['timer'],
                    'options': self.scrsavers_settings[name]['options']
                })
        if len(self.active_modules):
            self.active_modules = sorted(self.active_modules, key=lambda d: d['order'])
        logger.debug(f'Sorted active modules: {self.active_modules}')

def getArgs():
    """
        Screensaver command-line arguments.
        https://docs.microsoft.com/en-us/troubleshoot/windows/win32/screen-saver-command-line
    """
    parser = argparse.ArgumentParser(description='Running the application with no arguments shows the Settings dialog.', prefix_chars='/')
    g = parser.add_mutually_exclusive_group()
    g.add_argument('/c', '/C', help='Show the Settings dialog box, modal to the foreground window.', nargs='*')
    g.add_argument('/p', '/P', help='Preview Screen Saver as child of window <HWND>.', metavar='<HWND>', nargs=1, type=int)
    g.add_argument('/s', '/S', help='Run the Screen Saver.', action='store_true')
    g.add_argument('/d', '/D', help='Use development mode.', action='store_true')
    logger.info('Program starts with parameters: %s', str(sys.argv))
    return parser.parse_args()

def main():
    """
        Available options:
            /h    - show help message
            /d /D - development mode on - used only in config settings
            /p /P - Windows(tm) own preview mode
            /s /S - Start screensaver
            /c /C - Open config settings with config_handle
        If no option is set just open config settings.
        Also see getArgs function above.
    """
    args = getArgs()
    devmode = args.d
    if args.c or (not args.c and not args.p and not args.s):
        config_handle = int(args.c[0][1:]) if args.c else 0
        w = TkScrSaver(config=True, config_handle=config_handle, devmode=devmode)
    if args.p and args.p[0] > 1:
        w = TkScrSaver(preview=True, preview_handle=args.p[0])
    elif args.s:
        w = TkScrSaver()
    w.root.mainloop()

if __name__ == '__main__':
    main()
