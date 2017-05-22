import json


class Election():
    def __init__(self, voters_file, nominees_file, final_vote_date):
        try:
            voters = json.load(open(voters_file))
            nominees = json.load(open(nominees_file))
        except ValueError as e:
            raise e

        self.voters = voters
        self.nominees = nominees
        self.token = '' #TODO: Unique Election token
        self.anonymous_voting = False
        self.multi_vote = False
        self.final_vote_date = final_vote_date

    

if __name__ == '__main__':
    election = Election
    print(election)
