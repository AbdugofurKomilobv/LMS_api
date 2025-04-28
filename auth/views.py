from random import randint

from django.core.cache import cache
from django.template.context_processors import request
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from auth.serializers import LoginSerializer, MeSerializer, ChangePasswordSerializer, ResetPasswordSerializer, \
    VerifyOTPSerializer, SetNewPasswordSerializer

from user_app.models import User


class LohinAPIView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self,request):
        phone = request.data.get('phone')
        password = request.data.get('password')


        user = User.objects.filter(phone=phone).first()

        if user and user.check_password(password):

            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                # "is_admin": request.user.is_admin,
                # "is_student": request.user.is_student,
                # "is_teacher": request.user.is_teacher,
                # "is_staff": request.user.is_staff,

            },status=200)
        return Response({"status":False,"detail": "Telefon raqam yoki parol noto‘g‘ri"}, status=401)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({'error': 'Tokenni yangilash talab qilinadi.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Tokenni qora ro‘yxatga qo‘yish
            return Response({"message": "Chiqish muvaffaqiyatli"}, status=status.HTTP_200_OK)
        except (TokenError, InvalidToken) as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




class CurrentUserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user  # Bu tizimga kirgan foydalanuvchini qaytaradi

class CheckUserAuthenticationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            # Tizimga kirgan foydalanuvchi
            return Response({"message": "Foydalanuvchi tizimga kirgan",'user':request.user.full_name}, status=200)
        else:
            # Tizimga kirmagan foydalanuvchi
            return Response({"message": "Foydalanuvchi tizimga kirmagan"}, status=200)
        

