"""
Fast implementation of stars moving through the screen.
Based on Javascript code by Coding Train https://www.youtube.com/watch?v=17WoOqgXsRM

Note: while in test mode pressing Space bar or left mouse click
				will stop/resume animation and ESCappe key to close window.

@2024_03_31_1828 by Beotiger
"""

# Import needed libraries here, tkinter is a must obviously
import random
from tkinter import *

# Default width and height of canvas when testing screensaver.
# Adjust them to your needs
WIDTH, HEIGHT = 600, 600

# Default screensaver settings.
# They are used in tkscrsavers.py so we should not change their names
# but should and must change their values
app_name = 'Starfield Simulation'
app_version = '1.0'
app_authors = 'Daniel Shiffman'
app_url = 'https://youtube.com/watch?v=17WoOqgXsRM'
# For the sake of history add date of birth or finishing of your screensaver here
app_date = '2016-04-13'
app_license = 'MIT'
# Default screensaver options in a form of a dict
app_options = {
	'background': 'black',
	# Color or b&w mode for stars
	'colorMode': True,
	# Stars color when in color mode
	# Choose gradient color from color1 to color2
	'color1': '#1A1BA2',
	'color2': '#AA2BE2',
	# Default star speed
	'speed': 22,
	# Number of stars on the screen
	'stars': 800,
	# If we should show star tails
	'showTails': True,
}

class GradientColor:
	"""Static class for creating lists of gradient colors"""
	@staticmethod
	def hex_to_RGB(hex):
		""" "#FFFFFF" -> [255,255,255] """
		# Pass 16 to the integer function for change of base
		return [int(hex[i:i+2], 16) for i in range(1, 6, 2)]
	@staticmethod
	def RGB_to_hex(RGB):
		""" [255,255,255] -> "#FFFFFF" """
		# Components need to be integers for hex to make sense
		RGB = [int(x) for x in RGB]
		return "#"+"".join(["0{0:x}".format(v) if v < 16 else
							"{0:x}".format(v) for v in RGB])
	@staticmethod
	def color_dict(gradient):
		""" Takes in a list of RGB sub-lists and returns dictionary of
			colors in RGB and hex form for use in a graphing function
			defined later on """
		return {"hex": [GradientColor.RGB_to_hex(RGB) for RGB in gradient],
				"r": [RGB[0] for RGB in gradient],
				"g": [RGB[1] for RGB in gradient],
				"b": [RGB[2] for RGB in gradient]}
	@staticmethod
	def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
		""" returns a gradient list of (n) colors between
			two hex colors. start_hex and finish_hex
			should be the full six-digit color string,
			inlcuding the number sign ("#FFFFFF") """
		# Starting and ending colors in RGB form
		s = GradientColor.hex_to_RGB(start_hex)
		f = GradientColor.hex_to_RGB(finish_hex)
		# Initilize a list of the output colors with the starting color
		RGB_list = [s]
		# Calcuate a color at each evenly spaced value of t from 1 to n
		for t in range(1, n):
			# Interpolate RGB vector for color at the current value of t
			curr_vector = [
				int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
				for j in range(3)
			]
			# Add it to our list of output colors
			RGB_list.append(curr_vector)
		return GradientColor.color_dict(RGB_list)

class Star:
	def __init__(self, app, color):
		self.x = random.randint(-app.w, app.w)
		self.y = random.randint(-app.h, app.h)
		self.z = random.randint(0, app.w)
		self.pz = self.z
		self.app = app
		self.color = color if app.options['colorMode'] else 'white'

	def update(self, speed):
		self.z = self.z - speed
		if self.z < 1:
			self.z = self.app.w
			self.x = random.randint(-self.app.w, self.app.w)
			self.y = random.randint(-self.app.h, self.app.h)
			self.pz = self.z

	def show(self):
		sx = self.app.map(self.x / self.z, 0, 1, 0, self.app.w)
		sy = self.app.map(self.y / self.z, 0, 1, 0, self.app.h)
		r = self.app.map(self.z, 0, self.app.w, 16, 0)
		self.app.circle(self.color, sx, sy, r, width=0)
		if self.app.options['showTails']:
			px = self.app.map(self.x / self.pz, 0, 1, 0, self.app.w)
			py = self.app.map(self.y / self.pz, 0, 1, 0, self.app.h)
			self.pz = self.z
			self.app.drawLine(self.color, px, py, sx, sy, width=r / 3)
		else:
			self.pz = self.z

