from django.urls import path
from readit_site import views

urlpatterns = [
    path('', views.index, name="homepage"),
    path('login/', views.login_view),
    path('register/', views.readitusermodel_view, name="register"),
]