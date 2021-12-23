from django.contrib import admin
from django.urls import path,include
from home import views
from django_email_verification import urls as mail_urls

urlpatterns = [
    path('',views.index, name='home'),
    path('about',views.about, name='about'),
    path('Login',views.loginPage,name="loginPage"),
    path('login',views.loginUser,name="loginUser"),
    path('contacts',views.contacts,name="contacts"),
    path('search',views.search,name="search"),
    path('signup',views.signup,name="signup"),
    path('handlesignup',views.handlesignup,name="handlesignup"),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('resources',views.resources,name="resources"),
    path('discordLink',views.discordLink,name="discordLink"),
    path('handleContact',views.handleContacts,name="handleContacts"),



]