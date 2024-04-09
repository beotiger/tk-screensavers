"""
Simple rain drops demo from early The Coding Train samples
for Coding Challenge #4: Purple Rain in Processing - https://www.youtube.com/watch?v=KkyIDI6rQJI

Note: while in test mode pressing Space bar or left mouse click will stop/resume animation.

Adapted from HTML/Javascript/P5.js for Python/Tkinter
by Beotiger @2024_03_31 12:48
"""

import random
from tkinter import *

WIDTH = 600
HEIGHT = 800

# Default screensaver settings
app_name = 'Purple rain'
app_version = '1.0'
app_authors = 'The Coding Train'
app_url = 'https://www.youtube.com/watch?v=KkyIDI6rQJI'
app_date = '2016-04-25'
app_license = 'MIT'
# Default screensaver options
app_options = {
		# Background color
		'background': 'black',
		# How many drops we use
		'drops': 200,
		# Choose random gradient color from color1 to color2
		'color1': '#1A1BA2',
		'color2': '#AA2BE2'
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

class Drop:
	"""Single drop class"""
	def __init__(self, parent):
		self.parent = parent
		self.x = random.randint(0, self.parent.w)
		self.y = random.randint(-500, -50)
		self.z = random.randint(0, 20)
		self.len = self.map(self.z, 0, 20, 10, 20)
		self.yspeed = self.map(self.z, 0, 20, 1, 20)
		self.color = random.choice(self.parent.colors)

	def fall(self):
		self.y = self.y + self.yspeed
		grav = self.map(self.z, 0, 20, 0, 0.2)
		self.yspeed = self.yspeed + grav
		if self.y > self.parent.h:
			self.y = random.randint(-200, -100)
			self.yspeed = self.map(self.z, 0, 20, 4, 10)

	def show(self):
		thick = self.map(self.z, 0, 20, 3, 8)
		self.parent.drawLine(self.color, self.x, self.y, self.x, self.y + self.len, width=thick)

	# Some utility functions
	def constrain(self, n, low, high): return max(min(n, high), low)

	def map(self, n, start1, stop1, start2, stop2, withinBounds=True):
		newval = (n - start1) / (stop1 - start1) * (stop2 - start2) + start2
		if not withinBounds: return newval
		if start2 < stop2: return self.constrain(newval, start2, stop2)
		else: return self.constrain(newval, stop2, start2)

class Rain:
	"""Main rain canvas class - director of all rain drops"""
	def __init__(self, canvas, options):
		self.canvas = canvas
		# Set customable rain parameters
		self.options = dict(app_options)
		# Change default options values from parameter options if any
		for key, val in options.items():
			self.options[key] = val
		# create list of gradient colors
		colors = GradientColor.linear_gradient(self.options['color1'], self.options['color2'], 30)
		self.colors = list(colors['hex'])
		# start with running animations
		self.running = True
		# For full screen switch
		self.state = False
		# set background for the canvas
		self.canvas.config(bg=self.options['background'])
		# Mouse event listeners
		self.canvas.bind_all('<F11>', self.toggle_fullscreen)
		self.canvas.bind('<1>', self.pause)
		self.canvas.bind_all('<space>', self.pause)
		self.canvas.bind('<Configure>', self.resize)
		self.canvas.bind('<Destroy>', self.game_over)
		self.init()

	def toggle_fullscreen(self, evt=None):
			"""Toggle full screen mode"""
			self.state = not self.state
			self.canvas.master.attributes('-fullscreen', self.state)
			self.canvas.config(bd=int(not self.state), highlightthickness=int(not self.state))

	def resize(self, evt):
		"""Resize canvas"""
		nw, nh = self.canvas.master.winfo_width(), self.canvas.master.winfo_height()
		self.canvas.config(width=nw, height=nh)
		self.init()

	def pause(self, evt=None):
		"""Pause/resume animation"""
		self.running = not self.running

	def init(self):
		"""Initialise drops"""
		# Get new width/height of the canvas
		self.w, self.h = self.canvas.winfo_width(), self.canvas.winfo_height()
		self.drops = []
		[self.drops.append(Drop(self)) for _ in range(self.options['drops'])]
		# for _ in range(self.options['drops']):
		# 	self.drops.append(Drop(self))

	def drawLine(self, color, x1, y1, x2, y2, **kwargs):
		"""Draw a line on the canvas with specified color"""
		return self.canvas.create_line(x1, y1, x2, y2, capstyle=ROUND, fill=color, **kwargs)

	def update(self):
		"""Rain update routine"""
		if self.running:
			# Clear canvas
			self.canvas.delete('all')
			for drop in self.drops:
				drop.fall()
				drop.show()

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
		self.rain = Rain(self.canvas, options)
		self.run()

	def run(self, evt=None):
		"""Run animation while not any key pressed or mouse move"""
		self.rain.update()
		self.root.update_idletasks()
		self.root.update()
		self.afterId = self.root.after(25, self.run)

	def fin(self, evt=None):
		"""Finalize animation: set it to false and close window"""
		self.rain.running = False
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
		self.win.protocol('WM_DELETE_WINDOW', self.fin)
		self.canvas = Canvas(self.win, width=WIDTH, height=HEIGHT)
		self.canvas.pack()
		self.rain = Rain(self.canvas, options)
		self.run()
		self.win.mainloop()

	def run(self, evt=None):
		"""Run animation while not window closed or ESC key pressed"""
		self.rain.update()
		self.win.update_idletasks()
		self.win.update()
		# 40 fps? )
		self.afterId = self.win.after(25, self.run)

	def fin(self, evt=None):
		"""Finalize animation: set it to false and close window"""
		self.rain.running = False
		self.win.after_cancel(self.afterId)
		self.win.destroy()

# Test application when run directly
if __name__ == '__main__':
	App(app_options)
