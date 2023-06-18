import unittest
import sqlite3
import os

from card import Card
from card_repository import CardRepository

class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.db_file = "test.db"
        self.card_repo = CardRepository(self.db_file)
        self.card = Card("1234567812345678", "12/25", "123", "01/22", "00112233-4455-6677-8899-aabbccddeeff", "new")
        self.card_repo.create_table()

    def tearDown(self):
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_save_card(self):
        self.card_repo.save_card(self.card)

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cards WHERE pan = ?', (self.card.pan,))
        result = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], self.card.pan)
        self.assertEqual(result[1], self.card.expiry_date)
        self.assertEqual(result[2], self.card.cvv)
        self.assertEqual(result[3], self.card.issue_date)
        self.assertEqual(result[4], self.card.owner_id)
        self.assertEqual(result[5], self.card.status)

    def test_get_card_by_pan(self):
        self.card_repo.save_card(self.card)

        result = self.card_repo.get_card_by_pan(self.card.pan)

        self.assertEqual(result.pan, self.card.pan)
        self.assertEqual(result.expiry_date, self.card.expiry_date)
        self.assertEqual(result.cvv, self.card.cvv)
        self.assertEqual(result.issue_date, self.card.issue_date)
        self.assertEqual(result.owner_id, self.card.owner_id)
        self.assertEqual(result.status, self.card.status)

    def test_get_nonexistent_card(self):
        result = self.card_repo.get_card_by_pan("9999999999999999")
        self.assertIsNone(result)



    def test_update_card_status(self):
        self.card_repo.save_card(self.card)

        card = self.card_repo.get_card_by_pan(self.card.pan)
        self.assertEqual(card.status, "new")

        card.activate()
        self.card_repo.save_card(card)
        self.assertEqual(card.status, "active")

        card.block()
        self.card_repo.save_card(card)
        self.assertEqual(card.status, "blocked")

    def test_activate_already_activated_card(self):
        self.card.status = "active" or "blocked"
        with self.assertRaises(Exception):
            self.card.activate()


    def test_activate_blocked_card(self):
        self.card.status = "blocked"

        with self.assertRaises(Exception):
            self.card.activate()

    def test_block_already_blocked_card(self):
        self.card.status = "new"
        with self.assertRaises(Exception):
            self.card.block()

if __name__ == '__main__':
    unittest.main()