class Main:
	"""Main canvas class where all animation occurs"""
	def __init__(self, canvas, options):
		self.canvas = canvas
		# Set default options
		self.options = dict(app_options)
		# Change these options from options parameter
		for key, val in options.items():
			self.options[key] = val
		# Start with running animations
		self.running = True
		self.state = False
		# Set background for the canvas
		self.canvas.config(bg=self.options['background'])
		# Some mouse event listeners won't work in screensaver mode
		# but do work in test mode
		self.canvas.bind('<1>', self.pause)
		self.canvas.bind_all('<F11>', self.toggle_fullscreen)
		self.canvas.bind_all('<space>', self.pause)
		self.canvas.bind('<Motion>', self.motion)
		self.canvas.bind('<Leave>', self.leave)
		self.canvas.bind('<Configure>', self.resize)
		self.canvas.bind('<Destroy>', self.game_over)
		# For translating coordinates set to zero
		self.startX, self.startY = 0, 0
		# If use colors we will use gradint color from color1 to color2
		self.colors = GradientColor.linear_gradient(self.options['color1'], self.options['color2'], 50)['hex']
		# Run init animation at first time
		self.init()

	# Some utility functions can be removed if not in need
	def constrain(self, n, low, high):
		"""Helper function for map"""
		return max(min(n, high), low)
	def map(self, n, start1, stop1, start2, stop2, withinBounds=False):
		"""map function from P5.js"""
		newval = (n - start1) / (stop1 - start1) * (stop2 - start2) + start2
		if not withinBounds: return newval
		if start2 < stop2: return self.constrain(newval, start2, stop2)
		else: return self.constrain(newval, stop2, start2)

	# Some Tk canvas draw primitives wrappers we can use in our animation
	def drawLine(self, color, x1, y1, x2, y2, **kwargs):
		"""Draw a line on the canvas with specified color.
				This version uses translation"""
		return self.canvas.create_line(
				self.startX + x1, self.startY + y1,
				self.startX + x2, self.startY + y2, capstyle=ROUND, fill=color, **kwargs)
	def circle(self, color, x, y, r, **kwargs):
		"""Draw circle at x,y coords with radius r, kwargs - more optional Tk parameters.
				This version uses translation"""
		return self.canvas.create_oval(
				self.startX + x - r, self.startY + y - r,
				self.startX + x + r, self.startY + y + r, fill=color, **kwargs)
	def translate(self, x, y):
		"""Translates start of axises to x, y"""
		self.startX, self.startY = x, y
	# Some events bindings
	def motion(self, evt):
		"""Mouse moves over canvas"""
		self.mouseX = evt.x
	def leave(self, evt):
		"""Mouse leaves canvas"""
		# self.mouseX = random.randint(0, self.w)
		pass
	def resize(self, evt):
		"""Resize canvas"""
		# Get new canvas dimensions
		nw, nh = self.canvas.master.winfo_width(), self.canvas.master.winfo_height()
		# and recreate canvas size accordingly
		self.canvas.config(width=nw, height=nh)
		# And init animation anew
		self.init()
	def pause(self, evt=None):
		"""Pause/resume animation. Can be called directly or as an event binding"""
		self.running = not self.running
	def game_over(self, evt=None):
		"""Stop animations. Can be called directly or as an event binding"""
		self.running = False
	def toggle_fullscreen(self, evt=None):
			"""Toggle full screen mode"""
			self.state = not self.state
			self.canvas.master.attributes('-fullscreen', self.state)
			self.canvas.config(bd=int(not self.state), highlightthickness=int(not self.state))

	def init(self):
		"""Initialise any options"""
		# Store new width/height of the canvas
		self.w, self.h = self.canvas.winfo_width(), self.canvas.winfo_height()
		# self.mouseX = random.randint(0, self.w)
		self.mouseX = None
		# Create 800 stars
		self.stars = []
		[self.stars.append(Star(self, random.choice(self.colors))) for _ in range(self.options['stars'])]
		# Move the beginning of coordinates to the center of the window
		self.translate(self.w / 2, self.h / 2)

	def update(self):
		"""Main update routine"""
		if self.running:
			# Clear canvas if needed
			self.canvas.delete('all')
			speed = self.map(self.mouseX, 0, self.w, 0, 50) if self.mouseX else self.options['speed']
			for i in range(self.options['stars']):
				self.stars[i].update(speed)
				self.stars[i].show()

class TkScreenSaver:
	"""Screensaver"""
	def __init__(self, scrsaver, options, timer=0):
		"""Init application then run game loop."""
		self.root = scrsaver.win
		self.root.protocol('WM_DELETE_WINDOW', self.fin)
		self.timer = self.root.after(timer * 1000, self.fin) if timer else None
		self.canvas = Canvas(self.root, width=scrsaver.monitor.width, height=scrsaver.monitor.height,
													bd=0, relief='ridge', highlightthickness=0, cursor='none')
		self.canvas.pack()
		self.animate = Main(self.canvas, options)
		self.run()

	def run(self, evt=None):
		"""Run animation while not any key pressed or mouse move as a rule"""
		self.animate.update()
		self.root.update_idletasks()
		self.root.update()
		self.afterId = self.root.after(25, self.run)

	def fin(self, evt=None):
		"""Finalize animation: set it to false and close (i.e. destroy) window"""
		self.animate.running = False
		if self.timer is not None: self.root.after_cancel(self.timer)
		self.root.after_cancel(self.afterId)
		self.root.destroy()

class App:
	"""Test application"""
	def __init__(self, options):
		"""Init application then run game loop"""
		self.win = Tk()
		self.win.geometry(f'{WIDTH}x{HEIGHT}')
		self.win.title(f'{app_name} {app_version} by {app_authors}')
		self.win.bind('<KeyPress-Escape>', self.fin)
		self.win.protocol('WM_DELETE_WINDOW', self.fin)
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
		self.afterId = self.win.after(25, self.run)

	def fin(self, evt=None):
		"""Finalize animation: set it to false, stop timer and close window"""
		self.animate.running = False
		self.win.after_cancel(self.afterId)
		self.win.destroy()

# Run only if not in module mode
if __name__ == '__main__':
	App(app_options)
