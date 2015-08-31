import conf
from time import sleep
commandPrefix = conf.read()["commands"]["commandPrefix"]
def say(user,message,irc):
	i = 0
	while True:
		if message == "":
			break
		if message.find("\n") != -1 and message.find("\n") != len(message)-1:
			otherlines = message[(message.find("\n")+1):]
			message = message[:message.find("\n")]
		else:
			otherlines = ""
		while True:
			if len(message) > 455:
				messageToSay = " ".join(message[:455].split(" ")[:-1])
				message = message[:455].split(" ")[-1]+message[455:]
				print ("START")
				print messageToSay
				print "---"
				print message
				print ("END")
				irc.send("PRIVMSG "+user+" :"+messageToSay+" \r\n")
				i += 1
				del messageToSay
				if i >= 5:
					sleep(1)
			else:
				i += 1
				irc.send("PRIVMSG "+user+" :"+message+" \r\n")
				break
		message = otherlines
		if i >= 5:
			sleep(1)
def me(user,message,irc):
	irc.send("PRIVMSG "+user+" :"+"\x01"+"ACTION "+message+"\x01"+"\r\n")
def send(command,args,irc):
	if len(args) == 1:
		irc.send(command.upper()+" :"+args[1])
	elif len(args) != 0:
		irc.send(command.upper()+" "+" ".join((args[:-1])+" :"+args[-1]))
	else:
		irc.send(command.upper())
def type(input):
	i = input.split(" ")
	if len(i) == 1:
		return {type:"?","from":sender,args:""}
	sender,type = i[:2]
	args = i[2:]
	if type == "PRIVMSG":	
		return {"type":type,"from":sender,"to":args[0],"message":" ".join(args[1:])[1:]}
	else:
		return {"type":type,"from":sender,"args":stripBlanks(args)}
def join(*channels):
	for c in channels:
		irc.send("JOIN "+ c +"\r\n")
def part(*channels):
	for c in channels:
		irc.send("PART "+ c +"\r\n")
def command(message):
	if message["type"] == "PRIVMSG":
		m = message["message"].split(" ")
		if m[0][0] == commandPrefix:
			command = m[0][len(commandPrefix):]
			args = m[1:]
			try:
				if isinstance(args, basestring):
					args = [args]
			except:
				if isinstance(args, str) or isinstance(args, unicode):
					args = [args]
			message.update({"args":stripBlanks(args)})
			return command,message
		else:
			print "This is commands.py:"+commandPrefix+"##"+m[0][0]
			return "",message
	else:
		return None,message
def senderFormat(sender,type):
	if sender[0] == ":":
		sender = sender[1:]
	if type.lower() == "nick":
		return sender.split("!")[0]
	elif type.lower() == "ident":
		return sender.split("!")[1].split("@")[0]
	elif type.lower() == "host":
		return sender.split("@")[1]
	else:
		return sender
def substitute(text,message,alt={},altm={}):
	for k in altm:
		alt.update({k:message[altm[k]]})
	dict = {"sender":senderFormat(message["from"],"nick"),"senderNick":senderFormat(message["from"],"nick"),"senderIdent":senderFormat(message["from"],"ident"),"senderHost":senderFormat(message["from"],"host"),"original message":message["message"]}
	dict.update(alt)
	return text.format(**dict)
def stripBlanks(list):
	list2 = []
	for i in list:
		if i in ["",None," "]:
			pass
		else:
			list2 += [i]
	return list2