from django.urls import path
from readit_site import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.IndexView.as_view(), name="homepage"),
    path('change_password/',
         views.ChangePasswordView.as_view(), name='change_password'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logoutview, name='logout_url'),
    path('register/', views.readitusermodel_view, name="register"),
    path('new/', views.createsubreadit_view,
         name="new"),
    path('r/<str:subreadit>/', views.subreadit_view, name="subreadit"),
    path('r/<str:subreadit>/subscribe/',
         views.subreadit_subscribe, name="subscribe"),
    path('r/<str:subreadit>/<int:postid>/', views.post_view,
         name="post"),
    path('r/<str:subreadit>/<int:postid>/<str:action>/', views.post_action,
         name="post_action"),
    path('r/<str:subreadit>/<int:postid>/<int:commentid>/<str:action>/', views.comment_action,
         name="comment_action"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
