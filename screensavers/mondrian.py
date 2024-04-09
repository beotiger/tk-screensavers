"""
	Implementation of Mondrian-Inspired Generative Art.
	Based on Javascript code by Patt Vira https://www.youtube.com/watch?v=WfDgd5uflSc
	Source code in P5.js editor is here: https://editor.p5js.org/pattvira/sketches/q13O-lek4

	Note: while in test mode pressing Space bar or left mouse click
				will stop/resume animation and ESCape key will close window.
				F11 key toggles full screen mode.

	Adapted on @2024_04_06_1057 by Beotiger
"""

# Import needed libraries here, tkinter is a must obviously
import random
import math
from tkinter import *

# Default width and height of canvas when testing screensaver.
# Adjust them to your needs
WIDTH, HEIGHT = 400, 400

# Default screensaver settings.
# They are used in tkscrsavers.py so we should not change their names
# but should and must change their values
app_name = 'Mondrian Gen Art'
app_version = '1.0'
app_authors = 'Patt Vira'
app_url = 'https://www.youtube.com/watch?v=WfDgd5uflSc'
# For the sake of history add date of birth or finishing of your screensaver here
app_date = '2024-01-19'
app_license = 'MIT'
# Default screensaver options in a form of a dict
app_options = {
	# 'background': '#DCDCDC',
	'background': '#cdeeca',
	# Used colors
	'colors': ['#FFF001', '#FF0101', '#0101FD', '#f9f9f9'],
	# Number of arts
	'columns': 5,
	# Timer to redraw art in seconds
	'timer': 15
}

class Block:
	def __init__(self, c, main):
		self.c = c
		self.main = main
		self.colRange = self.randomLengthGen(main.cols + 1)
		self.rowRange = self.randomLengthGen(main.rows + 1)

		self.block = dict(
			((i, j), Cell(i * main.wx, j * main.hx, main.wx, main.hx, j)) for i in range(self.colRange[0], self.colRange[1]) for j in range(self.rowRange[0], self.rowRange[1])
		)

	def display(self):
		# strokeWeight(3);
		for i in range(self.colRange[0], self.colRange[1]):
			for j in range(self.rowRange[0], self.rowRange[1]):
				color = 'black' if i == self.colRange[0] or i == self.colRange[1] - 1 else self.c
				self.block[i, j].displayCell(color, self.main, 3)

	def randomLengthGen(self, length):
		while True:
			if length < 6: return (1, 5)
			a = random.randint(0, length)
			b = random.randint(0, length)
			if abs(a - b) >= 4: break
		return (min(a, b), max(a, b))

class Cell:
	def __init__(self, x, y, w, h, row):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.row = row

	def displayCell(self, color, main, width):
		# drawLine(self, color, x1, y1, x2, y2, **kwargs):
		if self.row % 2 == 0:
			main.drawLine(color, self.x, self.y, self.x + self.w, self.y + self.h, width=width)
		else:
			main.drawLine(color, self.x + self.w, self.y, self.x, self.y + self.h, width=width)


