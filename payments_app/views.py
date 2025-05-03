# payments/views.py
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.views import APIView
from django.utils.dateparse import parse_date
from rest_framework.response import Response
from rest_framework import status
from payments_app.models import Payment
from payments_app.serializer import AdminCreatePaymentSerializer, PaymentDetailSerializer
from common_app.permissions import AdminOrOwner

class AdminCreatePaymentView(APIView):
    permission_classes = [AdminOrOwner]
     
    @swagger_auto_schema(request_body=AdminCreatePaymentSerializer) 
    def post(self, request):
        serializer = AdminCreatePaymentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            payment = serializer.save()
            return Response(PaymentDetailSerializer(payment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentListView(APIView):
    permission_classes = [AdminOrOwner]

    @swagger_auto_schema(responses={200: PaymentDetailSerializer(many=True)})
    def get(self, request):
        # Agar admin bo‘lsa, barcha to‘lovlarni ko‘rsatish
        if request.user.is_admin:
            payments = Payment.objects.all()
        else:
            # Student bo‘lsa, faqat o‘zining to‘lovlarini ko‘rsatish
            payments = Payment.objects.filter(student__user=request.user)

        serializer = PaymentDetailSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdminUpdatePaymentView(APIView):
    permission_classes = [AdminOrOwner]

    @swagger_auto_schema(request_body=PaymentDetailSerializer)
    def put(self, request, payment_id):
        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            return Response({"detail": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

        # Faqat admin to‘lov holatini o‘zgartirishga ruxsat beradi
        if request.user.is_admin:
            serializer = PaymentDetailSerializer(payment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    
class AdminDeletePaymentView(APIView):
    permission_classes = [AdminOrOwner]

    def delete(self, request, payment_id):
        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            return Response({"detail": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

        # Faqat admin to‘lovni o‘chirishi mumkin
        if request.user.is_admin:
            payment.delete()
            return Response({"detail": "Payment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    
class PaymentStudentIDListView(APIView):
    permission_classes = [AdminOrOwner]

    @swagger_auto_schema(responses={200: PaymentDetailSerializer(many=True)})
    def get(self, request, id):
        # student_id 'id' orqali olinadi
        payments = Payment.objects.filter(student_id=id)
        
        serializer = PaymentDetailSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class PaymentDateRangeView(APIView):
    permission_classes = [AdminOrOwner]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Boshlanish sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Tugash sanasi (YYYY-MM-DD)", type=openapi.TYPE_STRING),
        ],
        responses={200: PaymentDetailSerializer(many=True)}
    )
    def get(self, request):
        start_date = parse_date(request.query_params.get('start_date'))
        end_date = parse_date(request.query_params.get('end_date'))

        if start_date and end_date:
            payments = Payment.objects.filter(created_at__date__range=(start_date, end_date))
        else:
            return Response({'error': "start_date va end_date kerak. Format: YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PaymentDetailSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


