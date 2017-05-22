import json
import sqlite3


class DBMS:
    def __init__(self):
        try:
            settings = json.load(open('settings.json'))
            conn = sqlite3.connect(settings['DATABASE'])
            self.cursor = conn.cursor()
        except:
            raise NotImplementedError

    def read_election(self, option, value):
        raise NotImplementedError

    def write_election(self, election):
        raise NotImplementedError



if __name__ == '__main__':
    db = DBMS()
