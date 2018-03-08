bl_info = {
	"name": "OpenForge",
	"author": "Devon Jones",
	"version": (1, 0, 0),
	"category": "Mesh",
	"description": "Tools to help build gaming models for 3d printing",
	"support": "COMMUNITY",
}

import bpy
import bmesh

boolean_operations = [
	("DIFFERENCE", "Difference", "", 1),
	("UNION", "Union", "", 2),
	("INTERSECT", "Intersect", "", 3)
]

boolean_solvers= [
	("BMESH", "BMesh", "", 1),
	("CARVE", "Carve", "", 2)
]

class BaseObject(object):
	def __init__(self, obj, context):
		self.obj = obj
		self.context = context
		self.name = obj.name

	def get_object(self):
		return bpy.data.objects[self.name]

	def select(self):
		self.context.scene.objects.active = self.get_object()

def count_selected_vertices(context, obj=None):
	if obj:
		set_object_active(context, obj)
	else:
		obj = context.active_object
	if context.mode == 'EDIT_MESH':
		bm = bmesh.from_edit_mesh(obj.data)
		verts = [ v.index for v in bm.verts if v.select ]
		return len(verts)
	else:
		verts = [ v.index for v in obj.data.vertices if v.select ]
		return len(verts)

def set_object_active(context, obj):
	#obj.select = True
	context.scene.objects.active = obj

class TestFacecount(object):
	def __init__(self, op, base, obj):
		self.op = op
		self.base = base
		self.obj = obj
		self.face_count = 0
		self.setup()

	def setup(self):
		self.face_count = len(list(self.base.data.polygons))
	
	def test(self, final, acceptable=0):
		final_count = len(list(final.data.polygons))
		if final_count == self.face_count:
			self.op.report({'INFO'}, "Test: %s, %s Failed: Facecount: %s:%s" % (final, self.obj, self.face_count, final_count))
			return False
		return True

class TestNonmanifold(object):
	def __init__(self, op, context, base, obj):
		self.op = op
		self.context = context
		self.base = base
		self.obj = obj
		self.base_count = 0
		self.obj_count = 0
		self.setup()

	def setup(self):
		active = self.context.scene.objects.active
		self.base_count = self.get_nonmanifold_count(self.base)
		self.obj_count = self.get_nonmanifold_count(self.obj)
		set_object_active(self.context, active)
		set_object_active(bpy.context, active)
	
	def get_nonmanifold_count(self, obj):
		set_object_active(self.context, obj)
		bpy.ops.object.mode_set(mode='EDIT')
		bpy.ops.mesh.select_all(action="DESELECT")
		bpy.ops.mesh.select_non_manifold()
		count = count_selected_vertices(self.context, obj)
		bpy.ops.object.mode_set(mode='OBJECT')
		return count

	def test(self, final, acceptable=0):
		active = self.context.scene.objects.active
		final_count = self.get_nonmanifold_count(final)
		set_object_active(self.context, active)
		before_count = self.base_count + self.obj_count
		if final_count > (before_count + acceptable):
			self.op.report({'INFO'}, "Test: %s, %s Failed: Nonmanifold: %s:%s" % (final, self.obj, before_count, final_count))
			return False
		return True

def union(op, context, aobject, bobject, operation='UNION', solver='CARVE'):
	op.report({'INFO'}, "Union: %s & %s" % (aobject, bobject))
	set_object_active(context, aobject)
	mod = aobject.modifiers.new('Modifier', 'BOOLEAN')
	mod.operation = operation
	mod.solver = solver
	mod.object = bobject
	bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)

def dist_unionize(op, context, objs, operation='UNION', solver='CARVE'):
	base = context.object
	for obj in objs:
		if obj != base:
			bpy.ops.ed.undo_push()
			union(op, context, obj, base, operation=operation, solver=solver)

def filter_unhidden(context):
	objs = []
	for obj in context.scene.objects:
		if obj.type in ['MESH']:
			if not obj.hide:
				objs.append(obj)
	return objs

def deselect_objects(objs):
	for obj in objs:
		obj.select = False

