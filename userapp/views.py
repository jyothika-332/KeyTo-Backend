from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status
from .models import *  
from .serializers import *
from .email import *
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView



# Create your views here.


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
                return Response({
                    'status' : 400,
                    'message' : 'Something went wrong',
                    'data' : 'Invalid email'
                })
                
            if user_otp.first().otp != int(otp):
                return Response({
                    'status' : 400,
                    'message' : 'Something went wrong',
                    'data' : 'Wrong otp'
                })
            user_otp = User_otp.objects.filter(email = email).first().delete()  
            return Response({
                'status' : 200,
                'message' : 'Account Verified',
                'data' : {},
            })

        except Exception as e:
            print(e)
    



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
   
# class LoginView(ListAPIView):
#     def post(self,req):
#         try:
#             username = self.request.data['email']
#             password = self.request.data['password']
#         except:
#             return Response({ "message" : "Invalid Request"} , status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             user = User.objects.get(email=username)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         if check_password(password, user.password):
#             data = {
#                 "id" : user.id,
#                 "role" : user.role
#             }
#             return Response({ "message" : "Succesfully Loged In" , "data" : data} , status=status.HTTP_200_OK)
#         else:
#             return Response({ "message" : "Invalid Username and Password"} , status=status.HTTP_400_BAD_REQUEST)
        