class Main:
	"""Main canvas class where all animation occurs"""
	def __init__(self, canvas, options):
		self.canvas = canvas
		# Set default options
		self.options = dict(app_options)
		# Change these options from options parameter
		for key, val in options.items():
			self.options[key] = val
		# Start with running animation
		self.running = True
		self.state = False
		self.timer = None
		# Set background for the canvas
		self.canvas.config(bg=self.options['background'])
		# Some mouse event listeners won't work in screensaver mode
		# but do work in test mode
		self.canvas.bind('<1>', self.pause)
		self.canvas.bind_all('<space>', self.pause)
		self.canvas.bind_all('<F11>', self.toggle_fullscreen)
		self.canvas.bind('<Configure>', self.resize)
		self.canvas.bind('<Destroy>', self.game_over)
		# Run init animation at first time
		self.init()

	# Some Tk canvas draw primitives wrappers we can use in our animation
	def drawLine(self, color, x1, y1, x2, y2, **kwargs):
		"""Draw a line on the canvas with specified color"""
		return self.canvas.create_line(x1, y1, x2, y2, capstyle=ROUND, fill=color, **kwargs)

	# Some events bindings
	def toggle_fullscreen(self, evt=None):
			"""Event or method: toggle full screen mode"""
			self.state = not self.state
			self.canvas.master.attributes('-fullscreen', self.state)
			self.canvas.config(bd=int(not self.state), highlightthickness=int(not self.state))
	def resize(self, evt):
		"""Event: resize canvas"""
		# Get new canvas dimensions from new main window size
		nw, nh = self.canvas.master.winfo_width(), self.canvas.master.winfo_height()
		# And recreate canvas size accordingly
		self.canvas.config(width=nw, height=nh)
		# And init animation anew
		self.init()
	def pause(self, evt=None):
		"""Pause/resume animation. Can be called directly or as an event binding"""
		self.running = not self.running
	def game_over(self, evt=None):
		"""Stop animation. Can be called directly or as an event binding"""
		if self.timer is not None: self.canvas.after_cancel(self.timer)
		self.running = False

	def init(self):
		"""Initialise any options"""
		# Store new width/height of the canvas
		self.w, self.h = self.canvas.winfo_width(), self.canvas.winfo_height()
		"""Init code here"""
		self.wx = self.options['columns']
		self.hx = self.wx * 2
		self.cols = self.w // self.wx
		self.rows = self.h // self.hx

		self.num = random.randint(6, 10)
		self.blocks = []
		for i in range(self.num):
			self.blocks.append(Block(self.options['colors'][i % len(self.options['colors'])], self))

		self.grid = [ [] for _ in range(self.cols) ]
		for i in range(self.cols):
			# self.grid[i] = list(range(self.rows))
			for j in range(self.rows):
				# self.grid[i][j] = Cell(i * self.wx, j * self.hx, self.wx, self.hx, j)
				self.grid[i].append(Cell(i * self.wx, j * self.hx, self.wx, self.hx, j))
		self.running = True

	def update(self):
		"""Main update routine"""
		if self.running:
			# Clear canvas if needed
			self.canvas.delete('all')
			for i in range(self.cols):
				for j in range(self.rows):
					self.grid[i][j].displayCell('white', self, 1)

			for i in range(self.num):
				self.blocks[i].display()

			self.running = False
			if self.timer is not None: self.canvas.after_cancel(self.timer)
			self.timer = self.canvas.after(self.options['timer'] * 1000, self.init)

class TkScreenSaver:
	"""Screensaver differs from App that it need not create main toplevel window
	but using those from tkscrsavers.py that calls self screensaver"""
	def __init__(self, scrsaver, options, timer=0):
		"""Init application then run game loop."""
		self.root = scrsaver.win
		self.root.protocol('WM_DELETE_WINDOW', self.fin)
		# Use timer to stop animation after timer * 1000 (ms)
		self.timer = self.root.after(timer * 1000, self.fin) if timer else None
		# Create canvas without borders with hidden mouse cursor
		self.canvas = Canvas(self.root, width=scrsaver.monitor.width, height=scrsaver.monitor.height,
													bd=0, relief='ridge', highlightthickness=0, cursor='none')
		self.canvas.pack()
		# Should give Main link to canvas for drawing and options to use
		self.animate = Main(self.canvas, options)
		self.run()

	def run(self, evt=None):
		"""Run animation while not any key pressed or mouse move as a rule"""
		self.animate.update()
		# Let all windows be updated and handle events
		self.root.update_idletasks()
		# Update our window too
		self.root.update()
		# 1000 / 25 = 40 fps approximately of course
		self.afterId = self.root.after(25, self.run)

	def fin(self, evt=None):
		"""Finalize animation: set it to false and close (i.e. destroy) window"""
		self.animate.running = False
		# Cancelling all Tk timers to prevent warning messages from Tk
		# when we destroy window while some timer on it has not been processed yet
		if self.timer is not None: self.root.after_cancel(self.timer)
		self.root.after_cancel(self.afterId)
		# We destroy Toplevel window of tkscrsavers.py.
		# It catches it up to run next screensaver in duty
		self.root.destroy()

class App:
	"""Test application"""
	def __init__(self, options):
		"""Init application then run game loop"""
		self.win = Tk()
		self.win.geometry(f'{WIDTH}x{HEIGHT}')
		self.win.title(f'{app_name} {app_version} by {app_authors}')
		# Close main window and exit on ESC keypress
		self.win.bind('<KeyPress-Escape>', self.fin)
		self.win.protocol('WM_DELETE_WINDOW', self.fin)
		# Create canvas for drawing
		self.canvas = Canvas(self.win, width=WIDTH, height=HEIGHT)
		self.canvas.pack()
		self.animate = Main(self.canvas, options)
		self.run()
		self.win.mainloop()

	def run(self, evt=None):
		"""Run animation while not window closed or ESC key pressed"""
		self.animate.update()
		self.win.update_idletasks()
		self.win.update()
		# ~40 fps?
		self.afterId = self.win.after(25, self.run)

	def fin(self, evt=None):
		"""Finalize animation: set it to false, stop timer and close window"""
		self.animate.running = False
		self.win.after_cancel(self.afterId)
		self.win.destroy()

# Run only if not in module mode
if __name__ == '__main__':
	App(app_options)
