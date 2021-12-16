from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination


class CustomOffsetPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response({
            'full_count': self.count,
            'showed_count': len(data),
            'data': data })

    def paginate_queryset(self, queryset, request, view=None):

        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.count = self.get_count(queryset)
        self.offset = self.get_offset(request)
        self.request = request

        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        final_offset = self.offset * self.limit
        if final_offset >= len(queryset):
            return []
        else:
            return list(queryset[final_offset:final_offset + self.limit])