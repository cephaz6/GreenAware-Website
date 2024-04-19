from django.urls import path
from main import views
from django.conf.urls import handler404

urlpatterns = [
    path('', views.index_page, name='index_page'),
    path('contact-us', views.contact_page, name='contact_page'),
    path('register/', views.register_page, name='register_page'),
    path('login/', views.login_page, name='login_page'),


    #OtherPages
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-and-conditions/', views.terms, name='terms'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('api-guide/', views.api_guide, name='api_guide'),
    path('pricing/', views.pricing, name='pricing'),
    path('about-us/', views.about),


    #Authentications
    path('register-user/', views.register, name='register'),
    path('login-user/', views.login, name='login'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]   

# handler404 = 'main.views.custom_404'