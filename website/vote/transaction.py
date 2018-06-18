"""
Wrapper for queries, performs validation
"""

import json
from .validation import validate_json, validate_content
import vote.queries as db


def create_election(voter_path, nominee_path, anon, multi_vote, date, time):
    """
    Create an election. Validates data integrity before inserting.
    :param voter_path: Path to voter json
    :param nominee_path: Path to nominee json
    :param anon: Anonymous voting - the ballot will not be reported
    :param multi_vote: Multiple voting - A voter may change their vote in the future
    :param date: The deadline that a user may vote
    :param time: The deadline that a user may vote
    :return: Newly created election token
    """

    voters = json.load(open(voter_path))
    nominees = json.load(open(nominee_path))
    validate_json(voters,'voter')
    validate_json(nominees, 'nominee')
    validate_content(voters)
    validate_content(nominees)
    voters, weights = db.insert_faculty(voters, True)
    faculty, _ = db.insert_faculty(nominees, False)
    election = db.insert_election(anon,
                                  multi_vote,
                                  date,
                                  time)
    db.insert_nominee(faculty, election)
    records = db.insert_record(voters, weights, election)
    return election.token, records


def validate_voter_token(voter_token):
    """
    Validate a voter token, raises an error with a message if invalid
    :param voter_token: Voter Token
    """
    db.validate_voter_token(voter_token)


def validate_election_token(election_token):
    """
    Validate an Election token, raises an error with a message if invalid
    :param election_token: Election Token
    """
    db.validate_election_token(election_token)


def get_nominee_choices(voter_token):
    """
    Get nominee choices given a token
    :param voter_token: Voter Token
    :return: List of tuples containing nominee choices
    """
    choices = []
    nominees = db.get_nominees(voter_token)
    for i, nominee in enumerate(nominees):
        faculty = nominee.faculty
        full_name = faculty.first_name + " " + faculty.last_name
        choices.append((str(i), full_name))
    return choices


def set_nominee_choice(voter_token, choice):
    """
    Associate a nominee with a voter's choice
    :param voter_token: Voter token
    :param choice: index of choice
    """
    nominees = db.get_nominees(voter_token)
    db.set_nominee_choice(voter_token, nominees[int(choice)])


def get_election_results(election_token):
    """
    Get election results given an election token
    :param election_token: Election token
    :return: Dictionary containing:
             The a list of voter ballots (Who voted for who)
             List of aggregated weights of each nominee
             The winner of the election with the highest percentage score
    """
    return db.get_election_results(election_token)


def get_voter_tokens(election_token):
    """
    Get a list of voter tokens given an election token
    :param election_token:
    :return:
    """
    return db.get_voter_tokens(election_token)