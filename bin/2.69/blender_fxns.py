def set_object_active(obj):
	#obj.select = True
	bpy.context.scene.objects.active = obj

def transform_apply(objs, location=False, rotation=False, scale=False):
	bpy.ops.ed.undo_push()
	for obj in objs:
		obj.select = True
		bpy.context.scene.objects.active = obj
		bpy.ops.object.transform_apply(location=location, rotation=rotation, scale=scale)
		obj.select = False

def center(objs, x=True, y=True, z=True):
	bpy.ops.ed.undo_push()
	for obj in objs:
		movex = 0
		if x:
			movex = obj.dimensions.x / 2 * -1
		movey = 0
		if y:
			movey = obj.dimensions.y / 2 * -1
		movez = 0
		if z:
			movez = obj.dimensions.z / 2 * -1
		translate(obj, movex, movey, movez)
		obj.select = True
		bpy.context.scene.objects.active = obj
		bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
		obj.select = False

def rename(objs, count, name):
	bpy.ops.ed.undo_push()
	import random
	random.shuffle(objs)
	for i in range(count):
		obj = objs.pop()
		obj.name = "%s" % (name)

def union(aobject, bobject, operation='UNION'):
	print("Union: %s & %s" % (aobject, bobject))
	set_object_active(aobject)
	mod = aobject.modifiers.new('Modifier', 'BOOLEAN')
	mod.operation = operation
	mod.object = bobject
	bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)

def unionize(base, objs, operation='UNION'):
	for i in objs:
		if i != base:
				bpy.ops.ed.undo_push()
				union(base, i, operation=operation)

def dist_unionize(base, objs, operation='UNION'):
	for i in objs:
		if i != base:
				bpy.ops.ed.undo_push()
				union(i, base, operation=operation)

def matrix_unionize(bases, objs, operation='UNION'):
	if len(bases) != len(objs):
		raise Exception("Must have the same number of bases and objects: %s vs %s" % (len(bases), len(objs)))
	for b, o in zip(bases, objs):
		bpy.ops.ed.undo_push()
		union(b, o, operation=operation)

def get_filename(obj):
	return obj.name.replace(" ",  "_").lower()

def save_objects(objs, directory=None, namer=get_filename):
	for o in bpy.data.objects:
		o.select  = False
	for o in objs:
		o.select  = True
		bpy.context.scene.objects.active = o
		name = namer(o)
		bpy.ops.export_mesh.stl(filepath="%s/%s.stl" % (directory,  name))
		o.select  = False

def filter_objects(word):
		objs = []
		for i in list(bpy.data.objects):
				if i.name.find(word) > -1:
						objs.append(i)
		return objs

def filter_unhidden():
		objs = []
		for i in list(bpy.data.objects):
			if i.type in ['MESH']:
					if not i.hide:
							objs.append(i)
		return objs

def decimator(objs, ratio=0.25):
	for i in objs:
		set_object_active(i)
		mod = i.modifiers.new('Modifier', 'DECIMATE')
		mod.ratio = ratio
		bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)

def add_full_base(objs, distance=6.0, minimum=0.0, maximum=0.0):
	for obj in objs:
		obj.location = (0.0, 0.0, distance)
		move_verts_z(distance*-1, minimum, maximum)
		for v in obj.data.vertices:
			if v.co.z >= minimum and v.co.z <= maximum:
				v.co.z = v.co.z - distance

def hide_objects(objs, hide=True):
	for obj in objs:
		obj.hide = hide

def move_verts_x(obj, distance=6.0, minimum=0.0, maximum=0.0):
	for v in obj.data.vertices:
		if v.co.x >= minimum and v.co.x <= maximum:
			v.co.x = v.co.x + distance

def move_verts_y(obj, distance=6.0, minimum=0.0, maximum=0.0):
	for v in obj.data.vertices:
		if v.co.y >= minimum and v.co.y <= maximum:
			v.co.y = v.co.y + distance

def move_verts_z(obj, distance=6.0, minimum=0.0, maximum=0.0):
	for v in obj.data.vertices:
		if v.co.z >= minimum and v.co.z <= maximum:
			v.co.z = v.co.z + distance

def select_verts(obj, zmin=0.0, zmax=0.0):
	for v in obj.data.vertices:
		if v.co.z <= zmax and v.co.z >= zmin:
			v.select = True
		else:
			v.select = False

def move(obj, x=None, y=None, z=None):
	set_object_active(obj)
	if x != None:
		obj.location.x = x
	if y != None:
		obj.location.y = y
	if z != None:
		obj.location.z = z

def translate(obj, x=None, y=None, z=None):
	set_object_active(obj)
	if x != None:
		obj.location.x = x + obj.location.x
	if y != None:
		obj.location.y = y + obj.location.y
	if z != None:
		obj.location.z = z + obj.location.z

