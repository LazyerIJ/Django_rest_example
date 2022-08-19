from django.test import TestCase, Client
from rest_framework import status


class APIUserTests(TestCase):
    
    def do_user_info_get(self, client):
        data = {
            "phone_number": "01012341234"
        }
        response = client.get("/api/user", data=data, follow=True)
        print('>>do_user_info_get: ', response.status_code, response.data.get('detail'))
        return response
        
    def do_user_login(self, client):
        data = {
            "phone_number": "01012341234",
            "password": "1234"
        }
        response = client.post("/api/login/", data=data, follow=True)
        print('>>do_user_login: ', response.status_code, response.data.get('detail'))
        return response
    
    def do_user_login_with_wrong_password(self, client):
        data = {
            "phone_number": "01012341234",
            "password": "4321"
        }
        response = client.post("/api/login/", data=data, follow=True)
        print('>>do_user_login_with_wrong_password: ', response.status_code, response.data.get('detail'))
        return response
    
    def do_user_logout(self, client):
        data = {
            "phone_number": "01012341234",
            "password": "1234"
        }
        response = client.post("/api/logout/", data=data, follow=True)
        print('>>do_user_logout: ', response.status_code, response.data.get('detail'))
        return response
    
    def do_user_signup(self, client):
        data = {
            "phone_number": "01012341234",
            "password": "1234",
            "email": "ablyproject@gmail.com",
            "nickname": "lazyer",
            "name": "홍길동"
        }
        response = client.post("/api/signup/", data=data, follow=True)
        print('>>do_user_signup: ', response.status_code, response.data.get('detail'))
        return response
    
    def do_user_auth(self, client):
        data = {
            "phone_number": "01012341234",
            "auth_number": "0000"
        }
        response = client.post("/api/auth/", data=data, follow=True)
        print('>>do_user_auth: ', response.status_code, response.data.get('detail'))
        return response
        
    def test_case_1(self):
        doc = '''
        1. 로그인 -> 회원가입을 하지 않았기 때문에 오류 발생
        2. 정보 확인 -> 로그인을 하지 않았기 때문에 오류 발생
        '''
        print("[*]{}".format(doc))
        client = Client()
        res_login = self.do_user_login(client)
        res_get = self.do_user_info_get(client)
        assert res_login.status_code == status.HTTP_400_BAD_REQUEST
        assert res_get.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_case_2(self):
        doc = '''
        1. 회원가입
        2. 문자인증
        3. 로그인
        4. 정보확인
        '''
        print("[*]{}".format(doc))
        client = Client()
        res_signup = self.do_user_signup(client)
        res_auth = self.do_user_auth(client)
        res_login = self.do_user_login(client)
        res_get = self.do_user_info_get(client)
        assert res_signup.status_code == status.HTTP_200_OK
        assert res_auth.status_code == status.HTTP_200_OK
        assert res_login.status_code == status.HTTP_200_OK
        assert res_get.status_code == status.HTTP_201_CREATED
    
    def test_case_3(self):
        doc = '''
        1. 회원가입
        2. 문자인증
        3. 로그인
        4. 로그인 -> 이미 로그인 하였으므로 오류발생
        '''
        print("[*]{}".format(doc))
        client = Client()
        res_signup = self.do_user_signup(client)
        res_auth = self.do_user_auth(client)
        res_login_1 = self.do_user_login(client)
        res_login_2 = self.do_user_login(client)
        assert res_signup.status_code == status.HTTP_200_OK
        assert res_auth.status_code == status.HTTP_200_OK
        assert res_login_1.status_code == status.HTTP_200_OK
        assert res_login_2.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_case_4(self):
        doc = '''
        1. 회원가입
        2. 문자인증
        3. 로그인
        4. 로그아웃
        5. 로그아웃 -> 이미 로그아웃 하였으므로 오류발생
        '''
        print("[*]{}".format(doc))
        client = Client()
        res_signup = self.do_user_signup(client)
        res_auth = self.do_user_auth(client)
        res_login = self.do_user_login(client)
        res_logout_1 = self.do_user_logout(client)
        res_logout_2 = self.do_user_logout(client)
        assert res_signup.status_code == status.HTTP_200_OK
        assert res_auth.status_code == status.HTTP_200_OK
        assert res_login.status_code == status.HTTP_200_OK
        assert res_logout_1.status_code == status.HTTP_200_OK
        assert res_logout_2.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_case_5(self):
        doc = '''
        1. 회원가입
        2. 문자인증
        3. 로그인(잘못된 패스워드) -> 패스워드가 틀렸으므로 오류발생
        '''
        print("[*]{}".format(doc))
        client = Client()
        res_signup = self.do_user_signup(client)
        res_auth = self.do_user_auth(client)
        res_login = self.do_user_login_with_wrong_password(client)
        assert res_signup.status_code == status.HTTP_200_OK
        assert res_auth.status_code == status.HTTP_200_OK
        assert res_login.status_code == status.HTTP_400_BAD_REQUEST