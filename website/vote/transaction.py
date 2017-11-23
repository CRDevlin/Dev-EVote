import json
from .validation import validate_json, validate_content
from .queries import *


def create_election(voter_path, nominee_path, anon, multi_vote, date, time):
    voters = json.load(open(voter_path))
    nominees = json.load(open(nominee_path))
    validate_json(voters,'voter')
    validate_json(nominees, 'nominee')
    validate_content(voters)
    validate_content(nominees)
    voters, weights = insert_faculty(voters, True)
    faculty, _ = insert_faculty(nominees, False)
    election = insert_election(anon,
                               multi_vote,
                               date,
                               time)
    insert_nominee(faculty, election)
    insert_record(voters, weights, election)


def validate_token(request, token):
    check_valid_token(token)
    request.session['valid_token'] = token


def find_nominees(token):
    return get_nominees(token)
