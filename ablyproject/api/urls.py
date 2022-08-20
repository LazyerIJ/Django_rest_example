from django.urls import path, include
from . import views


urlpatterns = [
    path('signup/', views.UserSignupView.as_view({"post": "post", "put": "update"})),
    path('auth/', views.UserAuthView.as_view({"post": "post"})),
    path('login/', views.UserLoginView.as_view({"post": "post"})),
    path('logout/', views.UserLogoutView.as_view({"post": "post"})),
    path('user/', views.UserInfoDetailView.as_view({"get": "get"})),
]