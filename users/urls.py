from django.urls import path
from users import views

urlpatterns = [
    path('csrf', views.GetCsrfToken.as_view(), name='get_csrf_token'),
    path('register', views.RegisterUserView.as_view(), name='register_user'),
    path('login', views.LoginUserView.as_view(), name='login_user'),
    path('logout', views.LogoutUserView.as_view(), name='logout_user'),
    path('whoami', views.WhoAmIView.as_view(), name='who_am_i'),
]