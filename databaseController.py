import sqlite3
from time import gmtime, strftime

from aesController import AESController


class DatabaseController:
    
    conn = None
    connCursor = None
    aes = None

    systemPassword = None

    def __init__(self, dbPath, systemPassword):
        self.conn = sqlite3.connect(dbPath)
        self.conn.text_factory = str
        self.connCursor = self.conn.cursor()
        self.aes = AESController()

        self.systemPassword = systemPassword

        #Create table if not exist
        sql = 'CREATE TABLE IF NOT EXISTS identities (id INTEGER PRIMARY KEY, data text, updated_at text)'
        self.connCursor.execute(sql)
        self.conn.commit()
        return

    def createIdentity(self, data):
        
        self.connCursor.executemany('''INSERT INTO identities (data, updated_at) values (?,?)''', [(self.aes.encrypt(data, self.systemPassword), strftime("%Y-%m-%d %H:%M:%S", gmtime()))])
        self.conn.commit()
        return

    def fetchAll(self):
        self.connCursor.execute('''SELECT id,data FROM identities''')
        #return self.connCursor.fetchall()
        results = self.connCursor.fetchall()

        returnArray = {}
        for ID, encryptedData in results:
            returnArray[ID] = self.aes.decrypt(encryptedData, self.systemPassword)

        return returnArray
    
    def readData(self, ID):

        self.connCursor.execute('''SELECT data FROM identities WHERE id = ? ORDER BY ROWID ASC LIMIT 1''', [(ID)])
        #print self.connCursor.fetchone()
        result = self.connCursor.fetchone()
        if result is None:
            return None
        else:
            return self.aes.decrypt(result[0], self.systemPassword)

    def modifyIdentity(self, ID, data):
        self.connCursor.executemany('''UPDATE identities SET data = ?, updated_at = ? WHERE id = ?''', [(self.aes.encrypt(data, self.systemPassword), strftime("%Y-%m-%d %H:%M:%S", gmtime()), ID)])
        self.conn.commit()
        return

    def removeIdentity(self, ID):
        
        self.connCursor.execute('''DELETE FROM identities WHERE id = ?''', [(ID)])
        self.conn.commit()
        return
