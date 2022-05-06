from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='base'),
    path('diagnosis/add/', views.DiagnosisCreateView.as_view(), name='diagnosis-add'),
    path('results/', views.single_result, name='results'),
    path('resultsMany/', views.many_results, name='results_many'),
    path('diagnosis_number/', views.number, name='number'),
    path('diagnosis/addMany/', views.many_diagnosis)
]