from django.test import TestCase, Client
from rest_framework import status


TEST_PHONE_NUMBER = "01012341234"


class APIUserTests(TestCase):
    
    def do_user_info_get(self, client):
        curl = '''curl --location \
            --request GET "http://127.0.0.1:8000/api/user?phone_number=01025467722" \
            --data-raw ""'''
        data = {
            "phone_number": "01025467722"
        }
        response = client.get("/api/user", data=data, follow=True)
        print('>>do_user_info_get: ', response.status_code, response.data.get('detail'))
        return response
        
    def do_user_login(self, client):
        curl = '''curl --location \
                --request POST "http://127.0.0.1:8000/api/login/" \
                --header "Content-Type: application/json" \
                --data-raw "{
                \"phone_number\": \"01025467722\",
                \"password\": \"4321\"
                }"'''
        data = {
            "phone_number": "01025467722",
            "password": "1234"
        }
        response = client.post("/api/login/", data=data, follow=True)
        print('>>do_user_login: ', response.status_code, response.data.get('detail'))
        return response
    
    def do_user_login_with_wrong_password(self, client):
        curl = '''curl --location \
                --request POST "http://127.0.0.1:8000/api/login/" \
                --header "Content-Type: application/json" \
                --data-raw "{
                \"phone_number\": \"01025467722\",
                \"password\": \"4321\"
                }"'''
        data = {
            "phone_number": "01025467722",
            "password": "4321"
        }
        response = client.post("/api/login/", data=data, follow=True)
        print('>>do_user_login_with_wrong_password: ', response.status_code, response.data.get('detail'))
        return response
    
    def do_user_logout(self, client):
        curl = '''curl --location \
                --request POST "http://127.0.0.1:8000/api/logout/" \
                --header "Content-Type: application/json" \
                --data-raw "{
                \"phone_number\": \"01025467722\",
                \"password\": \"1234\"
                }"'''
        data = {
            "phone_number": "01025467722",
            "password": "1234"
        }
        response = client.post("/api/logout/", data=data, follow=True)
        print('>>do_user_logout: ', response.status_code, response.data.get('detail'))
        return response
    
    def do_user_signup(self, client):
        curl = '''curl --location \
                --request POST "http://127.0.0.1:8000/api/signup/" \
                --header "Content-Type: application/json" \
                --data-raw "{
                \"phone_number\": \"01025467722\",
                \"password\": \"1234\",
                \"email\": \"ablyproject@gmail.com\",
                \"nickname\": \"lazyer\",
                \"name\": \"123\"
                }"'''
        data = {
            "phone_number": "01025467722",
            "password": "1234",
            "email": "ablyproject@gmail.com",
            "nickname": "lazyer",
            "name": "KimInJu"
        }
        response = client.post("/api/signup/", data=data, follow=True)
        print('>>do_user_signup: ', response.status_code, response.data.get('detail'))
        return response
    
    def do_user_signup_wrong_email(self, client):
        curl = '''curl --location \
                --request POST "http://127.0.0.1:8000/api/signup/" \
                --header "Content-Type: application/json" \
                --data-raw "{
                \"phone_number\": \"01025467722\",
                \"password\": \"1234\",
                \"email\": \"www.ablyproject.com\",
                \"nickname\": \"lazyer\",
                \"name\": \"123\"
                }"'''
        data = {
            "phone_number": "01025467722",
            "password": "1234",
            "email": "www.ablyproject.com",
            "nickname": "lazyer",
            "name": "KimInJu"
        }
        response = client.post("/api/signup/", data=data, follow=True)
        print('>>do_user_signup: ', response.status_code, response.data.get('detail'))
        return response
    
    def do_user_signup_wrong_phone_number(self, client):
        curl = '''curl --location \
                --request POST "http://127.0.0.1:8000/api/signup/" \
                --header "Content-Type: application/json" \
                --data-raw "{
                \"phone_number\": \"ably\",
                \"password\": \"1234\",
                \"email\": \"ablyproject@gmail.com\",
                \"nickname\": \"lazyer\",
                \"name\": \"123\"
                }"'''
        data = {
            "phone_number": "ably",
            "password": "1234",
            "email": "ablyproject@gmail.com",
            "nickname": "lazyer",
            "name": "KimInJu"
        }
        response = client.post("/api/signup/", data=data, follow=True)
        print('>>do_user_signup: ', response.status_code, response.data.get('detail'))
        return response
    
    def do_user_auth(self, client):
        curl = '''curl --location --request POST "http://127.0.0.1:8000/api/auth/" \
                --header "Content-Type: application/json" \
                --data-raw "{
                \"phone_number\": \"01025467722\",
                \"auth_number\": \"0000\"
                }"'''
        data = {
            "phone_number": "01025467722",
            "auth_number": "0000"
        }
        response = client.post("/api/auth/", data=data, follow=True)
        print('>>do_user_auth: ', response.status_code, response.data.get('detail'))
        return response
        
    def test_case_1(self):
        doc = '''
        1. ????????? -> ??????????????? ?????? ????????? ????????? ?????? ??????
        2. ?????? ?????? -> ???????????? ?????? ????????? ????????? ?????? ??????
        '''
        print("\n[*]Scenario{}".format(doc))
        client = Client()
        res_login = self.do_user_login(client)
        res_get = self.do_user_info_get(client)
        assert res_login.status_code == status.HTTP_400_BAD_REQUEST
        assert res_get.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_case_2(self):
        doc = '''
        1. ????????????
        2. ????????????
        3. ?????????
        4. ????????????
        '''
        print("\n[*]Scenario{}".format(doc))
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
        1. ????????????
        2. ????????????
        3. ?????????
        4. ????????? -> ?????? ????????? ??????????????? ????????????
        '''
        print("\n[*]Scenario{}".format(doc))
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
        1. ????????????
        2. ????????????
        3. ?????????
        4. ????????????
        5. ???????????? -> ?????? ???????????? ??????????????? ????????????
        '''
        print("\n[*]Scenario{}".format(doc))
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
        1. ????????????
        2. ????????????
        3. ?????????(????????? ????????????) -> ??????????????? ??????????????? ????????????
        '''
        print("\n[*]Scenario{}".format(doc))
        client = Client()
        res_signup = self.do_user_signup(client)
        res_auth = self.do_user_auth(client)
        res_login = self.do_user_login_with_wrong_password(client)
        assert res_signup.status_code == status.HTTP_200_OK
        assert res_auth.status_code == status.HTTP_200_OK
        assert res_login.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_case_6(self):
        doc = '''
        1. ???????????? ??? ????????? ?????? email ??????
        '''
        print("\n[*]Scenario{}".format(doc))
        client = Client()
        req_signup = self.do_user_signup_wrong_email(client)
        assert req_signup.status_code == status.HTTP_400_BAD_REQUEST
        
    def test_case_7(self):
        doc = '''
        1. ???????????? ??? ????????? ?????? phone_number ??????
        '''
        print("\n[*]Scenario{}".format(doc))
        client = Client()
        req_signup = self.do_user_signup_wrong_phone_number(client)
        assert req_signup.status_code == status.HTTP_400_BAD_REQUEST