def set_rotation(obj, x=None, y=None, z=None):
	import math
	set_object_active(obj)
	#print("Set Rotation: [%s,%s,%s]" %(x,y,z))
	if x != None:
		obj.rotation_euler.x = math.radians(x)
	if y != None:
		obj.rotation_euler.y = math.radians(y)
	if z != None:
		obj.rotation_euler.z = math.radians(z)

def rotate(obj, x=None, y=None, z=None):
	import math
	set_object_active(obj)
	#print("Rotate: [%s,%s,%s]" %(x,y,z))
	if x != None:
		obj.rotation_euler.x = math.radians(x) + obj.rotation_euler.x
	if y != None:
		obj.rotation_euler.y = math.radians(y) + obj.rotation_euler.y
	if z != None:
		obj.rotation_euler.z = math.radians(z) + obj.rotation_euler.z

def set_scale(obj, x=None, y=None, z=None):
	set_object_active(obj)
	#print("Set Scale: [%s,%s,%s]" %(x,y,z))
	if x != None:
		obj.scale.x = x
	if y != None:
		obj.scale.y = y
	if z != None:
		obj.scale.z = z

def scale(obj, x=None, y=None, z=None):
	set_object_active(obj)
	#print("Scale: [%s,%s,%s]" %(x,y,z))
	if x != None:
		obj.scale.x = x + obj.scale.x
	if y != None:
		obj.scale.y = y + obj.scale.y
	if z != None:
		obj.scale.z = z + obj.scale.z

def prepare_blocks(name=None):
	if not name:
		name = "Block"
	blocks = filter_objects(name)
	import random
	import copy
	blocks = copy.copy(blocks)
	random.shuffle(blocks)
	for b in blocks:
		b.hide = True
		move(b, 0,0,0)
		set_scale(b, 0,0,0)
		set_rotation(b, 0,0,0)
	return blocks

class Block(object):
	def __init__(self, name=None,
			randscalex=0.0, randscaley=0.0, randscalez=0.0,
			randanglex=0.0, randangley=0.0, randanglez=0.0):
		self.__name = name
		self.__x = 0.0
		self.__y = 0.0
		self.__z = 0.0
		self.__scale_x = 1.0
		self.__scale_y = 1.0
		self.__scale_z = 1.0
		self.__rotation_x = 0.0
		self.__rotation_y = 0.0
		self.__rotation_z = 0.0
		self.__hide = False
		self.actualize()
	def get_block(self):
		return bpy.data.objects[self.__name]
	def move(self, x=None, y=None, z=None):
		if x != None:
			self.__x = x
		if y != None:
			self.__y = y
		if z != None:
			self.__z = z
		self.actualize()
	def scale(self, x=None, y=None, z=None):
		if x != None:
			self.__scale_x = x
		if y != None:
			self.__scale_y = y
		if z != None:
			self.__scale_z = z
		self.actualize()
	def rotate(self, x=None, y=None, z=None):
		if x != None:
			self.__rotation_x = x
		if y != None:
			self._rotation_y = y
		if z != None:
			self.__rotation_z = z
		self.actualize()
	def hide(self, hide=True):
		self.__hide = hide
		self.actualize()
	def stochastic_modification(self,
			randscalex=0.0, randscaley=0.0, randscalez=0.0,
			randanglex=0.0, randangley=0.0, randanglez=0.0):
		import random
		def get_mod(rand, mod, bound=1):
			if rand > 0.0:
				val = random.uniform(-1.0,1.0)
				if abs(val) < rand:
					print("%s %s" % (bound+val, mod))
					return (bound+val) * mod
				return None
		sx = get_mod(randscalex, self.__scale_x * .5)
		sy = get_mod(randscaley, self.__scale_y * .5)
		sz = get_mod(randscalez, self.__scale_z * .5)
		self.scale(sx,sy,sz)
		ax = get_mod(randanglex, 1.0, bound=0)
		ay = get_mod(randangley, 1.0, bound=0)
		az = get_mod(randanglez, 1.0, bound=0)
		self.rotate(ax,ay,az)
		self.actualize()
	def get_name(self):
		return self.__name
	def set_name(self, name):
		self.__name = name
		self.actualize()
	def bounding_box(self):
		return ((self.__x-self.__scale_x/2*10,self.__x+self.__scale_x/2*10),
			(self.__y-self.__scale_y/2*10,self.__y+self.__scale_y/2*10),
			(self.__z-self.__scale_z/2*10,self.__z+self.__scale_z/2*10))
	def actualize(self):
		if self.__name != None:
			move(self.get_block(), self.__x, self.__y, self.__z)
			set_scale(self.get_block(), self.__scale_x, self.__scale_y, self.__scale_z)
			set_rotation(self.get_block(), self.__rotation_x, self.__rotation_y, self.__rotation_z)
			self.get_block().hide = self.__hide
	def __str__(self):
		return "Block: %s [%s,%s,%s], s(%s,%s,%s) d{%s,%s,%s}" % (self.__name,
			self.__x, self.__y, self.__z,
			self.__scale_x, self.__scale_y, self.__scale_z,
			self.__rotation_x, self.__rotation_y, self.__rotation_z)
	def __repr__(self):
		return self.__str__()

