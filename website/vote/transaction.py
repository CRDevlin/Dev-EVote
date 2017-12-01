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
    return election.token


def validate_token(request, token):
    check_valid_token(token)
    request.session['valid_token'] = token


def get_nominee_choices(token):
    choices = []
    nominees = get_nominees(token)
    for i, nominee in enumerate(nominees):
        faculty = nominee.faculty
        full_name = faculty.first_name + " " + faculty.last_name
        choices.append((str(i), full_name))
    return choices


def set_nominee_choice(token, choice):
    nominees = get_nominees(token)
    set_nominee(token, nominees[int(choice)])
