from django.urls import path
from . import views
# from .views import custom_404

urlpatterns = [
    path('', views.index_page, name='index_page'),
    path('contact-us', views.contact_page, name='contact_page'),

    #Authentications
    path('register/', views.register_page, name='register_page'),
    path('login/', views.login_page, name='login_page')
]   