class CurvedWall(object):
	def __init__(self, radius, width, height,
			blength=None, bwidth=None, height_count=8, bgap=1.0,
			mortar_height=None,
			xoffset=0.0, altxoff=False, altyoff=False,
			randscalex=0.0, randscaley=0.0, randscalez=0.0,
			randanglex=0.0, randangley=0.0, randanglez=0.0,
			testmeshes=None):
		import math
		self.radius = radius
		self.length = self.circle_segment()
		# http://stackoverflow.com/questions/1734745/how-to-create-circle-with-b%C3%A9zier-curves
		self.bezier_mult = 0.552284749831 #(4/3) * tan(pi/(2/n))
		self.wall = Wall(self.length, width, height,
			blength=blength, bwidth=bwidth, height_count=height_count, bgap=bgap,
			mortar_height=mortar_height,
			xoffset=xoffset, altxoff=altxoff, altyoff=altyoff,
			randscalex=randscalex, randscaley=randscaley, randscalez=randscalez,
			randanglex=randanglex, randangley=randangley, randanglez=randanglez,
			testmeshes=testmeshes)
		self.wall.subdivide_mortar()
		self.curve_name = None
		self.create_curve()
		self.adjust_curve()
	def circle_segment(self):
		import math
		return (math.pi * 2 * self.radius) / 4
	def create_curve(self):
		bpy.ops.curve.primitive_bezier_curve_add()
		curve = bpy.context.object
		self.curve_name = curve.name
		move(self.curve(), 0,0,0)
		self.curve().data.splines[0].bezier_points[0].co.x = 0
		self.curve().data.splines[0].bezier_points[0].co.y = 0
		self.curve().data.splines[0].bezier_points[0].co.z = 0
		self.curve().data.splines[0].bezier_points[1].co.x = self.radius
		self.curve().data.splines[0].bezier_points[1].co.y = self.radius
		self.curve().data.splines[0].bezier_points[1].co.z = 0
	def adjust_curve(self):
		self.curve().data.splines[0].bezier_points[0].handle_right.x = 0
		self.curve().data.splines[0].bezier_points[0].handle_left.x = 0
		self.curve().data.splines[0].bezier_points[0].handle_right.y = 1
		self.curve().data.splines[0].bezier_points[0].handle_left.y = -1
		self.curve().data.splines[0].bezier_points[1].handle_right.y = self.radius
		self.curve().data.splines[0].bezier_points[1].handle_right.x = self.radius+1
		self.curve().data.splines[0].bezier_points[1].handle_left.y = self.radius
		self.curve().data.splines[0].bezier_points[1].handle_left.x = self.radius-1
		self.curve().data.splines[0].bezier_points[0].handle_right.y = self.radius * self.bezier_mult
		self.curve().data.splines[0].bezier_points[0].handle_right.x = 0
		self.curve().data.splines[0].bezier_points[0].handle_left.y = -1 * self.radius * self.bezier_mult
		self.curve().data.splines[0].bezier_points[0].handle_left.x = 0
		self.curve().data.splines[0].bezier_points[1].handle_right.y = self.radius
		self.curve().data.splines[0].bezier_points[1].handle_right.x = self.radius + self.radius * self.bezier_mult
		self.curve().data.splines[0].bezier_points[1].handle_left.y = self.radius
		self.curve().data.splines[0].bezier_points[1].handle_left.x = self.radius - self.radius * self.bezier_mult
	def curve(self):
		return bpy.data.objects[self.curve_name]
	def create(self):
		self.wall.unionize()

