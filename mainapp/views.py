from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer


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

