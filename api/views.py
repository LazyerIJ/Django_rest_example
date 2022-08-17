from .models import UserInfo, UserAuth, UserLogin
from .serializers import UserInfoSerializer, UserLoginSerializer, UserSigninSerializer
from .handlers import sms_handler
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response


class UserAuthDetail(APIView):

    def post(self, request, *args, **kwargs):
        p_num = request.data['phone_number']
        user_auth, created = UserAuth.objects.update_or_create(phone_number=p_num)
        naver_sms_handler = sms_handler.NaverSMSHandler(user_auth.phone_number, user_auth.auth_number)
        result = naver_sms_handler.send_sms()
        return Response({
            'message': 'OK',
            'auth_number': user_auth.auth_number,
            'created': created,
            'result': result.status_code,
            'result.text': result.text
            })

    def get(self, request, *args, **kwargs):
        p_num = request.query_params['phone_number']
        a_num = request.query_params['auth_number']
        result = UserAuth.check_auth_number(p_num, a_num)
        return Response({
            'message': 'OK',
            'result': result
            })


class UserSigninView(APIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserSigninSerializer

    def get(self, request, *args, **kwargs):
        return {} 

    def post(self, request, *args, **kwargs):
        return {} 
    
    
class UserLoginView(APIView):
    queryset = UserLogin.objects.all()
    serializer_class = UserLoginSerializer

    def get(self, request, *args, **kwargs):
        return {} 

    def post(self, request, *args, **kwargs):
        return {} 
    

class UserInfoListView(generics.ListCreateAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer


class UserInfoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer


    