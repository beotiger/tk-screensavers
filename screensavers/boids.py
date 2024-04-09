"""
Implementaion of boids behaviour in Python using Tkinter canvas.

Based on code in Javasctipt/HTML5 canvas by Mike Christensen
from https://github.com/MikeC1995/BoidsCanvas

While testing app you can add new boid by left mouse click and select any boid
to see its visible radius (i.e. how far boid can see) by right mouse click.

And you can use interactive mode while interactive option is True so that
any boid in visible radius would follow mouse cursor.

Also pressing Space bar key pauses/resumes animation.

There is new mechanic using chasing points when a boid disrespects any flocking and interactive rules
and starts seeking one random point on the screen until it catches it up.

Chasing points can be spawned for any boid on every 100 cycles with 5% chance.
You can enable/disable this mode through useChasePoints option value (default: True).
Or/and you can set showChasePoints option to False not to see these annoying chasing points any more ;)

Note: chasing points would be spawned for any boid that overgoes screen boundaries
when bounce option set to True disregarding useChasePoints option value.

Final adaption by Beotiger (c) 2024_03_30 22:25
"""

import math
import random
from tkinter import *

WIDTH = 800
HEIGHT = 650

# Default screensaver settings
app_name = 'Tk Boids'
app_version = '1.0.0'
app_url = 'https://github.com/beotiger/tk-screensavers'
app_date = '2024-03-22'
app_authors = 'Beotiger & co.'
app_license = 'MIT'
# Default screensaver options
app_options = {
		'background': '#1a252f',
		'boidColours': ['#FFF', '#FBF', '#F8F', '#F4F'],
		# Size/radius of boids in pixels
		'boidRadius': 40,
		# Boid represantation: 'boid', 'ball', 'any'
		'vid': 'boid',
		# Number of boids: 'low', 'medium', 'high'
		'density': 'low',
		# Or use this precise number (if 0 density will be used)
		'numboids': 0,
		# Max speed of boids
		'speed': 2,
		# Should boids follow mouse cursor position
		'interactive': False,
		# Should boids group each other by color
		'colorize': False,
		# If spawned boids be mixed sizes
		'mixedSizes': False,
		# If boid should bounce off screen edges
		'bounce': False,
		# How far boids will see (in pixels)
		'visibleRadius': 200,
		# How far boids may align from each others (in pixels)
		'separationDist': 40,
		# If we should use/watch new chase mechanic for our boids
		'useChasePoints': True,
		'showChasePoints': True
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
	# normalize
	def norm(self):
		mag = self.mag()
		if mag != 0: return Vector(self.x / mag, self.y / mag)
		return Vector(0, 0)
	# distance
	def dist(self, v): return math.sqrt((self.x - v.x) * (self.x - v.x) + (self.y - v.y) * (self.y - v.y))
	def limit(self, limit):
		if self.mag() > limit: v = self.norm().mul(Vector(limit, limit))
		else: v = self
		return v
	# Multiply vector components by n - do not mix with mul
	def mult(self, n):
		self.x *= n
		self.y *= n
		return self
	def __str__(self) -> str:
		return f'V({round(self.x, 2)}, {round(self.y, 2)})'

class Boid:
	"""Individual boid class"""
	def __init__(self, parent, position, velocity, size, vid, colour):
		"""Initialise boid parameters
		 parent refers to BoidsCanvas"""
		self.position = Vector(position.x, position.y)
		self.velocity = Vector(velocity.x, velocity.y)
		self.acceleration = Vector()
		self.speed = parent.options['speed']
		self.size = size
		self.vid = 'boid' if vid == 'boid' else 'ball' if vid == 'ball' else random.choice(['boid', 'ball'])
		self.colour = colour
		self.parent = parent
		# @2024_02_15_1859 let us select a boid
		self.selected = 0
		# @2024_03_28_1232 added chase vector and frames - frame counter
		self.chase = None
		self.frames = 0

	def drawAsABall(self):
		"""Draw boid in ball shape"""
		self.parent.create_circle(
			self.position.x, self.position.y,
			self.parent.options['boidRadius'] * self.size, fill=self.colour)

	def drawAsABoid(self):
		"""Draw boid in boid shape)"""
		x, y = self.position.x, self.position.y
		speed = self.velocity.mag()
		# @2024_03_21_1617 draw boid only if its speed is not zero
		if speed != 0:
			lx = int((self.velocity.x * self.size * self.parent.options['boidRadius']) / speed)
			ly = int((self.velocity.y * self.size * self.parent.options['boidRadius']) / speed)
			xHead, yHead = x + (lx >> 1), y + (ly >> 1)
			xEye, yEye = x, y
			xTail, yTail = x - (lx >> 2), y - (ly >> 2)
			xLeft, yLeft = x - ((lx + ly) >> 1), y - ((ly - lx) >> 1)
			xRight, yRight = x - ((lx - ly) >> 1), y - ((ly + lx) >> 1)
			poly = (xLeft, yLeft, xTail, yTail, xRight, yRight, xHead, yHead, xLeft, yLeft)
			self.parent.canvas.create_polygon(poly, outline=self.colour, fill='')
			# self.parent.drawLine(self.colour, xLeft, yLeft, xTail, yTail)
			# self.parent.drawLine(self.colour, xRight, yRight, xTail, yTail)
			# self.parent.drawLine(self.colour, xLeft, yLeft, xHead, yHead)
			# self.parent.drawLine(self.colour, xRight, yRight, xHead, yHead)
			# Draw an eye of the boid
			self.parent.setPixel(self.colour, xEye, yEye)

	def drawVisibleRange(self):
		"""@2024_02_15_1902 draw circle of visible range around selected boid
				only for boid that was forced selected"""
		if self.selected == 1:
			self.parent.create_circle(
				self.position.x, self.position.y,
				self.parent.options['boidRadius'] * self.size + self.parent.options['visibleRadius'],
				outline=self.colour, width=2)
		if self.chase is not None and self.parent.options['showChasePoints']:
			self.parent.create_circle(
				self.chase.x, self.chase.y, (self.frames % 5) + 1, fill=self.colour)

	def draw(self):
		"""Can draw boid in two shapes: like a triangle with the head ahead or like a ball"""
		if self.vid == 'ball':
			self.drawAsABall()
		else:
			self.drawAsABoid()
		if self.selected:
			self.drawVisibleRange()

	def update(self):
		"""Update the boid positions according to Reynold's rules.
	 			Called on every frame"""
		self.frames += 1
		if self.chase is not None:
			# Chasing some point
			# If we got chase point stop chasing
			if self.position.dist(self.chase) < self.size * 2:
				self.chase = None
				self.speed = self.parent.options['speed']
				if self.selected == 2:
					self.selected = 0
			else: self.applyForce(self.seek(self.chase))
		else:
			v1 = self.cohesion()
			v2 = self.separation()
			v3 = self.alignment()
			v4 = self.interactivity()
			# Weight rules to get best behaviour
			v1.mult(1.2)
			v2.mult(1.8)
			v3.mult(1)
			v4.mult(1.8)
			self.applyForce(v1).applyForce(v2).applyForce(v3).applyForce(v4)
		self.velocity = self.velocity.add(self.acceleration).limit(self.speed)
		self.position = self.position.add(self.velocity)
		self.acceleration.mult(0)
		self.borders()
		# @2024_03_28_1248 Chance to chase random point
		if self.chase is None and self.parent.options['useChasePoints'] and self.frames % 100 == 0 and random.random() < 0.05:
			self.chase = Vector(random.randint(0, self.parent.w), random.randint(0, self.parent.h))
			# Add speed to boid which chases something
			self.speed *= 2.5
			if self.selected != 1: self.selected = 2

	def applyForce(self, force):
		"""Adjust the acceleration by applying a force, using A = F / M
				with M = boid size so that larger boids have more inertia"""
		self.acceleration = self.acceleration.add(
			force.div(Vector(self.size, self.size))
		)
		return self

	def borders(self):
		"""Rules for window edges behaviour"""
		if self.parent.options['bounce']:
			# Implement bouncing behaviour
			if self.position.x < 0 or self.position.x > self.parent.w:
				self.velocity.x = -self.velocity.x
				self.chase = Vector(random.randint(0, self.parent.w), random.randint(0, self.parent.h))
				self.speed *= 2.5
			if self.position.y < 0 or self.position.y > self.parent.h:
				self.velocity.y = -self.velocity.y
				self.chase = Vector(random.randint(0, self.parent.w), random.randint(0, self.parent.h))
				self.speed *= 2.5
		else:
			# Implement torus boundaries
			if self.position.x < 0: self.position.x = self.parent.w
			if self.position.y < 0: self.position.y = self.parent.h
			if self.position.x > self.parent.w: self.position.x = 0
			if self.position.y > self.parent.h: self.position.y = 0

	def seek(self, target):
		"""Calculate a force to apply to a boid to steer
			it towards a target position"""
		desired = target.sub(self.position).norm()
		desired.mult(self.speed)
		steer = desired.sub(self.velocity)
		return steer.limit(self.parent.maxForce)

	# BOIDS FLOCKING RULES
	def cohesion(self):
		"""Cohesion rule: steer towards average position of local flockmates"""
		sum = Vector(0, 0)	# average flockmate position
		count = 0 					# number of local flockmates
		# For each boid close enough to be seen...
		for i in range(len(self.parent.boids)):
			d = self.position.dist(self.parent.boids[i].position)
			if d > 0 and d < self.parent.options['visibleRadius']:
				sum = sum.add(self.parent.boids[i].position)
				count += 1
		if (count > 0):
			# Calculate average position and return the force required to steer towards it
			sum = sum.div(Vector(count, count))
			sum = self.seek(sum)
			return sum
		return Vector(0, 0)

	def separation(self):
		"""Separation rule: steer to avoid crowding local flockmates"""
		steer = Vector()	# average steer
		count = 0							# number of flockmates considered "too close"
		# For each boid which is too close, calculate a vector pointing
		# away from it weighted by the distance to it
		for i in range(len(self.parent.boids)):
			d = self.position.dist(self.parent.boids[i].position) - self.size * self.parent.options['boidRadius']
			# @2024_04_07_2114 colorize separation added
			if self.colour != self.parent.boids[i].colour:
				colorize = self.parent.options['boidRadius'] * 10 * int(self.parent.options['colorize'])
			else:
				colorize = 0
			if d > 0 and d < self.parent.options['separationDist'] + colorize:
				diff = self.position.sub(self.parent.boids[i].position)
				diff = diff.norm()
				diff = diff.div(Vector(d, d))
				steer = steer.add(diff)
				count += 1
		# Calculate average
		if count > 0:
			steer = steer.div(Vector(count, count))
		# Steering = Desired - Velocity
		if steer.mag() > 0:
			steer = steer.norm()
			steer = steer.mul(Vector(self.speed, self.speed))
			steer = steer.sub(self.velocity)
			steer = steer.limit(self.parent.maxForce)
		return steer

	def alignment(self):
		"""Alignment rule: steer toward average heading of local flockmates"""
		sum = Vector(0, 0)	# Average velocity
		count = 0						# number of local flockmates
		# For each boid which is close enough to be seen
		for i in range(len(self.parent.boids)):
			d = self.position.dist(self.parent.boids[i].position)
			if d > 0 and d < self.parent.options['visibleRadius']:
				sum = sum.add(self.parent.boids[i].velocity)
				count +=1
		if count > 0:
			# Calculate average and limit
			sum = sum.div(Vector(count, count)).norm().mul(Vector(self.speed, self.speed))
			# Steering = Desired - Velocity
			steer = sum.sub(self.velocity).limit(self.parent.maxForce)
			return steer
		return Vector(0, 0)

	def interactivity(self):
		"""If boids should follow mouse cursor"""
		if (
			self.parent.options['interactive'] and
			self.parent.mousePos and
			self.position.dist(self.parent.mousePos) < self.parent.options['visibleRadius']
		): return self.seek(self.parent.mousePos)
		return Vector(0, 0)

class BoidsCanvas:
	"""Main boids canvas class - director of all boids"""
	def __init__(self, canvas, options):
		self.canvas = canvas
		# get may be new width/height of the canvas
		self.w, self.h = canvas.winfo_width(), canvas.winfo_height()
		# Set customable boids parameters
		self.options = dict(app_options)
		# Determine min and max number of boids from possible options or default vaules
		self.minboids = options['minboids'] if 'minboids' in options else 1
		self.maxboids = options['maxboids'] if 'maxboids' in options else 100
		# Change default options values from parameter options if any
		for key, val in options.items():
			self.options[key] = val
		# For interactive mode
		self.mousePos = None
		self.boids = []
		# Maximum force! :)
		self.maxForce = 0.04
		self.init()

	def addBoid(self, evt):
		"""Add new boid on mouse left click"""
		if self.mousePos is not None and len(self.boids) < self.maxboids:
			self.newBoid(self.mousePos)
			self.showVars()
	def selectBoid(self, evt):
		"""Select boid to see its visible radius"""
		if self.mousePos is not None:
			min = 100000
			boid = -1
			for i in range(len(self.boids)):
				self.boids[i].selected = 0
				dist = self.boids[i].position.dist(self.mousePos)
				if min > dist:
					boid = i
					min = dist
			# Select only nearest boid if any
			if boid >= 0 and self.boids[boid].position.dist(self.mousePos) < self.options['separationDist']:
				self.boids[boid].selected = 1
	def motion(self, evt):
		"""Mouse move over canvas"""
		self.mousePos = Vector(evt.x, evt.y)
	def leave(self, evt):
		"""Mouse leaved canvas?"""
		self.mousePos = None
	def resize(self, evt):
		"""Resize canvas"""
		# print(evt.width, evt.height)
		# New width/height of resized window
		# print('Resize event was called!')
		nw, nh = self.canvas.master.winfo_width(), self.canvas.master.winfo_height()
		self.canvas.config(width=nw, height=nh)
		self.initialiseBoids()
	def pause(self, evt=None):
		"""Pause/resume animation"""
		self.running = not self.running
	def toggle_fullscreen(self, evt=None):
			"""Toggle full screen mode"""
			self.state = not self.state
			self.canvas.master.attributes('-fullscreen', self.state)
			self.canvas.config(bd=int(not self.state), highlightthickness=int(not self.state))

	def init(self):
		"""Init several options and canvas binds"""
		self.running = True
		# For full screen switch
		self.state = False
		# set background for the canvas
		self.canvas.config(bg=self.options['background'])
		self.canvas.bind_all('<space>', self.pause)
		# For screensaver mode do not bind more events to canvas
		if 'test' in self.options:
			self.canvas.focus_set()
			self.showVars()
			# Mouse event listeners
			self.canvas.bind('<Motion>', self.motion)
			self.canvas.bind('<Leave>', self.leave)
			self.canvas.bind('<1>', self.addBoid)
			self.canvas.bind('<3>', self.selectBoid)
			self.canvas.bind('<F11>', self.toggle_fullscreen)
		self.canvas.bind('<Configure>', self.resize)
		self.canvas.bind('<Destroy>', self.game_over)
		self.initialiseBoids()

	def initialiseBoids(self):
		"""Initialise boids according to options"""
		self.boids = []
		# Get may be changed width/height of the canvas
		self.w, self.h = self.canvas.winfo_width(), self.canvas.winfo_height()
		# Use option numboids value as number of boids
		# or option density high/medium/low if numboids == 0:
		denss = { 'high': 8000, 'medium': 15000, 'low': 30000 }
		dens = self.options['density']
		numboids = self.options['numboids']
		if numboids > 0:
			num = numboids
		else:
			num = (self.w * self.h) // denss[dens] if dens in denss else 20
		# Do not allow num exceeds allowed values
		if num < self.minboids:
			num = self.minboids
		elif num > self.maxboids:
			num = self.maxboids
		# print(f'Number of boids: {num}')
		for _ in range(num):
			position = Vector(random.randint(0, self.w), random.randint(0, self.h))
			self.newBoid(position)
		# self.update()

	def newBoid(self, position):
		"""Add new boid at @position with random velocity, color and size if mixedSizes option is true"""
		min_velocity, max_velocity = -5, 5
		velocity = Vector(
			random.uniform(min_velocity, max_velocity),
			random.uniform(min_velocity, max_velocity)
		)
		size = math.floor(random.random() * (3 - 1 + 1) + 1) if self.options['mixedSizes'] else 1
		colour = random.choice(self.options['boidColours'])
		self.boids.append(Boid(self, position, velocity, size, self.options['vid'], colour))

	def drawLine(self, colour, x1, y1, x2, y2):
		"""Draw a line on the canvas with specified color"""
		return self.canvas.create_line(x1, y1, x2, y2, width=1, capstyle=ROUND, fill=colour)

	def setPixel(self, c, x, y):
		"""Set one pixel as 1x1 rectangle"""
		return self.canvas.create_rectangle(x, y, x + 1, y + 1, outline=c, fill=c)

	def create_circle(self, x, y, r, **kwargs):
		"""Draw circle at x,y coords with radius r, kwargs - more optional Tk parameters"""
		return self.canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

	def update(self):
		"""Main update routine"""
		if self.running:
			# Clear canvas
			self.canvas.delete('all')
			# Update boids
			for i in range(len(self.boids)):
				self.boids[i].update()
			# Draw boids
			for i in range(len(self.boids)):
				self.boids[i].draw()
			# Print some statistics on the glass pane
			self.updateVars()

	def game_over(self, evt=None):
		"""Stop animations"""
		self.running = False

	def updateVars(self):
		"""TODO: Show current number of boids on the panel"""
		pass

	def showVars(self):
		"""TODO: Show current options values on the panel"""
		pass

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
		self.boids = BoidsCanvas(self.canvas, options)
		self.run()
	def run(self, evt=None):
		"""Run animation while not any key pressed or mouse move"""
		self.boids.update()
		self.root.update_idletasks()
		self.root.update()
		self.afterId = self.root.after(25, self.run)
	def fin(self, evt=None):
		"""Finalize animation: set it to false and close window"""
		self.boids.running = False
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
		# Create canvas for drawing some boids, in size as main window size
		self.canvas = Canvas(self.win, width=WIDTH, height=HEIGHT)
		self.canvas.pack()
		# Init BoidsCanvas - director of Boids class
		options['test'] = True
		self.boids = BoidsCanvas(self.canvas, options)
		# Close main window and exit on ESC keypress
		self.win.bind('<KeyPress-Escape>', self.fin)
		self.win.protocol('WM_DELETE_WINDOW', self.fin)
		self.run()
		self.win.mainloop()
	def run(self, evt=None):
		"""Running animations while window closed or ESC key pressed"""
		self.boids.update()
		self.win.update_idletasks()
		self.win.update()
		# 40 fps? )
		self.afterId = self.win.after(25, self.run)
	def fin(self, evt=None):
		"""Finalize animation: set it to false and close window"""
		self.boids.running = False
		self.win.after_cancel(self.afterId)
		self.win.destroy()

# Run only if not in module mode
if __name__ == '__main__':
	App(app_options)
