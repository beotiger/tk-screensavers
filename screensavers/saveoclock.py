"""This is my implementation of save'o'clock sample app
https://github.com/Ex-iT/save-o-clock by Ex-iT Jeroen D.

Displays a 24-hour clock that moves in circular way through the screen
Starts moving clockwise and change direction every full circle.
All options such as foregound, background, font size, font family
and label text are customizable here in the source code or through tkscrsavers.py application.

Note: time_format can be arbitrary text, not just date time format pattern
Adapted 2024_03_30 18:42 by Beotiger
"""

import math
from datetime import datetime
from tkinter import *

WIDTH = 900
HEIGHT = 600

# Default screensaver settings
app_name = 'Save-O-Clock'
app_authors = 'Jeroen D.'
app_version = '0.0.2'
app_url = 'https://github.com/Ex-iT/save-o-clock'
app_date = '2021-06-26'
app_license = 'MIT'
app_options = {
	'background': 'black',
	'time_format': '%H:%M:%S',
	'font_family': 'JetBrains Mono',
	'font_size': 64,
	'foreground_color': 'white',
	# How many circles should pass before direction changes
	'circles': 3
}

def showLabel(self):
	"""Show label on the screen in position that depends on passed frames.
	angle is 90 +/- fps: it's because radians begin from +quarter of circle and we want it to start from 0°.
		@self must be App or TkScreenSaver instance
	"""
	angle = math.radians((self.fps + 90) % 360) if self.dir else math.radians((90 - self.fps) % 360)
	self.label.configure(text=datetime.now().strftime(self.options['time_format']))
	self.label['font'] = (self.options['font_family'], self.options['font_size'])
	# Sizes of text label can change every time depending on datetime format pattern
	w2, h2 = self.label.winfo_width(), self.label.winfo_height()
	x = (self.wd2 - w2 / 2) + (self.wd2 - w2) * math.cos(angle)
	y = (self.ht2 - h2 / 2) + (self.ht2 - h2) * math.sin(angle)
	self.label.place(x=x, y=y, relwidth=0.9, relheight=0.9)

def resize(self):
	"""Resize event. @self must be App or TkScreenSaver instance"""
	nw, nh = self.frame.master.winfo_width(), self.frame.master.winfo_height()
	self.frame.config(width=nw, height=nh)
	self.wd, self.ht = self.win.winfo_width(), self.win.winfo_height()
	self.wd2, self.ht2 = self.wd // 2, self.ht // 2

class TkScreenSaver:
	"""Screensaver"""
	def __init__(self, scrsaver, options, timer=0):
		"""Init application then run game loop"""
		self.root = scrsaver.win
		self.monitor = scrsaver.monitor
		self.root.protocol('WM_DELETE_WINDOW', self.fin)
		# Use timer to stop animation after timer * 1000 (ms)
		self.timer = self.root.after(timer * 1000, self.fin) if timer else None
		self.fps = 0
		# Direction: clockwise or counter clockwise
		self.dir = True
		self.circs = 0
		# @2024_03_04_2050 get the halves of monitor sizes
		self.wd2 = self.monitor.width // 2
		self.ht2 = self.monitor.height // 2
		self.frame = Frame(
				self.root,
				background=options['background'],
				cursor = 'none',
				width = self.monitor.width,
				height = self.monitor.height
		)
		self.frame.pack(expand=True, fill=X)
		self.label = Label(self.frame, cursor = 'none', fg = options['foreground_color'], bg = options['background'])
		self.options = options
		self.running = True
		self.run()
	def run(self, evt=None):
		"""Run animation while not any key pressed or mouse move"""
		if self.running:
			showLabel(self)
			self.fps += 1
			# Change direction on full circle
			if self.fps % 360 == 0:
					self.circs += 1
					if self.circs >= self.options['circles']:
						self.circs = 0
						self.dir = not self.dir
			self.afterId = self.root.after(25, self.run)
	def fin(self, evt=None):
		"""Finalize animation: set it to false and close window"""
		self.running = False
		if self.timer is not None: self.root.after_cancel(self.timer)
		self.root.after_cancel(self.afterId)
		self.root.destroy()

class App:
	"""Test application"""
	def __init__(self, options):
			"""Init application then run game loop"""
			self.options = options
			self.win = Tk()
			self.win.geometry(f'{WIDTH}x{HEIGHT}')
			self.win.title(f'{app_name} {app_version} by {app_authors}')
			self.win.update_idletasks()
			self.frame = Frame(self.win, background=options['background'], width=WIDTH, height=HEIGHT)
			self.frame.pack(expand=True, fill=X)
			self.label = Label(self.frame, fg = options['foreground_color'], bg = options['background'])
			# @2024_03_04_2050 get the halves of monitor sizes
			self.wd, self.ht = self.win.winfo_width(), self.win.winfo_height()
			self.wd2, self.ht2 = self.wd // 2, self.ht // 2
			# Close main window and exit on ESC keypress
			self.win.bind_all('<KeyPress-Escape>', self.fin)
			# result = lambda x: f.a = x  # Error
			self.win.bind_all('<space>', lambda e: setattr(self, 'running', not self.running))
			self.win.bind_all('<F11>', self.toggle_fullscreen)
			self.win.protocol('WM_DELETE_WINDOW', self.fin)
			self.win.bind('<Configure>', lambda evt: resize(self))
			self.fps = 0
			# Direction: clockwise or counter clockwise
			self.dir = True
			self.circs = 0
			self.running = True
			self.state = False
			self.win.grab_set()
			self.run()
			self.win.mainloop()
	def run(self, evt=None):
			"""Run animation while not window closed or ESC key pressed"""
			if self.running:
				showLabel(self)
				self.fps += 1
				# Change direction on full circle
				if self.fps % 360 == 0:
					self.circs += 1
					if self.circs >= self.options['circles']:
						self.circs = 0
						self.dir = not self.dir
			self.afterId = self.win.after(25, self.run)
	def fin(self, evt=None):
		"""Finalize animation: set it to false and close window"""
		self.running = False
		self.win.after_cancel(self.afterId)
		self.win.destroy()
	def toggle_fullscreen(self, evt=None):
			"""Toggle full screen mode"""
			self.state = not self.state
			self.win.attributes('-fullscreen', self.state)
			# self.frame.config(bd=int(not self.state), highlightthickness=int(not self.state))

# Run only if not in module mode
if __name__ == '__main__':
	App(app_options)
