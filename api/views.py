from .models import UserInfo, UserAuth, UserLogin
from .serializers import UserInfoSerializer, UserLoginSerializer, UserSigninSerializer
from .handlers import sms_handler
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class UserSignupView(APIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserSigninSerializer

    def post(self, request, *args, **kwargs):
        # 입력 기본 정보 확인
        user_info_serializer = UserSigninSerializer(data=request.data)
        if not user_info_serializer.is_valid():
            return Response({"message": "FAIL"})

        user_login_serializer = UserLoginSerializer(data=request.data)
        if not user_login_serializer.is_valid():
            return Response({"message": "FAIL"})

        # need transaction
        user_info_serializer.save()
        user_login_serializer.save()

        # 문자 인증
        #phone_number = user_info_serializer.validated_data.get("phone_number")
        #user_auth, created = UserAuth.objects.update_or_create(phone_number=phone_number)
        #naver_sms_handler = sms_handler.NaverSMSHandler(user_auth.phone_number, user_auth.auth_number)
        #result = naver_sms_handler.send_sms()
        result = True
        if not result:
            return Response({"message": "FAIL"})

        return Response({"message": "TRUE"})

    def get(self, request, *args, **kwargs):
        phone_number = request.query_params['phone_number']
        #auth_number = request.query_params['auth_number']
        #result = UserAuth.check_auth_number(phone_number, auth_number)
        result = True
        if result:
            UserInfo.objects.filter(phone_number=phone_number).update(verified=True)
        return Response({
            'message': 'OK',
            'result': result
        })


class UserLoginView(APIView):
    queryset = UserLogin.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number", "")
        password = request.data.get("password", "")
        user = UserLogin.objects.filter(
            phone_number=phone_number
        )
        if user:
            if password == user[0].password:
                request.session[user[0].phone_number] = True
                return Response({"message": "TRUE"})
            return Response({"message": "not password"})
        return Response({"message": "not id"})


class UserInfoListView(generics.ListCreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    def get(self, request, *args, **kwargs):
        phone_number = request.query_params['phone_number']
        if request.session.get(phone_number, ""):
            return Response(UserInfo.objects.get(phone_number=phone_number))
        return Response({
            'message': 'FAIL',
        })


class UserInfoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
