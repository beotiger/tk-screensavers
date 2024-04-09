"""
CrazyChars is a base module to create awesome magnificent symbol effects on the screen.
Current realization mimics matrix effect from matrix.py module.

While tersting this module you can do the following:

	Space bar/Left mouse click to pause/unpause animation
	F11 - toggle full screen on/off
	ESC - close

	@2024_04_05_1911 by Beotiger
"""

import random
import math
from tkinter import *

WIDTH, HEIGHT = 800, 600

# Default screensaver settings.
app_name = 'Crazy chars'
app_version = '1.0'
app_authors = 'Beotiger & co.'
app_url = 'https://github.com/beotiger/tk-screensavers'
# For the sake of history add date of birth or finishing of your screensaver here
app_date = '2024-04-04'
app_license = 'MIT'
# Default screensaver options in a form of a dict
app_options = {
	'background': 'black',
	'fontsize': 30,
	# Choose gradient color from color1 to color2
	'color1': '#168324',
	'color2': '#1c2577',
	# Speed 1 to 5: 1 - min, 5 - max
	'speed': 3
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
	def normalize(self):
		mag = self.mag()
		if mag != 0: return Vector(self.x / mag, self.y / mag)
		return Vector(0, 0)
	# distance
	def dist(self, v): return math.sqrt((self.x - v.x) * (self.x - v.x) + (self.y - v.y) * (self.y - v.y))
	def setMag(self, n):
		"""Set desired magnitude"""
		self.normalize()._mul(n)
		return self
	def _add(self, n):
		"""Add vector components by n"""
		self.x += n
		self.y += n
		return self
	def _sub(self, n):
		"""Subtruct vector components by n"""
		self.x -= n
		self.y -= n
		return self
	def _mul(self, n):
		"""Multiply vector components by n"""
		self.x *= n
		self.y *= n
		return self
	def _div(self, n):
		"""Divide vector components by n"""
		self.x /= n
		self.y /= n
		return self
	def limit(self, limit):
		return self.normalize().mul(Vector(limit, limit)) if self.mag() > limit else self
	# Calculates the angle a 2D vector makes with the positive x-axis
	def heading(self): return math.atan2(self.y, self.x)
	def __str__(self) -> str:
		return f'V({round(self.x, 2)}, {round(self.y, 2)})'

class GradientColor:
	@staticmethod
	def hex_to_RGB(hex):
		""" '#FFFFFF' -> [255,255,255] """
		# Pass 16 to the integer function for change of base
		return [int(hex[i:i+2], 16) for i in range(1, 6, 2)]

	@staticmethod
	def RGB_to_hex(RGB):
		""" [255,255,255] -> '#FFFFFF' """
		# Components need to be integers for hex to make sense
		RGB = [int(x) for x in RGB]
		return "#"+"".join(["0{0:x}".format(v) if v < 16 else
							"{0:x}".format(v) for v in RGB])

	@staticmethod
	def color_dict(gradient):
		"""Takes in a list of RGB sub-lists and returns dictionary of
			colors in RGB and hex form for use in a graphing function
			defined later on"""
		return {"hex":[GradientColor.RGB_to_hex(RGB) for RGB in gradient],
				"r":[RGB[0] for RGB in gradient],
				"g":[RGB[1] for RGB in gradient],
				"b":[RGB[2] for RGB in gradient]}

	@staticmethod
	def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
		"""Returns a gradient list of (n) colors between
			two hex colors. start_hex and finish_hex
			should be the full six-digit color string,
			inlcuding the number sign ("#FFFFFF")"""
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

class Char:
	def __init__(self, main, char, x, y, size, color, speed, masterId=0, cycles=-1):
		"""If @masterId == 0 this is master char"""
		self.main = main
		self.char = char
		self.pos = Vector(x, y)
		self.size =	size
		self.color = color
		self.speed = speed
		self.id = main.create_text(self.pos.x, self.pos.y, self.char, self.color, ('MS Mincho.ttf', size , 'bold'))
		# If it is not master char tag it for deletion
		if masterId:
			main.canvas.addtag_withtag(f't_{masterId}', self.id)
			# print('Tag added:', f't_{masterId}')
		# Char behaviour
		self.behave = self.matrix
		# Cycles to live (-1 - forever)
		self.cycles = cycles
		# Id of master char
		self.masterId = masterId
		# Reproductive mechanics
		self.reprod = True

	def tick(self):
		if self.cycles > 0:
			self.cycles -= 1
		self.clone()
		self.behave()
		self.main.canvas.coords(self.id, self.pos.x, self.pos.y)

	def clone(self):
		"""Clone char if it size allows it. We can clone ony char during lifecycle?"""
		if self.reprod and self.size > 4:
			color = random.choice(self.main.colors)
			id = self.masterId if self.masterId else self.id
			size = self.size - 2
			self.main.chars.append(
				Char(self.main, random.choice(self.main.letters), self.pos.x + 2, self.pos.y + 2, size, color, self.speed, id)
			)
			self.reprod = False

	def dead(self):
		"""Determine if we are dead:
		we are not top level symbol and our Y coordinate overlaps window height"""
		isdead = self.masterId and self.pos.y > self.main.h - self.size
		if isdead: self.main.canvas.delete(self.id)
		return isdead

	def matrix(self):
		"""Matrix behaviour"""
		self.pos.y += self.size * self.speed
		if (not self.masterId) and self.pos.y > self.main.h:
			self.reprod = True
			self.pos.y = 0
			self.speed = self.main.chooseSpeed()
			# Delete all child chars from the list
			n = self.main.delChilds(self.id)
			# print(f'Matrix:{n} childs removed')
			# And from the canvas
			self.main.canvas.delete(f't_{self.id}')
			# Change symbol char
			self.char = random.choice(self.main.letters)
			self.main.canvas.itemconfigure(self.id, text=self.char)

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
		self.canvas.bind_all('<space>', self.pause)
		self.canvas.bind_all('<F11>', self.toggle_fullscreen)
		self.canvas.bind('<Motion>', self.motion)
		self.canvas.bind('<Leave>', self.leave)
		self.canvas.bind('<Configure>', self.resize)
		self.canvas.bind('<Destroy>', self.game_over)
		# Main attributes
		self.colors = GradientColor.linear_gradient(options['color1'], options['color2'], 32)['hex']
		self.font_size = self.options['fontsize']
		# self.font = ('MS Mincho.ttf', self.font_size, 'bold')
		# self.font = ('Consolas', self.font_size)
		self.letters = [chr(int('0x30a0', 16) + i) for i in range(1, 95)]
		# Run init animation at first time
		self.options['speed'] = self.constrain(self.options['speed'], 1, 5)
		# print(f"self.options['speed']={self.options['speed']}")
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

	def create_text(self, x, y, text, fill, font, **kwargs):
		return self.canvas.create_text(x, y, text=text, fill=fill, font=font, anchor=NW, **kwargs)

	# Some events bindings
	def toggle_fullscreen(self, evt=None):
			"""Toggle full screen mode"""
			self.state = not self.state
			self.canvas.master.attributes('-fullscreen', self.state)
			self.canvas.config(bd=int(not self.state), highlightthickness=int(not self.state))
	def motion(self, evt):
		"""Mouse moves over canvas"""
		pass
	def leave(self, evt):
		"""Mouse leaves canvas"""
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

	def chooseSpeed(self):
		return random.uniform(1, 1.5)
	def init(self):
		"""Initialise any options"""
		# Store new width/height of the canvas
		self.w, self.h = self.canvas.winfo_width(), self.canvas.winfo_height()
		"""Init code here"""
		# self.letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789'
		gap = 10
		self.columns = self.w // (self.font_size + gap)
		self.canvas.delete(ALL)
		# Set gap between chars in a row
		# Create self.columns chars at the top of the screen in a row
		self.chars = [Char(self, random.choice(self.letters), i * (self.font_size + gap), 0, self.font_size, random.choice(self.colors), self.chooseSpeed()) for i in range(self.columns)]
		# self.chars = [Char(self, random.choice(self.letters), self.w // 2 - self.font_size, 0, self.font_size, random.choice(self.colors), random.uniform(1, 1.5))]
		# self.update()
		self.speed = 6 - self.options['speed']

	def update(self):
		"""Main update routine"""
		if self.running:
			# Clear canvas if needed
			# self.canvas.delete('all')
			self.speed -= 1
			if self.speed == 0:
				self.speed = 6 - self.options['speed']
				for char in self.chars[:]:
					char.tick()
					if char.dead() and char in self.chars: self.chars.remove(char)

			# print(len(self.chars))
			# self.running = False

	def delChilds(self, masterId):
		n = 0
		for char in self.chars[:]:
			if char.masterId == masterId:
				self.chars.remove(char)
				n += 1
		return n

class TkScreenSaver:
	"""Screensaver differs from App that it need not create main toplevel window
	but using those from tkscrsavers.py that calls this screensaver"""
	def __init__(self, scrsaver, options, timer=0):
		"""
			Init application then run game loop.
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
