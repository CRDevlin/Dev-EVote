import random
from datetime import datetime as dt
from .models import *


random = random.SystemRandom() # Django uses this to create secret keys
alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
token_len = 32


def insert_nominee(ref_nominees, ref_election):
    res = []
    for nominee in ref_nominees:
        n = Nominee()
        n.faculty = nominee
        n.election = ref_election
        n.save()
        res.append(n)
    return res


def insert_record(ref_voters, ref_election):
    global token_len
    res = []

    for voter in ref_voters:
        token = ''.join(random.choice(alphabet) for _ in range(token_len))
        r = Record(token=token, weight=voter['WEIGHT'])
        r.voter = voter
        r.election = ref_election
        r.save()
        res.append(r)
    return res


def insert_election(anon, multi, date, time):
    e = Election(anon_voting=anon, multi_voting=multi, final_vote=dt.combine(date, time))
    e.save()
    return e


def insert_faculty(faculty):
    res = []
    for entity in faculty:
        try:
            f = Faculty.objects.get(email=entity['EMAIL'])
            res.append(f)
        except Faculty.DoesNotExist as dne:
            f = Faculty(last_name=entity['LAST_NAME'], first_name=entity['FIRST_NAME'], email=entity['EMAIL'])
            f.save()
            res.append(f)
    return res


def get_nominees(token):
    try:
        e = Election.objects.get(token=token)
        n = Nominee.objects.filter(election=e)
        return list(n)
    except Election.DoesNotExist:
        raise ValueError("Invalid token or election no longer exists")
    except Nominee.DoesNotExist:
        raise LookupError("No Nominees found")


def set_nominee(token, nominee):
    try:
        e = Election.objects.get(token=token)
        r = Record.objects.filter(election=e)
        r.nominee = nominee
        r.save()
    except Election.DoesNotExist:
        raise ValueError("Invalid token or the election no longer exists")

