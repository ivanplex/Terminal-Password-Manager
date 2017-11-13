import json
import re
from databaseController import DatabaseController
from inputUtil import query_yes_no

class IdentityController:

    databaseController = None

    def __init__(self, dbPath, systemPassword):

        self.databaseController = DatabaseController(dbPath, systemPassword)

        return

    def createIdentity(self, name, classification, password):

        #Check if Identity already exist
        entires = self.databaseController.fetchAll()
        for ID, jsonData in entires.iteritems():
            data = json.loads(jsonData)
            if (data['name'] == name):
                raise IdentityAlreadyExistException()
                return
        
        data = {}
        data['name'] = name
        data['classification'] = classification
        data['password'] = password

        self.databaseController.createIdentity(json.dumps(data))
        return

    def fetchIdentityByID(self, ID):
        """
        Fetch Identity by ID
        """
        sqlJsonData = self.databaseController.readData(ID)
        if(sqlJsonData is not None):          #Check if Identity exist
            return sqlJsonData
        else:
            raise NoSuchIdentityException()
        return

    def fetchAllIdentities(self):
        """
        List all Identities

        return <key> <identity-name> pair
        """
        result = {}
        entires = self.databaseController.fetchAll()
        for ID, jsonData in entires.iteritems():
            data = json.loads(jsonData)
            result[ID] = data['name']

        return result

    def fetchIdentityIDByName(self, name):
        """
        Fetch identity ID by identity name
        """
        entires = self.databaseController.fetchAll()
        for ID, jsonData in entires.iteritems():
            data = json.loads(jsonData)
            if data['name'] == name:
                return ID #return ID

        return None    #If no identity is found by name

    def listSimilar(self, inputName):
        """
        Find all identities with name containing input
        """
        regexp = re.compile(inputName.lower())  #Convert to lowercase for comparison

        entires = self.databaseController.fetchAll()

        results = {}
        for ID, jsonData in entires.iteritems():
            data = json.loads(jsonData)
            if regexp.search(data['name'].lower()) is not None:
                results[ID] = data['name']

        return results

    def searchIdentity(self, query):
        """
        Search for Identity using identity name.

        If only one identity is found, the Identity's ID will be returned.
        If more than one identities are found, a list of similar identities
        will be printed.

        Args:
            query (string): Identity name queried by user

        Returns:
            int: One identity is found and return the identity's ID
            dictionaries: More than one or no identity is found. 
                    - Identity ID <int> : Identity Name<string>
                    - An empty dictionary could be return if no result is found

        """
        identities = self.listSimilar(query)

        if(len(identities) == 1):
            #Print details of identity
            identityID = None
            for key, value in identities.iteritems():
                identityID = key

            return identityID
        else:
            #print all similar identities
            '''
            print "No matching identity found, here are some similar results:"
            for key, value in identities.iteritems():
                print value+": ["+str(key)+"]"
            '''
            raise NoMatchingIdentityException(identities)
            return None

    def removeIdentity(self, name):
        """
        Remove identity given name
        """
        entires = self.databaseController.fetchAll()
        for ID, jsonData in entires.iteritems():
            data = json.loads(jsonData)
            if data['name'] == name:
                self.databaseController.removeIdentity(ID) 
                return

        raise NoSuchIdentityException()
        return

    def checkIfPropertyExist(self, data, key):
        if(key in data):
            return True
        else:
            return False

    def createProperty(self, ID, key, value):
        """
        Create property but would NOT attempt to overwrite

        throws exception if 
            - property ID does not exist
            - attempt to overwrite property
        """
        #Read property by ID
        jsonData = self.fetchIdentityByID(ID)

        #Check if such property already exist
        data = json.loads(jsonData)
        if(self.checkIfPropertyExist(data, key)):
            raise PropertyAlreadyExistException()
            #refer to editing Property
        else:
            data[key] = value
            self.databaseController.modifyIdentity(ID, json.dumps(data))   #Save into database         
        #TODO: Sanitize Input
        return

    def viewProperty(self, ID, key):
        """
        Read property information
        """

        #Read property by ID
        jsonData = self.fetchIdentityByID(ID)

        #Check if such property already exist
        data = json.loads(jsonData)
        if(not self.checkIfPropertyExist(data, key)):
            raise PropertyDoesNotExistException()
            #refer to creating Property
        else:
            return data[key]


    def modifyProperty(self, ID, key, value):
        """
        Modify property 

        return true if property is modified

        throws exception if 
            - property ID does not exist
            - property does not exist
        """
        #Read property by ID
        jsonData = self.fetchIdentityByID(ID)

        #Check if such property exist
        data = json.loads(jsonData)
        if(not self.checkIfPropertyExist(data, key)):
            raise PropertyDoesNotExistException()
            #refer to creating Property
        else:
            if query_yes_no("Wouly you like to modify \""+key+"\" ?", None):
                data[key] = value
                self.databaseController.modifyIdentity(ID, json.dumps(data))   #Save into database
                return True
            else:
                return False
        return

    def removeProperty(self, ID, key):
        """
        Remove property given identity ID and property key

        return True if property deleted

        throws exception if 
            - property ID does not exist
            - property does not exist
        """
        #Read property by ID
        jsonData = self.fetchIdentityByID(ID)

        #Check if such property exist
        data = json.loads(jsonData)
        if(not self.checkIfPropertyExist(data, key)):
            raise PropertyDoesNotExistException()
            #refer to creating Property
        else:
            print '::'+key+':: is currently: '+ data[key]
            if query_yes_no("Are you sure to delete: "+ key + " ?", None):
                del data[key]
                self.databaseController.modifyIdentity(ID, json.dumps(data))   #Save into database
                return True
            else:
                return False
        return


class NoMatchingIdentityException(Exception):
    """
    No matching Identity was found
    This could be triggered by an ambiguous search term

    Attributes:
        similarResults: A dictionary of simiar results
                    - Identity ID <int> : Identity Name<string>
    """
    def __init__(self, similarResults):
        self.similarResults = similarResults

class IdentityAlreadyExistException(Exception):
    pass

class NoSuchIdentityException(Exception):
    pass

class PropertyAlreadyExistException(Exception):
    pass

class PropertyDoesNotExistException(Exception):
    pass

'''
i = IdentityHandler('data.db')
#i.createIdentity('hsbc', 'bank','12345678')
try:
    i.listSimilar('hs')
except NoSuchIdentityException as exp:
    print exp
'''
