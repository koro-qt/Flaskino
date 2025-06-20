from flask_login import UserMixin
from auth.db import get_db_connection

class User(UserMixin):
    def __init__(self, id_, username, password_hash, email, role='user', balance=1000):
        self.id = id_
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.role = role
        self.balance = balance

    def update_balance(self, new_balance):
        self.balance = new_balance
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET balance = ? WHERE id = ?", (self.balance, self.id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        conn.close()
        return User(*row) if row else None

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        conn.close()
        return User(*row) if row else None

    @staticmethod
    def create(username, password_hash, email, role='user'):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                (username, password_hash, email, role)
            )
            conn.commit()
        except Exception as e:
            return False
        finally:
            conn.close()
        return True

    def update_profile(self, new_email):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, self.id))
        conn.commit()
        conn.close()

    def delete_account(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()
