import sys
import os
import logging
from openforge.output import RedirectedStdStreams

def start():
	with RedirectedStdStreams(sys.stderr, os.devnull):
		with RedirectedStdStreams(sys.stdout, os.devnull):
			import bpy
	cube = bpy.data.objects['Cube']
	delete(cube)

def import_stl(fname):
	with RedirectedStdStreams(sys.stderr, os.devnull):
		with RedirectedStdStreams(sys.stdout, os.devnull):
			import bpy
	logger = logging.getLogger('openforge')
	logging.info("Importing: %s" % fname)
	preset = set([n.name for n in list(bpy.data.objects)])
	bpy.ops.import_mesh.stl(filepath=fname)
	postset = set([n.name for n in list(bpy.data.objects)])
	dset = postset - preset
	return bpy.data.objects[list(dset)[0]]

def export_stl(obj, fname):
	with RedirectedStdStreams(sys.stderr, os.devnull):
		with RedirectedStdStreams(sys.stdout, os.devnull):
			import bpy
	logger = logging.getLogger('openforge')
	logging.info("Exporting: %s" % fname)
	obj.select = True
	bpy.context.scene.objects.active = obj
	bpy.ops.export_mesh.stl(filepath=fname)

def union(aobject, bobject):
	with RedirectedStdStreams(sys.stderr, os.devnull):
		with RedirectedStdStreams(sys.stdout, os.devnull):
			import bpy
	logger = logging.getLogger('openforge')
	logging.info("Union: %s & %s" % (aobject, bobject))
	bpy.context.scene.objects.active = aobject
	mod = aobject.modifiers.new('Modifier', 'BOOLEAN')
	mod.operation = 'UNION'
	mod.object = bobject
	bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)

def delete(obj):
	with RedirectedStdStreams(sys.stderr, os.devnull):
		with RedirectedStdStreams(sys.stdout, os.devnull):
			import bpy
	logger = logging.getLogger('openforge')
	logging.info("Deleting: %s" % obj)
	obj.select = True
	bpy.ops.object.delete()

def print_objects():
	with RedirectedStdStreams(sys.stderr, os.devnull):
		with RedirectedStdStreams(sys.stdout, os.devnull):
			import bpy
	print(list(bpy.data.objects))

def open_blend(filename):
	with RedirectedStdStreams(sys.stderr, os.devnull):
		with RedirectedStdStreams(sys.stdout, os.devnull):
			import bpy
			bpy.ops.wm.open_mainfile(filepath=filename)
	logger = logging.getLogger('openforge')
	logging.info("Opened: %s" % filename)

def save_blend(filename):
	with RedirectedStdStreams(sys.stderr, os.devnull):
		with RedirectedStdStreams(sys.stdout, os.devnull):
			import bpy
			bpy.ops.wm.save_mainfile(filepath=filename)

def unionize(base, word):
	for i in list(bpy.data.objects):
		if i.name.find(word) > -1:
			union(i, base)

