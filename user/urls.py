from django.urls import path, include
from . import views
urlpatterns = [
    path('user-register/', views.UserRegister.as_view() ),
    path('verify/', views.VerifyAPIView.as_view()),
    path('login/', views.UserLogin.as_view()),
]