from django.db import models
from urllib.parse import urlencode
import pandas as pd
from manage import model

class Diagnostic(models.Model):
    diagnostico = models.TextField()

    def __str__(self):
            return self.diagnostico
    def get_absolute_url(self):
        #Cálculo probabilidad y cluster del diagnóstico
        df = pd.DataFrame({'study_and_condition': [self.diagnostico]})
        X = df
        groups = model.predict(X).tolist()
        probabilities = model.predict_proba(X).tolist()

        d = {}
        d['cluster'] = "No elegible" if groups[0] == "__label__1" else "Elegible"
        d['probability'] = round(probabilities[0][1]*100, 2) if groups[0] == "__label__1" else round(probabilities[0][0]*100, 2)

        base_url = '/results?'
        query_string =  urlencode(d) 
        return base_url+query_string