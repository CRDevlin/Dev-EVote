import json


class Election():
    def __init__(self, voters, nominees, final_vote_date):
        self.voters = voters
        self.nominees = nominees
        self.token = '' #TODO: Unique Election token
        self.anonymous_voting = False
        self.multi_vote = False
        self.final_vote_date = final_vote_date

    

if __name__ == '__main__':
    election = Election
    print(election)