class JiggleSettings(bpy.types.PropertyGroup):
	jiggle_max = bpy.props.FloatProperty(name="Max Jiggle Steps", default=0.05, min=0.01, max=0.1)
	jiggle_x_pos = bpy.props.BoolProperty(name="Jiggle X Positive", default=False)
	jiggle_x_neg = bpy.props.BoolProperty(name="Jiggle X Negative", default=False)
	jiggle_y_pos = bpy.props.BoolProperty(name="Jiggle Y Positive", default=False)
	jiggle_y_neg = bpy.props.BoolProperty(name="Jiggle Y Negative", default=False)
	jiggle_z_pos = bpy.props.BoolProperty(name="Jiggle Z Positive", default=False)
	jiggle_z_neg = bpy.props.BoolProperty(name="Jiggle Z Negative", default=False)

class BaseBoolean(object):
	def jiggle(self):
		if self.jiggle_x_pos or self.jiggle_x_neg or self.jiggle_y_pos or self.jiggle_y_neg or self.jiggle_z_pos or self.jiggle_z_neg:
			return True
		return False
	
	def unionize(self, context, objs):
		base = BaseObject(context.scene.objects.active, context)
		objs.sort(key=lambda x: x.name)
		objs = [BaseObject(o, context) for o in objs]
		for obj in objs:
			if obj.name != base.name:
				result = self.attempt_union(context, base, obj)
				if not result:
					if self.jiggle():
						result = self.run_jiggle(context, base, obj)
					if not result and self.halt:
						return

	def run_jiggle(self, context, base, obj, jiggleobj, hideobject=True):
		obj_x_start = obj.get_object().location.x
		obj_y_start = obj.get_object().location.y
		obj_z_start = obj.get_object().location.z
		jiggle_range = True
		xpos = 0.0
		ypos = 0.0
		zpos = 0.0
		xneg = 0.0
		yneg = 0.0
		zneg = 0.0
		while jiggle_range:
			if self.jiggle_x_pos:
				xpos += 0.01
				if xpos < self.jiggle_max:
					self.jiggle_set(jiggleobj, xpos, ypos, zpos)
					result = self.attempt_union(context, base, obj, hideobject)
					if result:
						return True
			if self.jiggle_y_pos:
				ypos += 0.01
				if ypos < self.jiggle_max:
					self.jiggle_set(jiggleobj, xpos, ypos, zpos)
					result = self.attempt_union(context, base, obj, hideobject)
					if result:
						return True
			if self.jiggle_z_pos:
				zpos += 0.01
				if zpos < self.jiggle_max:
					self.jiggle_set(jiggleobj, xpos, ypos, zpos)
					result = self.attempt_union(context, base, obj, hideobject)
					if result:
						return True
			if self.jiggle_x_neg:
				xneg += 0.01
				if xneg < self.jiggle_max:
					self.jiggle_set(jiggleobj, -xneg, ypos, zpos)
					result = self.attempt_union(context, base, obj, hideobject)
					if result:
						return True
			if self.jiggle_y_neg:
				yneg += 0.01
				if yneg < self.jiggle_max:
					self.jiggle_set(jiggleobj, -xneg, -yneg, zpos)
					result = self.attempt_union(context, base, obj, hideobject)
					if result:
						return True
			if self.jiggle_z_neg:
				zneg += 0.01
				if zneg < self.jiggle_max:
					self.jiggle_set(jiggleobj, -xneg, -yneg, -zneg)
					result = self.attempt_union(context, base, obj, hideobject)
					if result:
						return True
			if xpos >= self.jiggle_max:
				jiggle_range = False
		return False

	def jiggle_set(self, obj, x, y, z):
		obj.get_object().location.x = obj.get_object().location.x + x
		obj.get_object().location.y = obj.get_object().location.y + y
		obj.get_object().location.z = obj.get_object().location.z + z
		self.report({'INFO'}, "Jiggle: %s (%s,%s,%s) -> %s" % (obj.get_object(), x, y, z, obj.get_object().location))
	
	def attempt_union(self, context, base, obj, hideobject=True):
		bpy.ops.ed.undo_push()
		tests = []
		if self.test_nonmanifold:
			tests.append(TestNonmanifold(self, context, base.get_object(), obj.get_object()))
		if self.test_facecount:
			tests.append(TestFacecount(self, base.get_object(), obj.get_object()))
		union(self, context, base.get_object(), obj.get_object(), operation=self.operation, solver=self.solver)
		base.select()
		success = True
		print(base)
		for test in tests:
			if not test.test(base.get_object()):
				success = False
		if success and hideobject:
			obj.get_object().hide = True
		else:
			bpy.context.scene.objects.active = base.get_object()
			bpy.ops.ed.undo()
			return False
		base.select()
		return True
	
