import os
import sys
from openforge.operations import *
import openforge.operations as ops

def assemble_corners(config):
	print(config)
	for x in range(config['min'], config['max']+1):
		print("Starting: %s%sx%s%s" % (
			config['result'][0], x, x, config['result'][1]))
		newpid = os.fork()
		if newpid == 0:
			assemble_corner(config, x)
			sys.exit(0)
		else:
			os.waitpid(newpid, 0)
			print("\n")

def assemble_corner(config, x):
	ops.start()
	basefile = "%s%sx%s%s" %(config['base'][0], x, x, config['base'][1])
	base = ops.import_stl(basefile)
	backfile = "%s%sx%s" %(config['back'][0], x, config['back'][1])
	back = ops.import_stl(backfile)

	back.location = (0.0, 0.0, 5.2)
	ops.union(base, back)
	base.select = False
	ops.delete(back)

	ops.print_objects()
	resultfile = "%s%sx%s%s" %(config['result'][0], x, x, config['result'][1])
	ops.export_stl(base, resultfile)

def assemble_corner_backs(config):
	print(config)
	for x, segments in config['back_length'].items():
		print("Starting: %s.%sx.%s" % (
		config['result'][0], x, config['result'][1]))
		newpid = os.fork()
		if newpid == 0:
			assemble_corner_back(config, x, segments)
			sys.exit(0)
		else:
			os.waitpid(newpid, 0)
			print("\n")

def assemble_corner_back(config, x, segments):
	ops.start()
	corner_column_file = ".".join([
		config['columns_corner'][0],
		str(x) + "x",
		config['columns_corner'][1]])
	corner = ops.import_stl(corner_column_file)

	back_start = assemble_line(config, x, segments, angle=False)
	side_start = assemble_line(config, x, segments, angle=True)

	thickness = 10.2
	if config['external']:
		thickness = 12.5

	wall_diff = thickness
	if config['external'] and not config['inverse']:
		wall_diff = 0.0
	elif not config['external'] and config['inverse']:
		wall_diff = 0.0
	print("y: %s" % (x*25-wall_diff))
	back_start.location = (0.0, x*25-wall_diff, 0)

	wall_diff = 0.0
	if config['external'] and not config['inverse']:
		wall_diff = thickness
	elif not config['external'] and config['inverse']:
		wall_diff = thickness
	print("x: %s" % (x*25+wall_diff))
	side_start.location = (x*25+wall_diff, 0.0, 0)

	ops.union(corner, back_start)
	ops.union(corner, side_start)
	corner.select = False
	ops.delete(back_start)
	corner.select = False
	ops.delete(side_start)

	ops.print_objects()
	resultfile = "%s.%sx.%s" %(config['result'][0], x, config['result'][1])
	ops.export_stl(corner, resultfile)

def assemble_line(config, x, segments, angle=False):
	start = 'start.1'
	field = 'columns'
	if angle:
		field = 'columns_90'
		start = "start.2"
	start_file = ".".join([
		config[field][0],
		config[field][1],
		start,
		config[field][2]])
	line_start = ops.import_stl(start_file)

	if segments == 0:
		return line_start
	current_segments = segments
	if segments > 4:
		current_segments = 4
	line1_file = ".".join([
		config[field][0],
		"%sx" % current_segments,
		config[field][1],
		"1",
		config[field][2]])
	line1 = ops.import_stl(line1_file)
	ops.union(line_start, line1)
	line_start.select = False
	ops.delete(line1)

	current_segments = segments - 4
	if current_segments <= 0:
		return line_start
	line2_file = ".".join([
		config[field][0],
		"%sx" % current_segments,
		config[field][1],
		"5",
		config[field][2]])
	line2 = ops.import_stl(line2_file)
	if angle:
		line2.location = (0.0, 10.2*4, 0.0)
	else:
		line2.location = (10.2*4, 0.0, 0.0)
	ops.union(line_start, line2)
	line_start.select = False
	ops.delete(line2)

	return line_start

