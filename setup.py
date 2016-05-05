#!/usr/bin/env python3
import os.path
import re
from setuptools import Command, find_packages, setup

class PyTest(Command):
	user_options = []
	def initialize_options(self):
		pass
	def finalize_options(self):
		pass
	def run(self):
		import sys,subprocess
		errno = subprocess.call([sys.executable, "runtests.py"])
		raise SystemExit(errno)

def parse_requirements(file_name):
	"""Taken from http://cburgmer.posterous.com/pip-requirementstxt-and-setuppy"""
	requirements = []
	for line in open(os.path.join(os.path.dirname(__file__), "config", file_name), "r"):
		line = line.strip()
		# comments and blank lines
		if re.match(r"(^#)|(^$)", line):
			continue
		requirements.append(line)
	return requirements

setup(
	name="openforge-script",
	version="0.0.1",
	url = "https://github.com/devonjones/openforge-script",
	author="Devon Jones",
	author_email="devon.jones@gmail.com",
	license = "Apache",
	packages=find_packages(),
	cmdclass = {"test": PyTest},
	package_data = {"config": ["requirements.txt"]},
	install_requires=parse_requirements("requirements.txt"),
	tests_require=parse_requirements("requirements.txt"),
	description = "Scripts for working with openforge",
	long_description = "\n" + open("README.md").read(),
)
