from django.conf import settings
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render

import base64

from .serializers import RegisterSerializer, UserSerializer

from django.http import JsonResponse
from django.conf import settings

def debug_hosts(request):
    return JsonResponse({"ALLOWED_HOSTS": settings.ALLOWED_HOSTS})



# ---------- Protected Views ----------
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_data = UserSerializer(request.user).data
        return render(request, "me.html", {"user": user_data})


# ---------- Discovery Challenge: Riddle Game ----------

class ClueView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        riddle = "I speak without a mouth and hear without ears. I have nobody, but I come alive with wind. What am I?"
        context = {
            "message": "🔎 Solve this riddle to continue!",
            "riddle": riddle,
            "hint": "POST your answer as {'answer': '...'}"
        }
        return render(request, "clues.html", context)

    def post(self, request):
        answer = request.data.get("answer", "").strip().lower()
        expected = "echo"

        if answer == expected:
            secret_path = "/api/discover/x9c2k/"
            encoded = base64.b64encode(secret_path.encode()).decode()
            context = {
                "message": "✅ Correct! Here’s your encoded clue.",
                "next_encoded": encoded,
                "hint": "Decode this base64 to find your next endpoint"
            }
            return render(request, "clue_success.html", context)
        return render(request, "error.html", {"message": "❌ Wrong answer. Try again."})


class HiddenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        context = {
            "message": "✨ You found the hidden path!",
            "riddle": "I’m tall when I’m young and short when I’m old. What am I?",
            "hint": "POST {'answer': '...'} to continue"
        }
        return render(request, "hidden.html", context)

    def post(self, request):
        answer = request.data.get("answer", "").strip().lower()
        if answer == "candle":
            context = {
                "message": "🎉 Correct! You may now visit /api/discover/secret/ for the FLAG."
            }
            return render(request, "hidden_success.html", context)
        return render(request, "error.html", {"message": "❌ Wrong answer. Try again."})


class SecretView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        context = {
            "message": "🎉 Secret unlocked!",
            "hint": "Visit /api/discover/solve/ to get the FLAG 🚩"
        }
        return render(request, "secret.html", context)


class SolveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        context = {
            "secret_key": "FLAG{JWT_AUTH_SUCCESS}"
        }
        return render(request, "solve.html", context)

# ---------- Cookie Helpers ----------
def set_token_cookies(response, access: str, refresh: str):
    access_name = getattr(settings, 'JWT_ACCESS_COOKIE_NAME', 'access')
    refresh_name = getattr(settings, 'JWT_REFRESH_COOKIE_NAME', 'refresh')
    secure = getattr(settings, 'JWT_COOKIE_SECURE', False)
    samesite = getattr(settings, 'JWT_COOKIE_SAMESITE', 'Lax')
    domain = getattr(settings, 'JWT_COOKIE_DOMAIN', None)

    response.set_cookie(
        access_name, access,
        httponly=True, secure=secure, samesite=samesite, domain=domain,
        max_age=15 * 60, path='/'
    )
    response.set_cookie(
        refresh_name, refresh,
        httponly=True, secure=secure, samesite=samesite, domain=domain,
        max_age=7 * 24 * 60 * 60, path='/'
    )
    return response


def clear_token_cookies(response):
    access_name = getattr(settings, 'JWT_ACCESS_COOKIE_NAME', 'access')
    refresh_name = getattr(settings, 'JWT_REFRESH_COOKIE_NAME', 'refresh')
    response.delete_cookie(access_name, path='/')
    response.delete_cookie(refresh_name, path='/')
    return response


# ---------- Auth Endpoints ----------
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': '✅ Registered successfully'}, status=status.HTTP_201_CREATED)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CookieTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data
        access = data.get('access')
        refresh = data.get('refresh')

        if access and refresh:
            resp = Response({
                'message': '✅ Login successful, next_step: /api/discover/clue/',
                'access': access,
                'refresh': refresh
            }, status=status.HTTP_200_OK)
            return set_token_cookies(resp, access, refresh)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CookieTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        if 'refresh' not in request.data:
            refresh_name = getattr(settings, 'JWT_REFRESH_COOKIE_NAME', 'refresh')
            request.data['refresh'] = request.COOKIES.get(refresh_name)

        response = super().post(request, *args, **kwargs)
        access = response.data.get('access')
        refresh = response.data.get('refresh')

        if access:
            resp = Response({
                'message': '♻️ Token refreshed',
                'access': access,
                'refresh': refresh or request.data['refresh']
            }, status=status.HTTP_200_OK)
            return set_token_cookies(resp, access, refresh or request.data['refresh'])

        return Response({'detail': 'Invalid refresh'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get(getattr(settings, 'JWT_REFRESH_COOKIE_NAME', 'refresh'))
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass

        response = Response({'message': '👋 Logged out'}, status=status.HTTP_200_OK)
        return clear_token_cookies(response)
