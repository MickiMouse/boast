from django.urls import path

from .views import (
    BoastLoginView,
    BoastLogoutView,
    BoastRegisterView,
    BoastRegisterDoneView,
    BoastPasswordResetView,
    BoastPasswordResetConfirmView,
    activate,
    profile,
)

app_name = 'boast_auth'

urlpatterns = [
    path('register/activate/<str:sign>/', activate, name='register_activate'),
    path('register/done/', BoastRegisterDoneView.as_view(), name='register_done'),
    path('register/', BoastRegisterView.as_view(), name='register'),
    path('password-reset/<uidb64>/<token>/', BoastPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/', BoastPasswordResetView.as_view(), name='password_reset'),
    path('login/', BoastLoginView.as_view(), name='login'),
    path('logout/', BoastLogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
]