class Wall(object):
	def __init__(self, length, width, height,
			blength=None, bwidth=None, height_count=8, bgap=1.0, mdepth=1.0, mortar_height=None,
			xoffset=0.0, altxoff=False, altyoff=False,
			alty=True,  altx=True,
			randscalex=0.0, randscaley=0.0, randscalez=0.0,
			randanglex=0.0, randangley=0.0, randanglez=0.0,
			testmeshes=None):
		blocks = prepare_blocks()
		self.block_names = [b.name for b in blocks]
		self.mortar_name = None
		self.length = length
		self.width = width
		self.height = height
		self.block_length = blength
		self.block_width = bwidth
		self.block_height = None
		self.height_count = height_count
		self.block_gap = bgap
		self.mortar_depth = mdepth
		self.mortar_height = self.height/2 - self.mortar_depth/2 - 0.01
		if mortar_height != None:
			self.mortar_height = mortar_height/2
		self.golden_ratio = (1 + 5 ** 0.5) / 2
		self._set_block_height()
		self._set_block_length()
		self._set_block_width()
		self.xoffset = xoffset
		self.altxoff = altxoff
		self.altyoff = altyoff
		self.altx = altx
		self.alty = alty
		self.randomized_scale_x = randscalex
		self.randomized_scale_y = randscaley
		self.randomized_scale_z = randscalez
		self.randomized_angle_x = randanglex
		self.randomized_angle_y = randangley
		self.randomized_angle_z = randanglez
		self.active_blocks = []
		self.testmeshes = []
		self.used_blocks = []
		self.failed_blocks = []
		if testmeshes != None:
			self.testmeshes = testmeshes
		self.build_wall()
	def _set_block_height(self):
		self.block_height = (self.height - self.height_count * self.block_gap) /  self.height_count
	def _set_block_length(self):
		if self.block_length == None:
			self.block_length = self.block_height * self.golden_ratio
	def _set_block_width(self):
		if self.block_width == None:
			self.block_width = self.block_height * self.golden_ratio
	def build_wall(self):
		self.create_mortar()
		for h in range(self.height_count):
			start_height = self.block_height/2.0 + h * (self.block_height + self.block_gap)
			xoff = (h % 2 != 0)
			if self.altxoff:
				xoff = not xoff
			yoff = (h % 2 != 0)
			if self.altyoff:
				yoff = not yoff
			if not self.altx:
				xoff = 0.0
			if not self.alty:
				yoff = 0.0
			self.build_level(start_height, xoff, yoff)
	def mortar(self):
		return bpy.data.objects[self.mortar_name]
	def get_next_name(self):
		if len(self.block_names) > 0:
			return self.block_names.pop(0)
		if len(self.used_blocks) > 0:
			import random
			used_block_names = [b.get_name() for b in self.used_blocks]
			self.used_blocks = []
			random.shuffle(used_block_names)
			self.block_names = used_block_names
	def create_mortar(self):
		mortar = None
		bpy.ops.mesh.primitive_cube_add()
		mortar = bpy.context.object
		mortar.name = "Mortar"
		self.mortar_name = mortar.name
		move(mortar,
			self.length/2 + self.xoffset,
			self.width/2,
			self.mortar_height - 0.005)
		set_scale(mortar,
			self.length/2 - self.mortar_depth,
			self.width/2 - self.mortar_depth,
			self.mortar_height)
	def subdivide_mortar(self):
		mortar = self.mortar()
		set_object_active(mortar)
		cuts = max([int(self.length), int(self.width), int(self.height)])
		bpy.ops.object.editmode_toggle()
		bpy.ops.mesh.subdivide(number_cuts=(cuts + 1))
		bpy.ops.object.editmode_toggle()
	def build_level(self, start_height, xoff, yoff):
		ystart = 0.0
		yfirst = self.block_width
		if yoff:
			yfirst = (self.block_width + self.block_gap) / 2
		while ystart < self.width:
			block_width = self.block_width
			if yfirst != None:
				block_width = yfirst
				yfirst = None
			if (ystart + block_width + 3) > self.width:
				block_width = self.width - ystart
			start_width = ystart + block_width/2
			self.build_line(start_width, block_width, start_height, xoff)
			ystart += block_width + self.block_gap
	def build_line(self, start_width, block_width, start_height, xoff):
		import math
		retblocks = []
		xstart = 0.0
		xfirst = self.block_length
		if xoff:
			xfirst = (self.block_length + self.block_gap) / 2
		while xstart < self.length:
			b = Block(self.get_next_name())
			b.hide(False)
			block_length = self.block_length
			if xfirst != None:
				block_length = xfirst
				xfirst = None
			if (xstart + self.block_length + 3) > self.length:
				block_length = self.length - xstart
			b.scale(block_length/10.0, block_width/10.0, self.block_height/10.0)
			b.stochastic_modification(
				self.randomized_scale_x, self.randomized_scale_y, self.randomized_scale_z,
				self.randomized_angle_x, self.randomized_angle_y, self.randomized_angle_z)
			b.move(block_length/2.0 + xstart + self.xoffset, start_width, start_height)
			if self.filter_bounding_box(b):
				b.hide(True)
				self.block_names.append(b.get_name())
			else:
				self.active_blocks.append(b)
			xstart += block_length + self.block_gap
	def filter_bounding_box(self, block):
		mortar_bb = self.mortar_bounding_box()
		block_bb = block.bounding_box()
		result = inside_bounding_box(mortar_bb, block_bb)
		return result
	def mortar_bounding_box(self):
		return (1.0,self.length-2),(1.0,self.width-2),(-0.01,self.height-1)
	def unionize(self,retries=0):
		while len(self.active_blocks) > 0:
			block = self.active_blocks.pop(0)
			try:
				if block.get_name() == None:
					block.set_name(self.get_next_name())
				bpy.ops.ed.undo_push()
				block.hide(True)
				block.actualize()
				bpy.ops.ed.undo_push()
				vert_count = len(list(self.mortar().data.vertices))
				face_count = len(list(self.mortar().data.polygons))
				union(self.mortar(), block.get_block())
				if self.test_failed(vert_count, face_count, block):
					print("UNION FAILED: %s" % (block.get_block()))
					set_object_active(block.get_block())
					self.failed_blocks.append(block)
					bpy.ops.ed.undo()
				else:
					self.used_blocks.append(block)
			except Exception as e:
				self.failed_blocks.append(block)
				raise e
		self.recycle_failed()
		if retries > 0 and len(self.active_blocks) > 0:
			self.unionize(retries - 1)
	def recycle_failed(self):
		prepare_blocks()
		print("%s Failures" % len(self.failed_blocks))
		while len(self.failed_blocks) > 0:
			fb = self.failed_blocks.pop(0)
			self.block_names.append(fb.get_name())
			fb.set_name(self.get_next_name())
			self.active_blocks.append(fb)
	def test_failed(self, vert_count, face_count, block):
		new_vert_count = len(list(self.mortar().data.vertices))
		new_face_count = len(list(self.mortar().data.polygons))
		print("verts: %s -> %s, faces: %s -> %s" % (vert_count, new_vert_count, face_count, new_face_count))
		block_vert_count = len((list(block.get_block().data.vertices)))
		if (vert_count + 500) > new_vert_count:
			return True
		if face_count >= new_face_count:
			return True
		if (vert_count + int(block_vert_count * 0.9)) < new_vert_count:
			return True
		return False

