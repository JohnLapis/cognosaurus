from django.db import models


class Cognate(models.Model):
    concept_id = models.CharField(max_length=9, null=True)
    lang_1 = models.CharField(max_length=3)
    lang_2 = models.CharField(max_length=3)
    word_1 = models.CharField(max_length=80)
    word_2 = models.CharField(max_length=80)
