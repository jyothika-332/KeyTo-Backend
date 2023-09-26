from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import *  
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


# Create your views here.


class BannerView(ListAPIView):
    def get(self,request):
        try:
            id = self.request.GET.get("id")
        except:
            id = ""

        if id:
            banner = Banner.objects.get(id=id)
            serializer = Banner_serializer(banner,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            banner = Banner.objects.all()
            serializer = Banner_serializer(banner,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

    def post(self,request):
        serializer = Banner_serializer(data = request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)    
    

    def put(self,request):
        try:
            id = self.request.data['id']
        except:
            return Response({'error':'Banner not found'},status=status.HTTP_404_NOT_FOUND)
        
        banner = Banner.objects.get(id=id)
        serializer = Banner_serializer(banner,data = request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request):
        try:
            id = self.request.data['id']
        except:
            id = ""

        if id:
            datas = Banner.objects.get(id=id).delete()           
            return Response({
                "message" : "Banner Deleted Succesfully"
            })
        else:
            return Response(
                {
                    "message" : "Id not Given"
                }
            )
        

