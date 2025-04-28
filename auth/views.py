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


        

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self,request):
        serializer = ChangePasswordSerializer(data = request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'status': False, 'detail':'Eski parol xato'},status=400)
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response({'status':True,'detail':'Parolingiz muaffaqiyatli yangilandi!'},status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class ResetPasswordView(APIView):
    @swagger_auto_schema(request_body=ResetPasswordSerializer)
    def post(self,request):
        serializer = ResetPasswordSerializer(data = request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            user = User.objects.filter(phone=phone)

            if user:
                otp_code = str(randint(1000,9999))
                print('Otp code:', otp_code)
                cache.set(phone,otp_code,timeout=900)

                return Response({"status": True, "detail": "OTP muvaffaqiyatli yuborildi"}, status=status.HTTP_200_OK)
            return Response({"status": False, "detail": "Bunday telefon raqam mavjud emas"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    @swagger_auto_schema(request_body=VerifyOTPSerializer)
    def post(self,request):
        serializer = VerifyOTPSerializer(data = request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            cache.set(f'verified_{phone}', True,timeout=900)
            return Response({"status": True, "detail": "OTP muvaffaqiyatli tasdiqlandi"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordView(APIView):
    @swagger_auto_schema(request_body=SetNewPasswordSerializer)
    def post(self,request):
        serializer = SetNewPasswordSerializer(data = request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            verifed = cache.get(f'verified_{phone}')

            if not verifed:
                return Response({"status": False, "detail": "OTP tasdiqlanmagan"}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.filter(phone=phone).first()
            if user:
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({"status": True, "detail": "Parol muvaffaqiyatli o‘rnatildi"}, status=status.HTTP_200_OK)
            return Response({"status": False, "detail": "Foydalanuvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            




