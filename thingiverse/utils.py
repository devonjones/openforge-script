import re
import kconfig

ConfigPath = kconfig.ConfigPathDefaults([".openforge", "~/.openforge", "/etc/openforge"])
Config = kconfig.ConfigDefault(ConfigPath)

def parse_link(link_text):
	results = {}
	parts = link_text.split(",")
	for link_part in parts:
		m = re.search('<(http.*)>; rel="(.*)"', link_part)
		results[m.group(2)] = m.group(1)
	return results

