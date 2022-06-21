from rest_framework import generics
from .serializer import DogSerializer
from .models import Dogs
from .permissions import IsOwnerOrReadOnly

class DogList(generics.ListCreateAPIView):
    queryset = Dog.objects.all()
    serializer_class = DogSerializer


class DogDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,) # adds permissions
    queryset = Dogs.objects.all()
    serializer_class = DogSerializer
