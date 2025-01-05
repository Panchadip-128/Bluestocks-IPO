# ipo_app/viewsets.py
from .serializers import IPO_Serializer  # Correct import

# Other code for IPOViewSet
class IPOViewSet(viewsets.ModelViewSet):
    queryset = IPO.objects.all()
    serializer_class = IPO_Serializer
