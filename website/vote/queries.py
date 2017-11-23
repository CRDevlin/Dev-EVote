import random
from datetime import datetime as dt
from .models import *


random = random.SystemRandom()  # Django uses this to create secret keys
alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
token_len = 32


def insert_nominee(ref_nominees, ref_election):
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
    global token_len
    res = []
    i = 0

    while i < len(ref_voters):
        token = ''.join(random.choice(alphabet) for _ in range(token_len))
        r = Record(token=token, weight=ref_weights[i])
        r.voter = ref_voters[i]
        r.election = ref_election

        print(ref_voters[i].first_name, ref_voters[i].last_name, token, ref_weights[i])

        r.save()
        res.append(r)
        i += 1
    return res


def insert_election(anon, multi, date, time):
    e = Election(anon_voting=anon, multi_voting=multi, final_vote=dt.combine(date, time))
    e.save()
    return e


def insert_faculty(faculty, is_voter):
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


def check_valid_token(token):
    try:
        Record.objects.get(token=token)
        # if e.final_vote > dt.now():
        #    raise ValueError("This election expired.")
    except Record.DoesNotExist:
        raise ValueError("Invalid token")


def get_nominees(token):
    try:
        r = Record.objects.get(token=token)  # Get a single record
        e = r.election
        # if e.final_vote > dt.now():
        #    raise ValueError("This election expired.")
        n = Nominee.objects.filter(election=e)  # Get multiple model objects
        return list(n)
    except Record.DoesNotExist:
        raise ValueError("Invalid token")
    except Election.DoesNotExist:
        raise ValueError("Invalid Election")
    except Nominee.DoesNotExist:
        raise LookupError("No Nominees found")


def set_nominee(token, ref_nominee):
    try:
        r = Record.objects.get(token=token)
        r.choice = ref_nominee
        r.save()
    except Record.DoesNotExist:
        raise ValueError("Invalid token")
