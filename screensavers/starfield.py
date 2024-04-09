"""
Fast implementation of stars moving through the screen.
Based on Javascript code by Barney Codes https://www.youtube.com/watch?v=p0I5bNVcYP8
that was dreamed of on https://www.youtube.com/watch?v=17WoOqgXsRM by Coding Train
Adapted @2024_03_31 16:20 by Beotiger for Python and Tk

Note: while in test mode pressing Space bar or left mouse click will stop/resume animation.
"""

import math
import random
from tkinter import *

WIDTH = 800
HEIGHT = 800

# Default screensaver settings
app_name = 'Star Field'
app_version = '1.0'
app_authors = 'Barney Codes'
app_url = 'https://www.youtube.com/watch?v=p0I5bNVcYP8'
app_date = '2022-07-31'
app_license = 'MIT'
# Default screensaver options
app_options = {
		# Background color
		'background': 'black',
		# Color or b&w mode for stars
		'colorMode': True,
		# Stars color when in color mode
		# Choose gradient color from color1 to color2
		'color1': '#1A1BA2',
		'color2': '#AA2BE2',
		# Total count of stars
		'numstars': 500,
		# Acceleration of each star if not in cycled mode
		'acceleration': 0.4,
		# Cycle star accelaration
		'cycled': True,
		# When in interactive mode mouse will speed up/speed down stars
		'interactive': False,
		# Set width for stars
		'starWidth': 3
}

class Vector:
	"""Compact Vector2d class @2024_03_24_1520 updated by Beotiger"""
	def __init__(self, x=0.0, y=0.0): self.x = x; self.y = y
	def add(self, v): return Vector(self.x + v.x, self.y + v.y)
	def sub(self, v): return Vector(self.x - v.x, self.y - v.y)
	def mul(self, v): return Vector(self.x * v.x, self.y * v.y)
	def div(self, v): return Vector(self.x / v.x, self.y / v.y)
	# magnitude
	def mag(self): return math.sqrt(self.x * self.x + self.y * self.y)
	def normalise(self):
		mag = self.mag()
		if mag != 0: return Vector(self.x / mag, self.y / mag)
		return Vector(0, 0)
	# distance
	def dist(self, v): return math.sqrt((self.x - v.x) * (self.x - v.x) + (self.y - v.y) * (self.y - v.y))
	def limit(self, limit):
		if self.mag() > limit: v = self.normalise().mul(Vector(limit, limit))
		else: v = self
		return v

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
	"""Individual Star class"""
	def __init__(self, parent, x, y, color='white'):
		self.parent = parent
		self.pos = Vector(x , y)
		self.prevPos = Vector(x , y)
		self.vel = Vector()
		self.ang = math.atan2(y - self.parent.h / 2, x - self.parent.w / 2)
		self.color = color
		self.width = self.parent.options['starWidth']

	def update(self, acc):
		self.vel.x += math.cos(self.ang) * acc
		self.vel.y += math.sin(self.ang) * acc
		self.prevPos = Vector(self.pos.x, self.pos.y)
		self.pos = self.pos.add(self.vel)

	def draw(self):
		"""Draw star as a line from pos to prevPos"""
		# alpha = int(self.parent.map_v(self.vel.mag(), 0, 3, 0, 255, True))
		# print(f'alpha={alpha}')
		# P5JS: stroke(255, alpha)
		rgb = self.color if self.parent.options['colorMode'] else 'white'
		self.parent.drawLine(rgb, self.pos.x, self.pos.y, self.prevPos.x, self.prevPos.y, width=self.width)

	def isActive(self):
		"""Determine if star is out of screen boundaries"""
		return self.parent.onScreen(self.prevPos.x, self.prevPos.y)

