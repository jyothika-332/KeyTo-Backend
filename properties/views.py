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
            serializer = Property_serializer(property,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            property = Property.objects.all()
            serializer = Property_serializer(property,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

    def post(self,request): 
        print( self.request.data)
        try:
            user = User.objects.get(id=self.request.data['user'])
        except:
            return Response("User Not Found",status = status.HTTP_400_BAD_REQUEST)
        serializer = Property_serializer(data=self.request.data , partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save( user = user)
        
        return Response("ok")
    

    def put(self,request):
        try:
            id = self.request.data['id']
        except:
            return Response({'error':'Property not found'},status=status.HTTP_404_NOT_FOUND)
        
        property = Property.objects.get(id=id)
        serializer = Property_serializer(property,data=request.data,partial=True)
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
            datas = Property.objects.get(id=id).delete()           
            return Response({
                "message" : "Property Deleted Succesfully"
            })
        else:
            return Response(
                {
                    "message" : "Id not Given"
                }
            )
        

