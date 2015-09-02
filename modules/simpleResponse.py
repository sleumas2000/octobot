# Simple Response Module for sleumasBot
# written by sleumas2000
__help__ = "Simple Response Module. Provides text responses on certain triggers. Also allows you to add commands. For more help, type !sr help"
defaultConf = {'texts': [{'reactText': 'b', 'matchType': 'equals', 'matchText': 'a', 'reactType': 'say', 'reactTo': 'channel'}, {'reactText': '2', 'matchType': 'equals', 'matchText': '1', 'reactType': 'say', 'reactTo': 'channel'}, {'reactText': 'Cheer up, {sender}, All your friends are here!', 'matchType': 'contains', 'matchText': ':(', 'reactType': 'say', 'reactTo': 'channel'}, {'reactText': 'Cheer up, {sender}, All your friends are here!', 'matchType': 'contains', 'matchText': ":'(", 'reactType': 'say', 'reactTo': 'channel'}, {'reactText': 'Cheer up, {sender}, All your friends are here!', 'matchType': 'contains', 'matchText': ';(', 'reactType': 'say', 'reactTo': 'channel'}, {'reactText': 'Cheer up, {sender}, All your friends are here!', 'matchType': 'contains', 'matchText': 'D:', 'reactType': 'say', 'reactTo': 'channel'}], 'commands': {'hug': {'reactText': 'hugs {arg1}', 'reactType': 'me', 'reactTo': 'channel'}, 'ping': {'reactText': 'Pong {arg1} {arg2} {arg3} {arg4} {arg5} {arg6} {arg7} {arg8} {arg9} {arg10}', 'reactType': 'me', 'reactTo': 'channel'}, 'slap': {'reactText': 'slaps {arg1}', 'reactType': 'me', 'reactTo': 'channel'}}, 'helpText': {'edit': '{cp}sr edit command <name> <me|say> <channel|sender> <response> or {cp}sr edit text <equals|contains> <text to match> <me|say> <channel|sender> <response>', 'add': '{cp}sr add command <name> <me|say> <channel|sender> <response> or {cp}sr add text <equals|contains> <text to match> <me|say> <channel|sender> <response>', 'list': '{cp}sr list <command|text>', 'help': 'Available commands: ADD, EDIT, LIST, REMOVE. Type {cp}sr help <command> for more help', 'remove': '{cp}sr remove command <name> or {cp}sr remove text <text to match>'}}
import common
import traceback
cfg = common.persistence.confLoad("simpleResponse",defaultConf)
helpText = cfg["helpText"]
for k,t in helpText.items():
	helpText.update({k:t.replace("{cp}",common.conf.read()["commands"]["commandPrefix"])})
commands = cfg["commands"]
texts = cfg["texts"]
def help(args,caller,irc):
	print("Help is running")
	print("help("+str(args)+","+str(caller)+","+str(irc)+")")
	if len(args) <= 1:
		common.say(common.senderFormat(caller,"nick"),helpText["help"],irc)
	elif args[1] == "":
		print("saying helptext")
		common.say(common.senderFormat(caller,"nick"),helpText["help"],irc)
		print("said helptext")
	elif args[1][0] == "a":
		common.say(common.senderFormat(caller,"nick"),helpText["add"],irc)
	elif args[1][0] == "r":
		common.say(common.senderFormat(caller,"nick"),helpText["remove"],irc)
	elif args[1][0] == "e":
		common.say(common.senderFormat(caller,"nick"),helpText["edit"],irc)
	elif args[1][0] == "l":
		common.say(common.senderFormat(caller,"nick"),helpText["list"],irc)
	else:
		common.say(common.senderFormat(caller,"nick"),"Yerwhat!?",irc)
