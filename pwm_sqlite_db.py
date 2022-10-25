


import sqlite3

def lower_strip(string):
    return string.lower().strip()


class pwmDB:
    def __init__(self,fname,ftable_name):
        self.fname = fname
        self.ftable = ftable_name
        self.conn = sqlite3.connect(self.fname,check_same_thread=False)
        self.cur = self.conn.cursor()
        
        self.exec_cmd(f"""CREATE TABLE if not exists {self.ftable} (
            key text,
            passw text
        )""")
     

    def exec_cmd(self ,cmd,tup=None):
        if tup != None:
            self.cur.execute(cmd,tuple(tup))
            self.conn.commit()
        
        else:
            self.cur.execute(cmd)
            self.conn.commit()
    
    def getKeys(self):
        keysarr = []
        for data in self.getAllData():
            keysarr.append(data[1])
        
        return keysarr
           
    
    def getValues(self):
        valarr = []
        for data in self.getAllData():
            valarr.append(data[2])
        
        return valarr

    def GetDict(self):
        datas = {}
        for data in self.getAllData():
            datas.update({data[1] : data[2]})
        
        return datas
        
    
    def addData(self,key,passw,exc = None):
        if exc == None:
            exc = 'exist'
        if lower_strip(key) not in self.getKeys():
            self.exec_cmd(f"INSERT INTO {self.ftable} VALUES (?,?)",tup=(lower_strip(key),passw))
        else:
            return exc
    
    
    def updateData(self,key,new_passw):
        self.exec_cmd(f"UPDATE {self.ftable} SET passw = ? WHERE key = ?",tup=(new_passw,key))
    
    def update_by_passw(self,old_passw,new_passw):
        self.exec_cmd(f"UPDATE {self.ftable} SET passw = ? WHERE passw = ?",tup=(new_passw,old_passw))
    
    
    
    def removeAllData(self):
        self.exec_cmd(f"DELETE FROM {self.ftable}")
    
    def removeData(self,key):
        self.exec_cmd(f"DELETE FROM {self.ftable} WHERE key = ?",tup=(lower_strip(key),))
    
    
    
    def getAllData(self):
        self.exec_cmd(f"SELECT rowid,* FROM {self.ftable}",tup=None)
        return self.cur.fetchall()

    def get_by_key(self,key):
        self.exec_cmd(f"SELECT rowid, * FROM {self.ftable} WHERE key = ?",tup=(lower_strip(key),))
        return self.cur.fetchone()

    def get_by_passw(self,passw,key_only = None ):
       
        if key_only == None:
            key_only = False
       
        self.exec_cmd(f"SELECT rowid,* FROM {self.ftable} WHERE passw = ?",tup=(passw,))
        if key_only == False:
            return self.cur.fetchone()
        
        else:
            return self.cur.fetchone()[1]
        

 

