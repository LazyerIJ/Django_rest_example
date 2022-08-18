from .models import User, UserInfo, UserAuth
from django.db.models import Q

from .serializers import UserInfoSerializer, UserSerializer, UserAuthSerializer
from .handlers import sms_handler
from rest_framework.views import APIView
from rest_framework.response import Response


class UserSignupView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user_exists = User.objects.filter(
            Q(phone_number=request.data.get("phone_number")) |
            Q(email=request.data.get("email")))
        
        if len(user_exists):
            return Response({"message": "duplicated"})
        
        user_info_serializer = UserInfoSerializer(data=request.data) 
        if not user_info_serializer.is_valid():
            return Response({"message": "not valid"})
            
        user_serializer = UserSerializer(data=request.data) 
        if not user_serializer.is_valid():
            return Response({"message": "not valid"})
        
        user = User.objects.create_user(**user_serializer.data)
        user_info_serializer.validated_data['user'] = user
        user_info_serializer.save()

        phone_number = user_serializer.validated_data.get("phone_number")
        user_auth, _ = UserAuth.objects.update_or_create(phone_number=phone_number)
        naver_sms_handler = sms_handler.NaverSMSHandler(user_auth.phone_number, user_auth.auth_number)
        result = naver_sms_handler.send_sms()
        
        if not result:
            return Response({"message": "auth fail"})

        return Response({"message": "auth true"})
    
    def put(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number", "")
        password = request.data.get("password", "")
        users = User.objects.filter(phone_number=phone_number)
        user = users[0] if users else user
        
        if not user:
            return Response({"message": "not exists"})
        
        user.set_password(password)
        user.verified=False
        user.save()
        
        user_auth, _ = UserAuth.objects.update_or_create(phone_number=phone_number)
        naver_sms_handler = sms_handler.NaverSMSHandler(user_auth.phone_number, user_auth.auth_number)
        result = naver_sms_handler.send_sms()
        return Response({"message": "success. need auth"})
        
        
class UserAuthView(APIView):
    queryset = UserAuth.objects.all()
    serializer_class = UserAuthSerializer
    
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number', '')
        auth_number = request.data.get('auth_number', '')
        result = UserAuth.check_auth_number(phone_number, auth_number)
        if result:
            user = User.objects.filter(phone_number=phone_number)
            if user:
                user[0].verified=True
                user[0].save()
        return Response({
            'message': 'OK',
        })


class UserLoginView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer 

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number", "")
        password = request.data.get("password", "")
        users = UserLoginView.queryset.filter(phone_number=phone_number)
        user = users[0] if users else None
        if not user:
            return Response({"message": "wrong phone_number"})
        if not user.verified:
            return Response({"message": "not varified"})
        if not user.check_password(password):
            return Response({"message": "wrong password"})
        if user.is_login(request):
            return Response({"message": "already login"})
        user.login(request)
        return Response({"message": "login success"})
    
    
class UserLogoutView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer 

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number", "")
        password = request.data.get("password", "")
        users = UserLoginView.queryset.filter(phone_number=phone_number)
        user = users[0] if users else None
        if not user:
            return Response({"message": "wrong phone_number"})
        if not user.check_password(password):
            return Response({"message": "wrong password"})
        if user.is_login(request):
            user.logout(request)
            return Response({"message": "logout success"})
        return Response({"message": "already loged out"})


class UserInfoDetailView(APIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    def get(self, request, *args, **kwargs):
        phone_number = kwargs.get('phone_number', '')
        users = UserLoginView.queryset.filter(phone_number=phone_number)
        user = users[0] if users else None
        if not user:
            return Response({"message": "wrong phone_number"})
        if not user.is_login(request):
            return Response({"message": "not logged in"})
            
        user_info = UserInfoDetailView.queryset.get(user=user)
        serializer = UserInfoSerializer(user_info)
        return Response(serializer.data)