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
        for entry in entires:
            jsonData = entry[1]
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
        if(sqlJsonData != None):          #Check if Identity exist
            return sqlJsonData[0]
        else:
            raise NoSuchIdentityException()
        return

    def fetchAllIdentities(self):
        """
        List all Identities
        """
        entires = self.databaseController.fetchAll()

        results = {}
        for entry in entires:
            jsonData = entry[1]
            data = json.loads(jsonData)
            results[entry[0]] = data['name']
            #print data['name'] + " [" + str(entry[0]) + "]"
        return results

    def fetchIdentityIDByName(self, name):
        """
        Fetch identity ID by identity name
        """
        entires = self.databaseController.fetchAll()
        for entry in entires:
            jsonData = entry[1]
            data = json.loads(jsonData)
            if data['name'] == name:
                return entry[0] #return ID

        return None    #If no identity is found by name

    def listSimilar(self, inputName):
        """
        Find all identities with name containing input
        """
        regexp = re.compile(inputName.lower())  #Convert to lowercase for comparison

        entires = self.databaseController.fetchAll()

        results = {}
        for entry in entires:
            jsonData = entry[1]
            data = json.loads(jsonData)
            if regexp.search(data['name'].lower()) is not None:
                results[entry[0]] = data['name']
                #print data['name'] + " [" + str(entry[0]) + "]"
        return results

    def removeIdentity(self, name):
        """
        Remove identity given name
        """
        entires = self.databaseController.fetchAll()
        for entry in entires:
            jsonData = entry[1]
            data = json.loads(jsonData)
            if data['name'] == name:
                self.databaseController.removeIdentity(entry[0]) 
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