def add(args,caller,irc):
		if len(args) < 6:
			common.say(common.senderFormat(caller,"nick"),"Oops, try sending the right number of arguments (see \"{cp}sr help add\" if you're having trouble)".replace("{cp}",common.conf.read()["commands"]["commandPrefix"]),irc)
		elif args[1][0].lower() == "c": #command
			if len(args) > 6:
				args[5] = " ".join(args[5:])
				args = args[:6]
			if len(args) == 6:
				if args[3][0].lower() in ("m","s") and args[4][0].lower() in ("c","s"): #me,say channel,sender
					name = args[2]
					if args[3][0].lower() == "m":
						args[3] = "me"
					elif args[3][0].lower() == "s":
						args[3] = "say"
					if args[4][0].lower() == "c":
						args[4] = "channel"
					elif args[4][0].lower() == "s":
						args[4] = "sender"
					command = {"reactType":args[3],"reactTo":args[4],"reactText":args[5]}
					# DO THIS
					cfg = common.persistence.confLoad("simpleResponse",defaultConf)
					try:
						texts = cfg["texts"]
						commands = cfg["commands"]
						helpText = cfg["helpText"]
					except:
						common.say(common.senderFormat(caller,"nick"),"Something done gone wrong :(",irc)
					commands.update({name:command})
					common.persistence.confSave("simpleResponse",{"commands":commands,"texts":texts,"helpText":helpText})
					common.say(common.senderFormat(caller,"nick"),"Hoorah! command \"{cp}{0}\" will be responded to by {1} with \"/{2} {3}\"".replace("{cp}",common.conf.read()["commands"]["commandPrefix"]).format(args[2],args[4],args[3],args[5]),irc)
				else:
					common.say(common.senderFormat(caller,"nick"),"Oops, something went wrong. Check all your arguments are valid. (see \"{cp}sr help add\" if you're having trouble)".replace("{cp}",common.conf.read()["commands"]["commandPrefix"]),irc)
			else:
				common.say(common.senderFormat(caller,"nick"),"Oops, try sending the right number of arguments (see \"{cp}sr help add\" if you're having trouble)".replace("{cp}",common.conf.read()["commands"]["commandPrefix"]),irc)
		elif args[1][0].lower() == "t": #text
			if len(args) > 7:
				args[6] = " ".join(args[6:])
				args = args[:7]
			if len(args) == 7:
				if args[2][0].lower() in ("e","c") and args[4][0].lower() in ("m","s") and args[5][0].lower() in ("c","s"): #equals,contains me,say channel,sender
					if args[4][0].lower() == "m":
						args[4] = "me"
					elif args[4][0].lower() == "s":
						args[4] = "say"
					if args[5][0].lower() == "c":
						args[5] = "channel"
					elif args[5][0].lower() == "s":
						args[5] = "sender"
					if args[2][0].lower() == "e":
						args[2] = "equals"
					elif args[2][0].lower() == "c":
						args[2] = "contains"
					else:
						common.say(common.senderFormat(caller,"nick"),"Yerwhat!?",irc)
					command = {"matchType":args[2],"matchText":args[3],"reactType":args[4],"reactTo":args[5],"reactText":args[6]}
					cfg = common.persistence.confLoad("simpleResponse",defaultConf)
					try:
						texts = cfg["texts"]
						commands = cfg["commands"]
						helpText = cfg["helpText"]
					except:
						common.say(common.senderFormat(caller,"nick"),"Something done gone wrong :(",irc)
					texts += [command]
					cfg.update({"texts":texts,})
					common.persistence.confSave("simpleResponse",cfg)
					common.say(common.senderFormat(caller,"nick"),"Hoorah! text that {0} \"{1}\" will be responded to by {2} with \"/{3} {4}\"".format(args[2],args[3],args[5],args[4],args[6]),irc)
				else:
					common.say(common.senderFormat(caller,"nick"),"Oops, something went wrong. Check all your arguments are valid. (see \"!sr help add\" if you're having trouble)",irc)
			else:
				common.say(common.senderFormat(caller,"nick"),"Oops, try sending the right number of arguments (see \"!sr help add\" if you're having trouble)",irc)
		else:
			common.say(common.senderFormat(caller,"nick"),"Yerwhat!?",irc)
def remove(args,caller,irc):
	pass
def edit(args,caller,irc):
	pass
def list(args,caller,irc):
	pass
def textReact(message,irc):
	try:
		for c in texts:
			if c["reactTo"] == "sender":
				reactTo = common.senderFormat(message["from"],"nick")
			elif c["reactTo"] == "channel":
				if ommon.senderFormat(message["to"],"nick") != common.conf.read()["nick"]:
					reactTo = message["to"]
				else:
					reactTo = common.senderFormat(message["from"],"nick")
			if c["matchType"] == "equals" and message["message"].lower() == common.substitute(c["matchText"].lower(),message):
				if c["reactType"] == "say":
					common.say(reactTo,common.substitute(c["reactText"],message),irc)
					return True
				elif c["reactType"] == "me":
					common.me(reactTo,common.substitute(c["reactText"],message),irc)
					return True
			elif c["matchType"] == "contains" and message["message"].lower().find(common.substitute(c["matchText"].lower(),message)) != -1:
				if c["reactType"] == "say":
					common.say(reactTo,common.substitute(c["reactText"],message),irc)
					return True
				elif c["reactType"] == "me":
					common.me(reactTo,common.substitute(c["reactText"],message),irc)
					return True
		return False
	except:
		pass
def srEdit(message,irc):
	args = message["args"]
	print("I am running srEdit("+str(message)+","+str(irc)+")")
	if len(args) == 0:
		help(args,message["from"],irc)
	elif args[0][0].lower() == "h":
		print("arg was h")
		help(args,message["from"],irc)
	elif args[0][0].lower() == "a":
		add(args,message["from"],irc)
	elif args[0][0].lower() == "r" or args[0][0].lower() == "d":
		remove(args,message["from"],irc)
	elif args[0][0].lower() == "e":
		edit(args,message["from"],irc)
	elif args[0][0].lower() == "l":
		list(args,message["from"],irc)
	else:
		help(args,message["from"],irc)
def commandReact(command,message,irc):
	arg = {}
	for i in range(0,len(message["args"])):
		arg.update({"arg"+str(i+1):message["args"][i]})
	if len(message["args"]) < 10:
		for i in range(len(message["args"]),10):
			arg.update({"arg"+str(i+1):""})
	for name in commands:
		c = commands[name]
		if c["reactTo"] == "sender":
			reactTo = common.senderFormat(message["from"],"nick")
		elif c["reactTo"] == "channel":
			if message["to"].split("!")[0] != common.conf.read()["nick"]:
				reactTo = message["to"]
			else:
				reactTo = common.senderFormat(message["from"],"nick")
		if command == name and c["reactType"] == "say":
			common.say(reactTo,common.substitute(c["reactText"],message,arg),irc)
			return True
		elif command == name and c["reactType"] == "me":
			common.me(reactTo,common.substitute(c["reactText"],message,arg),irc)
			return True
	return False
def react(input,irc):
	command,message = common.command(common.type(input)) # dict
	if command == None:
		return
	elif command == "":
		textReact(message,irc)
	elif command == "sr" or command == "simpleresponse":
		srEdit(message,irc)
	else:
		commandReact(command,message,irc)
	print "stopping \"simpleResponse\""