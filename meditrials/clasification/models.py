from django.db import models
from urllib.parse import urlencode

class Diagnostic(models.Model):
    study_and_condition = models.TextField()

    def __str__(self):
            return self.study_and_condition
    def get_absolute_url(self):
        #Cálculo probabilidad y cluster del diagnóstico

        base_url = '/results?'
        query_string =  urlencode({'cluster': 0, 'probability': 0.5}) 
        return base_url+query_string