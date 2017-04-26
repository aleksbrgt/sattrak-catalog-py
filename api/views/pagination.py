from rest_framework import pagination

class StandardResultSetPagination(pagination.PageNumberPagination):
    """
        Pagination class used in views returning a lot of data
    """
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000