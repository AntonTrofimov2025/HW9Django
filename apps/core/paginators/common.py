from rest_framework.pagination import CursorPagination



class CommonPaginator(CursorPagination):
    page_size = 5
    ordering = ['created_at']

