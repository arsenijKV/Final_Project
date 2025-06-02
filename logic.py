import sqlite3
from config import DATABASE

class DB_Manager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE question(
                                    id INTEGER PRIMARY KEY,
                                    questions TEXT NOT NULL,
                                    tags TEXT
                                    
                                    
                                    
                        )''') 

            conn.commit()

            
        
            conn.execute('''
                        CREATE TABLE user_answers (
                            user_id INTEGER,
                            question_key INTEGER,
                            answer TEXT,
                            FOREIGN KEY(question_key) REFERENCES question(id)
                        )''')

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
        
    def get_all_quest(self):
        sql = 'SELECT id, questions FROM question'
        return self.__select_data(sql)
    
    def save_answer(self, user_id, key, answer):
        sql = 'INSERT INTO user_answers (user_id, question_key, answer) VALUES (?, ?, ?)'
        self.__executemany(sql, [(user_id, key, answer)])

    def insert_quest(self):
        all_questions = {
            "learn": "Где бы ты хотел работать (учиться)?",
            "job_wear": "Какой стиль (форму) работы ты предпочетаешь?",
            "skills": "Какими навыками ты обладаешь?",
            "internship": "Где ты ранее учился (работал)?",
            "kind": "Что тебе важно в работе?",
            "sfera": "Есть ли у тебя любимая сфера?",
            "motiv": "Что тебя мотивирует в работе?",
            "sientist": "Какое научное направление тебя интересует?",
            "annoy": "Что неудовлетворяет в работе?",
            "workers": "Что вы неприемлете в профессиональных отношениях?"
        }

        data = [(question, key) for key, question in all_questions.items()]
        sql = 'INSERT INTO question (questions, tags) VALUES (?, ?)'
        self.__executemany(sql, data)

    def get_user_ansfer(self):
        sql = 'SELECT answer FROM user_answers'
        return self.__select_data(sql)
    
    def get_user_answer(self, user_id):
        sql = '''SELECT user_answers.user_id, question.questions, user_answers.answer
                 FROM user_answers
                 INNER JOIN question ON user_answers.question_key = question.id
                 WHERE user_answers.user_id = ?
                 '''
        return self.__select_data(sql = sql, data = (user_id,))



    
        

        
        
    
if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()
    manager.insert_quest()