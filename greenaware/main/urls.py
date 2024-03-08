from django.urls import path
from . import views
# from .views import custom_404

urlpatterns = [
    path('', views.index_page, name='index_page'),
    # path('404/', custom_404, name='custom_404'),
]   