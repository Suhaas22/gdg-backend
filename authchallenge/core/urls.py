from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CookieTokenObtainPairView.as_view(), name='login'),
    path('refresh/', views.CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('me/', views.MeView.as_view(), name='me'),  # simple protected route

    # Discovery challenge
    path('discover/clue/', views.ClueView.as_view(), name='discover_clue'),
    path('discover/solve/', views.SolveView.as_view(), name='discover_solve'),
    path('discover/secret/', views.SecretView.as_view(), name='discover_secret'),
    path('discover/x9c2k/', views.HiddenView.as_view(), name='discover_hidden'),
]
