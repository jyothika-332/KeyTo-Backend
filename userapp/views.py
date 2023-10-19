from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.generics import ListAPIView,UpdateAPIView
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
from .models import *  
from .serializers import *
from .email import *
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
import random
from django.conf import settings



# Create your views here.

class UpdateSeller(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = User_serializer

    def partial_update(self, request, *args, **kwargs):
        # Exclude id_card_image from the request data before performing the update
        if 'id_card_image' in request.data:
            del request.data['id_card_image']

        return super().partial_update(request, *args, **kwargs)


class UserView(ListAPIView):
    def get(self,req):  
        try:
            id = self.request.GET.get("id")
        except:
            id = ""

        if id:
            user = User.objects.get(id=id)
            serializer = User_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user = User.objects.all()
            serializer = User_serializer(user , many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    



    def post(self,req):      
        body = None
        try:
            email = self.request.data['email']
            hashed_password = make_password(self.request.data['password'])
        except KeyError:
            return Response({ "message" : "Invalid Request" } , status = status.HTTP_400_BAD_REQUEST)
        
        data = User.objects.filter(email = email)
        print ( data.count() )
        if data.count() > 0:
            return Response({ "message" : "Email Already Exist"} , status = status.HTTP_409_CONFLICT)
        else:
            body = self.request.data
            body['username'] = email
            body['password'] = hashed_password

        serializer = User_serializer(data = body , partial=True)
        serializer.is_valid( raise_exception= True)
        serializer.save()
        send_otp(serializer.data['email'])
        return Response({"message" : "User Registered Succesfully"} , status = status.HTTP_200_OK)


    def put(self,req):
        try:
            id = self.request.data['id']
        except:
            id = ""
        if id:
            datas = User.objects.filter(id=id)
            if datas.count() > 0 :
                datas = datas.first()
                try:
                    password = self.request.data['password']
                except:
                    password = ""
                if password:
                    body = self.request.data
                    body['password'] = make_password(password)
                    serializer = User_serializer(datas , data = body , partial=True)
                    serializer.is_valid( raise_exception=True)
                    serializer.save()
                else:
                    serializer = User_serializer(datas , data = self.request.data , partial=True)
                    serializer.is_valid( raise_exception=True)
                    serializer.save()

                return Response({"message" : "User Updated Succesfully"} , status = status.HTTP_200_OK)
            else:
                return Response({"message" : "User Not Found"} , status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message" : "Invalid Request"} , status = status.HTTP_400_BAD_REQUEST)
        
    

class SendOTP (APIView):
    def post (self,request):
        try:


            email = self.request.data['email']

            data = User.objects.filter(email = email)
            if data.count():
                return Response({"message" : "Email Already Exist"} , status = status.HTTP_409_CONFLICT)

            else:
                subject = 'Your account varification email'
                otp = random.randint(1000 , 9999)
                message = f'Your otp is {otp} '
                email_from = settings.EMAIL_HOST
                send_mail(subject , message , email_from ,[email])
                user_obj = User_otp.objects.create(email = email,otp = otp)
                user_obj.save()
                return Response({"message" : "OTP Send to the Email"})
        except Exception as e:
            print(e)


class VerifyOTP(APIView):
    def post(self,request):
        try:
            data = self.request.data
            print ( data )
            # serializer = VerifyAccountSerializer(d if serializer.is_valid():
            email = self.request.data['email']
            otp = self.request.data['otp']
               
            user_otp = User_otp.objects.filter(email = email)
           
            if user_otp.count() == 0:
                return Response("Invalid OTP",status = status.HTTP_400_BAD_REQUEST)
                
            if user_otp.first().otp != int(otp):
                return Response("Invalid OTP",status = status.HTTP_400_BAD_REQUEST)
            user_otp = User_otp.objects.filter(email = email).delete()
            return Response("OTP OK",status = status.HTTP_200_OK)

        except Exception as e:
            print(e)
    

class AddtoPremium(APIView):
    def put(self,request):
        try:
            id = self.request.data['id']
            premium_starting = self.request.data['premium_starting']
            premium_ending = self.request.data['premium_ending']
        except:
            return Response({ "message" : "Invalid Request"}, status = status.HTTP_400_BAD_REQUEST)
        data = User.objects.filter(id=id)
        if data.count():
            datas = data.first()
            serializer = User_serializer(datas,data=self.request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message" : "Account Changed to Premium"})
        else:
            return Response({"message" : "User Not Found"} , status = status.HTTP_404_NOT_FOUND)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
   


class ChangePassword (ListAPIView):
    def post(self,request):
        try:
            user = self.request.data['id']
            oldpass = self.request.data['oldpass']
            newpass = self.request.data['newpass']
        except:
            return Response({"message" : "Invalid Request"} , stats = status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(id = user)
       
        if  (check_password(oldpass, user.password)):
            hashed_password = make_password(newpass)
            user.password = hashed_password
            user.save()
            return Response({"message" : "Password Updated Succesfully"} , status = status.HTTP_200_OK)
        else:
            return Response({"message" : "Old Password Does Not Match"} , status = status.HTTP_400_BAD_REQUEST)
        

