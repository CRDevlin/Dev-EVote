

#12 length token

class Election():
    def __init__(self, voters, nominees, final_vote_date, token_length):
        self.voters = voters
        self.nominees = nominees
        self.anonymous_voting = False
        self.multi_vote = False
        self.final_vote_date = final_vote_date
        self.token = ''.join(random.choice(alphabet) for _ in range(token_length))
        return


if __name__ == '__main__':
    import json
    import time
    from dbms import DBMS

    db = DBMS()
    settings = json.load(open('./data/settings.json', 'r'))
    voters = json.load(open('./data/sample_voters.json', 'r'))  # Obtained from file upload
    nominees = json.load(open('./data/sample_nominees.json', 'r'))  # Obtained from file upload
    vote_date = int(time.time()) + 10000 # Obtained from webpage input

    election = Election(voters, nominees, vote_date, settings['TOKEN_LEN'])
    db.write_election(election)
    db.save()
    db.close()
