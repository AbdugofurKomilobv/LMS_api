from django.contrib import admin

# Register your models here.


from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'status', 'payment_method', 'created_at', 'confirmed_by')
    search_fields = ('student__user__full_name', 'student__user__phone', 'status', 'payment_method')
    list_filter = ('status', 'payment_method', 'created_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'confirmed_by')

admin.site.register(Payment, PaymentAdmin)
