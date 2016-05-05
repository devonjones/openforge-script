import os
import sys
from openforge.operations import *
import openforge.operations as ops

def assemble_curved(config):
	print(config)
	for x in range(config['min'], config['max']+1):
		for y in range(config['min'], config['max']+1):
			if y >= x:
				print("Starting: %s%sx%s%s" % (
					config['result'][0], x, y, config['result'][1]))
				newpid = os.fork()
				if newpid == 0:
					assemble_c(config, x, y)
					sys.exit(0)
				else:
					os.waitpid(newpid, 0)
					print("\n")

def assemble_c(config, x, y):
	ops.start()
	basefile = "%s%sx%s%s" %(config['base'][0], x, y, config['base'][1])
	base = ops.import_stl(basefile)
	backfile = "%s%sx%s%s" %(config['back'][0], x, y, config['back'][1])
	back = ops.import_stl(backfile)

	back.location = (0.0, 0.0, 5.19)
	ops.union(base, back)
	base.select = False
	ops.delete(back)

	ops.print_objects()
	resultfile = "%s%sx%s%s" %(config['result'][0], x, y, config['result'][1])
	ops.export_stl(base, resultfile)

