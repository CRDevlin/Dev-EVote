import json

def handle_uploaded_file(fileName, f):
    try:
        with open(fileName, 'wb+') as destination:
            if f.multiple_chunks():
                for chunk in f.chunks():
                    destination.write(chunk)
            else:
                destination.write(f.read())
    except:
        return False
    return True
