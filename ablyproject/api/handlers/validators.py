from api.data import errors, exceptions
from rest_framework import serializers as rf_serializers


def validate_and_raise_exception(serializer, data):
    serializer_obj = serializer(data=data)
    if not serializer_obj.is_valid():
        value, code = exceptions.get_value_code_from_serializer(serializer_obj)
        raise rf_serializers.ValidationError(detail=value, code=code)


def validate_phone_number(phone_number):
    if not phone_number:
        raise rf_serializers.ValidationError(detail="phone_number", code="ably_required")
        
    phone_number = phone_number.replace("-", "")
    if not phone_number:
        raise rf_serializers.ValidationError(detail="phone_number", code="ably_invalid")
    
    if not phone_number.isdigit():
        raise rf_serializers.ValidationError(detail="phone_number", code="ably_invalid")
    return phone_number
