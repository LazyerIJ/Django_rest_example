from rest_framework.serializers import ModelSerializer
from .models import UserInfo, UserAuth, User


class UserSerializer(ModelSerializer):
    '''
    사용자 로그인 정보 Serializer
    '''
    class Meta:
        model = User
        fields = '__all__'
        
    def validate(self, attrs):
        return attrs
    

class UserInfoSerializer(ModelSerializer):
    '''
    사용자 일반 정보 Serializer
    '''
    class Meta:
        model = UserInfo
        fields = '__all__'
        
    def validate(self, attrs):
        return attrs
        

class UserAuthSerializer(ModelSerializer):
    '''
    사용자 인증 정보 Serializer
    '''
    class Meta:
        model = UserAuth
        fields = '__all__'
