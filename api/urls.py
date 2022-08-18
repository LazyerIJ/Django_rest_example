from django.urls import path, include
from . import views


urlpatterns = [
    path('signup/', views.UserSignupView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('user/', views.UserInfoListView.as_view()),
    path('user/<int:pk>/', views.UserInfoDetailView.as_view()),
]