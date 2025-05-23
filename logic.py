import sqlite3
from config import DATABASE

class DB_Manager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE questions(
                                    id INTEGER PRIMARY KEY,
                                    questions TEXT NOT NULL,
                                    tags TEXT
                                    
                                    
                                    
                        )''') 

            conn.commit()




    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
        

        
        
    
if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()