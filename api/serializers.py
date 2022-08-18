from rest_framework.serializers import ModelSerializer
from .models import UserInfo, UserLogin, UserAuth


class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'

        
class UserSigninSerializer(ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'


class UserAuthSerializer(ModelSerializer):
    class Meta:
        model = UserAuth
        fields = '__all__'
        
        
class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = UserLogin
        fields = '__all__'
