from django.urls import path

from . import views

app_name = 'berealeye'
urlpatterns = [
    path('', views.index, name='index'),
    path('refresh', views.refresh_token, name='refresh_token'),
    path('logout', views.logout, name='logout'),
]