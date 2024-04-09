"""
This code is adaption from Coder Space code from
his youtube video at https://www.youtube.com/watch?v=rzA8cZyisf8
Original code location: https://github.com/StanislavPetrovV/MATRIX-Digital-Rain/blob/master/main.py

It uses pygame (https://github.com/pygame/pygame)
but we redraw it on tkinter canvas with some limitations
for tkinter canvas has no alpha channel as far as I could find out.

@2024_03_31 11:24 adapted by Beotiger

Note: it uses font MS Mincho.ttf (https://learn.microsoft.com/en-us/typography/font-list/ms-mincho)
which should be available on your system while running this app/screensaver.
Font file MS Mincho.ttf is available with tkscrsavers.py application.

Note: while in test mode pressing Space bar or left mouse click will stop/resume animation.
"""

import random
from tkinter import *

WIDTH = 800
HEIGHT = 600

# Default screensaver settings
app_name = 'Matrix Digital Rain'
app_version = '1.0'
app_authors = 'StanislavPetrovV'
app_date = '2020-10-25'
app_url = 'https://github.com/StanislavPetrovV/MATRIX-Digital-Rain'
app_license = 'MIT'
# Default screensaver options
app_options = {
		# Background color
		'background': 'black',
		# Size of symbols
		'fontsize': 30,
		# Choose gradient color from color1 to color2
		# color0 used as a lighter color
		# Classic matrix colors are
		'color0': '#90EE90',
		'color1': '#28A028',
		'color2': '#28FF28',
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

class Symbol:
	"""Single symbol class"""
	def __init__(self, app, x, y, speed):
		"""@app is a Main class instance with canvas"""
		self.app = app
		self.x, self.y = x, y
		self.speed = speed
		self.value = random.choice(app.green_katakana)
		self.interval = random.randrange(5, 30)

	def draw(self, color):
		"""Update and draw symbol on the screen"""
		if not self.app.ticks % self.interval:
				self.value = random.choice(self.app.green_katakana if color == 'green' else self.app.lightgreen_katakana)
		self.y = self.y + self.speed if self.y < self.app.h else -self.app.options['fontsize']
		self.app.create_text(self.x, self.y, self.value[0], self.value[1], self.app.font)

class SymbolColumn:
	"""Column of symbols class"""
	def __init__(self, app, x, y):
		"""@app is a class Main instance"""
		fontsize = app.options['fontsize']
		column_height = random.randrange(8, 24)
		speed = random.randrange(5, 10)
		self.symbols = [Symbol(app, x, i, speed) for i in range(y, y - fontsize * column_height, -fontsize - 16)]
	def draw(self):
		"""Draw one symbol column"""
		[symbol.draw('green') if i else symbol.draw('lightgreen') for i, symbol in enumerate(self.symbols)]

class Main:
	"""Main canvas class"""
	def __init__(self, canvas, options):
		self.canvas = canvas
		# Set customable matrix parameters
		self.options = dict(app_options)
		# Change default options values from parameter options if any
		for key, val in options.items():
			self.options[key] = val
		# Start with running animations
		self.running = True
		# For full screen switch
		self.state = False
		# Set background for the canvas
		self.canvas.config(bg=self.options['background'])
		self.canvas.bind_all('<F11>', self.toggle_fullscreen)
		self.canvas.bind('<1>', self.click)
		self.canvas.bind_all('<space>', self.click)
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
	def click(self, evt=None):
		"""Mouse left-click - pause/resume animation"""
		self.running = not self.running

	def init(self):
		"""Initialise symbols"""
		# Get width/height of the canvas
		self.w, self.h = self.canvas.winfo_width(), self.canvas.winfo_height()
		self.font = ('Ms Mincho.ttf', self.options['fontsize'], 'normal')
		katakana = [chr(int('0x30a0', 16) + i) for i in range(96)]
		colors = GradientColor.linear_gradient(self.options['color1'], self.options['color2'], 30)['hex']
		lightgreen = self.options['color0']
		# self.colors = list(colors['hex'])
		self.green_katakana = [(char, (40, random.randrange(160, 256), 40)) for char in katakana]
		self.green_katakana = [(char, random.choice(colors)) for char in katakana]
		self.lightgreen_katakana = [(char, lightgreen) for char in katakana]
		self.symbol_columns = [SymbolColumn(self, x, random.randrange(-self.h, 0)) for x in range(0, self.w, self.options['fontsize'] + 12)]
		self.ticks = 0

	def create_text(self, x, y, text, fill, font, angle=0):
		self.canvas.create_text(x, y, text=text, fill=fill, font=font, angle=angle, anchor=NW)

	def update(self):
		"""Main update routine"""
		if self.running:
			# Clear canvas and draw all symbol columns
			self.canvas.delete('all')
			[symbol_column.draw() for symbol_column in self.symbol_columns]
			self.ticks += 1

	def game_over(self, evt=None):
		"""Stop animation"""
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
		self.matrix = Main(self.canvas, options)
		self.run()

	def run(self, evt=None):
		"""Running animations while any key pressed or mouse move"""
		self.matrix.update()
		self.root.update_idletasks()
		self.root.update()
		self.afterId = self.root.after(25, self.run)

	def fin(self, evt=None):
		"""Finalize animation: set it to false and close window"""
		self.matrix.running = False
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
		self.matrix = Main(self.canvas, options)
		self.run()
		self.win.mainloop()

	def run(self, evt=None):
		"""Run animation while not window closed or ESC key pressed"""
		self.matrix.update()
		self.win.update_idletasks()
		self.win.update()
		self.afterId = self.win.after(5, self.run)

	def fin(self, evt=None):
		"""Finalize animation: set it to false and close window"""
		self.matrix.running = False
		self.win.after_cancel(self.afterId)
		self.win.destroy()

# Test app if not in module mode
if __name__ == '__main__':
	App(app_options)
