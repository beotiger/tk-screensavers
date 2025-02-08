"""
	Fire demo from the book of M. Krasnov "OpenGL: Graphics in Delphi Projects",
		published by BHV - Saint Petersburg, 2000

	Note: while in test mode pressing Space bar or left mouse click will stop/resume animation
		and ESCape key will close window.
		F11 key toggles full screen mode.

	@2025_01_25_1144 by Beotiger
"""

# Import needed libraries here, tkinter is a must obviously
import random
from tkinter import *

# Default width and height of canvas when testing screensaver.
WIDTH, HEIGHT = 320, 250

# Default screensaver settings.
# They are used in tkscrsavers.py so we should not change their names
# but should and must change their values
app_name = 'Fire demo'
app_version = '1.1'
app_authors = 'Krasnov M.'
app_url = 'https://archive.org/details/B-001-031-243-ALL'
# For the sake of history add date of birth or finishing of your screensaver here
app_date = '2025-01-25'
app_license = 'MIT'
# Default screensaver options in a form of a dict
app_options = {
	'background': 'black'
}

STEP = 0.04
FADE = 0.385
NUMX = 50
NUMY = 50

class TCol():
	"""Represents RGB color from 0 to 1 as in OpenGL"""
	def __init__(self):
		self.r = 0.0
		self.g = 0.0
		self.b = 0.0

