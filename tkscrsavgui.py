"""
Options GUI settings for tkscrsavers.py
GUI module generated by PAGE version 8.0
 in conjunction with Tcl version 8.6
   Mar 23, 2024 12:45:34 AM +03  platform: Windows NT
@2024_03_24_2054-2024_03_30_1930 adapted by Beotiger
"""

import pathlib
from os import path
import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter.colorchooser import askcolor
import platform
import importlib
import random
# To open application link in web browser
import webbrowser
# @2024_03_29_2135 for tooltips - may be changed?
# from idlelib.tooltip import Hovertip
import tooltip

import logging
logger = logging.getLogger(__name__)

# Main app to deal with screensavers - this should be ran from that)
import tkscrsavers

class Toplevel1:
    """This class configures and populates the toplevel window.
        top is the toplevel containing window."""
    def __init__(self, top, scrsavers_settings, settings_file):
        top.minsize(120, 120)
        top.maxsize(1924, 1061)
        # Store global settings
        self.settings = scrsavers_settings
        self.settings_file = settings_file
        self.top = top
        self.combobox = tk.StringVar()
        self.comboNewbox = tk.StringVar()
        self.listbox = tk.StringVar()
        self.timer = tk.IntVar()
        self.timer.trace_add('write', self.spinbox)

        style = ttk.Style()
        if platform.system() == 'Windows':
            style.theme_use('xpnative')
        else:
            style.theme_use('alt')
        style.configure('CenterButton.TButton', anchor=CENTER)
        style.configure('Treeview.Heading', background='gray', font=('Times New Roman', 11, 'bold'))

        # style.configure('.', font = 'TkDefaultFont')
        # @2024_03_23_1028 font for system labels
        self.lblsysfont = '-family {Segoe UI} -size 9'
        # font for info labels
        self.lblinffont = '-family {Times New Roman} -size 12'

        self.TOptions = ScrolledTreeView(self.top)
        self.TOptions.configure(columns=('Name', 'Value'), displaycolumns=(0, 1), show='headings')
        self.TOptions.heading('Name', text='Name', anchor="center")
        self.TOptions.column('Name',width=75,minwidth=20,stretch=True,anchor='w')
        self.TOptions.heading('Value', text='Value', anchor="center")
        self.TOptions.column('Value',width=155,minwidth=20,stretch=True,anchor='w')
        self.TOptions.place(relx=0.473, rely=0.244, relheight=0.509, relwidth=0.49)
        # Mouse double click ans Enter key press
        self.TOptions.bind('<Double-Button-1>', self.treeview)
        self.TOptions.bind('<Return>', self.treeview)
        self.TButton8 = ttk.Button(self.top, text='Load default options', style='CenterButton.TButton', command=self.loadDefOpts)
        self.TButton8.place(relx=0.74, rely=0.178, height=28, width=130)
        self.TLabel3 = ttk.Label(self.top, text='Module options')
        self.TLabel3.configure(font="-family {Times New Roman} -size 14 -weight bold")
        self.TLabel3.place(relx=0.473, rely=0.178, height=27, width=130)

        self.TLabel5 = ttk.Label(self.top, font=self.lblsysfont, text='Title', anchor=CENTER)
        self.TLabel5.place(relx=0.3, rely=0.04, height=17, width=140)
        self.TLabel6 = ttk.Label(self.top, font=self.lblsysfont, text='Version')
        self.TLabel6.place(relx=0.541, rely=0.04, height=17, width=53)
        self.TLabel7 = ttk.Label(self.top, font=self.lblsysfont, text='Date')
        self.TLabel7.place(relx=0.659, rely=0.04, height=17, width=90)
        self.TLabel8 = ttk.Label(self.top, font=self.lblsysfont, text='Author(s)')
        self.TLabel8.place(relx=0.790, rely=0.04, height=17, width=90)

        self.TLblTitle = tk.Label(self.top, anchor='w', fg='blue', cursor='hand2', relief='raised')
        self.TLblTitle.configure(font='-family {Times New Roman} -size 12 -weight bold', anchor=CENTER)
        # Open app url on its title click
        self.TLblTitle.bind('<Button-1>', self.openUrl)
        self.TLblTitle.place(relx=0.3, rely=0.089, height=27, width=140)
        tooltip.CreateToolTip(self.TLblTitle, 'Click to open module home url')

        self.TLblVersion = ttk.Label(self.top, font=self.lblinffont)
        self.TLblVersion.place(relx=0.551, rely=0.089, height=27, width=50)
        self.TLblDate = ttk.Label(self.top, font=self.lblinffont)
        self.TLblDate.place(relx=0.629, rely=0.089, height=27, width=90)
        self.TLblAuthors = ttk.Label(self.top, font=self.lblinffont)
        self.TLblAuthors.place(relx=0.790, rely=0.089, height=27, width=120)

        self.TLabel1 = ttk.Label(self.top, text='Available modules')
        self.TLabel1.configure(font="-family {Times New Roman} -size 14 -weight bold")
        self.TLabel1.place(relx=0.034, rely=0.022, height=27, width=160)
        # Set font for combobox list as selected value has
        top.master.option_add("*TCombobox*Listbox*Font", self.lblinffont)
        # top.master.option_add("*TCombobox*Listbox*Background", "#ffffff")
        # top.master.option_add("*TCombobox*Listbox*Foreground", "#000000")
        self.TAvailModules = ttk.Combobox(self.top, font=self.lblinffont, textvariable=self.combobox)
        self.TAvailModules.config(exportselection=False, state='readonly') # style='Avail.TCombobox'
        self.TAvailModules.bind('<<ComboboxSelected>>', self.chModule)
        self.TAvailModules.place(relx=0.034, rely=0.089, relheight=0.064, relwidth=0.255)
        self.TLabel4 = ttk.Label(self.top, text='Timer', font=self.lblsysfont)
        self.TLabel4.place(relx=0.034, rely=0.17, height=17, width=43)
        self.TSpinbox1 = ttk.Spinbox(self.top, from_=5, to=3600,
            textvariable=self.timer, validate='key',
            validatecommand=(self.top.register(self._validate), '%P'))
        self.TSpinbox1.configure(increment=5, background="white")
        self.TSpinbox1.configure(font=self.lblsysfont)
        self.TSpinbox1.place(relx=0.1, rely=0.17, relheight=0.05, relwidth=0.09)

        self.Frame1 = tk.Frame(self.top, relief='raised', borderwidth=2)
        self.Frame1.place(relx=0.034, rely=0.778, relheight=0.189, relwidth=0.938)
        self.TButton4 = ttk.Button(self.Frame1, text='Cancel', command=self.closeApp)
        self.TButton4.place(relx=0.829, rely=0.235, height=46, width=85)
        tooltip.CreateToolTip(self.TButton4, 'Discard all changes and close window')
        self.TButton3 = ttk.Button(self.Frame1, text='Test module', command=self.testModule)
        self.TButton3.place(relx=0.432, rely=0.235, height=46, width=105)
        tooltip.CreateToolTip(self.TButton3, 'Test current module in separate window')
        self.TButton2 = ttk.Button(self.Frame1, text='Save & close', command=self.saveAndClose)
        self.TButton2.place(relx=0.018, rely=0.235, height=46, width=95)
        tooltip.CreateToolTip(self.TButton2, 'Accept all changes and close window')

        self.TLabel2 = ttk.Label(self.top, text='Active modules')
        self.TLabel2.place(relx=0.034, rely=0.238, height=37, width=133)
        self.TLabel2.config(font="-family {Times New Roman} -size 14 -weight bold")
        self.ActiveModules = ScrolledListBox(self.top)
        self.ActiveModules.place(relx=0.034, rely=0.314, relheight=0.44, relwidth=0.32)
        self.ActiveModules.config(listvariable=self.listbox, exportselection=False, bg='white', cursor='arrow')
        self.ActiveModules.config(activestyle='dotbox', selectmode=BROWSE, font=self.lblinffont)
        self.ActiveModules.config(highlightcolor="#d9d9d9", selectbackground="#d9d9d9", selectforeground='black')
        self.ActiveModules.bind('<<ListboxSelect>>', self.actModulesClick)

        self.TBtnAddAll = ttk.Button(self.top, text='Add all', command=self.addAll)
        self.TBtnAddAll.place(relx=0.35, rely=0.20, height=26, width=60)
        self.TBtnAdd = ttk.Button(self.top, text='Add', command=self.addModule)
        self.TBtnAdd.place(relx=0.372, rely=0.317, height=26, width=45)
        self.TBtnDel = ttk.Button(self.top, text='Del', command=self.delModule)
        self.TBtnDel.place(relx=0.372, rely=0.384, height=26, width=45)
        # Buttons for moving items up and down in listbox
        self.TBtnUp = ttk.Button(self.top, text='Up', command=self.actModulesUp)
        self.TBtnUp.place(relx=0.372, rely=0.507, height=26, width=45)
        self.TBtnDown = ttk.Button(self.top, text='Down', command=self.actModulesDown)
        self.TBtnDown.place(relx=0.372, rely=0.574, height=26, width=45)
        self.TBtnMix = ttk.Button(self.top, text='Mix', command=self.actModulesMix)
        self.TBtnMix.place(relx=0.372, rely=0.67, height=26, width=45)
        tooltip.CreateToolTip(self.TBtnAdd, 'Add module to active list')
        tooltip.CreateToolTip(self.TBtnDel, 'Remove module from active list')
        tooltip.CreateToolTip(self.TBtnDown, 'Move item down')
        tooltip.CreateToolTip(self.TBtnUp, 'Move item up')
        tooltip.CreateToolTip(self.TSpinbox1, 'Set timer in seconds')
        tooltip.CreateToolTip(self.TBtnAddAll, 'Add all available modules to active list')
        tooltip.CreateToolTip(self.TBtnMix, 'Mix up active modules')
        # Hovertip(self.TSpinbox1, 'Set timer in seconds when this module should close and next module in list should start')

        self.modalCreate()
        self.loadModules()

    def _validate(self, P):
        """Make sure numbers only in spinbox"""
        return P.isdigit()

    def modalCreate(self):
        """Create hidden modal window for entering module options values"""
        self.FrameNewVal = tk.Frame(self.top, borderwidth=2, relief='groove')
        self.LblNewTit = tk.Label(self.FrameNewVal, text='Enter new value for', font='-family {Times New Roman} -size 12 -weight bold')
        self.LblNewTit.place(relx=0.122, rely=0.089, height=21, width=204)
        self.LblNewVal = tk.Label(self.FrameNewVal, font='-family {Times New Roman} -size 14 -weight bold')
        self.LblNewVal.place(relx=0.122, rely=0.222, height=21, width=194)
        self.TBtnNewCancel = ttk.Button(self.FrameNewVal, text='Cancel', command=self.treeviewCancel)
        self.TBtnNewCancel.place(relx=0.535, rely=0.667, height=46, width=77)
        self.TBtnNewOk = ttk.Button(self.FrameNewVal, text='OK', command=self.treeviewOK)
        self.TBtnNewOk.place(relx=0.122, rely=0.667, height=46, width=77)
        self.EntNewVal = tk.Entry(self.FrameNewVal, exportselection=False, font='-family {Courier New} -size 10', textvariable=self.comboNewbox)
        self.TLblErr = ttk.Label(self.FrameNewVal, foreground='#ff0000', text='Value error: enter new value please', font='-family {Times New Roman} -size 12 -weight bold')
        # @2024_04_06_1921 color select button added
        self.TBtnSelCol = tk.Button(self.FrameNewVal, text='...', command=self.chooseColor)
    def saveAndClose(self):
        """Save settings and close settings window"""
        logger.info(f'Saving settings into file {self.settings_file}')
        with open(self.settings_file, 'w') as fd:
            json.dump(self.settings, fd)
        logger.info('Saving settings successful!')
        self.closeApp()
    def closeApp(self):
        """Destroy master window because top is Toplevel not master
        in order to application proper exit"""
        self.top.master.destroy()
    def loadDefOpts(self):
        """Load default options for current module"""
        name = self.TAvailModules.get()
        module = importlib.import_module('.' + name, 'screensavers')
        self.settings[name]['options'] = dict(module.app_options)
        self.chModule()

    def treeview(self, evt=None):
        """Event when treeview item selected"""
        s = self.TOptions.selection()
        self.afterid = None
        if len(s):
            self.idtree = s[0]
            self.optname, val = self.TOptions.item(self.idtree, option='values')
            self.LblNewVal.config(text=self.optname)
            self.comboNewbox.set(val)
            # Show combobox for entering True/False or entry for other values
            if val in ('True', 'False'):
                # @2024_03_28_1425 True <-> False every time
                val = 'True' if val == 'False' else False
                self.settings[self.TAvailModules.get()]['options'][self.optname] = (val == 'True')
                self.TOptions.item(self.idtree, values=(self.optname, val))
            else:
                self.EntNewVal.place(relx=0.122, rely=0.444, height=30, relwidth=0.660)
                self.EntNewVal.focus_set()
                self.EntNewVal.select_range(0, len(val))
                self.EntNewVal.icursor(END)
                # Place color chooser button if we can set its background color to val
                try:
                    self.TBtnSelCol.config(bg=val)
                    self.TBtnSelCol.place(relx=0.82, rely=0.454, height=24, relwidth=0.08)
                    # Flag of editing color value to test
                    self.thisisColor = True
                except: self.thisisColor = False
                # Show modal and bind several keypresses to it
                self.FrameNewVal.place(relx=0.236, rely=0.222, relheight=0.5, relwidth=0.45)
                self.FrameNewVal.bind_all('<KeyPress-Escape>', lambda e: self.TBtnNewCancel.invoke())
                self.FrameNewVal.bind_all('<Return>', lambda e: self.TBtnNewOk.invoke())
                self.FrameNewVal.grab_set()
    def chooseColor(self):
        """Choose color dialog. Try to set what is color if not color then None"""
        try:
            color = askcolor(color=self.comboNewbox.get(), title='Choose color please')
        except:
            color = askcolor(title='Choose new color please')
        if color[1] is not None:
            self.comboNewbox.set(color[1])
            self.EntNewVal.select_range(0, len(color[1]))
            self.EntNewVal.icursor(END)
            self.TBtnSelCol.config(bg=color[1])

    def treeviewOK(self):
        """Pressed OK button while entering new option value"""
        newval = self.comboNewbox.get()
        k = self.TAvailModules.get()
        try:
            if len(newval) < 1: raise ValueError
            # Test for valid color value if we are editing color
            if self.thisisColor:
                self.TBtnSelCol.config(bg=newval)
            # Change inner option value to newval respecting its type
            opttype = type(self.settings[k]['options'][self.optname])
            if opttype == int:
                self.settings[k]['options'][self.optname] = int(newval)
            elif opttype == float:
                self.settings[k]['options'][self.optname] = float(newval)
            elif opttype == bool:
                self.settings[k]['options'][self.optname] = (newval == 'True')
            elif opttype == list or opttype == tuple:
                self.settings[k]['options'][self.optname] = newval.split()
            else:
                # defaults to str type
                self.settings[k]['options'][self.optname] = newval
        except (ValueError, tk.TclError):
            # Show warning label and hide it in 4 seconds
            self.TLblErr.place(relx=0.025, rely=0.300, height=28, width=300)
            self.afterid = self.FrameNewVal.after(4000, lambda: self.TLblErr.place_forget())
            self.EntNewVal.select_range(0, len(newval))
            self.EntNewVal.icursor(END)
            self.EntNewVal.focus_set()
        else:
            # @2024_03_24_1131 Change treeview item to reflect new values
            self.TOptions.item(self.idtree, values=(self.optname, newval))
            # Hide modal frame
            self.treeviewCancel()
    def treeviewCancel(self):
        """Cancel button pressed in modal - close modal"""
        # If we have ongoing promise - cancel it and hide warning label
        if self.afterid is not None:
            self.FrameNewVal.after_cancel(self.afterid)
            self.TLblErr.place_forget()
        self.FrameNewVal.unbind_all('<KeyPress-Escape>')
        self.FrameNewVal.unbind_all('<Return>')
        self.FrameNewVal.grab_release()
        self.FrameNewVal.place_forget()
        self.TBtnSelCol.place_forget()
        # Return focus onto treeview
        self.TOptions.focus_set()

    def spinbox(self, *args):
        """Event when spinbox values changes"""
        timer = self.timer.get()
        if timer and type(timer) == int and timer >= 5:
            # Current module in combobox
            k = self.TAvailModules.get()
            if k in self.settings:
                self.settings[k]['timer'] = timer
    def openUrl(self, evt):
        k = self.TAvailModules.get()
        if k in self.settings:
            webbrowser.open(self.settings[k]['url'], new=2)

    def actModulesClick(self, evt=None):
        """Click on active modules list to change current active module"""
        cursel = self.ActiveModules.curselection()
        if(len(cursel)):
            name = self.ActiveModules.get(cursel[0])
            self.combobox.set(name)
            self.chModule()
    def actModulesUp(self):
        """Move up selected item in list"""
        cursel = self.ActiveModules.curselection()
        if(len(cursel)):
            im = cursel[0]
            if im > 0:
                name = self.ActiveModules.get(cursel[0])
                self.ActiveModules.delete(im)
                self.ActiveModules.insert(im - 1, name)
                self.ActiveModules.selection_set(im - 1)
                self.ActiveModules.see(im - 1)
                self.reorderModules()
    def actModulesDown(self):
        """Move down selected item in list"""
        cursel = self.ActiveModules.curselection()
        if(len(cursel)):
            im = cursel[0]
            if im < self.ActiveModules.index('end') - 1:
                name = self.ActiveModules.get(cursel[0])
                self.ActiveModules.delete(im)
                self.ActiveModules.insert(im + 1, name)
                self.ActiveModules.selection_set(im + 1)
                self.ActiveModules.see(im + 1)
                self.reorderModules()

    def chModule(self, evt=None):
        """Event after changing module name in combobox"""
        # Set labels for current module
        k = self.TAvailModules.get()
        self.TLblTitle.config(text=self.settings[k]['title'])
        self.TLblVersion.config(text=self.settings[k]['version'])
        self.TLblDate.config(text=self.settings[k]['date'])
        self.TLblAuthors.config(text=self.settings[k]['authors'])
        self.timer.set(self.settings[k]['timer'])
        # Update treeview widget with current module options
        self.TOptions.delete(*self.TOptions.get_children())
        for key, val in self.settings[k]['options'].items():
            self.TOptions.insert('', 'end', None, values=(key, val))

    def addAll(self):
        """Add all available modules to active modules list"""
        s = self.TAvailModules.cget('values')
        for name in s: self.addModule(name)

    def actModulesMix(self):
        """Mix up active modules list"""
        s = self.ActiveModules.get(0, END)
        if len(s) > 1:
            s = list(s)
            # Shuffle, delete and set again
            random.shuffle(s)
            self.ActiveModules.delete(0, END)
            # self.listbox.set(' '.join(s))
            for name in s: self.addModule(name)

    def addModule(self, name=None):
        """Event for adding current module into active list"""
        k = self.TAvailModules.get() if name is None else name
        s = self.ActiveModules.get(0, END)
        # Add only if it is not present yet
        if k in self.settings and k not in s:
            cursel = self.ActiveModules.curselection()
            if(len(cursel)):
                self.ActiveModules.insert(cursel[0], k)
            else:
                self.ActiveModules.insert(END, k)
                self.ActiveModules.see('end')
            self.reorderModules()
    def delModule(self):
        """Event for deleting current module from active list"""
        cursel = self.ActiveModules.curselection()
        if(len(cursel)):
            self.ActiveModules.delete(cursel[0])
            self.reorderModules()
    def reorderModules(self):
        """Reorder all modules anew"""
        for mmm in self.settings:
            self.settings[mmm]['order'] = 0
        # Reorder active modules due to new list
        values = self.ActiveModules.get(0, END)
        order = 0
        for mmm in values:
            order += 1
            self.settings[mmm]['order'] = order

    def loadModules(self):
        """Loading modules from settings on startup"""
        self.TAvailModules.config(values=list(self.settings.keys()))
        self.combobox.set('')
        # add active modules in listbox
        s = {}
        for k in self.settings.keys():
            if self.settings[k]['order']:
                s[k] = self.settings[k]['order']
        if len(s):
            active_scrsavers = sorted(s.items(), key=lambda x:x[1])
            ll = [i[0] for i in active_scrsavers]
            self.listbox.set(' '.join(ll))
            self.combobox.set(ll[0])
        # If there are no active modules yet add first module to combobox value
        if not self.combobox.get(): self.combobox.set(list(self.settings.keys())[0])
        self.chModule()

    def testModule(self):
        """Testing module by creating its App class using current options"""
        name = self.TAvailModules.get()
        module = importlib.import_module('.' + name, 'screensavers')
        module.App(self.settings[name]['options'])

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    """Configure the scrollbars for a widget."""
    def __init__(self, master):
        """Added: # type: ignore
                for VS Code intelliphense not seeing some parent attributes
            Beotiger @2024_04_06_1441
        """
        self.master = master
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview) # type: ignore
            self.configure(yscrollcommand=self._autoscroll(vsb)) # type: ignore
            vsb.grid(column=1, row=0, sticky='ns')
        except: pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview) # type: ignore
        self.configure(xscrollcommand=self._autoscroll(hsb)) # type: ignore
        hsb.grid(column=0, row=1, sticky='ew')

        self.grid(column=0, row=0, sticky='nsew') # type: ignore
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        """Hide and show scrollbar as needed."""
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    """Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget."""
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledListBox(AutoScroll, tk.Listbox):
    """A standard Tkinter Listbox widget with scrollbars that will
    automatically show/hide as needed."""
    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)
    def size_(self):
        sz = tk.Listbox.size(self)
        return sz

class ScrolledTreeView(AutoScroll, ttk.Treeview):
    """A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed."""
    @_create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')

# We should run this module from tkscrsavers.py, but if we wish we can run it directly also why not?
if __name__ == '__main__':
    w = tkscrsavers.TkScrSaver(config=True)
    w.root.mainloop()