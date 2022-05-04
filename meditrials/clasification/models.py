from django.db import models

class Diagnostic(models.Model):
    study_and_condition = models.TextField()
