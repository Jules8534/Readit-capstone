from django.urls import path
from readit_site import views

urlpatterns = [
    path('', views.index, name="homepage"),
    path('change_password/',
         views.change_password, name='change_password'),
    path('login/', views.login_view),
    path('logout/', views.logoutview, name='logout_url'),
    path('register/', views.readitusermodel_view, name="register"),
    path('new/', views.createsubreadit_view,
         name="new"),  # TODO: add new subreadit
    path('r/<str:subreadit>/', views.subreadit_view,
         name="subreadit"),  # TODO: add view subreadit
    path('r/<str:subreadit>/<int:postid>/', views.post_view,
         name="add_post"),  # TODO: add view subreadit/post
]
