from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from ..users.serializers import UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def auth_check(request):
    token_key = request.COOKIES.get("token")
    if not token_key:
        return Response({"error": "Authentication credentials were not provided."},
                        status=status.HTTP_401_UNAUTHORIZED)
    try:
        token_obj = Token.objects.get(key=token_key)
    except Token.DoesNotExist:
        return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = UserSerializer(token_obj.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(request, email=email, password=password)
    if not user:
        return Response({"error": "Invalid email or password"},
                        status=status.HTTP_400_BAD_REQUEST)

    update_last_login(None, user)
    
    token_obj, created = Token.objects.get_or_create(user=user)

    response = Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    response.set_cookie(
        key="token",
        value=token_obj.key,
        httponly=True,
        secure=True,   
        samesite="None", 
    )
    return response

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    token_key = request.COOKIES.get("token")
    if token_key:
        try:
            token_obj = Token.objects.get(key=token_key)
            token_obj.delete()
        except Token.DoesNotExist:
            pass
    response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    response.delete_cookie("token", path="/")
    return response
