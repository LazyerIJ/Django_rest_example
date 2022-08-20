from api.data import errors


def get_ably_error_required_input(parameter):
    return errors.AblyErrorRequireInput(parameter)


def get_ably_error_invalid_input(parameter): 
    return errors.AblyErrorInvalidInput(parameter)


def get_ably_error_inavlid_dtype(parameter):
    return errors.AblyErrorInvalidDtype(parameter)


def get_ably_error_max_length_data(parameter):
    return errors.AblyErrorMaxLengthData(parameter)


def get_ably_error_exception(parameter):
    return errors.AblyErrorException(parameter)


ERROR_STR_CODE_INSTANCE_DICT = {
    "required": get_ably_error_required_input,
    "invalid": get_ably_error_invalid_input,
    "dtype": get_ably_error_inavlid_dtype,
    "max_length": get_ably_error_max_length_data,
}


def get_field_message_dict(parameter):
    error_message = {
        "required": parameter,
        "null": parameter,
        "invalid": parameter,
        "blank": parameter,
    }
    return error_message


def get_value_code_from_serializer(serializer):
    serializer_errors = serializer.errors
    code = list(serializer_errors.values())[0][0].code
    value = list(serializer_errors.keys())[0]
    if code.startswith("ably_"):
        code = code.replace("ably_", "")
        value = list(serializer_errors.values())[0][0]
    return str(value), code


def get_error_instance_from_code(code):
    error = ERROR_STR_CODE_INSTANCE_DICT.get(code)
    if error:
        return error
    return get_ably_error_exception


def transform_serializer_error_to_ablyerror(serializer):
    value, code = get_value_code_from_serializer(serializer)
    error = get_error_instance_from_code(code)(value)
    return error
