from django.urls import path, include
from . import views


urlpatterns = [
    path("auth/", views.UserAuthDetail.as_view()),
    path('signin/', views.UserSigninView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('user/', views.UserInfoListView.as_view()),
    path('user/<int:pk>/', views.UserInfoDetailView.as_view()),
]