from django.urls import path, include
from . import views


urlpatterns = [
    path("auth/", views.UserAuthDetail.as_view()),
    path('user/', views.UserListMixins.as_view()),
    path('user/<int:pk>/', views.UserDetailMixins.as_view())

]