"""
This is adaption from The Coding Train code
for Coding Challenge #69: Evolutionary Steering Behaviors
Youtube video at https://www.youtube.com/watch?v=ykOcaInciBI (Part 4)
Original code location: https://editor.p5js.org/codingtrain/sketches/xgQNXkxx1

Adaption from Javascript/P5.js to Python/Tkinter
by Beotiger 2024-03-26 - 2024-03-31

Added some new features and limitations.
Vehicle drawings are changed to hollow triangles,
with dynamic angles of their tails. When last vehicle dies the game restarts.
So there is no need to create more food and poison
when there is maximum value of it on the field.

But the whole steering engine stayed intact as far as I feel it.

While in test mode you can press Space bar key to pause animation,
left mouse click to add new vehicle at mouse position.
And right mouse click will turn on/off debug mode for one vehicle under mouse cursor.
"""

from tkinter import *
import random
import math

# Default width and height of canvas when testing screensaver
WIDTH = 800
HEIGHT = 600

# Default settings
app_name = 'Evolutionary Steering'
app_version = '1.0'
app_authors = 'The Coding Train'
app_url = 'https://www.youtube.com/watch?v=ykOcaInciBI'
app_date = '2017-04-27'
app_license = 'MIT'
# Default options
app_options = {
	# Background of canvas
	'background': 'black',
	# number of vehicles
	'vehicles': 15,
	# Vehicle size
	'vehicleRadius': 15,
	# Vehicle width
	'vehicleWidth': 2,
	# Vehicle angle
	'vehicleAngle': 40,
	# Should we shrink a vehicle angle depending on its velocity
	'shrink': True,
	# Maximum number of food
	'food': 40,
	# Maximum number of poison
	'poison' : 20,
	# sizes of food & poison
	'foodRadius': 7,
	'poisonRadius': 4,
	# Color of food
	'foodColor': '#00FF00',
	# Color of poison
	'poisonColor': '#FF0000',
	# If we want more info about every vehicle... Answer: No)
	'debug': False
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
		return Vector()
	# distance
	def dist(self, v): return math.sqrt((self.x - v.x) * (self.x - v.x) + (self.y - v.y) * (self.y - v.y))
	# Set desired magnitude. Note: it is left-sided function
	def setMag(self, n):
		self.normalize().mult(n)
		return self
	# Multiply vector components by n - do not mix with mul
	def mult(self, n):
		self.x *= n
		self.y *= n
		return self
	def limit(self, limit):
		if self.mag() > limit: v = self.normalize().mul(Vector(limit, limit))
		else: v = self
		return v
	# Calculates the angle a 2D vector makes with the positive x-axis
	def heading(self): return math.atan2(self.y, self.x)
	def __str__(self) -> str:
		return f'Vector({round(self.x, 2)}, {round(self.y, 2)})'

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

class Vehicle:
	"""Individual vehicle class"""
	def __init__(self, app, x, y, dna=None):
		"""Init vehicle. @dna used when clone method works"""
		self.app = app
		# Zero accelaration at start
		self.acceleration = Vector()
		# Random vehicle speed
		self.velocity = Vector(random.randint(-2, 2), random.randint(-2, 2))
		# Vehicle position
		self.pos = Vector(x, y)
		# Vehicle radius
		self.r = app.options['vehicleRadius']
		# Vehicle angle
		self.phi = app.options['vehicleAngle']
		self.maxspeed = 5
		self.maxforce = 0.5
		# Why vehicle should die?
		self.health = 1
		# Use debug mode only for one on middle mouse click
		self.selected = 0

		self.dna = [0, 0, 0, 0]
		# Just a magic number. Ask Dan about it ;)
		mr = 0.01 # Do not ask me why it's there and what is it (Beotiger)
		if dna is None:
			# Food weight
			self.dna[0] = random.randint(-2, 2)
			# Poison weight
			self.dna[1] = random.randint(-2, 2)
			# Food perception
			self.dna[2] = random.randint(0, 100)
			# Poision Percepton
			self.dna[3] = random.randint(0, 100)
		else:
			# Mutation
			self.dna[0] = dna[0]
			if random.random() < mr:
				self.dna[0] += random.uniform(-0.1, 0.1)
			self.dna[1] = dna[1]
			if random.random() < mr:
				self.dna[1] += random.uniform(-0.1, 0.1)
			self.dna[2] = dna[2]
			if random.random() < mr:
				self.dna[2] += random.randint(-10, 10)
			self.dna[3] = dna[3]
			if random.random() < mr:
				self.dna[3] += random.randint(-10, 10)

	def update(self):
		"""Method to update location"""
		self.health -= 0.005
		# Update velocity
		self.velocity = self.velocity.add(self.acceleration)
		# Limit speed
		self.velocity = self.velocity.limit(self.maxspeed)
		self.pos = self.pos.add(self.velocity)
		# Reset accelerationelertion to 0 each cycle
		self.acceleration = self.acceleration.mult(0)

	def applyForce(self, force):
		"""We could add mass here if we want A = F / M"""
		self.acceleration = self.acceleration.add(force)

	def clone(self):
		"""Try to clone vehicle with low chance"""
		if random.random() < 0.005:
			return Vehicle(self.app, self.pos.x, self.pos.y, self.dna)
		return None

	def behaviors(self, good, bad):
		"""Main updating vehicles positions function"""
		steerG = self.eat(good, 0.2, self.dna[2])
		steerB = self.eat(bad, -1, self.dna[3])
		self.applyForce(steerG.mult(self.dna[0]))
		self.applyForce(steerB.mult(self.dna[1]))

	def eat(self, foodpois, nutrition, perception):
		"""Search and eat food/poison as foodpois"""
		record = 1000000 # Maximum number we can afford
		closest = None
		for i in range(len(foodpois) - 1, -1, -1):
			d = self.pos.dist(foodpois[i])
			if d < self.maxspeed:
				foodpois.pop(i)
				self.health += nutrition
			else:
				if d < record and d < perception:
					record = d
					closest = foodpois[i]
					# print(f'Found closest={closest}')
		# This is the moment of eating!
		if closest != None:
			return self.seek(closest)
		return Vector()

	def seek(self, target):
		"""A method that calculates a steering force towards a target
				STEER = DESIRED MINUS VELOCITY"""
		# A vector pointing from the location to the target scaled to maximum speed
		desired = target.sub(self.pos).setMag(self.maxspeed)
		# Steering = Desired minus velocity limited to maximum steering force
		steer = desired.sub(self.velocity).limit(self.maxforce)
		#self.applyForce(steer) - we apply force in behaviors() method
		return steer

	def dead(self):
		return self.health <= 0

	def draw(self):
		# Draw a triangle rotated in the direction of velocity
		heading = self.velocity.heading()
		angle = math.degrees(heading) + 90 # + math.pi / 2
		# print(f'Velocity={self.velocity}')
		# print(f'angle={round(angle, 1)}°')
		# vehicle radius
		"""push()
		translate(self.pos.x, self.pos.y)
		rotate(angle)"""
		if self.app.options['debug'] or self.selected:
			# Radians start counting from east not north side of the circle
			rangle = math.radians(angle) + math.pi / 2
			fc = self.app.options['foodColor']
			pc = self.app.options['poisonColor']
			self.app.drawLine(fc, self.pos.x, self.pos.y, self.pos.x, self.pos.y - self.dna[0] * 25, rangle, width=3)
			self.app.create_circle(self.pos.x, self.pos.y, self.dna[2] * 2, outline=fc, width=2)
			self.app.drawLine(pc, self.pos.x, self.pos.y, self.pos.x, self.pos.y - self.dna[1] * 25, rangle, width=2)
			self.app.create_circle(self.pos.x, self.pos.y, self.dna[3] * 2, outline=pc, width=2)

		hlt = int(self.health * 100) % 101
		color = self.app.colors[hlt]
		# Shrink vehicles angle when they are too fast
		phi = self.phi - self.velocity.mag() * 5 if self.app.options['shrink'] else self.phi
		if phi < 5: phi = 5 # 5 degrees is a minimum
		# Angle of our triangle in degrees
		self.app.drawTri(color, self.pos.x, self.pos.y, self.r, phi, angle, self.app.options['vehicleWidth'])
		# @2024_04_01_1139 add helth info of selected vehicle
		if self.selected:
			self.app.canvas.create_text(16, 16, text=str(round(self.health, 2)), fill='white', font=('Arial', 16), anchor=NW)

	def boundaries(self):
		d = 25
		desired = None
		if self.pos.x < d:
			desired = Vector(self.maxspeed, self.velocity.y)
		elif self.pos.x > self.app.w - d:
			desired = Vector(-self.maxspeed, self.velocity.y)
		if self.pos.y < d:
			desired = Vector(self.velocity.x, self.maxspeed)
		elif self.pos.y > self.app.h - d:
			desired = Vector(self.velocity.x, -self.maxspeed)
		if desired != None:
			desired.normalize().mult(self.maxspeed)
			steer = desired.sub(self.velocity).limit(self.maxforce)
			self.applyForce(steer)

class Main:
	"""Main canvas class where all animation occurs"""
	def __init__(self, canvas, options):
		self.canvas = canvas
		# Set default options
		self.options = dict(app_options)
		# Change these options from options parameter
		for key, val in options.items():
			self.options[key] = val
				# start with running animations
		self.running = True
		self.state = False
		# Set background for the canvas
		self.canvas.config(bg=self.options['background'])
		# Mouse event listeners which used in test mode mostly
		self.canvas.bind_all('<space>', self.pause)
		self.canvas.bind_all('<F11>', self.toggle_fullscreen)
		self.canvas.bind('<1>', self.addVehicle)
		self.canvas.bind('<3>', self.selectVehicle)
		self.canvas.bind('<Leave>', self.leave)
		self.canvas.bind('<Configure>', self.resize)
		self.canvas.bind('<Destroy>', self.game_over)
		# Gradient colors for vehicles depepend on their dna information
		colors = GradientColor.linear_gradient(self.options['poisonColor'], self.options['foodColor'], 101)
		self.colors = list(colors['hex'])
		self.foodRadius = self.options['foodRadius']
		self.poisonRadius = self.options['poisonRadius']
		# Init animation first time
		self.init()
	def selectVehicle(self, evt):
		"""Selects vehicle under mouse cursor position to see its debug information
		@2024_04_01_1032 added by Beotiger and co."""
		mousePos = Vector(evt.x, evt.y)
		min = 100000
		vehicle = -1
		for i in range(len(self.vehicles)):
			self.vehicles[i].selected = 0
			dist = self.vehicles[i].pos.dist(mousePos)
			if min > dist:
				vehicle = i
				min = dist
		# Select only nearest vehicle if any
		if vehicle >= 0 and self.vehicles[vehicle].pos.dist(mousePos) < self.options['vehicleRadius'] * 2:
			self.vehicles[vehicle].selected = 1

	# Some Tk canvas draw primitives wrappers
	def drawLine(self, color, x1, y1, x2, y2, angle=0.0, **kwargs):
		"""Draw a line on the canvas with specified color"""
		# @2024_03_27_0015 Added angle parameter
		if angle:
			# Find distance between two points of line
			r = int(math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)))
			# And calculate new vertices for opposite point
			x2 = x1 + r * math.cos(angle)
			y2 = y1 + r * math.sin(angle)
		return self.canvas.create_line(x1, y1, x2, y2, capstyle=ROUND, fill=color, **kwargs)
	def create_circle(self, x, y, r, **kwargs):
		"""Draw circle at x,y coords with radius r, kwargs - more optional Tk parameters"""
		return self.canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)
	def drawTri(self, color, x, y, r, phi, di, width=2):
		"""@2024_03_27_2337 Draw triangle with r pixels size,
		phi - angle between two lines, di - angle to the target
		Angles are in degrees here"""
		x1, y1 = x, y + r * 2
		self.drawLine(color, x, y, x1, y1, math.radians(phi + di) + math.pi / 2, width=width)
		self.drawLine(color, x, y, x1, y1, math.radians(-phi + di) + math.pi / 2, width=width)
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
		# Get new dimensiions
		nw, nh = self.canvas.master.winfo_width(), self.canvas.master.winfo_height()
		# and recreate canvas size accordingly
		self.canvas.config(width=nw, height=nh)
		# And init animation anew
		self.init()
	# Can be called directly or as an event binding
	def pause(self, evt=None):
		"""Pause/resume animation"""
		self.running = not self.running
	# Can be called directly or as an event binding
	def game_over(self, evt=None):
		"""Stop animation"""
		self.running = False

	def randXY(self):
		"""Return Vector as random coordinates in sizes of screen"""
		return Vector(random.randint(0, self.w - 1), random.randint(0, self.h - 1))
	def addVehicle(self, evt):
		"""Add new vehicle (on left mouse click as a rule)"""
		# coord = self.randXY()
		self.vehicles.append(Vehicle(self, evt.x, evt.y))

	def init(self):
		"""Initialise vehicles"""
		# Store new width/height of the canvas
		self.w, self.h = self.canvas.winfo_width(), self.canvas.winfo_height()
		self.vehicles = []
		self. food = []
		self.poison = []
		# Create vehicles, food and posions
		for _ in range(self.options['vehicles']):
			coord = self.randXY()
			self.vehicles.append(Vehicle(self, coord.x, coord.y))
		for _ in range(self.options['food']):
			self.food.append(self.randXY())
		for _ in range(self.options['poison']):
			self.poison.append(self.randXY())
		self.update()

	def update(self):
		"""Main update routine"""
		if self.running:
			# Clear canvas
			self.canvas.delete(ALL)
			# Chance to spawn more food and posion
			if len(self.food) < self.options['food'] and random.random() < 0.1:
				self.food.append(self.randXY())
			if len(self.poison) < self.options['poison'] and random.random() < 0.1:
				self.poison.append(self.randXY())
			# Draw food and poison as circles in 4px radius
			for i in range(len(self.food)):
				self.create_circle(self.food[i].x, self.food[i].y, self.foodRadius, fill=self.options['foodColor'])
			for i in range(len(self.poison)):
				self.create_circle(self.poison[i].x, self.poison[i].y, self.poisonRadius, fill=self.options['poisonColor'])
			for v in self.vehicles[:]:
				v.boundaries()
				v.behaviors(self.food, self.poison)
				v.update()
				v.draw()
				newVehicle = v.clone()
				if len(self.vehicles) < self.options['vehicles'] and newVehicle is not None:
					self.vehicles.append(newVehicle)
				# When vehicle is dead place food or poison in its place as a grave)
				if v.dead():
					if random.randint(1, 10) < 7:
						self.food.append(Vector(v.pos.x, v.pos.y))
					else:
						self.poison.append(Vector(v.pos.x, v.pos.y))
					self.vehicles.remove(v)
					# If we lost last one start anew
					if len(self.vehicles) < 1:
						self.init()

