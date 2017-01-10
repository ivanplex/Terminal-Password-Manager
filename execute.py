#!/usr/bin/python

import sys, getopt, getpass, hashlib

from identityController import NoSuchIdentityException, PropertyAlreadyExistException, PropertyDoesNotExistException
from view import View
from identityController import IdentityController
from auth import Auth

##############################
#
# Global variables
#
##############################



def displayHelper():
	"""
	Helper in terminal
	"""
	print "Direct Query:"
	print "<accout-name> <property-name> \n"
	print "-h or --help for help"
	print "-l or --list to list all accounts"
	print "-a <account-name> or --account=<account-name> to search for account"

def main(argv):

	#login
	authentication()

	global view
	global identityController

	view = View('data.db', systemPassword)
	identityController = IdentityController('data.db', systemPassword)

	try:
		opts, args = getopt.getopt(argv,'hlai:',["list=","account="])
	except getopt.GetoptError:
		print "Argument Error"
		displayHelper()
		sys.exit(2)

	if(len(opts) == 0 and len(sys.argv[1:]) == 0):
		#Start python Password Manager
		run()
	elif(len(opts) == 0 and len(sys.argv[1:]) == 2):
		#if arguments given in format : <identity-name> <property-name>
		view.directQuery(sys.argv[1],sys.argv[2])
	elif(len(opts) > 0):
	   	for opt, arg in opts:
	   		if opt in ("-h", "--help"):
	   			displayHelper()
			elif opt in ("-l", "--list"):
				print "All Identities"
				print "==================="
				view.viewAllIdentities()
				sys.exit()
			elif opt in ("-a", "--account"):
				view.searchIdentity(arg)
				sys.exit()
			elif opt in ("-i", "--id"):
				view.viewPropertiesByID(arg);
				sys.exit()
			else:
				print "ad"
	else:
		#Unknown argument parsing
		print "Unknown arguments: ",
		for unknownArgument in sys.argv[1:]:
			print unknownArgument,
		print "\n"
		displayHelper()



def internalConsoleHelper():
	"""
	Help information for internal functions
	"""
	print "At anytime:"
	print "\"help\" to trigger help information"
	print "\"exit\" to exit from Password Manager console\n" 
	print "While inside of Password Manager console:"

	return



def run():

	global identityID 
	identityID = None

	while True:
		print "[PM]> ",

		if identityID is not None:
			print view.getIdentityName(identityID)+" >",

		action = raw_input().split()

		if len(action) == 0:		#If nothing entered
			continue
		elif action[0] == "exit":
			sys.exit()
		elif action[0] == "help":
			internalConsoleHelper()
			continue
		else:
			if identityID is None:
				'''
				If querying for Identity
				'''
				if action[0] == "list":
					view.viewAllIdentities()
					continue
				elif action[0] == "find":
					if(len(action) == 2):
						view.searchIdentity(action[1])
						continue
					else:
						print "Invalid search: find <name>"
						continue
				elif action[0] == "create":
					if(len(action) == 2):
						view.createIdentity(action[1])
						continue
					else:
						print "Invalid systax"
						print "Usage: create <identity-name>"
						continue

				elif action[0] == "remove":
					if(len(action) == 2):
						view.removeIdentity(action[1])
						continue
					else:
						print "Invalid systax"
						print "Usage: remove <identity-name>"
						continue

				elif action[0] == "enter":
					if(len(action) == 2):
						identityID = view.getIdentityIDFromInput(action[1])
						continue
					else:
						print "Invalid syntax"
						print "Usage: enter <identity-ID> or enter <identity-name>"
						continue
			else:
				'''
				If querying for property
				'''
				if action[0] == "list":
					view.viewPropertiesByID(identityID)
					continue
				elif action[0] == "back":
					identityID = None
					continue
				elif action[0] == "set":
					if(len(action) == 2):
						view.setProperty(identityID, action[1])
						continue
					else:
						print "Invalid syntax"
						print "To create new property:"
						print "set <property-name>"
						print "Your value will be recorded in the Vim editor"
						continue
				elif action[0] == "remove":
					if(len(action) == 2):
						identityController.removeProperty(identityID, action[1])
						continue
					else:
						print "Invalid syntax"
						print "To remove property:"
						print "remove <property-name>"
						continue

		print "Invalid command"
		internalConsoleHelper()
		continue


def authentication():
	global systemPassword
	systemPassword = getpass.getpass()

	auth = Auth()
	if auth.check_password(systemPassword) is not True:
		print "Invalid login."
		sys.exit()




if __name__ == "__main__":
   main(sys.argv[1:])
