from django.db import transaction
from rest_framework.views import APIView

from api.data import errors
from api.models import User, UserInfo, UserAuth
from api.handlers import request_parser as req_parser
from api.handlers.sms_handler import NaverSMSHandler
from api.handlers.response_handler import ResponseHandler
from api.serializers import UserInfoSerializer, UserSerializer, UserAuthSerializer


class UserSignupView(APIView):
    '''
    사용자 회원가입 및 비밀번호 재설정을 담당합니다.
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        '''
        사용자 회원가입
        '''
        phone_number = req_parser.get_phone_number_from_request(request)
        
        # phone_number 중복 체크 
        is_exists, _ = User.is_exists_phone_number(phone_number)
        if is_exists:
            error = errors.AblyErrorUserDuplicated()
            return ResponseHandler.response_error(error)
        
        # request -> 사용자 로그인 정보 검증 
        user_serializer = UserSerializer(data=request.data) 
        if not user_serializer.is_valid():
            error = errors.AblyErrorInvalidInput(params="")
            return ResponseHandler.response_error(error)

        # request -> 사용자 일반 정보 검증
        user_info_serializer = UserInfoSerializer(data=request.data) 
        if not user_info_serializer.is_valid():
            error = errors.AblyErrorInvalidInput(params="")
            return ResponseHandler.response_error(error)
    
        # 사용자 로그인 정보 및 일반 정보 저장 
        user = User.objects.create_user(**user_serializer.data)
        user_info_serializer.validated_data['user'] = user
        user_info_serializer.save()

        # 인증 문자 발송
        validated_phone_number = user_serializer.validated_data.get("phone_number")
        user_auth, _ = UserAuth.objects.update_or_create(phone_number=validated_phone_number)
        naver_sms_handler = NaverSMSHandler(user_auth.phone_number, user_auth.auth_number)
        
        # 인증 문자 발송 결과 반환 
        result = naver_sms_handler.send_sms()
        if not result:
            error = errors.AblyErrorSMSSendFail()
            return ResponseHandler.response_error(error)

        error = errors.AblyErrorSMSSendSuccess()
        return ResponseHandler.response_success(error)
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        '''
        사용자 비밀번호 재설정
        '''
        phone_number = req_parser.get_phone_number_from_request(request)
        password = req_parser.get_password_from_request(request)
        
        # 사용자 확인 
        is_exists, user = User.is_exists_phone_number(phone_number)
        if not is_exists:
            error = errors.AblyErrorUserNotExists()
            return ResponseHandler.response_error(error)
        
        # 비밀번호 재설정 
        user.set_password(password)
        user.verified = False
        user.save()
        
        # 인증 문자 발송
        user_auth, _ = UserAuth.objects.update_or_create(phone_number=phone_number)
        naver_sms_handler = NaverSMSHandler(user_auth.phone_number, user_auth.auth_number)
        
        result = naver_sms_handler.send_sms()
        if not result:
            error = errors.AblyErrorSMSSendFail()
            return ResponseHandler.response_error(error)
        
        error = errors.AblyErrorSMSSendSuccess()
        return ResponseHandler.response_success(error)
        
        
class UserAuthView(APIView):
    '''
    사용자 회원가입 및 비밀번호 재설정에 따른 문자 인증을 담당합니다.
    '''
    queryset = UserAuth.objects.all()
    serializer_class = UserAuthSerializer
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        '''
        인증 문자 확인
        '''
        
        phone_number = req_parser.get_phone_number_from_request(request)
        auth_number = req_parser.get_auth_number_from_request(request)
        
        # phone_number ,auth_number 일치 확인 
        result = UserAuth.check_auth_number(phone_number, auth_number)
        
        # 미일치 시 에러 반환
        if not result:
            error = errors.AblyErrorSMSAuthFail()
            return ResponseHandler.response_error(error)
        
        # 일치 시 사용자 로그인 정보의 verified를 True로 업데이트 
        is_exists, user = User.is_exists_phone_number(phone_number)
        if is_exists:
            user[0].verified = True
            user[0].save()
            
        error = errors.AblyErrorSMSAuthSuccess()
        return ResponseHandler.response_success(error)


class UserLoginView(APIView):
    '''
    사용자 로그인을 담당합니다
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        '''
        사용자 로그인
        '''
        phone_number = req_parser.get_phone_number_from_request(request)
        password = req_parser.get_password_from_request(request)
        
        # phone_number 존재 확인 
        is_exists, user = User.is_exists_phone_number(phone_number)
        if not is_exists:
            error = errors.AblyErrorInvalidInput(param="phone_number")
            return ResponseHandler.response_error(error)
        
        # password 일치 확인 
        if not user.check_password(password):
            error = errors.AblyErrorInvalidInput(param="password")
            return ResponseHandler.response_error(error)
        
        # 문자 인증 정보 확인 
        if not user.verified:
            error = errors.AblyErrorSMSAuthNeeded()
            return ResponseHandler.response_error(error)
        
        # 이미 로그인 되어있는지 확인 
        if user.is_login(request):
            error = errors.AblyErrorAlreadyLogin()
            return ResponseHandler.response_error(error)
        
        # 로그인 수행 
        user.login(request)
        error = errors.AblyErrorLogoutSuccess()
        return ResponseHandler.response_success(error)
    
    
class UserLogoutView(APIView):
    '''
    사용자 로그아웃을 담당합니다
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer 

    def post(self, request, *args, **kwargs):
        '''
        사용자 로그아웃
        '''
        phone_number = req_parser.get_phone_number_from_request(request)
        password = req_parser.get_password_from_request(request)
        
        # phone_number 존재 확인 
        is_exists, user = User.is_exists_phone_number(phone_number)
        if not is_exists:
            error = errors.AblyErrorInvalidInput(params="phone_number")
            return ResponseHandler.response_error(error)
        
        # 비밀번호 일치 확인 
        if not user.check_password(password):
            error = errors.AblyErrorInvalidInput(params="password")
            return ResponseHandler.response_error(error)
        
        # 로그인 여부 확인 
        if not user.is_login(request):
            error = errors.AblyErrorAlreadyLogout() 
            return ResponseHandler.response_error(error)
        
        # 로그아웃 진행 
        user.logout(request)
        error = errors.AblyErrorLogoutSuccess()
        return ResponseHandler.response_success(error)


class UserInfoDetailView(APIView):
    '''
    사용자 정보 확인을 담당합니다.
    '''
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer

    @transaction.atomic
    def get(self, request, *args, **kwargs):
        '''
        사용자 정보 확인
        '''
        phone_number = req_parser.get_phone_number_from_request(request)
        
        # phone_number 존재 확인 
        is_exists, user = User.is_exists_phone_number(phone_number)
        if not is_exists:
            error = errors.AblyErrorInvalidInput("phone_number")
            return ResponseHandler.response_error(error)
        
        # 로그인 여부 확인 
        if not user.is_login(request):
            error = errors.AblyErrorNeedLogin()
            return ResponseHandler.response_error(error)
        
        # 사용자 정보 반환 
        user_info = UserInfoDetailView.queryset.get(user=user)
        serializer = UserInfoSerializer(user_info)
        error = errors.AblyErrorServiceOK()
        return ResponseHandler.response_created(data=serializer.data, error=error)
