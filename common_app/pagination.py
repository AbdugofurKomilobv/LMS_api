from rest_framework.pagination import PageNumberPagination



# Umumiy pagination sozlamalari
class Pagination(PageNumberPagination):
    page_size = 25  # Default sahifa o'lchami
    page_size_query_param = "page_size"  # URL orqali o'lchamni o'zgartirish parametri
    max_page_size = 55  # Maksimal sahifadagi obyektlar soni


# Talabalar davomati uchun sahifalash sozlamalari
class StudentAttendancePagination(PageNumberPagination):
    page_size = 1  # Default sahifadagi elementlar soni
    page_query_param = 'page_size'  # URL orqali page_size ni o'zgartirish imkoniyati
    max_page_size = 55  # Maksimal ruxsat etilgan sahifa o'lchami
