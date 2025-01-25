from django.urls import path
from Catalog import views

urlpatterns = [
    path('test/', views.TestView.as_view(), name='test'),
]
