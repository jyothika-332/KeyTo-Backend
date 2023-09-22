from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import *  
from .serializers import *
from rest_framework.response import Response
from rest_framework import status



# Create your views here.

class PropertyView(ListAPIView):
    def get(self,request):
        try:
            id = self.request.GET.get("id")
        except:
            id = ""

        if id:
            property = Property.objects.get(id=id)
            serializer = Property_serializer(property)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            property = Property.objects.all()
            serializer = Property_serializer(property)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

    def post(self,request): 
        serializer = Property_serializer(data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    

    def put(request,id):
        try:
            property = Property.objects.filter(id=id)
        except:
            return Response({'error':'Property not found'},status=status.HTTP_404_NOT_FOUND)

        serializer = Property_serializer(property,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
