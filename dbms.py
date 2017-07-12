import uuid
import json
import sqlite3
import re

class DBMS:
    def __init__(self):
        # try:
        settings = json.load(open('data/settings.json'))
        self.conn = sqlite3.connect(    settings['DATABASE'])
        self.cursor = self.conn.cursor()
        self.email_len = settings['MAX_EMAIL_LEN']
        self.name_len = settings['MAX_NAME_LEN']
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS election
                            (
                            election_id INTEGER PRIMARY KEY,
                            anonymous_voting_bool INTEGER,
                            multi_voting_bool INTEGER,
                            final_vote_epoch INTEGER
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
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS faculty
                            (
                            faculty_id INTEGER PRIMARY KEY,
                            faculty_last_name_txt TEXT,
                            faculty_first_name_txt TEXT,
                            faculty_email_txt TEXT
                            )
                            ''')

    def read_election(self, election_id):
        self.cursor.execute('''
                            SELECT * FROM election WHERE election_ID = (?)
                            ''', (election_id, ))
        result = self.cursor.fetchone()
        return result

        self.voters = voters
        self.nominees = nominees
        self.anonymous_voting = False
        self.multi_vote = False
        self.final_vote_date = final_vote_date

    def write_election(self, election):
        voters = election.voters
        nominees = election.nominees
        anonymous = election.anonymous_voting
        multi = election.multi_vote
        final_date = election.final_vote_date.timestamp()
        self.cursor.execute('''
                            INSERT INTO election VALUES (?, ?, ?)
                            ''', (anonymous, multi, final_date))
        self.cursor.execute('''
                            SELECT last_insert_rowid();
                            ''')
        election_id = self.cursor.fetchone()

    def write_voters(self):
        return 0

    def write_nominees(self):
        return 0

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

    def write_faculty(self, faculty):
        first_name = faculty.first_name
        last_name = faculty.last_name
        email = faculty.email

        self.validate_input(faculty, 'faculty')

        self.cursor.execute('''
                            SELECT * WHERE faculty_email_txt = (?)
                            ''', (email,))
        existing_email = self.cursor.fetchone()
        if existing_email is None:
            self.cursor.execute('''
                                INSERT INTO faculty NAME (?, ?, ?)
                                ''', (last_name, first_name, email))
            self.cursor.execute('''
                                SELECT last_insert_rowid();
                                ''')
            return self.cursor.fetchone()
        else:
            return 0

    def edit_election(self):
        raise NotImplementedError

    def save(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    db = DBMS()

