from django import forms

class DiagnosisForm(forms.Form):
    study_and_condition = forms.CharField(widget=forms.Textarea(attrs={"rows":20, "cols":80}), required=True)