class Starfield:
	"""Main starfield canvas class - director of all stars"""
	def __init__(self, canvas, options):
		"""Set customizable starfield parameters"""
		self.options = dict(app_options)
		# Change default options values from parameter options if any
		for key, val in options.items():
			self.options[key] = val
		self.mousePos = None
		# Choose one of the color in palette in colo rmode
		self.colors = GradientColor.linear_gradient(self.options['color1'], self.options['color2'], 50)['hex']
		self.canvas = canvas
		self.state = False
		# Set background for the canvas
		self.canvas.config(bg=self.options['background'])
		# Mouse event listeners
		self.canvas.bind('<Motion>', self.motion)
		self.canvas.bind_all('<F11>', self.toggle_fullscreen)
		self.canvas.bind('<1>', self.pause)
		self.canvas.bind_all('<space>', self.pause)
		self.canvas.bind('<Leave>', self.leave)
		self.canvas.bind('<Configure>', self.resize)
		# Start with running animation
		self.running = True
		self.initStars()

	def onScreen(self, x, y): return x >= 0 and x <= self.w and y >= 0 and y <= self.h
	def constrain(self, n, low, high): return max(min(n, high), low)
	def map(self, n, start1, stop1, start2, stop2, withinBounds=True):
		"""map function from P5.js"""
		newval = (n - start1) / (stop1 - start1) * (stop2 - start2) + start2
		if not withinBounds: return newval
		if start2 < stop2: return self.constrain(newval, start2, stop2)
		else: return self.constrain(newval, stop2, start2)
	def drawLine(self, color, x1, y1, x2, y2, **kwargs):
		"""Draw a line on the canvas with specified color"""
		return self.canvas.create_line(x1, y1, x2, y2, capstyle=ROUND, fill=color, **kwargs)

	def motion(self, evt):
		"""Mouse moves over canvas"""
		if self.options['interactive']:
			self.mousePos = Vector(evt.x, evt.y)
	def leave(self, evt):
		"""Mouse leaves canvas"""
		self.mousePos = None
	def resize(self, evt):
		"""Resize canvas"""
		nw, nh = self.canvas.master.winfo_width(), self.canvas.master.winfo_height()
		self.canvas.config(width=nw, height=nh)
		self.initStars()
	def pause(self, evt=None):
		"""Pause/resume animation"""
		self.running = not self.running
	def toggle_fullscreen(self, evt=None):
			"""Toggle full screen mode"""
			self.state = not self.state
			self.canvas.master.attributes('-fullscreen', self.state)
			self.canvas.config(bd=int(not self.state), highlightthickness=int(not self.state))

	def initStars(self):
		"""Initialise stars"""
		# Inner frames counter
		self.counter = 0
		self.forward = 1
		self.step = 0.01
		# Get new width/height of the canvas
		self.w, self.h = self.canvas.winfo_width(), self.canvas.winfo_height()
		self.numStars = self.options['numstars']
		self.stars = []
		for _ in range(self.numStars):
			self.newStar()

	def newStar(self, position=None):
		"""Add new star at position"""
		if position is None:
			position = Vector(random.randint(0, self.w), random.randint(0, self.h))
		self.stars.append(Star(self, position.x, position.y, random.choice(self.colors)))

	def update(self):
		"""Main update routine"""
		if self.running:
			# Clear canvas
			self.canvas.delete('all')
			# Stars acceleration
			self.counter += self.forward * self.step
			self.step += self.forward * 0.0005
			if self.counter > 2.0 or self.counter < 0: self.forward *= -1
			acc = self.counter if self.options['cycled'] else self.options['acceleration']
			acc = self.map(self.mousePos.x, 0, self.w, 0.0025, 2.9) if self.mousePos is not None else acc
			# print('acc=', acc)
			for star in self.stars[:]:
				star.draw()
				star.update(acc)
				if not star.isActive(): self.stars.remove(star)
			while len(self.stars) < self.numStars:
				self.newStar()

	def game_over(self, evt=None):
		"""Stop animations"""
		self.running = False

class TkScreenSaver:
	"""Screensaver"""
	def __init__(self, scrsaver, options, timer=0):
		"""Init application then run game loop"""
		self.root = scrsaver.win
		self.monitor = scrsaver.monitor
		self.root.protocol('WM_DELETE_WINDOW', self.fin)
		# Use timer to stop animation after timer * 1000 (ms)
		self.timer = self.root.after(timer * 1000, self.fin) if timer else None
		self.canvas = Canvas(self.root, width=self.monitor.width, height=self.monitor.height,
													bd=0, relief='ridge', highlightthickness=0, cursor='none')
		self.canvas.pack()
		self.starfield = Starfield(self.canvas, options)
		self.run()

	def run(self, evt=None):
		"""Run animation while not any key pressed or mouse move"""
		self.starfield.update()
		self.root.update_idletasks()
		self.root.update()
		self.afterId = self.root.after(25, self.run)

	def fin(self, evt=None):
		"""Finalize animation: set it to false and close window"""
		self.starfield.game_over()
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
		# Close main window and exit on ESC keypress
		self.win.bind('<KeyPress-Escape>', self.fin)
		# Create canvas for drawing some stars, in size as main window size with border width 5px
		self.canvas = Canvas(self.win, width=WIDTH, height=HEIGHT)
		self.canvas.pack()
		self.starfield = Starfield(self.canvas, options)
		self.win.protocol('WM_DELETE_WINDOW', self.fin)
		self.run()
		self.win.mainloop()

	def run(self, evt=None):
		"""Run animation while not window closed or ESC key pressed"""
		self.starfield.update()
		self.win.update_idletasks()
		self.win.update()
		# 40 fps? )
		self.afterId = self.win.after(25, self.run)

	def fin(self, evt=None):
		"""Finalize animation: set it to false and close window"""
		self.starfield.running = False
		self.win.after_cancel(self.afterId)
		self.win.destroy()

# Run test if not in module mode
if __name__ == '__main__':
	App(app_options)
