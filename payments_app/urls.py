
from django.urls import path
from payments_app.views import AdminCreatePaymentView,PaymentListView,AdminUpdatePaymentView,AdminDeletePaymentView,PaymentStudentIDListView,PaymentDateRangeView

app_name = 'payments_app'

urlpatterns = [
    path('admin/create/', AdminCreatePaymentView.as_view(), name='admin-payment-create'),
    path('list/', PaymentListView.as_view(), name='payment-list'),
    path('admin/update/<int:payment_id>/', AdminUpdatePaymentView.as_view(), name='admin-payment-update'),
      path('admin/delete/<int:payment_id>/', AdminDeletePaymentView.as_view(), name='admin-payment-delete'),
      path('admin/student-payments/<int:id>/',PaymentStudentIDListView.as_view()),
      path('payments/date-range/', PaymentDateRangeView.as_view(), name='payment-date-range'),

]
