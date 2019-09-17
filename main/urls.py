from django.urls import path

from .views import (
    dashboard,
    home,
    boast_create,
    UserDetailView,
    PostChangeView,
    detail_post,
    subscribe_unsubscribe,
    like_post,
    delete_post,
)

app_name = 'main'

urlpatterns = [
    path('subscription/<int:pk>/', subscribe_unsubscribe, name='subscription'),
    path('create/', boast_create, name='create'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='detail_user'),
    path('post/change/<int:pk>/', PostChangeView.as_view(), name='change_post'),
    path('post/delete/<int:pk>/', delete_post, name='delete_post'),
    path('post/<int:pk>/', detail_post, name='detail_post'),
    path('home/', home, name='home'),
    path('like/', like_post, name='like'),
    path('', dashboard, name='dashboard'),
]
