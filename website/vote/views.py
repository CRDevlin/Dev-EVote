from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hi")


def vote(request):
    return HttpResponse('''
                        <!doctype html>
                        <html>
                        <head>
                            <title>CSUCI E-Vote</title>
                        </head>
                        <body>
                        <p><strong><span style="font-family:arial,helvetica,sans-serif;">Enter your token</span></strong></p>
                        <form method="post" name="submit_token" action="/submit_token.php">
                        <p><input maxlength="32" size="32" name="token_textbox" type="password" value="" /></p>
                        </form>
                        <p><input name="submit_button" type="submit" value="Submit" /></p>
                        </body>
                        </html>
                        ''')
