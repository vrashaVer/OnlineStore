from django.urls import path
from Catalog import views

urlpatterns = [
    path('test/', views.TestView.as_view(), name='test'),
    path('help-center/<str:category>/', views.AccountHelpView.as_view(), name='account_help'),
    path('help-center/<str:category>/<str:section>/', views.AccountHelpView.as_view(), name='help'),
    path('about-us/', views.AboutView.as_view(), name='about'),
    path('join-us/', views.JoinUsView.as_view(), name='join_us'),

]
