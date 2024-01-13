import sqlite3


class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_db()

    def create_db(self):
        try:
            query = ("CREATE TABLE IF NOT EXISTS users("
                     "id INTEGER PRIMARY KEY,"
                     "user_name TEXT,"
                     "user_lat REAL,"
                     "user_lon REAL,"
                     "telegram_id TEXT);")
            self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as Error:
            print("Error while creating:", Error)

    def add_user(self, user_name, user_lat, user_lon, telegram_id):
        self.cursor.execute(f"INSERT INTO users (user_name,user_lat,user_lon,telegram_id) VALUES (?,?,?,?)",
                            (user_name, user_lat, user_lon, telegram_id))
        self.connection.commit()

    def select_user_id(self, telegram_id):
        users = self.cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        return users.fetchone()

    def select_user_lat(self, telegram_id):
        users = self.cursor.execute("SELECT user_lat FROM users WHERE telegram_id = ?", (telegram_id,))
        return users.fetchone()

    def select_user_lon(self, telegram_id):
        users = self.cursor.execute("SELECT user_lon FROM users WHERE telegram_id = ?", (telegram_id,))
        return users.fetchone()

    def update_user_location(self, user_id, new_lat, new_lon):
        try:
            self.cursor.execute("UPDATE users SET user_lat = ?, user_lon = ? WHERE id = ?",
                                (new_lat, new_lon, user_id))
            self.connection.commit()
            print(f"User ID {user_id} location updated successfully.")
        except sqlite3.Error as error:
            print("Error updating user location:", error)

    def __del(self):
        self.cursor.close()
        self.connection.close()
