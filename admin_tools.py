from election import Election


def create_election(voters_file, nominees_file, filetype='json'):
    try:
        if filetype is 'json':
            election = Election(voters_file, nominees_file)
        elif filetype is 'csv':
            raise NotImplementedError
        elif filetype is 'xml':
            raise NotImplementedError
    except ValueError as e:
        print("Error, invalid file path provided!")


def follow_existing_election(election_token):
    raise NotImplementedError
