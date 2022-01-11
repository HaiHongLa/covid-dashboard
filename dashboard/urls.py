from django.conf.urls import url
from . import views
from django.urls import path
from django.conf import settings
from django.views.generic import View, TemplateView
from dashboard.views import IndexView, SingleStateView

app_name = 'dashboard'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('state/', views.SingleStateView.as_view(), name='state'),
    path('update/', views.update_data, name='update'),

    path('usaNewCases/', views.TemplateView.as_view(template_name='LineChartDailyCases.html'), name='usaNewCases'),
    path('usaDeaths/', views.TemplateView.as_view(template_name='LineChartDailyDeaths.html'), name='usaDeaths'),
    path('newCases/', views.TemplateView.as_view(template_name = 'newCases.html'), name='newCases'),
    path('newDeaths/', views.TemplateView.as_view(template_name = 'newDeaths.html'), name='newDeaths'),
    path('top10cases/', views.TemplateView.as_view(template_name = 'top10StatesNewCases.html'), name='top10cases'),
    path('top10deaths/', views.TemplateView.as_view(template_name = 'top10StatesNewDeaths.html'), name='top10deaths'),
    path('nvp/', views.TemplateView.as_view(template_name='NegVsPos.html'), name='nvp'),

    # Risk level graphs paths
    path('riskLevelsOverall/', views.TemplateView.as_view(template_name='overall.html'), name='riskLevelsOverall'),
    path('riskLevelsTestPositivityRatio/', views.TemplateView.as_view(template_name='testPositivityRatio.html'), name='riskLevelsTestPositivityRatio'),
    path('riskLevelsCaseDensity/', views.TemplateView.as_view(template_name='caseDensity.html'), name='riskLevelsCaseDensity'),
    path('riskLevelsCTCR/', views.TemplateView.as_view(template_name='contactTracerCapacityRatio.html'), name='riskLevelsCTCR'),
    path('riskLevelsInfectionRate/', views.TemplateView.as_view(template_name='infectionRate.html'), name='riskLevelsInfectionRate'),
    path('riskLevelsICU/', views.TemplateView.as_view(template_name='icuCapacityRatio.html'), name='riskLevelsICU'),
]