class KrasFire:
	"""Main class to display fire mimic"""
	def __init__(self, master):
		self.PreF = [TCol() for i in range(NUMX)]
		self.Fire = [[TCol() for i in range(NUMX)] for j in range(NUMY)]
		self.master = master

	def SetFire(self):
		for i in range(1, NUMX - 1):
			f = random.randint(0, 299) / 100 - 0.8
			self.PreF[i].r = f
			self.PreF[i].g = f / 1.4
			self.PreF[i].b = f / 2

	def DrawPix(self, x, y):
		""" Draw 1 fire pixel """
		# Convert color from 0..1 (OpenGL) to 0..255
		r, g, b = int(self.Fire[x][y].r * 255), int(self.Fire[x][y].g * 255), int(self.Fire[x][y].b * 255)
		r = self.master.constrain(r, 0, 255)
		g = self.master.constrain(g, 0, 255)
		b = self.master.constrain(b, 0, 255)
		# and to hex form #RRGGBB
		rgb = f'#{r:02X}{g:02X}{b:02X}'

		# In OpenGL there is: glVertex2f(x * STEP - 1, y * STEP - 1.1)
		# Update coordiantes from 0.. NUMX into 0..WIDTH and NUMY..0 into 0..HEIGHT
		# OpenGL Y coordinate originates from bottom to top
		x = self.master.map(x, 0, NUMX, 0, self.master.w)
		y = self.master.map(y, NUMY, 0, 0, self.master.h)
		# @2025_02_08_1629 Set fire pixel size dynamically
		# self.master.setPixel(rgb, x, y, size=20)
		self.master.setPixel(rgb, x, y, size=self.master.w // 50)

	def MixFire(self):
		for i in range(1, NUMX - 1):
			self.Fire[i][0].r = (self.PreF[i - 1].r + self.PreF[i + 1].r + self.PreF[i].r) / 3
			self.Fire[i][0].g = (self.PreF[i - 1].g + self.PreF[i + 1].g + self.PreF[i].g) / 3
			self.Fire[i][0].b = (self.PreF[i - 1].b + self.PreF[i + 1].b + self.PreF[i].b) / 3
		for j in range(1, NUMY - 1):
				for i in range (1, NUMX - 1):
					self.Fire[i][j].r = (self.Fire[i-1][j].r + self.Fire[i+1][j].r + self.Fire[i-1][j-1].r + self.Fire[i][j-1].r + self.Fire[i+1][j-1].r + self.Fire[i][j].r) / 5
					self.Fire[i][j].g = (self.Fire[i-1][j].g + self.Fire[i+1][j].g + self.Fire[i-1][j-1].g + self.Fire[i][j-1].g + self.Fire[i+1][j-1].g + self.Fire[i][j].g) / 5
					self.Fire[i][j].b = (self.Fire[i-1][j].b + self.Fire[i+1][j].b + self.Fire[i-1][j-1].b + self.Fire[i][j-1].b + self.Fire[i+1][j-1].b + self.Fire[i][j].b) / 5

	def FireUp(self):
		for j in range(NUMY - 1, 0, -1):
			for i in range(NUMX):
				self.Fire[i][j].r = self.Fire[i][j - 1].r - FADE
				self.Fire[i][j].g = self.Fire[i][j - 1].g - FADE
				self.Fire[i][j].b = self.Fire[i][j - 1].b - FADE

	def DrawFire(self):
		for j in range(1, NUMY - 1):
			for i in range(1, NUMX - 1):
				self.DrawPix(i, j)

	def TickFire(self):
		self.SetFire()
		self.MixFire()
		self.DrawFire()
		self.FireUp()

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
		# Fullscreen state
		self.state = False
		# Set background for the canvas
		self.canvas.config(bg=self.options['background'])
		# Some mouse event listeners won't work in screensaver mode
		# but do work in test mode
		self.canvas.bind('<1>', self.pause)
		self.canvas.bind_all('<space>', self.pause)
		self.canvas.bind_all('<F11>', self.toggle_fullscreen)
		self.canvas.bind('<Motion>', self.motion)
		self.canvas.bind('<Leave>', self.leave)
		self.canvas.bind('<Configure>', self.resize)
		self.canvas.bind('<Destroy>', self.game_over)
		# Run init animation at first time
		self.init()

	# Some utility functions can be removed if not in need
	def constrain(self, n, low, high):
		"""Helper function for map"""
		return max(min(n, high), low)
	def map(self, n, start1, stop1, start2, stop2, withinBounds=True):
		"""map function from P5.js"""
		newval = (n - start1) / (stop1 - start1) * (stop2 - start2) + start2
		if not withinBounds: return newval
		if start2 < stop2: return self.constrain(newval, start2, stop2)
		else: return self.constrain(newval, stop2, start2)

	# Some Tk canvas draw primitives wrappers we can use in our animation
	def drawLine(self, color, x1, y1, x2, y2, **kwargs):
		"""Draw a line on the canvas with specified color"""
		return self.canvas.create_line(x1, y1, x2, y2, capstyle=ROUND, fill=color, **kwargs)
	def setPixel(self, color, x, y, size=1):
		"""Set one pixel as sizeXsize rectangle"""
		return self.canvas.create_rectangle(x, y, x + size, y + size, outline=color, fill=color)
	def create_circle(self, color, x, y, r, **kwargs):
		"""Draw circle at x,y coords with radius r, kwargs - more optional Tk parameters"""
		return self.canvas.create_oval(x - r, y - r, x + r, y + r, outline=color, **kwargs)
	def create_text(self, x, y, text, fill, font, angle=0):
		self.canvas.create_text(x, y, text=text, fill=fill, font=font, angle=angle, anchor=NW)

	# Some events bindings
	def toggle_fullscreen(self, evt=None):
			"""Event or method: toggle full screen mode"""
			self.state = not self.state
			self.canvas.master.attributes('-fullscreen', self.state)
			self.canvas.config(bd=int(not self.state), highlightthickness=int(not self.state))
	def motion(self, evt):
		"""Event: mouse moves over canvas"""
		pass
	def leave(self, evt):
		"""Event: mouse leaves canvas"""
		pass
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
		self.running = False

	def init(self):
		"""Initialise any options"""
		# Store new width/height of the canvas
		self.w, self.h = self.canvas.winfo_width(), self.canvas.winfo_height()
		# Light up our olympic fire!
		self.fire = KrasFire(self)

	def update(self):
		"""Main update routine"""
		if self.running:
			# Clear all canvas
			self.canvas.delete('all')
			self.fire.TickFire()

class TkScreenSaver:
	"""Screensaver differs from App that it need not create main toplevel window
	but using those from tkscrsavers.py that calls this screensaver"""
	def __init__(self, scrsaver, options, timer=0):
		"""
			Init application then run game loop.
			Use scrsaver.win as Toplevel window.
		"""
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
		"""Init application then run game loop.
		Unlike in TkScreenSaver we should create our own
		main Toplevel window to use animation of screensaver.
		Also we can bind several useful events to it for our purposes.
		"""
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