class OpenLockPort(object):
	def __init__(self, obj, layout=None, rot=None, x=None, y=None, negative_name='Negative', neg=True):
		self.obj_name = obj.name
		self.negative_name = negative_name
		self.port_block_name = None
		self.neg = neg
		layouts = {
			'A': [{'rot': 0, 'x': 1, 'y': 0}],
			'B': [{'rot': 0, 'x': 0.5, 'y': 0}, {'rot': 0, 'x': 1.5, 'y': 0} ],
			'BA': [{'rot': 0, 'x': 1, 'y': 0} ],
			'C': [{'rot': 0, 'x': 0.5, 'y': 0}, {'rot': 0, 'x': 1.5, 'y': 0} ],
			'D': [{'rot': 0, 'x': 0.5, 'y': 0}, {'rot': 0, 'x': 1.5, 'y': 0}, {'rot': 0, 'x': 2.5, 'y': 0} ],
			'IA': [{'rot': 0, 'x': 0.5, 'y': 0} ],
			'E': [{'rot': 0, 'x': 1, 'y': 0},
				{'rot': 1, 'x': 0, 'y': 1},
				{'rot': 2, 'x': 1, 'y': 2},
				{'rot': 3, 'x': 2, 'y': 1}],
			'EA': [{'rot': 0, 'x': 0.5, 'y': 0, 'neg': False}, {'rot': 0, 'x': 1.5, 'y': 0}, {'rot': 0, 'x': 2.5, 'y': 0, 'neg': False},
				{'rot': 1, 'x': 0, 'y': 0.5, 'neg': False}, {'rot': 1, 'x': 0, 'y': 1.5}, {'rot': 1, 'x': 0, 'y': 2.5, 'neg': False},
				{'rot': 2, 'x': 0.5, 'y': 3, 'neg': False}, {'rot': 2, 'x': 1.5, 'y': 3}, {'rot': 2, 'x': 2.5, 'y': 3, 'neg': False},
				{'rot': 3, 'x': 3, 'y': 0.5, 'neg': False}, {'rot': 3, 'x': 3, 'y': 1.5}, {'rot': 3, 'x': 3, 'y': 2.5, 'neg': False}],
			'EC': [{'rot': 0, 'x': 1, 'y': 0, 'neg': False}, {'rot': 0, 'x': 2, 'y': 0},
				{'rot': 1, 'x': 0, 'y': 1, 'neg': False}, {'rot': 1, 'x': 0, 'y': 2},
				{'rot': 2, 'x': 1, 'y': 3, 'neg': False}, {'rot': 2, 'x': 2, 'y': 3},
				{'rot': 3, 'x': 3, 'y': 1, 'neg': False}, {'rot': 3, 'x': 3, 'y': 2}],
			'F': [{'rot': 0, 'x': 1, 'y': 0},
				{'rot': 1, 'x': 0, 'y': 1}],
			'J': [{'rot': 0, 'x': 0.5, 'y': 0}],
			'K': [{'rot': 0, 'x': 0.5, 'y': 0}, {'rot': 0, 'x': 2.0, 'y': 0}],
			'L': [{'rot': 0, 'x': 1, 'y': 0}, {'rot': 0, 'x': 2, 'y': 0}],
			'M': [{'rot': 0, 'x': 1, 'y': 0}, {'rot': 0, 'x': 2, 'y': 0}, {'rot': 0, 'x': 3, 'y': 0}],
			'N': [{'rot': 0, 'x': 1, 'y': 0}],
			'Q': [{'rot': 0, 'x': 1, 'y': 0}, {'rot': 0, 'x': 2, 'y': 0}, {'rot': 0, 'x': 3, 'y': 0} ],
			'QA': [{'rot': 0, 'x': 0.5, 'y': 0}, {'rot': 0, 'x': 1.5, 'y': 0}, {'rot': 0, 'x': 2.5, 'y': 0}, {'rot': 0, 'x': 3.5, 'y': 0}, {'rot': 0, 'x': 4.5, 'y': 0} ],
			'QB': [{'rot': 0, 'x': 0.5, 'y': 0}, {'rot': 0, 'x': 1.5, 'y': 0}, {'rot': 0, 'x': 2.5, 'y': 0}, {'rot': 0, 'x': 3.5, 'y': 0} ],
			'QC': [{'rot': 0, 'x': 0.5, 'y': 0}, {'rot': 0, 'x': 1.5, 'y': 0}, {'rot': 0, 'x': 2.5, 'y': 0}, {'rot': 0, 'x': 3.5, 'y': 0} ],
			'R': [{'rot': 0, 'x': 1, 'y': 0}, {'rot': 0, 'x': 2, 'y': 0}, {'rot': 0, 'x': 3, 'y': 0},
				{'rot': 1, 'x': 0, 'y': 1},
				{'rot': 2, 'x': 1, 'y': 2}, {'rot': 2, 'x': 2, 'y': 2}, {'rot': 2, 'x': 3, 'y': 2},
				{'rot': 3, 'x': 4, 'y': 1}],
			'S': [{'rot': 0, 'x': 1, 'y': 0},
				{'rot': 1, 'x': 0, 'y': 0.5},
				{'rot': 2, 'x': 1, 'y': 1},
				{'rot': 3, 'x': 2, 'y': 0.5}],
			'SA': [{'rot': 0, 'x': 1, 'y': 0}, {'rot': 0, 'x': 2, 'y': 0},
				{'rot': 1, 'x': 0, 'y': 0.5},
				{'rot': 2, 'x': 1, 'y': 1}, {'rot': 2, 'x': 2, 'y': 1},
				{'rot': 3, 'x': 3, 'y': 0.5}],
			'SB': [{'rot': 0, 'x': 1, 'y': 0}, {'rot': 0, 'x': 2, 'y': 0}, {'rot': 0, 'x': 3, 'y': 0},
				{'rot': 1, 'x': 0, 'y': 0.5},
				{'rot': 2, 'x': 1, 'y': 1}, {'rot': 2, 'x': 2, 'y': 1}, {'rot': 2, 'x': 3, 'y': 1},
				{'rot': 3, 'x': 4, 'y': 0.5}],
			'T': [{'rot': 0, 'x': 3, 'y': 0},
				{'rot': 1, 'x': 0, 'y': 3},
				{'rot': 2, 'x': 1, 'y': 4}, {'rot': 2, 'x': 2, 'y': 4}, {'rot': 2, 'x': 3, 'y': 4},
				{'rot': 3, 'x': 4, 'y': 1}, {'rot': 3, 'x': 4, 'y': 2}, {'rot': 3, 'x': 4, 'y': 3}],
			'U': [{'rot': 0, 'x': 1, 'y': 0}, {'rot': 0, 'x': 2, 'y': 0}, {'rot': 0, 'x': 3, 'y': 0},
				{'rot': 1, 'x': 0, 'y': 1}, {'rot': 1, 'x': 0, 'y': 2}, {'rot': 1, 'x': 0, 'y': 3},
				{'rot': 2, 'x': 1, 'y': 4}, {'rot': 2, 'x': 2, 'y': 4}, {'rot': 2, 'x': 3, 'y': 4},
				{'rot': 3, 'x': 4, 'y': 1}, {'rot': 3, 'x': 4, 'y': 2}, {'rot': 3, 'x': 4, 'y': 3}],
			'V': [{'rot': 0, 'x': 1, 'y': 0}, {'rot': 0, 'x': 2, 'y': 0}, {'rot': 0, 'x': 3, 'y': 0},
				{'rot': 1, 'x': 0, 'y': 1}, {'rot': 1, 'x': 0, 'y': 2}, {'rot': 1, 'x': 0, 'y': 3}],
			'W': [{'rot': 2, 'x': 3, 'y': 4},
				{'rot': 3, 'x': 4, 'y': 3}],
		}
		if layout:
			self.layout = layouts[layout]
		elif rot != None and x != None and y != None:
			self.layout = [{'rot': rot, 'x': x, 'y': y, 'neg': neg}]
		else:
			raise Exception("Must have either a layout, or rot+x+y")
		self.apply()
	def create_port_block(self):
		bpy.ops.mesh.primitive_cube_add()
		block = bpy.context.object
		block.name = "Port Block"
		self.port_block_name = block.name
		set_scale(block, 8.0, 0.65, 3.25)
		move(block, 0.0, 0.0, 0.0)
	def get_object(self):
		return bpy.data.objects[self.obj_name]
	def negative(self):
		return bpy.data.objects[self.negative_name]
	def port_block(self):
		return bpy.data.objects[self.port_block_name]
	def apply(self):
		self.create_port_block()
		for layout in self.layout:
			self.apply_layout(layout)
		self.port_block().hide = True
	def apply_layout(self, layout):
		import math
		bpy.ops.ed.undo_push()
		if layout['rot'] == 0:
			set_rotation(self.port_block(), z=0)
			move(self.port_block(), layout['x'] * 25.4, layout['y'] * 25.4 + 0.53, 3.24)
			if layout.get('neg', True):
				set_rotation(self.negative(), z=90*math.pi/180)
				move(self.negative(), layout['x'] * 25.4, layout['y'] * 25.4)
		elif layout['rot'] == 1:
			set_rotation(self.port_block(), z=90*math.pi/180)
			move(self.port_block(), layout['x'] * 25.4 + 0.53, layout['y'] * 25.4, 3.24)
			if layout.get('neg', True):
				set_rotation(self.negative(), z=0*math.pi/180)
				move(self.negative(), layout['x'] * 25.4, layout['y'] * 25.4)
		elif layout['rot'] == 2:
			set_rotation(self.port_block(), z=0)
			move(self.port_block(), layout['x'] * 25.4, layout['y'] * 25.4 - 0.53, 3.24)
			if layout.get('neg', True):
				set_rotation(self.negative(), z=270*math.pi/180)
				move(self.negative(), layout['x'] * 25.4, layout['y'] * 25.4)
		elif layout['rot'] == 3:
			set_rotation(self.port_block(), z=90*math.pi/180)
			move(self.port_block(), layout['x'] * 25.4 - 0.53, layout['y'] * 25.4, 3.24)
			if layout.get('neg', True):
				set_rotation(self.negative(), z=180*math.pi/180)
				move(self.negative(), layout['x'] * 25.4, layout['y'] * 25.4)
		bpy.ops.ed.undo_push()
		union(self.get_object(), self.port_block(), operation='UNION')
		bpy.ops.ed.undo_push()
		union(self.get_object(), self.negative(), operation='DIFFERENCE')

