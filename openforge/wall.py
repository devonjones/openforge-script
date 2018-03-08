import os
import sys
import math
import openforge.operations as ops

def assemble_walls(config):
	print(config)
	for x in range(config['x-min'], config['x-max']+1):
		for y in range(config['y-min'], config['y-max']+1):
			print("Starting: %s%sx%s%s" % (
				config['result'][0], x, y, config['result'][1]))
			newpid = os.fork()
			if newpid == 0:
				assemble_wall(config, x, y)
				sys.exit(0)
			else:
				os.waitpid(newpid, 0)
				print("\n")

def assemble_wall(config, x, y):
	ops.start()
	basefile = "%s%sx%s%s" %(config['base'][0], x, y, config['base'][1])
	base = ops.import_stl(basefile)
	backfile = "%s%sx%s" %(config['back'][0], x, config['back'][1])
	back = ops.import_stl(backfile)

	edge_diff = 10.2
	if config['external']:
		edge_diff = 0.0

	back.location = (0.01, y*25-edge_diff, 5.19)
	ops.union(base, back)
	base.select = False
	ops.delete(back)

	ops.print_objects()
	resultfile = "%s%sx%s%s" %(config['result'][0], x, y, config['result'][1])
	ops.export_stl(base, resultfile)

def assemble_wall_backs(config):
	print(config)
	for x, segments in config['back_length'].items():
		print("Starting: %s.%sx.%s" % (
		config['result'][0], x, config['result'][1]))
		newpid = os.fork()
		if newpid == 0:
			assemble_wall_back(config, x, segments)
			sys.exit(0)
		else:
			os.waitpid(newpid, 0)
			print("\n")

def assemble_wall_back(config, x, segments):
	ops.start()
	split = config['split']
	end_number = 1
	if split:
		end_number = 2
	start_file = ".".join([
		config['columns'][0],
		config['columns'][1],
		"start",
		str(end_number),
		config['columns'][2]])
	start = ops.import_stl(start_file)

	assemble_line(start, config, x, segments, split)

	end_file = ".".join([
		config['columns'][0],
		str(x) + "x",
		config['columns'][1],
		"end",
		str(end_number),
		config['columns'][2]])
	end = ops.import_stl(end_file)

	ops.union(start, end)
	start.select = False
	ops.delete(end)

	ops.print_objects()
	resultfile = "%s.%sx.%s" %(config['result'][0], x, config['result'][1])
	ops.export_stl(start, resultfile)

def assemble_line(start, config, x, segments, split):
	beginning = "1"
	if split:
		beginning = "5"

	if segments == 0:
		return start
	current_segments = segments
	if segments > 4:
		current_segments = 4
	line1_file = ".".join([
		config['columns'][0],
		"%sx" % current_segments,
		config['columns'][1],
		beginning,
		config['columns'][2]])
	line1 = ops.import_stl(line1_file)
	ops.union(start, line1)
	start.select = False
	ops.delete(line1)

	beginning = "5"
	if split:
		beginning = "1"
	current_segments = segments - 4
	if current_segments <= 0:
		return start
	line2_file = ".".join([
		config['columns'][0],
		"%sx" % current_segments,
		config['columns'][1],
		beginning,
		config['columns'][2]])
	line2 = ops.import_stl(line2_file)
	line2.location = (10.2*4, 0.0, 0.0)
	ops.union(start, line2)
	start.select = False
	ops.delete(line2)

	return start

def assemble_wall_backs_arb(config):
	print(config)
	for back_length in config['back_length']:
		print("Starting: %s.%s.%s" % (
		config['result'][0], back_length, config['result'][1]))
		newpid = os.fork()
		if newpid == 0:
			assemble_wall_back_arb(config, back_length)
			sys.exit(0)
		else:
			os.waitpid(newpid, 0)
			print("\n")

def assemble_wall_back_arb(config, back_length):
	ops.start()
	start_file = ".".join([
		config['columns'][0],
		config['columns'][1],
		"start",
		"2",
		config['columns'][2]])
	start = ops.import_stl(start_file)

	assemble_line_arb(start, config, back_length)

	end_file = ".".join([
		config['columns'][0],
		config['columns'][1],
		"end",
		str(back_length),
		config['columns'][2]])
	end = ops.import_stl(end_file)

	ops.union(start, end)
	start.select = False
	ops.delete(end)

	ops.print_objects()
	resultfile = "%s.%s.%s" %(config['result'][0], back_length, config['result'][1])
	ops.export_stl(start, resultfile)

def assemble_line_arb(start, config, back_length):
	column_order = config['column_order']

	segments = math.floor(float(back_length) / 10.2) - 1
	if float(back_length) % 10.2 < 3.0:
		segments -= 1

	if segments == 0:
		return start
	current_segments = segments
	for val in range(segments):
		column_file = ".".join([
			config['columns'][0],
			"1x",
			config['columns'][1],
			"%s" % (column_order[val]),
			config['columns'][2]])
		column = ops.import_stl(column_file)
		print("x: %s" % 10.2*val)
		column.location = (10.2*val, 0.0, 0.0)
		ops.union(start, column)
		start.select = False
		ops.delete(column)
	return start

