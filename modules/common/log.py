def log(show,message): # Currently uses a lot of memory when the file is long
	message = str(message)
	if show:
		print(message)
		file = open(cfg["logging"]["verboseLogFile"], "a")
		file.write(time.strftime("%Y%m%d%H%M%S: ", time.gmtime())+message+"\n")
		if file.tell() > cfg["logging"]["maxVerboseLogSize"]:
			with open(cfg["logging"]["verboseLogFile"], "r") as file1:
				data = file1.read().splitlines(True)
			with open(cfg["logging"]["verboseLogFile"], "w") as file2:
				file2.writelines(data[50:]) # in an attempt to make it not so slow on a full file, it will cut away the first 50 lines when the file is too large, so it doesn't need to move so much stuff around the memory
		file.close()
		file = open(cfg["logging"]["logFile"], "a")
		file.write(time.strftime("%Y%m%d%H%M%S: ", time.gmtime())+message+"\n")
		while file.tell() > cfg["logging"]["maxLogSize"]:
			with open(cfg["logging"]["logFile"], "r") as file1:
				data = file1.read().splitlines(True)
			with open(cfg["logging"]["logFile"], "w") as file2:
				file2.writelines(data[50:]) # as above
		file.close()
		return True
	else:
		file = open(cfg["logging"]["verboseLogFile"], "a")
		file.write(time.strftime("%Y%m%d%H%M%S: ", time.gmtime())+message+"\n")
		while file.tell() > cfg["logging"]["maxVerboseLogSize"]:
			with open(cfg["logging"]["verboseLogFile"], "r") as file1:
				data = file1.read().splitlines(True)
			with open(cfg["logging"]["verboseLogFile"], "w") as file2:
				file2.writelines(data[50:]) # again
		file.close()
		return False