from django.db import models

token_len = 32
elec_token_len = 9
max_name_len = 50
max_email_len = 50
txt_length = 64


class Election(models.Model):
    anon_voting = models.BooleanField(verbose_name="Anonymous Voting")
    multi_voting = models.BooleanField(verbose_name="Vote Multiple Times")
    final_vote = models.DateTimeField(verbose_name="DateTime Vote By")
    token = models.CharField(max_length=elec_token_len, verbose_name="Election Token", unique=True)


class Faculty(models.Model):
    last_name = models.CharField(max_length=max_name_len)
    first_name = models.CharField(max_length=max_name_len)
    email = models.CharField(max_length=max_email_len)


class Nominee(models.Model):
    election = models.ForeignKey(Election, verbose_name="Election", null=True)
    faculty = models.ForeignKey(Faculty, verbose_name="Faculty", null=True)


class Record(models.Model):
    voter = models.ForeignKey(Faculty, verbose_name="Faculty", null=False, related_name="Voter")
    election = models.ForeignKey(Election, verbose_name="Election", null=False, related_name="Election")
    choice = models.ForeignKey(Nominee, verbose_name="Nominee", null=True, related_name="Nominee")
    token = models.CharField(max_length=token_len, verbose_name="Voter Token", unique=True)
    weight = models.FloatField(verbose_name="Voter Weight")
