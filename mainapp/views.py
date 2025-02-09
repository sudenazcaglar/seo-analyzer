from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, UserSerializer
from .seo_utils import analyze_seo


@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello from the SEO Analyzer!"})

# Kayıt (Register) için View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny] # Herkes kayıt olabilir.
    serializer_class = RegisterSerializer


# Profil görüntüleme için View
class ProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated] # Giriş yapmadan erişilemez.
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class SEOAnalyzerView(APIView):
    """Verilen URL için temel SEO analizinii dönen API."""

    def post(self, request):
        url = request.data.get("url")

        if not url:
            return Response({"error": "Lütfen bir URL girin."}, status=status.HTTP_400_BAD_REQUEST)
        
        seo_result = analyze_seo(url)
        return Response(seo_result, status=status.HTTP_200_OK)