# 16.0, 1.1, 6.5
# 25.4, 0.53, 3.24

def inside_bounding_box(bb1, bb2):
	bb1x = bb1[0]
	bb2x = bb2[0]
	if bb1x[0] > bb2x[0] or bb1x[1] < bb2x[1]:
		return False
	bb1y = bb1[1]
	bb2y = bb2[1]
	if bb1y[0] > bb2y[0] or bb1y[1] < bb2y[1]:
		return False
	bb1x = bb1[2]
	bb2x = bb2[2]
	if bb1x[0] > bb2x[0] or bb1x[1] < bb2x[1]:
		return False
	return True

def bounding_box(mesh):
	minx = None
	miny = None
	minz = None
	maxx = None
	maxy = None
	maxz = None
	for co in [(mesh.six_world * v.co) for v in mesh.data.vertices]:
		if minx == None or minx > co.x:
			minx = co.x
		if miny == None or miny > co.y:
			miny = co.y
		if minz == None or minz > co.z:
			minz = co.z
		if maxx == None or maxx < co.x:
			maxx = co.x
		if maxy == None or maxy < co.y:
			maxy = co.y
		if maxz == None or maxz < co.z:
			maxz = co.z
	return (minx,maxx),(miny,maxy),(minz,maxz)

def filter_internal(meshes, testmeshes):
	retmeshes = []
	for mesh in meshes:
		store = True
		for t in testmeshes:
			if mesh_is_inside(mesh, t):
				mesh.hide = True
		if not mesh.hide:
			retmeshes.append(mesh)
	return retmeshes

