def handle_uploaded_file(file_name, f):
    """
    Copy file uploaded from a client to destination folder
    :param file_name: Destination file path
    :param f: Source file (Should be cleaned data)
    """
    with open(file_name, 'wb+') as destination:
        if f.multiple_chunks():
            for chunk in f.chunks():
                destination.write(chunk)
        else:
            destination.write(f.read())