class Unionize(bpy.types.Operator, BaseBoolean):
	"""Booleans the active object with every visible object"""
	bl_idname = "openforge.unionize"
	bl_label = "Unionize"
	bl_options = {'REGISTER', 'UNDO'}
	
	operation = bpy.props.EnumProperty(name="Operation", default='UNION', items=boolean_operations)
	solver = bpy.props.EnumProperty(name="Solver", default='CARVE', items=boolean_solvers)
	test_nonmanifold = bpy.props.BoolProperty(name="Test Non Manifold", default=True)
	test_facecount = bpy.props.BoolProperty(name="Test Face Count", default=True)
	halt = bpy.props.BoolProperty(name="Halt on failure", default=True)
	#jiggle = bpy.props.PointerProperty(type=JiggleSettings, name="Jiggle")
	jiggle_max = bpy.props.FloatProperty(name="Max Jiggle Steps", default=0.05, min=0.01, max=0.1)
	jiggle_x_pos = bpy.props.BoolProperty(name="Jiggle X Positive", default=False)
	jiggle_x_neg = bpy.props.BoolProperty(name="Jiggle X Negative", default=False)
	jiggle_y_pos = bpy.props.BoolProperty(name="Jiggle Y Positive", default=False)
	jiggle_y_neg = bpy.props.BoolProperty(name="Jiggle Y Negative", default=False)
	jiggle_z_pos = bpy.props.BoolProperty(name="Jiggle Z Positive", default=False)
	jiggle_z_neg = bpy.props.BoolProperty(name="Jiggle Z Negative", default=False)

	def unionize(self, context, objs):
		base = BaseObject(context.scene.objects.active, context)
		objs.sort(key=lambda x: x.name)
		objs = [BaseObject(o, context) for o in objs]
		for obj in objs:
			if obj.name != base.name:
				result = self.attempt_union(context, base, obj)
				if not result:
					if self.jiggle():
						result = self.run_jiggle(context, base, obj, obj)
					if not result and self.halt:
						return
	
	def execute(self, context):
		self.unionize(context, filter_unhidden(context))
		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)

class DistUnionize(bpy.types.Operator, BaseBoolean):
	"""Booleans every visible object with the active object"""
	bl_idname = "openforge.dist_unionize"
	bl_label = "DistUnionize"
	bl_options = {'REGISTER', 'UNDO'}

	operation = bpy.props.EnumProperty(name="Operation", default='UNION', items=boolean_operations)
	solver = bpy.props.EnumProperty(name="Solver", default='CARVE', items=boolean_solvers)
	test_nonmanifold = bpy.props.BoolProperty(name="Test Non Manifold", default=True)
	test_facecount = bpy.props.BoolProperty(name="Test Face Count", default=True)
	halt = bpy.props.BoolProperty(name="Halt on failure", default=True)
	#jiggle = bpy.props.PointerProperty(type=JiggleSettings, name="Jiggle")
	jiggle_max = bpy.props.FloatProperty(name="Max Jiggle Steps", default=0.05, min=0.01, max=0.1)
	jiggle_x_pos = bpy.props.BoolProperty(name="Jiggle X Positive", default=False)
	jiggle_x_neg = bpy.props.BoolProperty(name="Jiggle X Negative", default=False)
	jiggle_y_pos = bpy.props.BoolProperty(name="Jiggle Y Positive", default=False)
	jiggle_y_neg = bpy.props.BoolProperty(name="Jiggle Y Negative", default=False)
	jiggle_z_pos = bpy.props.BoolProperty(name="Jiggle Z Positive", default=False)
	jiggle_z_neg = bpy.props.BoolProperty(name="Jiggle Z Negative", default=False)

	def distunionize(self, context, objs):
		base = BaseObject(context.scene.objects.active, context)
		objs.sort(key=lambda x: x.name)
		objs = [BaseObject(o, context) for o in objs]
		for obj in objs:
			if obj.name != base.name:
				result = self.attempt_union(context, obj, base, hideobject=False)
				if not result:
					if self.jiggle():
						result = self.run_jiggle(context, obj, base, obj, hideobject=False)
					if not result and self.halt:
						return

	def execute(self, context):
		self.distunionize(context, filter_unhidden(context))
		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)

def register():
	bpy.utils.register_class(Unionize)
	bpy.utils.register_class(DistUnionize)

def unregister():
	bpy.utils.unregister_class(Unionize)
	bpy.utils.unregister_class(DistUnionize)

if __name__ == "__main__":
	register()



