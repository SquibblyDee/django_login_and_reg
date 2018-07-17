from django.conf.urls import url
from . import views

urlpatterns = [
    # root goes to the index
    url(r'^$', views.index),
    #Processing route for registration
    url(r'process_register', views.process_register),
    #Processing route for login
    url(r'process_login', views.process_login),
    #Render success page
    url(r'success', views.success),

]