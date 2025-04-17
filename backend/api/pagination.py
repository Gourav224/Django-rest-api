from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 2  # Default number of items per page
    page_size_query_param = "limit"  # Allows clients to specify the limit
    max_page_size = 100  # Prevent abuse by setting a max limit

    def get_page_number(self, request, paginator):
        """
        Override the `get_page_number` method to return 1 if no page is specified.
        """
        page = request.query_params.get(
            self.page_query_param, 1
        )  # Default to 1 if page is not provided
        try:
            page = int(page)
        except ValueError:
            page = 1  # Fallback to 1 if the page is not a valid integer
        return page

    def get_paginated_response(self, data):
        """
        Customize the paginated response to include total count, hasNext, hasPrevious, totalpages, and currentpage.
        """
        total_count = self.page.paginator.count
        page_size = self.page.paginator.per_page
        total_pages = (
            total_count + page_size - 1
        ) // page_size  # Ceiling division to get total pages
        current_page = self.page.number

        return Response(
            {
                "count": total_count,
                "hasNext": self.get_next_link()
                is not None,  # Boolean indicating if there's a next page
                "hasPrevious": self.get_previous_link()
                is not None,  # Boolean indicating if there's a previous page
                "totalPages": total_pages,  # Total number of pages
                "currentPage": current_page,  # Current page number
                "results": data,  # The paginated data
            }
        )
