import json, re, tempfile, os, sys, getpass


from identityController import IdentityController
from identityController import NoSuchIdentityException, PropertyAlreadyExistException, PropertyDoesNotExistException, IdentityAlreadyExistException, NoMatchingIdentityException
from inputUtil import query_yes_no, callEditor

class View:

    identityController = None

    def __init__(self, dbPath, systemPassword):

        self.identityController = IdentityController(dbPath, systemPassword)

        #self.identityController.createIdentity('hsbc', None, None)
        return

    def createIdentity(self, name):
        """
        Ask user to fill information before creating identity
        """
        password = getpass.getpass()
        print "Class: ",
        classification = raw_input()

        try:
            self.identityController.createIdentity(name, classification, password)
        except IdentityAlreadyExistException:
            print "Error: Identity Alread Exist!\n"
            return

        print "Identity: "+name+" created successfully."
        return

    def removeIdentity(self, name):
        """
        Remove identity

        User must confirm removal with y/n
        """
        if query_yes_no("Are you sure to delete identity: "+name+" ?", None):
            try:
                self.identityController.removeIdentity(name)
            except NoSuchIdentityException:
                print "Identity Not Found."
                print "Usage: remove <identity-name>"
        else:
            print "Action removal terminated."
            return


    def viewAllIdentities(self):
        identities = self.identityController.fetchAllIdentities()
        #print identities
        for key, value in identities.iteritems():
            print value+": ["+str(key)+"]"

    def viewSetOfIdentities(self, identities):
        """
        Print the given list of identities

        Args:
            dictionaries: List of Identities in the following format
                        Identity ID <int> : Identity Name<string>
        """
        for key, value in identities.iteritems():
            print value+": ["+str(key)+"]"


    def getIdentityName(self, ID):
        jsonData = self.identityController.fetchIdentityByID(ID)
        data = json.loads(jsonData)
        return data['name']

    def getIdentityIDFromInput(self, input):
        """
        Find identity and return identity ID from user input
        User might input identity ID directly or identity name
        The function priorites identity name over ID
        
        For example:    
            If identity name: "3" exist, it will return the identity with name "3"
            instead of identity with ID = "3"

        return identity-ID
        """
        try:
            try:

                ID = self.identityController.searchIdentity(input)
                return ID

            except NoMatchingIdentityException, e:

                self.getIdentityName(input) #Check if ID exist by testing if getIdentityName returns valid output
                return input

        except NoSuchIdentityException:
            print "No matching identity found, here are some similar results:"
            self.viewSetOfIdentities(e.similarResults)

        return None     #Return None if no result is found by name/ID


    def viewPropertiesByID(self, ID):
        jsonData = self.identityController.fetchIdentityByID(ID)
        data = json.loads(jsonData)
        print "Identity: "+data['name']
        print "================================="
        for key,value in data.iteritems():
            print key+': '+value

    def setProperty(self, ID, key):
        try:
            preset = self.identityController.viewProperty(ID, key)
            newValue = callEditor(preset)
            self.identityController.modifyProperty(ID, key, newValue)
        except PropertyDoesNotExistException:
            newValue = callEditor()
            self.identityController.createProperty(ID, key, newValue)

        return



    def directQuery(self, identityName, propertyName):
        identities = self.identityController.listSimilar(identityName)

        if(len(identities) == 1):
            #Find Identity ID
            identityID = None
            for key, value in identities.iteritems():
                identityID = key


            #Find property
            regexp = re.compile(propertyName.lower())

            jsonData = self.identityController.fetchIdentityByID(identityID)
            data = json.loads(jsonData)

            for key,value in data.iteritems():
                if(regexp.search(key.lower()) is not None):
                    print key+': '+value
        else:
            #Ambiguous identity name
            print "Ambiguous Account/Identity name"
            print "Below are some similar accounts"
            for key, value in identities.iteritems():
                print value+": ["+str(key)+"]"


#viewPropertiesByID(18)


