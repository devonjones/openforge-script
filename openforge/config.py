import yaml

def parse_config(config):
	with open(config, 'r') as configfile:
		return yaml.load(configfile)
