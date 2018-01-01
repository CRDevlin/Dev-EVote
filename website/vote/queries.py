import random
from datetime import datetime as dt
from .models import *
from website.settings import CONFIG
from django.db.models import Sum


random = random.SystemRandom()  # Django uses this to create secret keys
alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


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
    res = []
    i = 0

    while i < len(ref_voters):
        token = ''.join(random.choice(alphabet) for _ in range(CONFIG['VOTE_TOKEN_LEN']))
        r = Record(token=token, weight=ref_weights[i])
        r.voter = ref_voters[i]
        r.election = ref_election

        print(ref_voters[i].first_name, ref_voters[i].last_name, token, ref_weights[i])

        r.save()
        res.append(r)
        i += 1
    return res


def insert_election(anon, multi, date, time):
    token = ''.join(random.choice(alphabet) for _ in range(CONFIG['ELEC_TOKEN_LEN']))
    e = Election(anon_voting=anon, multi_voting=multi, final_vote=dt.combine(date, time), token=token)
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


def get_results(token):
    """
    Get election results
    :param token: Election token
    :return:
    """
    res = {}
    e = Election.objects.get(token=token)
    r = Record.objects.filter(election=e)
    if not e.anon_voting:
        res['BALLOTS'] = []
        for record in list(r):
            v = record.voter
            n = record.choice.faculty
            res['BALLOTS'].append((v.first_name + ' ' + v.last_name, n.first_name + ' ' + n.last_name))

    res['RESULT'] = []
    R = r.values('choice').annotate(total_weight=Sum('weight'))
    for record in R:
        f = Nominee.objects.get(id=record['choice']).faculty
        percent = record['total_weight'] * 100
        res['RESULT'].append((f.first_name + ' ' + f.last_name, percent))

    return res
