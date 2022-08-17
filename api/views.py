from .models import User, UserAuth
from .serializers import UserSerializer
from .handlers import sms_handler
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response


class UserListMixins(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request)

    def post(self, request, *args, **kwargs):
        return self.create(request)


class UserDetailMixins(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrive(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class UserAuthDetail(APIView):

    def post(self, request, *args, **kwargs):
        p_num = request.data['phone_number']
        user_auth, updated = UserAuth.objects.update_or_create(phone_number=p_num)
        naver_sms_handler = sms_handler.NaverSMSHandler(user_auth.phone_number, user_auth.auth_number)
        result = naver_sms_handler.send_sms()
        print(result)
        return Response({'message': 'OK'})

    def get(self, request, *args, **kwargs):
        p_num = request.query_params['phone_number']
        a_num = request.query_params['auth_number']
        result = UserAuth.check_auth_number(p_num, a_num)
        return Response({'message': 'OK', 'result': result})
