import json
import pandas as pd
from joblib import load
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.http import JsonResponse, HttpResponse, HttpRequest
from clasification.models import Diagnostic
from manage import model


def index(request):
    return render(request, 'clasification/welcome.html')

def number(request):
    return render(request, 'clasification/diagnostic_number.html')

def many_diagnosis(request):
    if request.method == "POST":
        numero_diagnosticos = request.POST.get('number-diagnostics')
        context = {'range': range(int(numero_diagnosticos))}
        return render(request, 'clasification/multi_diagnosis_form.html', context=context)

    return HttpResponse("Error")

def many_results(request: HttpRequest):
    if request.content_type == "multipart/form-data":
        diagnostics = request.POST.getlist('study_and_condition')
        df = pd.DataFrame({'study_and_condition': diagnostics})
        X = df
        groups = model.predict(X).tolist()
        probabilities = model.predict_proba(X).tolist()
        final_diagnosis = []
        for i in range(len(groups)):
            final_diagnosis.append({'group': groups[i], 'probability': probabilities[i]})
        context = {'diagnosis': final_diagnosis}
        return render(request, 'clasification/diagnosis_results.html', context=context)
    elif request.content_type == 'application/json':
        parsed_body = json.loads(request.body.decode("utf-8"))
        df = pd.DataFrame(parsed_body)
        df.columns=['study_and_condition']
        X = df['study_and_condition']
        groups = model.predict(X).tolist()
        probabilities = model.predict_proba(X).tolist()
        groups = [0, 1]
        probabilities = [0.5 , 0]
        final_diagnosis = []
        for i in range(len(groups)):
            final_diagnosis.append({'group': groups[i], 'probability': probabilities[i]})
        return JsonResponse(final_diagnosis, safe=False)
    return HttpResponse("Error")

def single_result(request):
    group = request.GET.get('cluster')
    probability = request.GET.get('probability')
    context={'group': group,
    'probability': probability}
    return render(request, 'clasification/diagnosis_result.html', context=context)

class JsonableResponseMixin:
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        input_diagnosis = self.get_data(context)
        group = 0
        probability = 0.5
        final_diagnosis = {'group': group, 'probability': probability}

        return JsonResponse(
            final_diagnosis,
            **response_kwargs
        )
    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        return context

class DiagnosisCreateView(JsonableResponseMixin,CreateView):
    model = Diagnostic
    fields = ['study_and_condition']

    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.content_type == 'application/json':
            parsed_body = json.loads(self.request.body.decode("utf-8"))
            return self.render_to_json_response(parsed_body)
        else:
            return super().render_to_response(context)