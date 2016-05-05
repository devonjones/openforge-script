import os
import sys
from openforge.operations import *
import openforge.operations as ops

def add_bases(config):
	print(config)
	for x in range(config['x-min'], config['x-max']+1):
		for y in range(config['y-min'], config['y-max']+1):
			print("Starting: %s%sx%s%s" % (
				config['result'][0], x, y, config['result'][1]))
			newpid = os.fork()
			if newpid == 0:
				add_base(config, x, y)
				sys.exit(0)
			else:
				os.waitpid(newpid, 0)
				print("\n")

def add_base(config, x, y):
	ops.start()
	basefile = "%s%sx%s%s" %(config['base'][0], x, y, config['base'][1])
	base = ops.import_stl(basefile)
	tilefile = "%s%sx%s%s" %(config['tile'][0], x, y, config['tile'][1])
	tile = ops.import_stl(tilefile)

	tile.location = (0.0, 0.0, 6.0)
	ops.union(base, tile)
	base.select = False
	ops.delete(tile)

	ops.print_objects()
	resultfile = "%s%sx%s%s" %(config['result'][0], x, y, config['result'][1])
	ops.export_stl(base, resultfile)

