def get_phone_number_from_request(request):
    return request.data.get("phone_number", "")


def get_password_from_request(request):
    return request.data.get("password", "")


def get_auth_number_from_request(request):
    return request.data.get("auth_number", "")
