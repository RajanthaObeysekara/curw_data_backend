from os import name
import sqlite3
class StationModel:
    def __init__(self,name,value) :
        self.name= name
        self.value = value     
    
    def json(self):
        return {"name":self.name,"value":self.value}
    @classmethod
    def find_station_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM stations Where name=?"
        resutl = cursor.execute(query,( name,))
        row = resutl.fetchone()
        connection.close()
        if row :
            return cls(*row)
    

    def station_insert(self):
        connection = sqlite3.connect('data.db')
        cursor=connection.cursor()
        query= "INSERT INTO stations VALUES (?, ?)"
        cursor.execute(query,(self.name,self.value))
        connection.commit()
        connection.close()
    
          
    def station_update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE stations SET value =? WHERE name=?" 
        cursor.execute(query,(self.value,self.name,))
        connection.commit()
        connection.close()