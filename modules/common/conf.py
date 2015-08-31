import yaml
def read():
	with open("config.yml", "r") as cfgfile:
		return yaml.load(cfgfile)