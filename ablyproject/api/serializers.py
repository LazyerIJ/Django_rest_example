from api.data import exceptions
from api.models import UserInfo, UserAuth, User
from api.handlers import validators
from rest_framework.serializers import ModelSerializer


def update_fields_error_message(serializer):
    for key in serializer.fields.keys():
        field = serializer.fields[key]
        field.error_messages = exceptions.get_field_message_dict(key)
        

class UserSerializer(ModelSerializer):
    '''
    사용자 로그인 정보 Serializer
    '''
    class Meta:
        model = User
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        update_fields_error_message(self)
        
    def validate(self, attrs):
        attr = "phone_number"
        attrs[attr] = validators.validate_phone_number(attrs.get("phone_number", ""))
        return attrs
    

class UserInfoSerializer(ModelSerializer):
    '''
    사용자 일반 정보 Serializer
    '''
    class Meta:
        model = UserInfo
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(UserInfoSerializer, self).__init__(*args, **kwargs)
        update_fields_error_message(self)
        
    def validate(self, attrs):
        return attrs
        

class UserAuthSerializer(ModelSerializer):
    '''
    사용자 인증 정보 Serializer
    '''
    class Meta:
        model = UserAuth
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(UserAuthSerializer, self).__init__(*args, **kwargs)
        update_fields_error_message(self)

    def validate(self, attrs):
        attr = "phone_number"
        attrs[attr] = validators.validate_phone_number(attrs.get("phone_number", ""))
        return attrs
