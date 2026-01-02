from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupView, ReporteeCreateView, LogoutView, UserMeView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("reportees/", ReporteeCreateView.as_view(), name="reportee-create"),
    path("me/", UserMeView.as_view(), name="user-me"),
]
