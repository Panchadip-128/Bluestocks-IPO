from ipo_app.serializers import IPOSerializer  # Match the name exactly

# Other imports
from rest_framework import viewsets
from .models import IPO  # Assuming IPO is your model

# Define the viewset
class IPOViewSet(viewsets.ModelViewSet):
    queryset = IPO.objects.all()
    serializer_class = IPOSerializer  # Use the correct name here
