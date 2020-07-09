from django.urls import path
from readit_site import views

urlpatterns = [
    path('', views.index, name="homepage"),
    path('login/', views.login_view, name='login_url'),
    path('logout/', views.logoutview, name='logout_url'),
    path('change_password.html',
         views.change_password, name='change_password'),
]
