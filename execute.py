#!/usr/bin/python

import sys, getopt, getpass, hashlib

from identityController import NoSuchIdentityException, PropertyAlreadyExistException, PropertyDoesNotExistException, NoMatchingIdentityException
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
				identityController.searchIdentity(arg)
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
	print "At anytime:\n"
	print "   \"help\" to trigger help information\n"
	print "   \"exit\" to exit from Password Manager console\n" 

	print "While inside of Password Manager console:\n"
	print "   \"list\" to view all identities with their ID\n"
	print "   \"find <query>\" to find identity with name similar to <query>\n"
	print "   \"enter <identity-name>\" to enter Identity, or similarly,"
	print "   \"enter <identity-ID>\"\n"
	print "   \"create <new-identity-name>\" to create new identity\n"
	print "   \"remove <existing-identity-name>\" to remove identity\n"

	print "While inside of Identity:\n"
	print "   \"list\" to view all identity's information\n"


	return


def run():

	global identityID 
	identityID = None

	while True:
		print "[PM]> ",

		if identityID is not None:
			print view.getIdentityName(identityID)+" >",

		rawInput = raw_input().split()
		if len(rawInput) > 1:
			action = rawInput[0]
			actionParameter = ' '.join(rawInput[1:])
		elif len(rawInput) == 1:
			action = rawInput[0]
			actionParameter = None
		else:
			action = None
			actionParameter = None


		if action is None:		#If nothing entered
			continue
		elif action == "exit":
			sys.exit()
		elif action == "help":
			internalConsoleHelper()
			continue
		else:
			if identityID is None:
				'''
				If querying for Identity
				'''
				if action == "list":
					view.viewAllIdentities()
					continue
				elif action == "find":
					if actionParameter is not None:
						try:
							result = identityController.searchIdentity(actionParameter)
							view.viewPropertiesByID(result)
							continue
						except NoMatchingIdentityException, e:
							print "No matching identity found, here are some similar results:"
							view.viewSetOfIdentities(e.similarResults)
							continue
					else:
						print "Invalid search: find <name>"
						continue
				elif action == "create":
					if actionParameter is not None:
						view.createIdentity(actionParameter)
						continue
					else:
						print "Invalid systax"
						print "Usage: create <identity-name>"
						continue

				elif action == "remove":
					if actionParameter is not None:
						view.removeIdentity(actionParameter)
						continue
					else:
						print "Invalid systax"
						print "Usage: remove <identity-name>"
						continue

				elif action == "enter":
					if actionParameter is not None:
						try:
							result = view.getIdentityIDFromInput(actionParameter)
							identityID = result
							continue
						except NoMatchingIdentityException, e:
							print "No matching identity found, here are some similar results:"
							view.viewSetOfIdentities(e.similarResults)
							continue
					else:
						print "Invalid syntax"
						print "Usage: enter <identity-ID> or enter <identity-name>"
						continue
			else:
				'''
				If querying for property
				'''
				if action == "list":
					view.viewPropertiesByID(identityID)
					continue
				elif action == "back":
					identityID = None
					continue
				elif action == "set":
					if actionParameter is not None:
						view.setProperty(identityID, actionParameter)
						continue
					else:
						print "Invalid syntax"
						print "To create new property:"
						print "set <property-name>"
						print "Your value will be recorded in the Vim editor"
						continue
				elif action == "remove":
					if actionParameter is not None:
						identityController.removeProperty(identityID, actionParameter)
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
