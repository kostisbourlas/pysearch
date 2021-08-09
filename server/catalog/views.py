
from rest_framework.generics import ListAPIView
from django.db.models import Q

from .models import Wine
from .serializers import WineSerializer
from .filters import WineFilterSet


class WinesView(ListAPIView):
    # queryset = Wine.objects.all()
    serializer_class = WineSerializer
    # filterset_class = WineFilterSet

    def get_queryset(self):
        queryset = Wine.objects.all()
        country = self.request.query_params.get('country')
        if country is not None:
            queryset = queryset.filter(country=country)

        points = self.request.query_params.get('points')
        if points:
            queryset = queryset.filter(points=points)
        
        query = self.request.query_params.get('query')
        if query:
            queryset = queryset.filter(Q(
                Q(variety__contains=query) |
                Q(winery__contains=query) |
                Q(description__contains=query)
            ))
        
        return queryset
