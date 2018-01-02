"""
validation.py
Validates the integrity of the data being sent from a client.
"""

import re
import json
from website.settings import CONFIG

weight_key = 'WEIGHT'
name = re.compile('[a-z]+', re.IGNORECASE)
email = re.compile('[a-z0-9.]+@csuci.edu', re.IGNORECASE)


def validate_content(file):
    """
    Validate capacity range of the contents of the file, Throws an error if failure
    :param file: Loaded file
    """
    email_len = CONFIG['MAX_EMAIL_LEN']
    name_len = CONFIG['MAX_NAME_LEN']
    for i, entity in enumerate(file):
        # First Name
        if len(entity['FIRST_NAME']) > name_len:
            raise AssertionError('First name is greater than the maximum allowed length {}. Object #{}'
                                 .format(name_len, i))
        if name.match(entity['FIRST_NAME']) is None:
            raise AssertionError('Invalid first name, special characters are not allowed. Object #{}'.format(i))
        # Last Name
        if len(entity['LAST_NAME']) > name_len:
            raise AssertionError('Last name is greater than the maximum allowed length {}. Object #{}'
                                 .format(name_len, i))
        if name.match(entity['LAST_NAME']) is None:
            raise AssertionError('Invalid last name, special characters are not allowed. Object #{}'.format(i))
        # Email
        if len(entity['EMAIL']) > email_len:
            raise AssertionError('Email is greater than the maximum allowed length {}. Object #{}'
                                 .format(email_len, i))
        if name.match(entity['EMAIL']) is None:
            raise AssertionError('Email address must be in the domain \'@csuci.edu\'. Object #{}'.format(i))


def validate_json(file, json_type):
    """
    Validate voter or nominee json file, Throws an error if failure
    :param file: Loaded file
    :param json_type: 'voter' if voter json file, 'nominee' if nominee json file
    """
    if not isinstance(file, list):
        raise AssertionError("{} json file must be start with a list".format(json_type))
    if len(file) == 0:
        raise AssertionError("{} json file must contain at least one entry")
    for i, entity in enumerate(file):
        if not isinstance(entity, dict):
            raise AssertionError("json must contain dictionaries. Object #".format(i))
    if json_type == 'voter':
        validate_voter_json(file)
    elif json_type == 'nominee':
        validate_faculty_json(file)
    else:
        raise ValueError("Invalid value for \'type\'.")

    validate_content(file)


def validate_voter_json(file):
    """
    Validate voter json weights, Throws an error if failure
    :param file: Loaded voter file
    """
    global weight_key

    sigma = 0.0
    validate_faculty_json(file)

    for i, voter in enumerate(file):
        if weight_key not in voter:
            raise AssertionError("Required key \'{}\' is missing from this json. Object #{}".format(weight_key, i))
        if not isinstance(voter[weight_key], float):
            raise AssertionError("Value in key \'{}\' needs to be a valid float. Object #{}".format(weight_key, i))
        if 1.0 < voter[weight_key] <= 0.0:
            raise AssertionError(
                "Invalid value in key \'{}\' Acceptable interval: (0,1]. Object #{}".format(weight_key, i))
        sigma += voter[weight_key]

    if sigma != 1.0:
        raise AssertionError("Invalid total weight. The sum of all the weights must equal 1.0")


def validate_faculty_json(file):
    """
    Validate faculty contents, Throws an error if failure
    :param file: Loaded voter file
    """

    for i, person in enumerate(file):
        for key in CONFIG['FACULTY_KEYS']:
            if key not in person:
                raise AssertionError("Required key \'{}\' is missing from this json. Object #{}".format(key, i))
            if not isinstance(person[key], str):
                raise AssertionError("Value in key \'{}\' needs to be a valid string. Object #{}".format(key, i))
            if person[key].isspace() or person[key] == '':
                raise AssertionError("Value in key \'{}\' cannot be empty. Object #{}".format(key, i))


if __name__ == '__main__':
    import json

    voter_file = json.load(open('../uploaded/voter.json'))
    nominee_file = json.load(open('../uploaded/nominee.json'))
    validate_json(voter_file, 'voter')
    validate_json(nominee_file, 'nominee')
