from api.data.errors import AblyErrorServiceOK
from rest_framework.response import Response
from rest_framework import status


class ResponseHandler:
    '''
    Ablyproject 서비스 Response Handler
    '''
    def __init__(self):
        pass

    @staticmethod
    def response_success(self, ably_error=AblyErrorServiceOK()):
        return Response(
            data={
                "error_code": ably_error.info.code,
                "keyword": ably_error.info.keyword,
                "detail": ably_error.detail
            },
            status=status.HTTP_200_OK)
    
    @staticmethod
    def response_created(self, data, ably_error=AblyErrorServiceOK()):
        return Response(
            data={
                "error_code": ably_error.info.code,
                "keyword": ably_error.info.keyword,
                "detail": ably_error.detail,
                "data": data
            },
            status=status.HTTP_201_CREATED)
    
    @staticmethod
    def response_error(self, ably_error):
        return Response(
            data={
                "error_code": ably_error.info.code,
                "keyword": ably_error.info.keyword,
                "detail": ably_error.detail
            },
            status=status.HTTP_400_BAD_REQUEST)
