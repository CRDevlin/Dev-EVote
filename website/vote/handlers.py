# from .models import Election, Faculty, Record, Nominee


def handle_uploaded_file(file_name, f):
    with open(file_name, 'wb+') as destination:
        if f.multiple_chunks():
            for chunk in f.chunks():
                destination.write(chunk)
        else:
            destination.write(f.read())