class TkScreenSaver:
	"""Screensaver"""
	def __init__(self, scrsaver, options, timer=0):
		"""Init application then run game loop"""
		self.root = scrsaver.win
		self.monitor = scrsaver.monitor
		self.root.protocol('WM_DELETE_WINDOW', self.fin)
		# Use timer to stop animation after timer * 1000 (ms)
		self.timer = self.root.after(timer * 1000, self.fin) if timer else None
		# Create canvas without borders and with hidden mouse cursor
		self.canvas = Canvas(self.root, width=self.monitor.width, height=self.monitor.height,
													bd=0, relief='ridge', highlightthickness=0, cursor='none')
		self.canvas.pack()
		self.animate = Main(self.canvas, options)
		self.run()

	def run(self, evt=None):
		"""Run animation while not any key pressed or mouse move"""
		self.animate.update()
		self.root.update_idletasks()
		self.root.update()
		self.afterId = self.root.after(25, self.run)

	def fin(self, evt=None):
		"""Finalize animation: set it to false and close window"""
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
		self.win.protocol('WM_DELETE_WINDOW', self.fin)
		self.win.bind('<KeyPress-Escape>', self.fin)
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
		"""Finalize animation: set it to false and close window"""
		self.animate.running = False
		self.win.after_cancel(self.afterId)
		self.win.destroy()

# Test application if not in module mode
if __name__ == '__main__':
	App(app_options)
