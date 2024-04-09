"""
Implementation of Growing Tentacles with Code in Javascript/P5.js
by Barney Codes https://www.youtube.com/watch?v=cHlhdhZuZuc
Source code in P5js editor available at https://editor.p5js.org/BarneyCodes/sketches/zo4DsT95i

Note: while in test mode pressing Space bar or left mouse click will stop/resume animation.
@2024_03_31_1828 by Beotiger

Use left mouse button to restart drawing or Space bar key to pause it
"""

# Import needed libraries here, tkinter is a must obviously
import random
import math
from tkinter import *

# Default width and height of canvas when testing screensaver.
# Adjust them to your needs
WIDTH, HEIGHT = 600, 600

# Default screensaver settings.
app_name = 'Growing Tentacles'
app_version = '1.0'
app_authors = 'Barney Codes'
app_url = 'https://www.youtube.com/watch?v=cHlhdhZuZuc'
# For the sake of history add date of birth or finishing of your screensaver here
app_date = '2022-07-10'
app_license = 'MIT'
# Default screensaver options in a form of a dict
app_options = {
	'background': '#DCDCDC',
	# Default tentacles speed
	'speed': 0.3,
	# Starting radius of tentacles
	'startRad': 30,
	# Or use dynamic radius which depends on window height
	'dynamicRad': True,
	# Starting number of tentacles
	'num': 15,
	# Start/end colors for tentacles
	'startColor': '#500050',
	'endColor': '#FFC8FF',
	# Timer in seconds when redraw tentacles (0 to disable)
	'timer': 10
}

class GradientColor:
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
		return {"hex":[GradientColor.RGB_to_hex(RGB) for RGB in gradient],
				"r":[RGB[0] for RGB in gradient],
				"g":[RGB[1] for RGB in gradient],
				"b":[RGB[2] for RGB in gradient]}

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

class Point:
	def __init__(self, app, x, y, ang, rad):
		self.app = app
		self.x, self.y = x, y
		self.ang = ang
		self.rad = rad

	def update(self):
		self.rad -= 0.5
		self.ang += random.uniform(-math.pi / 6, math.pi / 6)
		self.x += math.cos(self.ang) * self.rad * self.app.options['speed']
		self.y += math.sin(self.ang) * self.rad * self.app.options['speed']

	def draw(self):
		# startColor = (80, 0, 80) 		# #500050
		# endColor = (255, 200, 255)	# #FFC8FF
		# color = self.app.lerpColor(startColor, endColor, self.app.map(self.rad, self.app.options['startRad'], 0, 0, 1))
		# rgb = '#' + '' . join(f'{i:02X}' for i in color)
		rgb = self.app.colors[int(self.rad * 2)]
		self.app.circle(rgb, self.x, self.y, self.rad * 2, width=0)

class Main:
	"""Main canvas class where all animation occurs"""
	def __init__(self, canvas, options):
		self.canvas = canvas
		# Set default options
		self.options = dict(app_options)
		# Change these options from options parameter
		for key, val in options.items():
			self.options[key] = val
		# Set background for the canvas
		self.canvas.config(bg=self.options['background'])
		# Some mouse event listeners won't work in screensaver mode
		# but do work in test mode
		self.canvas.bind_all('<F11>', self.toggle_fullscreen)
		self.canvas.bind('<1>', self.resize)
		self.canvas.bind_all('<space>', self.pause)
		self.canvas.bind('<Configure>', self.resize)
		self.timer = None
		# For full screen switch
		self.state = False
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
	def lerpColor(self, c1, c2, amt):
		"""Function from P5.js
		@c1, @c2 - 3-x color tuples in form (r, g, b)"""
		amt = max(min(amt, 1), 0)
		lerp = lambda start, stop, amt: amt * (stop - start) + start
		l0 = int(lerp(c1[0], c2[0], amt) * 255) % 256
		l1 = int(lerp(c1[1], c2[1], amt) * 255)	% 256
		l2 = int(lerp(c1[2], c2[2], amt) * 255)	% 256
		# l0 = max(min(l0, 255), 0)
		# l1 = max(min(l1, 255), 0)
		# l2 = max(min(l2, 255), 0)
		return (l0, l1, l2)

	def circle(self, color, x, y, r, **kwargs):
		"""Draw circle at x,y coords with radius r, kwargs - more optional Tk parameters.
				This version uses translation"""
		return self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, **kwargs)

	# Some events bindings
	def toggle_fullscreen(self, evt=None):
			"""Toggle full screen mode"""
			self.state = not self.state
			self.canvas.master.attributes('-fullscreen', self.state)
			self.canvas.config(bd=int(not self.state), highlightthickness=int(not self.state))
	def resize(self, evt=None):
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

	def init(self):
		"""Initialise any options"""
		# Stop timer if it is in progress
		if self.timer is not None:
			self.canvas.after_cancel(self.timer)
			self.timer = None
		# Store new width/height of the canvas
		self.w, self.h = self.canvas.winfo_width(), self.canvas.winfo_height()
		self.canvas.delete(ALL)
		self.done = False
		self.points = []
		TAU = math.pi * 2
		# We can use dynamic starting radius
		if self.options['dynamicRad']:
			self.options['startRad'] = self.h // 20
		# Use startRad * 2 gradient colors
		self.colors = GradientColor.linear_gradient(
			self.options['startColor'],
			self.options['endColor'],
			self.options['startRad'] * 2)['hex']
		# Create starting points to draw into tentacles
		for _ in range(self.options['num']):
			self.points.append(Point(self, self.w / 2, self.h / 2, random.uniform(0, TAU), self.options['startRad']))
		# Start animation
		self.running = True

	def update(self):
		"""Main update routine"""
		if self.running:
			# Clear canvas if needed
			# self.canvas.delete(ALL)
			if not self.done:
				for point in self.points:
					point.update()
					point.draw()
					if point.rad <= 0:
						self.done = True
			else:
				self.running = False
				if self.options['timer'] > 0:
					if self.timer is not None:
						self.canvas.after_cancel(self.timer)
					self.timer = self.canvas.after(self.options['timer'] * 1000, self.resize)

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
