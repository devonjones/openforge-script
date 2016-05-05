
def start():
	import bpy
	cube = bpy.data.objects['Cube']
	delete(cube)

def import_stl(fname):
	import bpy
	print("Importing: %s" % fname)
	preset = set([n.name for n in list(bpy.data.objects)])
	bpy.ops.import_mesh.stl(filepath=fname)
	postset = set([n.name for n in list(bpy.data.objects)])
	dset = postset - preset
	return bpy.data.objects[list(dset)[0]]

def export_stl(obj, fname):
	import bpy
	print("Exporting: %s" % fname)
	obj.select = True
	bpy.context.scene.objects.active = obj
	bpy.ops.export_mesh.stl(filepath=fname)

def union(aobject, bobject):
	import bpy
	print("Union: %s & %s" % (aobject, bobject))
	bpy.context.scene.objects.active = aobject
	mod = aobject.modifiers.new('Modifier', 'BOOLEAN')
	mod.operation = 'UNION'
	mod.object = bobject
	bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)

def delete(obj):
	import bpy
	print("Deleting: %s" % obj)
	obj.select = True
	bpy.ops.object.delete()

def print_objects():
	import bpy
	print(list(bpy.data.objects))

def open_blend(filename):
	import bpy
	bpy.ops.wm.open_mainfile(filepath=filename)

def save_blend(filename):
	import bpy
	bpy.ops.wm.save_mainfile(filepath=filename)
