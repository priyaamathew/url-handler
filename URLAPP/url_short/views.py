from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import URL
from .serializers import URLSerializer

class ShortenURLView(APIView):
    def post(self, request):
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.save()
            short_link = request.build_absolute_uri(f'/{url.short_code}')
            return Response({
                "short_url": short_link,
                "original_url": url.original_url,
                "expires_at": url.expires_at
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RedirectURLView(APIView):
    def get(self, request, code):
        url = get_object_or_404(URL, short_code=code)
        if url.is_expired():
            return Response({"error": "This link has expired."}, status=status.HTTP_410_GONE)
        return redirect(url.original_url)
