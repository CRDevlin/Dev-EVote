import os


def handle_uploaded_file(file_path, file_name, f):
    """
    Copy file uploaded from a client to destination folder
    :param file_path: Destination file path
    :param f: Source file (Should be cleaned data)
    """
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(file_path + '/' + file_name, 'wb+') as destination:
        if f.multiple_chunks():
            for chunk in f.chunks():
                destination.write(chunk)
        else:
            destination.write(f.read())
