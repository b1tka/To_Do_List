import sqlite3

from pprint import pprint
from export import export

class TDLdb:
    def __init__(self):
        self.db_connection = sqlite3.connect('TDL_db.db')
        self.cursor = self.db_connection.cursor()

    def get_profiles(self):
        query = '''SELECT * FROM profiles'''
        data = self.cursor.execute(query).fetchall()
        return data

    def get_id(self, name):
        query = '''SELECT id FROM profiles WHERE name = ?'''
        id = self.cursor.execute(query, (name,)).fetchone()
        return id

    def get_list_id(self, profile_id, lists_name):
        query = '''SELECT id_list FROM lists WHERE id_profile = ? AND lists_name = ?'''
        data = self.cursor.execute(query, (profile_id, lists_name,)).fetchone()
        return data

    def get_list_ids(self, profile_id):
        query = '''SELECT * FROM lists WHERE id_profile = ?'''
        data = self.cursor.execute(query, (profile_id,))
        return data

    def get_lists(self, id_profile):
        query = '''SELECT lists_name FROM lists WHERE id_profile = ?'''
        data = self.cursor.execute(query, (id_profile,)).fetchall()
        return data

    def get_tasks(self, list_id):
        query = '''SELECT task, complete FROM tasks WHERE id_list = ?'''
        data = self.cursor.execute(query, (list_id[0],)).fetchall()
        data = list(map(lambda x: (x[0], 'Не выполнено') if x[-1] == 0 else (x[0], 'Выполнено'), data))
        return data

    def get_task_id(self, text):
        query = '''SELECT id_task FROM tasks WHERE task = ?'''
        data = self.cursor.execute(query, (text,)).fetchone()
        return data

    def get_state_task(self, task_id):
        query = '''SELECT complete FROM tasks WHERE id_task = ?'''
        data = self.cursor.execute(query, (task_id[0],)).fetchone()
        data = 'Выполнено' if data[0] == 1 else 'Не выполнено'
        return data

    def add_profiles(self, profile_name):
        query = '''INSERT INTO profiles(name) VALUES(?)'''
        self.cursor.execute(query, (profile_name,))
        self.db_connection.commit()

    def add_lists(self, profile, list_name):
        query = '''INSERT INTO lists(id_profile, lists_name) VALUES(?, ?)'''
        self.cursor.execute(query, (profile, list_name,))
        self.db_connection.commit()

    def add_task(self, list_id, text):
        query = '''INSERT INTO tasks(id_list, task, complete) VALUES(?, ?, False)'''
        self.cursor.execute(query, (list_id[0], text,))
        self.db_connection.commit()

    def edit_list(self, list_id, text):
        query = '''UPDATE lists SET lists_name = ? WHERE id_list = ?'''
        self.cursor.execute(query, (text, list_id[0],))
        self.db_connection.commit()

    def edit_task(self, task_id, text, state):
        state = False if state == 'Не выполнено' else True
        query = '''UPDATE tasks SET task = ?, complete = ? WHERE id_task = ?'''
        self.cursor.execute(query, (text, state, task_id[0],))
        self.db_connection.commit()

    def delete_list(self, list_id):
        query = '''DELETE FROM lists WHERE id_list = ?'''
        self.cursor.execute(query, (list_id[0],))
        self.db_connection.commit()
        query = '''DELETE FROM tasks WHERE id_list = ?'''
        self.cursor.execute(query, (list_id[0],))
        self.db_connection.commit()

    def delete_task(self, task_id):
        query = '''DELETE FROM tasks WHERE id_task = ?'''
        self.cursor.execute(query, (task_id[0],))
        self.db_connection.commit()

    def delete_profile(self, profile_id):
        query = '''DELETE FROM profiles WHERE id = ?'''
        self.cursor.execute(query, (profile_id,))
        self.db_connection.commit()
        data = self.get_list_ids(profile_id)
        for elem in data:
            self.delete_list(elem)

    def complete_task(self, task_id):
        query = '''UPDATE tasks SET complete = True WHERE id_task = ?'''
        self.cursor.execute(query, (task_id[0],))
        self.db_connection.commit()

    def export_file(self):
        query_profile = '''SELECT * FROM profiles WHERE id = ?'''
        query_lists = '''SELECT * FROM lists WHERE id_profile = ?'''
        query_tasks = '''SELECT * FROM tasks WHERE id_list IN (?)'''
        data = list()
        for i in range(len())

    def close_connection(self):
        self.db_connection.close()
