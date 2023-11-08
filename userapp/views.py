from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.generics import ListAPIView,UpdateAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
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
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class CustomPagination(PageNumberPagination):
    page_size = 5  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class UpdateSeller(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = User_serializer

    def partial_update(self, request, *args, **kwargs):
        # Exclude id_card_image from the request data before performing the update
        if 'id_card_image' in request.data:
            del request.data['id_card_image']

        return super().partial_update(request, *args, **kwargs)


class UserView(ListAPIView):
    pagination_class = CustomPagination
    def get(self,req):  
        try:
            id = self.request.GET.get("id")
        except:
            id = ""
        try:
            is_seller = self.request.GET.get("is_seller")
        except:
            is_seller = False
        try:
            search = self.request.GET.get("search")
        except:
            search = ""

        if is_seller == "true":
            user = User.objects.filter(role = "seller")
            if search:
                user = user.filter(first_name__icontains = search)
            serializer = User_serializer(user,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if is_seller == "false":
            user = User.objects.filter(role = "user")
            if search:
                user = user.filter(first_name__icontains = search)
            serializer = User_serializer(user,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if id:
            user = User.objects.get(id=id)
            serializer = User_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            paginator = CustomPagination()
            result_page = paginator.paginate_queryset(User.objects.all(), req)
            serializer = User_serializer(result_page, many=True)
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
        except KeyError:
            id = ""   
        if id:
            datas = User.objects.filter(id=id)
            if datas.count() > 0 :
                datas = datas.first()
                try:
                    password = self.request.data['password']
                except KeyError:
                    password = ""
                try:
                    type = self.request.data['type']
                except KeyError:
                    type = ""
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
                
                if type == "status":
                    print("THE IS ACTIVE" , self.request.data['is_active'])
                    if self.request.data['is_active'] == True:
                        subject = 'Account Status Changed',
                        message = "Hi , Your Account is Activated Now"
                        email_from = settings.EMAIL_HOST
                        send_mail(subject , message , email_from ,[self.request.data['email']])
                    else:
                        subject = 'Account Status Changed',
                        message = "Hi , Your Account is Deactivated Now"
                        email_from = settings.EMAIL_HOST
                        send_mail(subject , message , email_from ,[self.request.data['email']])
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
                is_present = User_otp.objects.filter(email = email).count()
                if is_present == 0 :
                    user_obj = User_otp.objects.create(email = email,otp = otp)
                    user_obj.save()

                else:
                    user_obj = User_otp.objects.get(email = email)
                    user_obj.email = email
                    user_obj.otp = otp
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

class SendResetLink(ListAPIView):
    def post(self,request):
        try:
            email = self.request.data['email']
        except:
            return Response({"message" : "Invalid Request"} , stats = status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(username = email)

        if user.count():
            user  = user.first()
            token = default_token_generator.make_token(user)
            reset_url = "Your Password Reset Link is Here Please Click "f"http://localhost:5173/reset-password/{user.id}/{token}"
            subject = 'Password Reset'
            message = reset_url
            email_from = settings.EMAIL_HOST
            send_mail(subject , message , email_from ,[email]) 
            return Response({"message" : "ok"} , status= status.HTTP_200_OK)
        else:
            return Response({"message" : "This Email is Not Registered"} , status= status.HTTP_400_BAD_REQUEST)

class ResetPassword(ListAPIView):
    def post(self,request):
        try:
            token = self.request.data['token']
            password = self.request.data['password']
            user_id = self.request.data['user']
        except:
            return Response({"message" : "Invalid Request"} , stats = status.HTTP_400_BAD_REQUEST)
    
        try:
            user = User.objects.get(pk=user_id)
            if default_token_generator.check_token(user, token):
                password = make_password(password)
                user.password = password
                user.save()
                return Response({"message" : "Password Changed Succesfully"},status = status.HTTP_200_OK)
            else:
                return Response({"message" : "Token is Invalid"} , status = status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message" : "User Does Not Exist"} , status = status.HTTP_400_BAD_REQUEST)

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
        

