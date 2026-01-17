from django.urls import path
from . import views

app_name = 'wrapped'

urlpatterns = [
    path('', views.home, name='home'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('upload/', views.upload_data, name='upload'),
    path('r/<str:token>/', views.wrapped_result, name='wrapped_result'),
]