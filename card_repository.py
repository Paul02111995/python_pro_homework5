import sqlite3
import uuid

from card import Card

class CardRepository:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_file)

    def close(self):
        if self.connection:
            self.connection.close()

    def create_table(self):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cards (
                pan TEXT NOT NULL,
                expiry_date TEXT NOT NULL,
                cvv TEXT NOT NULL,
                issue_date TEXT NOT NULL,
                owner_id TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        self.connection.commit()
        self.close()

    def save_card(self, card):
        self.connect()
        cursor = self.connection.cursor()

        cursor.execute(
            '''
            INSERT OR REPLACE INTO cards (pan, expiry_date, cvv, issue_date, owner_id, status)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (card.pan, card.expiry_date, card.cvv, card.issue_date, card.owner_id, card.status)
        )

        self.connection.commit()
        self.close()

    def get_card_by_pan(self, pan):
        self.connect()
        cursor = self.connection.cursor()

        cursor.execute('SELECT * FROM cards WHERE pan = ?', (pan,))
        result = cursor.fetchone()

        self.close()

        if result:
            pan, expiry_date, cvv, issue_date, owner_id, status = result
            return Card(pan, expiry_date, cvv, issue_date, owner_id, status)

        return None
