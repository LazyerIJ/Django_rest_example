import abc


class AblyErrorInfo:
    def __init__(self, code, keyword):
        self.code = code
        self.keyword = keyword


class AblyError:
    def __init__(self, params=None):
        self.params = params
        
    @property
    @abc.abstractmethod
    def info(self):
        raise NotImplementedError
    
        
class AblyErrorServiceOK(AblyError):
    info = AblyErrorInfo(
        code="100000", 
        keyword="ABLY_ERROR_SERVICE_OK"
    )
    
    def __init__(self, params=None):
        super().__init__(params)
        self.detail = "요청하신 작업이 정상수행 되었습니다."
        
        
class AblyErrorUserDuplicated(AblyError):
    info = AblyErrorInfo(
        code="100001", 
        keyword="ABLY_ERROR_DUPLICATED_USER"
    )
    
    def __init__(self, params=None):
        super().__init__(params)
        self.detail = "이미 존재하는 사용자입니다."
        
        
class AblyErrorInvalidInput(AblyError):
    info = AblyErrorInfo(
        code="100002", 
        keyword="ABLY_ERROR_INVALID_INPUT"
    )
    
    def __init__(self, params=None):
        super().__init__(params)
        self.detail = "올바르지 않은 값이 입력되었습니다.({})".format(params)
        
        
class AblyErrorUserNotExists(AblyError):
    info = AblyErrorInfo(
        code="100003", 
        keyword="ABLY_ERROR_USER_NOT_EXISTS"
    )
    
    def __init__(self, params=None):
        super().__init__(params)
        self.detail = "존재하지 않는 사용자입니다."
        
        
class AblyErrorLoginSuccess(AblyError):
    info = AblyErrorInfo(
        code="101001", 
        keyword="ABLY_ERROR_LOGIN_SUCCESS"
    )
    
    def __init__(self, params=None):
        super().__init__(params)
        self.detail = "로그인에 성공하였습니다."
        
        
class AblyErrorLogoutSuccess(AblyError):
    info = AblyErrorInfo(
        code="101002", 
        keyword="ABLY_ERROR_LOGOUT_SUCCESS"
    )
    
    def __init__(self, params=None):
        super().__init__(params)
        self.detail = "로그아웃에 성공하였습니다."
        
        
class AblyErrorAlreadyLogin(AblyError):
    info = AblyErrorInfo(
        code="101003", 
        keyword="ABLY_ERROR_ALREADY_LOGIN"
    )
    
    def __init__(self, params=None):
        super().__init__(params)
        self.detail = "이미 로그인되어 있습니다."
        
        
class AblyErrorAlreadyLogout(AblyError):
    info = AblyErrorInfo(
        code="101004", 
        keyword="ABLY_ERROR_ALREADY_LOGOUT"
    )
    
    def __init__(self, params=None):
        super().__init__(params)
        self.detail = "이미 로그아웃되어 있습니다."
        
        
class AblyErrorNeedLogin(AblyError):
    info = AblyErrorInfo(
        code="101002", 
        keyword="ABLY_ERROR_NEED_LOGIN"
    )
    
    def __init__(self, params=None):
        super().__init__(params)
        self.detail = "로그인이 필요합니다."

        
class AblyErrorSMSSendFail(AblyError):
    info = AblyErrorInfo(
        code="102001", 
        keyword="ABLY_ERROR_SMS_SEND_FAIL"
    )
    
    def __init__(self, params=None):
        super().__init__(params)
        self.detail = "SMS 인증문자 발송에 실패하였습니다."
       
        
class AblyErrorSMSSendSuccess(AblyError):
    info = AblyErrorInfo(
        code="102002", 
        keyword="ABLY_ERROR_SMS_SEND_SUCCESS"
    )
    
    def __init__(self, params=None):
        super().__init__(params)
        self.detail = "SMS 인증문자 발송에 성공하였습니다."
        
        
class AblyErrorSMSAuthFail(AblyError):
    info = AblyErrorInfo(
        code="102003", 
        keyword="ABLY_ERROR_SMS_AUTH_FAIL"
    )
    
    def __init__(self, params=None):
        super().__init__(params)
        self.detail = "SMS 인증에 실패하였습니다."
        
        
class AblyErrorSMSAuthSuccess(AblyError):
    info = AblyErrorInfo(
        code="102003", 
        keyword="ABLY_ERROR_SMS_AUTH_SUCCESS"
    )
    
    def __init__(self, params=None):
        super().__init__(params)
        self.detail = "SMS 인증에 성공하였습니다."