from django.db import models
from website.settings import CONFIG

"""
The .gliffy file contains ERD
"""


class Election(models.Model):
    anon_voting = models.BooleanField(verbose_name="Anonymous Voting")
    multi_voting = models.BooleanField(verbose_name="Vote Multiple Times")
    final_vote = models.DateTimeField(verbose_name="DateTime Vote By")
    token = models.CharField(max_length=CONFIG['ELEC_TOKEN_LEN'], verbose_name="Election Token", unique=True)


class Faculty(models.Model):
    last_name = models.CharField(max_length=CONFIG['MAX_NAME_LEN'])
    first_name = models.CharField(max_length=CONFIG['MAX_NAME_LEN'])
    email = models.CharField(max_length=CONFIG['MAX_EMAIL_LEN'])


class Nominee(models.Model):
    election = models.ForeignKey(Election, verbose_name="Election", null=True, on_delete=models.DO_NOTHING)
    faculty = models.ForeignKey(Faculty, verbose_name="Faculty", null=True, on_delete=models.DO_NOTHING)


class Record(models.Model):
    choice = models.ForeignKey(Nominee, verbose_name="Nominee", null=True, related_name="Nominee", on_delete=models.DO_NOTHING)
    election = models.ForeignKey(Election, verbose_name="Election", null=False, related_name="Election", on_delete=models.DO_NOTHING)
    voter = models.ForeignKey(Faculty, verbose_name="Faculty", null=False, related_name="Voter", on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=CONFIG['VOTE_TOKEN_LEN'], verbose_name="Voter Token", unique=True)
    weight = models.FloatField(verbose_name="Voter Weight")
