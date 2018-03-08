import os
import contextlib

def redirect_output(stdchannel, dest_filename):
	oldstdchannel = os.dup(stdchannel.fileno())
	dest_file = open(dest_filename, 'w')
	os.dup2(dest_file.fileno(), stdchannel.fileno())

@contextlib.contextmanager
def RedirectedStdStreams(stdchannel, dest_filename):
	"""
	A context manager to temporarily redirect stdout or stderr

	e.g.:

	with stdchannel_redirected(sys.stderr, os.devnull):
	...
	"""

	try:
		oldstdchannel = os.dup(stdchannel.fileno())
		dest_file = open(dest_filename, 'w')
		os.dup2(dest_file.fileno(), stdchannel.fileno())

		yield
	finally:
		if oldstdchannel is not None:
			os.dup2(oldstdchannel, stdchannel.fileno())
		if dest_file is not None:
			dest_file.close()
