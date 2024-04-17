from django.urls import path
from . import views
# from .views import custom_404

urlpatterns = [
    path('', views.index_page, name='index_page'),
    path('contact-us', views.contact_page, name='contact_page'),
    path('register/', views.register, name='signup'),
    # path('404/', custom_404, name='custom_404'),
]   