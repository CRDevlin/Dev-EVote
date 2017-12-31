from django.db import models
from website.settings import CONFIG


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
    election = models.ForeignKey(Election, verbose_name="Election", null=True)
    faculty = models.ForeignKey(Faculty, verbose_name="Faculty", null=True)


class Record(models.Model):
    voter = models.ForeignKey(Faculty, verbose_name="Faculty", null=False, related_name="Voter")
    election = models.ForeignKey(Election, verbose_name="Election", null=False, related_name="Election")
    choice = models.ForeignKey(Nominee, verbose_name="Nominee", null=True, related_name="Nominee")
    token = models.CharField(max_length=CONFIG['VOTE_TOKEN_LEN'], verbose_name="Voter Token", unique=True)
    weight = models.FloatField(verbose_name="Voter Weight")
