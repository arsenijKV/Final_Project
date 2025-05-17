import sqlite3
from config import DATABASE

class DB_Manager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE work(
                                    name TEXT,
                                    id INTEGER PRIMARY KEY,
                                    minutes INTEGER,
                                    contributor_id INTEGER,
                                    submitted DATE,
                                    tags TEXT,
                                    nutrition TEXT,
                                    n_steps INTEGER,
                                    steps TEXT,
                                    description TEXT,
                                    ingredients TEXT,
                                    n_ingredients INTEGER
                        )''') 
            
            conn.execute('''CREATE TABLE interw(
                                    user_id INTEGER PRIMARY KEY,
                                    recipe_id INTEGER,
                                    FOREIGN KEY(recipe_id) REFERENCES recipe(id),
                                    date DATE,
                                    rating INT,
                                    review TEXT
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