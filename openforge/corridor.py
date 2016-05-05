import os
import sys
import openforge.operations as ops

def assemble_corridors(config):
	print(config)
	for x in range(config['x-min'], config['x-max']+1):
		for y in range(config['y-min'], config['y-max']+1):
			print("Starting: %s%sx%s%s" % (
				config['result'][0], x, y, config['result'][1]))
			newpid = os.fork()
			if newpid == 0:
				assemble_corridor(config, x, y)
				sys.exit(0)
			else:
				os.waitpid(newpid, 0)
				print("\n")

def assemble_corridor(config, x, y):
	ops.start()
	basefile = "%s%sx%s%s" %(config['base'][0], x, y, config['base'][1])
	base = ops.import_stl(basefile)
	backfile = "%s%sx%s" %(config['back'][0], x, config['back'][1])
	back = ops.import_stl(backfile)
	frontfile = "%s%sx%s" %(config['front'][0], x, config['front'][1])
	front = ops.import_stl(frontfile)

	edge_diff = 10.2
	if config['external']:
		edge_diff = 0.0

	front.location = (0.0, y*25-edge_diff, 5.2)
	ops.union(base, front)
	base.select = False
	ops.delete(front)

	edge_diff = 0.0
	if config['external']:
		edge_diff = 12.5

	back.location = (0.0, 0-edge_diff, 5.2)
	ops.union(base, back)
	base.select = False
	ops.delete(back)

	ops.print_objects()
	base.select = True
	resultfile = "%s%sx%s%s" %(config['result'][0], x, y, config['result'][1])
	ops.export_stl(base, resultfile)

