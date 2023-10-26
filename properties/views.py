from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import *  
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from userapp.models import *
from properties.models import *

# Create your views here.

class PropertyView(ListAPIView):
    def get(self,request):
        try:
            id = self.request.GET.get("id")

        except:
            id = ""
        
        try:
          user = self.request.GET.get("user")
        except:
          user = ""
        
        try:
          price = self.request.GET.get("price")
        except:
          price = ""

        try:
          place = self.request.GET.get("place")
        except:
          place = ""
        
        try:
            is_premium = self.request.GET.get("is_premium")
        except:
            is_premium = False

        property = Property.objects.all()
        if user:
            property = Property.objects.all()
        else:
            property = property.filter(is_sold = False)
        if id:
            property = property.get(id=id)
            serializer = Property_serializer(property)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if user:
            property = property.filter(user__id = user)

        if place :
            property = property.filter(location__icontains = place)
        if price :
            property = property.filter(price_per_cent__lte=price )
  
        
        if is_premium :
            property = property.filter(user__is_premium = True)[:6]

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
        

class DashboardDatasViews(ListAPIView):
    def get(self,req):
        user_count = User.objects.filter(role = 'user').count()
        premium = User.objects.filter(role = 'seller' , is_premium = True).count()
        not_premium = User.objects.filter(role = 'seller' , is_premium = False).count()
        seller_count = User.objects.filter(role = 'seller').count()
        sold_property = Property.objects.filter(is_sold = True).count()
        not_sold_property = Property.objects.filter(is_sold = False).count()
        rent_property = Property.objects.filter(type = 'rent').count()
        sale_property = Property.objects.filter(type = 'sale').count()

        data = {
            'user_count' : user_count,
            'seller_count' : seller_count,
            "sold_property" : sold_property,
                "not_sold_property" : not_sold_property,
                "premium" : premium,
"not_premium" : not_premium,
"rent_property" : rent_property,
"sale_property" : sale_property,
        }

        return Response(data,status=status.HTTP_200_OK)

class DashboardDatasViewsSeller(ListAPIView):
    def get(self,req):
        try:
            id = self.request.GET.get("id")
        except:
            id = ""
        if id:
            propertyes = Property.objects.filter(user__id = id).count()
            sold = Property.objects.filter(user__id = id , is_sold = True).count()
       

        data = {
            'property' : propertyes,
            'sold' : sold
        }

        return Response(data,status=status.HTTP_200_OK)