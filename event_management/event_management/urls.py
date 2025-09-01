from django.contrib import admin
from django.urls import path , include
from django.shortcuts import redirect
from event_management_application import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', views.login, name='login_page'),
    path('reset-password/', views.reset_password, name='reset_password'), 
    path('logout/', views.logout, name='logout_action'),
    path('send-otp/', views.send_otp, name='send_otp'),

    # Client pages (no trailing slash)
    path('client_dashboard', views.client_dashboard, name='client_dashboard'),
    path('client_event_list_page.html', views.client_event_list_page, name='client_event_list_page'),
    path("events/<int:event_id>/", views.client_event_detail, name="client_event_detail"),
    path("event/<int:event_id>/", views.event_detail, name="event_detail"),

    # Redirect empty path to login
    path('', lambda request: redirect('login_page')),
]
