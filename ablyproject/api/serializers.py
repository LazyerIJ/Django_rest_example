from rest_framework.serializers import ModelSerializer
from .models import UserInfo, UserAuth, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
    def validate(self, attrs):
        return attrs
    

class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = UserInfo
        fields = '__all__'
        
    def validate(self, attrs):
        return attrs
        

class UserAuthSerializer(ModelSerializer):
    class Meta:
        model = UserAuth
        fields = '__all__'
