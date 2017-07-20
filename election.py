import random
random = random.SystemRandom() # Django uses this to create secret keys
alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

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
    election = Election
    print(election)
