import sqlite3
from aesController import AESController


class DatabaseController:
    
    conn = None
    connCursor = None
    aes = None

    def __init__(self, dbPath, systemPassword):
        self.conn = sqlite3.connect(dbPath)
        self.connCursor = self.conn.cursor()
        self.aes = AESController(systemPassword)

        #Create table if not exist
        sql = 'CREATE TABLE IF NOT EXISTS identities (id INTEGER PRIMARY KEY, data text)'
        self.connCursor.execute(sql)
        self.conn.commit()
        return

    def createIdentity(self, data):
        
        self.connCursor.execute('''INSERT INTO identities (data) values (?)''', [(self.aes.encrypt(data))])
        self.conn.commit()
        return

    def fetchAll(self):
        self.connCursor.execute('''SELECT id,data FROM identities''')
        return self.connCursor.fetchall()
    
    def readData(self, ID):

        self.connCursor.execute('''SELECT data FROM identities WHERE id = ? ORDER BY ROWID ASC LIMIT 1''', [(ID)])
        return self.connCursor.fetchone()

    def modifyIdentity(self, ID, data):
        self.connCursor.executemany('''UPDATE identities SET data = ? WHERE id = ?''', [(data, ID)])
        self.conn.commit()
        return

    def removeIdentity(self, ID):
        
        self.connCursor.execute('''DELETE FROM identities WHERE id = ?''', [(ID)])
        self.conn.commit()
        return


