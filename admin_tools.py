import json
import csv

from exceptions import *
from election import Election


def read_file(file):
    """
    Open file containing election information
    :param file: *.csv, .json, or .xml (not implemented)
    :return: python dictionary with contents of the file
    """
    if file.endswith('.json'):
        with open(file, 'r') as json_file:
            contents = json.load(json_file)
    elif file.endswith('.csv'):
        with open(file, 'r') as csv_file:
            contents = []
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader:
                data = {'LAST_NAME': row[0],
                        'FIRST_NAME': row[1]}
                if row == 4: # Sample Voters File
                    data['EMAIL'] = row[2]
                    data['WEIGHT'] = float(row[3])
                contents.append(data)
    elif file.endswith('.xml'):
        raise NotImplementedError("\'.xml\' files are not be read")
    else:
        raise InvalidFileError("\'{}\' is an invalid path".format(file))

    return contents


def create_election(voters_file, nominees_file):
    try:
        voters = read_file(voters_file)
        nominees = read_file(nominees_file)
        election = Election(voters, nominees, None)
    except ValueError as e:
        print("Error, invalid file path provided!")
    except FileNotFoundError as e:
        print(e)
    except InvalidFileError:
        print("Error, invalid file provided!")
    except IndexError:
        print("Error, list index out of range")


def follow_existing_election(election_token):
    raise NotImplementedError

if __name__ == '__main__':
    file_content = read_file('data\sample_nominees.json')
    print(file_content)
