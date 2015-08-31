#!/usr/local/bin/python
import threading
import socket
import ssl
import time
from modules import *
import imp
import traceback
import os
import sys
import yaml
from importlib import import_module
print(sys.version)
with open("config.yml", "r") as cfgfile:
	cfg = yaml.load(cfgfile)
ircUnencrypted = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the unencrypted socket
irc = ssl.wrap_socket(ircUnencrypted) # encrypts it	
MODULE_EXTENSIONS = (".pyc",".py",".pyo")
def packageContents(package_name):
	file, pathname, description = imp.find_module(package_name)
	if file:
		raise ImportError("Not a package: %r", package_name)
	# Use a set because some may be both source and compiled.
	return set([os.path.splitext(module)[0]
		for module in os.listdir(pathname)
		if module.endswith(MODULE_EXTENSIONS)])
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
def react(input,moduleList):
	log(False,"input: "+input)
	if input.find("PING") != -1:
		irc.send("PONG " + input.split() [1] + "\r\n")
		log(False,"input: "+input)
		log(True,"Ping Request Responded to Successfully")
		return {}
	threads = {}
	for m in moduleList:
		try:
			this_m = import_module("modules."+m)
			if hasattr(this_m,"react"):
				threads.update({m:threading.Thread(name=m,target=this_m.react,args=(input,irc))})
				threads[m].setDaemon(True)
				try:
					threads[m].start()
				except Exception as e:
					log(True,("Exception in module %s: %s " % (m,str(e))) )
					log(False,"Traceback: "+str(traceback.format_exc()))
			else:
				log(True,"Module %s has no react function" % (m)) 
		except Exception as e:
			log(True,("Exception in module %s: %s " % (m,str(e))) )
			log(False,"Traceback: "+str(traceback.format_exc()))
		del this_m
	return threads
def main():
	log(True,"Establishing connection to [%s]" % (cfg["server"]))
	# Connect
	irc.connect((cfg["server"], cfg["port"]))
	irc.setblocking(False)
	irc.send("PASS %s\r\n" % (cfg["password"]))
	irc.send("USER "+ cfg["nick"] +" "+ cfg["nick"] +" "+ cfg["nick"] +" :sleumasBot\r\n")
	irc.send("NICK "+ cfg["nick"] +"\r\n")
	errors = 0
	timeElapsed = 0
	while True:
		try:
			time.sleep(0.1)
			timeElapsed += 1
			text=irc.recv(2040)
			errors = 0
			log(True,text)
			if text.find("PING") != -1:
				irc.send("PONG " + text.split() [1] + "\r\n")
				log(True,"Ping Request Responded to Successfully")
			if text.find("Nickname is already in use") != -1:
				irc.send("NICK "+ cfg["nick"]+"_\r\n")
				irc.send("PRIVMSG nickserv :identify %s %s\r\n" % (cfg["nick"], cfg["password"]))
				irc.send("PRIVMSG nickserv :ghost %s\r\n" % (cfg["nick"]))
				time.sleep(1)
				irc.send("NICK "+ cfg["nick"]+"\r\n")
				sleep(0.5)
		except:
			print("Read error (expected)")
			errors += 1
			if errors >= 3 and timeElapsed >= 10:
				del timeElapsed
				del errors
				break
	irc.send("PRIVMSG nickserv :identify %s %s\r\n" % (cfg["nick"], cfg["password"]))
	time.sleep(1)
	for c in cfg["defaultChannels"]:
		irc.send("JOIN "+ c +"\r\n")
	log(True,"Connected")
	while True:
		moduleList = ()
		for m in packageContents("modules"):
			if m != "modules" and m != "__init__":
				moduleList += (m,)
		threads = []
		try:
			text=irc.recv(2040)
			text = text.split("\r\n") [:-1]
			for t in text:
				if t.find("ERROR :Closing link:") != -1:
					closingStatus = t
					log(True,"Link Closed. Reason: %s" % (closingStatus))
					sys.exit()
					break
				if t.find("[Errno 10054] An existing connection was forcibly closed") != -1:
					closingStatus = t
					log(True,"Link Closed. Reason: %s" % (closingStatus))
					sys.exit()
					break	
				if t.find("KILL "+cfg["nick"]) != -1:
					closingStatus = t.split(" ")[0]+" killed connection because "+" ".join(t.split(" ")[3:])
					log(True,"Link Closed. Reason: %s" % (closingStatus))
					sys.exit()
					break
				threads = react(t,moduleList)
				for t in threads.values():
					t.join()
				print("all joined")
		except Exception as e:
			if str(e) != "[Errno 2] _ssl.c:1426: The operation did not complete (read)":
				log(True,"Exception in main loop: "+str(e))
				log(False,"Traceback: "+str(traceback.format_exc()))
	log(True,"Link Closed. Reason: %s" % (closingStatus))
if __name__ == "__main__":
	main()