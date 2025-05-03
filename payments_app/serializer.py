# payments/serializers.py

from rest_framework import serializers
from payments_app.models import Payment

class AdminCreatePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'student', 'amount', 'description']
        extra_kwargs = {
            'student': {'write_only': True}
        }

    def create(self, validated_data):
        user = self.context['request'].user
        payment = Payment.objects.create(
            status='accepted',
            confirmed_by=user,
            **validated_data
        )
        return payment


class PaymentDetailSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    confirmed_by = serializers.StringRelatedField()
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    student_full_name = serializers.CharField(source='student.user.full_name', read_only=True)
    student_id = serializers.IntegerField(source='student.id', read_only=True)
    payment_method = serializers.CharField(source='get_payment_method_display', read_only=True)
    class Meta:
        model = Payment
        fields = ['id', 'student','student_full_name', 'student_id','amount', 'description', 'status', 'payment_method','created_at', 'confirmed_by']