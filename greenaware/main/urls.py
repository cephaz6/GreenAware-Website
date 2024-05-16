from django.urls import path, re_path
from main import views
from django.conf.urls import handler404
from django.views.generic import TemplateView

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
    path('verify/<str:token>/', views.activate, name='activate'),
    path('logout/', views.logout_user, name='logout'),

    #User Dashboard
    path('dashboard/', views.user_dashboard, name='user-dashboard'),
    path('subscriptions/', views.user_subscribe, name='user-subscribe'),
    path('checkout/', views.user_checkout, name='user-checkout'),
    path('pay/<str:payment_intent_id>', views.pay, name='pay'),
    path('update-profile/', views.user_update_profile, name='user-profile-update'),
    path('update-password/', views.user_update_password, name='user-password-update'),
    path('payment-history/', views.user_history, name='user-pay-history'),
    path('my-services/', views.user_services, name='user-services'),
    path('generate-api-key/', views.generate_key, name='generate-key'),

    #Observer Dashboard
    path('new-observation/', views.add_observation, name='new-observation'),
    path('bulk-observations/', views.bulk_observations, name='bulk_observations'),
    path('view-observations/', views.observations, name='observations'),
    path('edit-observation/<int:observation_id>/', views.edit_observation, name='edit_observation'),
    # path('delete-observation/<int:observation_id>/', views.delete_observation, name='delete_observation'),


    #system Endpoints
    path('fetch-api-keys/', views.fetch_api_keys, name='fetch-api-keys'),
    path('register-api-call/', views.register_call, name='register_api_call'),
    
    #Error
    path('404/', TemplateView.as_view(template_name='404.html'), name='404'),
    path('unauthorized/', views.error_401, name='401'),
]   

# Assign the custom_404 function as the handler for 404 errors
handler404 = views.custom_404_view