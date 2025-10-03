from .serializers import *
from rest_framework import generics
from.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status

# Create your views here.
class PostPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100

class CategoryListView(generics.ListAPIView):   
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SVGImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    pagination_class = PostPagination

class FileByCategoryAPIView(APIView):
    pagination_class = LimitOffsetPagination()

    def post(self, request, format=None):
        category_list = request.data.get('categories', None)
        search_query = request.data.get('search', '').strip()  # search keyword from JSON

        # Start with all files
        files = File.objects.all()

        # Filter by categories if provided
        if category_list:
            files = files.filter(category_id__in=category_list)

        # Filter by name if search keyword provided
        if search_query:
            files = files.filter(name__icontains=search_query)

        # Order by latest first
        files = files.order_by('-id')

        # Pagination
        paginator = self.pagination_class
        page = paginator.paginate_queryset(files, request, view=self)
        serializer = FileSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

class CopySVG(generics.RetrieveAPIView):
    serializer_class = SvgSerializer
    queryset = File.objects.all()
    lookup_field = 'pk'