def mesh_is_inside(mesh, obj):
	coords = [(mesh.matrix_world * v.co) for v in mesh.data.vertices]
	for coord in coords:
		if not point_is_inside(coord, obj):
			return False
	print("INTERNAL: %s" % mesh)
	return True

def point_is_inside(pt, ob):
	import mathutils
	Intersect = mathutils.geometry.intersect_ray_tri # less dict lookups.
	def ptInFaceXYBounds(f, pt):
		co = obvert[f.vertices[0]].co
		xmax = xmin= co.x
		ymax = ymin= co.y
		co = obvert[f.vertices[1]].co
		xmax = max(xmax, co.x)
		xmin = min(xmin, co.x)
		ymax = max(ymax, co.y)
		ymin = min(ymin, co.y)
		co = obvert[f.vertices[2]].co
		xmax = max(xmax, co.x)
		xmin = min(xmin, co.x)
		ymax = max(ymax, co.y)
		ymin = min(ymin, co.y)
		if len(f.vertices) == 4:
			co = obvert[f.vertices[3]].co
			xmax = max(xmax, co.x)
			xmin = min(xmin, co.x)
			ymax = max(ymax, co.y)
			ymin = min(ymin, co.y)
		# Now we have the bounds, see if the point is in it.
		return xmin <= pt.x <= xmax and ymin <= pt.y <= ymax
	def faceIntersect(f):
		isect = Intersect(obvert[f.vertices[0]].co, obvert[f.vertices[1]].co, obvert[f.vertices[2]].co, ray, obSpacePt, 1) # Clipped.
		if not isect and len(f.vertices) == 4:
			isect = Intersect(obvert[f.vertices[0]].co, obvert[f.vertices[2]].co, obvert[f.vertices[3]].co, ray, obSpacePt, 1) # Clipped.
		return bool(isect and isect.z > obSpacePt.z) # This is so the ray only counts if its above the point.
	obImvMat = mathutils.Matrix(ob.matrix_world)
	obImvMat.invert()
	pt.resize_4d()
	obSpacePt = obImvMat * pt
	pt.resize_3d()
	obSpacePt.resize_3d()
	ray = mathutils.Vector()
	ray.x = 0
	ray.y = 0
	ray.z = 1
	me = ob.data
	obvert = ob.data.vertices
	# Here we find the number on intersecting faces, return true if an odd number (inside), false (outside) if its true.
	return len([None for f in me.polygons if ptInFaceXYBounds(f, obSpacePt) if faceIntersect(f)]) % 2

