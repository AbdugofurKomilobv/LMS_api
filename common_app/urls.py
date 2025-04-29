from django.urls import path

from common_app.views import InfoTemplateView

app_name = 'infos'
urlpatterns = [
    path('',InfoTemplateView.as_view(),name='info'),
]