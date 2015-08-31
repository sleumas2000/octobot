import yaml
def confSave(filename,dict):
	file="modules/conf/"+filename+".yml"
	try:
		with open(file, "w") as saveFile:
			print("Saved")
			saveFile.write(yaml.dump(dict,default_flow_style=False)) # Save in the block style - it looks neater
			return True
	except:
		return False
def confLoad(filename,default):
	file="modules/conf/"+filename+".yml"
	try:
		with open(file, "r") as saveFile:
			return yaml.load(saveFile)
	except Exception as e:
		print("Read Failed")
		print(e)
		confSave(filename,default)
		return default
def textSave(filename,string,mode="a"): # IT IS HIGHLY RECOMMENDED THAT YOU SPECIFY MODE - be that "a", "r+", or "w"
	file="modules/conf/"+filename+".txt"
	try:
		with open(file, mode) as saveFile:
			saveFile.write(string)
			return True
	except:
		return False
def textLoad(filename,overflowLimit):
	file="modules/conf/"+filename+".txt"
	try:
		with open(file, "r") as saveFile:
			return saveFile.read(overflowLimit)
	except:
		return None
