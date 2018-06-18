"""
queries.py
This layer interfaces directly with the database, performing commands and queries
"""

import random
from datetime import datetime as dt
from .models import *
from website.settings import CONFIG
from django.db.models import Sum

random = random.SystemRandom()  # Django uses this to create secret keys
alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def get_nominees(voter_token):
    """
    Gets a list of election nominees given a voter token.
    :param voter_token: Voter token
    :return: Returns a list of Nominee model objects
    """
    try:
        r = Record.objects.get(token=voter_token)  # Get a single record
        e = r.election
        n = Nominee.objects.filter(election=e)  # Get multiple model objects
        return list(n)
    except Record.DoesNotExist:
        raise ValueError("Invalid token")
    except Election.DoesNotExist:
        raise ValueError("Invalid Election")
    except Nominee.DoesNotExist:
        raise LookupError("No Nominees found")


def get_election_results(election_token):
    """
    Get election results given election token (Administrator function)
    :param election_token: Election token
    :return: Dictionary containing:
             The a list of voter ballots (Who voted for who)
             List of aggregated weights of each nominee
             The winner of the election with the highest percentage score
    """
    res = {'BALLOT': None,
           'RESULT':  [],
           'WINNER':  []}

    e = Election.objects.get(token=election_token)
    r = Record.objects.filter(election=e)  # Get all records from a specific election
    if not e.anon_voting:
        res['BALLOT'] = []
        for record in list(r):
            v = record.voter  # Voter
            if record.choice is not None:
                # Voter choice
                n = record.choice.faculty
                ballot = (v.first_name + ' ' + v.last_name, n.first_name + ' ' + n.last_name)
                res['BALLOT'].append(ballot)

    # Aggregate based on field Record.choice, add all the weights
    # Creates a dictionary for each nomineee [{'choice': Nominee1, 'total_weight': Val1}, ...]
    R = r.values('choice').annotate(total_weight=Sum('weight'))

    for record in R:
        # Get nominee first/last
        if record['choice'] is not None:
            f = Nominee.objects.get(id=record['choice']).faculty
            f_name = f.first_name + ' ' + f.last_name
            # Convert the weight into a percentage
            percent = record['total_weight'] * 100
            score = (f_name, percent)

            # Calculate the winner (With the highest score)
            if len(res['WINNER']) == 0:
                res['WINNER'].append(score)
            else:
                if res['WINNER'][0][1] < percent:  # This nominee has a higher score, replace it
                    res['WINNER'].clear()
                    res['WINNER'].append(score)
                elif res['WINNER'][0][1] == percent:  # In the event of a tie
                    res['WINNER'].append(score)

            res['RESULT'].append(score)
    return res


def insert_nominee(ref_nominees, ref_election):
    """
    Insert a new Nominee
    :param ref_nominees: List of Faculty model objects
    :param ref_election: Election model object
    :return: List of newly inserted Nominee model objects
    """
    res = []
    for nominee in ref_nominees:
        n = Nominee()
        n.faculty = nominee
        n.election = ref_election
        n.faculty_id = nominee.id
        n.election_id = ref_election.id
        n.save()
        res.append(n)
    return res


def insert_record(ref_voters, ref_weights, ref_election):
    """
    Insert new records for every voter
    :param ref_voters: List of Faculty model objects
    :param ref_weights: List of the voters weights
    :param ref_election: Election model object
    :return: List of newly inserted Record model objects
    """
    res = []
    i = 0

    while i < len(ref_voters):
        token = ''.join(random.choice(alphabet) for _ in range(CONFIG['VOTE_TOKEN_LEN']))
        r = Record(token=token, weight=ref_weights[i])
        r.voter = ref_voters[i]
        r.election = ref_election

        # For debugging purposes
        print(ref_voters[i].first_name, ref_voters[i].last_name, token, ref_weights[i])

        r.save()
        res.append(r)
        i += 1
    return res


def insert_election(anon, multi, date, time):
    """
    Insert a new election
    :param anon: Anonymous voting - the ballot will not be reported
    :param multi: Multiple voting - A voter may change their vote in the future
    :param date: The deadline that a user may vote
    :param time: The deadline that a user may vote
    :return: A new Election model object
    """
    token = ''.join(random.choice(alphabet) for _ in range(CONFIG['ELEC_TOKEN_LEN']))
    e = Election(anon_voting=anon, multi_voting=multi, final_vote=dt.combine(date, time), token=token)
    e.save()
    return e


def insert_faculty(faculty, is_voter):
    """
    Insert new faculty into the database and gets a list of Faculty model objects.
    :param faculty: Dictionary containing the information of each faculty
    :param is_voter: if true, records the weights associated to each faculty
    :return: list of Faculty model objects based on dictionary input
    """
    res = []
    weight = []
    for entity in faculty:
        try:
            f = Faculty.objects.get(email=entity['EMAIL'])
        except Faculty.DoesNotExist as dne:
            f = Faculty(last_name=entity['LAST_NAME'], first_name=entity['FIRST_NAME'], email=entity['EMAIL'])
        f.save()
        res.append(f)
        if is_voter:
            weight.append(entity['WEIGHT'])
    return res, weight


# TODO: Need to properly compare a django Datetime with python datetime.
# TODO: We also need to consider UTC to PST conversion
def validate_voter_token(voter_token):
    """
    Validate a voter token, raises an error with a message if invalid
    :param voter_token: Voter token
    """
    try:
        r = Record.objects.get(token=voter_token)
        e = r.election
        if r.choice is not None:
            if not e.multi_voting:
                raise ValueError('You already voted')
        # if e.final_vote > dt.now():
        #    raise ValueError("This election expired.")
    except Record.DoesNotExist:
        raise ValueError("Invalid token")


def validate_election_token(election_token):
    """
    Validate a election token, raises an error with a message if invalid
    :param election_token: Election Token
    """
    try:
        Election.objects.get(token=election_token)
    except Election.DoesNotExist:
        raise ValueError("Invalid token")


def set_nominee_choice(voter_token, ref_nominee):
    """
    Associate a nominee with a voter's choice
    :param voter_token: Voter token
    :param ref_nominee: Nominee model object
    """
    try:
        r = Record.objects.get(token=voter_token)
        r.choice = ref_nominee
        r.save()
    except Record.DoesNotExist:
        raise ValueError('Invalid token')


def get_voter_tokens(election_token):
    """
    Query voter tokens given election token
    :param election_token:
    :return:
    """
    res = []

    e = Election.objects.get(token=election_token)
    r = Record.objects.filter(election=e)  # Get all records from a specific election

    for record in list(r):
        # Voter
        v = record.voter
        voter_info = {'NAME': v.first_name + ' ' + v.last_name,
                      'EMAIL': v.email,
                      'TOKEN': record.token}
        res.append(voter_info)
    return res