def copy_object(obj):
	new = obj.copy()
	new.data = obj.data.copy()
	bpy.context.scene.objects.link(new)
	return new

def create_base(base, flourish, template, subname):
	xcopies = 3
	xtrans = [25,0,-25]
	if template.dimensions.x > 50:
		xcopies = 2
		xtrans = [12.5,-12.5]
	if template.dimensions.x > 75:
		xcopies = 1
		xtrans = [0]
	ycopies = 3
	ytrans = [25,0,-25]
	if template.dimensions.y > 50:
		ycopies = 2
		ytrans = [12.5,-12.5]
	if template.dimensions.y > 75:
		ycopies = 1
		ytrans = [0]
	bases = []
	counter = 0
	for i in range(xcopies):
		for j in range(ycopies):
			counter += 1
			new = copy_object(base)
			bases.append(new)
			move(new, xtrans[i], ytrans[j], 0.01)
			name = new.name
			name = name.replace('Core.001', '')
			name = name + subname + ".00" + str(counter)
			new.name = name
	for base in bases:
		base.hide = False
		unionize(base, [template], operation='INTERSECT')
		unionize(base, [flourish], operation='UNION')

def deselect_all():
	for o in bpy.data.objects:
		o.select = False

def upright_bases(bases, negative,xan=0,yan=90,xdist=2,ydist=0):
	for base in bases:
		base.hide = False
		new = copy_object(base)
		set_rotation(base, x=xan,y=yan)
		translate(base, x=xdist,y=ydist)
		set_rotation(new, x=-1*xan, y=-1*yan)
		translate(new, x=-1*xdist,y=-1*ydist)
		unionize(base,[negative], operation='DIFFERENCE')
		unionize(new,[negative], operation='DIFFERENCE')
		deselect_all()
		new.select = True
		base.select = True
		set_object_active(base)
		bpy.ops.object.join()
		base.name = base.name + '.Upright'


#w = Wall(25.4*2, 25.4,50, bwidth=12.7, altyoff=True)
#c = CurvedWall(25.4*4, 12.7, 50)
#c = CurvedWall(25.4*2, 12.7, 6.485, mortar_height=6.5, height_count=1)

#w = Wall(25*2, 10.2,50, bwidth=10.2, altyoff=True, randscaley=0.2, randanglex=0.1, randanglez=0.1)
#w = Wall(71.8, 8.98*2,6.485, height_count=1, mortar_height=6.5, bwidth=8.98*2, altyoff=True)
#w = Wall(100, 10.2, 50, height_count=10, bgap=0.0, alty=False, altx=False, randscalex=0.5, randscaley=0.5, randscalez=0.5, randanglex=0.5, randangley=0.5, randanglez=0.5)
