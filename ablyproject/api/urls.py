from django.urls import path, include
from . import views


urlpatterns = [
    path('signup/', views.UserSignupView.as_view()),
    path('auth/', views.UserAuthView.as_view()),
    path('login/', views.UserLoginView.as_view()),
    path('logout/', views.UserLogoutView.as_view()),
    path('user/<str:phone_number>/', views.UserInfoDetailView.as_view()),
]