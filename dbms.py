import json
import sqlite3
import re
import time
import random
random = random.SystemRandom() # Django uses this to create secret keys
alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


class DBMS:
    def __init__(self):
        # try:
        settings = json.load(open('data/settings.json'))
        self.conn = sqlite3.connect(settings['DATABASE'])
        self.cursor = self.conn.cursor()
        self.token_len = settings['TOKEN_LEN']
        self.email_len = settings['MAX_EMAIL_LEN']
        self.name_len = settings['MAX_NAME_LEN']
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS election
                            (
                            election_id INTEGER PRIMARY KEY ASC,
                            election_token_txt TEXT
                            anon_voting_bool INTEGER,
                            multi_voting_bool INTEGER,
                            final_vote_epoch INTEGER,
                            )
                            ''')
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS faculty
                            (
                            faculty_id INTEGER PRIMARY KEY,
                            faculty_last_name_txt TEXT,
                            faculty_first_name_txt TEXT,
                            faculty_email_txt TEXT
                            )
                            ''')
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS voters (
                            election_id UNSIGNED INTEGER,
                            faculty_id UNSIGNED INTEGER,
                            token_txt TEXT,
                            weight_amt REAL
                            )
                            ''')
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS nominees (
                            election_id UNSIGNED INTEGER,
                            faculty_id UNSIGNED INTEGER
                            )
                            ''')

    def read_election(self, election_id):
        self.cursor.execute('''
                            SELECT * FROM election WHERE election_ID = (?)
                            ''', (election_id, ))
        result = self.cursor.fetchmany(10)
        return result

    def write_election(self, e):
        self.validate_input(e, 'election')

        self.cursor.execute('''
                            INSERT INTO election(election_token, anon_voting_bool, multi_voting_bool, final_vote_epoch)
                            VALUES (?, ?, ?, ?)
                            ''', (e.token, e.anonymous_voting, e.multi_vote, e.final_vote_date))

        self.cursor.execute('''
                            SELECT last_insert_rowid();
                            ''')
        election_id = self.cursor.fetchone()[0]
        for voter in e.voters:
            faculty_id = self.write_faculty(voter)
            token = ''.join(random.choice(alphabet) for _ in range(self.token_len))
            weight = voter['WEIGHT']
            self.cursor.execute('''
                                INSERT INTO voters VALUES (?, ?, ?, ?)
                                ''', (election_id, faculty_id, token, weight))

        for nominee in e.nominees:
            faculty_id = self.write_faculty(nominee)
            self.cursor.execute('''
                                INSERT INTO nominees VALUES (?, ?)
                                ''', (election_id, faculty_id))

    def validate_input(self, struct, struct_type):
        name = re.compile('[a-z]+', re.IGNORECASE)
        email = re.compile('[a-z0-9.]@csuci.edu', re.IGNORECASE)

        if struct_type is 'faculty':
            if len(struct.first_name) > self.name_len:
                raise ValueError('First name \'{}\' is greater than the maximum allowed length {}'.format(
                                 struct.first_name, self.name_len))
            if len(struct.last_name) > self.name_len:
                raise ValueError('Last name \'{}\' is greater than the maximum allowed length {}'.format(
                                 struct.last_name, self.name_len))
            if len(struct.email) > self.email_len:
                raise ValueError('Email \'{}\' is greater than the maximum allowed length {}'.format(
                                 struct.email, self.email_len))
            if name.match(struct.first_name) is None:
                raise ValueError('{} is not a valid first name'.format(struct.first_name))
            if name.match(struct.last_name) is None:
                raise ValueError('{} is not a valid last name'.format(struct.last_name))
            if name.match(struct.email) is None:
                raise ValueError('{} is not a valid email address (must be \'@csuci.edu\')'.format(struct.email))

    def write_faculty(self, f):

        self.cursor.execute('''
                            SELECT faculty_id FROM faculty WHERE faculty_email_txt = (?)
                            ''', (f['EMAIL'],))
        existing_email = self.cursor.fetchone()
        if existing_email is None:
            self.cursor.execute('''
                                INSERT INTO faculty (faculty_last_name_txt, faculty_first_name_txt, faculty_email_txt)
                                VALUES (?, ?, ?)
                                ''', (f['LAST_NAME'], f['FIRST_NAME'], f['EMAIL']))
            self.cursor.execute('''
                                SELECT last_insert_rowid();
                                ''')
            return self.cursor.fetchone()[0]
        else:
            return -1

    def edit_election(self):
        raise NotImplementedError

    def lookup_token(self, token):
        self.cursor.execute('''
                            SELECT (election_id, faculty_id) FROM voters WHERE token_txt = (?)
                            ''', (token,))

    def get_active_elections(self):
        epoch = int(time.time())
        self.cursor.execute('''
                            SELECT * FROM election WHERE final_vote_epoch > (?)
                            ''', (epoch,))
        self.cursor.fetchall()

    def get_expired_elections(self, n):
        epoch = int(time.time())
        self.cursor.execute('''
                            SELECT * FROM election WHERE final_vote_epoch <= (?)
                            ''', (epoch,))

    def save(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    db = DBMS()

